"""
Núcleo de Oikos - Clases base y excepciones.

Este módulo contiene las clases abstractas base que definen la estructura
común de todos los modelos económicos, así como el sistema de excepciones
personalizado para manejo de errores.
"""

# Imports locales
from .base import FuncionEconomica, MercadoBase, ModeloEconomico
from .excepciones import (
    ErrorEquilibrio,
    ErrorGrafico,
    ErrorOikos,
    ErrorParseador,
    ErrorValidacion,
)

__all__ = [
    "FuncionEconomica",
    "MercadoBase",
    "ModeloEconomico",
    "ErrorEquilibrio",
    "ErrorGrafico",
    "ErrorOikos",
    "ErrorParseador",
    "ErrorValidacion",
]