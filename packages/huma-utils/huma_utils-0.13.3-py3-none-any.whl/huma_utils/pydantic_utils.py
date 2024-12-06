import pydantic

from huma_utils import string_utils


class Model(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(
        validate_assignment=True,
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        populate_by_name=True,
    )


class CamelCaseAliased(Model):
    model_config = pydantic.ConfigDict(alias_generator=string_utils.snake_to_camel)
