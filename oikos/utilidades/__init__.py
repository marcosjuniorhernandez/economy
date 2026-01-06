"""
Utilidades de Oikos - Herramientas generales.
"""

from .parseador import translatex, despejar, extraerVariables
from .validadores import (
    validarPositivo,
    validarNoNegativo,
    validarRango,
    validarPropension,
    validarElasticidad,
    validarEcuacion
)
from .visuales import (
    escribir,
    Lienzo,
    EstiloGrafico,
    graficoRapido,
    # Colores predefinidos
    ROJO, AZUL, VERDE, AMARILLO, NARANJA, MORADO, TURQUESA, ROSA
)
from .decoradores import (
    ayuda,
    explicacion,
    validarEconomico,
    memoizarResultado,
    deprecado
)

__all__ = [
    # Parseador
    'translatex',
    'despejar',
    'extraerVariables',

    # Validadores
    'validarPositivo',
    'validarNoNegativo',
    'validarRango',
    'validarPropension',
    'validarElasticidad',
    'validarEcuacion',

    # Visuales
    'escribir',
    'Lienzo',
    'EstiloGrafico',
    'graficoRapido',
    'ROJO', 'AZUL', 'VERDE', 'AMARILLO', 'NARANJA', 'MORADO', 'TURQUESA', 'ROSA',

    # Decoradores
    'ayuda',
    'explicacion',
    'validarEconomico',
    'memoizarResultado',
    'deprecado'
]