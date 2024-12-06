import typing
import json
import click
import functools
from typing import List, Optional

from chaiverse import submit
from chaiverse import formatters
from chaiverse.cli_utils.formatters_cli import get_formatter

FORMATTER_FIELDS = ["formatter"]
FIELDS_TO_EXCLUDE = FORMATTER_FIELDS + ["generation_params"]


def print_model_info(submission_id):
    response = submit.get_model_info(submission_id)
    response.pop('logs', None)
    for key, value in response.items():
        print(key, ':', value)


def add_submit_cli_options(*model_classes):
    def list_callback(ctx, param, value):
        return list(value) if value else None

    def generate_cli_option(field_name, model_field):
        field_name = field_name.replace('_', '-')
        field_type = model_field.type_
        multiple = "List" in model_field._type_display()
        option = click.option(
            f'--{field_name}',
            type=field_type,
            multiple=multiple,
            required=model_field.required,
            help=model_field.field_info.description or "",
            callback=list_callback if multiple else None
        )
        return option

    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        cli_param_fields = {}
        for model_class in model_classes:
            cli_param_fields.update(model_class.__fields__)

        for field in FIELDS_TO_EXCLUDE:
            cli_param_fields.pop(field, None)

        for field_name, model_field in cli_param_fields.items():
            option = generate_cli_option(field_name, model_field)
            wrapped_func = option(wrapped_func)

        return wrapped_func
    return decorator


def add_formatter_cli_options(model_class):
    def decorator(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        cli_param_fields = model_class.__fields__
        for formatter_field in FORMATTER_FIELDS:
            option = click.option(
                f"--{formatter_field.replace('_','-')}",
                type=str,
                help=cli_param_fields[formatter_field].field_info.description
            )
            wrapped_func = option(wrapped_func)

        return wrapped_func
    return decorator


def get_param_dict(params, model_class, ignore_fields=None):
    if not ignore_fields:
        ignore_fields = []
    param_dict = {
            param_name: param_value
            for param_name in model_class.__fields__
            if param_name not in ignore_fields and (param_value := params.get(param_name))}
    return param_dict


def submit_model_from_params(**params):
    generation_params = get_param_dict(params, submit.GenerationParams)
    submission_params = get_param_dict(params, submit.FrontEndSubmissionRequest, ignore_fields=FIELDS_TO_EXCLUDE)
    submission_params['generation_params'] = generation_params
    for formatter_field in FORMATTER_FIELDS:
        if formatter_name := params.get(formatter_field):
            Formatter = get_formatter(formatter_name)
            submission_params[formatter_field] = Formatter()
    submitter = submit.ModelSubmitter()
    submission_id = submitter.submit(submission_params)
    print("submission_id:", submission_id)
    return submission_id


def submit_blend_from_params(**params):
    submission_params = get_param_dict(params, submit.FrontEndBlendSubmissionRequest)
    submitter = submit.ModelSubmitter()
    submission_id = submitter.submit_blend(submission_params)
    print("submission_id:", submission_id)
    return submission_id

