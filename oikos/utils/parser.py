from latex2sympy2 import latex2sympy

def translatex(strLatex: str):
    """
    Convierte un string de LaTeX en una expresión de SymPy.
    """
    try:
        # Reemplazamos '=' por '-' para que SymPy lo trate como expresión = 0
        if "=" in strLatex:
            parts = strLatex.split("=")
            return latex2sympy(f"{parts[0]} - ({parts[1]})")
        
        return latex2sympy(strLatex)
    
    except Exception as e:
        print(f"Error en el Parser: {e}")
        return None