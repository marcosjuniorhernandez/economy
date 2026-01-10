"""
Excepciones personalizadas para Oikos.

Este módulo define todas las excepciones que pueden ocurrir
al trabajar con modelos económicos en la biblioteca Oikos.
Todas las excepciones heredan de ErrorOikos para facilitar
el manejo de errores específicos de la biblioteca.
"""


class ErrorOikos(Exception):
    """
    Excepción base para todos los errores de Oikos.

    Esta es la clase base de la que heredan todas las excepciones
    personalizadas de la biblioteca. Permite capturar cualquier
    error específico de Oikos con un solo bloque except.
    """
    pass


class ErrorParseador(ErrorOikos):
    """
    Error al parsear una ecuación en LaTeX.

    Se lanza cuando el parseador no puede convertir una expresión
    LaTeX en una expresión simbólica de SymPy. Esto puede ocurrir
    por sintaxis incorrecta o uso de símbolos no soportados.

    Atributos:
        ecuacion: La ecuación LaTeX que causó el error
        mensaje: Descripción detallada del error
    """
    def __init__(self, ecuacion: str, mensaje: str = "") -> None:
        self.ecuacion: str = ecuacion
        self.mensaje: str = mensaje or f"No se pudo parsear la ecuación: {ecuacion}"
        super().__init__(self.mensaje)


class ErrorEquilibrio(ErrorOikos):
    """
    Error al calcular un equilibrio económico.

    Se lanza cuando no existe equilibrio en un modelo económico,
    por ejemplo cuando las curvas de oferta y demanda no se intersectan,
    o cuando el sistema de ecuaciones no tiene solución.

    Atributos:
        mensaje: Descripción del problema con el equilibrio
    """
    def __init__(self, mensaje: str = "No existe equilibrio para este sistema") -> None:
        self.mensaje: str = mensaje
        super().__init__(self.mensaje)


class ErrorValidacion(ErrorOikos):
    """
    Error de validación de parámetros económicos.

    Se lanza cuando un parámetro no cumple con las restricciones
    económicas necesarias, como precios negativos, cantidades
    negativas, o elasticidades fuera de rango válido.

    Atributos:
        parametro: Nombre del parámetro que falló la validación
        mensaje: Descripción del error de validación
    """
    def __init__(self, parametro: str, mensaje: str = "") -> None:
        self.parametro: str = parametro
        self.mensaje: str = mensaje or f"Valor inválido para {parametro}"
        super().__init__(self.mensaje)


class ErrorGrafico(ErrorOikos):
    """
    Error al intentar graficar un modelo.

    Se lanza cuando ocurre un error durante la generación de
    gráficos, como problemas con matplotlib, parámetros
    inconsistentes, o imposibilidad de guardar la figura.

    Atributos:
        mensaje: Descripción del error de graficación
    """
    def __init__(self, mensaje: str = "No se pudo generar el gráfico") -> None:
        self.mensaje: str = mensaje
        super().__init__(self.mensaje)
