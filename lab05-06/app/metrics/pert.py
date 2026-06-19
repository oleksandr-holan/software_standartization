"""PERT risk engine."""

from dataclasses import dataclass


@dataclass
class PERTResult:
    e: float
    sd: float
    safe: float
    risk_pct: float
    risk_budget: float
    total_budget: float
    is_high_risk: bool


def calc_pert(o: float, m: float, p: float, base_budget: float) -> PERTResult:
    e = (o + 4 * m + p) / 6
    sd = (p - o) / 6
    safe = e + 2 * sd
    risk_pct = (sd / e * 100) if e else 0
    risk_budget = base_budget * (risk_pct / 100)
    total = base_budget + risk_budget
    return PERTResult(
        e=e, sd=sd, safe=safe,
        risk_pct=risk_pct, risk_budget=risk_budget,
        total_budget=total, is_high_risk=sd > 15,
    )
