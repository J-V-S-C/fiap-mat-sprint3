"""Painel Streamlit de limites e derivadas aplicado a uma crise asmática."""
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from sample_cases import SCENARIOS
from simulator import (
    derivative_over_range,
    distance_to_limit,
    interpretation,
    numerical_derivative,
)


st.set_page_config(page_title="Análise matemática da SpO₂", layout="wide")
st.title("Crise asmática: análise matemática da SpO₂")
st.caption(
    "Modelo didático integrado ao caso de Carlos Mendes. "
    "Ele demonstra tendência e estabilização; não realiza previsão médica."
)

with st.sidebar:
    st.header("Configuração")
    scenario_name = st.selectbox("Cenário", list(SCENARIOS))
    t_max = st.slider("Tempo observado (min)", 5, 30, 15)
    t_point = st.slider("Instante analisado (min)", 0.0, float(t_max), 5.0, 0.5)
    st.markdown(
        "**Como demonstrar:** compare os dois cenários e observe o sinal da "
        "derivada e o limite indicado pela linha tracejada."
    )

scenario = SCENARIOS[scenario_name]
f = scenario.function
xs = np.linspace(0, t_max, 400)
ys = np.array([f(float(x)) for x in xs])
rates = derivative_over_range(f, xs)
value = f(t_point)
rate = numerical_derivative(f, t_point)
distance = distance_to_limit(value, scenario.limit)

st.subheader("Fenômeno analisado")
st.write(
    "A saturação de oxigênio (SpO₂) de um paciente com crise asmática é "
    "observada ao longo do tempo. O painel compara a piora sem a conduta e "
    "a recuperação após oxigênio suplementar."
)

formula_col, derivative_col = st.columns(2)
with formula_col:
    st.markdown("**Função da saturação**")
    st.latex(scenario.formula)
with derivative_col:
    st.markdown("**Derivada: velocidade da mudança**")
    st.latex(scenario.derivative_formula)

chart_data = pd.DataFrame(
    {"Tempo (min)": xs, "SpO2 (%)": ys, "Derivada (%/min)": rates}
)
selected_data = pd.DataFrame({"Tempo (min)": [t_point], "SpO2 (%)": [value]})

spo2_line = (
    alt.Chart(chart_data)
    .mark_line(color="#2563eb", strokeWidth=3)
    .encode(
        x=alt.X("Tempo (min):Q"),
        y=alt.Y("SpO2 (%):Q", scale=alt.Scale(domain=[80, 100])),
        tooltip=["Tempo (min):Q", alt.Tooltip("SpO2 (%):Q", format=".2f")],
    )
)
limit_line = (
    alt.Chart(pd.DataFrame({"Limite": [scenario.limit]}))
    .mark_rule(color="#16a34a", strokeDash=[6, 4])
    .encode(y="Limite:Q")
)
selected_point = (
    alt.Chart(selected_data)
    .mark_point(color="#1e293b", filled=True, size=90)
    .encode(x="Tempo (min):Q", y="SpO2 (%):Q")
)
st.altair_chart(
    (spo2_line + limit_line + selected_point).interactive(), width="stretch"
)

rate_chart = (
    alt.Chart(chart_data)
    .mark_line(color="#f97316", strokeWidth=2)
    .encode(
        x=alt.X("Tempo (min):Q"),
        y=alt.Y("Derivada (%/min):Q", title="Taxa de variação (%/min)"),
        tooltip=["Tempo (min):Q", alt.Tooltip("Derivada (%/min):Q", format=".2f")],
    )
    .properties(height=180, title="Derivada da SpO2")
    .interactive()
)
st.altair_chart(rate_chart, width="stretch")

metric1, metric2, metric3 = st.columns(3)
metric1.metric("SpO2 no instante", f"{value:.2f}%")
metric2.metric("Derivada", f"{rate:+.2f} %/min")
metric3.metric(
    "Limite quando t → ∞",
    f"{scenario.limit:.0f}%",
    f"distância {distance:.2f}",
)

st.subheader("Interpretação e apoio à decisão")
st.info(interpretation(value, rate, scenario.limit))
if scenario.is_recovery:
    if rate > 0.05:
        st.success(
            "Tendência de recuperação: a derivada positiva mostra resposta à "
            "conduta. Continue o acompanhamento até a estabilização."
        )
    else:
        st.success("A curva está próxima da estabilização esperada em 98%.")
else:
    st.error(
        "Tendência de piora: a derivada negativa indica queda da saturação. "
        "No simulador, isso sinaliza prioridade para a conduta com oxigênio."
    )

with st.expander("Explicação curta para a apresentação"):
    st.markdown(
        """
1. **Variáveis:** `t` é o tempo em minutos e `S(t)` é a SpO₂ em porcentagem.
2. **Limite:** mostra onde a saturação tende a se estabilizar no longo prazo.
3. **Derivada:** mostra quantos pontos percentuais a saturação muda por minuto.
4. **Decisão:** derivada negativa indica piora; positiva indica recuperação.

As curvas são modelos didáticos e não substituem dados ou protocolos clínicos.
"""
    )
