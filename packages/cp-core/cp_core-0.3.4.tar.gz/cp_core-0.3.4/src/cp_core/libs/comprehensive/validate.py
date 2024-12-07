from .forms import InputData


def parse_external(values: dict) -> InputData:
    """
    综合风险评判
    :param values:
    :return:
    """
    return InputData.model_validate(values)
