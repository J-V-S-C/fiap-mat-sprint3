"""Modelos didáticos para a análise da SpO₂ no caso de crise asmática.

O instante ``t = 0`` representa o início da observação. Os modelos não são
previsões médicas: apenas tornam limite e derivada visíveis no simulador.
"""
from dataclasses import dataclass
from math import exp
from typing import Callable


def _validate_time(t: float) -> None:
    if t < 0:
        raise ValueError("O tempo não pode ser negativo.")


def spo2_without_oxygen(t: float) -> float:
    """SpO₂ em piora: parte de 92% e se aproxima de 82%."""
    _validate_time(t)
    return 82 + 10 * exp(-t / 6)


def spo2_with_oxygen(t: float) -> float:
    """SpO₂ em recuperação: parte de 92% e se aproxima de 98%."""
    _validate_time(t)
    return 98 - 6 * exp(-t / 3)


@dataclass(frozen=True)
class ClinicalScenario:
    """Dados necessários para calcular e apresentar um cenário."""

    function: Callable[[float], float]
    formula: str
    derivative_formula: str
    limit: float
    is_recovery: bool


SCENARIOS = {
    "Sem oxigênio (piora)": ClinicalScenario(
        function=spo2_without_oxygen,
        formula=r"S(t)=82+10e^{-t/6}",
        derivative_formula=r"S'(t)=-\frac{10}{6}e^{-t/6}",
        limit=82.0,
        is_recovery=False,
    ),
    "Com oxigênio (recuperação)": ClinicalScenario(
        function=spo2_with_oxygen,
        formula=r"S(t)=98-6e^{-t/3}",
        derivative_formula=r"S'(t)=2e^{-t/3}",
        limit=98.0,
        is_recovery=True,
    ),
}
