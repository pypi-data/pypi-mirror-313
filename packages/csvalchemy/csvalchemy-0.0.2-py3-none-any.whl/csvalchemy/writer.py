from collections import abc
from dataclasses import dataclass
import typing
import csv

from . import result as _result


@dataclass
class ResultsCSVWriterIterator(abc.Iterator):
    results: typing.Iterator[_result.Result]
    csv_file: typing.IO

    def __post_init__(self) -> None:
        self.headers: bool = False
        self.writer: csv.DictWriter | None = None

    def __next__(self) -> _result.Result:
        result: _result.Result = next(self.results)
        return self.write_result(result)

    def write_result(
        self,
        result: _result.Result
    ) -> _result.Result:
        if result.error:
            return result
        row: dict[str, typing.Any] = result.result.model_dump()
        if self.headers == False:
            self.writer = csv.DictWriter(self.csv_file, fieldnames=row)
            try:
                self.writer.writeheader()
            except Exception as e:
                return _result.Result(e, None, result.value)
            self.headers = True
        try:
            self.writer.writerow(row)
        except Exception as e:
            return _result.Result(e, None, result.value)
        return result


@dataclass
class ResultsCSVWriter(abc.Iterable):
    results: typing.Iterator[_result.Result]
    csv_file: typing.IO

    def __iter__(self) -> ResultsCSVWriterIterator:
        return ResultsCSVWriterIterator(self.results, self.csv_file)