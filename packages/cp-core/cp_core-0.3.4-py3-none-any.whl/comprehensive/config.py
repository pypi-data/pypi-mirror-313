# coding: utf-8
# Items

from loguru import logger
from cp_core.config import DEBUG


if not DEBUG:
    logger.add("info.log")


class MetaName:
    corrosive = "土壤腐蚀性"
    detect = "防腐层缺陷"
    protect = "阴极保护"
    ac = "交流杂散电流"
    dc = "直流杂散电流"
    file = "批量计算"
    result = "燃气管道外腐蚀风险综合评判结果"


class MetaContent:
    title = "燃气管网外腐蚀风险综合评判模块"


class MetaKey:
    corrosive = "corrosive"
    detect = "detect"
    protect = "is_protect"
    ac = "jiaoliu"
    dc = "zhiliu"
    file = "files"
    result = "result"


class Options:
    corrosive = ["高", "中", "低"]
    detect = ["有", "无"]
    protect = ["达标", "欠保护", "过保护"]
    ac = ["高", "中", "低"]
    dc = ["高", "中", "低"]
    result = ["空", "高", "中", "低"]


class Media:
    beiran_icon = "media/beiran_icon.png-small.png"
    ustb_icon = "media/ustb_icon.png-small.png"
    icon_size = (100, 100)

    jiuliu_pic = "media/jiaoliu-3.png-resize.png"
    zhiliu_pic = "media/zhiliu-3.png-resize.png"
    pic_size = (300, 200)


class Font:
    simson_name = "SimSon 10"
    simson_big_name = "SimSon 12"
    sigson_super_big_name = "SimSon 25 bold"
    # Helve = ('Helvetica', 25)
