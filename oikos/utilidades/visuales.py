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
# Usa estos colores con el prefijo 'ok.' para consistencia con 'import oikos as ok'
# Ejemplo: lienzo.agregar(demanda, color=ok.ROJO)

# COLORES PUROS
ROJO     = "#FF0000"
AZUL     = "#0000FF"
VERDE    = "#00FF00"
AMARILLO = "#FFFF00"
CIAN     = "#00FFFF"
MAGENTA  = "#FF00FF"

NARANJA  = "#FF7F00"
MORADO   = "#8000FF"
ROSA     = "#FF1493"
LIMA     = "#32FF00"

# COLORES SUAVES
TURQUESA = "#00BFFF"
CELESTE  = "#1E90FF"
VIOLETA  = "#9400D3"
CORAL    = "#FF4040"

ROJO2    = "#FF3333"
AZUL2    = "#0066FF"
VERDE2   = "#00CC66"
AMARILLO2= "#FFD700"

GRIS     = "#666666"
NEGRO    = "#000000"

# COLORES POR DEFECTO PARA ECONOMÍA
COLOR_DEMANDA = ROJO   # Rojo para demanda
COLOR_OFERTA = AZUL    # Azul para oferta

# ============= CONSTANTES DE DIRECCIÓN =============
# Para alinear ejes entre cuadrantes en gráficos matriciales
# Ejemplo: lienzo.cuadrante(2, 1, alinearX=ok.ARRIBA)
ARRIBA = 'ARRIBA'
ABAJO = 'ABAJO'
IZQUIERDA = 'IZQUIERDA'
DERECHA = 'DERECHA'


def escribir(contenido, titulo: Optional[str] = None):
    """
    Muestra resultados económicos en formato LaTeX (Jupyter) o texto plano (terminal).

    Esta función es como print() pero con formato LaTeX para Jupyter.

    Args:
        contenido: Puede ser:
                  - String: Se muestra en formato LaTeX
                  - Diccionario: Se muestra cada clave-valor en formato LaTeX
                  Ejemplo dict: {'P^*': 25, 'Q^*': 50}
                  Ejemplo str: "m = P_x X + P_y Y"
        titulo: (Opcional) Título del análisis

    Ejemplos:
        >>> # Con string (ecuación)
        >>> escribir("m = P_x X + P_y Y")

        >>> # Con diccionario (resultados)
        >>> resultados = {'Q^*': 50, 'P^*': 10, 'E_p': -1.5}
        >>> escribir(resultados, "Equilibrio de Mercado")
    """
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

        # Si es un diccionario
        if isinstance(contenido, dict):
            # Mostramos cada variable en su propia línea
            for variable, valor in contenido.items():
                # Convertimos el valor a LaTeX si es necesario
                valorLatex = latex(valor) if hasattr(valor, '__class__') and not isinstance(valor, (int, float, str)) else str(valor)

                # Mostramos cada resultado en su propia línea
                ecuacion = rf"{variable} = {valorLatex}"
                display(Math(ecuacion))

        # Si es un string
        elif isinstance(contenido, str):
            # Mostramos el string directamente en formato LaTeX
            display(Math(contenido))

        else:
            # Fallback: convertir a string
            display(Math(str(contenido)))

    else:
        # ====== TERMINAL ======
        if titulo:
            print(f"\n{'='*50}")
            print(f"  {titulo}")
            print(f"{'='*50}")

        # Si es un diccionario
        if isinstance(contenido, dict):
            # Mostramos cada resultado en su propia línea
            for variable, valor in contenido.items():
                print(f"  {variable} = {valor}")

            if titulo:
                print(f"{'='*50}\n")

        # Si es un string u otro tipo
        else:
            print(f"  {contenido}")
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
        >>> import oikos as ok
        >>> # Usar estilo personalizado
        >>> mi_estilo = ok.EstiloGrafico(
        ...     paletaColores=[ok.ROJO, ok.AZUL, ok.VERDE],
        ...     anchoLinea=3.0
        ... )
        >>> lienzo = ok.Lienzo(estilo=mi_estilo)
    """

    # Paleta de colores VIVOS (nueva para v0.3.0)
    paletaColores: List[str] = field(default_factory=lambda: [
        # COLORES PUROS
        "#FF0000",  # ROJO
        "#0000FF",  # AZUL
        "#00FF00",  # VERDE
        "#FFFF00",  # AMARILLO
        "#00FFFF",  # CIAN
        "#FF00FF",  # MAGENTA

        "#FF7F00",  # NARANJA
        "#8000FF",  # MORADO
        "#FF1493",  # ROSA
        "#32FF00",  # LIMA

        # COLORES SUAVES
        "#00BFFF",  # TURQUESA
        "#1E90FF",  # CELESTE
        "#9400D3",  # VIOLETA
        "#FF4040",  # CORAL

        "#FF3333",  # ROJO2
        "#0066FF",  # AZUL2
        "#00CC66",  # VERDE2
        "#FFD700",  # AMARILLO2

        "#666666",  # GRIS
        "#000000"   # NEGRO
    ])

    # Estilo de líneas
    anchoLinea: float = 2.5
    anchoEje: float = 1.2
    anchoGrid: float = 0.8

    # Estilo de grid
    alphaGrid: float = 0.3
    estiloLineaGrid: str = '-'
    colorGrid: str = '#cccccc'

    # Fondo y ejes
    colorFondo: str = 'white'
    colorEje: str = '#333333'

    # Texto y labels
    familiaFuente: str = 'sans-serif'
    dimensionTitulo: int = 12
    dimensionLabel: int = 11
    dimensionTick: int = 10
    dimensionLeyenda: int = 9
    pesoFuenteTitulo: str = 'bold'
    pesoFuenteLabel: str = 'bold'

    # Figura
    dimensionFigura: Tuple[int, int] = (10, 7)
    dpi: int = 100  # Alta calidad para publicaciones y presentaciones

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
    - Gráficos matriciales (múltiples secciones)

    Args:
        estilo: Configuración visual personalizada
        cuadrantes: "I" (solo primer cuadrante), "I-IV" (todos), "auto"
        relacionAspecto: "equal" (1:1) o "auto" (automático)
        matriz: (filas, columnas) para crear una matriz de secciones. Ej: (2, 2) para 4 cuadrantes
        dimensionMatriz: (ancho, alto) en pulgadas para figuras con matriz

    Ejemplo:
        >>> import oikos as ok
        >>> # Crear un gráfico simple
        >>> lienzo = ok.Lienzo()
        >>> lienzo.configurarEtiquetas(
        ...     etiquetaX="Cantidad (Q)",
        ...     etiquetaY="Precio (P)",
        ...     titulo="Mercado Competitivo"
        ... )
        >>> lienzo.agregar(demanda, etiqueta="Demanda", color=ok.ROJO)
        >>> lienzo.agregar(oferta, etiqueta="Oferta", color=ok.AZUL)
        >>> lienzo.graficar()

        >>> # Crear gráfico matricial (estilo económico clásico)
        >>> lienzo = ok.Lienzo(matriz=(2, 2), dimensionMatriz=(18, 12))
        >>> # Usar cuadrante(fila, columna) para seleccionar posición
        >>> lienzo.cuadrante(1, 2)  # Fila 1, Columna 2
        >>> lienzo.configurarEtiquetas(titulo="Cruz Keynesiana")
        >>> # ... agregar curvas ...
    """

    def __init__(self,
                 estilo: Optional[EstiloGrafico] = None,
                 cuadrantes: str = "I",
                 relacionAspecto: str = "auto",
                 matriz: Optional[Tuple[int, int]] = None,
                 dimensionMatriz: Optional[Tuple[int, int]] = None,
                 alinearEjes: bool = False,
                 mostrarLeyenda: bool = False):
        """
        Inicializa un lienzo para gráficos económicos.

        Args:
            alinearEjes: Si True, alinea los ejes compartidos entre cuadrantes (útil para IS-LM)
            mostrarLeyenda: Si True, muestra la leyenda. Por defecto False para gráficos económicos limpios
        """
        
        self.estilo = estilo or EstiloGrafico()
        self.cuadrantes = cuadrantes
        self.relacionAspecto = relacionAspecto

        # Configuración de matriz
        self.matriz = matriz
        self.dimensionMatriz = dimensionMatriz
        self.alinearEjes = alinearEjes
        self.mostrarLeyenda = mostrarLeyenda

        self.fig = None
        self.ax = None
        self.axes = None  # Array de cuadrantes si es matricial
        self._cuadrante_actual = None  # Para saber en qué cuadrante estamos trabajando

        self._funciones = []  # Lista de funciones a graficar
        self._funciones_por_cuadrante = {}  # Diccionario {(fila, col): [funciones]}
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
    
    def cuadrante(self, fila: int, columna: int, alinearX: str = None, alinearY: str = None):
        """
        Selecciona una cuadrante específica en una matriz para trabajar.

        Args:
            fila: Índice de fila (1-indexed, comienza desde 1)
            columna: Índice de columna (1-indexed, comienza desde 1)
            alinearX: Alinear eje X con cuadrante vecino. Opciones: 'ARRIBA', 'ABAJO'
            alinearY: Alinear eje Y con cuadrante vecino. Opciones: 'IZQUIERDA', 'DERECHA'

        Returns:
            self (para encadenar métodos)

        Ejemplo:
            >>> lienzo = Lienzo(matriz=(3, 2))
            >>> # Cuadrante (2,1): tiene vecino arriba (1,1) y abajo (3,1)
            >>> lienzo.cuadrante(2, 1, alinearX='ARRIBA')
            >>> lienzo.configurarEtiquetas(titulo="Gráfica central")
            >>> lienzo.agregar(funcion1)
        """
        if not self.matriz:
            raise ValueError("Este lienzo no tiene una matriz de cuadrantes. Usa matriz=(filas, cols) al crear el Lienzo.")

        # Convertir de 1-indexed a 0-indexed
        filaIdx = fila - 1
        columnaIdx = columna - 1

        # Validar índices
        if fila < 1 or fila > self.matriz[0]:
            raise ValueError(f"Fila {fila} fuera de rango. Debe estar entre 1 y {self.matriz[0]}.")
        if columna < 1 or columna > self.matriz[1]:
            raise ValueError(f"Columna {columna} fuera de rango. Debe estar entre 1 y {self.matriz[1]}.")

        # Validar alineación de ejes con vecinos tipo torre (knn=1)
        alinearXValidado = None
        alinearYValidado = None

        if alinearX:
            if alinearX == 'ARRIBA' and fila > 1:
                # Verificar que existe vecino arriba
                alinearXValidado = 'ARRIBA'
            elif alinearX == 'ABAJO' and fila < self.matriz[0]:
                # Verificar que existe vecino abajo
                alinearXValidado = 'ABAJO'
            elif alinearX in ['ARRIBA', 'ABAJO']:
                # No tiene vecino en esa dirección, ignorar
                pass

        if alinearY:
            if alinearY == 'IZQUIERDA' and columna > 1:
                # Verificar que existe vecino a la izquierda
                alinearYValidado = 'IZQUIERDA'
            elif alinearY == 'DERECHA' and columna < self.matriz[1]:
                # Verificar que existe vecino a la derecha
                alinearYValidado = 'DERECHA'
            elif alinearY in ['IZQUIERDA', 'DERECHA']:
                # No tiene vecino en esa dirección, ignorar
                pass

        self._cuadrante_actual = (filaIdx, columnaIdx)

        # Resetear configuraciones para esta cuadrante
        self.etiquetaX = "x"
        self.etiquetaY = "y"
        self.titulo = ""
        self.rangoX = None
        self.rangoY = None
        self.pasoX = None
        self.pasoY = None

        # Inicializar lista de funciones para esta cuadrante si no existe
        if self._cuadrante_actual not in self._funciones_por_cuadrante:
            self._funciones_por_cuadrante[self._cuadrante_actual] = {
                'funciones': [],
                'etiquetaX': 'x',
                'etiquetaY': 'y',
                'titulo': '',
                'rangoX': None,
                'rangoY': None,
                'pasoX': None,
                'pasoY': None,
                'indiceColor': 0,
                'alinearX': alinearXValidado,
                'alinearY': alinearYValidado
            }
        else:
            # Actualizar alineación si ya existe
            self._funciones_por_cuadrante[self._cuadrante_actual]['alinearX'] = alinearXValidado
            self._funciones_por_cuadrante[self._cuadrante_actual]['alinearY'] = alinearYValidado

        return self

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

        # Si estamos en modo matricial, guardar configuración para la cuadrante actual
        if self.matriz and self._cuadrante_actual:
            if etiquetaX:
                self._funciones_por_cuadrante[self._cuadrante_actual]['etiquetaX'] = etiquetaX
            if etiquetaY:
                self._funciones_por_cuadrante[self._cuadrante_actual]['etiquetaY'] = etiquetaY
            if titulo:
                self._funciones_por_cuadrante[self._cuadrante_actual]['titulo'] = titulo

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
                    - Tupla de arrays: (valoresX, valoresY)
            etiqueta: Texto para la leyenda
            color: Color de la curva (hex o nombre). Si no se especifica, se detecta automáticamente:
                   ok.ROJO para Demanda, ok.VERDE para Oferta, colores de paleta para otros
            anchoLinea: Grosor de la línea
            estiloLinea: '-' (sólida), '--' (guiones), ':' (puntos)
            rangoPersonalizado: Rango específico para esta función

        Returns:
            self (para encadenar métodos)

        Ejemplo:
            >>> import oikos as ok
            >>> lienzo.agregar(demanda, etiqueta="Demanda", color=ok.ROJO)
            >>> lienzo.agregar(oferta, etiqueta="Oferta", color=ok.VERDE2)
            >>> lienzo.agregar(lambda q: 20 + 0.5*q, etiqueta="Otra", color=ok.AZUL)
        """
        # Auto-detectar si es un objeto de oikos
        esObjetoOikos = hasattr(funcion, '__module__') and 'oikos' in str(funcion.__module__)

        # Detectar tipo de función para color automático
        tipoFuncion = None
        if esObjetoOikos:
            nombreClase = funcion.__class__.__name__
            if 'Demanda' in nombreClase:
                tipoFuncion = 'demanda'
            elif 'Oferta' in nombreClase:
                tipoFuncion = 'oferta'

        # Determinar color final
        if color:
            colorFinal = color
        elif tipoFuncion == 'demanda':
            colorFinal = COLOR_DEMANDA
        elif tipoFuncion == 'oferta':
            colorFinal = COLOR_OFERTA
        else:
            # Si estamos en modo matricial, usar el índice de color de la cuadrante actual
            if self.matriz and self._cuadrante_actual:
                cuadranteInfo = self._funciones_por_cuadrante[self._cuadrante_actual]
                colorFinal = self.estilo.paletaColores[cuadranteInfo['indiceColor'] % len(self.estilo.paletaColores)]
                cuadranteInfo['indiceColor'] += 1
            else:
                colorFinal = self._obtenerSiguienteColor()

        datosFuncion = {
            'funcion': funcion,
            'etiqueta': etiqueta or self._generarEtiqueta(funcion),
            'color': colorFinal,
            'anchoLinea': anchoLinea or self.estilo.anchoLinea,
            'estiloLinea': estiloLinea,
            'rango': rangoPersonalizado,
            'esOikos': esObjetoOikos,
            'tipo': 'curva'
        }

        # Guardar en la cuadrante actual o en la lista general
        if self.matriz and self._cuadrante_actual:
            self._funciones_por_cuadrante[self._cuadrante_actual]['funciones'].append(datosFuncion)
        else:
            self._funciones.append(datosFuncion)

        return self
    
    def agregarPunto(self,
                    x: float,
                    y: float,
                    etiqueta: str = None,
                    color: str = NEGRO,
                    dimension: int = 5,
                    marcador: str = 's',
                    mostrarNombre: bool = False,
                    nombre: str = None,
                    mostrarLineasGuia: bool = True):
        """
        Añade un punto específico (útil para equilibrios).

        Args:
            x: Coordenada x
            y: Coordenada y
            etiqueta: Texto para la leyenda
            color: Color del punto
            dimension: Dimensión del marcador
            marcador: Tipo de marcador ('o', 's', '^', etc.)
            mostrarNombre: Si True, muestra el nombre junto al punto
            nombre: Nombre a mostrar (soporta LaTeX, ej: "$E_0$")
            mostrarLineasGuia: Si True, muestra líneas grises en forma de cruz

        Returns:
            self (para encadenar métodos)

        Ejemplo:
            >>> import oikos as ok
            >>> # Marcar el equilibrio
            >>> lienzo.agregarPunto(50, 25, etiqueta="Equilibrio", color=ok.VERDE,
            ...                     mostrarNombre=True, nombre="$E_0$")
        """
        datosPunto = {
            'x': x,
            'y': y,
            'etiqueta': etiqueta,
            'color': color or self._obtenerSiguienteColor(),
            'dimension': dimension,
            'marcador': marcador,
            'mostrarNombre': mostrarNombre,
            'nombre': nombre,
            'mostrarLineasGuia': mostrarLineasGuia,
            'tipo': 'punto'
        }

        # Guardar en la cuadrante actual o en la lista general
        if self.matriz and self._cuadrante_actual:
            self._funciones_por_cuadrante[self._cuadrante_actual]['funciones'].append(datosPunto)
        else:
            self._funciones.append(datosPunto)

        return self
    
    def agregarLineaVertical(self,
                            x: float,
                            etiqueta: str = None,
                            color: str = 'gray',
                            estiloLinea: str = ':'):
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
        datosLinea = {
            'x': x,
            'etiqueta': etiqueta,
            'color': color,
            'estiloLinea': estiloLinea,
            'tipo': 'linea_vertical'
        }

        # Guardar en la cuadrante actual o en la lista general
        if self.matriz and self._cuadrante_actual:
            self._funciones_por_cuadrante[self._cuadrante_actual]['funciones'].append(datosLinea)
        else:
            self._funciones.append(datosLinea)

        return self

    def agregarLineaHorizontal(self,
                              y: float,
                              etiqueta: str = None,
                              color: str = 'gray',
                              estiloLinea: str = ':'):
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
        datosLinea = {
            'y': y,
            'etiqueta': etiqueta,
            'color': color,
            'estiloLinea': estiloLinea,
            'tipo': 'linea_horizontal'
        }

        # Guardar en la cuadrante actual o en la lista general
        if self.matriz and self._cuadrante_actual:
            self._funciones_por_cuadrante[self._cuadrante_actual]['funciones'].append(datosLinea)
        else:
            self._funciones.append(datosLinea)

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
            >>> import oikos as ok
            >>> # Excedente del consumidor
            >>> lienzo.agregarRelleno(
            ...     demanda,
            ...     lambda q: precioEquilibrio,
            ...     rangoX=(0, cantidadEquilibrio),
            ...     color=ok.AZUL,
            ...     etiqueta="Excedente Consumidor"
            ... )
        """
        datosRelleno = {
            'funcion1': funcion1,
            'funcion2': funcion2,
            'rangoX': rangoX,
            'color': color or self._obtenerSiguienteColor(),
            'alpha': alpha or self.estilo.alphaRelleno,
            'etiqueta': etiqueta,
            'tipo': 'relleno'
        }

        # Guardar en la cuadrante actual o en la lista general
        if self.matriz and self._cuadrante_actual:
            self._funciones_por_cuadrante[self._cuadrante_actual]['funciones'].append(datosRelleno)
        else:
            self._funciones.append(datosRelleno)

        return self
    
    def graficar(self, mostrar: bool = True):
        """
        Genera y muestra el gráfico con todos los elementos añadidos.

        Args:
            mostrar: Si True, muestra el gráfico inmediatamente

        Returns:
            (fig, ax) o (fig, axes) - La figura y ejes de matplotlib
        """
        # Si es modo matricial
        if self.matriz:
            return self._graficarMatriz(mostrar)

        # Modo simple (un solo gráfico)
        # Crear figura
        self.fig, self.ax = plt.subplots(
            figsize=self.estilo.dimensionFigura,
            dpi=self.estilo.dpi
        )

        # Configurar estilo general
        self._configurarEstiloGeneral(self.ax)

        # Configurar cuadrantes
        self._configurarCuadrantes(self.ax)

        # Graficar todas las funciones
        self._graficarFunciones(self.ax, self._funciones)

        # Configurar ejes y etiquetas
        self._configurarEjes(self.ax, self.etiquetaX, self.etiquetaY, self.titulo,
                           self.rangoX, self.rangoY)

        # Añadir leyenda solo si está activada y hay etiquetas
        if self.mostrarLeyenda:
            etiquetasExistentes = [f['etiqueta'] for f in self._funciones if f.get('etiqueta')]
            if etiquetasExistentes:
                self.ax.legend(
                    fontsize=self.estilo.dimensionLeyenda,
                    framealpha=0.9,
                    loc='upper center',
                    bbox_to_anchor=(0.5, -0.1),
                    ncol=min(3, len(etiquetasExistentes))
                )

        # Ajustar diseño
        plt.tight_layout()

        if mostrar:
            plt.show()

        return self.fig, self.ax

    def _graficarMatriz(self, mostrar: bool = True):
        """
        Genera gráficos en modo matricial.
        """
        filas, columnas = self.matriz
        figsize = self.dimensionMatriz or (6 * columnas, 5 * filas)

        # Si se requiere alineación de ejes, usar sharex y sharey
        if self.alinearEjes:
            self.fig, self.axes = plt.subplots(
                filas, columnas,
                figsize=figsize,
                dpi=self.estilo.dpi,
                sharex='col',  # Compartir eje X por columnas
                sharey='row'   # Compartir eje Y por filas
            )
        else:
            self.fig, self.axes = plt.subplots(
                filas, columnas,
                figsize=figsize,
                dpi=self.estilo.dpi
            )

        # Asegurar que axes sea siempre 2D
        if filas == 1 and columnas == 1:
            self.axes = np.array([[self.axes]])
        elif filas == 1:
            self.axes = self.axes.reshape(1, -1)
        elif columnas == 1:
            self.axes = self.axes.reshape(-1, 1)

        # Graficar cada cuadrante
        for (fila, col), cuadranteData in self._funciones_por_cuadrante.items():
            ax = self.axes[fila, col]

            # Configurar estilo general
            self._configurarEstiloGeneral(ax)

            # Configurar cuadrantes
            self._configurarCuadrantes(ax)

            # Graficar funciones de esta cuadrante
            self._graficarFunciones(ax, cuadranteData['funciones'])

            # Configurar ejes y etiquetas
            self._configurarEjes(
                ax,
                cuadranteData['etiquetaX'],
                cuadranteData['etiquetaY'],
                cuadranteData['titulo'],
                cuadranteData['rangoX'],
                cuadranteData['rangoY']
            )

            # Añadir leyenda solo si está activada y hay etiquetas
            if self.mostrarLeyenda:
                etiquetasExistentes = [f['etiqueta'] for f in cuadranteData['funciones'] if f.get('etiqueta')]
                if etiquetasExistentes:
                    ax.legend(
                        fontsize=self.estilo.dimensionLeyenda,
                        framealpha=0.9,
                        loc='upper center',
                        bbox_to_anchor=(0.5, -0.1),
                        ncol=min(3, len(etiquetasExistentes))
                    )

        # APLICAR ALINEACIÓN ESPECÍFICA DE EJES ENTRE CUADRANTES
        for (fila, col), cuadranteData in self._funciones_por_cuadrante.items():
            axActual = self.axes[fila, col]

            # Alinear eje X con vecino ARRIBA o ABAJO
            if cuadranteData.get('alinearX'):
                if cuadranteData['alinearX'] == 'ARRIBA' and fila > 0:
                    axVecino = self.axes[fila - 1, col]
                    axActual.sharex(axVecino)
                elif cuadranteData['alinearX'] == 'ABAJO' and fila < filas - 1:
                    axVecino = self.axes[fila + 1, col]
                    axActual.sharex(axVecino)

            # Alinear eje Y con vecino IZQUIERDA o DERECHA
            if cuadranteData.get('alinearY'):
                if cuadranteData['alinearY'] == 'IZQUIERDA' and col > 0:
                    axVecino = self.axes[fila, col - 1]
                    axActual.sharey(axVecino)
                elif cuadranteData['alinearY'] == 'DERECHA' and col < columnas - 1:
                    axVecino = self.axes[fila, col + 1]
                    axActual.sharey(axVecino)

        # Ocultar cuadrantes vacías
        for fila in range(filas):
            for col in range(columnas):
                if (fila, col) not in self._funciones_por_cuadrante:
                    self.axes[fila, col].axis('off')

        # Ajustar diseño
        plt.tight_layout()

        if mostrar:
            plt.show()

        return self.fig, self.axes
    
    # ========== MÉTODOS PRIVADOS ==========

    def _configurarEstiloGeneral(self, ax):
        """Configura el estilo general del gráfico."""
        ax.set_facecolor(self.estilo.colorFondo)

        # Grid con estilo mejorado (cuadrados)
        ax.grid(
            True,
            alpha=self.estilo.alphaGrid,
            linestyle=self.estilo.estiloLineaGrid,
            linewidth=self.estilo.anchoGrid,
            color=self.estilo.colorGrid
        )

        # Configurar fuentes
        plt.rcParams['font.family'] = self.estilo.familiaFuente

        # Hacer que los ejes tengan el mismo aspecto (cuadrados en el grid)
        ax.set_aspect('auto')

    def _configurarCuadrantes(self, ax):
        """Configura los cuadrantes visibles con estilo de bordes completos."""
        # Mostrar todos los bordes (estilo de cuadro)
        ax.spines['top'].set_visible(True)
        ax.spines['right'].set_visible(True)
        ax.spines['bottom'].set_visible(True)
        ax.spines['left'].set_visible(True)

        # Aplicar estilos a todos los spines
        for spine in ['top', 'right', 'bottom', 'left']:
            ax.spines[spine].set_linewidth(self.estilo.anchoEje)
            ax.spines[spine].set_color(self.estilo.colorEje)

    def _configurarEjes(self, ax, etiquetaX, etiquetaY, titulo, rangoX, rangoY):
        """Configura las etiquetas y rangos de los ejes."""
        # Desactivar LaTeX en matplotlib
        plt.rcParams['text.usetex'] = False

        # Etiquetas (sin LaTeX)
        ax.set_xlabel(
            etiquetaX,
            fontsize=self.estilo.dimensionLabel,
            fontweight=self.estilo.pesoFuenteLabel
        )
        ax.set_ylabel(
            etiquetaY,
            fontsize=self.estilo.dimensionLabel,
            fontweight=self.estilo.pesoFuenteLabel
        )

        # Título
        if titulo:
            ax.set_title(
                titulo,
                fontsize=self.estilo.dimensionTitulo,
                fontweight=self.estilo.pesoFuenteTitulo,
                pad=15
            )

        # RANGOS AUTOMÁTICOS (v0.3.0)
        # Las gráficas DEBEN ocupar TODO el espacio sin dejar márgenes
        if not rangoX or not rangoY:
            # Obtener los límites actuales de matplotlib (basados en los datos graficados)
            xlimActual = ax.get_xlim()
            ylimActual = ax.get_ylim()

            # Usar rangos exactos de los datos para ocupar TODO el cuadro
            if not rangoX:
                xMin, xMax = xlimActual
                ax.set_xlim(xMin, xMax)

            if not rangoY:
                yMin, yMax = ylimActual
                ax.set_ylim(yMin, yMax)
        else:
            # Rangos manuales
            if rangoX:
                ax.set_xlim(rangoX)
            if rangoY:
                ax.set_ylim(rangoY)

        # Dimensión de ticks
        ax.tick_params(labelsize=self.estilo.dimensionTick)

    def _graficarFunciones(self, ax, funciones):
        """Grafica todas las funciones añadidas."""
        for datosFuncion in funciones:
            tipo_func = datosFuncion.get('tipo')

            if tipo_func == 'punto':
                self._graficarPunto(ax, datosFuncion)
            elif tipo_func == 'linea_vertical':
                self._graficarLineaVertical(ax, datosFuncion)
            elif tipo_func == 'linea_horizontal':
                self._graficarLineaHorizontal(ax, datosFuncion)
            elif tipo_func == 'relleno':
                self._graficarRelleno(ax, datosFuncion)
            else:
                self._graficarCurva(ax, datosFuncion)
    
    def _graficarCurva(self, ax, datosFuncion):
        """Grafica una curva, ocultando partes negativas."""
        funcion = datosFuncion['funcion']

        # Determinar rango de x
        if datosFuncion['rango']:
            xMin, xMax = datosFuncion['rango']
        elif self.rangoX:
            xMin, xMax = self.rangoX
        else:
            # AUTODETECCIÓN DE RANGO (v0.3.0)
            # Si el usuario no especificó rango, intentamos deducirlo de los datos
            # Para tuplas (x, y), usamos directamente los valores de x
            if isinstance(funcion, tuple) and len(funcion) == 2:
                valoresXTemp = np.array(funcion[0])
                xMin = float(np.min(valoresXTemp))
                xMax = float(np.max(valoresXTemp))
            else:
                # Para funciones, usar rango por defecto
                xMin, xMax = 0, 100

        valoresX = np.linspace(xMin, xMax, 500)

        # Calcular valoresY según el tipo de función
        if isinstance(funcion, tuple) and len(funcion) == 2:
            # Datos pre-calculados - USAR DIRECTAMENTE sin linspace
            valoresX, valoresY = funcion
            valoresX = np.array(valoresX)
            valoresY = np.array(valoresY)
        elif datosFuncion['esOikos']:
            # Objeto de oikos
            valoresY = self._evaluarObjetoOikos(funcion, valoresX)
        elif callable(funcion):
            # Función Python normal
            valoresY = np.array([funcion(x) for x in valoresX])
        else:
            raise TypeError(
                f"Tipo de función no soportado: {type(funcion).__name__}. "
                f"Se esperaba un objeto de oikos, función callable o tupla (x, y)."
            )

        # Asegurar que valoresY sea un array numpy
        if not isinstance(valoresY, np.ndarray):
            valoresY = np.array(valoresY)

        # GRAFICAR TODA LA FUNCIÓN: incluir valores negativos y positivos
        # Solo filtrar valores NaN/infinitos
        mask = ~np.isnan(valoresY) & ~np.isinf(valoresY)
        valoresXFiltrados = valoresX[mask]
        valoresYFiltrados = valoresY[mask]

        # Solo graficar si hay puntos válidos
        if len(valoresXFiltrados) > 0:
            ax.plot(
                valoresXFiltrados, valoresYFiltrados,
                color=datosFuncion['color'],
                linewidth=datosFuncion['anchoLinea'],
                linestyle=datosFuncion['estiloLinea'],
                label=datosFuncion['etiqueta'],
                zorder=3
            )

    def _graficarRelleno(self, ax, datosRelleno):
        """Grafica un área de relleno."""
        rangoX = datosRelleno['rangoX'] or self.rangoX or (0, 100)
        valoresX = np.linspace(rangoX[0], rangoX[1], 500)

        # Evaluar funciones
        y1 = self._evaluarFuncion(datosRelleno['funcion1'], valoresX)
        y2 = self._evaluarFuncion(datosRelleno['funcion2'], valoresX) if datosRelleno['funcion2'] else 0

        # Filtrar solo valores NaN/infinitos
        if isinstance(y1, np.ndarray):
            mask = ~np.isnan(y1) & ~np.isinf(y1)
            if isinstance(y2, np.ndarray):
                mask = mask & ~np.isnan(y2) & ~np.isinf(y2)
        else:
            mask = np.ones(len(valoresX), dtype=bool)

        # Aplicar máscara
        valoresXFiltrados = valoresX[mask]
        y1_filtrado = y1[mask] if isinstance(y1, np.ndarray) else y1
        if isinstance(y2, np.ndarray):
            y2_filtrado = y2[mask]
        else:
            y2_filtrado = y2

        # Solo graficar si hay puntos válidos
        if len(valoresXFiltrados) > 0:
            ax.fill_between(
                valoresXFiltrados, y1_filtrado, y2_filtrado,
                color=datosRelleno['color'],
                alpha=datosRelleno['alpha'],
                label=datosRelleno['etiqueta'],
                zorder=1
            )

    def _graficarPunto(self, ax, datosPunto):
        """Grafica un punto."""
        xVal = datosPunto['x']
        yVal = datosPunto['y']

        # Agregar líneas guía en forma de cruz si está activado
        if datosPunto.get('mostrarLineasGuia', True):
            ax.axvline(x=xVal, color='gray', linestyle=':', alpha=0.5, zorder=1)
            ax.axhline(y=yVal, color='gray', linestyle=':', alpha=0.5, zorder=1)

        ax.plot(
            xVal, yVal,
            marker=datosPunto['marcador'],
            color=datosPunto['color'],
            markersize=datosPunto['dimension'],
            label=datosPunto['etiqueta'],
            zorder=5
        )

        # Agregar nombre si se especifica
        if datosPunto.get('mostrarNombre') and datosPunto.get('nombre'):
            ax.annotate(
                datosPunto['nombre'],
                xy=(xVal, yVal),
                xytext=(5, 5),
                textcoords='offset points',
                fontsize=self.estilo.dimensionLabel,
                color=datosPunto['color']
            )

    def _graficarLineaVertical(self, ax, datosLinea):
        """Grafica una línea vertical."""
        ax.axvline(
            x=datosLinea['x'],
            color=datosLinea['color'],
            linestyle=datosLinea['estiloLinea'],
            alpha=0.5,
            label=datosLinea['etiqueta'],
            zorder=2
        )

    def _graficarLineaHorizontal(self, ax, datosLinea):
        """Grafica una línea horizontal."""
        ax.axhline(
            y=datosLinea['y'],
            color=datosLinea['color'],
            linestyle=datosLinea['estiloLinea'],
            alpha=0.5,
            label=datosLinea['etiqueta'],
            zorder=2
        )
    
    def _evaluarObjetoOikos(self, obj, valoresX):
        """
        Evalúa un objeto de oikos en los valores de x.

        IMPORTANTE: Los economistas grafican FUNCIONES INVERSAS.
        - Si tenemos Q = 100 - 2P, graficamos P en el eje Y vs Q en el eje X
        - Por lo tanto: valoresX representa cantidades (Q), valoresY representa precios (P)
        - Usamos obj.precio(cantidad) para obtener P dado Q
        """
        import numpy as np

        # ECONOMISTAS GRAFICAN INVERSAS: eje X = cantidad (Q), eje Y = precio (P)
        # Por lo tanto, siempre usamos precio(cantidad)
        if hasattr(obj, 'precio') and callable(obj.precio):
            valoresY = []
            for q in valoresX:  # valoresX son cantidades
                try:
                    p = obj.precio(q)  # obtenemos precio
                    # Asegurar que sea real
                    if isinstance(p, complex):
                        p = p.real
                    valoresY.append(p)
                except Exception:
                    valoresY.append(np.nan)
            return np.array(valoresY)

        # Si tiene expresión simbólica, convertirla a función
        if hasattr(obj, 'expresion'):
            try:
                from sympy import lambdify
                var = list(obj.expresion.free_symbols)[0]
                func = lambdify(var, obj.expresion, 'numpy')
                valoresY = func(valoresX)
                # Asegurar que sean reales
                if np.iscomplexobj(valoresY):
                    valoresY = np.real(valoresY)
                return valoresY
            except (IndexError, AttributeError, TypeError):
                pass

        # Si tiene __call__, intentar usarlo
        if hasattr(obj, '__call__') and not isinstance(obj, type):
            try:
                valoresY = []
                for x in valoresX:
                    try:
                        y = obj(x)
                        if isinstance(y, complex):
                            y = y.real
                        valoresY.append(y)
                    except Exception:
                        valoresY.append(np.nan)
                return np.array(valoresY)
            except (TypeError, ValueError):
                pass

        raise ValueError(
            f"No se pudo evaluar el objeto oikos: {type(obj)}. "
            f"Asegúrate de que tenga un método .cantidad(p), .precio(q) o una expresión evaluable."
        )
    
    def _evaluarFuncion(self, funcion, valoresX):
        """Evalúa cualquier tipo de función."""
        import numpy as np

        if funcion is None:
            return 0
        elif hasattr(funcion, '__module__') and 'oikos' in str(funcion.__module__):
            return self._evaluarObjetoOikos(funcion, valoresX)
        elif callable(funcion):
            valoresY = []
            for x in valoresX:
                try:
                    y = funcion(x)
                    # Asegurar que sea real
                    if isinstance(y, complex):
                        y = y.real
                    valoresY.append(y)
                except Exception:
                    valoresY.append(np.nan)
            return np.array(valoresY)
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
        *funciones: Una o más funciones a graficar. Acepta:
                   - Objetos de oikos (Demanda, Oferta, etc.)
                   - Tuplas (x, y) de arrays
                   - Si el primer argumento es un array y el segundo es una lista de arrays,
                     se interpreta como (x, [y1, y2, ...])
        **kwargs: Opciones de configuración
                 - titulo: Título del gráfico
                 - etiquetaX: Etiqueta del eje X
                 - etiquetaY: Etiqueta del eje Y
                 - leyendas: Lista de etiquetas para las curvas
                 - colores: Lista de colores para las curvas

    Returns:
        Lienzo configurado y graficado

    Ejemplo:
        >>> # Con objetos de oikos
        >>> graficoRapido(
        ...     demanda, oferta,
        ...     titulo="Mi Mercado",
        ...     etiquetaX="Cantidad",
        ...     etiquetaY="Precio"
        ... )
        >>>
        >>> # Con arrays numpy
        >>> x = np.linspace(0, 10, 100)
        >>> y1 = 100 - 2*x
        >>> y2 = -20 + 3*x
        >>> graficoRapido(
        ...     x, [y1, y2],
        ...     titulo="Oferta y Demanda",
        ...     leyendas=["Demanda", "Oferta"]
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

    # Extraer configuraciones opcionales
    leyendas = kwargs.get('leyendas', [])
    colores = kwargs.get('colores', [])

    # Caso especial: graficoRapido(x, [y1, y2, ...], ...)
    if len(funciones) == 2 and hasattr(funciones[0], '__iter__') and hasattr(funciones[1], '__iter__'):
        # Verificar si el segundo argumento es una lista de arrays
        try:
            import numpy as np
            xVals = funciones[0]
            yVals = funciones[1]

            # Si yVals es una lista/array de arrays
            if isinstance(yVals, (list, tuple)):
                for i, y in enumerate(yVals):
                    etiqueta = leyendas[i] if i < len(leyendas) else None
                    color = colores[i] if i < len(colores) else None
                    lienzo.agregar((xVals, y), etiqueta=etiqueta, color=color)
                lienzo.graficar()
                return lienzo
        except (TypeError, IndexError, AttributeError):
            pass  # Si falla, continuar con el procesamiento normal

    # Procesamiento normal: cada argumento es una función independiente
    for i, funcion in enumerate(funciones):
        etiqueta = leyendas[i] if i < len(leyendas) else None
        color = colores[i] if i < len(colores) else None
        lienzo.agregar(funcion, etiqueta=etiqueta, color=color)

    lienzo.graficar()
    return lienzo