import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
import pandas as pd
import altair as alt

from presets import CRYPTOWALLET_PRESET, LR5_DEMO_CODE
from glossary import (
    CK_INPUTS,
    CK_LEGEND,
    LORENZ_INPUTS,
    LORENZ_LEGEND,
    MOOD_INPUTS_ENCAP,
    MOOD_INPUTS_FLEX,
    MOOD_INPUTS_INHERIT,
    MOOD_LEGEND,
    MOOD_RESULTS,
    PERT_LEGEND,
    UCP_LEGEND,
    input_label,
    mood_number_input,
    render_legend,
)
from metrics.lorenz import calc_lorenz
from metrics.ck import calc_ck, ck_verdict
from metrics.mood import calc_mood
from metrics.ucp import calc_ucp, calc_op
from metrics.pert import calc_pert
from views.lr5_audit import render_lr5_audit

st.set_page_config(page_title="Лабораторія метрик ПЗ", layout="wide", page_icon="📊")

COLOR_MAP = {"green": "#22c55e", "orange": "#f59e0b", "red": "#ef4444"}

LR5_MODULE = "ЛР-5: Аудит коду (Холстед / Мак-Кейб / Чепін)"
LR6_MODULES = [
    "ЛР-6: Ієрархія (SI)",
    "ЛР-6: Метрики CK",
    "ЛР-6: Аналіз MOOD",
    "ЛР-6: Калькулятор UCP",
    "ЛР-6: PERT і пропозиція",
]


def status_badge(text: str, color: str) -> None:
    st.markdown(
        f'<span style="background:{COLOR_MAP.get(color, "#64748b")};color:white;'
        f'padding:4px 12px;border-radius:6px;font-weight:600;">{text}</span>',
        unsafe_allow_html=True,
    )


def init_state():
    if "preset_loaded" not in st.session_state:
        st.session_state.preset_loaded = False


init_state()

st.title("Лабораторія метрик ПЗ")
st.caption("ЛР-5 · ЛР-6 — CryptoWallet (варіант 13)")

with st.sidebar:
    st.header("Навігація")
    module = st.radio(
        "Модуль",
        [LR5_MODULE, *LR6_MODULES],
        label_visibility="collapsed",
    )
    st.divider()
    if module != LR5_MODULE:
        if st.button("Завантажити preset CryptoWallet (v13)", use_container_width=True):
            p = CRYPTOWALLET_PRESET
            for section, values in p.items():
                if isinstance(values, dict):
                    for k, v in values.items():
                        st.session_state[f"{section}_{k}"] = v
            st.session_state.preset_loaded = True
            st.success("Preset завантажено!")
        if st.session_state.preset_loaded:
            st.info(f"Система: {CRYPTOWALLET_PRESET['system']} (#{CRYPTOWALLET_PRESET['variant']})")
    else:
        if st.button("Завантажити демо-код ЛР-5", use_container_width=True):
            st.session_state.lr5_code_input = LR5_DEMO_CODE
            st.rerun()

# ── LR-5 ───────────────────────────────────────────────────────────────────
if module == LR5_MODULE:
    render_lr5_audit(LR5_DEMO_CODE, COLOR_MAP, status_badge)

# ── LR-6: Hierarchy ──────────────────────────────────────────────────────────
elif module == "ЛР-6: Ієрархія (SI)":
    st.subheader("Lorenz & Kidd — індекс спеціалізації (SI)")
    st.caption("Оцінка ризику агресивного успадкування класів")
    render_legend("Розшифровка скорочень (Lorenz & Kidd)", LORENZ_LEGEND, expanded=True)

    c1, c2, c3, c4 = st.columns(4)
    nm_base = c1.number_input(
        input_label(*LORENZ_INPUTS["nm_base"][:2]),
        1, 100, int(st.session_state.get("lorenz_nm_base", 7)),
        help=LORENZ_INPUTS["nm_base"][2],
    )
    noo = c2.number_input(
        input_label(*LORENZ_INPUTS["noo"][:2]),
        0, 100, int(st.session_state.get("lorenz_noo", 3)),
        help=LORENZ_INPUTS["noo"][2],
    )
    noa = c3.number_input(
        input_label(*LORENZ_INPUTS["noa"][:2]),
        0, 100, int(st.session_state.get("lorenz_noa", 4)),
        help=LORENZ_INPUTS["noa"][2],
    )
    nv = c4.number_input(
        input_label(*LORENZ_INPUTS["nv"][:2]),
        0, 100, int(st.session_state.get("lorenz_nv", 1)),
        help=LORENZ_INPUTS["nv"][2],
    )

    result = calc_lorenz(nm_base, noo, noa)
    m1, m2, m3 = st.columns(3)
    m1.metric("NM_child — методів у дочірньому класі", f"{result.nm_child:.0f}", help="NM_base + NOA")
    m2.metric("SI — індекс спеціалізації", f"{result.si:.2f}", help="(NOO + NOA) / NM_base. ≤0.5 стабільно, >1.0 ризик.")
    m3.markdown("**Статус**")
    status_badge(result.status, result.color)

    st.divider()
    st.markdown(
        "**Managerial Report:** SI > 1.0 — агресивне успадкування; "
        "рекомендовано композиція замість поглиблення ієрархії."
    )

# ── LR-6: CK ───────────────────────────────────────────────────────────────
elif module == "ЛР-6: Метрики CK":
    st.subheader("Chidamber & Kemerer — метрики класу")
    st.caption("Метрики одного класу (варіант: WalletSecurity)")
    render_legend("Розшифровка скорочень (CK)", CK_LEGEND, expanded=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    wmc = c1.number_input(
        input_label(CK_INPUTS["wmc"][0], CK_INPUTS["wmc"][1]),
        1, 200, int(st.session_state.get("ck_wmc", 12)),
        help=f"{CK_INPUTS['wmc'][2]} {CK_INPUTS['wmc'][3]}",
    )
    dit = c2.number_input(
        input_label(CK_INPUTS["dit"][0], CK_INPUTS["dit"][1]),
        1, 20, int(st.session_state.get("ck_dit", 2)),
        help=f"{CK_INPUTS['dit'][2]} {CK_INPUTS['dit'][3]}",
    )
    cbo = c3.number_input(
        input_label(CK_INPUTS["cbo"][0], CK_INPUTS["cbo"][1]),
        1, 50, int(st.session_state.get("ck_cbo", 5)),
        help=f"{CK_INPUTS['cbo'][2]} {CK_INPUTS['cbo'][3]}",
    )
    lcom = c4.number_input(
        input_label(CK_INPUTS["lcom"][0], CK_INPUTS["lcom"][1]),
        0.0, 1.0, float(st.session_state.get("ck_lcom", 0.10)), step=0.01,
        help=f"{CK_INPUTS['lcom'][2]} {CK_INPUTS['lcom'][3]}",
    )
    rfc = c5.number_input(
        input_label(CK_INPUTS["rfc"][0], CK_INPUTS["rfc"][1]),
        1, 300, int(st.session_state.get("ck_rfc", 18)),
        help=f"{CK_INPUTS['rfc'][2]} {CK_INPUTS['rfc'][3]}",
    )

    metrics = calc_ck(wmc, dit, cbo, lcom, rfc)
    rows = [
        {
            "Метрика": f"{m.name} — {CK_INPUTS[m.name.lower()][1]}",
            "Значення": m.value,
            "Статус": m.status,
            "Color": m.color,
        }
        for m in metrics
    ]
    df = pd.DataFrame(rows)

    for _, row in df.iterrows():
        col1, col2, col3 = st.columns([3, 2, 2])
        col1.write(f"**{row['Метрика']}** = {row['Значення']}")
        col2.markdown(
            f'<div style="color:{COLOR_MAP[row["Color"]]};font-weight:bold;">{row["Статус"]}</div>',
            unsafe_allow_html=True,
        )

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Метрика:N", sort=None, title="Метрика"),
        y=alt.Y("Значення:Q", title="Значення"),
        color=alt.Color("Color:N", scale=alt.Scale(domain=["green", "orange", "red"], range=["#22c55e", "#f59e0b", "#ef4444"])),
    ).properties(height=300)
    st.altair_chart(chart, use_container_width=True)

    verdict = ck_verdict(metrics)
    st.info(f"**Вердикт:** {verdict}")

# ── LR-6: MOOD ─────────────────────────────────────────────────────────────
elif module == "ЛР-6: Аналіз MOOD":
    st.subheader("MOOD — метрики об'єктно-орієнтованого дизайну")
    st.caption("Якість ОО-дизайну: інкапсуляція, успадкування, зв'язність")
    render_legend("Розшифровка всіх скорочень (MOOD)", MOOD_LEGEND, expanded=True)

    tab1, tab2, tab3 = st.tabs([
        "Інкапсуляція (MHF, AHF)",
        "Успадкування (MIF, AIF)",
        "Гнучкість і зв'язність (POF, COF)",
    ])

    with tab1:
        st.markdown("**Вхідні дані для інкапсуляції** — скільки методів і атрибутів приховано (приватні).")
        c1, c2, c3, c4 = st.columns(4)
        m_tot = mood_number_input(c1, "m_tot", MOOD_INPUTS_ENCAP, "mood_encap_m_tot", 160, min_val=1)
        m_pub = mood_number_input(c2, "m_pub", MOOD_INPUTS_ENCAP, "mood_encap_m_pub", 16)
        a_tot = mood_number_input(c3, "a_tot", MOOD_INPUTS_ENCAP, "mood_encap_a_tot", 95, min_val=1)
        a_pub = mood_number_input(c4, "a_pub", MOOD_INPUTS_ENCAP, "mood_encap_a_pub", 0)

    with tab2:
        st.markdown("**Вхідні дані для успадкування** — скільки методів/атрибутів успадковано від батьківських класів.")
        c1, c2, c3, c4 = st.columns(4)
        m_tot2 = mood_number_input(c1, "m_tot", MOOD_INPUTS_INHERIT, "mood_inherit_m_tot", 220, min_val=1)
        m_inh = mood_number_input(c2, "m_inh", MOOD_INPUTS_INHERIT, "mood_inherit_m_inh", 25)
        a_tot2 = mood_number_input(c3, "a_tot", MOOD_INPUTS_INHERIT, "mood_inherit_a_tot", 100, min_val=1)
        a_inh = mood_number_input(c4, "a_inh", MOOD_INPUTS_INHERIT, "mood_inherit_a_inh", 10)

    with tab3:
        st.markdown("**Поліморфізм і зв'язність** — перевизначені методи і реальні зв'язки між класами.")
        c1, c2, c3, c4 = st.columns(4)
        m_over = mood_number_input(c1, "m_over", MOOD_INPUTS_FLEX, "mood_flex_m_over", 40, max_val=500)
        m_max_ov = mood_number_input(c2, "m_max_ov", MOOD_INPUTS_FLEX, "mood_flex_m_max_ov", 100, min_val=1, max_val=500)
        c_act = mood_number_input(c3, "c_act", MOOD_INPUTS_FLEX, "mood_flex_c_act", 15, max_val=500)
        c_max = mood_number_input(c4, "c_max", MOOD_INPUTS_FLEX, "mood_flex_c_max", 130, min_val=1, max_val=500)

    mood = calc_mood(m_tot, m_pub, a_tot, a_pub, m_tot2, m_inh, a_tot2, a_inh, m_over, m_max_ov, c_act, c_max)

    st.markdown("### Результати")
    summary_df = pd.DataFrame([
        {
            "Метрика": f"{m.name} — {MOOD_RESULTS[m.name][1]}",
            "Результат %": round(m.pct, 2),
            "Норма": m.target,
            "Статус": m.status,
            "Пояснення": MOOD_RESULTS[m.name][2],
        }
        for m in mood["summary"]
    ])
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    mif = MOOD_RESULTS["MIF"]
    aif = MOOD_RESULTS["AIF"]
    c1.metric(
        f"MIF — {mif[1]}",
        f"{mood['mif_pct']:.1f}%",
        help=f"{mif[2]} Формула: {mif[3]}.",
    )
    c2.metric(
        f"AIF — {aif[1]}",
        f"{mood['aif_pct']:.1f}%",
        help=f"{aif[2]} Формула: {aif[3]}.",
    )

    for m in mood["summary"]:
        full = MOOD_RESULTS[m.name]
        status_badge(f"{m.name} ({full[1]}): {m.status} — {m.pct:.1f}%", m.color)
        st.caption(full[2])
        st.write("")

# ── LR-6: UCP ──────────────────────────────────────────────────────────────
elif module == "ЛР-6: Калькулятор UCP":
    st.subheader("Use Case Points та Object Points")
    render_legend("Розшифровка скорочень (UCP / OP)", UCP_LEGEND)
    tab_op, tab_ucp = st.tabs(["Object Points (OP)", "Use Case Points (UCP)"])

    with tab_op:
        p = CRYPTOWALLET_PRESET["op"]
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Екрани** — S/M/H = прості / середні / складні")
            ss = st.number_input("Екрани S — прості", value=p["screens_s"], key="ss", help="Прості форми, мало полів.")
            sm = st.number_input("Екрани M — середні", value=p["screens_m"], key="sm", help="Середня складність інтерфейсу.")
            sh = st.number_input("Екрани H — складні", value=p["screens_h"], key="sh", help="Складні форми, багато логіки.")
        with c2:
            st.markdown("**Звіти** — S/M/H")
            rs = st.number_input("Звіти S — прості", value=p["reports_s"], key="rs")
            rm = st.number_input("Звіти M — середні", value=p["reports_m"], key="rm")
            rh = st.number_input("Звіти H — складні", value=p["reports_h"], key="rh")
        with c3:
            gl3 = st.number_input("Модулі 3GL — код", value=p["gl3"], key="gl3", help="Кожен модуль 3GL = 10 Object Points.")
            prod = st.number_input("PROD — продуктивність (год/OP)", value=float(p["prod"]), key="prod")

        op_res = calc_op(ss, sm, sh, rs, rm, rh, gl3, prod)
        st.metric("OP — об'єктні точки", f"{op_res['op']:.0f}", help="Сума зважених екранів, звітів і 3GL-модулів.")
        st.metric("PM — людино-місяці", f"{op_res['pm']:.2f}", help="OP / (PROD × (1 − reuse)).")

    with tab_ucp:
        u = CRYPTOWALLET_PRESET["ucp"]
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Актори** — хто користується системою")
            as_ = st.number_input("Актори S — прості", value=u["actors_s"], key="as", help="Простий актор (вага ×1).")
            am = st.number_input("Актори M — середні", value=u["actors_m"], key="am", help="Середній актор (вага ×2).")
            ah = st.number_input("Актори H — складні", value=u["actors_h"], key="ah", help="Складний актор (вага ×3).")
        with c2:
            st.markdown("**Сценарії (use case)**")
            us = st.number_input("UC S — прості", value=u["uc_s"], key="us", help="Простий сценарій (вага ×5).")
            um = st.number_input("UC M — середні", value=u["uc_m"], key="um", help="Середній сценарій (вага ×10).")
            uh = st.number_input("UC H — складні", value=u["uc_h"], key="uh", help="Складний сценарій (вага ×15).")

        c3, c4 = st.columns(2)
        tcf = c3.number_input(
            "TCF — технічний коефіцієнт складності",
            value=u["tcf"], step=0.05,
            help="Множник технічної складності (безпека, інтеграції). >1 для фінтех.",
        )
        ecf = c4.number_input(
            "ECF — коефіцієнт середовища",
            value=u["ecf"], step=0.05,
            help="Множник досвіду команди. <1 якщо команда досвідчена.",
        )

        ucp_res = calc_ucp(as_, am, ah, us, um, uh, tcf, ecf, u["hours_per_ucp"], u["rate"])
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("UAW — вага акторів", f"{ucp_res.uaw:.0f}", help="Нескоригована вага акторів.")
        m2.metric("UUCW — вага сценаріїв", f"{ucp_res.uucw:.0f}", help="Нескоригована вага use case.")
        m3.metric("UCP — use case points", f"{ucp_res.ucp:.2f}", help="(UAW + UUCW) × TCF × ECF")
        m4.metric("Години", f"{ucp_res.hours:.0f}", help="UCP × 20 год/точку")
        st.metric("Базовий бюджет ($35/год)", f"${ucp_res.budget:,.0f}")

# ── LR-6: PERT ───────────────────────────────────────────────────────────────
else:
    st.subheader("PERT — оцінка ризиків і комерційна пропозиція")
    render_legend("Розшифровка скорочень (PERT)", PERT_LEGEND)
    u = CRYPTOWALLET_PRESET["ucp"]
    pert_p = CRYPTOWALLET_PRESET["pert"]

    ucp_res = calc_ucp(
        u["actors_s"], u["actors_m"], u["actors_h"],
        u["uc_s"], u["uc_m"], u["uc_h"],
        u["tcf"], u["ecf"], u["hours_per_ucp"], u["rate"],
    )

    c1, c2, c3 = st.columns(3)
    o = c1.number_input("O — оптимістична (дні)", value=float(pert_p["o"]), help="Найкращий сценарій.")
    m = c2.number_input("M — найімовірніша (дні)", value=float(pert_p["m"]), help="Реалістичний термін.")
    p = c3.number_input("P — песимістична (дні)", value=float(pert_p["p"]), help="Якщо все піде не так.")

    pert = calc_pert(o, m, p, ucp_res.budget)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("E — очікуваний термін (дні)", f"{pert.e:.1f}", help="E = (O + 4M + P) / 6")
    m2.metric("SD — стандартне відхилення", f"{pert.sd:.2f}", help="SD = (P − O) / 6")
    m3.metric("Безпечний дедлайн", f"{pert.safe:.1f} днів", help="E + 2×SD (~95% впевненості)")
    m4.metric("Високий ризик?", "Так" if pert.is_high_risk else "Ні")

    chart_df = pd.DataFrame({
        "id": ["opt", "exp", "ml", "pes", "safe"],
        "Оцінка": ["Оптимістична", "Очікувана", "Найімовірніша", "Песимістична", "Безпечна (95%)"],
        "Дні": [o, pert.e, m, p, pert.safe],
    })
    chart = alt.Chart(chart_df).mark_bar().encode(
        x=alt.X("Оцінка:N", sort=None, title="Оцінка"),
        y=alt.Y("Дні:Q", title="Дні"),
        color=alt.condition(
            alt.datum.id == "safe",
            alt.value("#ef4444"),
            alt.value("#3b82f6"),
        ),
    ).properties(height=320, title="Хронологія PERT")
    st.altair_chart(chart, use_container_width=True)

    st.divider()
    st.subheader("Комерційна пропозиція")
    proposal = pd.DataFrame([
        {"Стаття": "Базова розробка", "Значення": f"{ucp_res.hours:.0f} людино-годин", "Сума ($)": f"${ucp_res.budget:,.0f}"},
        {"Стаття": "Буфер на ризики", "Значення": f"{pert.risk_pct:.1f}%", "Сума ($)": f"${pert.risk_budget:,.0f}"},
        {"Стаття": "Гарантований реліз (PERT Safe)", "Значення": f"{pert.safe:.1f} днів", "Сума ($)": "—"},
        {"Стаття": "РАЗОМ", "Значення": "—", "Сума ($)": f"${pert.total_budget:,.0f}"},
    ])
    st.dataframe(proposal, use_container_width=True, hide_index=True)

    if pert.risk_pct > 25:
        st.warning("Буфер > 25% — рекомендовано зменшити невизначеність через технічний spike.")
