class CathodicException(Exception):
    """father of cathodic_exception"""


class ValidateError(CathodicException):
    """输入的数据结构存在问题时，抛出此异常

    Args:
        CathodicException (_type_): _description_
    """

    pass


class FileError(CathodicException):
    """文件出现异常时抛出本错误

    Args:
        CathodicException (_type_): _description_
    """
