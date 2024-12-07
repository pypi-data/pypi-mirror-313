"""This module contains the constants and enums used for pagination and sorting"""

from enum import Enum

DEFAULT_PAGE_NUMBER = 1
"""Pagination constants. Default page number is 1"""
DEFAULT_PAGE_SIZE = 10
"""Pagination constants. Default page size is 10"""
ACTIVITY_DEFAULT_PAGE_SIZE = 100
"""Pagination constants for the activity logs. Default page size is 100"""
MAX_PAGE_SIZE = 500
"""Pagination constants. Maximum page size is 500"""


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"
