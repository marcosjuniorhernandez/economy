"""
Utilidades de Oikos - Herramientas generales.

Este módulo contiene funciones de utilidad para parsear ecuaciones,
validar parámetros económicos, crear visualizaciones y decorar código
con información pedagógica.
"""

# Imports locales
from .decoradores import (
    ayuda,
    deprecado,
    explicacion,
    memorizarResultado,
    validarEconomico,
)
from .parseador import despejar, extraerVariables, translatex
from .validadores import (
    validarEcuacion,
    validarElasticidad,
    validarNoNegativo,
    validarPositivo,
    validarPropension,
    validarRango,
)
from .visuales import (
    ABAJO,
    AMARILLO,
    AMARILLO2,
    ARRIBA,
    AZUL,
    AZUL2,
    CELESTE,
    CIAN,
    COLOR_DEMANDA,
    COLOR_OFERTA,
    CORAL,
    DERECHA,
    EstiloGrafico,
    GRIS,
    IZQUIERDA,
    Lienzo,
    LIMA,
    MAGENTA,
    MORADO,
    NARANJA,
    NEGRO,
    ROJO,
    ROJO2,
    ROSA,
    TURQUESA,
    VERDE,
    VERDE2,
    VIOLETA,
    escribir,
    graficoRapido,
)

__all__ = [
    # Parseador
    "despejar",
    "extraerVariables",
    "translatex",
    # Validadores
    "validarEcuacion",
    "validarElasticidad",
    "validarNoNegativo",
    "validarPositivo",
    "validarPropension",
    "validarRango",
    # Visuales
    "escribir",
    "EstiloGrafico",
    "graficoRapido",
    "Lienzo",
    # Colores
    "AMARILLO",
    "AMARILLO2",
    "AZUL",
    "AZUL2",
    "CELESTE",
    "CIAN",
    "COLOR_DEMANDA",
    "COLOR_OFERTA",
    "CORAL",
    "GRIS",
    "LIMA",
    "MAGENTA",
    "MORADO",
    "NARANJA",
    "NEGRO",
    "ROJO",
    "ROJO2",
    "ROSA",
    "TURQUESA",
    "VERDE",
    "VERDE2",
    "VIOLETA",
    # Constantes de dirección
    "ABAJO",
    "ARRIBA",
    "DERECHA",
    "IZQUIERDA",
    # Decoradores
    "ayuda",
    "deprecado",
    "explicacion",
    "memorizarResultado",
    "validarEconomico",
]