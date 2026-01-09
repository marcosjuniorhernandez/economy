__version__ = "0.3.0"
__author__ = "Marcos Jr."

# ============= MICROECONOMÍA =============
from .microeconomia import (
    # Mercado
    Demanda,
    Oferta,
    equilibrio,
    excedentes,
    
    # Teoría del Consumidor
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
    RestriccionPresupuestaria,
    EleccionOptima,
    CurvaIndiferencia
)

# ============= MACROECONOMÍA =============
from .macroeconomia import (
    ISLM
)

# ============= UTILIDADES =============
from .utilidades import (
    # Parseador
    translatex,
    despejar,
    extraerVariables,

    # Visuales
    escribir,
    Lienzo,
    EstiloGrafico,
    graficoRapido,

    # Colores predefinidos - Todos disponibles sin prefijo
    ROJO, AZUL, VERDE, AMARILLO, CIAN, MAGENTA,
    NARANJA, MORADO, ROSA, LIMA,
    TURQUESA, CELESTE, VIOLETA, CORAL,
    ROJO2, AZUL2, VERDE2, AMARILLO2,
    GRIS, NEGRO,
    COLOR_DEMANDA, COLOR_OFERTA,

    # Constantes de dirección
    ARRIBA, ABAJO, IZQUIERDA, DERECHA,

    # Validadores
    validarPositivo,
    validarNoNegativo,
    validarRango,
    validarPropension,

    # Decoradores
    ayuda,
    explicacion
)

# ============= EXCEPCIONES =============
from .nucleo.excepciones import (
    ErrorOikos,
    ErrorParseador,
    ErrorEquilibrio,
    ErrorValidacion,
    ErrorGrafico
)


__all__ = [
    # Versión
    '__version__',

    # Microeconomía - Mercado
    'Demanda',
    'Oferta',
    'equilibrio',
    'excedentes',

    # Microeconomía - Teoría del Consumidor
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
    'RestriccionPresupuestaria',
    'EleccionOptima',
    'CurvaIndiferencia',

    # Macroeconomía
    'ISLM',

    # Utilidades - Parseador
    'translatex',
    'despejar',
    'extraerVariables',

    # Utilidades - Visuales (disponibles directamente)
    'escribir',
    'Lienzo',
    'EstiloGrafico',
    'graficoRapido',

    # Colores (disponibles directamente sin prefijo)
    'ROJO', 'AZUL', 'VERDE', 'AMARILLO', 'CIAN', 'MAGENTA',
    'NARANJA', 'MORADO', 'ROSA', 'LIMA',
    'TURQUESA', 'CELESTE', 'VIOLETA', 'CORAL',
    'ROJO2', 'AZUL2', 'VERDE2', 'AMARILLO2',
    'GRIS', 'NEGRO',
    'COLOR_DEMANDA', 'COLOR_OFERTA',

    # Constantes de dirección
    'ARRIBA', 'ABAJO', 'IZQUIERDA', 'DERECHA',

    # Validadores
    'validarPositivo',
    'validarNoNegativo',
    'validarRango',
    'validarPropension',

    # Decoradores
    'ayuda',
    'explicacion',

    # Excepciones
    'ErrorOikos',
    'ErrorParseador',
    'ErrorEquilibrio',
    'ErrorValidacion',
    'ErrorGrafico'
]


# ============= ATAJO PARA FACILITAR USO =============
# Ahora puedes hacer: import oikos as ok
# Y usar directamente: ok.escribir(), ok.ROJO, ok.Lienzo(), etc.


def info():
    """
    Muestra información sobre Oikos.
    """
    print(f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                      OIKOS v{__version__}                              ║
    ║            Librería para Economía en Python                      ║
    ╚══════════════════════════════════════════════════════════════════╝
    
    Módulos disponibles:
       • Microeconomia: Demanda, Oferta, Equilibrio
       • Macroeconomia: IS-LM, OA-DA (próximamente)
            
    Documentación: https://oikos.readthedocs.io/en/latest/manual/
    """)