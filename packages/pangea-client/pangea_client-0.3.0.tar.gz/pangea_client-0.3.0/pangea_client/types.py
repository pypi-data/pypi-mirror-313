# enum of formats
from enum import Enum


class Format(str, Enum):
    Csv = "csv"
    Json = "json"
    JsonStream = "json_stream"
    Arrow = "arrow"
    ArrowStream = "arrow_stream"
