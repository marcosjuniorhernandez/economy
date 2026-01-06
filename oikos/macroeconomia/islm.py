"""
Modelo IS-LM - Equilibrio de corto plazo en economía cerrada.

El modelo IS-LM (Inversión-Ahorro / Liquidez-Dinero) analiza
el equilibrio simultáneo del mercado de bienes y del mercado monetario.
"""

from sympy import symbols, solve, diff
from typing import Dict, Optional
from ..nucleo.base import ModeloEconomico
from ..nucleo.excepciones import ErrorEquilibrio
from ..utilidades.parseador import translatex
from ..utilidades.decoradores import ayuda, explicacion


@ayuda(
    descripcion_economica="""
    El modelo IS-LM representa el equilibrio macroeconómico de corto plazo
    en una economía cerrada. Combina:
    
    - Curva IS: Equilibrio en el mercado de bienes (Y = C + I + G)
    - Curva LM: Equilibrio en el mercado de dinero (M/P = L(Y, r))
    
    El modelo permite analizar los efectos de políticas fiscales y monetarias
    sobre el producto (Y) y la tasa de interés (r).
    """,
    supuestos=[
        "Economía cerrada (sin sector externo)",
        "Precios fijos en el corto plazo",
        "Desempleo (economía por debajo del pleno empleo)",
        "Tasa de interés flexible",
        "Expectativas estáticas"
    ],
    cursos=[
        "Macroeconomía Intermedia",
        "Teoría Macroeconómica",
        "Política Económica"
    ]
)
class ISLM(ModeloEconomico):
    """
    Modelo IS-LM de equilibrio macroeconómico.
    
    Analiza el equilibrio simultáneo de:
    - Mercado de bienes (IS)
    - Mercado de dinero (LM)
    
    Ejemplo:
        >>> modelo = ISLM()
        >>> resultados = modelo.equilibrio(
        ...     consumo="C = 200 + 0.8(Y - T)",
        ...     inversion="I = 1000 - 50r",
        ...     demandaDinero="L = 0.25Y - 50r",
        ...     gastoPublico=900,
        ...     impuestos=800,
        ...     ofertaMonetaria=3400,
        ...     nivelPrecios=1
        ... )
        >>> escribir(resultados, "Equilibrio IS-LM")
    """
    
    def __init__(self):
        """Inicializa el modelo IS-LM."""
        super().__init__()
        
        # Definir símbolos económicos
        self.Y = symbols('Y')      # Producto/Ingreso
        self.r = symbols('r')      # Tasa de interés
        self.C = symbols('C')      # Consumo
        self.I = symbols('I')      # Inversión
        self.G = symbols('G')      # Gasto público
        self.T = symbols('T')      # Impuestos
        self.M = symbols('M')      # Oferta monetaria
        self.P = symbols('P')      # Nivel de precios
        self.L = symbols('L')      # Demanda de dinero
    
    @explicacion("""
    Calcula el equilibrio macroeconómico resolviendo simultáneamente
    las ecuaciones IS y LM. También calcula los multiplicadores de política.
    """)
    def equilibrio(self,
                  consumo: str,
                  inversion: str,
                  demandaDinero: str,
                  gastoPublico: float,
                  impuestos: float,
                  ofertaMonetaria: float,
                  nivelPrecios: float = 1.0) -> Dict[str, float]:
        """
        Calcula el equilibrio IS-LM.
        
        Args:
            consumo: Función de consumo en LaTeX
                    Ejemplo: "C = 200 + 0.8(Y - T)"
            inversion: Función de inversión en LaTeX
                      Ejemplo: "I = 1000 - 50r"
            demandaDinero: Demanda de dinero en LaTeX
                          Ejemplo: "L = 0.25Y - 50r"
            gastoPublico: Gasto del gobierno (G)
            impuestos: Impuestos netos (T)
            ofertaMonetaria: Oferta monetaria nominal (M)
            nivelPrecios: Nivel de precios (P), default=1
            
        Returns:
            Diccionario con:
                - 'Y*': Producto de equilibrio
                - 'r*': Tasa de interés de equilibrio
                - 'multiplicador_fiscal': ∂Y/∂G
                - 'multiplicador_monetario': ∂Y/∂M
                - 'C*': Consumo de equilibrio
                - 'I*': Inversión de equilibrio
                
        Raises:
            ErrorEquilibrio: Si no se puede resolver el sistema
        """
        # 1. Parsear las funciones de comportamiento
        C_expr = translatex(consumo)
        I_expr = translatex(inversion)
        L_expr = translatex(demandaDinero)
        
        # 2. Definir condiciones de equilibrio
        # IS: Y = C + I + G
        ecuacionIS = self.Y - C_expr - I_expr - self.G
        
        # LM: M/P = L(Y, r)
        ecuacionLM = L_expr - (self.M / self.P)
        
        # 3. Resolver sistema simbólicamente (para multiplicadores)
        try:
            solucion_simbolica = solve(
                [ecuacionIS, ecuacionLM],
                (self.Y, self.r)
            )
        except Exception as e:
            raise ErrorEquilibrio(f"No se pudo resolver el sistema IS-LM: {str(e)}")
        
        if not solucion_simbolica:
            raise ErrorEquilibrio("No existe equilibrio IS-LM para estos parámetros")
        
        Y_estrella_expr = solucion_simbolica[self.Y]
        r_estrella_expr = solucion_simbolica[self.r]
        
        # 4. Calcular multiplicadores
        multiplicadorFiscal = diff(Y_estrella_expr, self.G)
        multiplicadorMonetario = diff(Y_estrella_expr, self.M)
        
        # 5. Sustituir valores numéricos
        valores = {
            self.G: gastoPublico,
            self.T: impuestos,
            self.M: ofertaMonetaria,
            self.P: nivelPrecios
        }
        
        Y_equilibrio = float(Y_estrella_expr.subs(valores))
        r_equilibrio = float(r_estrella_expr.subs(valores))
        
        # 6. Calcular C* e I* de equilibrio
        C_equilibrio = float(C_expr.subs({**valores, self.Y: Y_equilibrio, self.r: r_equilibrio}))
        I_equilibrio = float(I_expr.subs({**valores, self.Y: Y_equilibrio, self.r: r_equilibrio}))
        
        return {
            'Y*': Y_equilibrio,
            'r*': r_equilibrio,
            'k': float(multiplicadorFiscal.subs(valores)),
            'm': float(multiplicadorMonetario.subs(valores)),
            'C*': C_equilibrio,
            'I*': I_equilibrio
        }
    
    def resolver(self) -> Dict[str, float]:
        """Implementación del método abstracto."""
        # Este método requiere parámetros, usar equilibrio() directamente
        raise NotImplementedError("Usa el método equilibrio() con los parámetros requeridos")
    
    def explicar(self) -> str:
        """Explicación del modelo IS-LM."""
        return """
        El modelo IS-LM muestra cómo se determina el ingreso (Y) y la tasa de interés (r)
        en el corto plazo cuando los precios son rígidos.
        
        - La curva IS representa combinaciones de (Y, r) donde el mercado de bienes está en equilibrio
        - La curva LM representa combinaciones de (Y, r) donde el mercado de dinero está en equilibrio
        - El equilibrio ocurre donde se cruzan ambas curvas
        
        Política Fiscal Expansiva (↑G):
            → IS se desplaza a la derecha
            → ↑Y, ↑r
            → Puede causar "efecto expulsión" de la inversión privada
        
        Política Monetaria Expansiva (↑M):
            → LM se desplaza a la derecha
            → ↑Y, ↓r
            → Estimula inversión privada
        """