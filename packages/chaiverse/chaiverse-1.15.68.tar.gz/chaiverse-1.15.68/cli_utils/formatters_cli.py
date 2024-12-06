from chaiverse import formatters


def get_formatter_map():
    cls_names = dir(formatters)
    formatter_classes = {
        cls_name: getattr(formatters, cls_name)
        for cls_name in cls_names
        if _is_formatter(cls_name)}
    return formatter_classes


def print_formatter_info(formatter_name):
    formatter = get_formatter(formatter_name)
    for field_name, model_field in formatter.__fields__.items():
        print(field_name, ':', repr(model_field.default))


def get_formatter(formatter_name):
    formatter_classes = get_formatter_map()
    formatter = formatter_classes.get(formatter_name)
    if not formatter:
        raise NameError(f'{formatter_name} is not a valid formatter for Chaiverse. Check chaiverse.formatters for the supported ones.')
    return formatter


def _is_formatter(cls_name):
    cls = getattr(formatters, cls_name)
    is_not_base_class = (cls_name != 'PromptFormatter')
    is_subclass = isinstance(cls, type) and issubclass(cls, formatters._PromptFormatter)
    return is_not_base_class and is_subclass

