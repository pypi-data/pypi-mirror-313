import typing
import csv

import pydantic

from . import validator as _validator


class CSVReaderValidator(_validator.Validator):
    def __init__(
        self,
        csv_file: typing.IO,
        model: pydantic.BaseModel
    ) -> None:
        data = csv.DictReader(csv_file)
        super().__init__(data, model)


def read(csv_file: typing.IO, model: pydantic.BaseModel) -> CSVReaderValidator:
    return CSVReaderValidator(csv_file, model)