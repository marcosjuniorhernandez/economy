"""
Excepciones personalizadas para Oikos.

Este módulo define todas las excepciones que pueden ocurrir
al trabajar con modelos económicos.
"""


class ErrorOikos(Exception):
    """Excepción base para todos los errores de Oikos."""
    pass


class ErrorParseador(ErrorOikos):
    """Error al parsear una ecuación en LaTeX."""
    def __init__(self, ecuacion: str, mensaje: str = ""):
        self.ecuacion = ecuacion
        self.mensaje = mensaje or f"No se pudo parsear la ecuación: {ecuacion}"
        super().__init__(self.mensaje)


class ErrorEquilibrio(ErrorOikos):
    """Error al calcular un equilibrio económico."""
    def __init__(self, mensaje: str = "No existe equilibrio para este sistema"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ErrorValidacion(ErrorOikos):
    """Error de validación de parámetros económicos."""
    def __init__(self, parametro: str, mensaje: str = ""):
        self.parametro = parametro
        self.mensaje = mensaje or f"Valor inválido para {parametro}"
        super().__init__(self.mensaje)


class ErrorGrafico(ErrorOikos):
    """Error al intentar graficar un modelo."""
    def __init__(self, mensaje: str = "No se pudo generar el gráfico"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
