"""
Economía Internacional - Comercio y Ventajas Comparativas.

Este módulo implementa los principales modelos de comercio internacional:
- Modelo Ricardiano (ventaja absoluta y comparativa)
- Frontera de Posibilidades de Producción (FPP)
- Frontera de Posibilidades de Consumo (FPC)
- Términos de intercambio
- Modelo de Factores Específicos
- Modelo Heckscher-Ohlin
- Política comercial (aranceles, subsidios, cuotas)
"""

import numpy as np
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
from rich.console import Console
from rich.table import Table
from rich import box
from ..utilidades.decoradores import ayuda, explicacion
from ..utilidades.validadores import validarPositivo, validarNoNegativo
from ..nucleo.excepciones import ErrorValidacion


@dataclass
class BienEconomico:
    """Representa un bien económico con su nombre y unidad."""
    nombre: str
    unidad: str = "unidades"

    def __str__(self):
        return self.nombre


@ayuda(
    descripcionEconomica="""
    La Frontera de Posibilidades de Producción (FPP) muestra las combinaciones
    máximas de dos bienes que una economía puede producir con sus recursos
    disponibles y tecnología dada.

    La pendiente de la FPP representa el costo de oportunidad de producir
    un bien en términos del otro bien que se debe dejar de producir.
    """,
    supuestos=[
        "Recursos fijos y pleno empleo",
        "Tecnología constante",
        "Dos bienes producidos",
        "Eficiencia productiva"
    ]
)
class FPP:
    """
    Frontera de Posibilidades de Producción (FPP).

    Representa las combinaciones máximas de dos bienes que se pueden
    producir con los recursos disponibles.

    Args:
        bien1: Primer bien a producir
        bien2: Segundo bien a producir
        max_bien1: Producción máxima del bien 1 si se dedican todos los recursos
        max_bien2: Producción máxima del bien 2 si se dedican todos los recursos
        nombre_pais: Nombre del país o región

    Ejemplo:
        >>> tela = BienEconomico("Tela", "metros")
        >>> vino = BienEconomico("Vino", "litros")
        >>> fpp = FPP(tela, vino, 100, 50, "España")
        >>> co = fpp.costoOportunidad(bien=tela)
        >>> print(f"Costo de oportunidad de Tela: {co} litros de Vino")
    """

    def __init__(self,
                 bien1: BienEconomico,
                 bien2: BienEconomico,
                 max_bien1: float,
                 max_bien2: float,
                 nombre_pais: str = "País"):
        self.bien1 = bien1
        self.bien2 = bien2
        self.max_bien1 = validarPositivo(max_bien1, f"max_{bien1.nombre}")
        self.max_bien2 = validarPositivo(max_bien2, f"max_{bien2.nombre}")
        self.nombre_pais = nombre_pais

    def costoOportunidad(self, bien: BienEconomico) -> float:
        """
        Calcula el costo de oportunidad de producir una unidad del bien.

        El costo de oportunidad es cuánto del otro bien se debe sacrificar
        para producir una unidad adicional del bien especificado.

        Args:
            bien: Bien del cual calcular el costo de oportunidad

        Returns:
            Costo de oportunidad (unidades del otro bien)
        """
        if bien == self.bien1:
            # CO de bien1 = max_bien2 / max_bien1
            return self.max_bien2 / self.max_bien1
        elif bien == self.bien2:
            # CO de bien2 = max_bien1 / max_bien2
            return self.max_bien1 / self.max_bien2
        else:
            raise ErrorValidacion("bien", f"El bien {bien} no está en esta FPP")

    def produccionFactible(self, cantidad_bien1: float, cantidad_bien2: float) -> bool:
        """
        Verifica si una combinación de producción es factible.

        Args:
            cantidad_bien1: Cantidad a producir del bien 1
            cantidad_bien2: Cantidad a producir del bien 2

        Returns:
            True si la combinación está dentro de la FPP
        """
        cantidad_bien1 = validarNoNegativo(cantidad_bien1, self.bien1.nombre)
        cantidad_bien2 = validarNoNegativo(cantidad_bien2, self.bien2.nombre)

        # Para FPP lineal: (Q1/max_Q1) + (Q2/max_Q2) <= 1
        ratio = (cantidad_bien1 / self.max_bien1) + (cantidad_bien2 / self.max_bien2)
        return ratio <= 1.0

    def produccionBien2DadaBien1(self, cantidad_bien1: float) -> float:
        """
        Calcula la cantidad máxima del bien 2 que se puede producir
        dada una cantidad del bien 1.

        Args:
            cantidad_bien1: Cantidad producida del bien 1

        Returns:
            Cantidad máxima del bien 2
        """
        cantidad_bien1 = validarNoNegativo(cantidad_bien1, self.bien1.nombre)

        if cantidad_bien1 > self.max_bien1:
            return 0

        # Q2 = max_Q2 - (max_Q2/max_Q1) * Q1
        return self.max_bien2 - (self.max_bien2 / self.max_bien1) * cantidad_bien1

    def graficar(self, punto_produccion: Optional[Tuple[float, float]] = None,
                 color: Optional[str] = None, mostrar: bool = True):
        """
        Grafica la Frontera de Posibilidades de Producción.

        Args:
            punto_produccion: Tupla (bien1, bien2) con el punto de producción a marcar
            color: Color de la curva (si no se especifica, usa azul)
            mostrar: Si True, muestra el gráfico inmediatamente

        Returns:
            Figure de matplotlib

        Ejemplo:
            >>> fpp = FPP(tela, vino, 100, 50, "España")
            >>> fpp.graficar(punto_produccion=(50, 25))
        """
        import matplotlib.pyplot as plt

        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 7))

        # Generar puntos de la FPP (línea recta)
        bien1_valores = np.linspace(0, self.max_bien1, 100)
        bien2_valores = np.array([self.produccionBien2DadaBien1(q1) for q1 in bien1_valores])

        # Color
        color_fpp = color if color else '#0066FF'

        # Graficar la FPP
        ax.plot(bien1_valores, bien2_valores, color=color_fpp, linewidth=2.5, label=f'FPP {self.nombre_pais}')

        # Sombrear área factible
        ax.fill_between(bien1_valores, 0, bien2_valores, alpha=0.1, color=color_fpp)

        # Marcar los puntos extremos
        ax.plot([0, self.max_bien1], [self.max_bien2, 0], 'o', color=color_fpp, markersize=8)

        # Si hay punto de producción, graficarlo
        if punto_produccion:
            q1, q2 = punto_produccion
            ax.plot(q1, q2, 's', color='#FF0000', markersize=15, label=f'Producción ({q1}, {q2})')

            # Líneas punteadas al punto
            ax.plot([0, q1], [q2, q2], '--', color='gray', linewidth=1, alpha=0.5)
            ax.plot([q1, q1], [0, q2], '--', color='gray', linewidth=1, alpha=0.5)

        # Etiquetas y título
        ax.set_xlabel(f'{self.bien1.nombre} ({self.bien1.unidad})', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'{self.bien2.nombre} ({self.bien2.unidad})', fontsize=12, fontweight='bold')
        ax.set_title(f'Frontera de Posibilidades de Producción - {self.nombre_pais}',
                     fontsize=14, fontweight='bold')

        # Leyenda
        ax.legend(fontsize=10)

        # Grid
        ax.grid(True, alpha=0.3)

        # Ajustar límites
        ax.set_xlim(-self.max_bien1*0.05, self.max_bien1*1.1)
        ax.set_ylim(-self.max_bien2*0.05, self.max_bien2*1.1)

        plt.tight_layout()

        if mostrar:
            plt.show()

        return fig

    def __repr__(self):
        return (f"FPP({self.nombre_pais}): "
                f"{self.bien1.nombre}={self.max_bien1}, "
                f"{self.bien2.nombre}={self.max_bien2}")


@ayuda(
    descripcionEconomica="""
    El Modelo Ricardiano de comercio internacional se basa en las diferencias
    en la productividad del trabajo entre países. Demuestra que incluso si un
    país tiene ventaja absoluta en todos los bienes, aún puede beneficiarse
    del comercio basándose en la ventaja comparativa.

    La ventaja comparativa se determina por el costo de oportunidad relativo:
    un país debe especializarse en producir el bien en el que tiene el menor
    costo de oportunidad.
    """,
    supuestos=[
        "Un solo factor de producción: trabajo",
        "Trabajo homogéneo dentro de cada país",
        "Movilidad perfecta del trabajo dentro del país",
        "Inmovilidad del trabajo entre países",
        "Tecnología constante (coeficientes técnicos fijos)",
        "Competencia perfecta"
    ]
)
class Ricardiano:
    """
    Modelo Ricardiano de comercio internacional.

    Analiza el comercio basado en ventajas comparativas derivadas de
    diferencias en productividad del trabajo.

    Args:
        pais1: Nombre del primer país
        pais2: Nombre del segundo país
        bien1: Primer bien
        bien2: Segundo bien
        fpp1: Frontera de Posibilidades de Producción del país 1
        fpp2: Frontera de Posibilidades de Producción del país 2

    Ejemplo:
        >>> tela = BienEconomico("Tela", "metros")
        >>> vino = BienEconomico("Vino", "litros")
        >>>
        >>> fpp_esp = FPP(tela, vino, 100, 50, "España")
        >>> fpp_col = FPP(tela, vino, 80, 120, "Colombia")
        >>>
        >>> modelo = Ricardiano("España", "Colombia", tela, vino, fpp_esp, fpp_col)
        >>> modelo.analizar()
    """

    def __init__(self,
                 pais1: str,
                 pais2: str,
                 bien1: BienEconomico,
                 bien2: BienEconomico,
                 fpp1: FPP,
                 fpp2: FPP):
        self.pais1 = pais1
        self.pais2 = pais2
        self.bien1 = bien1
        self.bien2 = bien2
        self.fpp1 = fpp1
        self.fpp2 = fpp2

        # Estado del modelo
        self.produccion_sin_comercio: Dict = {}
        self.produccion_con_comercio: Dict = {}
        self.comercio: Dict = {}
        self.consumo_con_comercio: Dict = {}

    @explicacion("""
    Determina qué país tiene ventaja absoluta en cada bien.
    Ventaja absoluta: capacidad de producir más de un bien con los mismos recursos.
    """)
    def ventajaAbsoluta(self) -> Dict[str, str]:
        """
        Determina qué país tiene ventaja absoluta en cada bien.

        Returns:
            Diccionario con el país que tiene ventaja absoluta en cada bien
        """
        ventaja = {}

        # Bien 1
        if self.fpp1.max_bien1 > self.fpp2.max_bien1:
            ventaja[self.bien1.nombre] = self.pais1
        elif self.fpp2.max_bien1 > self.fpp1.max_bien1:
            ventaja[self.bien1.nombre] = self.pais2
        else:
            ventaja[self.bien1.nombre] = "Empate"

        # Bien 2
        if self.fpp1.max_bien2 > self.fpp2.max_bien2:
            ventaja[self.bien2.nombre] = self.pais1
        elif self.fpp2.max_bien2 > self.fpp1.max_bien2:
            ventaja[self.bien2.nombre] = self.pais2
        else:
            ventaja[self.bien2.nombre] = "Empate"

        return ventaja

    @explicacion("""
    Determina qué país tiene ventaja comparativa en cada bien.
    Ventaja comparativa: capacidad de producir un bien con menor costo de oportunidad.
    """)
    def ventajaComparativa(self) -> Dict[str, str]:
        """
        Determina qué país tiene ventaja comparativa en cada bien.

        La ventaja comparativa se determina por el costo de oportunidad:
        el país con menor costo de oportunidad tiene ventaja comparativa.

        Returns:
            Diccionario con el país que tiene ventaja comparativa en cada bien
        """
        ventaja = {}

        # Costo de oportunidad del bien 1 en cada país
        co_bien1_pais1 = self.fpp1.costoOportunidad(self.bien1)
        co_bien1_pais2 = self.fpp2.costoOportunidad(self.bien1)

        # Costo de oportunidad del bien 2 en cada país
        co_bien2_pais1 = self.fpp1.costoOportunidad(self.bien2)
        co_bien2_pais2 = self.fpp2.costoOportunidad(self.bien2)

        # Ventaja comparativa en bien 1
        if co_bien1_pais1 < co_bien1_pais2:
            ventaja[self.bien1.nombre] = self.pais1
        else:
            ventaja[self.bien1.nombre] = self.pais2

        # Ventaja comparativa en bien 2
        if co_bien2_pais1 < co_bien2_pais2:
            ventaja[self.bien2.nombre] = self.pais1
        else:
            ventaja[self.bien2.nombre] = self.pais2

        return ventaja

    @explicacion("""
    Calcula los términos de intercambio mutuamente beneficiosos.
    Los términos de intercambio deben estar entre los costos de oportunidad
    de ambos países para que el comercio sea beneficioso para ambos.
    """)
    def terminosIntercambio(self) -> Dict[str, Tuple[float, float]]:
        """
        Calcula el rango de términos de intercambio mutuamente beneficiosos.

        Los términos de intercambio indican cuánto de un bien se intercambia
        por una unidad del otro bien. Para que el comercio sea mutuamente
        beneficioso, deben estar entre los costos de oportunidad de ambos países.

        Returns:
            Diccionario con rangos de términos de intercambio para cada bien
        """
        co_bien1_pais1 = self.fpp1.costoOportunidad(self.bien1)
        co_bien1_pais2 = self.fpp2.costoOportunidad(self.bien1)

        co_bien2_pais1 = self.fpp1.costoOportunidad(self.bien2)
        co_bien2_pais2 = self.fpp2.costoOportunidad(self.bien2)

        return {
            self.bien1.nombre: (min(co_bien1_pais1, co_bien1_pais2),
                               max(co_bien1_pais1, co_bien1_pais2)),
            self.bien2.nombre: (min(co_bien2_pais1, co_bien2_pais2),
                               max(co_bien2_pais1, co_bien2_pais2))
        }

    def establecerProduccionSinComercio(self,
                                        pais1_bien1: float,
                                        pais1_bien2: float,
                                        pais2_bien1: float,
                                        pais2_bien2: float):
        """
        Establece la producción y consumo de cada país en autarquía (sin comercio).

        En autarquía, producción = consumo.

        Args:
            pais1_bien1: Producción/consumo del bien 1 en país 1
            pais1_bien2: Producción/consumo del bien 2 en país 1
            pais2_bien1: Producción/consumo del bien 1 en país 2
            pais2_bien2: Producción/consumo del bien 2 en país 2
        """
        # Validar que sean factibles
        if not self.fpp1.produccionFactible(pais1_bien1, pais1_bien2):
            raise ErrorValidacion(
                "producción",
                f"La producción de {self.pais1} no es factible según su FPP"
            )

        if not self.fpp2.produccionFactible(pais2_bien1, pais2_bien2):
            raise ErrorValidacion(
                "producción",
                f"La producción de {self.pais2} no es factible según su FPP"
            )

        self.produccion_sin_comercio = {
            self.pais1: {
                self.bien1.nombre: pais1_bien1,
                self.bien2.nombre: pais1_bien2
            },
            self.pais2: {
                self.bien1.nombre: pais2_bien1,
                self.bien2.nombre: pais2_bien2
            }
        }

    def establecerEspecializacionCompleta(self):
        """
        Establece la producción con especialización completa según ventaja comparativa.

        Cada país se especializa completamente en el bien en el que tiene
        ventaja comparativa.
        """
        ventaja = self.ventajaComparativa()

        self.produccion_con_comercio = {
            self.pais1: {
                self.bien1.nombre: 0,
                self.bien2.nombre: 0
            },
            self.pais2: {
                self.bien1.nombre: 0,
                self.bien2.nombre: 0
            }
        }

        # País 1 se especializa en su bien con ventaja comparativa
        if ventaja[self.bien1.nombre] == self.pais1:
            self.produccion_con_comercio[self.pais1][self.bien1.nombre] = self.fpp1.max_bien1
        else:
            self.produccion_con_comercio[self.pais1][self.bien2.nombre] = self.fpp1.max_bien2

        # País 2 se especializa en su bien con ventaja comparativa
        if ventaja[self.bien1.nombre] == self.pais2:
            self.produccion_con_comercio[self.pais2][self.bien1.nombre] = self.fpp2.max_bien1
        else:
            self.produccion_con_comercio[self.pais2][self.bien2.nombre] = self.fpp2.max_bien2

    def establecerComercio(self,
                          exportador: str,
                          bien_exportado: BienEconomico,
                          cantidad_exportada: float):
        """
        Establece el patrón de comercio entre los países.

        Args:
            exportador: País que exporta
            bien_exportado: Bien que se exporta
            cantidad_exportada: Cantidad exportada
        """
        cantidad_exportada = validarPositivo(cantidad_exportada, "cantidad_exportada")

        importador = self.pais2 if exportador == self.pais1 else self.pais1

        # Determinar el bien importado (el otro bien)
        bien_importado = self.bien2 if bien_exportado == self.bien1 else self.bien1

        # Los términos de intercambio deben estar especificados
        # Por simplicidad, usaremos el punto medio del rango
        terminos = self.terminosIntercambio()
        rango = terminos[bien_exportado.nombre]
        precio_relativo = (rango[0] + rango[1]) / 2

        cantidad_importada = cantidad_exportada * precio_relativo

        self.comercio = {
            exportador: {
                "exporta": {bien_exportado.nombre: cantidad_exportada},
                "importa": {bien_importado.nombre: cantidad_importada}
            },
            importador: {
                "exporta": {bien_importado.nombre: cantidad_importada},
                "importa": {bien_exportado.nombre: cantidad_exportada}
            }
        }

        # Calcular consumo = producción + importaciones - exportaciones
        self.consumo_con_comercio = {
            self.pais1: {},
            self.pais2: {}
        }

        for pais in [self.pais1, self.pais2]:
            for bien in [self.bien1.nombre, self.bien2.nombre]:
                produccion = self.produccion_con_comercio.get(pais, {}).get(bien, 0)
                importado = self.comercio.get(pais, {}).get("importa", {}).get(bien, 0)
                exportado = self.comercio.get(pais, {}).get("exporta", {}).get(bien, 0)

                self.consumo_con_comercio[pais][bien] = produccion + importado - exportado

    def gananciaComercio(self) -> Dict[str, Dict[str, float]]:
        """
        Calcula las ganancias del comercio para cada país.

        Ganancias del comercio = Consumo con comercio - Consumo sin comercio

        Returns:
            Diccionario con las ganancias de cada país en cada bien
        """
        if not self.produccion_sin_comercio or not self.consumo_con_comercio:
            raise ErrorValidacion(
                "modelo",
                "Debe establecer producción sin comercio y con comercio primero"
            )

        ganancias = {}

        for pais in [self.pais1, self.pais2]:
            ganancias[pais] = {}
            for bien in [self.bien1.nombre, self.bien2.nombre]:
                sin_comercio = self.produccion_sin_comercio[pais][bien]
                con_comercio = self.consumo_con_comercio[pais][bien]
                ganancias[pais][bien] = con_comercio - sin_comercio

        return ganancias

    def mostrarAnalisis(self):
        """
        Muestra un análisis completo del modelo usando tablas Rich.

        Incluye:
        - Costos de oportunidad
        - Ventajas absolutas y comparativas
        - Términos de intercambio
        - Producción sin y con comercio
        - Comercio
        - Consumo con comercio
        - Ganancias del comercio
        """
        console = Console()

        # Tabla 1: Costos de Oportunidad
        tabla_co = Table(
            title=f"[bold cyan]Costos de Oportunidad[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )

        tabla_co.add_column("País", style="cyan", justify="left")
        tabla_co.add_column(f"CO de {self.bien1.nombre}\n(en {self.bien2.unidad} de {self.bien2.nombre})",
                           justify="center")
        tabla_co.add_column(f"CO de {self.bien2.nombre}\n(en {self.bien1.unidad} de {self.bien1.nombre})",
                           justify="center")

        co1_bien1 = self.fpp1.costoOportunidad(self.bien1)
        co1_bien2 = self.fpp1.costoOportunidad(self.bien2)
        co2_bien1 = self.fpp2.costoOportunidad(self.bien1)
        co2_bien2 = self.fpp2.costoOportunidad(self.bien2)

        tabla_co.add_row(self.pais1, f"{co1_bien1:.2f}", f"{co1_bien2:.2f}")
        tabla_co.add_row(self.pais2, f"{co2_bien1:.2f}", f"{co2_bien2:.2f}")

        console.print(tabla_co)
        console.print()

        # Tabla 2: Ventajas
        tabla_ventajas = Table(
            title=f"[bold cyan]Ventajas Absolutas y Comparativas[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta"
        )

        tabla_ventajas.add_column("Bien", style="cyan")
        tabla_ventajas.add_column("Ventaja Absoluta", justify="center")
        tabla_ventajas.add_column("Ventaja Comparativa", justify="center", style="bold green")

        va = self.ventajaAbsoluta()
        vc = self.ventajaComparativa()

        tabla_ventajas.add_row(self.bien1.nombre, va[self.bien1.nombre],
                              f"[bold]{vc[self.bien1.nombre]}[/bold]")
        tabla_ventajas.add_row(self.bien2.nombre, va[self.bien2.nombre],
                              f"[bold]{vc[self.bien2.nombre]}[/bold]")

        console.print(tabla_ventajas)
        console.print()

        # Tabla 3: Producción, Comercio y Consumo (si están disponibles)
        if self.produccion_sin_comercio and self.consumo_con_comercio:
            tabla_completa = Table(
                title=f"[bold cyan]Análisis Completo del Comercio[/bold cyan]",
                box=box.DOUBLE_EDGE,
                show_header=True,
                header_style="bold magenta"
            )

            tabla_completa.add_column("", style="bold yellow", justify="left")
            tabla_completa.add_column(f"{self.pais1}\n{self.bien1.nombre}", justify="center")
            tabla_completa.add_column(f"{self.pais1}\n{self.bien2.nombre}", justify="center")
            tabla_completa.add_column(f"{self.pais2}\n{self.bien1.nombre}", justify="center")
            tabla_completa.add_column(f"{self.pais2}\n{self.bien2.nombre}", justify="center")

            # Fila separadora
            tabla_completa.add_row(
                "[bold]SIN COMERCIO (Autarquía)[/bold]",
                "", "", "", "",
                style="dim"
            )

            # Consumo y producción (son iguales en autarquía)
            tabla_completa.add_row(
                "  Consumo y Producción",
                f"{self.produccion_sin_comercio[self.pais1][self.bien1.nombre]:.1f}",
                f"{self.produccion_sin_comercio[self.pais1][self.bien2.nombre]:.1f}",
                f"{self.produccion_sin_comercio[self.pais2][self.bien1.nombre]:.1f}",
                f"{self.produccion_sin_comercio[self.pais2][self.bien2.nombre]:.1f}"
            )

            # Separador
            tabla_completa.add_row("", "", "", "", "")
            tabla_completa.add_row(
                "[bold]CON COMERCIO[/bold]",
                "", "", "", "",
                style="dim"
            )

            # Producción con comercio
            tabla_completa.add_row(
                "  Producción",
                f"{self.produccion_con_comercio[self.pais1][self.bien1.nombre]:.1f}",
                f"{self.produccion_con_comercio[self.pais1][self.bien2.nombre]:.1f}",
                f"{self.produccion_con_comercio[self.pais2][self.bien1.nombre]:.1f}",
                f"{self.produccion_con_comercio[self.pais2][self.bien2.nombre]:.1f}"
            )

            # Comercio (exportaciones como negativo, importaciones como positivo)
            exp1_b1 = -self.comercio.get(self.pais1, {}).get("exporta", {}).get(self.bien1.nombre, 0)
            imp1_b1 = self.comercio.get(self.pais1, {}).get("importa", {}).get(self.bien1.nombre, 0)
            comercio1_b1 = exp1_b1 + imp1_b1

            exp1_b2 = -self.comercio.get(self.pais1, {}).get("exporta", {}).get(self.bien2.nombre, 0)
            imp1_b2 = self.comercio.get(self.pais1, {}).get("importa", {}).get(self.bien2.nombre, 0)
            comercio1_b2 = exp1_b2 + imp1_b2

            exp2_b1 = -self.comercio.get(self.pais2, {}).get("exporta", {}).get(self.bien1.nombre, 0)
            imp2_b1 = self.comercio.get(self.pais2, {}).get("importa", {}).get(self.bien1.nombre, 0)
            comercio2_b1 = exp2_b1 + imp2_b1

            exp2_b2 = -self.comercio.get(self.pais2, {}).get("exporta", {}).get(self.bien2.nombre, 0)
            imp2_b2 = self.comercio.get(self.pais2, {}).get("importa", {}).get(self.bien2.nombre, 0)
            comercio2_b2 = exp2_b2 + imp2_b2

            def formato_comercio(valor):
                if valor > 0:
                    return f"[green]+{valor:.1f}[/green]"
                elif valor < 0:
                    return f"[red]{valor:.1f}[/red]"
                else:
                    return "0.0"

            tabla_completa.add_row(
                "  Comercio (+ imp, - exp)",
                formato_comercio(comercio1_b1),
                formato_comercio(comercio1_b2),
                formato_comercio(comercio2_b1),
                formato_comercio(comercio2_b2)
            )

            # Consumo con comercio
            tabla_completa.add_row(
                "  Consumo",
                f"[bold]{self.consumo_con_comercio[self.pais1][self.bien1.nombre]:.1f}[/bold]",
                f"[bold]{self.consumo_con_comercio[self.pais1][self.bien2.nombre]:.1f}[/bold]",
                f"[bold]{self.consumo_con_comercio[self.pais2][self.bien1.nombre]:.1f}[/bold]",
                f"[bold]{self.consumo_con_comercio[self.pais2][self.bien2.nombre]:.1f}[/bold]"
            )

            # Separador
            tabla_completa.add_row("", "", "", "", "")

            # Ganancias del comercio
            ganancias = self.gananciaComercio()

            def formato_ganancia(valor):
                if valor > 0:
                    return f"[bold green]+{valor:.1f}[/bold green]"
                elif valor < 0:
                    return f"[bold red]{valor:.1f}[/bold red]"
                else:
                    return "0.0"

            tabla_completa.add_row(
                "[bold]GANANCIAS DEL COMERCIO[/bold]",
                formato_ganancia(ganancias[self.pais1][self.bien1.nombre]),
                formato_ganancia(ganancias[self.pais1][self.bien2.nombre]),
                formato_ganancia(ganancias[self.pais2][self.bien1.nombre]),
                formato_ganancia(ganancias[self.pais2][self.bien2.nombre]),
                style="bold"
            )

            console.print(tabla_completa)
            console.print()

        # Mostrar interpretación
        console.print("[bold yellow]Interpretación:[/bold yellow]")
        vc = self.ventajaComparativa()

        # Determinar en qué bien tiene ventaja comparativa cada país
        bien_vc_pais1 = self.bien1.nombre if vc[self.bien1.nombre] == self.pais1 else self.bien2.nombre
        bien_vc_pais2 = self.bien1.nombre if vc[self.bien1.nombre] == self.pais2 else self.bien2.nombre

        console.print(f"• {self.pais1} tiene ventaja comparativa en [bold green]{bien_vc_pais1}[/bold green]")
        console.print(f"• {self.pais2} tiene ventaja comparativa en [bold green]{bien_vc_pais2}[/bold green]")

        if self.consumo_con_comercio:
            console.print(f"\n[bold green]>>> Ambos países se benefician del comercio[/bold green]")

    def graficarFPPs(self, mostrar: bool = True):
        """
        Grafica las FPPs de ambos países en el mismo gráfico.

        Args:
            mostrar: Si True, muestra el gráfico inmediatamente

        Returns:
            Figure de matplotlib

        Ejemplo:
            >>> modelo = Ricardiano("España", "Colombia", tela, vino, fpp_esp, fpp_col)
            >>> modelo.graficarFPPs()
        """
        import matplotlib.pyplot as plt

        # Crear figura
        fig, ax = plt.subplots(figsize=(10, 7))

        # Graficar FPP del país 1
        bien1_valores_p1 = np.linspace(0, self.fpp1.max_bien1, 100)
        bien2_valores_p1 = np.array([self.fpp1.produccionBien2DadaBien1(q1) for q1 in bien1_valores_p1])
        ax.plot(bien1_valores_p1, bien2_valores_p1, color='#0066FF', linewidth=2.5, label=f'FPP {self.pais1}')

        # Graficar FPP del país 2
        bien1_valores_p2 = np.linspace(0, self.fpp2.max_bien1, 100)
        bien2_valores_p2 = np.array([self.fpp2.produccionBien2DadaBien1(q1) for q1 in bien1_valores_p2])
        ax.plot(bien1_valores_p2, bien2_valores_p2, color='#FF0000', linewidth=2.5, label=f'FPP {self.pais2}')

        # Marcar puntos sin comercio si están definidos
        if self.produccion_sin_comercio:
            p1_b1 = self.produccion_sin_comercio[self.pais1][self.bien1.nombre]
            p1_b2 = self.produccion_sin_comercio[self.pais1][self.bien2.nombre]
            ax.plot(p1_b1, p1_b2, 'o', color='#0066FF', markersize=10, label=f'{self.pais1} (autarquía)')

            p2_b1 = self.produccion_sin_comercio[self.pais2][self.bien1.nombre]
            p2_b2 = self.produccion_sin_comercio[self.pais2][self.bien2.nombre]
            ax.plot(p2_b1, p2_b2, 'o', color='#FF0000', markersize=10, label=f'{self.pais2} (autarquía)')

        # Marcar puntos con especialización si están definidos
        if self.produccion_con_comercio:
            p1_b1 = self.produccion_con_comercio[self.pais1][self.bien1.nombre]
            p1_b2 = self.produccion_con_comercio[self.pais1][self.bien2.nombre]
            ax.plot(p1_b1, p1_b2, '*', color='#0066FF', markersize=15, label=f'{self.pais1} (especialización)')

            p2_b1 = self.produccion_con_comercio[self.pais2][self.bien1.nombre]
            p2_b2 = self.produccion_con_comercio[self.pais2][self.bien2.nombre]
            ax.plot(p2_b1, p2_b2, '*', color='#FF0000', markersize=15, label=f'{self.pais2} (especialización)')

        # Etiquetas y título
        ax.set_xlabel(f'{self.bien1.nombre} ({self.bien1.unidad})', fontsize=12, fontweight='bold')
        ax.set_ylabel(f'{self.bien2.nombre} ({self.bien2.unidad})', fontsize=12, fontweight='bold')
        ax.set_title('Fronteras de Posibilidades de Producción', fontsize=14, fontweight='bold')

        # Leyenda
        ax.legend(fontsize=10)

        # Grid
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if mostrar:
            plt.show()

        return fig

    def graficarComercio(self, mostrar: bool = True):
        """
        Grafica las FPPs con los puntos de consumo antes y después del comercio.

        Args:
            mostrar: Si True, muestra el gráfico inmediatamente

        Returns:
            Lienzo con el gráfico

        Ejemplo:
            >>> modelo.establecerProduccionSinComercio(50, 25, 40, 60)
            >>> modelo.establecerEspecializacionCompleta()
            >>> modelo.establecerComercio("España", tela, 40)
            >>> modelo.graficarComercio()
        """
        from ..utilidades.visuales import Lienzo, AZUL, ROJO, VERDE, NARANJA

        # Crear matriz 1x2 para comparar ambos países
        lienzo = Lienzo(
            matriz=(1, 2),
            dimensionMatriz=(16, 7)
        )

        # ===== PAÍS 1 =====
        lienzo.seccion(0, 0)
        lienzo.titulo(f"{self.pais1}")
        lienzo.ejes(
            ejeX=f"{self.bien1.nombre} ({self.bien1.unidad})",
            ejeY=f"{self.bien2.nombre} ({self.bien2.unidad})"
        )

        # FPP del país 1
        bien1_valores_p1 = np.linspace(0, self.fpp1.max_bien1, 100)
        bien2_valores_p1 = [self.fpp1.produccionBien2DadaBien1(q1) for q1 in bien1_valores_p1]
        lienzo.agregar(
            bien1_valores_p1,
            bien2_valores_p1,
            etiqueta=f"FPP",
            color=AZUL,
            grosor=2.5
        )

        # Punto sin comercio
        if self.produccion_sin_comercio:
            p1_b1_sc = self.produccion_sin_comercio[self.pais1][self.bien1.nombre]
            p1_b2_sc = self.produccion_sin_comercio[self.pais1][self.bien2.nombre]
            lienzo.punto(p1_b1_sc, p1_b2_sc, color=NARANJA, tamaño=120, marcador='o',
                        etiqueta=f"Sin comercio")

        # Punto con especialización
        if self.produccion_con_comercio:
            p1_b1_prod = self.produccion_con_comercio[self.pais1][self.bien1.nombre]
            p1_b2_prod = self.produccion_con_comercio[self.pais1][self.bien2.nombre]
            lienzo.punto(p1_b1_prod, p1_b2_prod, color=ROJO, tamaño=120, marcador='s',
                        etiqueta=f"Producción")

        # Punto de consumo con comercio
        if self.consumo_con_comercio:
            p1_b1_cons = self.consumo_con_comercio[self.pais1][self.bien1.nombre]
            p1_b2_cons = self.consumo_con_comercio[self.pais1][self.bien2.nombre]
            lienzo.punto(p1_b1_cons, p1_b2_cons, color=VERDE, tamaño=140, marcador='*',
                        etiqueta=f"Consumo con comercio")

            # Línea de comercio (del punto de producción al punto de consumo)
            lienzo.agregar(
                [p1_b1_prod, p1_b1_cons],
                [p1_b2_prod, p1_b2_cons],
                color='purple',
                estilo='--',
                grosor=2,
                alpha=0.7,
                etiqueta="Comercio"
            )

        # ===== PAÍS 2 =====
        lienzo.seccion(0, 1)
        lienzo.titulo(f"{self.pais2}")
        lienzo.ejes(
            ejeX=f"{self.bien1.nombre} ({self.bien1.unidad})",
            ejeY=f"{self.bien2.nombre} ({self.bien2.unidad})"
        )

        # FPP del país 2
        bien1_valores_p2 = np.linspace(0, self.fpp2.max_bien1, 100)
        bien2_valores_p2 = [self.fpp2.produccionBien2DadaBien1(q1) for q1 in bien1_valores_p2]
        lienzo.agregar(
            bien1_valores_p2,
            bien2_valores_p2,
            etiqueta=f"FPP",
            color=AZUL,
            grosor=2.5
        )

        # Punto sin comercio
        if self.produccion_sin_comercio:
            p2_b1_sc = self.produccion_sin_comercio[self.pais2][self.bien1.nombre]
            p2_b2_sc = self.produccion_sin_comercio[self.pais2][self.bien2.nombre]
            lienzo.punto(p2_b1_sc, p2_b2_sc, color=NARANJA, tamaño=120, marcador='o',
                        etiqueta=f"Sin comercio")

        # Punto con especialización
        if self.produccion_con_comercio:
            p2_b1_prod = self.produccion_con_comercio[self.pais2][self.bien1.nombre]
            p2_b2_prod = self.produccion_con_comercio[self.pais2][self.bien2.nombre]
            lienzo.punto(p2_b1_prod, p2_b2_prod, color=ROJO, tamaño=120, marcador='s',
                        etiqueta=f"Producción")

        # Punto de consumo con comercio
        if self.consumo_con_comercio:
            p2_b1_cons = self.consumo_con_comercio[self.pais2][self.bien1.nombre]
            p2_b2_cons = self.consumo_con_comercio[self.pais2][self.bien2.nombre]
            lienzo.punto(p2_b1_cons, p2_b2_cons, color=VERDE, tamaño=140, marcador='*',
                        etiqueta=f"Consumo con comercio")

            # Línea de comercio
            lienzo.agregar(
                [p2_b1_prod, p2_b1_cons],
                [p2_b2_prod, p2_b2_cons],
                color='purple',
                estilo='--',
                grosor=2,
                alpha=0.7,
                etiqueta="Comercio"
            )

        if mostrar:
            lienzo.mostrar()

        return lienzo


@ayuda(
    descripcionEconomica="""
    El Modelo de Factores Específicos (también llamado modelo Ricardo-Viner)
    analiza el comercio cuando algunos factores de producción son específicos
    a ciertas industrias y no pueden moverse entre sectores.

    Este modelo es útil para analizar los efectos redistributivos del comercio
    en el corto plazo, cuando el capital es específico de cada sector pero el
    trabajo es móvil entre sectores.
    """,
    supuestos=[
        "Tres factores: trabajo (móvil), capital específico sector 1, capital específico sector 2",
        "Dos sectores productivos",
        "Rendimientos decrecientes a escala",
        "Competencia perfecta",
        "Movilidad perfecta del trabajo entre sectores",
        "Inmovilidad del capital entre sectores (corto plazo)"
    ]
)
class FactoresEspecificos:
    """
    Modelo de Factores Específicos para comercio internacional.

    Analiza cómo la apertura comercial afecta a diferentes factores de
    producción cuando algunos factores son específicos de ciertos sectores.

    Args:
        nombre_pais: Nombre del país
        sector1: Nombre del primer sector
        sector2: Nombre del segundo sector
        trabajo_total: Cantidad total de trabajo disponible
        capital1: Capital específico del sector 1
        capital2: Capital específico del sector 2

    Ejemplo:
        >>> modelo = FactoresEspecificos(
        ...     "Portugal",
        ...     "Manufacturas",
        ...     "Alimentos",
        ...     trabajo_total=100,
        ...     capital1=50,
        ...     capital2=30
        ... )
    """

    def __init__(self,
                 nombre_pais: str,
                 sector1: str,
                 sector2: str,
                 trabajo_total: float,
                 capital1: float,
                 capital2: float):
        self.nombre_pais = nombre_pais
        self.sector1 = sector1
        self.sector2 = sector2
        self.L = validarPositivo(trabajo_total, "trabajo_total")
        self.K1 = validarPositivo(capital1, "capital1")
        self.K2 = validarPositivo(capital2, "capital2")

        # Asignación de trabajo en equilibrio
        self.L1 = None  # Trabajo en sector 1
        self.L2 = None  # Trabajo en sector 2

    def asignarTrabajo(self, trabajo_sector1: float):
        """
        Asigna el trabajo entre los dos sectores.

        Args:
            trabajo_sector1: Cantidad de trabajo asignada al sector 1
        """
        trabajo_sector1 = validarNoNegativo(trabajo_sector1, "trabajo_sector1")

        if trabajo_sector1 > self.L:
            raise ErrorValidacion(
                "trabajo",
                f"No hay suficiente trabajo disponible. Total: {self.L}"
            )

        self.L1 = trabajo_sector1
        self.L2 = self.L - trabajo_sector1

    def produccion(self, alpha: float = 0.5) -> Tuple[float, float]:
        """
        Calcula la producción de cada sector usando función Cobb-Douglas.

        Q_i = K_i^α * L_i^(1-α)

        Args:
            alpha: Parámetro de participación del capital (0 < α < 1)

        Returns:
            Tupla (producción_sector1, producción_sector2)
        """
        if self.L1 is None or self.L2 is None:
            raise ErrorValidacion(
                "modelo",
                "Debe asignar el trabajo primero usando asignarTrabajo()"
            )

        Q1 = (self.K1 ** alpha) * (self.L1 ** (1 - alpha))
        Q2 = (self.K2 ** alpha) * (self.L2 ** (1 - alpha))

        return Q1, Q2

    def __repr__(self):
        return (f"FactoresEspecificos({self.nombre_pais}: "
                f"{self.sector1}, {self.sector2})")


# TODO: Implementar modelos adicionales
# - Modelo Heckscher-Ohlin completo
# - Aranceles y política comercial
# - Cuotas de importación
# - Subsidios a las exportaciones
# - Dumping y medidas antidumping
# - Efectos de bienestar de la política comercial
