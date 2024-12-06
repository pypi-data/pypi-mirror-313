"""This module contains the builder for the Thoughtful Object."""
from typing import Callable, Union

from pydantic import ConfigDict

from .base_object import _BaseThoughtfulObject
from .config_enums import Extra, RevalidateInstances, SerJsonInfNan, SerJsonTimedelta


def build_custom_t_object(
    title: str = None,
    str_to_lower: bool = None,
    str_to_upper: bool = None,
    str_strip_whitespace: bool = None,
    str_min_length: int = None,
    str_max_length: int = None,
    extra: str = Extra.ignore,
    frozen: bool = None,
    populate_by_name: bool = None,
    use_enum_values: bool = None,
    validate_assignment: bool = None,
    arbitrary_types_allowed: bool = None,
    from_attributes: bool = None,
    loc_by_alias: bool = None,
    alias_generator: Callable = None,
    ignored_types: tuple[type] = None,
    allow_inf_nan: bool = None,
    json_schema_extra: Union[dict, Callable] = None,
    json_encoders: Union[dict, object] = None,
    strict: bool = None,
    revalidate_instances: str = RevalidateInstances.never,
    ser_json_timedelta: str = SerJsonTimedelta.iso8601,
    ser_json_inf_nan: str = SerJsonInfNan.null,
    validate_default: bool = None,
    validate_return: bool = None,
    protected_namespaces: tuple[str] = None,
    hide_input_in_errors: bool = None,
    defer_build: bool = None,
    plugin_settings: dict = None,
    coerce_numbers_to_str: bool = None,
    validation_error_cause: bool = None,
):
    """Thoughtful Object Builder.

    For mo information visit https://docs.pydantic.dev/2.6/api/config/

    Args:
        title (str): The title for the generated JSON schema, defaults to the model's name
        str_to_lower(bool): Whether to convert all characters to lowercase for str types. Defaults to False.
        str_to_upper(bool): Whether to convert all characters to uppercase for str types. Defaults to False.
        str_strip_whitespace(bool): Whether to strip leading and trailing whitespace for str types.
        str_min_length(int): The minimum length for str types. Defaults to None.
        str_max_length(int): The maximum length for str types. Defaults to None.
        extra(str): Whether to ignore, allow, or forbid extra attributes during model initialization.
                    Defaults to 'ignore'.
        frozen(bool): Whether models are faux-immutable, i.e. whether __setattr__ is allowed, and also generates a
                    __hash__() method for the model. This makes instances of the model potentially hashable
                    if all the attributes are hashable. Defaults to False.
        populate_by_name(bool): Whether an aliased field may be populated by its name as given by the model attribute,
                    as well as the alias. Defaults to False.
        use_enum_values(bool): Whether to populate models with the value property of enums, rather than the raw enum.
                    This may be useful if you want to serialize model.model_dump() later. Defaults to False.
        validate_assignment(bool): Whether to validate the data when the model is changed. Defaults to False.
                    The default behavior of Pydantic is to validate the data when the model is created.
                    In case the user changes the data after the model is created, the model is not revalidated.
        arbitrary_types_allowed(bool): Whether arbitrary types are allowed for field types. Defaults to False.
        from_attributes(bool): Whether to build models and look up discriminators of tagged unions
                    using python object attributes.
        loc_by_alias(bool): Whether to use the actual key provided in the data (e.g. alias) for error locs
                    rather than the field's name. Defaults to True.
        alias_generator(callable): A callable that takes a field name and returns an alias for it or an instance
                    of AliasGenerator. Defaults to None. When using a callable, the alias generator is used for both
                    validation and serialization. If you want to use different alias generators for validation
                    and serialization, you can use AliasGenerator instead. If data source field names do not match
                     your code style (e. g. CamelCase fields), you can automatically generate aliases
                     using alias_generator
        ignored_types(tuple[type]): A tuple of types that may occur as values of class attributes without
                    annotations. This is typically used for custom descriptors
                    (classes that behave like property). If an attribute is set on a class without an annotation
                    and has a type that is not in this tuple (or otherwise recognized by pydantic),
                    an error will be raised. Defaults to ().
        allow_inf_nan(bool): Whether to allow infinity (+inf an -inf) and NaN values to float fields. Defaults to True.
        json_schema_extra(dict or callable): A dict or callable to provide extra JSON schema properties.
                    Defaults to None.
        json_encoders(dict): A dict of custom JSON encoders for specific types. Defaults to None.
        strict(bool): If True, strict validation is applied to all fields on the model.By default, Pydantic attempts
                    to coerce values to the correct type, when possible. There are situations in which you may
                    want to disable this behavior, and instead raise an error if a value's type does not match
                    the field's type annotation.
        revalidate_instances(str): When and how to revalidate models and dataclasses during validation. Accepts the
                    string values of 'never', 'always' and 'subclass-instances'. Defaults to 'never'.
                        'never' will not revalidate models and dataclasses during validation
                        'always' will revalidate models and dataclasses during validation
                        'subclass-instances' will revalidate models and dataclasses during validation
                            if the instance is a subclass of the model or dataclass
        ser_json_timedelta(str): The format of JSON serialized timedeltas. Accepts the string values of 'iso8601' and
                    'float'. Defaults to 'iso8601'.
                        'iso8601' will serialize timedeltas to ISO 8601 durations.
                        'float' will serialize timedeltas to the total number of seconds.
        ser_json_inf_nan(str): The encoding of JSON serialized infinity and NaN float values. Accepts the string values
                    of 'null' and 'constants'. Defaults to 'null'.
        validate_default(bool): Whether to validate default values during validation. Defaults to False.
        validate_return(bool): whether to validate the return value from call validators. Defaults to False
        protected_namespaces(tuple[str[): A tuple of strings that prevent model to have field which conflict with them.
                    Defaults to ('model_', )).
        hide_input_in_errors(bool): Whether to hide inputs when printing errors. Defaults to False.ydantic shows the
                    input value and type when it raises ValidationError during the validation
        defer_build(bool): Whether to defer model validator and serializer construction until the first model
                    validation. This can be useful to avoid the overhead of building models which are only used nested
                    within other models, or when you want to manually define type namespace
                    via Model.model_rebuild(_types_namespace=...). Defaults to False.
        plugin_settings(dict): A dict of settings for plugins. Defaults to None.
                    See https://docs.pydantic.dev/2.6/concepts/plugins/
        coerce_numbers_to_str(bool): If True, enables automatic coercion of any Number type to str in "lax" (non-strict)
                    mode. Defaults to False. Pydantic doesn't allow number types (int, float, Decimal)
                    to be coerced as type str by default.
        validation_error_cause(bool): If True, python exceptions that were part of a validation failure will be shown
                    as an exception group as a cause. Can be useful for debugging. Defaults to False.
    """
    config = {k: v for k, v in locals().items() if v is not None}

    class _TObject(_BaseThoughtfulObject):
        """This class is the base."""

        model_config = ConfigDict(**config)
        _custom_model_config = {
            "json_file_counter": 0,
        }

    return _TObject
