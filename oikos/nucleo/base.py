"""
Clases base abstractas para todos los modelos económicos de Oikos.

Estas clases definen la estructura común que deben seguir todos los modelos,
asegurando consistencia en la interfaz y facilitando la extensión del sistema.
Cada clase base proporciona métodos abstractos que las implementaciones
concretas deben definir.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from sympy import Expr, Symbol


class ModeloEconomico(ABC):
    """
    Clase base abstracta para todos los modelos económicos.
    
    Todos los modelos en Oikos (IS-LM, Demanda, Oferta, Mercado, etc.) 
    heredan de esta clase. Define la interfaz común que permite resolver,
    explicar y representar modelos económicos de manera consistente.
    
    Atributos:
        variables: Diccionario de símbolos económicos del modelo
        parametros: Parámetros numéricos del modelo
        solucion: Solución calculada del modelo (si aplica)
    """
    
    def __init__(self) -> None:
        self.variables: Dict[str, Symbol] = {}
        self.parametros: Dict[str, float] = {}
        self.solucion: Optional[Dict[str, Any]] = None
    
    @abstractmethod
    def resolver(self) -> Dict[str, Any]:
        """
        Resuelve el modelo económico.
        
        Cada tipo de modelo implementa su propia lógica de solución.
        Por ejemplo, un mercado resuelve para precio y cantidad de equilibrio,
        mientras que un modelo IS-LM resuelve para ingreso y tasa de interés.
        
        Returns:
            Dict con las variables resueltas y sus valores
        """
        pass
    
    @abstractmethod
    def explicar(self) -> str:
        """
        Genera una explicación económica del modelo.
        
        Proporciona una interpretación teórica del modelo y sus resultados,
        explicando el significado económico de las variables y relaciones.
        
        Returns:
            Texto explicativo del significado económico del modelo
        """
        pass
    
    def __repr__(self) -> str:
        """Representación del modelo."""
        nombreClase: str = self.__class__.__name__
        return f"{nombreClase}(variables={list(self.variables.keys())})"


class FuncionEconomica(ABC):
    """
    Clase base para funciones económicas (Demanda, Oferta, Consumo, etc.).
    
    Representa una relación funcional entre variables económicas.
    Por ejemplo, una función de demanda relaciona precio con cantidad
    demandada, mientras que una función de producción relaciona
    factores de producción con nivel de producto.
    
    Todas las funciones económicas pueden:
    - Evaluarse en puntos específicos
    - Calcular elasticidades
    - Graficarse
    - Representarse en LaTeX
    
    Atributos:
        expresion: Expresión simbólica de SymPy que define la función
        variablesLibres: Lista de símbolos que aparecen en la expresión
    """
    
    def __init__(self, expresion: Expr) -> None:
        """
        Inicializa una función económica.
        
        Args:
            expresion: Expresión simbólica de SymPy que define la relación
        """
        self.expresion: Expr = expresion
        self.variablesLibres: list = list(expresion.free_symbols)
    
    @abstractmethod
    def evaluar(self, **valores: float) -> float:
        """
        Evalúa la función en valores específicos.
        
        Sustituye las variables por valores numéricos y calcula
        el resultado. Por ejemplo, evaluar una demanda Q = 100 - 2P
        en P=10 devuelve Q=80.
        
        Args:
            **valores: Variables y sus valores (ej: P=10, Q=5)
            
        Returns:
            Resultado numérico de la evaluación
        """
        pass
    
    @abstractmethod
    def calcularElasticidad(self, **punto: float) -> float:
        """
        Calcula la elasticidad en un punto.
        
        La elasticidad mide la sensibilidad porcentual de una variable
        ante cambios porcentuales en otra. Es fundamental para análisis
        de sensibilidad y políticas económicas.
        
        Args:
            **punto: Valores de las variables en el punto de evaluación
            
        Returns:
            Elasticidad calculada en el punto especificado
        """
        pass
    
    def __str__(self) -> str:
        """Representación en texto de la función."""
        from sympy import latex
        return latex(self.expresion)


class MercadoBase(ABC):
    """
    Clase base para representar mercados económicos.
    
    Un mercado es el espacio donde se coordinan las decisiones
    de compradores y vendedores. Esta clase proporciona la estructura
    para modelar mercados de diferentes estructuras (competencia perfecta,
    monopolio, oligopolio, etc.).
    
    Un mercado incluye:
    - Agentes (compradores, vendedores, gobierno)
    - Funciones de comportamiento (demanda, oferta, costos)
    - Mecanismo de equilibrio (precio que iguala oferta y demanda)
    
    Atributos:
        agentes: Diccionario de agentes económicos en el mercado
        funciones: Diccionario de funciones de comportamiento
        equilibrio: Solución de equilibrio calculada
    """
    
    def __init__(self) -> None:
        self.agentes: Dict[str, Any] = {}
        self.funciones: Dict[str, FuncionEconomica] = {}
        self.equilibrio: Optional[Dict[str, float]] = None
    
    @abstractmethod
    def calcularEquilibrio(self) -> Dict[str, float]:
        """
        Calcula el equilibrio del mercado.
        
        Encuentra el punto donde se igualan oferta y demanda,
        determinando precio y cantidad de equilibrio. En modelos
        más complejos puede incluir múltiples variables de equilibrio.
        
        Returns:
            Diccionario con variables de equilibrio (precio, cantidad, etc.)
        """
        pass
    
    @abstractmethod
    def graficar(self, **opciones: Any) -> None:
        """
        Genera un gráfico del mercado.
        
        Visualiza las curvas de oferta y demanda, puntos de equilibrio,
        áreas de excedente del consumidor y productor, y otros elementos
        relevantes del análisis de mercado.
        
        Args:
            **opciones: Configuración del gráfico (título, colores, etc.)
        """
        pass
