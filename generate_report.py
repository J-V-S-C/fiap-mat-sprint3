"""Gera o PDF único de apresentação da Sprint 4 de DPS."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

from sample_cases import CRITICAL_SPO2, SCENARIOS
from simulator import decision, numerical_derivative


OUTPUT = Path(__file__).with_name("ENTREGA_DPS_SPRINT4.pdf")
PERIOD = 10.0


def text_page(pdf: PdfPages) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.patch.set_facecolor("#f8fafc")
    fig.text(0.08, 0.93, "FIAP  |  Challenge Hospital Moinhos de Vento", fontsize=11, color="#475569")
    fig.text(0.08, 0.86, "DPS - Sprint 4", fontsize=26, weight="bold", color="#0f172a")
    fig.text(0.08, 0.81, "Da curva à decisão no Simulador Clínico", fontsize=15, color="#334155")
    team = Path(__file__).with_name("INTEGRANTES.txt").read_text(encoding="utf-8")
    fig.text(0.08, 0.75, "Equipe: " + team.replace("Integrantes:", "").strip().replace("• ", ""),
             fontsize=9, va="top", linespacing=1.6)
    sections = [
        (0.60, "Problema e dados", [
            "O MVP treina decisões em atendimentos fictícios. O caso de síndrome coronariana",
            "no backend começa com SpO2 de 90% e marca 85% como valor crítico.",
            "Esses dois valores vêm do caso do produto; as curvas são hipóteses didáticas.",
        ]),
        (0.48, "Evolução da Sprint 3", [
            "A Sprint 3 mostrava tendência por limite e velocidade por derivada.",
            "Nesta Sprint 4, o caso foi alinhado ao MVP e acrescentou-se a integral",
            "do déficit acumulado, a comparação de cenários e uma regra de decisão.",
        ]),
        (0.36, "Três conceitos usados em conjunto", [
            "Limite: patamar para o qual a curva tende no longo prazo.",
            "Derivada: direção e intensidade da mudança em cada instante.",
            "Integral: área de 100 - SpO2 entre 0 e T, em pp.min.",
        ]),
        (0.23, "Relação com o produto", [
            "O painel Streamlit deste repositório usa o caso e o limite crítico do MVP",
            "e fornece a classificação didática. Seu link para o simulador publicado",
            "permite navegar entre a análise matemática e o atendimento.",
        ]),
    ]
    for y, title, lines in sections:
        fig.text(0.08, y, title, fontsize=13, weight="bold", color="#0f172a")
        fig.text(0.08, y - 0.035, "\n".join(lines), fontsize=10, va="top", linespacing=1.6)
    fig.text(0.08, 0.06, "Modelos educacionais. Não são previsões nem recomendações médicas.",
             fontsize=9, color="#64748b")
    pdf.savefig(fig)
    plt.close(fig)


def analysis_page(pdf: PdfPages) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.suptitle("Tendência, evolução e acúmulo", x=0.08, y=0.96,
                 ha="left", fontsize=19, weight="bold")
    xs = np.linspace(0, PERIOD, 301)
    ax1 = fig.add_axes((0.12, 0.55, 0.78, 0.25))
    ax2 = fig.add_axes((0.12, 0.27, 0.78, 0.22))
    colors = ["#dc2626", "#2563eb"]
    for (name, scenario), color in zip(SCENARIOS.items(), colors):
        ax1.plot(xs, [scenario.function(float(t)) for t in xs], label=name, color=color, linewidth=2.5)
        ax2.plot(xs, [scenario.deficit_integral(float(t)) for t in xs], label=name,
                 color=color, linewidth=2.5)
    ax1.axhline(CRITICAL_SPO2, color="#64748b", linestyle="--", label="Valor crítico 85%")
    ax1.set(ylabel="SpO2 (%)", xlabel="Tempo (min)", ylim=(84, 99), title="Curvas de SpO2")
    ax2.set(ylabel="Déficit (pp.min)", xlabel="Tempo (min)", title="Integral acumulada de 100 - SpO2")
    ax1.legend(loc="upper right", fontsize=8)
    for ax in (ax1, ax2):
        ax.grid(alpha=0.2)
    fig.text(0.08, 0.88, "Sem intervenção: S(t) = 85 + 5e^(-t/6);  S'(t) = -(5/6)e^(-t/6)", fontsize=10)
    fig.text(0.08, 0.855, "Com oxigênio: S(t) = 97 - 7e^(-t/3);  S'(t) = (7/3)e^(-t/3)", fontsize=10)
    fig.text(0.08, 0.22, "D(T) = integral de [100 - S(t)] de 0 até T", fontsize=10, weight="bold")
    fig.text(0.08, 0.195, "Sem intervenção: D(T) = 15T - 30[1 - e^(-T/6)]", fontsize=10)
    fig.text(0.08, 0.17, "Com oxigênio: D(T) = 3T + 21[1 - e^(-T/3)]", fontsize=10)
    fig.text(0.08, 0.10,
             "A área azul menor indica menos déficit acumulado no mesmo intervalo.\n"
             "A integral compara exposição ao déficit; não representa risco clínico validado.",
             fontsize=9, linespacing=1.5, color="#475569")
    pdf.savefig(fig)
    plt.close(fig)


def decision_page(pdf: PdfPages) -> None:
    fig = plt.figure(figsize=(8.27, 11.69))
    fig.suptitle("Interpretação e regra de decisão", x=0.08, y=0.96,
                 ha="left", fontsize=19, weight="bold")
    base_deficit = SCENARIOS["Sem intervenção (piora)"].deficit_integral(PERIOD)
    lines = []
    for name, scenario in SCENARIOS.items():
        value = scenario.function(PERIOD)
        rate = numerical_derivative(scenario.function, PERIOD)
        deficit = scenario.deficit_integral(PERIOD)
        result = decision(value, rate, scenario.limit, deficit, base_deficit, CRITICAL_SPO2)
        lines.extend([
            name,
            f"  SpO2 em 10 min: {value:.2f}%  |  derivada: {rate:+.2f} pp/min",
            f"  limite: {scenario.limit:.0f}%  |  integral: {deficit:.2f} pp.min",
            f"  classificação: {result}",
            "",
        ])
    fig.text(0.08, 0.86, "Exemplo comparável: T = 10 minutos", fontsize=13, weight="bold")
    fig.text(0.08, 0.82, "\n".join(lines), fontsize=11, va="top", linespacing=1.8)
    fig.text(0.08, 0.57, "Regra programada no painel", fontsize=13, weight="bold")
    fig.text(0.08, 0.53,
             "1. Em atenção: SpO2 <= 85%, limite <= 85% ou derivada < -0,05 pp/min.\n"
             "2. Em evolução: derivada > +0,05 pp/min e integral menor que a referência.\n"
             "3. Estável / acompanhar: demais situações.",
             fontsize=10, va="top", linespacing=1.8)
    fig.text(0.08, 0.40, "Análise crítica", fontsize=13, weight="bold")
    fig.text(0.08, 0.36,
             "A curva sem intervenção tende a 85%, mas não chega lá durante os 10 min.\n"
             "A curva com oxigênio tende a 97% e reduz o déficit acumulado. O valor\n"
             "de 100% é uma referência matemática comum, não uma meta terapêutica.\n"
             "As curvas não foram ajustadas a dados de pacientes ou de usuários.\n"
             "A API do MVP usa regras discretas; este painel explica o raciocínio,\n"
             "sem substituir o resultado real exibido pelo simulador.",
             fontsize=10, va="top", linespacing=1.7)
    fig.text(0.08, 0.16, "Fonte e acesso", fontsize=13, weight="bold")
    fig.text(0.08, 0.12,
             "Caso-base: backend/sample_data.py do Simulador Clínico.\n"
             "MVP: https://simulador-clinico-front.vercel.app\n"
             "Código e painel: https://github.com/J-V-S-C/fiap-mat-sprint3",
             fontsize=9, va="top", linespacing=1.6)
    pdf.savefig(fig)
    plt.close(fig)


def main() -> None:
    with PdfPages(OUTPUT) as pdf:
        text_page(pdf)
        analysis_page(pdf)
        decision_page(pdf)
    print(f"PDF gerado: {OUTPUT}")


if __name__ == "__main__":
    main()
