import typing

from pydantic import BaseModel
from typing import NamedTuple, Mapping
from dataclasses import asdict

DataModel = typing.Union[BaseModel, Mapping, NamedTuple]


def data_to_dict(model: DataModel) -> dict:
    if isinstance(model, BaseModel):
        return model.model_dump()
    if isinstance(model, tuple):
        return model._asdict()
    if isinstance(model, Mapping):
        return dict(model)
    # Also works on dataclassses
    return asdict(model)