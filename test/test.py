from oikos.microeconomics.market import *
from oikos.graphs.microeconomics import *

oferta = Supply(intercepto=10, pendiente=2)
demanda = Demand(intercepto=100, pendiente=3)

# Gráfica simple
fig, ax = marketGraph(oferta, demanda)

# Gráfica con excedentes
fig, ax, surplus = surplusGraph(oferta, demanda)
print(f"Excedente del consumidor: {surplus['consumer_surplus']}")