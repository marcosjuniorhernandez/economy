"""
Decoradores para Oikos.

Este módulo contiene decoradores que mejoran las clases y funciones
de Oikos con funcionalidades adicionales como ayuda contextual.
"""

from functools import wraps
from typing import Callable, Optional
import inspect


def ayuda(descripcion_economica: str, 
          supuestos: Optional[list] = None,
          cursos: Optional[list] = None,
          ejemplos: Optional[str] = None):
    """
    Decorador que añade ayuda económica contextual a clases y funciones.
    
    Este decorador permite que los estudiantes obtengan explicaciones
    económicas directamente desde el código usando help().
    
    Args:
        descripcion_economica: Explicación del concepto económico
        supuestos: Lista de supuestos del modelo
        cursos: Lista de cursos donde se usa este concepto
        ejemplos: Código de ejemplo de uso
        
    Ejemplo de uso:
        >>> @ayuda(
        ...     descripcion_economica="Modelo de equilibrio de mercado competitivo",
        ...     supuestos=["Competencia perfecta", "Precio flexible"],
        ...     cursos=["Microeconomía I", "Introducción a la Economía"]
        ... )
        ... class Mercado:
        ...     pass
        
        >>> help(Mercado)
        # Mostrará toda la información económica
    """
    def decorador(obj):
        # Construir documentación económica
        doc_economica = f"""

╔══════════════════════════════════════════════════════════════════╗
║                    OIKOS - AYUDA ECONÓMICA                       ║
╚══════════════════════════════════════════════════════════════════╝

{descripcion_economica}
"""
        
        if supuestos:
            doc_economica += "\n🔍 SUPUESTOS DEL MODELO:\n"
            for i, supuesto in enumerate(supuestos, 1):
                doc_economica += f"   {i}. {supuesto}\n"
        
        if cursos:
            doc_economica += "\n🎓 USADO EN:\n"
            for curso in cursos:
                doc_economica += f"   • {curso}\n"
        
        if ejemplos:
            doc_economica += f"\n💡 EJEMPLO DE USO:\n{ejemplos}\n"
        
        doc_economica += "\n" + "─" * 66 + "\n"
        
        # Añadir la documentación económica al objeto
        if hasattr(obj, '__doc__'):
            doc_original = obj.__doc__ or ""
            obj.__doc__ = doc_economica + doc_original
        else:
            obj.__doc__ = doc_economica
        
        # Guardar metadata para acceso programático
        obj._oikos_ayuda = {
            'descripcion': descripcion_economica,
            'supuestos': supuestos or [],
            'cursos': cursos or [],
            'ejemplos': ejemplos
        }
        
        return obj
    
    return decorador


def explicacion(texto_explicativo: str):
    """
    Decorador que añade explicación económica a métodos.
    
    Útil para explicar qué hace un método desde la perspectiva económica.
    
    Args:
        texto_explicativo: Explicación de lo que hace el método económicamente
        
    Ejemplo:
        >>> class Demanda:
        ...     @explicacion("Calcula la elasticidad precio de la demanda")
        ...     def elasticidadPrecio(self, P, Q):
        ...         pass
    """
    
    def decorador(func):
        @wraps(func)
        def envoltura(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Añadir explicación al docstring
        explicacion_doc = f"\n{'─'*50}\n📖 EXPLICACIÓN ECONÓMICA:\n{texto_explicativo}\n{'─'*50}\n"
        
        if func.__doc__:
            envoltura.__doc__ = explicacion_doc + func.__doc__
        else:
            envoltura.__doc__ = explicacion_doc
        
        return envoltura
    
    return decorador


def validarEconomico(**validaciones):
    """
    Decorador que valida parámetros económicos antes de ejecutar.
    
    Args:
        **validaciones: Diccionario de validaciones a aplicar
                       Ejemplo: precio='positivo', cantidad='no_negativo'
        
    Ejemplo:
        >>> @validar_economico(precio='positivo', cantidad='no_negativo')
        ... def calcular_ingreso(precio, cantidad):
        ...     return precio * cantidad
    """
    def decorador(func):
        @wraps(func)
        def envoltura(*args, **kwargs):
            # Obtener nombres de parámetros
            sig = inspect.signature(func)
            parametros = sig.parameters
            
            # Crear diccionario de argumentos
            args_dict = {}
            param_names = list(parametros.keys())
            
            for i, valor in enumerate(args):
                if i < len(param_names):
                    args_dict[param_names[i]] = valor
            
            args_dict.update(kwargs)
            
            # Validar cada parámetro
            from ..utilidades.validadores import (
                validarPositivo,
                validarNoNegativo,
                validarRango,
                validarPropension
            )
            
            for nombre_param, tipo_validacion in validaciones.items():
                if nombre_param in args_dict:
                    valor = args_dict[nombre_param]
                    
                    if tipo_validacion == 'positivo':
                        validarPositivo(valor, nombre_param)
                    elif tipo_validacion == 'no_negativo':
                        validarNoNegativo(valor, nombre_param)
                    elif tipo_validacion == 'propension':
                        validarPropension(valor, nombre_param)
                    elif isinstance(tipo_validacion, tuple):
                        # Rango: (min, max)
                        validarRango(valor, tipo_validacion[0], tipo_validacion[1], nombre_param)
            
            return func(*args, **kwargs)
        
        return envoltura
    
    return decorador


def memoizarResultado(func):
    """
    Decorador que cachea el resultado de funciones económicas costosas.
    
    Útil para equilibrios que se calculan múltiples veces.
    
    Ejemplo:
        >>> @memoizar_resultado
        ... def calcular_equilibrio(a, b, c):
        ...     # Cálculo costoso...
        ...     return resultado
    """
    cache = {}
    
    @wraps(func)
    def envoltura(*args, **kwargs):
        # Crear clave de cache
        clave = str(args) + str(sorted(kwargs.items()))
        
        if clave not in cache:
            cache[clave] = func(*args, **kwargs)
        
        return cache[clave]
    
    return envoltura


def deprecado(mensaje: str = "Esta función está deprecada"):
    """
    Marca una función como deprecada y muestra advertencia.
    
    Args:
        mensaje: Mensaje de advertencia personalizado
        
    Ejemplo:
        >>> @deprecated("Usa calcular_equilibrio_v2() en su lugar")
        ... def calcular_equilibrio_v1():
        ...     pass
    """
    def decorador(func):
        @wraps(func)
        def envoltura(*args, **kwargs):
            import warnings
            warnings.warn(
                f"{func.__name__} está deprecada. {mensaje}",
                category=DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        
        return envoltura
    
    return decorador