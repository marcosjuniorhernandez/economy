class Supply():
    """
    Linear supply:
    Q_s = c + dP
    """

    def __init__(self, intercepto: float, pendiente: float):
        self.c = intercepto
        self.d = pendiente

    def quantity(self, precio: float) -> float:
        """
        Retorna la cantidad ofrecida a un nivel de precios dado.
        """

        return self.c + self.d * precio
        
class Demand():
    """
    Linear demmand:
    Q_d = a - bP
    """

    def __init__(self, intercepto: float, pendiente: float):
        self.a = intercepto
        self.b = pendiente

    def quantity(self, precio: float) -> float:
        """
        Retorna la cantidad ofrecida a un nivel de precios dado.
        """

        return self.a - self.b * precio
        
def equilibrium(supply: Supply, demand: Demand) -> tuple[float, float]:
    """
    Calcula el equilibrio de mercado igualando:
    Q_s = Q_d
    """

    equilibriumPrice = (demand.a - supply.c) / (supply.d + demand.b)
    equilibriumQuantity = supply.quantity(equilibriumPrice)

    return equilibriumPrice, equilibriumQuantity