"""Halstead lexical complexity metrics."""

import ast
import math
from dataclasses import dataclass


@dataclass
class HalsteadResult:
    operators: dict[str, int]
    operands: dict[str, int]
    n1: int
    n2: int
    n1_total: int
    n2_total: int
    vocabulary: int
    length: int
    volume: float
    difficulty: float
    effort: float
    bugs: float
    dev_time_sec: float


def calc_halstead(tree: ast.AST) -> HalsteadResult:
    operators: dict[str, int] = {}
    operands: dict[str, int] = {}

    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.FunctionDef, ast.Return, ast.Break)):
            op_name = type(node).__name__
            operators[op_name] = operators.get(op_name, 0) + 1
        elif isinstance(node, ast.BinOp):
            op_name = type(node.op).__name__
            operators[op_name] = operators.get(op_name, 0) + 1
        elif isinstance(node, ast.Compare):
            for op in node.ops:
                op_name = type(op).__name__
                operators[op_name] = operators.get(op_name, 0) + 1
        elif isinstance(node, ast.Assign):
            operators["Assign (=)"] = operators.get("Assign (=)", 0) + 1
        elif isinstance(node, ast.AugAssign):
            key = f"AugAssign ({type(node.op).__name__}=)"
            operators[key] = operators.get(key, 0) + 1

        if isinstance(node, ast.Name):
            operands[node.id] = operands.get(node.id, 0) + 1
        elif isinstance(node, ast.Constant):
            val = str(node.value)
            operands[val] = operands.get(val, 0) + 1
        elif isinstance(node, ast.arg):
            operands[node.arg] = operands.get(node.arg, 0) + 1

    n1 = len(operators)
    n2 = len(operands)
    n1_total = sum(operators.values())
    n2_total = sum(operands.values())
    vocabulary = n1 + n2
    length = n1_total + n2_total

    volume = length * math.log2(vocabulary) if vocabulary > 0 else 0.0
    difficulty = (n1 / 2) * (n2_total / n2) if n2 > 0 else 0.0
    effort = volume * difficulty
    bugs = (effort ** (2 / 3)) / 3000 if effort > 0 else 0.0
    dev_time_sec = effort / 18

    return HalsteadResult(
        operators=operators,
        operands=operands,
        n1=n1,
        n2=n2,
        n1_total=n1_total,
        n2_total=n2_total,
        vocabulary=vocabulary,
        length=length,
        volume=volume,
        difficulty=difficulty,
        effort=effort,
        bugs=bugs,
        dev_time_sec=dev_time_sec,
    )
