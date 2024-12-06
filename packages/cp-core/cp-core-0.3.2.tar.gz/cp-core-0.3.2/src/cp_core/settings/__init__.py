"""
The proportion of time that the pipeline polarization potential
is positive relative to the minimum protection potential criterion.

DC interference evaluation: dcie
AC interference evaluation: acie

composite index

The algorithm is based on the following standards:
"""

import ast

default_settings = {
    "dcie": {
        "level_low": [
            {
                "id": 1,
                "condition": "电位正于最小保护准则的时间比例不超过测试时间的%",
                "value": [
                    10,
                ],
            },
            {
                "id": 2,
                "condition": "且电位正于最小保护准则+mV的时间比例不超过测试时间的%;",
                "value": [50, 5],
            },
            {
                "id": 3,
                "condition": "且电位正于最小保护准则%mV的时间比例不超过测试时间的%",
                "value": [100, 1],
            },
        ],
        "level_mid": [
            {
                "id": 1,
                "condition": "处于“低”腐蚀风险与“高”腐蚀风险间的为“中”腐蚀风险等级",
            }
        ],
        "level_high": [
            {
                "id": 1,
                "condition": "电位正于最小保护准则的时间比例超过测试时间的%;",
                "value": [
                    20,
                ],
            },
            {
                "id": 2,
                "condition": "②或电位正于最小保护准则+mV的时间比例超过测试时间的%",
                "value": [20, 15],
            },
            {
                "id": 3,
                "condition": "或电位正于最小保护准则+mV的时间比例超过测试时间的%",
                "value": [100, 10],
            },
        ],
    },
    "acie": {
        "jac": [
            {
                "id": 1,
                "condition": "Jac≤ A/m2",
                "value": [
                    15,
                ],
            },
        ],
        "composite index": [
            {
                "id": 1,
                "conditions": "当A/m2<J2<A/m2时， 应满足:",
                "value": [30, 100],
            },
            {
                "id": 2,
                "conditions": " V_cse ≤ E_IR-free ≤ V_CSE or Jdc ≤ A/m 2 and EIR-free ≤ V CSE",
                "value": [-1.15, 0.9, 1, 0.9],
            },
        ],
    },
}


def parse(str_format: str) -> tuple[list[str], list[float]]:
    """
    example: dcie.level_low.1=[12]
    """

    def parse_stat():
        key, v = str_format.split("=")
        return key, v

    def parse_dot(keys) -> list[str]:
        keys = keys.split(".")
        return keys

    k, v = parse_stat()
    keys = parse_dot(k)

    value = ast.literal_eval(v)
    if not isinstance(value, list):
        value = [value]

    return keys, value


def assign(settings: dict, keys: list[str], v: list[float]):
    r = None
    for k in keys[:-1]:
        if r is None:
            r = settings.get(k, None)
        else:
            r = r.get(k, None)

        if r is None:
            raise ValueError(f"key: {k} not found")

    # {name: {name: []} or { name: [] }
    assert isinstance(r, list), "r should be a list"

    id = ast.literal_eval(keys[-1])[0]
    for object in r:
        if object["id"] == id:
            object["value"] = v
            return settings

    raise ValueError(f"key: {id} not found")


def parse_and_assign(settings, str_format: str):
    keys, v = parse(str_format)
    return assign(settings, keys, v)
