"""Enums for thoughtful_object configuration."""


class Extra:
    """Extra field from build_thoughtful_object."""

    allow: str = "allow"
    forbid: str = "forbid"
    ignore: str = "ignore"


class RevalidateInstances:
    """Revalidate_instances from build_thoughtful_object."""

    never: str = "never"
    always: str = "always"
    subclass_instances: str = "subclass-instances"


class SerJsonTimedelta:
    """Ser_json_timedelta from build_thoughtful_object."""

    iso8601: str = "iso8601"
    float_type: str = "float"


class SerJsonInfNan:
    """Ser_json_inf_nan from build_thoughtful_object."""

    null: str = "null"
    constants: str = "constants"
