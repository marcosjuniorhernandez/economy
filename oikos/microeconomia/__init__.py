"""
Microeconomía - Análisis de mercados y comportamiento individual.
"""

from .mercado import Demanda, Oferta, equilibrio, excedentes
from .consumidor import (
    # Funciones de utilidad
    FuncionUtilidad,
    SustitutosPerfectos,
    ComplementariosPerfectos,
    CobbDouglas,
    CuasiLineal,
    ConcavaRaiz,
    StoneGeary,
    PreferenciasSaciadas,
    CES,
    BienMalo,
    BienNeutral,
    # Herramientas de análisis
    RestriccionPresupuestaria,
    EleccionOptima,
    CurvaIndiferencia
)

__all__ = [
    # Mercado
    'Demanda',
    'Oferta',
    'equilibrio',
    'excedentes',

    # Teoría del Consumidor - Funciones de utilidad
    'FuncionUtilidad',
    'SustitutosPerfectos',
    'ComplementariosPerfectos',
    'CobbDouglas',
    'CuasiLineal',
    'ConcavaRaiz',
    'StoneGeary',
    'PreferenciasSaciadas',
    'CES',
    'BienMalo',
    'BienNeutral',

    # Teoría del Consumidor - Herramientas
    'RestriccionPresupuestaria',
    'EleccionOptima',
    'CurvaIndiferencia'
]