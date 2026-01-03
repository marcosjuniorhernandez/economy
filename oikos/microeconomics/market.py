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
        
def show(res):
    """
    Muestra el resultado con formato matemático si está en un Notebook,
    o como texto limpio si está en una terminal.
    """
    valueQuantity = latex(res[0])
    valuePrice = latex(res[1])
    
    # 1. Creamos el string de LaTeX profesional
    # Usamos \\\\ para el salto de línea en Math() y \quad para espacio
    tex = rf"Q^{{*}} = {valueQuantity} \quad ; \quad P^{{*}} = {valuePrice}"
    
    # 2. Intentamos detectar si estamos en un entorno interactivo (Jupyter/Colab)
    try:
        # Si esto falla, es que no hay una interfaz gráfica para display
        from IPython import get_ipython
        if get_ipython() is not None:
            display(Math(tex))
        else:
            # Si es una terminal normal, usamos un print limpio
            print(f"Q* = {res[0]}, P* = {res[1]}")
    except:
        # Si algo falla con IPython, volvemos al print básico
        print(f"Q* = {res[0]}, P* = {res[1]}")