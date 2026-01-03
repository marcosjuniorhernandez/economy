from sympy import solve, latex, symbols
from IPython.display import display, Math

def equilibrium(supply, demand):
    """
    Calcula el punto de equilibrio asegurando resultados numéricos.
    """
    P, Q = symbols('P Q')
    
    # 1. Extraemos las expresiones. 
    # Aseguramos que SymPy vea: (Lado Izquierdo) - (Lado Derecho) = 0
    # Esto es vital para que devuelva números y no símbolos.
    equationOne = supply.expr
    equationTwo = demand.expr
    
    # 2. Resolvemos pidiendo explícitamente los valores de Q y P
    solutions = solve([equationOne, equationTwo], [Q, P], dict=True)
    
    if not solutions:
        return "There is no solution", "There is no solution"
    
    # 3. Extraemos el primer resultado del diccionario
    results = solutions[0]
    equilibriumQuantity = results[Q]
    equilibriumPrice = results[P]
    
    return equilibriumQuantity, equilibriumPrice