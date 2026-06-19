"""McCabe cyclomatic complexity and CFG."""

import ast
from dataclasses import dataclass

import graphviz


@dataclass
class McCabeResult:
    vg: int
    decisions: int
    cfg: graphviz.Digraph
    category: str
    color: str


def calc_mccabe(tree: ast.AST) -> McCabeResult:
    decisions = 0
    dot = graphviz.Digraph(comment="CFG")
    dot.attr(rankdir="LR", nodesep="0.2", ranksep="0.3")
    dot.attr("node", fontsize="10", height="0.2", width="0.2")

    prev_node = "Start"
    dot.node(prev_node, "Початок", shape="ellipse")
    node_idx = 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
            decisions += 1
            node_label = f"{type(node).__name__}_{node_idx}"
            dot.node(
                node_label,
                type(node).__name__,
                shape="diamond",
                color="red",
                style="filled",
                fillcolor="#ffcccc",
            )
            dot.edge(prev_node, node_label)
            prev_node = node_label
            node_idx += 1

    dot.node("End", "Кінець", shape="ellipse")
    dot.edge(prev_node, "End")

    vg = decisions + 1
    if vg <= 10:
        category, color = "Простий (1–10)", "green"
    elif vg <= 20:
        category, color = "Помірний (11–20)", "orange"
    else:
        category, color = "Складний (>20)", "red"

    return McCabeResult(vg=vg, decisions=decisions, cfg=dot, category=category, color=color)
