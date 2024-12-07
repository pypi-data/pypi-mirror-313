import typing as t


class Params(t.TypedDict):
    period: int  # 4 for total. Seems not used.
    types: int
    type_zhiliu: int
    is_protect: int
    device_id: str
    piece_id: str
    piece_area: float
    resistivity: float
    interval_jihua: bool
    judge_metric: float
    udl2_file: str
    udl1_file: t.Optional[str]
    out_file_path_1: str
    out_file_path_2: str
    out_file_path_3: str


class FilterParams(t.TypedDict):
    """_summary_"""

    type_zhiliu: bool
    device_id: str
    resistivity: float
    piece_id: str
    piece_area: float
    udl2_file: str
    udl1_file: t.Optional[str]
    out_file_path: str


class StatParams(t.TypedDict):
    type_zhiliu: bool
    is_protect: bool
    resistivity: float
    filtered_file: str
    judge_metric: float
    interval_jihua: bool
    out_file_path: str


class ModelParams(t.TypedDict):
    type_zhiliu: bool
    is_protect: bool
    in_file_path: str
    out_file_path: str


class ParamGroup(t.TypedDict):
    # 使用 dict，结构更简单
    output_path: t.Optional[
        t.Callable[[str], str]
    ]  # 获取最终结果的文件路径；输入是 out_file_path1
    get_full_path: t.Callable[[str], str]  # 获取最终结果的文件路径，输入是 ac, dc
    param_list: t.List[Params]
