"""Lorenz & Kidd metrics."""

from dataclasses import dataclass


@dataclass
class LorenzResult:
    nm_child: float
    si: float
    status: str
    color: str


def calc_lorenz(nm_base: int, noo: int, noa: int) -> LorenzResult:
    nm_child = nm_base + noa
    si = (noo + noa) / nm_base if nm_base else 0.0

    if si <= 0.5:
        status, color = "Стабільно", "green"
    elif si > 1.0:
        status, color = "Агресивне успадкування", "red"
    else:
        status, color = "На межі", "orange"

    return LorenzResult(nm_child=nm_child, si=si, status=status, color=color)
