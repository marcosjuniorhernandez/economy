"""
Teoría del Consumidor - Utilidad, Preferencias, Restricción Presupuestaria.

Este módulo implementa las principales funciones de utilidad y herramientas
para el análisis del comportamiento del consumidor en microeconomía.
"""

import numpy as np
from typing import Tuple, Optional, List
from scipy.optimize import minimize, fsolve
from ..nucleo.base import FuncionEconomica
from ..nucleo.excepciones import ErrorValidacion, ErrorEquilibrio
from ..utilidades.validadores import validarPositivo, validarNoNegativo
from ..utilidades.decoradores import ayuda, explicacion


class FuncionUtilidad:
    """
    Clase base para funciones de utilidad del consumidor.

    Una función de utilidad representa las preferencias de un consumidor,
    asignando un número a cada cesta de consumo que refleja el nivel de
    satisfacción que proporciona.
    """

    def __init__(self, nombre: str):
        self.nombre = nombre

    def utilidad(self, x: float, y: float) -> float:
        """
        Calcula la utilidad para una canasta (x, y).

        Args:
            x: Cantidad del bien X
            y: Cantidad del bien Y

        Returns:
            Nivel de utilidad
        """
        raise NotImplementedError("Debe implementarse en las subclases")

    def utilidadMarginalX(self, x: float, y: float) -> float:
        """
        Utilidad marginal del bien X: ∂U/∂x

        Mide el cambio en utilidad por una unidad adicional de X.
        """
        raise NotImplementedError("Debe implementarse en las subclases")

    def utilidadMarginalY(self, x: float, y: float) -> float:
        """
        Utilidad marginal del bien Y: ∂U/∂y

        Mide el cambio en utilidad por una unidad adicional de Y.
        """
        raise NotImplementedError("Debe implementarse en las subclases")

    def rms(self, x: float, y: float) -> float:
        """
        Relación Marginal de Sustitución (RMS).

        RMS = UMgₓ / UMgᵧ

        Indica cuántas unidades de Y está dispuesto a ceder el consumidor
        para obtener una unidad adicional de X, manteniendo la utilidad constante.

        Returns:
            RMS en el punto (x, y)
        """
        umgY = self.utilidadMarginalY(x, y)
        if abs(umgY) < 1e-10:
            return np.inf
        return self.utilidadMarginalX(x, y) / umgY

    def graficar(self, restriccion: Optional['RestriccionPresupuestaria'] = None,
                 nivelesUtilidad: Optional[List[float]] = None,
                 mostrarOptimo: bool = True,
                 rangoX: Optional[Tuple[float, float]] = None,
                 rangoY: Optional[Tuple[float, float]] = None):
        """
        Grafica curvas de indiferencia usando Lienzo.

        Args:
            restriccion: Restricción presupuestaria (opcional)
            nivelesUtilidad: Lista de niveles de utilidad para graficar
            mostrarOptimo: Si True y hay restricción, muestra el punto óptimo
            rangoX: Rango del eje X (min, max)
            rangoY: Rango del eje Y (min, max)

        Returns:
            Lienzo configurado

        Ejemplo:
            >>> from oikos import *
            >>> utilidad = CobbDouglas(α=0.6, β=0.4)
            >>> restriccion = RestriccionPresupuestaria(m=100, Px=2, Py=4)
            >>> utilidad.graficar(restriccion)
        """
        from ..utilidades.visuales import Lienzo, ROJO, AZUL, VERDE, AMARILLO

        lienzo = Lienzo()
        lienzo.configurarEtiquetas(etiquetaX="Bien X", etiquetaY="Bien Y",
                                  titulo=f"Preferencias: {self.nombre}")

        # Determinar rango
        if restriccion:
            xMax = restriccion.cantidadMaximaX()
            yMax = restriccion.cantidadMaximaY()
        else:
            xMax = rangoX[1] if rangoX else 50
            yMax = rangoY[1] if rangoY else 50

        xMin = rangoX[0] if rangoX else 0
        yMin = rangoY[0] if rangoY else 0

        # Graficar restricción presupuestaria - SIEMPRE EN ROJO
        if restriccion:
            # Sombrear la región FACTIBLE (por debajo de la restricción)
            lienzo.agregarRelleno(
                funcion1=lambda x: 0,  # Desde el eje X
                funcion2=lambda x: restriccion.cantidadYDadaX(x) if x <= xMax else 0,  # Hasta la restricción
                rangoX=(0, xMax),
                color=ROJO,
                alpha=0.1,
                etiqueta=None
            )

            # Luego la línea de restricción
            xRestr = np.array([0, xMax])
            yRestr = np.array([yMax, 0])
            lienzo.agregar((xRestr, yRestr), etiqueta="Restricción Presupuestaria", color=ROJO, anchoLinea=2)

        # Calcular punto óptimo si hay restricción
        xOpt, yOpt, uOpt = None, None, None
        if restriccion and mostrarOptimo:
            try:
                eleccion = EleccionOptima(self, restriccion)
                xOpt, yOpt, uOpt = eleccion.optimizar()
            except:
                pass

        # Graficar SOLO la curva de indiferencia óptima (si hay restricción)
        # Si no hay restricción, graficar una curva de ejemplo
        if nivelesUtilidad is None:
            if uOpt:
                # Solo graficar la curva que pasa por el óptimo
                nivelesUtilidad = [uOpt]
            else:
                # Sin restricción: graficar una curva de ejemplo en el medio
                nivelesUtilidad = [self.utilidad(xMax*0.5, yMax*0.5)]

        # Graficar curva de indiferencia - SIEMPRE EN AZUL
        curva = CurvaIndiferencia(self)

        # Determinar rango de x según el tipo de función
        if isinstance(self, StoneGeary):
            # Stone-Geary: empezar desde γx para evitar valores inválidos
            xInicio = max(self.γx + 0.01, xMin)
        elif isinstance(self, (SustitutosPerfectos, CES)):
            # Sustitutos perfectos y CES: empezar desde 0 para mostrar toda la línea
            xInicio = 0
        else:
            # Otras funciones: empezar un poco después de 0 para evitar problemas numéricos
            xInicio = max(0.01, xMin)

        xValores = np.linspace(xInicio, xMax * 1.5, 400)

        for nivelU in nivelesUtilidad:
            try:
                yValores = curva.calcularCurva(nivelUtilidad=nivelU, xValores=xValores)

                # Filtrar valores que causan el efecto rebote
                mask = (yValores >= 0) & ~np.isnan(yValores) & ~np.isinf(yValores)
                mask = mask & (yValores <= yMax * 1.5)

                # Para Stone-Geary, también filtrar y < γγ
                if isinstance(self, StoneGeary):
                    mask = mask & (yValores >= self.γγ)

                xValores_filtrados = xValores[mask]
                yValores_filtrados = yValores[mask]

                if len(xValores_filtrados) > 0:
                    etiqueta = f"U = {nivelU:.2f}"
                    lienzo.agregar((xValores_filtrados, yValores_filtrados), etiqueta=etiqueta,
                                 color=AZUL, estiloLinea='-', anchoLinea=2)
            except:
                pass

        # Punto óptimo
        if xOpt and yOpt:
            lienzo.agregarPunto(xOpt, yOpt, etiqueta=f"Óptimo ({xOpt:.1f}, {yOpt:.1f})",
                              color='#000000', dimension=5, mostrarLineasGuia=True)

        lienzo.configurarRango(rangoX=(xMin, xMax*1.1), rangoY=(yMin, yMax*1.1))
        return lienzo.graficar()


@ayuda(
    descripcionEconomica="""
    Los sustitutos perfectos son bienes que el consumidor considera completamente
    intercambiables entre sí. La tasa de sustitución entre ellos es constante.

    Ejemplos: Coca-Cola y Pepsi para algunos consumidores, bolígrafos azules y negros.
    """,
    supuestos=[
        "Los bienes son completamente intercambiables",
        "La RMS es constante",
        "Las curvas de indiferencia son líneas rectas"
    ]
)
class SustitutosPerfectos(FuncionUtilidad):
    """
    Función de utilidad para sustitutos perfectos.

    U(x, y) = αx + βy

    Args:
        α: Ponderación del bien X (por defecto 1.0)
        β: Ponderación del bien Y (por defecto 1.0)
    """

    def __init__(self, α: float = 1.0, β: float = 1.0):
        super().__init__("Sustitutos Perfectos")
        self.α = validarPositivo(α, "α")
        self.β = validarPositivo(β, "β")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        return self.α * x + self.β * y

    def utilidadMarginalX(self, x: float, y: float) -> float:
        return self.α

    def utilidadMarginalY(self, x: float, y: float) -> float:
        return self.β

    def rms(self, x: float, y: float) -> float:
        """Para sustitutos perfectos, RMS es constante = α/β."""
        return self.α / self.β

    def graficar(self, restriccion: Optional['RestriccionPresupuestaria'] = None,
                 nivelesUtilidad: Optional[List[float]] = None,
                 mostrarOptimo: bool = True,
                 rangoX: Optional[Tuple[float, float]] = None,
                 rangoY: Optional[Tuple[float, float]] = None):
        """
        Grafica curvas de indiferencia lineales para sustitutos perfectos.

        Las curvas son líneas rectas con pendiente -α/β.
        """
        from ..utilidades.visuales import Lienzo, ROJO, AZUL, VERDE, AMARILLO

        lienzo = Lienzo()
        lienzo.configurarEtiquetas(etiquetaX="Bien X", etiquetaY="Bien Y",
                                  titulo=f"Preferencias: {self.nombre}")

        # Determinar rango
        if restriccion:
            xMax = restriccion.cantidadMaximaX()
            yMax = restriccion.cantidadMaximaY()
        else:
            xMax = rangoX[1] if rangoX else 50
            yMax = rangoY[1] if rangoY else 50

        xMin = rangoX[0] if rangoX else 0
        yMin = rangoY[0] if rangoY else 0

        # Graficar restricción presupuestaria - SIEMPRE EN ROJO
        if restriccion:
            # Sombrear la región FACTIBLE (por debajo de la restricción)
            lienzo.agregarRelleno(
                funcion1=lambda x: 0,  # Desde el eje X
                funcion2=lambda x: restriccion.cantidadYDadaX(x) if x <= xMax else 0,  # Hasta la restricción
                rangoX=(0, xMax),
                color=ROJO,
                alpha=0.1,
                etiqueta=None
            )

            # Luego la línea de restricción
            xRestr = np.array([0, xMax])
            yRestr = np.array([yMax, 0])
            lienzo.agregar((xRestr, yRestr), etiqueta="Restricción Presupuestaria", color=ROJO, anchoLinea=2)

        # Calcular punto óptimo si hay restricción
        xOpt, yOpt, uOpt = None, None, None
        if restriccion and mostrarOptimo:
            try:
                eleccion = EleccionOptima(self, restriccion)
                xOpt, yOpt, uOpt = eleccion.optimizar()
            except:
                pass

        # Graficar SOLO la curva de indiferencia óptima
        if nivelesUtilidad is None:
            if uOpt:
                nivelesUtilidad = [uOpt]
            else:
                # Sin restricción: graficar una curva de ejemplo
                nivelesUtilidad = [self.utilidad(xMax*0.5, yMax*0.5)]

        # Graficar líneas rectas - SIEMPRE EN AZUL
        # Para sustitutos perfectos: U = αx + βy => y = (U - αx) / β
        # Pendiente = -α/β
        for U in nivelesUtilidad:
            # Calcular los puntos extremos de la línea
            # Cuando x = 0: y = U/β
            y_cuando_x_0 = U / self.β

            # Cuando y = 0: x = U/α
            x_cuando_y_0 = U / self.α

            # Extender la línea más allá de los límites para que se vea completa
            # Crear línea desde (0, y_max_linea) hasta (x_max_linea, 0)
            x_linea = np.array([0, x_cuando_y_0])
            y_linea = np.array([y_cuando_x_0, 0])

            etiqueta = f"U = {U:.2f}"
            lienzo.agregar((x_linea, y_linea), etiqueta=etiqueta,
                         color=AZUL, estiloLinea='-', anchoLinea=2)

        # Punto óptimo - EN ROJO CON MARCADOR CUADRADO
        if xOpt is not None and yOpt is not None:
            lienzo.agregarPunto(xOpt, yOpt, etiqueta=f"Óptimo ({xOpt:.1f}, {yOpt:.1f})",
                              color=ROJO, dimension=5, marcador='s', mostrarLineasGuia=True)

        lienzo.configurarRango(rangoX=(xMin, xMax*1.1), rangoY=(yMin, yMax*1.1))
        return lienzo.graficar()

    def optimoAnalitico(self, restriccion: 'RestriccionPresupuestaria') -> Tuple[float, float, float]:
        """
        Calcula el óptimo analíticamente para sustitutos perfectos.

        Solución de esquina:
        - Si α/β > Px/Py: consumir solo X (y=0)
        - Si α/β < Px/Py: consumir solo Y (x=0)
        - Si α/β = Px/Py: cualquier combinación en la restricción

        Returns:
            Tupla (x*, y*, U*)
        """
        rms = self.α / self.β
        ratioPrecio = restriccion.Px / restriccion.Py

        if rms > ratioPrecio:
            # X es relativamente más valioso: consumir solo X
            xOpt = restriccion.cantidadMaximaX()
            yOpt = 0.0
        elif rms < ratioPrecio:
            # Y es relativamente más valioso: consumir solo Y
            xOpt = 0.0
            yOpt = restriccion.cantidadMaximaY()
        else:
            # Indiferente: elegir punto medio en la restricción
            xOpt = restriccion.cantidadMaximaX() / 2
            yOpt = restriccion.cantidadYDadaX(xOpt)

        uOpt = self.utilidad(xOpt, yOpt)
        return xOpt, yOpt, uOpt


@ayuda(
    descripcionEconomica="""
    Los complementarios perfectos son bienes que deben consumirse en proporciones
    fijas. El consumidor no obtiene utilidad adicional de tener más de uno sin
    aumentar el otro en la proporción adecuada.

    Ejemplos: Zapatos izquierdos y derechos, café y azúcar para algunos consumidores.
    """,
    supuestos=[
        "Los bienes deben consumirse en proporciones fijas",
        "Exceso de un bien no aumenta la utilidad",
        "Las curvas de indiferencia son en forma de L"
    ]
)
class ComplementariosPerfectos(FuncionUtilidad):
    """
    Función de utilidad para complementarios perfectos (Leontief).

    U(x, y) = min(αx, βy)

    Args:
        α: Proporción del bien X (por defecto 1.0)
        β: Proporción del bien Y (por defecto 1.0)
    """

    def __init__(self, α: float = 1.0, β: float = 1.0):
        super().__init__("Complementarios Perfectos (Leontief)")
        self.α = validarPositivo(α, "α")
        self.β = validarPositivo(β, "β")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        return min(self.α * x, self.β * y)

    def utilidadMarginalX(self, x: float, y: float) -> float:
        """La utilidad marginal depende de si x o y es el bien limitante."""
        if self.α * x < self.β * y:
            return self.α
        return 0

    def utilidadMarginalY(self, x: float, y: float) -> float:
        """La utilidad marginal depende de si x o y es el bien limitante."""
        if self.β * y < self.α * x:
            return self.β
        return 0

    def graficar(self, restriccion: Optional['RestriccionPresupuestaria'] = None,
                 nivelesUtilidad: Optional[List[float]] = None,
                 mostrarOptimo: bool = True,
                 rangoX: Optional[Tuple[float, float]] = None,
                 rangoY: Optional[Tuple[float, float]] = None):
        """
        Grafica curvas de indiferencia en forma de L para complementarios perfectos.

        Las curvas tienen esquinas (vértices) donde αx = βy.
        """
        from ..utilidades.visuales import Lienzo, ROJO, AZUL, VERDE, AMARILLO

        lienzo = Lienzo()
        lienzo.configurarEtiquetas(etiquetaX="Bien X", etiquetaY="Bien Y",
                                  titulo=f"Preferencias: {self.nombre}")

        # Determinar rango
        if restriccion:
            xMax = restriccion.cantidadMaximaX()
            yMax = restriccion.cantidadMaximaY()
        else:
            xMax = rangoX[1] if rangoX else 50
            yMax = rangoY[1] if rangoY else 50

        xMin = rangoX[0] if rangoX else 0
        yMin = rangoY[0] if rangoY else 0

        # Graficar restricción presupuestaria - SIEMPRE EN ROJO
        if restriccion:
            # Sombrear la región FACTIBLE (por debajo de la restricción)
            lienzo.agregarRelleno(
                funcion1=lambda x: 0,  # Desde el eje X
                funcion2=lambda x: restriccion.cantidadYDadaX(x) if x <= xMax else 0,  # Hasta la restricción
                rangoX=(0, xMax),
                color=ROJO,
                alpha=0.1,
                etiqueta=None
            )

            # Luego la línea de restricción
            xRestr = np.array([0, xMax])
            yRestr = np.array([yMax, 0])
            lienzo.agregar((xRestr, yRestr), etiqueta="Restricción Presupuestaria", color=ROJO, anchoLinea=2)

        # Calcular punto óptimo si hay restricción
        xOpt, yOpt, uOpt = None, None, None
        if restriccion and mostrarOptimo:
            try:
                eleccion = EleccionOptima(self, restriccion)
                xOpt, yOpt, uOpt = eleccion.optimizar()
            except:
                pass

        # Graficar SOLO la curva de indiferencia óptima
        if nivelesUtilidad is None:
            if uOpt:
                nivelesUtilidad = [uOpt]
            else:
                nivelesUtilidad = [min(xMax, yMax) * 0.5]

        # Graficar curva en L - SIEMPRE EN AZUL
        for U in nivelesUtilidad:
            # La esquina está en: αx = βy = U
            # Por lo tanto: x_esquina = U/α, y_esquina = U/β
            x_esquina = U / self.α
            y_esquina = U / self.β

            # Crear la curva en forma de L
            # Parte horizontal (desde x_esquina hasta xMax, y = y_esquina)
            x_horizontal = np.array([x_esquina, xMax * 1.2])
            y_horizontal = np.array([y_esquina, y_esquina])

            # Parte vertical (desde y_esquina hasta yMax, x = x_esquina)
            x_vertical = np.array([x_esquina, x_esquina])
            y_vertical = np.array([y_esquina, yMax * 1.2])

            etiqueta = f"U = {U:.2f}"

            # Graficar ambas partes
            lienzo.agregar((x_horizontal, y_horizontal), etiqueta=etiqueta,
                         color=AZUL, estiloLinea='-', anchoLinea=2)
            lienzo.agregar((x_vertical, y_vertical), color=AZUL, estiloLinea='-', anchoLinea=2)

        # Punto óptimo
        if xOpt and yOpt:
            lienzo.agregarPunto(xOpt, yOpt, etiqueta=f"Óptimo ({xOpt:.1f}, {yOpt:.1f})",
                              color=ROJO, dimension=5, mostrarLineasGuia=True)

        lienzo.configurarRango(rangoX=(xMin, xMax*1.1), rangoY=(yMin, yMax*1.1))
        return lienzo.graficar()


@ayuda(
    descripcionEconomica="""
    La función Cobb-Douglas es una de las más utilizadas en economía.
    Representa preferencias donde el consumidor gasta una proporción constante
    de su ingreso en cada bien, independientemente del precio.

    Cumple con las propiedades estándar de preferencias: monotonicidad,
    convexidad estricta y tasas marginales de sustitución decrecientes.
    """,
    supuestos=[
        "Utilidad marginal positiva y decreciente",
        "RMS decreciente (curvas de indiferencia convexas)",
        "Gasto proporcional constante en cada bien"
    ]
)
class CobbDouglas(FuncionUtilidad):
    """
    Función de utilidad Cobb-Douglas.

    U(x, y) = A · x^α · y^β

    Args:
        α: Exponente del bien X (por defecto 0.5)
        β: Exponente del bien Y (por defecto 0.5)
        A: Parámetro de tecnología/escala (por defecto 1.0)

    Ejemplo:
        >>> utilidad = CobbDouglas(α=0.6, β=0.4)
        >>> u = utilidad.utilidad(10, 15)
        >>> rms = utilidad.rms(10, 15)

        >>> # Con tecnología
        >>> utilidad2 = CobbDouglas(α=0.6, β=0.4, A=2.0)
    """

    def __init__(self, A: float = 1.0, α: float = 0.5, β: float = 0.5):
        super().__init__("Cobb-Douglas")
        self.α = validarPositivo(α, "α")
        self.β = validarPositivo(β, "β")
        self.A = validarPositivo(A, "A")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        if x <= 0 or y <= 0:
            return 0
        return self.A * (x ** self.α) * (y ** self.β)

    def utilidadMarginalX(self, x: float, y: float) -> float:
        if x <= 0 or y <= 0:
            return 0
        return self.A * self.α * (x ** (self.α - 1)) * (y ** self.β)

    def utilidadMarginalY(self, x: float, y: float) -> float:
        if x <= 0 or y <= 0:
            return 0
        return self.A * self.β * (x ** self.α) * (y ** (self.β - 1))

    def rms(self, x: float, y: float) -> float:
        if y <= 0:
            return np.inf
        return (self.α / self.β) * (y / x)


@ayuda(
    descripcionEconomica="""
    Las preferencias cuasilineales representan situaciones donde el consumidor
    tiene preferencias no lineales sobre un bien (X) pero lineales sobre el otro (Y).

    Esto implica que no hay efectos ingreso sobre el bien X, solo efectos sustitución.
    """,
    supuestos=[
        "Utilidad marginal del bien Y es constante",
        "No hay efecto ingreso sobre el bien X",
        "Curvas de indiferencia paralelas verticalmente"
    ]
)
class CuasiLineal(FuncionUtilidad):
    """
    Función de utilidad cuasilineal (cóncava tipo I).

    U(x, y) = α√x + y

    Args:
        α: Parámetro de ponderación (por defecto 1.0)
    """

    def __init__(self, α: float = 1.0):
        super().__init__("Cuasilineal")
        self.α = validarPositivo(α, "α")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        if x < 0 or y < 0:
            return -np.inf
        return self.α * np.sqrt(x) + y

    def utilidadMarginalX(self, x: float, y: float) -> float:
        if x <= 0:
            return np.inf
        return self.α / (2 * np.sqrt(x))

    def utilidadMarginalY(self, x: float, y: float) -> float:
        return 1.0


@ayuda(
    descripcionEconomica="""
    Función de utilidad con raíces cuadradas en ambos bienes.
    Representa preferencias simétricas con utilidades marginales decrecientes.
    """,
    supuestos=[
        "Utilidades marginales positivas y decrecientes",
        "Simetría en las preferencias",
        "RMS decreciente"
    ]
)
class ConcavaRaiz(FuncionUtilidad):
    """
    Función de utilidad cóncava con raíces.

    U(x, y) = √x + √y
    """

    def __init__(self):
        super().__init__("Cóncava con Raíz")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        if x < 0 or y < 0:
            return -np.inf
        return np.sqrt(x) + np.sqrt(y)

    def utilidadMarginalX(self, x: float, y: float) -> float:
        if x <= 0:
            return np.inf
        return 1 / (2 * np.sqrt(x))

    def utilidadMarginalY(self, x: float, y: float) -> float:
        if y <= 0:
            return np.inf
        return 1 / (2 * np.sqrt(y))


@ayuda(
    descripcionEconomica="""
    La función Stone-Geary es una generalización de Cobb-Douglas que incluye
    niveles de subsistencia o consumo mínimo requerido para cada bien.

    Solo se obtiene utilidad del consumo que excede estos niveles mínimos.
    """,
    supuestos=[
        "Existe un consumo mínimo de subsistencia para cada bien",
        "Solo el consumo que excede la subsistencia proporciona utilidad",
        "Preferencias tipo Cobb-Douglas sobre el consumo de lujo"
    ]
)
class StoneGeary(FuncionUtilidad):
    """
    Función de utilidad Stone-Geary.

    U(x, y) = (x - γx)^α · (y - γγ)^β

    donde γx, γγ son cantidades de subsistencia.

    Args:
        α: Exponente del bien X (por defecto 0.5)
        β: Exponente del bien Y (por defecto 0.5)
        γx: Cantidad de subsistencia de X (por defecto 0)
        γγ: Cantidad de subsistencia de Y (por defecto 0)
    """

    def __init__(self, α: float = 0.5, β: float = 0.5,
                 γx: float = 0, γγ: float = 0):
        super().__init__("Stone-Geary")
        self.α = validarPositivo(α, "α")
        self.β = validarPositivo(β, "β")
        self.γx = validarNoNegativo(γx, "γx")
        self.γγ = validarNoNegativo(γγ, "γγ")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        xAjustado = x - self.γx
        yAjustado = y - self.γγ
        if xAjustado <= 0 or yAjustado <= 0:
            return -np.inf
        return (xAjustado ** self.α) * (yAjustado ** self.β)

    def utilidadMarginalX(self, x: float, y: float) -> float:
        xAjustado = x - self.γx
        yAjustado = y - self.γγ
        if xAjustado <= 0 or yAjustado <= 0:
            return 0
        return self.α * (xAjustado ** (self.α - 1)) * (yAjustado ** self.β)

    def utilidadMarginalY(self, x: float, y: float) -> float:
        xAjustado = x - self.γx
        yAjustado = y - self.γγ
        if xAjustado <= 0 or yAjustado <= 0:
            return 0
        return self.β * (xAjustado ** self.α) * (yAjustado ** (self.β - 1))


@ayuda(
    descripcionEconomica="""
    Las preferencias saciadas representan la existencia de un punto de saciedad
    o "punto bienhechor" donde el consumidor alcanza su máxima utilidad.

    Más allá de este punto, consumir cantidades adicionales reduce la utilidad
    (el consumidor está sobresaturado).
    """,
    supuestos=[
        "Existe un punto de saciedad único",
        "La utilidad disminuye al alejarse del punto de saciedad",
        "Las curvas de indiferencia son círculos concéntricos"
    ]
)
class PreferenciasSaciadas(FuncionUtilidad):
    """
    Función de utilidad con punto de saciedad.

    U(x, y) = -(x - x*)² - (y - y*)²

    donde (x*, y*) es el punto de saciedad.

    Args:
        xÓptimo: Cantidad óptima del bien X (por defecto 5)
        yÓptimo: Cantidad óptima del bien Y (por defecto 5)
    """

    def __init__(self, xÓptimo: float = 5, yÓptimo: float = 5):
        super().__init__("Preferencias Saciadas")
        self.xÓptimo = validarPositivo(xÓptimo, "xÓptimo")
        self.yÓptimo = validarPositivo(yÓptimo, "yÓptimo")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        return -((x - self.xÓptimo) ** 2 + (y - self.yÓptimo) ** 2)

    def utilidadMarginalX(self, x: float, y: float) -> float:
        return -2 * (x - self.xÓptimo)

    def utilidadMarginalY(self, x: float, y: float) -> float:
        return -2 * (y - self.yÓptimo)

    def graficar(self, restriccion: Optional['RestriccionPresupuestaria'] = None,
                 nivelesUtilidad: Optional[List[float]] = None,
                 mostrarOptimo: bool = True,
                 rangoX: Optional[Tuple[float, float]] = None,
                 rangoY: Optional[Tuple[float, float]] = None):
        """
        Grafica curvas de indiferencia como círculos concéntricos para preferencias saciadas.

        Las curvas son círculos centrados en (xÓptimo, yÓptimo).
        """
        from ..utilidades.visuales import Lienzo, ROJO, AZUL, VERDE, AMARILLO

        lienzo = Lienzo()
        lienzo.configurarEtiquetas(etiquetaX="Bien X", etiquetaY="Bien Y",
                                  titulo=f"Preferencias: {self.nombre}")

        # Determinar rango
        if restriccion:
            xMax = restriccion.cantidadMaximaX()
            yMax = restriccion.cantidadMaximaY()
        else:
            xMax = rangoX[1] if rangoX else self.xÓptimo * 2.5
            yMax = rangoY[1] if rangoY else self.yÓptimo * 2.5

        xMin = rangoX[0] if rangoX else 0
        yMin = rangoY[0] if rangoY else 0

        # Graficar restricción presupuestaria - SIEMPRE EN ROJO
        if restriccion:
            # Sombrear la región FACTIBLE (por debajo de la restricción)
            lienzo.agregarRelleno(
                funcion1=lambda x: 0,  # Desde el eje X
                funcion2=lambda x: restriccion.cantidadYDadaX(x) if x <= xMax else 0,  # Hasta la restricción
                rangoX=(0, xMax),
                color=ROJO,
                alpha=0.1,
                etiqueta=None
            )

            # Luego la línea de restricción
            xRestr = np.array([0, xMax])
            yRestr = np.array([yMax, 0])
            lienzo.agregar((xRestr, yRestr), etiqueta="Restricción Presupuestaria", color=ROJO, anchoLinea=2)

        # Calcular punto óptimo si hay restricción
        xOpt, yOpt, uOpt = None, None, None
        if restriccion and mostrarOptimo:
            try:
                eleccion = EleccionOptima(self, restriccion)
                xOpt, yOpt, uOpt = eleccion.optimizar()
            except:
                pass

        # Graficar SOLO la curva de indiferencia óptima
        if nivelesUtilidad is None:
            if uOpt:
                nivelesUtilidad = [uOpt]
            else:
                # Sin restricción: círculo de radio 10 por defecto
                nivelesUtilidad = [-(10**2)]

        # Graficar círculo - SIEMPRE EN AZUL
        for U in nivelesUtilidad:
            # U = -(x - x*)² - (y - y*)²
            # => (x - x*)² + (y - y*)² = -U
            # => radio = sqrt(-U)
            if U >= 0:
                continue  # No hay curva para U >= 0

            radio = np.sqrt(-U)

            # Crear círculo paramétrico
            theta = np.linspace(0, 2*np.pi, 400)
            x_circulo = self.xÓptimo + radio * np.cos(theta)
            y_circulo = self.yÓptimo + radio * np.sin(theta)

            # Filtrar solo valores positivos
            mask = (x_circulo >= 0) & (y_circulo >= 0)
            x_circulo_filtrado = x_circulo[mask]
            y_circulo_filtrado = y_circulo[mask]

            etiqueta = f"U = {U:.2f}"

            if len(x_circulo_filtrado) > 0:
                lienzo.agregar((x_circulo_filtrado, y_circulo_filtrado), etiqueta=etiqueta,
                             color=AZUL, estiloLinea='-', anchoLinea=2)

        # Marcar el punto de saciedad
        lienzo.agregarPunto(self.xÓptimo, self.yÓptimo,
                          etiqueta=f"Saciedad ({self.xÓptimo}, {self.yÓptimo})",
                          color=AZUL, dimension=10, marcador='o', mostrarLineasGuia=False)

        # Punto óptimo (si hay restricción)
        if xOpt and yOpt:
            lienzo.agregarPunto(xOpt, yOpt, etiqueta=f"Óptimo ({xOpt:.1f}, {yOpt:.1f})",
                              color=ROJO, dimension=5, mostrarLineasGuia=False)

        lienzo.configurarRango(rangoX=(xMin, xMax*1.1), rangoY=(yMin, yMax*1.1))
        return lienzo.graficar()


@ayuda(
    descripcionEconomica="""
    La función CES (Constant Elasticity of Substitution) es una familia flexible
    de funciones de utilidad que incluye como casos especiales a Cobb-Douglas,
    sustitutos perfectos y complementarios perfectos.

    El parámetro ρ determina la elasticidad de sustitución entre los bienes.
    """,
    supuestos=[
        "Elasticidad de sustitución constante",
        "Incluye casos especiales según el valor de ρ",
        "Rendimientos constantes a escala"
    ]
)
class CES(FuncionUtilidad):
    """
    Función de utilidad de Elasticidad de Sustitución Constante (CES).

    U(x, y) = (αx^ρ + βy^ρ)^(1/ρ)

    donde ρ determina la elasticidad de sustitución:
    - ρ → 1: Sustitutos perfectos
    - ρ → 0: Cobb-Douglas
    - ρ → -∞: Complementarios perfectos

    Args:
        α: Ponderación del bien X (por defecto 1.0)
        β: Ponderación del bien Y (por defecto 1.0)
        ρ: Parámetro de sustitución (por defecto 0.5)
    """

    def __init__(self, α: float = 1.0, β: float = 1.0, ρ: float = 0.5):
        super().__init__("CES (Elasticidad de Sustitución Constante)")
        self.α = validarPositivo(α, "α")
        self.β = validarPositivo(β, "β")
        self.ρ = ρ
        # Si ρ ≈ 0, usar límite Cobb-Douglas
        self._usar_cobb_douglas = abs(ρ) < 1e-6

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        if x < 0 or y < 0:
            return -np.inf

        # Cuando ρ → 0, la CES converge a Cobb-Douglas: U = x^α * y^β
        if self._usar_cobb_douglas:
            if x <= 0 or y <= 0:
                return 0
            # Límite cuando ρ→0: (αx^ρ + βy^ρ)^(1/ρ) → x^α * y^β
            return (x ** self.α) * (y ** self.β)

        return (self.α * (x ** self.ρ) + self.β * (y ** self.ρ)) ** (1 / self.ρ)

    def utilidadMarginalX(self, x: float, y: float) -> float:
        if x <= 0 or y < 0:
            return 0

        # Caso Cobb-Douglas (ρ ≈ 0)
        if self._usar_cobb_douglas:
            if x <= 0 or y <= 0:
                return 0
            return self.α * (x ** (self.α - 1)) * (y ** self.β)

        base = self.α * (x ** self.ρ) + self.β * (y ** self.ρ)
        return self.α * (x ** (self.ρ - 1)) * (base ** ((1 - self.ρ) / self.ρ))

    def utilidadMarginalY(self, x: float, y: float) -> float:
        if y <= 0 or x < 0:
            return 0

        # Caso Cobb-Douglas (ρ ≈ 0)
        if self._usar_cobb_douglas:
            if x <= 0 or y <= 0:
                return 0
            return self.β * (x ** self.α) * (y ** (self.β - 1))

        base = self.α * (x ** self.ρ) + self.β * (y ** self.ρ)
        return self.β * (y ** (self.ρ - 1)) * (base ** ((1 - self.ρ) / self.ρ))


@ayuda(
    descripcionEconomica="""
    Un bien malo (o "bad") es aquel cuyo consumo reduce la utilidad del consumidor.
    A diferencia de los bienes normales, el consumidor prefiere tener menos de este bien.

    Ejemplos: Contaminación, ruido, tiempo de desplazamiento.
    """,
    supuestos=[
        "El bien Y reduce la utilidad",
        "El bien X es un bien normal",
        "La utilidad marginal de Y es negativa"
    ]
)
class BienMalo(FuncionUtilidad):
    """
    Función de utilidad con un bien malo.

    U(x, y) = x - y

    donde y es el bien malo que reduce la utilidad.
    """

    def __init__(self):
        super().__init__("Bien Malo")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        return x - y

    def utilidadMarginalX(self, x: float, y: float) -> float:
        return 1.0

    def utilidadMarginalY(self, x: float, y: float) -> float:
        return -1.0


@ayuda(
    descripcionEconomica="""
    Un bien neutral es aquel que no afecta la utilidad del consumidor.
    El consumidor es indiferente a tener más o menos de este bien.

    Las curvas de indiferencia son líneas verticales.
    """,
    supuestos=[
        "El bien Y no afecta la utilidad",
        "Solo el bien X proporciona utilidad",
        "La utilidad marginal de Y es cero"
    ]
)
class BienNeutral(FuncionUtilidad):
    """
    Función de utilidad con un bien neutral.

    U(x, y) = x

    donde y es el bien neutral que no afecta la utilidad.
    """

    def __init__(self):
        super().__init__("Bien Neutral")

    def utilidad(self, x: float, y: float) -> float:
        x = validarNoNegativo(x, "x")
        return x

    def utilidadMarginalX(self, x: float, y: float) -> float:
        return 1.0

    def utilidadMarginalY(self, x: float, y: float) -> float:
        return 0.0


@ayuda(
    descripcionEconomica="""
    La restricción presupuestaria representa todas las combinaciones de bienes
    que el consumidor puede adquirir con su ingreso dado los precios de mercado.

    La ecuación es: m = Pₓ·X + Pᵧ·Y

    donde Pₓ, Pᵧ son los precios y m es el ingreso.
    """,
    supuestos=[
        "El consumidor gasta todo su ingreso",
        "Los precios son dados (consumidor precio-aceptante)",
        "No hay ahorro ni endeudamiento"
    ]
)
class RestriccionPresupuestaria:
    """
    Representa la restricción presupuestaria del consumidor.

    m = Pₓ·X + Pᵧ·Y

    Args:
        m: Ingreso o presupuesto del consumidor
        Px: Precio del bien X
        Py: Precio del bien Y

    Ejemplo:
        >>> restriccion = RestriccionPresupuestaria(m=100, Px=2, Py=4)
        >>> asequible = restriccion.esAsequible(10, 15)
        >>> xMax = restriccion.cantidadMaximaX()
    """

    def __init__(self, m: float, Px: float, Py: float):
        self.m = validarPositivo(m, "m")
        self.Px = validarPositivo(Px, "Px")
        self.Py = validarPositivo(Py, "Py")

        # Mantener alias para compatibilidad (opcional)
        self.ingreso = self.m
        self.precioX = self.Px
        self.precioY = self.Py

    @explicacion("Verifica si una canasta es asequible dado el presupuesto")
    def esAsequible(self, x: float, y: float) -> bool:
        """
        Verifica si la canasta (x, y) es asequible.

        Returns:
            True si Pₓ·X + Pᵧ·Y ≤ m
        """
        x = validarNoNegativo(x, "x")
        y = validarNoNegativo(y, "y")
        return self.Px * x + self.Py * y <= self.m

    def cantidadMaximaY(self) -> float:
        """Cantidad máxima del bien Y si X = 0."""
        return self.m / self.Py

    def cantidadMaximaX(self) -> float:
        """Cantidad máxima del bien X si Y = 0."""
        return self.m / self.Px

    def pendiente(self) -> float:
        """Pendiente de la recta presupuestaria: -Pₓ/Pᵧ."""
        return -self.Px / self.Py

    def cantidadYDadaX(self, x: float) -> float:
        """
        Calcula Y dada la cantidad de X en la restricción presupuestaria.

        Resuelve: Y = (m - Pₓ·X) / Pᵧ
        """
        x = validarNoNegativo(x, "x")
        return (self.m - self.Px * x) / self.Py


@ayuda(
    descripcionEconomica="""
    La elección óptima del consumidor es la canasta que maximiza su utilidad
    sujeto a su restricción presupuestaria.

    Condiciones de optimalidad:
    1. Condición de tangencia: RMS = pₓ/pᵧ
    2. Restricción presupuestaria: pₓ·x + pᵧ·y = I

    Esto implica que el consumidor ajusta su consumo hasta que la tasa a la que
    está dispuesto a intercambiar bienes (RMS) iguala la tasa a la que puede
    intercambiarlos en el mercado (ratio de precios).
    """,
    supuestos=[
        "El consumidor maximiza utilidad",
        "Las preferencias son convexas",
        "Solución interior (consumo positivo de ambos bienes)"
    ]
)
class EleccionOptima:
    """
    Calcula la elección óptima del consumidor.

    Encuentra la canasta (x*, y*) que maximiza la utilidad
    sujeta a la restricción presupuestaria.

    Args:
        funcionUtilidad: Objeto de tipo FuncionUtilidad
        restriccion: Objeto RestriccionPresupuestaria

    Ejemplo:
        >>> utilidad = CobbDouglas(α=0.6, β=0.4)
        >>> restriccion = RestriccionPresupuestaria(m=100, Px=2, Py=4)
        >>> eleccion = EleccionOptima(utilidad, restriccion)
        >>> xOpt, yOpt, uOpt = eleccion.optimizar()
    """

    def __init__(self, funcionUtilidad: FuncionUtilidad,
                 restriccion: RestriccionPresupuestaria):
        self.funcionUtilidad = funcionUtilidad
        self.restriccion = restriccion

    @explicacion("""
    Encuentra la canasta óptima que maximiza la utilidad del consumidor
    sujeta a su restricción presupuestaria usando métodos numéricos.
    """)
    def optimizar(self) -> Tuple[float, float, float]:
        """
        Encuentra la canasta óptima que maximiza la utilidad.

        Returns:
            Tupla (x*, y*, U*) con las cantidades óptimas y la utilidad máxima

        Raises:
            ErrorEquilibrio: Si no se puede encontrar el óptimo
        """
        # Si la función tiene solución analítica, usarla
        if hasattr(self.funcionUtilidad, 'optimoAnalitico'):
            try:
                return self.funcionUtilidad.optimoAnalitico(self.restriccion)
            except:
                pass  # Si falla, continuar con método numérico

        # Función objetivo a minimizar (negativo de la utilidad)
        def objetivo(vars):
            x, y = vars
            if x < 0 or y < 0:
                return 1e10
            try:
                return -self.funcionUtilidad.utilidad(x, y)
            except:
                return 1e10

        # Restricción presupuestaria
        def restriccionEq(vars):
            x, y = vars
            return (self.restriccion.ingreso -
                    self.restriccion.precioX * x -
                    self.restriccion.precioY * y)

        # Punto inicial (en el medio de la restricción presupuestaria)
        x0 = self.restriccion.cantidadMaximaX() / 2
        y0 = self.restriccion.cantidadYDadaX(x0)

        # Restricciones
        constraints = {'type': 'eq', 'fun': restriccionEq}
        bounds = [(0, self.restriccion.cantidadMaximaX()),
                  (0, self.restriccion.cantidadMaximaY())]

        # Optimización
        resultado = minimize(objetivo, [x0, y0], method='SLSQP',
                           bounds=bounds, constraints=constraints)

        if resultado.success:
            xOpt, yOpt = resultado.x
            uOpt = self.funcionUtilidad.utilidad(xOpt, yOpt)
            return xOpt, yOpt, uOpt
        else:
            raise ErrorEquilibrio("No se pudo encontrar la elección óptima del consumidor")

    def verificarCondicionTangencia(self, x: float, y: float,
                                   tolerancia: float = 0.01) -> bool:
        """
        Verifica si se cumple la condición de tangencia en un punto.

        Condición: RMS = pₓ/pᵧ

        Args:
            x: Cantidad del bien X
            y: Cantidad del bien Y
            tolerancia: Tolerancia para la comparación

        Returns:
            True si se cumple la condición de tangencia
        """
        rms = self.funcionUtilidad.rms(x, y)
        ratioPrecios = self.restriccion.precioX / self.restriccion.precioY
        return abs(rms - ratioPrecios) < tolerancia


@ayuda(
    descripcionEconomica="""
    Las curvas de indiferencia representan todas las combinaciones de bienes
    que proporcionan el mismo nivel de utilidad al consumidor.

    Propiedades:
    - Pendiente negativa (más de un bien, menos del otro)
    - No se cruzan entre sí
    - Curvas más alejadas del origen representan mayor utilidad
    - Convexas al origen (en la mayoría de los casos)
    """,
    supuestos=[
        "Preferencias completas y transitivas",
        "Monotonicidad (más es mejor)",
        "Convexidad (en la mayoría de los casos)"
    ]
)
class CurvaIndiferencia:
    """
    Representa y calcula curvas de indiferencia para una función de utilidad.

    Args:
        funcionUtilidad: Objeto de tipo FuncionUtilidad

    Ejemplo:
        >>> utilidad = CobbDouglas(α=0.5, β=0.5)
        >>> curva = CurvaIndiferencia(utilidad)
        >>> yValores = curva.calcularCurva(nivelUtilidad=10, xValores=np.linspace(1, 20, 100))
    """

    def __init__(self, funcionUtilidad: FuncionUtilidad):
        self.funcionUtilidad = funcionUtilidad

    @explicacion("""
    Calcula los valores de y para una curva de indiferencia dada,
    resolviendo numéricamente U(x, y) = Ū para cada valor de x.
    """)
    def calcularCurva(self, nivelUtilidad: float,
                     xValores: np.ndarray) -> np.ndarray:
        """
        Calcula los valores de y para una curva de indiferencia dada.

        Args:
            nivelUtilidad: Nivel de utilidad de la curva (Ū)
            xValores: Valores de x para calcular

        Returns:
            Array con valores de y correspondientes
        """
        yValores = []
        for xVal in xValores:
            # Convertir x a float para evitar problemas con validadores
            x_float = float(xVal)

            # Buscar y tal que U(x, y) = nivelUtilidad
            def ecuacion(y_array):
                # fsolve pasa arrays, necesitamos convertir a float
                y_float = float(y_array[0]) if isinstance(y_array, np.ndarray) else float(y_array)
                try:
                    utilidad_calc = self.funcionUtilidad.utilidad(x_float, y_float)
                    return utilidad_calc - nivelUtilidad
                except:
                    return 1e10  # Valor alto si hay error

            # Intentar encontrar y
            try:
                # Mejorar valor inicial según el tipo de función
                if isinstance(self.funcionUtilidad, CobbDouglas):
                    # Para Cobb-Douglas: U = A * x^α * y^β => y = (U/(A*x^α))^(1/β)
                    A = self.funcionUtilidad.A
                    α = self.funcionUtilidad.α
                    β = self.funcionUtilidad.β
                    if x_float > 0 and nivelUtilidad > 0:
                        yInicial = ((nivelUtilidad / (A * (x_float ** α))) ** (1/β))
                    else:
                        yInicial = max(0.1, nivelUtilidad)
                else:
                    yInicial = max(0.1, nivelUtilidad)

                ySol = fsolve(ecuacion, [yInicial], full_output=False)[0]
                if ySol >= 0:
                    yValores.append(ySol)
                else:
                    yValores.append(np.nan)
            except:
                yValores.append(np.nan)

        return np.array(yValores)