"""Chapin information complexity metrics."""

import ast
from dataclasses import dataclass

CHAPIN_OPTIONS = [
    "P — вхідна (вага 1.0)",
    "M — змінювана (вага 2.0)",
    "C — керуюча (вага 3.0)",
    "T — стороння (вага 0.5)",
]

CHAPIN_WEIGHTS = {"P": 1.0, "M": 2.0, "C": 3.0, "T": 0.5}
CHAPIN_Q_THRESHOLD = 26.0


@dataclass
class ChapinResult:
    variables: list[str]
    defaults: dict[str, str]
    q: float
    breakdown: dict[str, int]
    color: str
    status: str


def _option_prefix(option: str) -> str:
    return option[0]


def chapin_weight(option: str) -> float:
    return CHAPIN_WEIGHTS.get(_option_prefix(option), 0.5)


def extract_chapin_defaults(tree: ast.AST) -> tuple[set[str], dict[str, str]]:
    variables: set[str] = set()
    defaults: dict[str, str] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                variables.add(arg.arg)
                defaults[arg.arg] = CHAPIN_OPTIONS[0]
        elif isinstance(node, (ast.If, ast.While, ast.For)):
            condition = getattr(node, "test", None) or getattr(node, "iter", None)
            if condition:
                for subnode in ast.walk(condition):
                    if isinstance(subnode, ast.Name):
                        variables.add(subnode.id)
                        defaults[subnode.id] = CHAPIN_OPTIONS[2]
        elif isinstance(node, (ast.Assign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if isinstance(target, ast.Name):
                    variables.add(target.id)
                    if target.id not in defaults:
                        defaults[target.id] = CHAPIN_OPTIONS[1]
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            variables.add(node.id)

    return variables, defaults


def calc_chapin(classifications: dict[str, str]) -> ChapinResult:
    breakdown = {"P": 0, "M": 0, "C": 0, "T": 0}
    q = 0.0
    for option in classifications.values():
        prefix = _option_prefix(option)
        breakdown[prefix] = breakdown.get(prefix, 0) + 1
        q += chapin_weight(option)

    if q >= CHAPIN_Q_THRESHOLD:
        status, color = "Важко підтримувати", "red"
    else:
        status, color = "Прийнятно", "green"

    return ChapinResult(
        variables=sorted(classifications),
        defaults=classifications,
        q=q,
        breakdown=breakdown,
        color=color,
        status=status,
    )


def audit_verdict(vg: int, bugs: float, q: float) -> tuple[str, str, list[str]]:
    """Return verdict label, color, and failing reasons."""
    if vg <= 10 and bugs < 0.5 and q < CHAPIN_Q_THRESHOLD:
        return "Рекомендовано реліз", "green", []

    issues = []
    if vg > 10:
        issues.append(f"V(G) занадто високий ({vg} > 10)")
    if bugs >= 0.5:
        issues.append(f"Прогноз помилок зависокий ({bugs:.2f} ≥ 0.5)")
    if q >= CHAPIN_Q_THRESHOLD:
        issues.append(f"Чепін Q перевантажений ({q:.1f} ≥ {CHAPIN_Q_THRESHOLD})")
    return "Потрібен рефакторинг", "red", issues
