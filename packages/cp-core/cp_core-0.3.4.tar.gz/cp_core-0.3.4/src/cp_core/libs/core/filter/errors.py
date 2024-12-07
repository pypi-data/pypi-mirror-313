# coding: utf-8

"""
Define all error strs
"""


class FilterError(Exception):
    """
    basic filter error.
    """


class FileError(FilterError):
    """文件异常全部使用本类

    Args:
        FilterError (_type_): _description_
    """

    not_found = "文件不存在"
    not_csv = "文件不是csv文件"
    not_support = "文件类型不支持"
    not_found_udl2 = "文件名中不存在udl2"
    not_found_udl1 = "文件名中不存在udl1"
    not_found_anko = "文件名中不存在Anko"
    not_found_anko_and_udl1 = "文件名中不存在Anko或udl1"

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class FormatError(FilterError):
    """When file format error, use this class"""

    pass


class ColumnError(Exception):
    pass


class InputError(Exception):
    """
    handle the input params error.
    """

    pass


class EmptyError(Exception):
    """
    Exception of no readings
    """

    pass
