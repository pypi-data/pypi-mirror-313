from collections import abc
from dataclasses import dataclass
import typing
import csv

from . import result as _result
from . import to_dict as _to_dict


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
        if result.result:
            row: dict[str, typing.Any] = _to_dict.data_to_dict(result.result)
        else:
            return result
        if self.headers == False:
            self.writer = csv.DictWriter(self.csv_file, fieldnames=row)
            try:
                self.writer.writeheader()
            except Exception as e:
                return _result.Result(e, None, result.value)
            self.headers = True
        if self.writer:
            try:
                self.writer.writerow(row)
            except Exception as e:
                return _result.Result(e, None, result.value)
        else:
            raise ValueError('CSV Writer is not initialized.')
        return result


@dataclass
class ResultsCSVWriter(abc.Iterable):
    results: typing.Iterator[_result.Result]
    csv_file: typing.IO

    def __iter__(self) -> ResultsCSVWriterIterator:
        return ResultsCSVWriterIterator(self.results, self.csv_file)