"""
Oikos - Librería para Economía en Python.

Biblioteca educativa que facilita el análisis económico mediante
modelos de microeconomía, macroeconomía y herramientas de visualización.
"""

__version__ = "0.3.0"
__author__ = "Marcos Junior Hernández-Moreno"

# Imports locales (módulos de Oikos)
from .macroeconomia import ISLM
from .microeconomia import (
    BienEconomico,
    BienMalo,
    BienNeutral,
    CES,
    CobbDouglas,
    ComplementariosPerfectos,
    ConcavaRaiz,
    CuasiLineal,
    CurvaIndiferencia,
    Demanda,
    EleccionOptima,
    FactoresEspecificos,
    FPP,
    FuncionUtilidad,
    Oferta,
    PreferenciasSaciadas,
    RestriccionPresupuestaria,
    Ricardiano,
    StoneGeary,
    SustitutosPerfectos,
    equilibrio,
    excedentes,
)
from .nucleo.excepciones import (
    ErrorEquilibrio,
    ErrorGrafico,
    ErrorOikos,
    ErrorParseador,
    ErrorValidacion,
)
from .utilidades import (
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
    ayuda,
    despejar,
    escribir,
    explicacion,
    extraerVariables,
    graficoRapido,
    translatex,
    validarNoNegativo,
    validarPositivo,
    validarPropension,
    validarRango,
)


__all__ = [
    # Versión y metadata
    "__version__",
    # Microeconomía - Mercado
    "Demanda",
    "Oferta",
    "equilibrio",
    "excedentes",
    # Microeconomía - Teoría del Consumidor
    "BienEconomico",
    "BienMalo",
    "BienNeutral",
    "CES",
    "CobbDouglas",
    "ComplementariosPerfectos",
    "ConcavaRaiz",
    "CuasiLineal",
    "CurvaIndiferencia",
    "EleccionOptima",
    "FactoresEspecificos",
    "FPP",
    "FuncionUtilidad",
    "PreferenciasSaciadas",
    "RestriccionPresupuestaria",
    "Ricardiano",
    "StoneGeary",
    "SustitutosPerfectos",
    # Macroeconomía
    "ISLM",
    # Utilidades - Parseador
    "despejar",
    "extraerVariables",
    "translatex",
    # Utilidades - Visuales
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
    # Validadores
    "validarNoNegativo",
    "validarPositivo",
    "validarPropension",
    "validarRango",
    # Decoradores
    "ayuda",
    "explicacion",
    # Excepciones
    "ErrorEquilibrio",
    "ErrorGrafico",
    "ErrorOikos",
    "ErrorParseador",
    "ErrorValidacion",
]


def info():
    """
    Muestra información sobre Oikos.
    """
    print(f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                      OIKOS v{__version__}                              ║
    ║            Librería para Economía en Python                      ║
    ╚══════════════════════════════════════════════════════════════════╝
                
    Documentación: https://oikos.readthedocs.io/en/latest/manual/
    """)