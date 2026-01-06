"""
Clases base abstractas para todos los modelos económicos de Oikos.

Estas clases definen la estructura común que deben seguir todos los modelos,
asegurando consistencia en la interfaz y facilitando la extensión.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from sympy import Symbol, Expr


class ModeloEconomico(ABC):
    """
    Clase base abstracta para todos los modelos económicos.
    
    Todos los modelos en Oikos (IS-LM, Demanda, Oferta, etc.) heredan de esta clase.
    Define métodos que todo modelo debe implementar.
    """
    
    def __init__(self):
        self.variables = {}   # Diccionario de símbolos económicos
        self.parametros = {}  # Parámetros del modelo
        self.solucion = None  # Solución del modelo (si aplica)
    
    @abstractmethod
    def resolver(self) -> Dict[str, Any]:
        """
        Resuelve el modelo económico.
        
        Returns:
            Dict con las variables resueltas y sus valores
        """
        pass
    
    @abstractmethod
    def explicar(self) -> str:
        """
        Genera una explicación económica del modelo.
        
        Returns:
            Texto explicativo del significado económico
        """
        pass
    
    def __repr__(self):
        """Representación del modelo."""
        nombre_clase = self.__class__.__name__
        return f"{nombre_clase}(variables={list(self.variables.keys())})"


class FuncionEconomica(ABC):
    """
    Clase base para funciones económicas (Demanda, Oferta, Consumo, etc.).
    
    Representa una relación funcional entre variables económicas.
    Todas las funciones pueden:
    - Evaluarse en puntos específicos
    - Calcular elasticidades
    - Graficarse
    """
    
    def __init__(self, expresion: Expr):
        """
        Inicializa una función económica.
        
        Args:
            expresion: Expresión simbólica de SymPy
        """
        self.expresion = expresion
        self.variables_libres = list(expresion.free_symbols)
    
    @abstractmethod
    def evaluar(self, **valores) -> float:
        """
        Evalúa la función en valores específicos.
        
        Args:
            **valores: Variables y sus valores (ej: P=10, Q=5)
            
        Returns:
            Resultado numérico de la evaluación
        """
        pass
    
    @abstractmethod
    def calcularElasticidad(self, **punto) -> float:
        """
        Calcula la elasticidad en un punto.
        
        Args:
            **punto: Valores de las variables en el punto
            
        Returns:
            Elasticidad calculada
        """
        pass
    
    def __str__(self):
        """Representación en texto de la función."""
        from sympy import latex
        return latex(self.expresion)


class MercadoBase(ABC):
    """
    Clase base para representar mercados económicos.
    
    Un mercado incluye:
    - Agentes (compradores, vendedores)
    - Funciones de comportamiento (demanda, oferta)
    - Mecanismo de equilibrio
    """
    
    def __init__(self):
        self.agentes = {}
        self.funciones = {}
        self.equilibrio = None
    
    @abstractmethod
    def calcularEquilibrio(self) -> Dict[str, float]:
        """
        Calcula el equilibrio del mercado.
        
        Returns:
            Diccionario con variables de equilibrio
        """
        pass
    
    @abstractmethod
    def graficar(self, **opciones):
        """
        Genera un gráfico del mercado.
        
        Args:
            **opciones: Configuración del gráfico
        """
        pass