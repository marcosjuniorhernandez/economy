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
    - Curva LM: Equilibrio en el mercado de dinero (M/P = L(Y, i))
    
    El modelo permite analizar los efectos de políticas fiscales y monetarias
    sobre el producto (Y) y la tasa de interés (i).
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
        ...     consumo="C = 100 + 0.8(Y - T)",
        ...     inversion="I = 300 - 20r",
        ...     demandaDinero="L = 0.2Y - 10r",
        ...     gastoPublico=200,
        ...     impuestos=150,
        ...     ofertaMonetaria=200,
        ...     nivelPrecios=1
        ... )
        >>> escribir(resultados, "Equilibrio IS-LM")
    """
    
    def __init__(self):
        """Inicializa el modelo IS-LM."""
        super().__init__()
        
        # Definir símbolos económicos
        self.Y = symbols('Y')      # Producto/Ingreso
        self.i = symbols('i')      # Tasa de interés
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
                - 'i*': Tasa de interés de equilibrio
                - 'multiplicador_fiscal': ∂Y/∂G
                - 'multiplicador_monetario': ∂Y/∂M
                - 'C*': Consumo de equilibrio
                - 'I*': Inversión de equilibrio
                
        Raises:
            ErrorEquilibrio: Si no se puede resolver el sistema
        """
        # 1. Parsear las funciones de comportamiento
        C_eq = translatex(consumo)
        I_eq = translatex(inversion)
        L_eq = translatex(demandaDinero)

        # Extraer lado derecho de las ecuaciones (rhs = right hand side)
        C_expr = C_eq.rhs if hasattr(C_eq, 'rhs') else C_eq
        I_expr = I_eq.rhs if hasattr(I_eq, 'rhs') else I_eq
        L_expr = L_eq.rhs if hasattr(L_eq, 'rhs') else L_eq

        # Sustituir notaciones alternativas de tasa de interés por 'i'
        # Esto permite que el usuario use 'r', 'rho', 'rate', etc.
        for expr in [C_expr, I_expr, L_expr]:
            simbolos = expr.free_symbols
            for s in simbolos:
                nombre = str(s)
                # Si encuentra 'r', 'rho', 'rate' o similar, lo sustituye por 'i'
                if nombre.lower() in ['r', 'rho', 'rate']:
                    if s == symbols('r'):
                        C_expr = C_expr.subs(s, self.i)
                        I_expr = I_expr.subs(s, self.i)
                        L_expr = L_expr.subs(s, self.i)

        # 2. Definir condiciones de equilibrio
        # IS: Y = C + I + G
        ecuacionIS = self.Y - C_expr - I_expr - self.G

        # LM: M/P = L(Y, i)
        ecuacionLM = L_expr - (self.M / self.P)
        
        # 3. Resolver sistema simbólicamente (para multiplicadores)
        try:
            solucion_simbolica = solve(
                [ecuacionIS, ecuacionLM],
                (self.Y, self.i)
            )
        except Exception as e:
            raise ErrorEquilibrio(f"No se pudo resolver el sistema IS-LM: {str(e)}")
        
        if not solucion_simbolica:
            raise ErrorEquilibrio("No existe equilibrio IS-LM para estos parámetros")
        
        Y_estrella_expr = solucion_simbolica[self.Y]
        i_estrella_expr = solucion_simbolica[self.i]
        
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
        i_equilibrio = float(i_estrella_expr.subs(valores))
        
        # 6. Calcular C* e I* de equilibrio
        C_equilibrio = float(C_expr.subs({**valores, self.Y: Y_equilibrio, self.i: i_equilibrio}))
        I_equilibrio = float(I_expr.subs({**valores, self.Y: Y_equilibrio, self.i: i_equilibrio}))
        
        return {
            'Y*': Y_equilibrio,
            'r*': i_equilibrio,
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
        El modelo IS-LM muestra cómo se determina el ingreso (Y) y la tasa de interés (i)
        en el corto plazo cuando los precios son rígidos.
        
        - La curva IS representa combinaciones de (Y, i) donde el mercado de bienes está en equilibrio
        - La curva LM representa combinaciones de (Y, i) donde el mercado de dinero está en equilibrio
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