# Definimos una versión de tu librería
__version__ = "0.1.0"

# Microeconomía
from .microeconomics import Demand, Supply
from .microeconomics import equilibrium

# Macroeconomía
from .macroeconomics import ISLM
from .microeconomics import equilibrium

# Traemos herramientas útiles
from .utils.parser import translatex
from .utils.visuals import write