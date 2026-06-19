"""Use Case Points calculator."""

from dataclasses import dataclass


@dataclass
class UCPResult:
    uaw: float
    uucw: float
    uucp: float
    ucp: float
    hours: float
    budget: float


def calc_ucp(
    actors_s: int, actors_m: int, actors_h: int,
    uc_s: int, uc_m: int, uc_h: int,
    tcf: float, ecf: float,
    hours_per_ucp: int = 20,
    rate: float = 35,
) -> UCPResult:
    uaw = actors_s * 1 + actors_m * 2 + actors_h * 3
    uucw = uc_s * 5 + uc_m * 10 + uc_h * 15
    uucp = uaw + uucw
    ucp = uucp * tcf * ecf
    hours = ucp * hours_per_ucp
    budget = hours * rate
    return UCPResult(uaw=uaw, uucw=uucw, uucp=uucp, ucp=ucp, hours=hours, budget=budget)


def calc_op(
    screens_s: int, screens_m: int, screens_h: int,
    reports_s: int, reports_m: int, reports_h: int,
    gl3: int, prod: float, reuse: float = 20,
) -> dict:
    screens = screens_s * 1 + screens_m * 2 + screens_h * 3
    reports = reports_s * 2 + reports_m * 5 + reports_h * 8
    op = screens + reports + gl3 * 10
    pm = op / (prod * (1 - reuse / 100)) if prod else 0
    return {"op": op, "pm": pm, "screens": screens, "reports": reports, "gl3_pts": gl3 * 10}
