"""Main module."""
from .builder import build_custom_t_object
from .config_enums import Extra, RevalidateInstances

ThoughtfulObject = build_custom_t_object(
    validate_assignment=True,
    extra=Extra.forbid,
    frozen=False,
    populate_by_name=False,
    arbitrary_types_allowed=True,
    allow_inf_nan=True,
    strict=True,
    revalidate_instances=RevalidateInstances.always,
    validate_default=False,
    coerce_numbers_to_str=True,
    validation_error_cause=True,
    str_strip_whitespace=True,
)
