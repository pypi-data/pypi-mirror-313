from enum import Enum


class Result(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"
