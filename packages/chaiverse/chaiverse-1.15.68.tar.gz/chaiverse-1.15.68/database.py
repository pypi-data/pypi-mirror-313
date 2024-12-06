from collections import defaultdict
from functools import reduce, partial
import json
from operator import getitem
from typing import Optional

import firebase_admin
import firebase_admin.db
from flatten_dict import flatten, unflatten
from pydantic.utils import deep_update


class _FirebaseDatabase:
    def __init__(self, credentials_file: str, url: str):
        self.credentials_file = credentials_file
        self.url = url
        self._initialize_firebase()

    def reference(self, path: str):
        return firebase_admin.db.reference(path, app=self.app)

    def get(self, path: str, shallow: bool = False):
        firebase_reference = self.reference(path)
        record = firebase_reference.get(shallow=shallow)
        return record

    def is_in_database(self, path: str):
        value = self.get(path, shallow=True)
        return value is not None

    def set(self, path: str, value):
        firebase_reference = self.reference(path)
        value = serialise_input(value)
        firebase_reference.set(value)

    def update(self, path: str, record: dict):
        firebase_reference = self.reference(path)
        record = serialise_input(record)
        firebase_reference.update(record)

    def multi_update(self, path: str, record: dict):
        # While the logic for this function is the same as update, the intended
        # use-case is different due to the different syntax for multi-path
        # updates
        # See https://firebase.google.com/docs/database/admin/save-data#section-update
        record = flatten(record, reducer="path")
        self.update(path, record)

    def where(self, path, **kwargs):
        firebase_reference = self.reference(path)
        assert len(kwargs) > 0, "No query provided!"
        field_name, field_value = list(kwargs.items())[0]
        record = firebase_reference.order_by_child(field_name).equal_to(field_value).get()
        # Firebase doesn't support querying on multiple keys, so have to
        # filter the further keys here
        records = list(record.values())
        if len(kwargs) > 1:
            records = filter_records(records, kwargs)
        return records

    def remove(self, path):
        assert path not in ["", "/"]
        self.reference(path).delete()

    def query_by_key_range(self, path, start_at=None, end_at=None, limit_to_first: Optional[int] = None, limit_to_last: Optional[int] = None):
        firebase_reference = self.reference(path)
        query = firebase_reference.order_by_key()
        query = self._range_query_modifier(query, start_at, end_at, limit_to_first, limit_to_last)
        result = query.get()
        return result

    def query_by_child_value_range(self, path, by, start_at=None, end_at=None, limit_to_first: Optional[int] = None, limit_to_last: Optional[int] = None):
        firebase_reference = self.reference(path)
        query = firebase_reference.order_by_child(by)
        query = self._range_query_modifier(query, start_at, end_at, limit_to_first, limit_to_last)
        result = query.get()
        return result

    def atomic_add(self, path: str, value: float):
        func = partial(add, y=value)
        self.atomic_set(path, func)

    def atomic_increment(self, path: str):
        self.atomic_set(path, incrementer)

    def atomic_decrement(self, path: str):
        self.atomic_set(path, decrementer)

    def atomic_set(self, path: str, operation: callable):
        """Atomic version of set to avoid write clashes"""
        firebase_reference = self.reference(path)
        firebase_reference.transaction(operation)

    def _initialize_firebase(self):
        name = self.__class__.__name__
        try:
            credentials = firebase_admin.credentials.Certificate(self.credentials_file)
            init_params = {"databaseURL": self.url}
            self.app = firebase_admin.initialize_app(credentials, init_params, name=name)
        except ValueError:
            self.app = firebase_admin.get_app(name=name)

    def _range_query_modifier(self, query, start_at, end_at, limit_to_first, limit_to_last):
        if start_at:
            query = query.start_at(start_at)
        if end_at:
            query = query.end_at(end_at)
        if limit_to_first:
            query = query.limit_to_first(limit_to_first)
        if limit_to_last:
            query = query.limit_to_last(limit_to_last)
        return query


def serialise_input(record: dict):
    json_string = json.dumps(record, default=str)
    serialised_record = json.loads(json_string)
    return serialised_record


def add(x, y):
    return x + y


def incrementer(x):
    """Separate to make testable"""
    x = x if x else 0
    return x + 1


def decrementer(x):
    """Separate to make testable"""
    x = x if x else 0
    return x - 1


def filter_records(records, filters):
    filtered_records = []
    for record in records:
        # If filters is a subset of the record, then its good
        if filters.items() <= record.items():
            filtered_records.append(record)
    return filtered_records


class MockDatabase():
    def __init__(self):
        nested_dict = lambda: defaultdict(nested_dict)
        self.store = nested_dict()

    def get(self, path: str, shallow=False):
        keys = self._get_keys(path)
        record = self._get_from_store(keys) or {}
        if shallow:
            record = {key: True for key, _ in record.items()}
        record = None if record in [{}, []] else record
        return record

    def is_in_database(self, path: str):
        keys = self._get_keys(path)
        is_in = self._is_in_store(keys)
        record = None
        if is_in:
            record = self.get(path)
        return record is not None

    def set(self, path: str, value: dict):
        keys = self._get_keys(path)
        value = serialise_input(value)
        value = dict_to_default_dict(value)
        self._set_in_store(keys, value)

    def update(self, path: str, record: dict):
        keys = self._get_keys(path)
        record = serialise_input(record)
        record = dict_to_default_dict(record)
        for record_keys, value in record.items():
            self._update_in_store(keys + record_keys.split('/'), value)

    def multi_update(self, path: str, record: dict):
        record = unflatten(record, splitter="path")
        self.update(path, record)

    def where(self, path, **kwargs):
        keys = self._get_keys(path)
        records = self._get_from_store(keys) or {}
        records = list(records.values())
        records = filter_records(records, kwargs)
        return records

    def _remove_recursively(self, keys, current_node, current_index):
        key = keys[current_index]
        if key in current_node:
            if current_index == len(keys) - 1:
                current_node.pop(key)
            else:
                self._remove_recursively(keys, current_node[key], current_index + 1)
                if len(current_node[key]) == 0:
                    current_node.pop(key)

    def remove(self, path: str):
        keys = self._get_keys(path)
        self._remove_recursively(keys, self.store, 0)

    def query_by_key_range(self, path, start_at=None, end_at=None, limit_to_first: Optional[int] = None, limit_to_last: Optional[int] = None):
        if limit_to_first and limit_to_last:
            raise ValueError('Cannot set both first and last limits.')
        keys = self._get_keys(path)
        records = self._get_from_store(keys) or {}
        record_tuples = list(records.items())
        key_func = lambda tuple: tuple[0]
        record_tuples = self._range_query_modifier(record_tuples, start_at, end_at, limit_to_first, limit_to_last, key_func=key_func)
        records = {key: value for key, value in record_tuples} or None
        return records

    def query_by_child_value_range(self, path, by, start_at=None, end_at=None, limit_to_first: Optional[int] = None, limit_to_last: Optional[int] = None):
        if limit_to_first and limit_to_last:
            raise ValueError('Cannot set both first and last limits.')
        keys = self._get_keys(path)
        records = self._get_from_store(keys) or {}
        record_tuples = list(records.items())
        key_func = lambda tuple: tuple[1].get(by)
        record_tuples = self._range_query_modifier(record_tuples, start_at, end_at, limit_to_first, limit_to_last, key_func=key_func)
        records = {key: value for key, value in record_tuples} or None
        return records

    def _range_query_modifier(self, record_tuples, start_at, end_at, limit_to_first, limit_to_last, key_func):
        record_tuples = sorted(record_tuples, key=key_func)
        record_tuples = [
            record_tuple for record_tuple in record_tuples
            if (not start_at or key_func(record_tuple) >= start_at) and (not end_at or key_func(record_tuple) <= end_at)
        ]
        if limit_to_first:
            record_tuples = record_tuples[:limit_to_first]
        if limit_to_last:
            record_tuples = record_tuples[-limit_to_last:]
        return record_tuples

    def atomic_add(self, path: str, value: float):
        func = partial(add, y=value)
        self.atomic_set(path, func)

    def atomic_increment(self, path: str):
        self.atomic_set(path, incrementer)

    def atomic_decrement(self, path: str):
        self.atomic_set(path, decrementer)

    def atomic_set(self, path, operation: callable):
        value = self.get(path)
        value = operation(value)
        self.set(path, value)

    @staticmethod
    def _get_keys(path: str):
        path = path.lstrip("/")
        path = path.rstrip("/")
        keys = path.split("/")
        # To avoid using emptystring as key when
        # interfacing with root leaf
        keys = keys if keys != [""] else []
        return keys

    def _get_from_store(self, keys):
        node = self.store
        for key in keys:
            if key not in node:
                node = None
                break
            node = node[key]
        return node

    def _is_in_store(self, keys):
        node = self.store
        is_in = True
        for key in keys:
            if key not in node:
                is_in = False
                break
            node = node[key]
        return is_in

    def _get_or_create_from_store(self, keys):
        return reduce(getitem, keys, self.store) if keys else self.store

    def _set_in_store(self, keys, value):
        _raise_for_disallowed_key(keys)
        _raise_for_disallowed_key(value)
        if keys:
            self._get_or_create_from_store(keys[:-1])[keys[-1]] = value
        else:
            self.store = value

    def _update_in_store(self, keys, value):
        current_value = self._get_or_create_from_store(keys[:-1]) or {}
        current_value = current_value.get(keys[-1])
        # Updating is only relevant if both stored value and new value are
        # dicts
        if isinstance(current_value, dict) and isinstance(value, dict):
            value = deep_update(current_value, value)
        self._set_in_store(keys, value)

    @property
    def nested_default_dict(self):
        # To make it easy to do self.store["some"]["key"] without raising
        # KeyError
        return defaultdict(self.nested_default_dict)


def _raise_for_disallowed_key(obj):
    disallowed_keys = [".", "$", "#", "[", "]", "/"]
    if isinstance(obj, str):
        msg = f"Key {obj} contains disallowed character!"
        assert not any(disallowed in obj for disallowed in disallowed_keys), msg
    elif isinstance(obj, list):
        [_raise_for_disallowed_key(key) for key in obj]
    elif isinstance(obj, dict):
        [_raise_for_disallowed_key(key) for key in obj.keys()]
        [
            _raise_for_disallowed_key(value) for value in obj.values()
            if isinstance(value, dict)
        ]


def _string_is_disallowed(string):
    disallowed_keys = [".", "$", "#", "[", "]", "/"]
    return any(disallowed in string for disallowed in disallowed_keys)


def dict_to_default_dict(d):
    if isinstance(d, dict):
        nested_dict = lambda: defaultdict(nested_dict)
        d = defaultdict(nested_dict, {k: dict_to_default_dict(v) for k, v in d.items()})
    return d
