from IPython.display import display, Math
from sympy import latex

import matplotlib.pyplot as plt
import numpy as np
from typing import Optional, Tuple, List, Union, Callable
from dataclasses import dataclass, field


def write(results_dict, title=None):
    """
    Función universal para mostrar resultados de Oikos.
    
    Args:
        results_dict (dict): Diccionario con variables y valores. 
                            Ej: {'Q^*': 50, 'P^*': 10}
        title (str, optional): Encabezado del análisis.
    """
    # 1. Preparar las partes de la ecuación en LaTeX
    # latex() se encarga de que las fracciones y exponentes se vean pro
    parts = [rf"{key} = {latex(val)}" for key, val in results_dict.items()]
    
    # Unimos con un punto y coma elegante
    tex_body = " \quad ; \quad ".join(parts)
    
    try:
        from IPython import get_ipython
        # Si detectamos Jupyter/Colab
        if get_ipython() is not None:
            if title:
                display(Math(rf"\text{{\textbf{{{title}}}}}"))
            display(Math(tex_body))
        else:
            # Si es terminal pura
            if title: print(f"--- {title} ---")
            print(", ".join([f"{k} = {v}" for k, v in results_dict.items()]))
            
    except (ImportError, NameError):
        # Fallback de seguridad por si no hay IPython instalado
        if title: print(f"--- {title} ---")
        print(", ".join([f"{k} = {v}" for k, v in results_dict.items()]))


@dataclass
class GraphStyle:
    """Configuración de estilo para gráficos económicos"""
    
    # Paleta de colores por defecto (se ciclan automáticamente)
    color_palette: List[str] = field(default_factory=lambda: [
        '#2E7D99',  # Azul petróleo
        '#8B4A4A',  # Marrón rojizo
        '#2C6B4F',  # Verde oscuro
        '#8B6914',  # Dorado oscuro
        '#6B4A8B',  # Púrpura
        '#8B2C2C',  # Rojo oscuro
    ])
    
    # Estilo de líneas
    curve_linewidth: float = 2.5
    axis_linewidth: float = 1.5
    grid_linewidth: float = 0.5
    
    # Estilo de grid
    grid_alpha: float = 0.3
    grid_linestyle: str = '--'
    
    # Fondo y ejes
    background_color: str = 'white'
    spine_color: str = '#2C3E50'
    
    # Texto y labels
    font_family: str = 'serif'
    title_size: int = 14
    label_size: int = 12
    tick_size: int = 10
    legend_size: int = 10
    
    # Figura
    figure_size: Tuple[int, int] = (10, 7)
    dpi: int = 100
    
    # Áreas de relleno
    fill_alpha: float = 0.4


class Canvas:
    """
    Lienzo flexible para gráficos económicos
    
    Permite graficar múltiples funciones económicas con control total sobre:
    - Ejes y cuadrantes
    - Escalas y proporciones
    - Leyendas y títulos
    - Auto-graficado de objetos de oikos
    """
    
    def __init__(self, 
                 style: Optional[GraphStyle] = None,
                 quadrants: str = "I",
                 aspect_ratio: str = "auto"):
        """
        Inicializa un lienzo para gráficos económicos
        
        Args:
            style: Configuración de estilo personalizada
            quadrants: Cuadrantes a mostrar ("I", "I-IV", "all", etc.)
            aspect_ratio: Relación de aspecto ("equal" para 1:1, "auto" para automático)
        """
        self.style = style or GraphStyle()
        self.quadrants = quadrants
        self.aspect_ratio = aspect_ratio
        
        self.fig = None
        self.ax = None
        self._functions = []  # Lista de funciones a graficar
        self._color_index = 0
        
        # Configuración de ejes
        self.x_label = "x"
        self.y_label = "y"
        self.title = ""
        
        # Rangos de ejes (None = automático)
        self.x_range = None
        self.y_range = None
        
        # Configuración de saltos (ticks)
        self.x_step = None
        self.y_step = None
        
    def setLabels(self, xlabel: str = None, ylabel: str = None, title: str = None):
        """
        Configura las etiquetas de los ejes y título
        
        Args:
            xlabel: Etiqueta del eje X
            ylabel: Etiqueta del eje Y
            title: Título del gráfico
        """
        if xlabel:
            self.x_label = xlabel
        if ylabel:
            self.y_label = ylabel
        if title:
            self.title = title
        return self
    
    def setRange(self, 
                 x_range: Tuple[float, float] = None,
                 y_range: Tuple[float, float] = None):
        """
        Configura el rango de los ejes
        
        Args:
            x_range: (min, max) para eje X
            y_range: (min, max) para eje Y
        """
        self.x_range = x_range
        self.y_range = y_range
        return self
    
    def setTicks(self, x_step: float = None, y_step: float = None):
        """
        Configura el salto entre marcas de los ejes
        
        Args:
            x_step: Salto para el eje X
            y_step: Salto para el eje Y
        """
        self.x_step = x_step
        self.y_step = y_step
        return self
    
    def add(self, 
            func,
            label: str = None,
            color: str = None,
            linewidth: float = None,
            linestyle: str = '-',
            range_override: Tuple[float, float] = None):
        """
        Añade una función para graficar
        
        Args:
            func: Puede ser:
                  - Objeto de oikos (Demand, Supply, etc.) con método auto-plot
                  - Función callable que recibe x y retorna y
                  - Tupla de arrays (x_values, y_values)
            label: Etiqueta para la leyenda (None = auto)
            color: Color de la curva (None = automático)
            linewidth: Grosor de línea (None = usar estilo por defecto)
            linestyle: Estilo de línea ('-', '--', '-.', ':')
            range_override: Rango específico para esta función
        """
        # Auto-detectar si es un objeto de oikos
        is_oikos_object = hasattr(func, '__module__') and 'oikos' in func.__module__
        
        func_data = {
            'func': func,
            'label': label or self._generate_label(func),
            'color': color or self._get_next_color(),
            'linewidth': linewidth or self.style.curve_linewidth,
            'linestyle': linestyle,
            'range': range_override,
            'is_oikos': is_oikos_object
        }
        
        self._functions.append(func_data)
        return self
    
    def addFill(self,
                func1,
                func2=None,
                x_range: Tuple[float, float] = None,
                color: str = None,
                alpha: float = None,
                label: str = None):
        """
        Añade un área de relleno entre dos funciones o entre una función y el eje
        
        Args:
            func1: Primera función (o la única si func2 es None)
            func2: Segunda función (None = rellenar hasta el eje x)
            x_range: Rango de x para el relleno
            color: Color del relleno
            alpha: Transparencia
            label: Etiqueta para la leyenda
        """
        fill_data = {
            'type': 'fill',
            'func1': func1,
            'func2': func2,
            'x_range': x_range,
            'color': color or self._get_next_color(),
            'alpha': alpha or self.style.fill_alpha,
            'label': label
        }
        
        self._functions.append(fill_data)
        return self
    
    def addPoint(self,
                 x: float,
                 y: float,
                 label: str = None,
                 color: str = None,
                 size: float = 10,
                 marker: str = 'o'):
        """
        Añade un punto específico (ej: equilibrio)
        
        Args:
            x: Coordenada x
            y: Coordenada y
            label: Etiqueta
            color: Color del punto
            size: Tamaño del marcador
            marker: Estilo del marcador
        """
        point_data = {
            'type': 'point',
            'x': x,
            'y': y,
            'label': label,
            'color': color or self.style.spine_color,
            'size': size,
            'marker': marker
        }
        
        self._functions.append(point_data)
        return self
    
    def addVerticalLine(self, x: float, label: str = None, color: str = None, linestyle: str = '--'):
        """Añade una línea vertical"""
        line_data = {
            'type': 'vline',
            'x': x,
            'label': label,
            'color': color or self.style.spine_color,
            'linestyle': linestyle
        }
        self._functions.append(line_data)
        return self
    
    def addHorizontalLine(self, y: float, label: str = None, color: str = None, linestyle: str = '--'):
        """Añade una línea horizontal"""
        line_data = {
            'type': 'hline',
            'y': y,
            'label': label,
            'color': color or self.style.spine_color,
            'linestyle': linestyle
        }
        self._functions.append(line_data)
        return self
    
    def plot(self, show_legend: bool = True):
        """
        Genera y muestra el gráfico con todas las funciones añadidas
        
        Args:
            show_legend: Si mostrar la leyenda
        """
        self._setup_canvas()
        self._plot_functions()
        
        if show_legend and any(f.get('label') for f in self._functions):
            self.ax.legend(loc='best', 
                          fontsize=self.style.legend_size,
                          framealpha=0.95,
                          edgecolor=self.style.spine_color,
                          fancybox=True)
        
        plt.tight_layout()
        plt.show()
    
    def save(self, filename: str, dpi: int = None):
        """Guarda el gráfico"""
        if self.fig is None:
            self._setup_canvas()
            self._plot_functions()
        
        plt.tight_layout()
        plt.savefig(filename, 
                   dpi=dpi or self.style.dpi,
                   facecolor=self.style.background_color,
                   bbox_inches='tight')
    
    def _setup_canvas(self):
        """Configura el lienzo base"""
        self.fig, self.ax = plt.subplots(
            figsize=self.style.figure_size,
            dpi=self.style.dpi,
            facecolor=self.style.background_color
        )
        
        self.ax.set_facecolor(self.style.background_color)
        
        # Configurar cuadrantes
        self._setup_quadrants()
        
        # Configurar relación de aspecto
        if self.aspect_ratio == "equal":
            self.ax.set_aspect('equal', adjustable='box')
        
        # Grid
        self.ax.grid(True,
                    alpha=self.style.grid_alpha,
                    linestyle=self.style.grid_linestyle,
                    linewidth=self.style.grid_linewidth,
                    color=self.style.spine_color)
        
        # Labels y título
        self.ax.set_xlabel(self.x_label, 
                          fontsize=self.style.label_size,
                          fontfamily=self.style.font_family,
                          weight='bold')
        
        self.ax.set_ylabel(self.y_label,
                          fontsize=self.style.label_size,
                          fontfamily=self.style.font_family,
                          weight='bold')
        
        if self.title:
            self.ax.set_title(self.title,
                            fontsize=self.style.title_size,
                            fontfamily=self.style.font_family,
                            weight='bold',
                            pad=20)
        
        # Configurar ticks
        self.ax.tick_params(labelsize=self.style.tick_size, 
                           colors=self.style.spine_color)
        
        # Aplicar rangos si están definidos
        if self.x_range:
            self.ax.set_xlim(self.x_range)
        if self.y_range:
            self.ax.set_ylim(self.y_range)
        
        # Aplicar saltos personalizados
        if self.x_step and self.x_range:
            self.ax.set_xticks(np.arange(self.x_range[0], self.x_range[1] + self.x_step, self.x_step))
        if self.y_step and self.y_range:
            self.ax.set_yticks(np.arange(self.y_range[0], self.y_range[1] + self.y_step, self.y_step))
    
    def _setup_quadrants(self):
        """Configura los cuadrantes visibles"""
        if self.quadrants == "I":
            # Solo primer cuadrante (x≥0, y≥0)
            self.ax.spines['top'].set_visible(False)
            self.ax.spines['right'].set_visible(False)
            self.ax.spines['bottom'].set_position('zero')
            self.ax.spines['left'].set_position('zero')
            
        elif self.quadrants == "all" or self.quadrants == "I-IV":
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
                self.ax.spines[spine].set_linewidth(self.style.axis_linewidth)
                self.ax.spines[spine].set_color(self.style.spine_color)
    
    def _plot_functions(self):
        """Grafica todas las funciones añadidas"""
        for func_data in self._functions:
            func_type = func_data.get('type')
            
            if func_type == 'point':
                self._plot_point(func_data)
            elif func_type == 'vline':
                self._plot_vline(func_data)
            elif func_type == 'hline':
                self._plot_hline(func_data)
            elif func_type == 'fill':
                self._plot_fill(func_data)
            else:
                self._plot_curve(func_data)
    
    def _plot_curve(self, func_data):
        """Grafica una curva"""
        func = func_data['func']
        
        # Determinar rango de x
        if func_data['range']:
            x_min, x_max = func_data['range']
        elif self.x_range:
            x_min, x_max = self.x_range
        else:
            x_min, x_max = 0, 100  # Valor por defecto
        
        x_values = np.linspace(x_min, x_max, 500)
        
        # Calcular y_values según el tipo de función
        if func_data['is_oikos']:
            # Objeto de oikos - intentar métodos comunes
            y_values = self._evaluate_oikos_object(func, x_values)
        elif callable(func):
            # Función Python normal
            y_values = [func(x) for x in x_values]
        elif isinstance(func, tuple) and len(func) == 2:
            # Datos pre-calculados
            x_values, y_values = func
        else:
            print(f"Tipo de función no soportado: {type(func)}")
            return
        
        # Graficar
        self.ax.plot(x_values, y_values,
                    color=func_data['color'],
                    linewidth=func_data['linewidth'],
                    linestyle=func_data['linestyle'],
                    label=func_data['label'],
                    zorder=3)
    
    def _plot_fill(self, fill_data):
        """Grafica un área de relleno"""
        x_range = fill_data['x_range'] or self.x_range or (0, 100)
        x_values = np.linspace(x_range[0], x_range[1], 500)
        
        # Evaluar funciones
        y1 = self._evaluate_function(fill_data['func1'], x_values)
        y2 = self._evaluate_function(fill_data['func2'], x_values) if fill_data['func2'] else 0
        
        self.ax.fill_between(x_values, y1, y2,
                            color=fill_data['color'],
                            alpha=fill_data['alpha'],
                            label=fill_data['label'],
                            zorder=1)
    
    def _plot_point(self, point_data):
        """Grafica un punto"""
        self.ax.plot(point_data['x'], point_data['y'],
                    marker=point_data['marker'],
                    color=point_data['color'],
                    markersize=point_data['size'],
                    label=point_data['label'],
                    zorder=5)
    
    def _plot_vline(self, line_data):
        """Grafica una línea vertical"""
        self.ax.axvline(x=line_data['x'],
                       color=line_data['color'],
                       linestyle=line_data['linestyle'],
                       alpha=0.5,
                       label=line_data['label'],
                       zorder=2)
    
    def _plot_hline(self, line_data):
        """Grafica una línea horizontal"""
        self.ax.axhline(y=line_data['y'],
                       color=line_data['color'],
                       linestyle=line_data['linestyle'],
                       alpha=0.5,
                       label=line_data['label'],
                       zorder=2)
    
    def _evaluate_oikos_object(self, obj, x_values):
        """Evalúa un objeto de oikos en los valores de x"""
        # Intentar diferentes métodos comunes
        if hasattr(obj, 'quantity'):
            return [obj.quantity(x) for x in x_values]
        elif hasattr(obj, 'price'):
            return [obj.price(x) for x in x_values]
        elif hasattr(obj, 'Q'):
            return [obj.Q(x) for x in x_values]
        elif hasattr(obj, 'P'):
            return [obj.P(x) for x in x_values]
        elif hasattr(obj, '__call__'):
            return [obj(x) for x in x_values]
        else:
            raise ValueError(f"No se pudo evaluar el objeto oikos: {type(obj)}")
    
    def _evaluate_function(self, func, x_values):
        """Evalúa cualquier tipo de función"""
        if func is None:
            return 0
        elif hasattr(func, '__module__') and 'oikos' in func.__module__:
            return self._evaluate_oikos_object(func, x_values)
        elif callable(func):
            return [func(x) for x in x_values]
        else:
            return func
    
    def _generate_label(self, func):
        """Genera una etiqueta automática para la función"""
        if hasattr(func, '__class__'):
            return func.__class__.__name__
        return None
    
    def _get_next_color(self):
        """Obtiene el siguiente color de la paleta"""
        color = self.style.color_palette[self._color_index % len(self.style.color_palette)]
        self._color_index += 1
        return color


# ============= FUNCIONES DE UTILIDAD =============

def quickPlot(*functions, **kwargs):
    """
    Función rápida para graficar múltiples funciones
    
    Ejemplo:
        ok.quickPlot(demanda, oferta, title="Mi Mercado")
    """
    canvas = Canvas()
    
    # Configurar opciones
    if 'title' in kwargs:
        canvas.title = kwargs['title']
    if 'xlabel' in kwargs:
        canvas.x_label = kwargs['xlabel']
    if 'ylabel' in kwargs:
        canvas.y_label = kwargs['ylabel']
    
    # Añadir funciones
    for func in functions:
        canvas.add(func)
    
    canvas.plot()
    return canvas