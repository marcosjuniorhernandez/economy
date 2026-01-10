"""
Validadores para inputs económicos.

Funciones que verifican que los parámetros económicos sean válidos
antes de usarlos en los modelos. Cada validador lanza ErrorValidacion
si los parámetros no cumplen con las restricciones económicas necesarias.
"""

from typing import Optional, Union

from ..nucleo.excepciones import ErrorValidacion


def validarPositivo(valor: Union[int, float], nombre: str = "valor") -> float:
    """
    Valida que un valor sea positivo (> 0).
    
    En economía, muchas variables como precios, cantidades, ingreso,
    consumo, etc. deben ser estrictamente positivos por definición.
    
    Args:
        valor: Número a validar
        nombre: Nombre del parámetro (para el mensaje de error)
        
    Returns:
        El valor convertido a float si es válido
        
    Raises:
        ErrorValidacion: Si el valor no es positivo o no es numérico
        
    Ejemplo:
        >>> precio = validarPositivo(10, "precio")
        >>> # OK, retorna 10.0
        
        >>> precio = validarPositivo(-5, "precio")
        >>> # Lanza ErrorValidacion: precio debe ser positivo
    """
    try:
        valorNum = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(nombre, f"{nombre} debe ser un número")
    
    if valorNum <= 0:
        raise ErrorValidacion(nombre, f"{nombre} debe ser positivo, recibido: {valorNum}")
    
    return valorNum


def validarNoNegativo(valor: Union[int, float], nombre: str = "valor") -> float:
    """
    Valida que un valor sea no negativo (≥ 0).
    
    Algunas variables económicas pueden ser cero pero no negativas,
    como el ahorro, el gasto en ciertos bienes, o la cantidad consumida.
    
    Args:
        valor: Número a validar
        nombre: Nombre del parámetro
        
    Returns:
        El valor convertido a float si es válido
        
    Raises:
        ErrorValidacion: Si el valor es negativo o no es numérico
    """
    try:
        valorNum = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(nombre, f"{nombre} debe ser un número")
    
    if valorNum < 0:
        raise ErrorValidacion(nombre, f"{nombre} no puede ser negativo, recibido: {valorNum}")
    
    return valorNum


def validarRango(valor: Union[int, float], 
                 minimo: Optional[float] = None,
                 maximo: Optional[float] = None,
                 nombre: str = "valor") -> float:
    """
    Valida que un valor esté dentro de un rango especificado.
    
    Útil para validar parámetros que deben estar acotados,
    como probabilidades, propensiones marginales, o porcentajes.
    
    Args:
        valor: Número a validar
        minimo: Valor mínimo permitido (inclusive), None si no hay límite inferior
        maximo: Valor máximo permitido (inclusive), None si no hay límite superior
        nombre: Nombre del parámetro
        
    Returns:
        El valor convertido a float si está en el rango
        
    Raises:
        ErrorValidacion: Si está fuera del rango o no es numérico
        
    Ejemplo:
        >>> # Validar que la propensión marginal esté entre 0 y 1
        >>> pmc = validarRango(0.8, 0, 1, "propensionMarginalConsumir")
        >>> # OK, retorna 0.8
    """
    try:
        valorNum = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(nombre, f"{nombre} debe ser un número")
    
    if minimo is not None and valorNum < minimo:
        raise ErrorValidacion(
            nombre, 
            f"{nombre} debe ser ≥ {minimo}, recibido: {valorNum}"
        )
    
    if maximo is not None and valorNum > maximo:
        raise ErrorValidacion(
            nombre,
            f"{nombre} debe ser ≤ {maximo}, recibido: {valorNum}"
        )
    
    return valorNum


def validarPropension(valor: Union[int, float], nombre: str = "propension") -> float:
    """
    Valida que una propensión marginal esté entre 0 y 1.
    
    Las propensiones marginales (a consumir, a ahorrar, a importar) deben estar
    en el intervalo [0, 1] por definición económica, ya que representan la
    fracción de ingreso adicional destinada a un uso específico.
    
    Args:
        valor: Propensión a validar
        nombre: Nombre de la propensión
        
    Returns:
        El valor si es válido (entre 0 y 1)
        
    Raises:
        ErrorValidacion: Si no está entre 0 y 1
        
    Ejemplo:
        >>> pmc = validarPropension(0.75, "propensionMarginalConsumir")
        >>> # OK, retorna 0.75
    """
    return validarRango(valor, 0, 1, nombre)


def validarElasticidad(valor: float, nombre: str = "elasticidad", tipo: str = "general") -> float:
    """
    Valida y clasifica una elasticidad económica.
    
    Las elasticidades miden la sensibilidad porcentual de una variable
    ante cambios en otra. Este validador verifica que sean numéricas
    y proporciona advertencias para casos económicamente inusuales.

    Args:
        valor: Elasticidad calculada
        nombre: Nombre de la elasticidad
        tipo: Tipo de elasticidad ("demanda", "oferta", "general")

    Returns:
        El valor validado

    Raises:
        ErrorValidacion: Si el valor no es numérico o es infinito/NaN

    Ejemplo:
        >>> elasticidad = validarElasticidad(-1.5, "elasticidadPrecio", "demanda")
        >>> # OK, elasticidad negativa es normal para demanda
        
        >>> elasticidad = validarElasticidad(2.0, "elasticidadPrecio", "demanda")
        >>> # Advertencia: elasticidad positiva indica bien Giffen
    """
    try:
        valorNum = float(valor)
    except (TypeError, ValueError):
        raise ErrorValidacion(nombre, f"{nombre} debe ser un número")

    # Validar infinitos o NaN
    if not (-float('inf') < valorNum < float('inf')):
        raise ErrorValidacion(nombre, f"{nombre} no puede ser infinito o NaN")

    # Validaciones específicas por tipo
    if tipo == "demanda":
        # Para demanda normal, la elasticidad precio debe ser negativa
        if valorNum > 0:
            import warnings
            warnings.warn(
                f"{nombre} es positiva ({valorNum}), lo cual indica un bien Giffen. "
                "Esto es económicamente inusual.",
                UserWarning
            )
    elif tipo == "oferta":
        # Para oferta normal, la elasticidad precio debe ser positiva
        if valorNum < 0:
            import warnings
            warnings.warn(
                f"{nombre} es negativa ({valorNum}), lo cual es económicamente inusual.",
                UserWarning
            )

    return valorNum


def validarEcuacion(ecuacion: str) -> bool:
    """
    Verifica que una ecuación tenga formato válido.
    
    Realiza validaciones básicas de formato para ecuaciones en LaTeX,
    asegurando que sean strings no vacíos y con estructura correcta.
    
    Args:
        ecuacion: String con la ecuación en LaTeX
        
    Returns:
        True si es válida
        
    Raises:
        ErrorValidacion: Si la ecuación no es válida
        
    Ejemplo:
        >>> validarEcuacion("Q = 100 - 2P")
        >>> # True
        
        >>> validarEcuacion("")
        >>> # Lanza ErrorValidacion: ecuación vacía
    """
    if not isinstance(ecuacion, str):
        raise ErrorValidacion("ecuacion", "La ecuación debe ser un string")
    
    if not ecuacion.strip():
        raise ErrorValidacion("ecuacion", "La ecuación no puede estar vacía")
    
    # Validaciones básicas
    if ecuacion.count("=") > 1:
        raise ErrorValidacion("ecuacion", "La ecuación solo puede tener un signo '='")
    
    return True
