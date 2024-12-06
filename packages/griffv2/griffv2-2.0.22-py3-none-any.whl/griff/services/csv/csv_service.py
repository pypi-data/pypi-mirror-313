import csv

from injector import inject, singleton

from griff.services.abstract_service import AbstractService
from griff.services.csv.csv_models import CsvOptions
from griff.services.path.path_service import PathService


@singleton
class CsvService(AbstractService):
    @inject
    def __init__(self, path_service: PathService):
        self._path_service = path_service

    def load(self, csv_filename, options: CsvOptions | None = None):
        csv_path = self._path_service.check_exists(csv_filename)
        options = options or CsvOptions()
        with csv_path.open() as df:
            reader = csv.reader(df, delimiter=options.field_delimiter)
            headers = [c for c in next(reader)]
            return [
                {headers[i]: value for i, value in enumerate(row)}
                for row in reader
                if not options.ignore_empty_rows or any(row)
            ]
