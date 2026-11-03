"""Painel DPS Sprint 4: limite, derivada e integral para o caso do MVP."""

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from sample_cases import CASE_NAME, CRITICAL_SPO2, SCENARIOS
from simulator import decision, numerical_derivative


st.set_page_config(page_title="Análise matemática da SpO₂", layout="wide")
st.title("SpO₂ no caso de síndrome coronariana")
st.caption(
    "Painel matemático complementar ao "
    "[Simulador Clínico](https://simulador-clinico-front.vercel.app). "
    "As curvas são cenários didáticos, não dados medidos nem previsões clínicas."
)

with st.sidebar:
    st.header("Período e cenário")
    t_max = st.slider("Período do atendimento (min)", 1, 10, 10)
    t_point = st.slider("Instante de análise (min)", 0.0, float(t_max), float(t_max), 0.5)
    scenario_name = st.selectbox("Cenário para a decisão", list(SCENARIOS))

scenario = SCENARIOS[scenario_name]
reference = SCENARIOS["Sem intervenção (piora)"]
value = scenario.function(t_point)
rate = numerical_derivative(scenario.function, t_point)
deficit = scenario.deficit_integral(t_point)
reference_deficit = reference.deficit_integral(t_point)
classification = decision(value, rate, scenario.limit, deficit, reference_deficit, CRITICAL_SPO2)

st.write(
    f"**Caso relacionado ao MVP:** {CASE_NAME}. O caso publicado no código da API "
    f"começa com SpO₂ de 90% e usa {CRITICAL_SPO2:.0f}% como limite crítico. "
    "O painel compara trajetórias matemáticas plausíveis a partir desse ponto. "
    "A API aplica suas próprias regras discretas e pode produzir outros valores."
)

st.subheader("Tendência, evolução e acúmulo")
st.latex(scenario.formula)
formula_a, formula_b = st.columns(2)
with formula_a:
    st.markdown("**Derivada — velocidade da variação**")
    st.latex(scenario.derivative_formula)
with formula_b:
    st.markdown("**Integral — déficit acumulado em relação a 100%**")
    st.latex(scenario.integral_formula)

xs = np.linspace(0, t_max, 201)
rows = [
    {
        "Tempo (min)": float(t),
        "SpO₂ (%)": item.function(float(t)),
        "Déficit acumulado (pp·min)": item.deficit_integral(float(t)),
        "Cenário": name,
    }
    for name, item in SCENARIOS.items()
    for t in xs
]
chart_data = pd.DataFrame(rows)
spo2_chart = (
    alt.Chart(chart_data)
    .mark_line(strokeWidth=3)
    .encode(
        x=alt.X("Tempo (min):Q"),
        y=alt.Y("SpO₂ (%):Q", scale=alt.Scale(domain=[84, 100])),
        color="Cenário:N",
        tooltip=["Cenário:N", "Tempo (min):Q", alt.Tooltip("SpO₂ (%):Q", format=".2f")],
    )
    .properties(title="Trajetórias comparadas de SpO₂", height=300)
)
critical_line = (
    alt.Chart(pd.DataFrame({"Valor crítico": [CRITICAL_SPO2]}))
    .mark_rule(color="#dc2626", strokeDash=[5, 5])
    .encode(y="Valor crítico:Q")
)
deficit_chart = (
    alt.Chart(chart_data)
    .mark_line(strokeWidth=3)
    .encode(
        x=alt.X("Tempo (min):Q"),
        y="Déficit acumulado (pp·min):Q",
        color="Cenário:N",
        tooltip=[
            "Cenário:N",
            "Tempo (min):Q",
            alt.Tooltip("Déficit acumulado (pp·min):Q", format=".2f"),
        ],
    )
    .properties(title="Área acumulada de 100 − SpO₂", height=300)
)
left, right = st.columns(2)
with left:
    st.altair_chart((spo2_chart + critical_line).interactive(), width="stretch")
with right:
    st.altair_chart(deficit_chart.interactive(), width="stretch")

m1, m2, m3, m4 = st.columns(4)
m1.metric("SpO₂ no instante", f"{value:.2f}%")
m2.metric("Derivada", f"{rate:+.2f} pp/min")
m3.metric("Limite da curva", f"{scenario.limit:.0f}%")
m4.metric("Déficit acumulado", f"{deficit:.2f} pp·min")

st.subheader("Regra de decisão do exercício")
st.info(
    f"**{classification}** no instante {t_point:g} min. "
    f"Comparação no mesmo intervalo: {deficit:.2f} pp·min no cenário selecionado "
    f"e {reference_deficit:.2f} pp·min sem intervenção."
)
st.markdown(
    "- **Em atenção:** SpO₂ no valor crítico, limite projetado no valor crítico "
    "ou derivada negativa relevante.\n"
    "- **Em evolução:** derivada positiva e déficit acumulado menor que o cenário "
    "sem intervenção.\n"
    "- **Estável / acompanhar:** demais situações, inclusive variação pequena."
)
st.caption(
    "O déficit é a integral de (100 − SpO₂) no intervalo observado. "
    "Sua unidade é ponto percentual × minuto; não é uma probabilidade nem um diagnóstico. "
    "O valor de 100% é uma referência matemática comum aos dois cenários, "
    "não uma meta terapêutica."
)

with st.expander("Dados e interpretação crítica"):
    st.write(
        "Fonte do ponto inicial e do valor crítico: caso didático de síndrome "
        "coronariana em `backend/sample_data.py` do projeto. Os demais parâmetros "
        "são hipóteses didáticas escolhidas para comparar piora e recuperação. "
        "A análise não usa medições reais de pacientes nem resultados da validação "
        "com estudantes. A integral resume a exposição ao déficit no período; "
        "a derivada indica a direção instantânea; o limite descreve a tendência "
        "da função se o tempo continuasse além da simulação."
    )
    st.write(
        "Como o simulador dura no máximo 10 minutos e atualiza o paciente por "
        "regras próprias, os limites em tempo infinito não são desfechos previstos "
        "para um atendimento específico. Use a classificação somente para explicar "
        "o raciocínio matemático do MVP."
    )
