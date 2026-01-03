from sympy import symbols, solve, diff
from ..utils.parser import translatex

class ISLM:
    """
    Representa el equilibrio general de corto plazo bajo el esquema Hicks-Hansen (IS-LM).
    Sector Real: Y = C + I + G
    Sector Monetario: M/P = L(Y, r)
    """
    def __init__(self):
        # Símbolos con notación económica estándar
        self.output = symbols('Y')               # Ingreso nacional / Producto
        self.interestRate = symbols('r')         # Tasa de interés real
        self.govermentSpending = symbols('G')    # Gasto público
        self.taxes = symbols('T')                # Impuestos netos
        self.moneySupply = symbols('M')          # Oferta monetaria nominal
        self.priceLevel = symbols('P')           # Nivel de precios

    def equilibrium(self, 
                                  consumptionFunction, 
                                  investmentFunction, 
                                  liquidityPreferenceFunction, 
                                  gValue, tValue, mValue, pValue):
        """
        Calcula el equilibrio macroeconómico simultáneo y los multiplicadores de política.
        """
        
        # 1. Parsing de las funciones de comportamiento
        C = translatex(consumptionFunction)
        I = translatex(investmentFunction)
        L = translatex(liquidityPreferenceFunction)

        # 2. Definición de las condiciones de equilibrio (Identidades)
        # IS: Y - C - I - G = 0
        goods_market_eq = self.output - C - I - self.govermentSpending
        # LM: L - M/P = 0
        money_market_eq = L - (self.moneySupply / self.priceLevel)

        # 3. Resolución del sistema en términos simbólicos primero
        # Resolvemos para Y y r manteniendo G, T, M, P como símbolos para poder derivar
        symbolic_solution = solve([goods_market_eq, money_market_eq], 
                                  (self.output, self.interestRate))
        
        y_star_expr = symbolic_solution[self.output]
        r_star_expr = symbolic_solution[self.interestRate]

        # 4. Cálculo de Multiplicadores (Derivadas de la solución de equilibrio)
        # Multiplicador del Gasto Público (dY/dG)
        fiscal_multiplier = diff(y_star_expr, self.govermentSpending)
        
        # Multiplicador de la Política Monetaria (dY/dM)
        monetary_multiplier = diff(y_star_expr, self.moneySupply)

        # 5. Sustitución de valores numéricos para el punto de equilibrio final
        values = {
            self.govermentSpending: gValue,
            self.taxes: tValue,
            self.moneySupply: mValue,
            self.priceLevel: pValue
        }
        
        y_final = float(y_star_expr.subs(values))
        r_final = float(r_star_expr.subs(values))
        gamma = float(fiscal_multiplier.subs(values))
        
        return {
            'Y^*': y_final,
            'r^*': r_final,
            'fiscal_multiplier': gamma,
            'monetary_multiplier': float(monetary_multiplier.subs(values))
        }