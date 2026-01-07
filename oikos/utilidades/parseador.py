"""
Parseador de ecuaciones económicas en LaTeX.

Convierte expresiones matemáticas escritas en LaTeX a objetos SymPy
que pueden ser manipulados simbólicamente.
"""

from latex2sympy2 import latex2sympy
from sympy import symbols, solve, Eq
from typing import Optional, Union, Tuple
from ..nucleo.excepciones import ErrorParseador


def translatex(expresionLatex: str, variableDespejar: Optional[str] = None):
    """
    Convierte una expresión en LaTeX a SymPy y opcionalmente la despeja.
    
    Esta función es inteligente y puede:
    1. Detectar automáticamente ecuaciones con '='
    2. Despejar variables sin que el usuario lo especifique
    3. Manejar expresiones sin igualdad
    
    Args:
        expresionLatex: Ecuación o expresión en formato LaTeX
                        Ejemplos: "Q = 100 - 2P", "P^2 + Q", "C = 200 + 0.8Y_d"

        variableDespejar: (Opcional) Variable a despejar. Si es None, 
                          la función intenta detectarla automáticamente.
    
    Returns:
        Expresión de SymPy lista para usar
        
    Raises:
        ErrorParseador: Si no se puede parsear la expresión
        
    Ejemplos:
        >>> # Ecuación simple
        >>> demanda = translatex("Q = 100 - 2P")
        >>> # Detecta automáticamente que debe despejar
        
        >>> # Expresión sin igualdad
        >>> demamnda = translatex("P^2 + 3Q")
        >>> # Retorna la expresión tal cual
        
        >>> # Forzar despeje de variable específica
        >>> demanda = translatex("Q = 100 - 2P", variableDespejar="P")
        >>> # Despeja P en función de Q
    """
    try:
        # Limpiamos espacios y verificamos si hay igualdad
        expresionLatex = expresionLatex.strip()
        tieneIgualdad = "=" in expresionLatex
        
        if tieneIgualdad:
            # Separamos los lados de la ecuación
            ladoIzquierdo, ladoDerecho = expresionLatex.split("=", 1)
            
            # Convertimos cada lado a SymPy
            izq = latex2sympy(ladoIzquierdo.strip())
            der = latex2sympy(ladoDerecho.strip())
            
            # Si el usuario especificó variable, despejamos
            if variableDespejar:
                variable = symbols(variableDespejar)
                ecuacion = Eq(izq, der)
                solucion = solve(ecuacion, variable)
                
                if not solucion:
                    raise ErrorParseador(
                        expresionLatex,
                        f"No se pudo despejar {variableDespejar}"
                    )
                
                # Retornamos la primera solución
                return solucion[0] if len(solucion) == 1 else solucion
            
            # IMPORTANTE: NO despejamos automáticamente
            # Las clases Demanda/Oferta necesitan la ecuación completa para poder
            # despejar P o Q según lo necesiten
            # Retornamos siempre la ecuación completa como Eq(izq, der)
            return Eq(izq, der)
        
        else:
            # No hay igualdad, solo parseamos la expresión
            return latex2sympy(expresionLatex)
    
    except Exception as e:
        raise ErrorParseador(
            expresionLatex,
            f"Error al parsear: {str(e)}"
        )


def despejar(ecuacion, variable: str):
    """
    Despeja una variable de una ecuación.
    
    Args:
        ecuacion: Ecuación de SymPy o string en LaTeX
        variable: Nombre de la variable a despejar
        
    Returns:
        Expresión despejada
        
    Ejemplo:
        >>> from sympy import symbols
        >>> P, Q = symbols('P Q')
        >>> ecuacion = Q - (100 - 2*P)
        >>> resultado = despejar(ecuacion, 'P')
        >>> # Retorna: P = (100 - Q) / 2
    """
    if isinstance(ecuacion, str):
        ecuacion = translatex(ecuacion)
    
    varSym = symbols(variable)
    solucion = solve(ecuacion, varSym)
    
    if not solucion:
        raise ErrorParseador(
            str(ecuacion),
            f"No se pudo despejar {variable}"
        )
    
    return solucion[0] if len(solucion) == 1 else solucion


def extraerVariables(expresion: str) -> list:
    """
    Extrae todas las variables de una expresión LaTeX.

    Args:
        expresion: Expresión en LaTeX

    Returns:
        Lista de nombres de variables encontradas

    Ejemplo:
        >>> vars = extraerVariables("C = 200 + 0.8(Y - T)")
        >>> print(vars)
        ['C', 'Y', 'T']
    """
    try:
        expr = translatex(expresion)
        simbolos = list(expr.free_symbols)
        return [str(s) for s in simbolos]
    except (ErrorParseador, ValueError, AttributeError, TypeError):
        # Si no se puede parsear, retornar lista vacía
        return []