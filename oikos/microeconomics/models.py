from sympy import symbols, diff, solve
from ..utils.parser import translatex

class EconomicFunction:
    def __init__(self, tex: str):
        # Definimos solo los símbolos base
        self.P, self.Q = symbols('P Q')
        
        # Convertimos el LaTeX
        self.expr = translatex(tex)

    def calculateElasticity(self, valueQuantity, valuePrice):
        # 1. Despejamos Q (obtenemos la expresión del lado derecho)
        solutions = solve(self.expr, self.Q)
        quantityExpr = solutions[0]
        
        # 2. Derivamos respecto a P
        derivativeP = diff(quantityExpr, self.P)
        
        # 3. Sustituimos el valor de P para obtener un número
        # Usamos float() directamente en el resultado de la sustitución
        derivValue = float(derivativeP.subs(self.P, valuePrice))
        
        # 4. Calculamos elasticidad: (dQ/dP) * (P/Q)
        elasticity = derivValue * (float(valuePrice) / float(valueQuantity))
        
        return elasticity

class Demand(EconomicFunction):
    def priceElasticity(self, valueQuantity, valuePrice):
        return self.calculateElasticity(valueQuantity, valuePrice)

    def getPriceInterpretation(self, valueQuantity, valuePrice):
        e = self.priceElasticity(valueQuantity, valuePrice)
        abs_e = abs(e)

        # Creo que el abs_e debe ir en la impresión
        if abs_e > 1: return f"Elastic ({e:.2f})"
        if abs_e < 1: return f"Inelastic ({e:.2f})"
        return f"Unitary ({e:.2f})"

class Supply(EconomicFunction):
    def priceElasticity(self, valueQuantity, valuePrice):
        return self.calculateElasticity(valueQuantity, valuePrice)