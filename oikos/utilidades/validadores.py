"""
Validadores para inputs económicos.

Funciones que verifican que los parámetros económicos sean válidos
antes de usarlos en los modelos.
"""

from typing import Union, Optional
from ..nucleo.excepciones import ErrorValidacion


def validarPositivo(valor: Union[int, float], nombre: str = "valor") -> float:
    """
    Valida que un valor sea positivo.
    
    Args:
        valor: Número a validar
        nombre: Nombre del parámetro (para el mensaje de error)
        
    Returns:
        El valor si es válido
        
    Raises:
        ErrorValidacion: Si el valor no es positivo
        
    Ejemplo:
        >>> precio = validarPositivo(10, "precio")
        >>> # OK, retorna 10
        
        >>> precio = validarPositivo(-5, "precio")
        >>> # Lanza ErrorValidacion
    """
    try:
        valor_num = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(nombre, f"{nombre} debe ser un número")
    
    if valor_num <= 0:
        raise ErrorValidacion(nombre, f"{nombre} debe ser positivo, recibido: {valor_num}")
    
    return valor_num


def validarNoNegativo(valor: Union[int, float], nombre: str = "valor") -> float:
    """
    Valida que un valor sea no negativo (≥ 0).
    
    Args:
        valor: Número a validar
        nombre: Nombre del parámetro
        
    Returns:
        El valor si es válido
        
    Raises:
        ErrorValidacion: Si el valor es negativo
    """
    try:
        valor_num = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(nombre, f"{nombre} debe ser un número")
    
    if valor_num < 0:
        raise ErrorValidacion(nombre, f"{nombre} no puede ser negativo, recibido: {valor_num}")
    
    return valor_num


def validarRango(valor: Union[int, float], 
                 minimo: Optional[float] = None,
                 maximo: Optional[float] = None,
                 nombre: str = "valor") -> float:
    """
    Valida que un valor esté dentro de un rango.
    
    Args:
        valor: Número a validar
        minimo: Valor mínimo permitido (inclusive)
        maximo: Valor máximo permitido (inclusive)
        nombre: Nombre del parámetro
        
    Returns:
        El valor si está en el rango
        
    Raises:
        ErrorValidacion: Si está fuera del rango
        
    Ejemplo:
        >>> # Validar que la propensión marginal esté entre 0 y 1
        >>> pmc = validarRango(0.8, 0, 1, "propension_marginal_consumir")
    """
    try:
        valor_num = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(nombre, f"{nombre} debe ser un número")
    
    if minimo is not None and valor_num < minimo:
        raise ErrorValidacion(
            nombre, 
            f"{nombre} debe ser ≥ {minimo}, recibido: {valor_num}"
        )
    
    if maximo is not None and valor_num > maximo:
        raise ErrorValidacion(
            nombre,
            f"{nombre} debe ser ≤ {maximo}, recibido: {valor_num}"
        )
    
    return valor_num


def validarPropension(valor: Union[int, float], nombre: str = "propension") -> float:
    """
    Valida que una propensión marginal esté entre 0 y 1.
    
    Las propensiones marginales (consumir, ahorrar, importar) deben estar
    en el intervalo [0, 1] por definición económica.
    
    Args:
        valor: Propensión a validar
        nombre: Nombre de la propensión
        
    Returns:
        El valor si es válido
        
    Raises:
        ErrorValidacion: Si no está entre 0 y 1
    """
    return validarRango(valor, 0, 1, nombre)


def validarElasticidad(valor: float, nombre: str = "elasticidad", tipo: str = "general") -> float:
    """
    Valida y clasifica una elasticidad económica.

    Args:
        valor: Elasticidad calculada
        nombre: Nombre de la elasticidad
        tipo: Tipo de elasticidad ("demanda", "oferta", "general")

    Returns:
        El valor validado

    Raises:
        ErrorValidacion: Si el valor no es numérico o no es económicamente válido

    Ejemplo:
        >>> elasticidad = validarElasticidad(-1.5, "elasticidad_precio", "demanda")
        >>> # Valida que sea negativa para demanda
    """
    try:
        valor_num = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(nombre, f"{nombre} debe ser un número")

    # Validar infinitos o NaN
    if not (-float('inf') < valor_num < float('inf')):
        raise ErrorValidacion(nombre, f"{nombre} no puede ser infinito o NaN")

    # Validaciones específicas por tipo
    if tipo == "demanda":
        # Para demanda normal, la elasticidad precio debe ser negativa
        if valor_num > 0:
            import warnings
            warnings.warn(
                f"{nombre} es positiva ({valor_num}), lo cual indica un bien Giffen. "
                "Esto es económicamente inusual.",
                UserWarning
            )
    elif tipo == "oferta":
        # Para oferta normal, la elasticidad precio debe ser positiva
        if valor_num < 0:
            import warnings
            warnings.warn(
                f"{nombre} es negativa ({valor_num}), lo cual es económicamente inusual.",
                UserWarning
            )

    return valor_num


def validarEcuacion(ecuacion: str) -> bool:
    """
    Verifica que una ecuación tenga formato válido.
    
    Args:
        ecuacion: String con la ecuación en LaTeX
        
    Returns:
        True si es válida
        
    Raises:
        ErrorValidacion: Si la ecuación no es válida
    """
    if not isinstance(ecuacion, str):
        raise ErrorValidacion("ecuacion", "La ecuación debe ser un string")
    
    if not ecuacion.strip():
        raise ErrorValidacion("ecuacion", "La ecuación no puede estar vacía")
    
    # Validaciones básicas
    if ecuacion.count("=") > 1:
        raise ErrorValidacion("ecuacion", "La ecuación solo puede tener un signo '='")
    
    return True