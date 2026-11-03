from typing import Callable
from math import isfinite

import numpy as np


def numerical_derivative(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-4,
    domain_min: float = 0.0,
) -> float:
    """Aproxima ``f'(x)`` sem avaliar tempos negativos.

    Usa diferença central no domínio e diferença progressiva de segunda ordem
    na borda ``x = domain_min``.
    """
    if x < domain_min:
        raise ValueError("O ponto deve pertencer ao domínio da função.")
    if h <= 0:
        raise ValueError("h deve ser positivo.")
    if x - h < domain_min:
        return float((-3 * f(x) + 4 * f(x + h) - f(x + 2 * h)) / (2 * h))
    return float((f(x + h) - f(x - h)) / (2 * h))


def derivative_over_range(
    f: Callable[[float], float], xs: np.ndarray, h: float = 1e-4
) -> np.ndarray:
    """Calcula a derivada numérica nos instantes informados."""
    return np.array([numerical_derivative(f, float(x), h) for x in xs])


def distance_to_limit(value: float, limit: float) -> float:
    """Retorna a distância absoluta entre um valor e o limite."""
    return abs(limit - value)


def interpretation(value: float, rate: float, limit: float) -> str:
    """Gera uma leitura curta dos numeros exibidos no painel."""
    distance = distance_to_limit(value, limit)
    if rate > 0.05:
        trend = "está aumentando"
    elif rate < -0.05:
        trend = "está diminuindo"
    else:
        trend = "está praticamente estável"
    return (
        f"A SpO2 {trend} a {abs(rate):.2f} ponto percentual por minuto. "
        f"No instante analisado vale {value:.2f}% e está a {distance:.2f} "
        f"ponto(s) do limite de {limit:.0f}%."
    )


def decision(value: float, rate: float, limit: float, cumulative_deficit: float,
             reference_deficit: float, critical_value: float = 85.0) -> str:
    """Classificação didática baseada em tendência, limite e déficit acumulado.

    O déficit de referência usa o cenário sem intervenção no mesmo intervalo.
    Não corresponde a uma recomendação clínica automática.
    """
    values = (value, rate, limit, cumulative_deficit, reference_deficit, critical_value)
    if not all(isfinite(v) for v in values):
        raise ValueError("Os indicadores precisam ser finitos.")
    if cumulative_deficit < 0 or reference_deficit < 0:
        raise ValueError("O déficit acumulado não pode ser negativo.")
    if value <= critical_value or limit <= critical_value or rate < -0.05:
        return "Em atenção"
    if rate > 0.05 and cumulative_deficit < reference_deficit:
        return "Em evolução"
    return "Estável / acompanhar"
