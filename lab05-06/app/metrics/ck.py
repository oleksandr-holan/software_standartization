"""Chidamber & Kemerer metrics."""

from dataclasses import dataclass

THRESHOLDS = {
    "wmc": {"norm": 20, "critical": 40, "higher_is_worse": True},
    "dit": {"norm": 4, "critical": 5, "higher_is_worse": True},
    "cbo": {"norm": 12, "critical": 20, "higher_is_worse": True},
    "lcom": {"norm": 0.3, "critical": 0.7, "higher_is_worse": True},
    "rfc": {"norm": 50, "critical": 100, "higher_is_worse": True},
}


@dataclass
class CKMetric:
    name: str
    value: float
    status: str
    color: str


def _status(metric: str, value: float) -> tuple[str, str]:
    t = THRESHOLDS[metric]
    norm, critical = t["norm"], t["critical"]

    if metric == "lcom":
        if value <= 0.3:
            return "Норма", "green"
        if value >= critical:
            return "Критично", "red"
        return "Ризик", "orange"

    if value <= norm:
        return "Норма", "green"
    if value > critical:
        return "Критично", "red"
    return "Ризик", "orange"


def calc_ck(wmc: int, dit: int, cbo: int, lcom: float, rfc: int) -> list[CKMetric]:
    values = {"wmc": wmc, "dit": dit, "cbo": cbo, "lcom": lcom, "rfc": rfc}
    return [
        CKMetric(name=k.upper(), value=v, status=_status(k, v)[0], color=_status(k, v)[1])
        for k, v in values.items()
    ]


def ck_verdict(metrics: list[CKMetric]) -> str:
    bad = sum(1 for m in metrics if m.status in ("Ризик", "Критично"))
    if bad > 2:
        return "Негайно переписати архітектуру"
    if bad > 0:
        return "Провести частковий рефакторинг"
    return "Залишити як є"
