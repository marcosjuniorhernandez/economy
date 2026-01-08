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
    # Colores predefinidos - Ahora disponibles sin prefijo
    ROJO, AZUL, VERDE, AMARILLO, CIAN, MAGENTA,
    NARANJA, MORADO, ROSA, LIMA,
    TURQUESA, CELESTE, VIOLETA, CORAL,
    ROJO2, AZUL2, VERDE2, AMARILLO2,
    GRIS, NEGRO,
    COLOR_DEMANDA, COLOR_OFERTA
)
from .decoradores import (
    ayuda,
    explicacion,
    validarEconomico,
    memorizarResultado,
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

    # Colores - Todos exportados para uso directo
    'ROJO', 'AZUL', 'VERDE', 'AMARILLO', 'CIAN', 'MAGENTA',
    'NARANJA', 'MORADO', 'ROSA', 'LIMA',
    'TURQUESA', 'CELESTE', 'VIOLETA', 'CORAL',
    'ROJO2', 'AZUL2', 'VERDE2', 'AMARILLO2',
    'GRIS', 'NEGRO',
    'COLOR_DEMANDA', 'COLOR_OFERTA',

    # Decoradores
    'ayuda',
    'explicacion',
    'validarEconomico',
    'memorizarResultado',
    'deprecado'
]