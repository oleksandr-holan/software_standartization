"""ЛР-5 — UI метричного аудиту (Холстед, Мак-Кейб, Чепін)."""

import ast
import json

import pandas as pd
import streamlit as st

from glossary import LR5_LEGEND, render_legend
from metrics.chapin import (
    CHAPIN_OPTIONS,
    CHAPIN_Q_THRESHOLD,
    audit_verdict,
    calc_chapin,
    extract_chapin_defaults,
)
from metrics.halstead import calc_halstead
from metrics.mccabe import calc_mccabe


def render_lr5_audit(demo_code: str, color_map: dict[str, str], status_badge) -> None:
    st.subheader("Метричний аудит коду")
    st.caption("ЛР-5 — Холстед · Мак-Кейб V(G) · Чепін Q")
    render_legend("Розшифровка скорочень (ЛР-5)", LR5_LEGEND, expanded=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.markdown("**Вихідний код (Python)**")
        if "lr5_code_input" not in st.session_state:
            st.session_state.lr5_code_input = demo_code
        code_input = st.text_area(
            "Код",
            height=360,
            label_visibility="collapsed",
            key="lr5_code_input",
        )
        run_audit = st.button("Запустити комплексний аудит", use_container_width=True, type="primary")
    with c2:
        st.info(
            "Вставте модуль Python з розгалуженнями (if/elif), циклами та різними змінними. "
            "Метрики оновлюються після кожного запуску аудиту."
        )

    if not (run_audit or code_input):
        return

    try:
        tree = ast.parse(code_input)
    except SyntaxError as exc:
        st.error(f"Синтаксична помилка у коді: {exc}")
        return

    halstead = calc_halstead(tree)
    mccabe = calc_mccabe(tree)
    variables, defaults = extract_chapin_defaults(tree)

    # ── Холстед ──────────────────────────────────────────────────────────────
    st.markdown("### 1. Лексичний аналіз (Холстед)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("n — словник", halstead.vocabulary, help="Унікальних операторів + операндів (n1 + n2).")
    m2.metric("N — довжина", halstead.length, help="Загальна кількість операторів і операндів (N1 + N2).")
    m3.metric("V — об'єм", f"{halstead.volume:.2f}", help="Інтелектуальний об'єм коду.")
    m4.metric("D — складність", f"{halstead.difficulty:.2f}", help="Наскільки важко читати код.")

    m5, m6, m7, _ = st.columns(4)
    m5.metric("E — зусилля", f"{halstead.effort:.2f}", help="Ментальні зусилля на розуміння.")
    m6.metric("T — час розробки (с)", f"{halstead.dev_time_sec:.2f}", help="Оцінка часу написання в секундах.")
    m7.metric("B — прогноз помилок", f"{halstead.bugs:.4f}", help="Очікувана кількість дефектів. Норма < 0.5.")

    with st.expander("Таблиці операторів і операндів"):
        t1, t2 = st.columns(2)
        with t1:
            op_df = (
                pd.DataFrame(list(halstead.operators.items()), columns=["Оператор", "Кількість (N1)"])
                .sort_values("Кількість (N1)", ascending=False)
                .reset_index(drop=True)
            )
            st.dataframe(op_df, use_container_width=True, hide_index=True)
        with t2:
            ond_df = (
                pd.DataFrame(list(halstead.operands.items()), columns=["Операнд", "Кількість (N2)"])
                .sort_values("Кількість (N2)", ascending=False)
                .reset_index(drop=True)
            )
            st.dataframe(ond_df, use_container_width=True, hide_index=True)

    # ── Мак-Кейб ───────────────────────────────────────────────────────────
    st.markdown("### 2. Структурний аналіз (Мак-Кейб)")
    mc1, mc2 = st.columns([1, 2])
    with mc1:
        st.metric("V(G) — цикломатична складність", mccabe.vg, help="Кількість незалежних шляхів = розвилки + 1.")
        status_badge(f"NIST: {mccabe.category}", mccabe.color)
        st.caption(
            f"Мінімум тестів (basis path): **{mccabe.vg}** × 0.5 год = "
            f"**{mccabe.vg * 0.5:.1f}** год QA"
        )
    with mc2:
        st.markdown("**Граф потоку керування (CFG)**")
        st.graphviz_chart(mccabe.cfg, use_container_width=True)

    # ── Чепін ──────────────────────────────────────────────────────────────
    st.markdown("### 3. Інформаційний аналіз (Чепін)")
    st.caption("Класифікуйте кожну змінну — Q перераховується миттєво.")

    classifications: dict[str, str] = {}
    if variables:
        cols = st.columns(4)
        for i, var in enumerate(sorted(variables)):
            default_val = defaults.get(var, CHAPIN_OPTIONS[3])
            with cols[i % 4]:
                idx = CHAPIN_OPTIONS.index(default_val) if default_val in CHAPIN_OPTIONS else 0
                classifications[var] = st.selectbox(
                    f"`{var}`",
                    CHAPIN_OPTIONS,
                    index=idx,
                    key=f"chapin_{var}",
                )
    else:
        st.warning("Змінні в AST не знайдено.")

    chapin = calc_chapin(classifications)
    b = chapin.breakdown
    q_text = (
        f"Q = 1×{b['P']} + 2×{b['M']} + 3×{b['C']} + 0.5×{b['T']} = **{chapin.q:.1f}**"
    )
    if chapin.q >= CHAPIN_Q_THRESHOLD:
        st.error(q_text)
    else:
        st.success(q_text)
    status_badge(chapin.status, chapin.color)

    # ── Звіт ───────────────────────────────────────────────────────────────
    st.markdown("### 4. Підсумковий вердикт")
    verdict, verdict_color, issues = audit_verdict(mccabe.vg, halstead.bugs, chapin.q)
    status_badge(verdict, verdict_color)

    if verdict == "Рекомендовано реліз":
        st.markdown(
            "**Managerial Report:** V(G), B і Q у безпечних межах. "
            "Достатньо стандартного покриття модульними тестами перед релізом."
        )
    else:
        st.markdown(
            "**Managerial Report:** " + "; ".join(issues) + ". "
            "Розбити на дрібніші функції (SRP), щоб знизити когнітивне навантаження."
        )

    # ── Експорт ────────────────────────────────────────────────────────────
    st.markdown("### 5. Експорт")
    report = {
        "halstead": {
            "n1": halstead.n1,
            "n2": halstead.n2,
            "N1": halstead.n1_total,
            "N2": halstead.n2_total,
            "vocabulary_n": halstead.vocabulary,
            "length_N": halstead.length,
            "volume_V": round(halstead.volume, 2),
            "difficulty_D": round(halstead.difficulty, 2),
            "effort_E": round(halstead.effort, 2),
            "dev_time_sec": round(halstead.dev_time_sec, 2),
            "bugs_B": round(halstead.bugs, 4),
        },
        "mccabe": {"VG": mccabe.vg, "category": mccabe.category},
        "chapin": {
            "classifications": classifications,
            "Q": chapin.q,
            "breakdown": chapin.breakdown,
        },
        "verdict": verdict,
    }
    st.download_button(
        label="Завантажити звіт (JSON)",
        data=json.dumps(report, indent=2, ensure_ascii=False),
        file_name="metrics_report.json",
        mime="application/json",
        use_container_width=True,
    )
