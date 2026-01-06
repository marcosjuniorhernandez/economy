"""
Herramientas de visualización para Oikos.

Este módulo contiene:
- escribir(): Muestra resultados económicos de forma elegante
- Lienzo: Lienzo para gráficos económicos
- EstiloGrafico: Configuración de estilos visuales
"""

from IPython.display import display, Math
from sympy import latex
import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, Tuple, List, Union, Callable
from dataclasses import dataclass, field


# ============= COLORES PREDEFINIDOS =============
# Puedes usar estos colores directamente: escribir(..., color=ROJO)

ROJO = '#E63946'
AZUL = '#1D3557'
VERDE = '#2A9D8F'
AMARILLO = '#F4A261'
NARANJA = '#E76F51'
MORADO = '#6A4C93'
TURQUESA = '#06AED5'
ROSA = '#FF006E'


def escribir(diccionarioResultados: dict, titulo: Optional[str] = None):
    """
    Muestra resultados económicos de forma clara y centrada.

    Mejoras v0.3.0:
    - Formato en lista con saltos de línea
    - Alineación a la izquierda
    - Mejor legibilidad en terminal y Jupyter

    Args:
        diccionarioResultados: Diccionario con variables y valores
                              Ejemplo: {'P^*': 25, 'Q^*': 50}
        titulo: (Opcional) Título del análisis

    Ejemplo:
        >>> resultados = {'Q^*': 50, 'P^*': 10, 'E_p': -1.5}
        >>> escribir(resultados, "Equilibrio de Mercado")

        # Salida en Jupyter:
        Equilibrio de Mercado
        Q* = 50
        P* = 10
        Ep = -1.5
    """
    # Validar entrada
    if not isinstance(diccionarioResultados, dict):
        raise TypeError(f"Se esperaba un diccionario, se recibió {type(diccionarioResultados).__name__}")

    # Verificamos si estamos en Jupyter/Colab o terminal
    try:
        from IPython import get_ipython
        enJupyter = get_ipython() is not None
    except ImportError:
        enJupyter = False
    
    if enJupyter:
        # ====== JUPYTER/COLAB ======
        # Mostramos el título si existe
        if titulo:
            display(Math(rf"\textbf{{{titulo}}}"))
            display(Math(r"\text{ }"))  # Espacio
        
        # Mostramos cada variable en su propia línea, alineada a la izquierda
        for variable, valor in diccionarioResultados.items():
            # Convertimos el valor a LaTeX si es necesario
            valor_latex = latex(valor) if hasattr(valor, '__class__') else str(valor)
            
            # Mostramos cada resultado en su propia línea
            ecuacion = rf"{variable} = {valor_latex}"
            display(Math(ecuacion))
    
    else:
        # ====== TERMINAL ======
        if titulo:
            print(f"\n{'='*50}")
            print(f"  {titulo}")
            print(f"{'='*50}")
        
        # Mostramos cada resultado en su propia línea
        for variable, valor in diccionarioResultados.items():
            print(f"  {variable} = {valor}")
        
        if titulo:
            print(f"{'='*50}\n")


@dataclass
class EstiloGrafico:
    """
    Configuración de estilo para gráficos económicos.
    
    Esta clase define todos los aspectos visuales de los gráficos:
    colores, fuentes, dimensiones, etc.
    
    Atributos:
        paletaColores: Lista de colores para usar en las curvas
        anchoLinea: Grosor de las curvas económicas
        anchoEje: Grosor de los ejes
        dimensionFigura: (ancho, alto) de la figura en pulgadas
        familiaFuente: Familia de fuente ('serif', 'sans-serif', 'monospace')
        
    Ejemplo:
        >>> # Usar estilo personalizado
        >>> mi_estilo = EstiloGrafico(
        ...     paletaColores=[ROJO, AZUL, VERDE],
        ...     anchoLinea=3.0
        ... )
        >>> lienzo = Lienzo(estilo=mi_estilo)
    """
    
    # Paleta de colores VIVOS (nueva para v0.3.0)
    paletaColores: List[str] = field(default_factory=lambda: [
        '#E63946',  # Rojo vibrante
        '#1D3557',  # Azul marino profundo
        '#2A9D8F',  # Verde turquesa
        '#F4A261',  # Naranja cálido
        '#E76F51',  # Coral
        '#6A4C93',  # Púrpura
        '#06AED5',  # Cyan brillante
        '#FF006E',  # Rosa magenta
    ])
    
    # Estilo de líneas
    anchoLinea: float = 2.8
    anchoEje: float = 1.8
    anchoGrid: float = 0.6
    
    # Estilo de grid
    alphaGrid: float = 0.25
    estiloLineaGrid: str = '--'
    
    # Fondo y ejes
    colorFondo: str = 'white'
    colorEje: str = '#2C3E50'
    
    # Texto y labels
    familiaFuente: str = 'serif'
    dimensionTitulo: int = 15
    dimensionLabel: int = 13
    dimensionTick: int = 11
    dimensionLeyenda: int = 11
    
    # Figura
    dimensionFigura: Tuple[int, int] = (10, 7)
    dpi: int = 110
    
    # Áreas de relleno
    alphaRelleno: float = 0.3


class Lienzo:
    """
    Lienzo flexible para gráficos económicos.
    
    El Lienzo permite crear gráficos profesionales de modelos económicos
    con control total sobre la apariencia y el contenido.
    
    Características:
    - Agregar múltiples curvas económicas
    - Puntos de equilibrio
    - Áreas de excedente
    - Líneas de referencia
    - Leyendas automáticas
    - Exportar a imagen
    
    Args:
        estilo: Configuración visual personalizada
        cuadrantes: "I" (solo primer cuadrante), "I-IV" (todos), "auto"
        relacionAspecto: "equal" (1:1) o "auto" (automático)
        
    Ejemplo:
        >>> # Crear un gráfico simple
        >>> lienzo = Lienzo()
        >>> lienzo.configurarEtiquetas(
        ...     etiquetaX="Cantidad (Q)",
        ...     etiquetaY="Precio (P)",
        ...     titulo="Mercado Competitivo"
        ... )
        >>> lienzo.agregar(demanda, etiqueta="Demanda", color=ROJO)
        >>> lienzo.agregar(oferta, etiqueta="Oferta", color=AZUL)
        >>> lienzo.graficar()
    """
    
    def __init__(self, 
                 estilo: Optional[EstiloGrafico] = None,
                 cuadrantes: str = "I",
                 relacionAspecto: str = "auto"):
        """
        Inicializa un lienzo para gráficos económicos.
        """
        self.estilo = estilo or EstiloGrafico()
        self.cuadrantes = cuadrantes
        self.relacionAspecto = relacionAspecto
        
        self.fig = None
        self.ax = None
        self._funciones = []  # Lista de funciones a graficar
        self._indiceColor = 0
        
        # Configuración de ejes
        self.etiquetaX = "x"
        self.etiquetaY = "y"
        self.titulo = ""
        
        # Rangos de ejes (None = automático)
        self.rangoX = None
        self.rangoY = None
        
        # Configuración de saltos (ticks)
        self.pasoX = None
        self.pasoY = None
    
    def configurarEtiquetas(self, 
                           etiquetaX: str = None, 
                           etiquetaY: str = None, 
                           titulo: str = None):
        """
        Configura las etiquetas de los ejes y título.
        
        Args:
            etiquetaX: Etiqueta del eje X (ej: "Cantidad")
            etiquetaY: Etiqueta del eje Y (ej: "Precio")
            titulo: Título del gráfico
            
        Returns:
            self (para encadenar métodos)
        """
        if etiquetaX:
            self.etiquetaX = etiquetaX
        if etiquetaY:
            self.etiquetaY = etiquetaY
        if titulo:
            self.titulo = titulo
        return self
    
    def configurarRango(self, 
                       rangoX: Tuple[float, float] = None,
                       rangoY: Tuple[float, float] = None):
        """
        Configura el rango de los ejes.
        
        Args:
            rangoX: (minimo, maximo) para eje X
            rangoY: (minimo, maximo) para eje Y
            
        Returns:
            self (para encadenar métodos)
        """
        self.rangoX = rangoX
        self.rangoY = rangoY
        return self
    
    def configurarPasos(self, pasoX: float = None, pasoY: float = None):
        """
        Configura el salto entre marcas de los ejes.
        
        Args:
            pasoX: Salto para el eje X
            pasoY: Salto para el eje Y
            
        Returns:
            self (para encadenar métodos)
        """
        self.pasoX = pasoX
        self.pasoY = pasoY
        return self
    
    def agregar(self, 
               funcion,
               etiqueta: str = None,
               color: str = None,
               anchoLinea: float = None,
               estiloLinea: str = '-',
               rangoPersonalizado: Tuple[float, float] = None):
        """
        Añade una función para graficar.
        
        Args:
            funcion: Puede ser:
                    - Objeto de oikos (Demanda, Oferta, etc.)
                    - Función callable: lambda x: x**2
                    - Tupla de arrays: (valores_x, valores_y)
            etiqueta: Texto para la leyenda
            color: Color de la curva (hex o nombre)
            anchoLinea: Grosor de la línea
            estiloLinea: '-' (sólida), '--' (guiones), ':' (puntos)
            rangoPersonalizado: Rango específico para esta función
            
        Returns:
            self (para encadenar métodos)
            
        Ejemplo:
            >>> lienzo.agregar(demanda, etiqueta="Demanda", color=ROJO)
            >>> lienzo.agregar(lambda q: 20 + 0.5*q, etiqueta="Oferta", color=AZUL)
        """
        # Auto-detectar si es un objeto de oikos
        es_objeto_oikos = hasattr(funcion, '__module__') and 'oikos' in str(funcion.__module__)
        
        datos_funcion = {
            'funcion': funcion,
            'etiqueta': etiqueta or self._generarEtiqueta(funcion),
            'color': color or self._obtenerSiguienteColor(),
            'anchoLinea': anchoLinea or self.estilo.anchoLinea,
            'estiloLinea': estiloLinea,
            'rango': rangoPersonalizado,
            'es_oikos': es_objeto_oikos,
            'tipo': 'curva'
        }
        
        self._funciones.append(datos_funcion)
        return self
    
    def agregarPunto(self,
                    x: float,
                    y: float,
                    etiqueta: str = None,
                    color: str = None,
                    dimension: int = 8,
                    marcador: str = 'o'):
        """
        Añade un punto específico (útil para equilibrios).
        
        Args:
            x: Coordenada x
            y: Coordenada y
            etiqueta: Texto para la leyenda
            color: Color del punto
            dimension: Dimensión del marcador
            marcador: Tipo de marcador ('o', 's', '^', etc.)
            
        Returns:
            self (para encadenar métodos)
            
        Ejemplo:
            >>> # Marcar el equilibrio
            >>> lienzo.agregarPunto(50, 25, etiqueta="Equilibrio", color=VERDE)
        """
        datos_punto = {
            'x': x,
            'y': y,
            'etiqueta': etiqueta,
            'color': color or self._obtenerSiguienteColor(),
            'dimension': dimension,
            'marcador': marcador,
            'tipo': 'punto'
        }
        
        self._funciones.append(datos_punto)
        return self
    
    def agregarLineaVertical(self,
                            x: float,
                            etiqueta: str = None,
                            color: str = 'gray',
                            estiloLinea: str = '--'):
        """
        Añade una línea vertical de referencia.
        
        Args:
            x: Posición x de la línea
            etiqueta: Texto para la leyenda
            color: Color de la línea
            estiloLinea: Estilo de la línea
            
        Returns:
            self (para encadenar métodos)
        """
        datos_linea = {
            'x': x,
            'etiqueta': etiqueta,
            'color': color,
            'estiloLinea': estiloLinea,
            'tipo': 'linea_vertical'
        }
        
        self._funciones.append(datos_linea)
        return self
    
    def agregarLineaHorizontal(self,
                              y: float,
                              etiqueta: str = None,
                              color: str = 'gray',
                              estiloLinea: str = '--'):
        """
        Añade una línea horizontal de referencia.
        
        Args:
            y: Posición y de la línea
            etiqueta: Texto para la leyenda
            color: Color de la línea
            estiloLinea: Estilo de la línea
            
        Returns:
            self (para encadenar métodos)
        """
        datos_linea = {
            'y': y,
            'etiqueta': etiqueta,
            'color': color,
            'estiloLinea': estiloLinea,
            'tipo': 'linea_horizontal'
        }
        
        self._funciones.append(datos_linea)
        return self
    
    def agregarRelleno(self,
                      funcion1,
                      funcion2=None,
                      rangoX: Tuple[float, float] = None,
                      color: str = None,
                      alpha: float = None,
                      etiqueta: str = None):
        """
        Añade un área de relleno entre dos funciones.
        
        Útil para mostrar excedentes del consumidor/productor.
        
        Args:
            funcion1: Primera función
            funcion2: Segunda función (None = rellenar hasta el eje x)
            rangoX: Rango horizontal del relleno
            color: Color del relleno
            alpha: Transparencia (0-1)
            etiqueta: Texto para la leyenda
            
        Returns:
            self (para encadenar métodos)
            
        Ejemplo:
            >>> # Excedente del consumidor
            >>> lienzo.agregarRelleno(
            ...     demanda, 
            ...     lambda q: precio_equilibrio,
            ...     rangoX=(0, cantidad_equilibrio),
            ...     color=AZUL,
            ...     etiqueta="Excedente Consumidor"
            ... )
        """
        datos_relleno = {
            'funcion1': funcion1,
            'funcion2': funcion2,
            'rangoX': rangoX,
            'color': color or self._obtenerSiguienteColor(),
            'alpha': alpha or self.estilo.alphaRelleno,
            'etiqueta': etiqueta,
            'tipo': 'relleno'
        }
        
        self._funciones.append(datos_relleno)
        return self
    
    def graficar(self, mostrar: bool = True):
        """
        Genera y muestra el gráfico con todos los elementos añadidos.
        
        Args:
            mostrar: Si True, muestra el gráfico inmediatamente
            
        Returns:
            (fig, ax) - La figura y ejes de matplotlib
        """
        # Crear figura
        self.fig, self.ax = plt.subplots(
            figsize=self.estilo.dimensionFigura,
            dpi=self.estilo.dpi
        )
        
        # Configurar estilo general
        self._configurarEstiloGeneral()
        
        # Configurar cuadrantes
        self._configurarCuadrantes()
        
        # Graficar todas las funciones
        self._graficarFunciones()
        
        # Configurar ejes y etiquetas
        self._configurarEjes()
        
        # Añadir leyenda si hay etiquetas
        etiquetas_existentes = [f['etiqueta'] for f in self._funciones if f.get('etiqueta')]
        if etiquetas_existentes:
            self.ax.legend(
                fontsize=self.estilo.dimensionLeyenda,
                framealpha=0.9,
                loc='best'
            )
        
        # Ajustar diseño
        plt.tight_layout()
        
        if mostrar:
            plt.show()
        
        return self.fig, self.ax
    
    # ========== MÉTODOS PRIVADOS ==========
    
    def _configurarEstiloGeneral(self):
        """Configura el estilo general del gráfico."""
        self.ax.set_facecolor(self.estilo.colorFondo)
        self.ax.grid(
            True,
            alpha=self.estilo.alphaGrid,
            linestyle=self.estilo.estiloLineaGrid,
            linewidth=self.estilo.anchoGrid
        )
        
        # Configurar fuentes
        plt.rcParams['font.family'] = self.estilo.familiaFuente
    
    def _configurarCuadrantes(self):
        """Configura los cuadrantes visibles."""
        if self.cuadrantes == "I":
            # Solo primer cuadrante (x≥0, y≥0)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['bottom'].set_position('zero')
            self.ax.spines['left'].set_position('zero')
            
        elif self.cuadrantes in ["all", "I-IV"]:
            # Todos los cuadrantes (cruz en el origen)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['bottom'].set_position('zero')
            self.ax.spines['left'].set_position('zero')
            
        else:
            # Estilo tradicional (bordes)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
        
        # Aplicar estilos a spines visibles
        for spine in ['bottom', 'left']:
            if self.ax.spines[spine].get_visible():
                self.ax.spines[spine].set_linewidth(self.estilo.anchoEje)
                self.ax.spines[spine].set_color(self.estilo.colorEje)
    
    def _configurarEjes(self):
        """Configura las etiquetas y rangos de los ejes."""
        # Etiquetas
        self.ax.set_xlabel(
            self.etiquetaX,
            fontsize=self.estilo.dimensionLabel,
            fontweight='bold'
        )
        self.ax.set_ylabel(
            self.etiquetaY,
            fontsize=self.estilo.dimensionLabel,
            fontweight='bold'
        )
        
        # Título
        if self.titulo:
            self.ax.set_title(
                self.titulo,
                fontsize=self.estilo.dimensionTitulo,
                fontweight='bold',
                pad=20
            )
        
        # Rangos
        if self.rangoX:
            self.ax.set_xlim(self.rangoX)
        if self.rangoY:
            self.ax.set_ylim(self.rangoY)
        
        # Dimensión de ticks
        self.ax.tick_params(labelsize=self.estilo.dimensionTick)
    
    def _graficarFunciones(self):
        """Grafica todas las funciones añadidas."""
        for datos_funcion in self._funciones:
            tipo_func = datos_funcion.get('tipo')
            
            if tipo_func == 'punto':
                self._graficarPunto(datos_funcion)
            elif tipo_func == 'linea_vertical':
                self._graficarLineaVertical(datos_funcion)
            elif tipo_func == 'linea_horizontal':
                self._graficarLineaHorizontal(datos_funcion)
            elif tipo_func == 'relleno':
                self._graficarRelleno(datos_funcion)
            else:
                self._graficarCurva(datos_funcion)
    
    def _graficarCurva(self, datos_funcion):
        """Grafica una curva."""
        funcion = datos_funcion['funcion']
        
        # Determinar rango de x
        if datos_funcion['rango']:
            x_min, x_max = datos_funcion['rango']
        elif self.rangoX:
            x_min, x_max = self.rangoX
        else:
            x_min, x_max = 0, 100  # Valor por defecto
        
        valores_x = np.linspace(x_min, x_max, 500)
        
        # Calcular valores_y según el tipo de función
        if datos_funcion['es_oikos']:
            # Objeto de oikos
            valores_y = self._evaluarObjetoOikos(funcion, valores_x)
        elif callable(funcion):
            # Función Python normal
            valores_y = [funcion(x) for x in valores_x]
        elif isinstance(funcion, tuple) and len(funcion) == 2:
            # Datos pre-calculados
            valores_x, valores_y = funcion
        else:
            raise TypeError(
                f"Tipo de función no soportado: {type(funcion).__name__}. "
                f"Se esperaba un objeto de oikos, función callable o tupla (x, y)."
            )
        
        # Graficar
        self.ax.plot(
            valores_x, valores_y,
            color=datos_funcion['color'],
            linewidth=datos_funcion['anchoLinea'],
            linestyle=datos_funcion['estiloLinea'],
            label=datos_funcion['etiqueta'],
            zorder=3
        )
    
    def _graficarRelleno(self, datos_relleno):
        """Grafica un área de relleno."""
        rangoX = datos_relleno['rangoX'] or self.rangoX or (0, 100)
        valores_x = np.linspace(rangoX[0], rangoX[1], 500)
        
        # Evaluar funciones
        y1 = self._evaluarFuncion(datos_relleno['funcion1'], valores_x)
        y2 = self._evaluarFuncion(datos_relleno['funcion2'], valores_x) if datos_relleno['funcion2'] else 0
        
        self.ax.fill_between(
            valores_x, y1, y2,
            color=datos_relleno['color'],
            alpha=datos_relleno['alpha'],
            label=datos_relleno['etiqueta'],
            zorder=1
        )
    
    def _graficarPunto(self, datos_punto):
        """Grafica un punto."""
        self.ax.plot(
            datos_punto['x'], datos_punto['y'],
            marker=datos_punto['marcador'],
            color=datos_punto['color'],
            markersize=datos_punto['dimension'],
            label=datos_punto['etiqueta'],
            zorder=5
        )
    
    def _graficarLineaVertical(self, datos_linea):
        """Grafica una línea vertical."""
        self.ax.axvline(
            x=datos_linea['x'],
            color=datos_linea['color'],
            linestyle=datos_linea['estiloLinea'],
            alpha=0.6,
            label=datos_linea['etiqueta'],
            zorder=2
        )
    
    def _graficarLineaHorizontal(self, datos_linea):
        """Grafica una línea horizontal."""
        self.ax.axhline(
            y=datos_linea['y'],
            color=datos_linea['color'],
            linestyle=datos_linea['estiloLinea'],
            alpha=0.6,
            label=datos_linea['etiqueta'],
            zorder=2
        )
    
    def _evaluarObjetoOikos(self, obj, valores_x):
        """Evalúa un objeto de oikos en los valores de x."""
        from sympy import lambdify, Symbol
        
        # Intentar diferentes métodos comunes
        if hasattr(obj, 'cantidad') and callable(obj.cantidad):
            return [obj.cantidad(x) for x in valores_x]
        elif hasattr(obj, 'precio') and callable(obj.precio):
            return [obj.precio(x) for x in valores_x]
        
        # Si tiene expresión simbólica, convertirla a función
        if hasattr(obj, 'expresion'):
            try:
                from sympy import symbols
                var = list(obj.expresion.free_symbols)[0]
                func = lambdify(var, obj.expresion, 'numpy')
                return func(valores_x)
            except (IndexError, AttributeError, TypeError):
                pass

        # Si tiene __call__, intentar usarlo
        if hasattr(obj, '__call__') and not isinstance(obj, type):
            try:
                return [obj(x) for x in valores_x]
            except (TypeError, ValueError):
                pass
        
        raise ValueError(
            f"No se pudo evaluar el objeto oikos: {type(obj)}. "
            f"Asegúrate de que tenga un método .cantidad(p), .precio(q) o una expresión evaluable."
        )
    
    def _evaluarFuncion(self, funcion, valores_x):
        """Evalúa cualquier tipo de función."""
        if funcion is None:
            return 0
        elif hasattr(funcion, '__module__') and 'oikos' in str(funcion.__module__):
            return self._evaluarObjetoOikos(funcion, valores_x)
        elif callable(funcion):
            return [funcion(x) for x in valores_x]
        else:
            return funcion
    
    def _generarEtiqueta(self, funcion):
        """Genera una etiqueta automática para la función."""
        if hasattr(funcion, '__class__'):
            return funcion.__class__.__name__
        return None
    
    def _obtenerSiguienteColor(self):
        """Obtiene el siguiente color de la paleta."""
        color = self.estilo.paletaColores[self._indiceColor % len(self.estilo.paletaColores)]
        self._indiceColor += 1
        return color


# ============= FUNCIONES DE UTILIDAD =============

def graficoRapido(*funciones, **kwargs):
    """
    Función rápida para graficar múltiples funciones.
    
    Args:
        *funciones: Una o más funciones a graficar
        **kwargs: Opciones de configuración (titulo, etiquetaX, etiquetaY, etc.)
        
    Returns:
        Lienzo configurado y graficado
        
    Ejemplo:
        >>> graficoRapido(
        ...     demanda, oferta,
        ...     titulo="Mi Mercado",
        ...     etiquetaX="Cantidad",
        ...     etiquetaY="Precio"
        ... )
    """
    
    lienzo = Lienzo()
    
    # Configurar opciones
    if 'titulo' in kwargs:
        lienzo.titulo = kwargs['titulo']
    if 'etiquetaX' in kwargs:
        lienzo.etiquetaX = kwargs['etiquetaX']
    if 'etiquetaY' in kwargs:
        lienzo.etiquetaY = kwargs['etiquetaY']
    
    # Añadir funciones
    for funcion in funciones:
        lienzo.agregar(funcion)
    
    lienzo.graficar()
    return lienzo