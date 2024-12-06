from dataclasses import dataclass


@dataclass
class ACSettings(object):
    jac_low: float
    jac_range: tuple[float, float]
    jac_high: float

    ir_free_range: tuple[float, float]
    ir_free_high: float
    jdc_low: float


@dataclass
class DCSettings(object):
    low_protect: tuple[float, float]
    high_protect: tuple[float, float]

    low_percent: tuple[float, float, float]
    high_percent: tuple[float, float, float]

    @property
    def polar_value(self):
        return (
            "极化电位正于评判准则的比例/%",
            f"极化电位正于评判准则+{self.low_protect[0] / 1000}V的比例/%",
            f"极化电位正于评判准则+{self.low_protect[1] / 1000}V的比例/%",
            "极化电位正于评判准则+0.85V的比例/%",
            "极化电位负于评判准则-0.25V的比例/%",
            "极化电位负于评判准则-0.3V的比例/%",
            "极化电位负于评判准则-0.35V的比例/%",
            "极化电位负于评判准则-0.4V的比例/%",
        )
