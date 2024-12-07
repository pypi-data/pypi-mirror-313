"""
controller 是处理请求的基本单位。
"""

from cp_core.libs.total.controller import compute  # noqa
from cp_core.libs.total.fileutils import merge_files  # noqa

from cp_core.libs import proto


from cp_core.libs.core.filter.controller import filter_controller
from cp_core.libs.core.stat.controller import stat_controller
from cp_core.libs.core.model.controller import model_controller

use_filter: proto.UseFilter = filter_controller
use_stat: proto.UseStat = stat_controller
use_model: proto.UseModel = model_controller
