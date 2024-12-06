import typing
from collections import abc
from dataclasses import dataclass

import dydactic
import pydantic

from . import result as _result
from . import writer as _writer

 
Record = dict[str, typing.Any]

 
@dataclass
class ValidatorIterator(abc.Iterator):
    data: typing.Iterator[Record]
    model: pydantic.BaseModel

    def __post_init__(self) -> None:
        self.iterator = dydactic.validate(self.data, self.model)

    def __next__(self) -> _result.Result:
        result = next(self.iterator)
        return _result.Result(result.error, result.result, result.value)

    def __iter__(self) -> typing.Self:
        return self


@dataclass
class Validator(abc.Iterable):
    data: typing.Iterator[Record]
    model: pydantic.BaseModel

    def __iter__(self) -> ValidatorIterator:
        return ValidatorIterator(self.data, self.model)

    def csv_writer(self, csv_file: typing.IO) -> _writer.ResultsCSVWriter:
        return _writer.ResultsCSVWriter(iter(self), csv_file)