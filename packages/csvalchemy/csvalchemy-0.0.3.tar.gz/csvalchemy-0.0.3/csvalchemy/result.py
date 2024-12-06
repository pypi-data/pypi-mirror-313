import typing

import pydantic


class Result(typing.NamedTuple):
    error: Exception | None
    result: pydantic.BaseModel | None
    value: typing.Any
