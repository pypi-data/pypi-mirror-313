from pydantic import BaseModel


class CsvOptions(BaseModel):
    field_delimiter: str = ","
    line_terminator: str = "\n"
    ignore_empty_rows: bool = False
