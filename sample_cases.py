"""Cenários didáticos de SpO₂ para o caso de síndrome coronariana do MVP.

O caso do backend começa em 90% e marca 85% como valor crítico. As curvas
exponenciais abaixo são aproximações para a análise matemática; não reproduzem
as transições discretas nem a avaliação de condutas do simulador clínico.
"""

from dataclasses import dataclass
from math import exp, isfinite
from typing import Callable


CASE_NAME = "Síndrome coronariana - caso didático"
INITIAL_SPO2 = 90.0
CRITICAL_SPO2 = 85.0
REFERENCE_SPO2 = 100.0


def _validate_time(t: float) -> None:
    if not isfinite(t) or t < 0:
        raise ValueError("O tempo deve ser finito e não negativo.")


def spo2_without_oxygen(t: float) -> float:
    """Piora didática: 90% inicialmente, aproximando-se de 85%."""
    _validate_time(t)
    return 85 + 5 * exp(-t / 6)


def spo2_with_oxygen(t: float) -> float:
    """Recuperação didática: 90% inicialmente, aproximando-se de 97%."""
    _validate_time(t)
    return 97 - 7 * exp(-t / 3)


def deficit_without_oxygen(t: float) -> float:
    """Integral de 100 - S(t) de 0 a t, em pontos percentuais × minuto."""
    _validate_time(t)
    return 15 * t - 30 * (1 - exp(-t / 6))


def deficit_with_oxygen(t: float) -> float:
    """Integral de 100 - S(t) de 0 a t, em pontos percentuais × minuto."""
    _validate_time(t)
    return 3 * t + 21 * (1 - exp(-t / 3))


@dataclass(frozen=True)
class ClinicalScenario:
    function: Callable[[float], float]
    deficit_integral: Callable[[float], float]
    formula: str
    derivative_formula: str
    integral_formula: str
    limit: float
    is_recovery: bool


SCENARIOS = {
    "Sem intervenção (piora)": ClinicalScenario(
        function=spo2_without_oxygen,
        deficit_integral=deficit_without_oxygen,
        formula=r"S(t)=85+5e^{-t/6}",
        derivative_formula=r"S'(t)=-\frac{5}{6}e^{-t/6}",
        integral_formula=r"D(T)=\int_0^T(100-S(t))\,dt=15T-30(1-e^{-T/6})",
        limit=85.0,
        is_recovery=False,
    ),
    "Após oxigênio (recuperação)": ClinicalScenario(
        function=spo2_with_oxygen,
        deficit_integral=deficit_with_oxygen,
        formula=r"S(t)=97-7e^{-t/3}",
        derivative_formula=r"S'(t)=\frac{7}{3}e^{-t/3}",
        integral_formula=r"D(T)=\int_0^T(100-S(t))\,dt=3T+21(1-e^{-T/3})",
        limit=97.0,
        is_recovery=True,
    ),
}
