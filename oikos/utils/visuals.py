from IPython.display import display, Math
from sympy import latex

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