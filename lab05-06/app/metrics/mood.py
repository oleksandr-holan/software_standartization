"""MOOD metrics."""

from dataclasses import dataclass


@dataclass
class MoodMetric:
    name: str
    value: float
    pct: float
    target: str
    status: str
    color: str


def _ahf_status(pct: float) -> tuple[str, str]:
    if pct >= 95:
        return "Норма", "green"
    if pct >= 80:
        return "Ризик", "orange"
    return "Критично", "red"


def _mhf_status(pct: float) -> tuple[str, str]:
    if 40 <= pct <= 70:
        return "Норма", "green"
    if 25 <= pct < 40 or 70 < pct <= 80:
        return "Ризик", "orange"
    return "Критично", "red"


def _cof_status(pct: float) -> tuple[str, str]:
    if pct < 15:
        return "Норма", "green"
    if pct <= 18:
        return "Ризик", "orange"
    return "Критично", "red"


def _pof_status(pct: float) -> tuple[str, str]:
    if pct >= 20:
        return "Норма", "green"
    if pct >= 10:
        return "Ризик", "orange"
    return "Критично", "red"


def calc_mood(
    m_tot: int, m_pub: int, a_tot: int, a_pub: int,
    m_tot2: int, m_inh: int, a_tot2: int, a_inh: int,
    m_over: int, m_max_ov: int, c_act: int, c_max: int,
) -> dict:
    mhf = (m_tot - m_pub) / m_tot if m_tot else 0
    ahf = (a_tot - a_pub) / a_tot if a_tot else 0
    mif = m_inh / m_tot2 if m_tot2 else 0
    aif = a_inh / a_tot2 if a_tot2 else 0
    pof = m_over / m_max_ov if m_max_ov else 0
    cof = c_act / c_max if c_max else 0

    summary = [
        MoodMetric("AHF", ahf, ahf * 100, "> 95%", *_ahf_status(ahf * 100)),
        MoodMetric("MHF", mhf, mhf * 100, "40-70%", *_mhf_status(mhf * 100)),
        MoodMetric("COF", cof, cof * 100, "< 15%", *_cof_status(cof * 100)),
        MoodMetric("POF", pof, pof * 100, "> 20%", *_pof_status(pof * 100)),
    ]

    return {
        "summary": summary,
        "mif": mif,
        "aif": aif,
        "mif_pct": mif * 100,
        "aif_pct": aif * 100,
    }
