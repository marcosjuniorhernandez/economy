"""
Visualization module for microeconomic models.
"""

import matplotlib.pyplot as plt
import numpy as np


def marketGraph(supply, demand):
    """
    Graph supply, demand, and market equilibrium.
    
    Parameters
    ----------
    supply : Supply
        Supply curve
    demand : Demand
        Demand curve
    """
    from ..microeconomics.market import equilibrium
    
    # Calcular equilibrio
    equilibriumPrice, equilibriumQuantity = equilibrium(supply, demand)
    
    # Rango de precios para graficar
    maxPrice = (demand.a / demand.b) * 1.2
    prices = np.linspace(0, maxPrice, 100)
    
    # Calcular cantidades
    Q_oferta = [supply.quantity(P) for P in prices]
    Q_demanda = [demand.quantity(P) for P in prices]
    
    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(Q_oferta, prices, 'g-', label='Supply', linewidth=2)
    plt.plot(Q_demanda, prices, 'r-', label='Demand', linewidth=2)
    
    # Punto de equilibrio
    plt.plot(equilibriumQuantity, equilibriumPrice, 'ko', markersize=5, label=f'Equilirium (Q={equilibriumQuantity:.1f}, P={equilibriumPrice:.1f})')
    plt.axhline(equilibriumPrice, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(equilibriumQuantity, color='gray', linestyle='--', alpha=0.5)
    
    # Etiquetas
    plt.xlabel('Quantity (Q)', fontsize=12)
    plt.ylabel('Price (P)', fontsize=12)
    plt.title('Market equilibrium', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    plt.show()


def surplusGraph(supply, demand):
    """
    Consumer and producer surplus graph.
    
    Parameters
    ----------
    supply: Supply
        Supply curve
    demand: Demand
        Demand curve
    """
    from ..microeconomics.market import equilibrium
    
    # Equilibrio
    equilibriumPrice, equilibriumQuantity = equilibrium(supply, demand)
    
    # Rango de cantidades
    cantidades = np.linspace(0, equilibriumQuantity, 100)
    
    # Curvas inversas: P en función de Q
    demandPrice = [(demand.a - Q) / demand.b for Q in cantidades]
    supplyPrice = [(Q - supply.c) / supply.d for Q in cantidades]
    
    # Graficar
    plt.figure(figsize=(10, 6))
    plt.plot(cantidades, demandPrice, 'r-', label='Demand', linewidth=2)
    plt.plot(cantidades, supplyPrice, 'g-', label='Supply', linewidth=2)
    
    # Sombrear excedentes
    plt.fill_between(cantidades, equilibriumPrice, demandPrice, alpha=0.3, color='red', label='Consumer surplus')
    plt.fill_between(cantidades, supplyPrice, equilibriumPrice, alpha=0.3, color='green', label='Producer surplus')
    
    # Equilibrio
    plt.plot(equilibriumQuantity, equilibriumPrice, 'ko', markersize=5)
    plt.axhline(equilibriumPrice, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(equilibriumQuantity, color='gray', linestyle='--', alpha=0.5)
    
    # Etiquetas
    plt.xlabel('Quantity (Q)', fontsize=12)
    plt.ylabel('Price (P)', fontsize=12)
    plt.title('Consumer and Producer Surpluses', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    
    plt.tight_layout()
    plt.show()