import enum
import typing as t

from pydantic import BaseModel


class Status(enum.IntEnum):
    success = 0
    failed = 1


class Result(BaseModel):
    status: Status
    msg: str
    value: int = -10
    data: t.Any = None

    def is_success(self) -> bool:
        return self.status == Status.success

    @classmethod
    def make_failed_result(cls, e: Exception):
        return Result(status=Status.failed, msg=str(e))

    def msg_to_file(self, filename: str):
        with open(filename, "w") as f:
            f.write(self.msg)

    def to_json(self, filename: str):
        import json

        with open(filename, "w") as f:
            json.dump(self.model_dump(), f)


class ResultFile(BaseModel):
    """用于返回算法的处理结果"""

    id: int
    current_type: int  # 0 means ac, 1 means dc
    original_filename: str
    original_filepath: str
    in_filename: str
    filepath: str
    filename: str


class ComputeResult(Result):
    """计算结果"""

    # file list
    # contains level 1, level 2, level 3, final files
    data: t.List[ResultFile]

    def get_file(self, level: int) -> ResultFile:
        index = level - 1
        return self.data[index]


class FinalFiles(BaseModel):
    """整合好的最终结果"""

    ac: ResultFile
    dc: ResultFile


class FinalResult(Result):
    compute_result: list[ComputeResult]
    final_files: FinalFiles
