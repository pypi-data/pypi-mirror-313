from collections import defaultdict
from collections.abc import Iterable
from contextlib import contextmanager
from datetime import datetime
from dill.source import getsource
from inspect import isclass
import logging
from typing import Callable, ClassVar, Dict, List, Optional, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, validate_model, parse_obj_as, validator
from pydantic.error_wrappers import ValidationError
from pydantic.main import object_setattr, ModelMetaclass
from pytz import UTC

from chaiverse.chaiverse_secrets import scrub_secrets
from chaiverse.database import _FirebaseDatabase
from chaiverse.lib.func import deserialize_function
from chaiverse.lib.func import is_base_64


class class_property(property):
    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


class InfernoLogEntry(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    entry: str
    level: str
    line_number: int
    path: str

    @staticmethod
    def from_logging_record(record: logging.LogRecord):
        entry = str(scrub_secrets(record.msg))
        log_entry = InfernoLogEntry(
            timestamp=datetime.utcfromtimestamp(record.created).replace(tzinfo=UTC),
            entry=entry,
            level=record.levelname,
            line_number=record.lineno,
            path=record.pathname
        )
        return log_entry


class InfernoModel(BaseModel):
    """
    Inferno is a light-weight object relational-mapper (ORM/ODM)
    for Firebase. It maps records in the database to python
    objects to ensure type-safety, validation and encourage
    cleaner coding standards when interfacing with the database.
    """
    database: ClassVar[_FirebaseDatabase]
    path: ClassVar[str]

    logs: Optional[List[InfernoLogEntry]]

    @class_property
    def lazy(cls):
        # Mixin lazy behaviour into base class
        lazy_class = type(f"Lazy{cls.__name__}", (LazyInfernoModelMixin, cls), {})
        return lazy_class

    @classmethod
    def create(cls, **kwargs):
        data = cls(**kwargs)
        msg = f'entry with id "{data.id}" already exists in database! Please use a different id'
        assert not cls.is_in_database(**{cls._id: data.id}), msg
        return data

    @classmethod
    def from_id(cls, default=None, **kwargs):
        instance_id = cls._get_instance_id(kwargs)
        data = cls.database.get(path=f'{cls.path}/{instance_id}') or default
        assert data is not None, f'no entry with id "{instance_id}" found on database!'
        return cls(**data)

    @classmethod
    def from_records(cls, records):
        instances = []
        for record in records:
            try:
                instance = cls(**record)
                instances.append(instance)
            except ValidationError:
                pass
        return instances

    @classmethod
    def where(cls, **kwargs):
        records = cls.database.where(path=cls.path, **kwargs)
        return cls.from_records(records)

    @classmethod
    def all(cls, **kwargs):
        all_entries = cls.database.get(path=cls.path)
        all_records = all_entries.values() if all_entries else []
        return cls.from_records(all_records)

    @classmethod
    def paginate(cls, index, limit):
        # Paginate (in reverse order) an Inferno model with a sortable id
        entries = cls.database.query_by_child_value_range(cls.path, cls._id, end_at=index, limit_to_last=limit)
        entries = cls.from_records(entries.values()) if entries else []
        entries.sort(key=lambda x: getattr(x, cls._id), reverse=True)
        return entries

    @classmethod
    def is_in_database(cls, **kwargs):
        instance_id = cls._get_instance_id(kwargs)
        is_in = cls.database.is_in_database(path=f'{cls.path}/{instance_id}')
        return is_in

    def to_dict(self, **kwargs):
        serialised_record = jsonable_encoder(self, **kwargs)
        return serialised_record

    def to_lazy(self):
        kwargs = {self.__class__._id: self.id}
        lazy_model = self.lazy.from_id(**kwargs)
        return lazy_model

    @contextmanager
    def register_logger(self):
        handler = InfernoLoggerHandler(inferno_model=self, level=logging.DEBUG)
        try:
            root_logger = logging.getLogger()
            root_logger.addHandler(handler)
            yield
        finally:
            root_logger.removeHandler(handler)

    def save(self):
        record = self._build_save_record()
        self.database.multi_update(path="/", record=record)

    def dict(self, *args, **kwargs):
        # So that FastAPI doesn't include null values in response
        kwargs["exclude_none"] = True
        return BaseModel.dict(self, *args, **kwargs)

    @property
    def id(self):
        id_field = self.__class__._id
        instance_id = getattr(self, id_field)
        return instance_id

    @classmethod
    def _get_denormalised_fields(cls):
        # Cannot set this as a Pydantic ClassVar as it gets shared across all
        # InfernoModel instances
        denormalised_fields = getattr(cls, "_denormalised_fields", {})
        return denormalised_fields

    @classmethod
    def _get_instance_id(cls, kwargs):
        assert cls._id in kwargs, f'invalid keyword id, please use keyword "{cls._id}"'
        instance_id = kwargs[cls._id]
        return instance_id

    def _build_save_record(self):
        record = {self.path: {self.id: self.to_dict()}}
        for field, path in self._get_denormalised_fields().items():
            denormalised_record = {path: {self.id: self.to_dict(include=[self._id, field])}}
            record.update(denormalised_record)
        return record


class LazyInfernoModelMixin():

    @classmethod
    def construct(cls, **kwargs):
        # Build pydantic model without validation
        instance = cls.__new__(cls)
        # Initialize pydantic private attributes
        object_setattr(instance, '__fields_set__', set())
        instance._init_private_attributes()
        for field, value in kwargs.items():
            instance._set_field(field, value)
        return instance

    @classmethod
    def from_id(cls, **kwargs):
        assert cls._id in kwargs, f'invalid keyword id, please use keyword "{cls._id}"'
        instance = cls.construct()
        instance_id = kwargs[cls._id]
        instance._set_field(cls._id, instance_id)
        return instance

    @classmethod
    def where(cls, **kwargs):
        assert len(kwargs) == 1, "Cannot perform a lazy where on more than one field!"
        field = list(kwargs.keys())[0]
        assert field in cls._get_denormalised_fields(), f"Cannot perform a lazy where on the field `{field}` as it has not been denormalised!"
        denormalised_path = cls._denormalised_fields[field]
        records = cls.database.where(path=denormalised_path, **kwargs)
        return [cls.construct(**data) for data in records]

    def _set_field(self, field, value):
        data = {field: value}
        values, _, validation_error = validate_model(self.__class__, data)
        if field not in values.keys():
            validation_error = _get_pydantic_errors_for_field(validation_error, field)
            raise validation_error
        object_setattr(self, field, value)

    def __getattribute__(self, field):
        value = super().__getattribute__(field)
        # Have to redirect to database if None as optional fields are
        # instantiated with None (and therefore have a value)
        if value is None and field in self.__fields__:
            value = self.__getattr__(field)
        return value

    def __getattr__(self, field):
        if field in self.__fields__:
            value = self.database.get(f"{self.path}/{self.id}/{field}")
            self._set_field(field, value)
        else:
            value = super().__getattribute__(field)
        return value


def get_source(function):
    source = getattr(function, "__source__", None) or getsource(function)
    source = source.lstrip()
    return source


class InfernoCallableMixin(BaseModel):
    ### Mixin to support callable objects in Inferno
    ### WARNING: This is a potential security issue
    ###          as there is a bare exec. Do not expose
    ###          unauthenticated access to Inferno callables.
    ###          This is a Mixin to ensure developer opts-in to
    ###          unsafe behaviour.

    class Config:
        json_encoders = {
            Callable: get_source
        }

    @validator("*", pre=True)
    def validate_callable(cls, v, field):
        if field.type_ != Callable:
            return v

        if type(v) == list:
            v = [InfernoCallableMixin.process_callable(func) for func in v]
        else:
            v = InfernoCallableMixin.process_callable(v)
        return v

    @staticmethod
    def process_callable(func):
        if type(func) == str and is_base_64(func):
            func = InfernoCallableMixin.load_pickled_function(func)
        elif type(func) == str:
            func = InfernoCallableMixin.load_function(func)
        elif getattr(func, "__name__", None) == "<lambda>":
            # Seems difficult to get source code of inline lambdas
            raise NotImplementedError("Cannot use lambda callables in Inferno!")
        return func

    @staticmethod
    def load_pickled_function(string):
        base_64_pickle = string
        func = deserialize_function(string)
        func.__source__ = string
        return func

    @staticmethod
    def load_function(source):
        # Remove any unwanted indentation
        source = source.lstrip()
        locals = {}
        # Execute the python code, with no access to globals, and empty
        # locals for later inspection
        exec(source, None, locals)
        assert len(locals) == 1, "Unexpected input"
        func = list(locals.values())[0]
        assert callable(func), f"{func} is not callable"
        # Not possible to get source code for function defined by exec
        # so we store it for future reference
        func.__source__ = source
        return func


class InfernoLoggerHandler(logging.Handler):
    def __init__(self, inferno_model, level):
        super().__init__(level)
        # Convert to lazy to ensure we are not overwriting data in other
        # threads while logging
        self.inferno_model = inferno_model.to_lazy()

    def emit(self, record):
        log_entry = InfernoLogEntry.from_logging_record(record)
        if not self.inferno_model.logs:
            self.inferno_model.logs = []
        self.inferno_model.logs.append(log_entry)
        self.inferno_model.save()


def _get_pydantic_errors_for_field(validation_error, field):
    errors = [
        err_wrapper for err_wrapper in validation_error.raw_errors
        if err_wrapper.loc_tuple()[0] == field
    ]
    validation_error.raw_errors = errors
    return validation_error


def set_id(field: str):
    def wrapped(cls):
        cls._id = field
        return cls
    return wrapped


def denormalise_field(field: str, path_format: str = "{path}_{field}_denormalisation"):
    # Used to duplicate information in an Inferno model to improve read
    # performance, as is usually suggested when dealing with NoSQL databases
    # (especially Firebase)
    # See https://firebase.blog/posts/2013/04/denormalizing-your-data-is-normal
    def wrapped(cls):
        denormalisation_path = path_format.format(path=cls.path, field=field)
        cls._denormalised_fields = getattr(cls, "_denormalised_fields", {})
        cls._denormalised_fields[field] = denormalisation_path
        return cls
    return wrapped


class InfernoUnionMetaClass(ModelMetaclass):
    def __setattr__(self, name, value):
        # We do this so we can set database patches at the Union level, and
        # ensure they propogate to the polymorphisms
        # This has to be in a metaclass, because the Inferno database field is
        # a class attribute
        if getattr(self, "database", None) and name == "database":
            for cls in self._polymorphisms:
                cls.database = value
        super().__setattr__(name, value)


class InfernoUnion(InfernoModel, metaclass=InfernoUnionMetaClass):
    """
    Helper class to do polymorphism with InfernoModel.
    Example:
            class BaseSubmission(InfernoModel):
                platform = Literal["base"]

            class RewardSubmission(InfernoModel):
                platform = Literal["reward"]

            Submission = InfernoUnion[BaseSubmission, RewardSubmission]
    This relies on Pydantic's valdiation behaviour to resolve the correct class,
    so each polymorphism must implement a discriminator in a similar fashion to 'platform'
    in the above example.
    """
    @class_property
    def greatest_common_superclass(cls):
        return get_greatest_common_superclass(cls._polymorphisms)

    @class_property
    def lazy(cls):
        lazy_cls = cls.greatest_common_superclass.lazy
        lazy_cls.database = cls.database
        return lazy_cls

    def __new__(cls, *args, **kwargs):
        instance = parse_obj_as(Union[cls._polymorphisms], kwargs)
        return instance

    def __class_getitem__(cls, classes):
        cls._validate_union(classes)
        greatest_common_superclass = get_greatest_common_superclass(classes)
        new_class = type("InfernoUnion", (greatest_common_superclass, InfernoUnion), {})
        new_class._polymorphisms = classes
        new_class.database = classes[0].database
        new_class.path = classes[0].path
        new_class._id = classes[0]._id
        return new_class

    @classmethod
    def _validate_union(cls, item):
        item = item if isinstance(item, Iterable) else [item]
        assert all([isclass(i) for i in item]), "Can only create an InfernoUnion from classes!"
        assert all([issubclass(i, InfernoModel) for i in item]), "Can only create an InfernoUnion from InfernoModels!"
        assert len(set([i.database for i in item])) == 1, "Cannot create an InfernoUnion from InfernoModels with different databases!"
        assert len(set([i.path for i in item])) == 1, "Cannot create an InfernoUnion from InfernoModels with different paths!"


def get_greatest_common_superclass(classes):
    classes = [cls.mro() for cls in classes]
    for x in classes[0]:
        if all(x in mro for mro in classes):
            return x
