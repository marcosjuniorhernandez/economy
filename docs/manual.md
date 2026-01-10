# Manual Completo de OIKOS v0.3.1
---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Guía Rápida](#guía-rápida)
4. [Microeconomía](#microeconomía)
   - [Consumidor](#consumidor)
   - [Demanda](#demanda)
   - [Oferta](#oferta)
   - [Equilibrio de Mercado](#equilibrio-de-mercado)
   - [Excedentes](#excedentes)
   - [Elasticidades](#elasticidades)
5. [Macroeconomía](#macroeconomía)
   - [Modelo IS-LM](#modelo-is-lm)
   - [Política Fiscal](#política-fiscal)
   - [Política Monetaria](#política-monetaria)
   - [Multiplicadores](#multiplicadores)
6. [Comercio Internacional](#comercio-internacional)
   - [Frontera de Posibilidades de Producción (FPP)](#frontera-de-posibilidades-de-producción-fpp)
   - [Modelo Ricardiano](#modelo-ricardiano)
   - [Ventaja Absoluta vs Comparativa](#ventaja-absoluta-vs-comparativa)
   - [Términos de Intercambio](#términos-de-intercambio)
   - [Modelo de Factores Específicos](#modelo-de-factores-específicos)
7. [Visualización](#visualización)
   - [Lienzo Simple](#lienzo-simple)
   - [Lienzo Matricial](#lienzo-matricial)
   - [Estilos Personalizados](#estilos-personalizados)
   - [Rellenos y Sombreado](#rellenos-y-sombreado)
8. [Utilidades](#utilidades)
   - [Parseador LaTeX](#parseador-latex)
   - [Validadores](#validadores)
   - [Decoradores](#decoradores)
9. [Ejemplos Avanzados](#ejemplos-avanzados)
10. [FAQ](#faq)
11. [Referencia de API](#referencia-de-api)

---

## Introducción

**OIKOS** es una librería académica diseñada para enseñar y entender teoría económica mediante código Python.

### ¿Por qué OIKOS?

- ✅ **Sintaxis económica**: El código se lee como economía, no como matemática
- ✅ **Parser LaTeX**: Escribe ecuaciones tal como las escribirías en papel
- ✅ **Gráficos profesionales**: Visualizaciones listas para presentaciones
- ✅ **Documentación en español**: Pensado para estudiantes hispanohablantes
- ✅ **Sistema de ayuda**: Cada función explica su teoría económica

### Filosofía de diseño

OIKOS está diseñado para **economistas que programan**, no para programadores que hacen economía.

**Ejemplo comparativo:**

```python
# ❌ Forma matemática tradicional (numpy/scipy)
import numpy as np
from scipy.optimize import fsolve

def sistema(vars):
    Q, P = vars
    demanda = Q - (100 - 2*P)
    oferta = Q - (-20 + 3*P)
    return [demanda, oferta]

Q, P = fsolve(sistema, [50, 20])
print(f"Q={Q}, P={P}")

# ✅ Forma económica con OIKOS
from oikos import Demanda, Oferta, equilibrio

demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")
eq = equilibrio(oferta, demanda)
print(eq)  # {'P*': 24.0, 'Q*': 52.0}
```

La diferencia es clara: **OIKOS habla tu idioma** (economía).

---

## Instalación

### Requisitos

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación vía pip

```bash
pip install oikos
```

### Instalación desde el código fuente

```bash
git clone https://github.com/marcosjuniorhernandez/economy.git
cd oikos
pip install -e .
```

### Dependencias

OIKOS instala automáticamente:
- `sympy` (álgebra simbólica)
- `latex2sympy2` (parser LaTeX)
- `matplotlib` (gráficos)
- `numpy` (cálculos numéricos)

---

## Guía Rápida

### Tu primer programa con OIKOS

```python
# Importar las clases principales
from oikos import Demanda, Oferta, equilibrio
from oikos.utilidades import Lienzo, ROJO, VERDE2, AZUL

# 1. Crear funciones de demanda y oferta
demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")

# 2. Calcular el equilibrio
eq = equilibrio(oferta, demanda)
print(eq)  # {'P*': 24.0, 'Q*': 52.0}

# 3. Graficar el mercado
lienzo = Lienzo()
lienzo.configurarEtiquetas(
    etiquetaX="Cantidad (Q)",
    etiquetaY="Precio (P)",
    titulo="Mi Primer Mercado"
)
lienzo.agregar(demanda, color=ROJO)
lienzo.agregar(oferta, color=VERDE2)
lienzo.agregarPunto(eq['Q*'], eq['P*'], color=AZUL, dimension=10)
lienzo.graficar()
```

**¡Eso es todo!** Con 15 líneas de código ya tienes un análisis de mercado completo.

---

## Microeconomía

### Consumidor

La clase `Consumidor` representa un agente económico que toma decisiones de consumo para maximizar su utilidad sujeto a una restricción presupuestaria.

#### Teoría del consumidor

**Función de Utilidad**: Representa las preferencias del consumidor sobre distintas canastas de bienes.

**Restricción Presupuestaria**: Limita las opciones del consumidor según su ingreso y los precios de los bienes.
```
p₁·x₁ + p₂·x₂ = m
```

**Maximización de Utilidad**: El consumidor elige la canasta que maximiza su utilidad sujeto a su restricción presupuestaria.

#### Creación básica

```python
from oikos import Consumidor

# Crear consumidor con función de utilidad Cobb-Douglas
consumidor = Consumidor(
    utilidad="U = x^0.5 * y^0.5",
    ingreso=100,
    precio_bien1=2,
    precio_bien2=5
)

# Obtener la demanda óptima
demanda_optima = consumidor.demandarOptima()
print(demanda_optima)
# {'x': 25.0, 'y': 10.0, 'U': 15.81}

# Verificar cuánto gasta
gasto_total = demanda_optima['x'] * 2 + demanda_optima['y'] * 5
print(f"Gasto total: ${gasto_total:.2f}")  # $100.00
```

#### Métodos principales

**`demandarOptima()`**: Encuentra la canasta óptima que maximiza la utilidad

```python
consumidor = Consumidor(
    utilidad="U = x^0.6 * y^0.4",
    ingreso=120,
    precio_bien1=3,
    precio_bien2=2
)

canasta = consumidor.demandarOptima()
print(f"Consumir {canasta['x']:.2f} unidades del bien X")
print(f"Consumir {canasta['y']:.2f} unidades del bien Y")
print(f"Utilidad alcanzada: U = {canasta['U']:.2f}")
```

**`utilidadAlcanzada(x, y)`**: Calcula la utilidad de una canasta específica

```python
# ¿Qué utilidad da la canasta (10, 15)?
u = consumidor.utilidadAlcanzada(10, 15)
print(f"U(10, 15) = {u:.2f}")
```

**`curvaIndiferencia(nivel_utilidad, bien)`**: Obtiene puntos de una curva de indiferencia

```python
# Curva de indiferencia para U = 20
puntos = consumidor.curvaIndiferencia(nivel_utilidad=20, bien='x')
# Devuelve lista de puntos (x, y) con utilidad = 20
```

**`restriccionPresupuestaria()`**: Devuelve la ecuación de la restricción presupuestaria

```python
restriccion = consumidor.restriccionPresupuestaria()
print(restriccion)
# "3x + 2y = 120"
```

#### Cambio en precios e ingreso

```python
# Crear consumidor inicial
consumidor = Consumidor(
    utilidad="U = x * y",
    ingreso=100,
    precio_bien1=2,
    precio_bien2=4
)

demanda_inicial = consumidor.demandarOptima()
print(f"Canasta inicial: x={demanda_inicial['x']:.2f}, y={demanda_inicial['y']:.2f}")

# CAMBIO EN PRECIO: Bien X baja de precio
consumidor.cambiarPrecio(bien='x', nuevo_precio=1)
demanda_nueva = consumidor.demandarOptima()
print(f"Canasta después de que P_x baja: x={demanda_nueva['x']:.2f}, y={demanda_nueva['y']:.2f}")

# CAMBIO EN INGRESO: Aumenta el ingreso
consumidor.cambiarIngreso(nuevo_ingreso=150)
demanda_final = consumidor.demandarOptima()
print(f"Canasta con mayor ingreso: x={demanda_final['x']:.2f}, y={demanda_final['y']:.2f}")
```

#### Tipos de bienes

```python
# Analizar si un bien es normal o inferior
# (comparando cambios en la demanda cuando cambia el ingreso)

consumidor = Consumidor(
    utilidad="U = x^0.7 * y^0.3",
    ingreso=100,
    precio_bien1=2,
    precio_bien2=3
)

demanda_m100 = consumidor.demandarOptima()

consumidor.cambiarIngreso(200)
demanda_m200 = consumidor.demandarOptima()

# Cambio en la demanda
delta_x = demanda_m200['x'] - demanda_m100['x']
delta_y = demanda_m200['y'] - demanda_m100['y']

print(f"Cuando ingreso aumenta de $100 a $200:")
print(f"  Bien X: {demanda_m100['x']:.2f} → {demanda_m200['x']:.2f} (Δ = {delta_x:+.2f})")
print(f"  Bien Y: {demanda_m100['y']:.2f} → {demanda_m200['y']:.2f} (Δ = {delta_y:+.2f})")

if delta_x > 0:
    print("  → Bien X es NORMAL (aumenta con el ingreso)")
else:
    print("  → Bien X es INFERIOR (disminuye con el ingreso)")

if delta_y > 0:
    print("  → Bien Y es NORMAL (aumenta con el ingreso)")
else:
    print("  → Bien Y es INFERIOR (disminuye con el ingreso)")
```

#### Graficar restricción presupuestaria y curvas de indiferencia

```python
from oikos.utilidades import Lienzo, AZUL, ROJO, VERDE

consumidor = Consumidor(
    utilidad="U = x^0.5 * y^0.5",
    ingreso=100,
    precio_bien1=2,
    precio_bien2=5
)

# Graficar la restricción presupuestaria y curvas de indiferencia
consumidor.graficar()

# O graficar manualmente con más control
lienzo = Lienzo()
lienzo.configurarEtiquetas(
    etiquetaX="Bien X",
    etiquetaY="Bien Y",
    titulo="Elección del Consumidor"
)

# Agregar restricción presupuestaria
# p_x * x + p_y * y = m  →  y = (m - p_x * x) / p_y
lienzo.agregar(
    lambda x: (100 - 2*x) / 5,
    etiqueta="Restricción Presupuestaria",
    color=AZUL
)

# Agregar punto óptimo
optimo = consumidor.demandarOptima()
lienzo.agregarPunto(
    x=optimo['x'],
    y=optimo['y'],
    color=ROJO,
    dimension=12,
    mostrarNombre=True,
    nombre="E*"
)

# Agregar curva de indiferencia óptima
nivel_u = optimo['U']
puntos_ci = consumidor.curvaIndiferencia(nivel_utilidad=nivel_u, bien='x')
x_vals, y_vals = zip(*puntos_ci)
lienzo.agregar(
    lambda x: consumidor.utilidadInversa(nivel_u, x),
    etiqueta=f"U = {nivel_u:.2f}",
    color=VERDE,
    estiloLinea='--'
)

lienzo.graficar()
```

#### Ejemplo completo: Efecto de un impuesto

```python
# Analizar cómo afecta un impuesto al consumidor

# Estado inicial
consumidor = Consumidor(
    utilidad="U = x^0.6 * y^0.4",
    ingreso=200,
    precio_bien1=4,
    precio_bien2=5
)

print("SIN IMPUESTO:")
antes = consumidor.demandarOptima()
print(f"  Canasta: x={antes['x']:.2f}, y={antes['y']:.2f}")
print(f"  Utilidad: U={antes['U']:.2f}")
print(f"  Gasto: ${4*antes['x'] + 5*antes['y']:.2f}")

# Se aplica un impuesto de $2 por unidad del bien X
# Nuevo precio: $4 + $2 = $6
consumidor.cambiarPrecio(bien='x', nuevo_precio=6)

print("\nCON IMPUESTO ($2 por unidad de X):")
despues = consumidor.demandarOptima()
print(f"  Canasta: x={despues['x']:.2f}, y={despues['y']:.2f}")
print(f"  Utilidad: U={despues['U']:.2f}")
print(f"  Gasto: ${6*despues['x'] + 5*despues['y']:.2f}")

print("\nEFECTOS DEL IMPUESTO:")
print(f"  Δx = {despues['x'] - antes['x']:.2f} (consume menos X)")
print(f"  Δy = {despues['y'] - antes['y']:.2f}")
print(f"  ΔU = {despues['U'] - antes['U']:.2f} (pierde bienestar)")
print(f"  Recaudación = ${2 * despues['x']:.2f}")
```

---

### Demanda

La clase `Demanda` representa la función de demanda de un bien.

#### Creación

```python
from oikos import Demanda

# Forma 1: Q como función de P
demanda = Demanda("Q = 100 - 2P")

# Forma 2: P como función de Q
demanda = Demanda("P = 50 - 0.5Q")

# Forma 3: Ecuaciones más complejas
demanda = Demanda("Q = 200 - 3P + 0.5M")  # M = ingreso
```

#### Métodos principales

**`cantidad(precio)`**: Calcula la cantidad demandada a un precio dado

```python
demanda = Demanda("Q = 100 - 2P")

# ¿Cuánto se demanda a P=$10?
q = demanda.cantidad(precio=10)
print(q)  # 80.0
```

**`precio(cantidad)`**: Calcula el precio dado una cantidad (precio de reserva)

```python
# ¿A qué precio se demandan 60 unidades?
p = demanda.precio(cantidad=60)
print(p)  # 20.0
```

**`elasticidadPrecio(precio, cantidad)`**: Calcula la elasticidad precio de la demanda

```python
# Evaluar elasticidad en (P=10, Q=80)
e = demanda.elasticidadPrecio(precio=10, cantidad=80)
print(e)  # -0.25

# Interpretación automática
interpretacion = demanda.interpretarElasticidad(precio=10, cantidad=80)
print(interpretacion)
# "Demanda INELÁSTICA (ε = -0.25): Los consumidores son poco sensibles al precio"
```

#### Interpretación de elasticidades

La elasticidad precio de la demanda (ε) mide qué tan sensible es la cantidad demandada ante cambios en el precio:

| Elasticidad | Interpretación | Ejemplo |
|-------------|----------------|---------|
| \|ε\| > 1 | **ELÁSTICA** - Muy sensible al precio | Viajes de lujo, restaurantes |
| \|ε\| < 1 | **INELÁSTICA** - Poco sensible al precio | Pan, insulina, gasolina |
| \|ε\| = 1 | **UNITARIA** - Proporcional | Raro en la práctica |

**Fórmula matemática**:

```
ε = (dQ/dP) × (P/Q)
```

**Ejemplo práctico**:

```python
# Demanda de pan (inelástica)
pan = Demanda("Q = 100 - 0.5P")
e_pan = pan.elasticidadPrecio(precio=40, cantidad=80)
print(f"Elasticidad del pan: {e_pan:.2f}")  # -0.25 (inelástica)

# Demanda de viajes de lujo (elástica)
viajes = Demanda("Q = 200 - 5P")
e_viajes = viajes.elasticidadPrecio(precio=20, cantidad=100)
print(f"Elasticidad de viajes: {e_viajes:.2f}")  # -1.00 (elástica)
```

---

### Oferta

La clase `Oferta` representa la función de oferta de un bien.

#### Creación

```python
from oikos import Oferta

# Oferta típica (pendiente positiva)
oferta = Oferta("Q = -20 + 3P")

# Oferta con costo marginal constante
oferta = Oferta("P = 10 + 0.5Q")

# Oferta perfectamente inelástica (cantidad fija)
oferta = Oferta("Q = 100")
```

#### Métodos principales

Los mismos que `Demanda`:
- `cantidad(precio)`: Cantidad ofrecida a un precio
- `precio(cantidad)`: Precio mínimo para ofertar una cantidad
- `elasticidadPrecio(precio, cantidad)`: Elasticidad precio de la oferta

**Diferencia clave**: La elasticidad de la oferta es **positiva** (η > 0)

```python
oferta = Oferta("Q = -20 + 3P")

# Elasticidad en equilibrio
eta = oferta.elasticidadPrecio(precio=24, cantidad=52)
print(eta)  # +1.38 (elástica)
```

---

### Equilibrio de Mercado

La función `equilibrio()` encuentra el punto donde se cruzan oferta y demanda.

#### Uso básico

```python
from oikos import Demanda, Oferta, equilibrio

demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")

eq = equilibrio(oferta, demanda)
print(eq)
# {'P*': 24.0, 'Q*': 52.0}
```

#### ¿Qué hace internamente?

Resuelve el sistema:
```
Q_demanda = Q_oferta
P_demanda = P_oferta
```

#### Condiciones de equilibrio

En equilibrio se cumple:
1. **Cantidad demandada = Cantidad ofrecida** (no hay escasez ni excedente)
2. **No hay presión para que el precio cambie**
3. **Se maximiza el bienestar social** (bajo competencia perfecta)

#### Casos especiales

**Error: No existe equilibrio**

```python
# Demanda y oferta no se cruzan
demanda = Demanda("Q = 50 - P")
oferta = Oferta("Q = 200 + 2P")

try:
    eq = equilibrio(oferta, demanda)
except ErrorEquilibrio as e:
    print(e)  # "No existe equilibrio para este mercado"
```

---

### Excedentes

La función `excedentes()` calcula el excedente del consumidor (EC) y del productor (EP).

#### Teoría económica

**Excedente del Consumidor (EC)**:
- Beneficio que obtienen los consumidores
- Pagan menos de lo que estarían dispuestos a pagar
- Área entre la demanda y el precio de mercado

**Excedente del Productor (EP)**:
- Beneficio que obtienen los productores
- Reciben más de lo mínimo que aceptarían
- Área entre el precio de mercado y la oferta

**Excedente Social (ES)**:
- Bienestar total de la economía
- ES = EC + EP
- Se maximiza en competencia perfecta

#### Uso

```python
from oikos import excedentes

demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")

exc = excedentes(oferta, demanda)
print(exc)
# {
#   'EC': 1352.0,      # Excedente del consumidor
#   'EP': 2028.0,      # Excedente del productor
#   'ES': 3380.0,      # Excedente social
#   'P': 24.0,         # Precio de equilibrio
#   'Q': 52.0          # Cantidad de equilibrio
# }
```

#### Excedentes con intervención

Puedes calcular excedentes a cualquier precio/cantidad (ej: con impuestos):

```python
# Con precio máximo (control de precios)
exc_control = excedentes(oferta, demanda, precio=20, cantidad=40)

# Comparar con equilibrio libre
print(f"Pérdida de bienestar: {exc['ES'] - exc_control['ES']:.2f}")
```

---

### Elasticidades

#### Elasticidad Precio de la Demanda

**Definición**: Cambio porcentual en cantidad demandada ante un cambio del 1% en el precio.

**Fórmula**:
```
ε = (ΔQ/Q) / (ΔP/P) = (dQ/dP) × (P/Q)
```

**Interpretación**:
- Si ε = -2: Un aumento del 1% en P reduce Q en 2% (elástica)
- Si ε = -0.5: Un aumento del 1% en P reduce Q en 0.5% (inelástica)

**Ejemplo completo**:

```python
demanda = Demanda("Q = 100 - 2P")

# Evaluar en P=10
P = 10
Q = demanda.cantidad(P)  # Q = 80

# Calcular elasticidad
e = demanda.elasticidadPrecio(precio=P, cantidad=Q)

print(f"En el punto (P={P}, Q={Q}):")
print(f"  Elasticidad: ε = {e:.3f}")
print(f"  |ε| = {abs(e):.3f}")

if abs(e) > 1:
    print("  → ELÁSTICA: Los consumidores son MUY sensibles al precio")
elif abs(e) < 1:
    print("  → INELÁSTICA: Los consumidores son POCO sensibles al precio")
else:
    print("  → UNITARIA: Proporcional")
```

#### Elasticidad Precio de la Oferta

**Definición**: Cambio porcentual en cantidad ofrecida ante un cambio del 1% en el precio.

**Diferencia con demanda**: La elasticidad de la oferta es **positiva** (η > 0)

```python
oferta = Oferta("Q = -20 + 3P")

P = 24
Q = oferta.cantidad(P)  # Q = 52

eta = oferta.elasticidadPrecio(precio=P, cantidad=Q)
print(f"Elasticidad de oferta: η = {eta:.3f}")  # +1.38

if eta > 1:
    print("→ ELÁSTICA: Los productores pueden aumentar fácilmente la producción")
elif eta < 1:
    print("→ INELÁSTICA: Es difícil aumentar la producción")
```

---

## Macroeconomía

### Modelo IS-LM

El modelo IS-LM analiza el equilibrio macroeconómico de **corto plazo** en una economía cerrada.

#### Teoría del modelo

**Curva IS** (Investment-Savings):
- Representa el equilibrio en el **mercado de bienes**
- Ecuación: Y = C + I + G
- Pendiente negativa en el plano (Y, r)

**Curva LM** (Liquidity-Money):
- Representa el equilibrio en el **mercado de dinero**
- Ecuación: M/P = L(Y, r)
- Pendiente positiva en el plano (Y, r)

**Equilibrio IS-LM**:
- Punto donde se cruzan IS y LM
- Determina Y* (PIB) y r* (tasa de interés)

#### Creación del modelo

```python
from oikos import ISLM

# Instanciar el modelo
modelo = ISLM()

# Definir las funciones de comportamiento
consumo = "C = 200 + 0.8(Y - T)"
inversion = "I = 300 - 20r"
demandaDinero = "L = 0.2Y - 10r"

# Variables exógenas
G = 200   # Gasto público
T = 150   # Impuestos
M = 200   # Oferta monetaria
P = 1     # Nivel de precios

# Calcular equilibrio
eq = modelo.equilibrio(
    consumo=consumo,
    inversion=inversion,
    demandaDinero=demandaDinero,
    gastoPublico=G,
    impuestos=T,
    ofertaMonetaria=M,
    nivelPrecios=P
)

print(eq)
# {
#   'Y*': 1000.0,    # PIB de equilibrio
#   'r*': 5.0,       # Tasa de interés
#   'k': 0.83,       # Multiplicador fiscal
#   'm': 1.67,       # Multiplicador monetario
#   'C*': 680.0,     # Consumo
#   'I*': 200.0      # Inversión
# }
```

#### Interpretación de las ecuaciones

**Función de Consumo**: `C = 200 + 0.8(Y - T)`
- **200**: Consumo autónomo (lo que consumen aunque no tengan ingreso)
- **0.8**: Propensión marginal a consumir (PMgC)
  - Por cada $1 extra de ingreso disponible, consumen $0.80
- **(Y - T)**: Ingreso disponible (ingreso después de impuestos)

**Función de Inversión**: `I = 300 - 20r`
- **300**: Inversión autónoma (inversión cuando r=0%)
- **-20**: Sensibilidad de la inversión a la tasa de interés
  - Por cada 1% que sube r, la inversión cae en 20 unidades

**Demanda de Dinero**: `L = 0.2Y - 10r`
- **0.2Y**: Demanda transaccional (más ingreso → más dinero para transacciones)
- **-10r**: Demanda especulativa (mayor r → menos dinero, más bonos)

---

### Política Fiscal

La función `politicaFiscal()` simula el efecto de cambios en el gasto público (G).

#### Uso básico

```python
resultado = modelo.politicaFiscal(
    tipo="EXPANSIVA",      # O "CONTRACTIVA"
    magnitud=100,          # Cambio en G
    consumo=consumo,
    inversion=inversion,
    demandaDinero=demandaDinero,
    gastoPublicoInicial=200,
    impuestos=150,
    ofertaMonetaria=200,
    nivelPrecios=1
)

print(resultado['cambios'])
# {
#   'deltaY': +83.33,      # El PIB aumentó
#   'deltaR': +4.17,       # La tasa subió
#   'deltaC': +66.67,      # El consumo aumentó
#   'deltaI': -83.33,      # La inversión CAYÓ (efecto expulsión)
#   'deltaG': +100         # Aumento del gasto
# }

if resultado['efectoExpulsion']:
    print(f"⚠️ HAY EFECTO EXPULSIÓN")
    print(f"Proporción: {resultado['proporcionExpulsion']:.2%}")
    # Por cada $1 que gasta el gobierno, I cae $0.83
```

#### Efecto Expulsión (Crowding-out)

**¿Qué es?**
Cuando el gobierno aumenta G:
1. Y↑ (el PIB sube)
2. Mayor Y → Mayor demanda de dinero
3. Mayor demanda de dinero → r↑ (para equilibrar el mercado de dinero)
4. r↑ → I↓ (la inversión privada cae)

**Resultado**: El aumento de Y es menor que el esperado por el multiplicador fiscal simple.

**Visualización del efecto**:

```python
print(f"Gasto público aumentó: ΔG = +{resultado['cambios']['deltaG']}")
print(f"PIB aumentó: ΔY = +{resultado['cambios']['deltaY']}")
print(f"Inversión cayó: ΔI = {resultado['cambios']['deltaI']}")

# Multiplicador efectivo vs teórico
mult_efectivo = resultado['cambios']['deltaY'] / resultado['cambios']['deltaG']
mult_teorico = 1 / (1 - 0.8)  # 1 / (1 - PMgC) = 5

print(f"\\nMultiplicador teórico (sin crowding-out): {mult_teorico:.2f}")
print(f"Multiplicador efectivo (con crowding-out): {mult_efectivo:.2f}")
print(f"Diferencia: {mult_teorico - mult_efectivo:.2f}")
```

---

### Política Monetaria

La función `politicaMonetaria()` simula el efecto de cambios en la oferta monetaria (M).

#### Uso básico

```python
resultado = modelo.politicaMonetaria(
    tipo="EXPANSIVA",      # O "CONTRACTIVA"
    magnitud=50,           # Cambio en M
    consumo=consumo,
    inversion=inversion,
    demandaDinero=demandaDinero,
    gastoPublico=200,
    impuestos=150,
    ofertaMonetariaInicial=200,
    nivelPrecios=1
)

print(resultado['cambios'])
# {
#   'deltaY': +166.67,     # El PIB aumentó MÁS que con política fiscal
#   'deltaR': -8.33,       # La tasa BAJÓ (al revés que fiscal)
#   'deltaC': +133.33,     # El consumo aumentó
#   'deltaI': +166.67,     # La inversión SUBIÓ (no hay crowding-out)
#   'deltaM': +50          # Aumento de oferta monetaria
# }
```

#### ¿Por qué la política monetaria es más efectiva?

**Mecanismo de transmisión**:
1. M↑ (el Banco Central inyecta dinero)
2. Mayor oferta de dinero → r↓ (para equilibrar el mercado de dinero)
3. r↓ → I↑ (la inversión es más barata)
4. I↑ → Y↑ (vía efecto multiplicador)

**Ventajas**:
- ✅ NO causa efecto expulsión
- ✅ La inversión SUBE (en vez de caer)
- ✅ El multiplicador es mayor

**Comparación con política fiscal**:

```python
# Política Fiscal: ΔG = +100
# ΔY = +83.33, Δr = +4.17, ΔI = -83.33 (crowding-out)

# Política Monetaria: ΔM = +50
# ΔY = +166.67, Δr = -8.33, ΔI = +166.67 (NO crowding-out)

print("Política Fiscal:")
print("  ✓ Y↑, r↑")
print("  ✗ I↓ (crowding-out)")

print("\\nPolítica Monetaria:")
print("  ✓ Y↑, r↓")
print("  ✓ I↑ (estimula inversión)")
```

---

### Multiplicadores

#### Multiplicador Fiscal (k)

**Definición**: Cuánto cambia el PIB cuando el gasto público cambia en 1 unidad.

**Fórmula**:
```
k = ∂Y*/∂G
```

**Interpretación**:
- Si k = 2: Un aumento de G en $100 aumenta Y en $200
- El multiplicador es MENOR en IS-LM que en el modelo keynesiano simple (por el crowding-out)

**En el código**:

```python
eq = modelo.equilibrio(...)
print(f"Multiplicador fiscal: k = {eq['k']:.2f}")

# Si k = 0.83, significa:
# ΔG = +1 → ΔY = +0.83
# (El efecto expulsión reduce el multiplicador)
```

#### Multiplicador Monetario (m)

**Definición**: Cuánto cambia el PIB cuando la oferta monetaria cambia en 1 unidad.

**Fórmula**:
```
m = ∂Y*/∂M
```

**Interpretación**:
- Si m = 1.67: Un aumento de M en $100 aumenta Y en $167

**En el código**:

```python
eq = modelo.equilibrio(...)
print(f"Multiplicador monetario: m = {eq['m']:.2f}")

# Si m = 1.67, significa:
# ΔM = +1 → ΔY = +1.67
```

#### Comparación de multiplicadores

```python
eq = modelo.equilibrio(...)

print(f"Multiplicador fiscal: k = {eq['k']:.2f}")
print(f"Multiplicador monetario: m = {eq['m']:.2f}")

if eq['m'] > eq['k']:
    print("\\n✅ La política monetaria es MÁS efectiva")
else:
    print("\\n✅ La política fiscal es MÁS efectiva")
```

---

## Comercio Internacional

El módulo de comercio internacional implementa los modelos clásicos de comercio basados en ventajas comparativas y absolutas.

### Frontera de Posibilidades de Producción (FPP)

La Frontera de Posibilidades de Producción muestra las combinaciones máximas de dos bienes que una economía puede producir con sus recursos disponibles.

#### Teoría económica

**Concepto**: La FPP representa todas las combinaciones eficientes de dos bienes que se pueden producir con recursos fijos y tecnología dada.

**Pendiente de la FPP**: Representa el **costo de oportunidad** de producir un bien en términos del otro bien que se debe sacrificar.

**Puntos en la FPP**:
- **Sobre la frontera**: Producción eficiente (pleno empleo de recursos)
- **Dentro de la frontera**: Producción ineficiente (desempleo o recursos no utilizados)
- **Fuera de la frontera**: Inalcanzable con los recursos actuales

#### Creación básica

```python
from oikos import BienEconomico, FPP

# Definir los bienes
tela = BienEconomico("Tela", "metros")
vino = BienEconomico("Vino", "litros")

# Crear FPP para España
# España puede producir máximo 100 metros de Tela o 50 litros de Vino
fpp_espana = FPP(
    bien1=tela,
    bien2=vino,
    max_bien1=100,  # Producción máxima de tela
    max_bien2=50,   # Producción máxima de vino
    nombre_pais="España"
)

# Calcular costo de oportunidad
co_tela = fpp_espana.costoOportunidad(bien=tela)
print(f"Costo de oportunidad de 1 metro de Tela: {co_tela} litros de Vino")
# Salida: Costo de oportunidad de 1 metro de Tela: 0.5 litros de Vino

co_vino = fpp_espana.costoOportunidad(bien=vino)
print(f"Costo de oportunidad de 1 litro de Vino: {co_vino} metros de Tela")
# Salida: Costo de oportunidad de 1 litro de Vino: 2.0 metros de Tela
```

#### Interpretación del costo de oportunidad

```python
# Si España produce 1 metro más de Tela, debe renunciar a 0.5 litros de Vino
# Si España produce 1 litro más de Vino, debe renunciar a 2 metros de Tela

# Verificar si una producción es factible
es_factible = fpp_espana.produccionFactible(
    cantidad_bien1=50,  # 50 metros de tela
    cantidad_bien2=25   # 25 litros de vino
)
print(f"¿Es factible producir (50, 25)? {es_factible}")  # True

# Calcular la máxima producción de vino dada una cantidad de tela
tela_producida = 60
vino_max = fpp_espana.produccionBien2DadaBien1(tela_producida)
print(f"Si producimos {tela_producida} metros de tela, podemos producir máximo {vino_max} litros de vino")
```

#### Graficar la FPP

```python
# Graficar la FPP con un punto de producción
fpp_espana.graficar(
    punto_produccion=(50, 25),  # Marcar el punto (50 tela, 25 vino)
    color='#0066FF'
)
```

---

### Modelo Ricardiano

El Modelo Ricardiano explica el comercio internacional basado en diferencias en la productividad del trabajo entre países. Demuestra que el comercio beneficia a todos los países, incluso si uno es más productivo en todos los bienes.

#### Teoría del modelo

**Ventaja Absoluta**: Un país tiene ventaja absoluta si puede producir más de un bien con los mismos recursos.

**Ventaja Comparativa**: Un país tiene ventaja comparativa en el bien que puede producir con menor costo de oportunidad.

**Principio de Ricardo**: Los países deben especializarse en producir el bien en el que tienen ventaja comparativa, no ventaja absoluta.

#### Ejemplo completo: España vs Colombia

```python
from oikos import BienEconomico, FPP, Ricardiano

# Definir los bienes
tela = BienEconomico("Tela", "metros")
vino = BienEconomico("Vino", "litros")

# Crear FPPs
fpp_espana = FPP(tela, vino, max_bien1=100, max_bien2=50, nombre_pais="España")
fpp_colombia = FPP(tela, vino, max_bien1=80, max_bien2=120, nombre_pais="Colombia")

# Crear modelo ricardiano
modelo = Ricardiano(
    pais1="España",
    pais2="Colombia",
    bien1=tela,
    bien2=vino,
    fpp1=fpp_espana,
    fpp2=fpp_colombia
)

# Establecer producción sin comercio (autarquía)
# En autarquía, cada país produce en algún punto de su FPP
modelo.establecerProduccionSinComercio(
    pais1_bien1=50,   # España: 50 metros de tela
    pais1_bien2=25,   # España: 25 litros de vino
    pais2_bien1=40,   # Colombia: 40 metros de tela
    pais2_bien2=60    # Colombia: 60 litros de vino
)

# Análisis de ventajas
ventaja_absoluta = modelo.ventajaAbsoluta()
print("VENTAJA ABSOLUTA:")
print(f"  Tela: {ventaja_absoluta['Tela']}")      # España (100 > 80)
print(f"  Vino: {ventaja_absoluta['Vino']}")      # Colombia (120 > 50)

ventaja_comparativa = modelo.ventajaComparativa()
print("\nVENTAJA COMPARATIVA:")
print(f"  Tela: {ventaja_comparativa['Tela']}")   # España (CO = 0.5 < 0.67)
print(f"  Vino: {ventaja_comparativa['Vino']}")   # Colombia (CO = 1.5 < 2.0)
```

#### ¿Cómo se determina la ventaja comparativa?

```python
# Costos de oportunidad en cada país
co_tela_espana = fpp_espana.costoOportunidad(tela)      # 0.5 litros de Vino
co_tela_colombia = fpp_colombia.costoOportunidad(tela)  # 1.5 litros de Vino

co_vino_espana = fpp_espana.costoOportunidad(vino)      # 2.0 metros de Tela
co_vino_colombia = fpp_colombia.costoOportunidad(vino)  # 0.67 metros de Tela

print("COSTOS DE OPORTUNIDAD:")
print(f"Tela - España: {co_tela_espana:.2f} litros de Vino")
print(f"Tela - Colombia: {co_tela_colombia:.2f} litros de Vino")
print(f"Vino - España: {co_vino_espana:.2f} metros de Tela")
print(f"Vino - Colombia: {co_vino_colombia:.2f} metros de Tela")

print("\nINTERPRETACIÓN:")
print("• España tiene MENOR costo de oportunidad en Tela (0.5 < 1.5)")
print("  → España tiene ventaja comparativa en Tela")
print("• Colombia tiene MENOR costo de oportunidad en Vino (0.67 < 2.0)")
print("  → Colombia tiene ventaja comparativa en Vino")
```

---

### Ventaja Absoluta vs Comparativa

**Caso interesante**: Un país puede tener ventaja absoluta en ambos bienes, pero aún así beneficiarse del comercio.

```python
from oikos import BienEconomico, FPP, Ricardiano

tela = BienEconomico("Tela", "metros")
vino = BienEconomico("Vino", "litros")

# Portugal es más eficiente en AMBOS bienes (ventaja absoluta en ambos)
fpp_portugal = FPP(tela, vino, max_bien1=90, max_bien2=120, nombre_pais="Portugal")

# Inglaterra es menos eficiente en ambos
fpp_inglaterra = FPP(tela, vino, max_bien1=100, max_bien2=50, nombre_pais="Inglaterra")

modelo = Ricardiano(
    pais1="Portugal",
    pais2="Inglaterra",
    bien1=tela,
    bien2=vino,
    fpp1=fpp_portugal,
    fpp2=fpp_inglaterra
)

# Analizar ventajas
va = modelo.ventajaAbsoluta()
vc = modelo.ventajaComparativa()

print("VENTAJA ABSOLUTA:")
print(f"  Tela: {va['Tela']}")    # Inglaterra (100 > 90)
print(f"  Vino: {va['Vino']}")    # Portugal (120 > 50)

print("\nVENTAJA COMPARATIVA:")
print(f"  Tela: {vc['Tela']}")    # Inglaterra (CO = 0.5 < 1.33)
print(f"  Vino: {vc['Vino']}")    # Portugal (CO = 0.75 < 2.0)

print("\n¡CONCLUSIÓN CLAVE!")
print("Aunque Portugal tiene ventaja absoluta en Vino,")
print("ambos países se benefician si se especializan según ventaja comparativa:")
print("  • Inglaterra → Tela (donde su desventaja es menor)")
print("  • Portugal → Vino (donde su ventaja es mayor)")
```

---

### Términos de Intercambio

Los términos de intercambio determinan **cuánto de un bien se intercambia por una unidad del otro**.

#### Rango de términos mutuamente beneficiosos

Para que el comercio beneficie a ambos países, los términos de intercambio deben estar **entre los costos de oportunidad de ambos países**.

```python
# Usando el modelo anterior (España vs Colombia)
terminos = modelo.terminosIntercambio()

print("TÉRMINOS DE INTERCAMBIO MUTUAMENTE BENEFICIOSOS:")
print(f"Tela: entre {terminos['Tela'][0]:.2f} y {terminos['Tela'][1]:.2f} litros de Vino")
print(f"Vino: entre {terminos['Vino'][0]:.2f} y {terminos['Vino'][1]:.2f} metros de Tela")

# Interpretación:
# Si 1 metro de Tela se intercambia por 0.8 litros de Vino:
#   • España gana (su CO era 0.5, ahora obtiene 0.8)
#   • Colombia gana (su CO era 1.5, ahora paga solo 0.8)
```

#### Simulación de comercio completa

```python
# Establecer especialización completa según ventaja comparativa
modelo.establecerEspecializacionCompleta()

# Establecer el patrón de comercio
# España exporta Tela (su ventaja comparativa)
modelo.establecerComercio(
    exportador="España",
    bien_exportado=tela,
    cantidad_exportada=40  # España exporta 40 metros de tela
)

# Calcular ganancias del comercio
ganancias = modelo.gananciaComercio()

print("\nGANANCIAS DEL COMERCIO:")
for pais in ["España", "Colombia"]:
    print(f"\n{pais}:")
    for bien in ["Tela", "Vino"]:
        ganancia = ganancias[pais][bien]
        if ganancia > 0:
            print(f"  {bien}: +{ganancia:.1f} (GANA)")
        elif ganancia < 0:
            print(f"  {bien}: {ganancia:.1f}")
        else:
            print(f"  {bien}: 0.0")

# Mostrar análisis completo con tablas Rich
modelo.mostrarAnalisis()
```

#### Visualización del comercio

```python
# Graficar las FPPs de ambos países
modelo.graficarFPPs()

# Graficar el comercio con puntos de producción y consumo
modelo.graficarComercio()
```

Esta gráfica mostrará:
- **FPP** de cada país (línea azul)
- **Punto naranja**: Consumo/Producción sin comercio (autarquía)
- **Punto rojo**: Producción con especialización
- **Punto verde**: Consumo con comercio (¡fuera de la FPP original!)
- **Línea púrpura**: Intercambio comercial

---

### Modelo de Factores Específicos

El Modelo de Factores Específicos analiza el comercio cuando algunos factores de producción son **específicos de ciertos sectores** y no pueden moverse entre industrias (en el corto plazo).

#### Teoría del modelo

**Supuestos**:
- Tres factores de producción:
  - **Trabajo (L)**: Móvil entre sectores
  - **Capital sector 1 (K1)**: Específico del sector 1
  - **Capital sector 2 (K2)**: Específico del sector 2
- La apertura comercial afecta de manera diferente a cada factor

#### Uso básico

```python
from oikos import FactoresEspecificos

# Crear modelo
modelo = FactoresEspecificos(
    nombre_pais="Portugal",
    sector1="Manufacturas",
    sector2="Alimentos",
    trabajo_total=100,   # 100 trabajadores disponibles
    capital1=50,         # Capital específico de Manufacturas
    capital2=30          # Capital específico de Alimentos
)

# Asignar trabajo entre sectores
modelo.asignarTrabajo(trabajo_sector1=60)
# 60 trabajadores en Manufacturas, 40 en Alimentos

# Calcular producción usando función Cobb-Douglas
Q_manufacturas, Q_alimentos = modelo.produccion(alpha=0.5)

print(f"Producción de Manufacturas: {Q_manufacturas:.2f}")
print(f"Producción de Alimentos: {Q_alimentos:.2f}")
```

#### Análisis de efectos redistributivos

```python
# Antes de la apertura comercial
modelo.asignarTrabajo(trabajo_sector1=50)
Q1_antes, Q2_antes = modelo.produccion(alpha=0.5)

# Después de la apertura (el trabajo se reasigna)
modelo.asignarTrabajo(trabajo_sector1=70)  # Más trabajo a Manufacturas
Q1_despues, Q2_despues = modelo.produccion(alpha=0.5)

print("EFECTOS DE LA APERTURA COMERCIAL:")
print(f"Manufacturas: {Q1_antes:.2f} → {Q1_despues:.2f} ({Q1_despues - Q1_antes:+.2f})")
print(f"Alimentos: {Q2_antes:.2f} → {Q2_despues:.2f} ({Q2_despues - Q2_antes:+.2f})")

print("\nEFECTOS REDISTRIBUTIVOS:")
print("• Propietarios de K1 (capital de Manufacturas): GANAN")
print("• Propietarios de K2 (capital de Alimentos): PIERDEN")
print("• Trabajadores: Efecto ambiguo (depende del cambio en salarios)")
```

---

## Visualización

### Lienzo Simple

El `Lienzo` es la herramienta principal para crear gráficos económicos.

**IMPORTANTE**: Los economistas grafican funciones INVERSAS. Si tu función es `Q = 100 - 2P`, la gráfica muestra `P` en el eje Y vs `Q` en el eje X.

#### Uso básico

```python
from oikos import Demanda, Oferta, equilibrio
from oikos.utilidades import Lienzo, ROJO, VERDE2, AZUL

# Crear mercado
demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")
eq = equilibrio(oferta, demanda)

# Crear lienzo
lienzo = Lienzo()

# Configurar ejes y título
lienzo.configurarEtiquetas(
    etiquetaX="Cantidad (Q)",
    etiquetaY="Precio (P)",
    titulo="Mercado de Ejemplo"
)

# Agregar curvas (se grafican automáticamente como P vs Q)
lienzo.agregar(demanda, color=ROJO)
lienzo.agregar(oferta, color=VERDE2)

# Marcar equilibrio
lienzo.agregarPunto(
    x=eq['Q*'],
    y=eq['P*'],
    color=AZUL,
    dimension=10
)

# Mostrar
lienzo.graficar()
```

#### Método graficar() directo

Desde v0.3.1, puedes graficar directamente desde las clases:

```python
# Graficar solo demanda
demanda = Demanda("Q = 100 - 2P")
demanda.graficar()

# Graficar solo oferta
oferta = Oferta("Q = -20 + 3P")
oferta.graficar()

# Graficar IS-LM
modelo = ISLM()
modelo.graficar(
    consumo="C = 200 + 0.8(Y - T)",
    inversion="I = 300 - 20i",
    demandaDinero="L = 0.2Y - 10i",
    gastoPublico=200,
    impuestos=150,
    ofertaMonetaria=200
)
```

#### Métodos disponibles

| Método | Descripción |
|--------|-------------|
| `configurarEtiquetas()` | Establece títulos y etiquetas de ejes |
| `configurarRango()` | Define límites de los ejes |
| `configurarSaltos()` | Establece la separación entre marcas |
| `agregar()` | Añade una curva económica |
| `agregarPunto()` | Marca un punto (ej: equilibrio) |
| `agregarLineaVertical()` | Línea vertical |
| `agregarLineaHorizontal()` | Línea horizontal |
| `agregarRelleno()` | Sombrea un área (excedentes, DWL) |
| `graficar()` | Genera y muestra el gráfico |

---

### Lienzo Matricial

Permite crear múltiples gráficos en una cuadrícula.

#### Uso básico

```python
# Crear lienzo de 2x2
lienzo = Lienzo(
    matriz=(2, 2),              # 2 filas, 2 columnas
    dimensionMatriz=(16, 12),   # Tamaño total
    alinearEjes=False           # Cada gráfico con su escala
)

# ========== PANEL (1, 1) ==========
lienzo.cuadrante(1, 1)  # Fila 1, Columna 1
lienzo.configurarEtiquetas(titulo="Mercado A")
lienzo.agregar(demandaA, etiqueta="D", color=ROJO)
lienzo.agregar(ofertaA, etiqueta="S", color=AZUL)

# ========== PANEL (1, 2) ==========
lienzo.cuadrante(1, 2)  # Fila 1, Columna 2
lienzo.configurarEtiquetas(titulo="Mercado B")
lienzo.agregar(demandaB, etiqueta="D", color=ROJO)
lienzo.agregar(ofertaB, etiqueta="S", color=AZUL)

# ... (continuar con los demás paneles)

# Generar todo de una vez
lienzo.graficar()
```

#### Alinear ejes

Útil cuando quieres comparar mercados con la misma escala:

```python
lienzo = Lienzo(
    matriz=(2, 2),
    alinearEjes=True  # Compartir ejes X e Y
)

# Ahora todos los gráficos tendrán la misma escala
# (útil para comparar IS-LM antes/después de políticas)
```

---

### Estilos Personalizados

Puedes crear estilos custom para tus gráficos:

```python
from oikos import EstiloGrafico

# Crear estilo personalizado
mi_estilo = EstiloGrafico(
    dimensionFigura=(14, 10),    # Tamaño (ancho, alto)
    dpi=100,                      # Resolución
    dimensionTitulo=18,           # Tamaño del título
    dimensionLabel=14,            # Tamaño de etiquetas
    dimensionLeyenda=12,          # Tamaño de la leyenda
    anchoLinea=3,                 # Grosor de líneas
    paletaColores=['#E74C3C', '#3498DB', '#2ECC71']  # Colores custom
)

# Usar el estilo
lienzo = Lienzo(estilo=mi_estilo)
```

#### Parámetros de EstiloGrafico

| Parámetro | Descripción | Default |
|-----------|-------------|---------|
| `dimensionFigura` | Tamaño (ancho, alto) en pulgadas | (10, 7) |
| `dpi` | Resolución en puntos por pulgada | 100 |
| `dimensionTitulo` | Tamaño del título | 14 |
| `dimensionLabel` | Tamaño de etiquetas de ejes | 12 |
| `dimensionLeyenda` | Tamaño de leyenda | 10 |
| `anchoLinea` | Grosor de las curvas | 2 |
| `alphaRelleno` | Transparencia de rellenos (0-1) | 0.3 |
| `paletaColores` | Lista de colores predefinidos | Ver colores |

---

### Rellenos y Sombreado

Para visualizar excedentes, pérdida de bienestar, etc.

#### Excedente del Consumidor

```python
# Sombrear área entre demanda y precio de equilibrio
lienzo.agregarRelleno(
    funcion1=demanda,
    funcion2=lambda q: eq['P*'],  # Línea horizontal en P*
    rangoX=(0, eq['Q*']),
    color=ROJO,
    alpha=0.25,
    etiqueta="EC"
)
```

#### Excedente del Productor

```python
# Sombrear área entre precio de equilibrio y oferta
lienzo.agregarRelleno(
    funcion1=lambda q: eq['P*'],
    funcion2=oferta,
    rangoX=(0, eq['Q*']),
    color=AZUL,
    alpha=0.25,
    etiqueta="EP"
)
```

#### Pérdida de Bienestar (Deadweight Loss)

```python
# Con impuesto
P_con_impuesto = 30
Q_con_impuesto = 40

# Área del triángulo de pérdida
lienzo.agregarRelleno(
    funcion1=demanda,
    funcion2=oferta,
    rangoX=(Q_con_impuesto, eq['Q*']),
    color='red',
    alpha=0.3,
    etiqueta="DWL"
)
```

---

## Utilidades

### Parseador LaTeX

El parseador `translatex()` convierte ecuaciones LaTeX a objetos SymPy.

#### Uso básico

```python
from oikos import translatex

# Parsear ecuación simple
eq = translatex("Q = 100 - 2P")
print(eq)  # Eq(Q, 100 - 2*P)

# Parsear expresión (sin igualdad)
expr = translatex("P^2 + 3Q")
print(expr)  # P**2 + 3*Q
```

#### Sintaxis soportada

| LaTeX | Python | Ejemplo |
|-------|--------|---------|
| `+`, `-`, `*` | Básicos | `Q = 100 - 2P` |
| `^` | Potencia | `P^2` |
| `/` | División | `M/P` |
| `()` | Paréntesis | `0.8(Y - T)` |
| `sqrt{}` | Raíz cuadrada | `sqrt{P}` |
| `frac{}{}` | Fracción | `frac{M}{P}` |

#### Despejar variables

```python
from oikos import despejar

eq = translatex("Q = 100 - 2P")

# Despejar P en función de Q
P_expr = despejar(eq, 'P')
print(P_expr)  # (100 - Q) / 2
```

#### Extraer variables

```python
from oikos import extraerVariables

vars = extraerVariables("C = 200 + 0.8(Y - T)")
print(vars)  # ['C', 'Y', 'T']
```

---

### Validadores

Los validadores aseguran que los parámetros económicos sean válidos.

#### `validarPositivo()`

```python
from oikos import validarPositivo

precio = validarPositivo(10, "precio")  # OK

try:
    precio = validarPositivo(-5, "precio")
except ErrorValidacion as e:
    print(e)  # "El precio debe ser positivo"
```

#### `validarNoNegativo()`

```python
from oikos import validarNoNegativo

cantidad = validarNoNegativo(0, "cantidad")  # OK (acepta cero)
```

#### `validarRango()`

```python
from oikos import validarRango

probabilidad = validarRango(0.5, 0, 1, "probabilidad")  # OK

try:
    probabilidad = validarRango(1.5, 0, 1, "probabilidad")
except ErrorValidacion as e:
    print(e)  # "La probabilidad debe estar entre 0 y 1"
```

#### `validarPropension()`

Específico para propensiones marginales (0 ≤ PMg ≤ 1):

```python
from oikos import validarPropension

pmgc = validarPropension(0.8, "PMgC")  # OK

try:
    pmgc = validarPropension(1.5, "PMgC")
except ErrorValidacion as e:
    print(e)  # "La PMgC debe estar entre 0 y 1"
```

---

### Decoradores

Los decoradores añaden ayuda contextual a las funciones.

#### `@ayuda`

Añade información económica a las clases:

```python
from oikos import ayuda

@ayuda(
    descripcion_economica="Teoría de la demanda...",
    supuestos=["Preferencias constantes", "Ingreso constante"],
    cursos=["Microeconomía I"]
)
class MiModelo:
    pass
```

#### `@explicacion`

Añade explicación a los métodos:

```python
from oikos import explicacion

@explicacion("Calcula el equilibrio resolviendo oferta = demanda")
def equilibrio(oferta, demanda):
    # ...
    pass
```

---

## Ejemplos Avanzados

### Shock de Oferta con Análisis de Excedentes

```python
from oikos import Demanda, Oferta, equilibrio, excedentes, Lienzo, ROJO, AZUL, VERDE, NARANJA

# Mercado inicial
demanda = Demanda("Q = 150 - 2P")
oferta_original = Oferta("Q = -30 + 3P")

eq_antes = equilibrio(oferta_original, demanda)
exc_antes = excedentes(oferta_original, demanda)

# SHOCK NEGATIVO DE OFERTA (ej: desastre natural)
# La oferta se desplaza a la izquierda
oferta_shock = Oferta("Q = -60 + 3P")  # Intercepto más negativo

eq_despues = equilibrio(oferta_shock, demanda)
exc_despues = excedentes(oferta_shock, demanda)

# Análisis
print("ANTES DEL SHOCK:")
print(f"  P* = ${eq_antes['P*']:.2f}, Q* = {eq_antes['Q*']:.2f}")
print(f"  ES = ${exc_antes['ES']:.2f}")

print("\\nDESPUÉS DEL SHOCK:")
print(f"  P* = ${eq_despues['P*']:.2f}, Q* = {eq_despues['Q*']:.2f}")
print(f"  ES = ${exc_despues['ES']:.2f}")

print("\\nEFECTOS:")
print(f"  ΔP = +${eq_despues['P*'] - eq_antes['P*']:.2f}")
print(f"  ΔQ = {eq_despues['Q*'] - eq_antes['Q*']:.2f}")
print(f"  ΔES = -${exc_antes['ES'] - exc_despues['ES']:.2f}")

# Graficar
lienzo = Lienzo()
lienzo.configurarEtiquetas(titulo="Shock Negativo de Oferta")
lienzo.agregar(demanda, etiqueta="D", color=ROJO)
lienzo.agregar(oferta_original, etiqueta="S₀", color=AZUL, estiloLinea='--')
lienzo.agregar(oferta_shock, etiqueta="S₁ (post-shock)", color=AZUL)
lienzo.agregarPunto(eq_antes['Q*'], eq_antes['P*'], color=VERDE,
                   mostrarNombre=True, nombre="$E_0$")
lienzo.agregarPunto(eq_despues['Q*'], eq_despues['P*'], color=NARANJA,
                   mostrarNombre=True, nombre="$E_1$")
lienzo.graficar()
```

### Análisis de Impuestos

```python
# Mercado libre
demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")
eq_libre = equilibrio(oferta, demanda)
exc_libre = excedentes(oferta, demanda)

# Impuesto de $10 por unidad
# La oferta se desplaza hacia arriba en $10
# Q = -20 + 3(P - 10) = -50 + 3P
oferta_impuesto = Oferta("Q = -50 + 3P")
eq_impuesto = equilibrio(oferta_impuesto, demanda)

# Precios
Pc = eq_impuesto['P*']  # Precio consumidor
Ps = Pc - 10             # Precio productor

# Recaudación
recaudacion = 10 * eq_impuesto['Q*']

# Excedentes con impuesto
EC_impuesto = float(excedentes(oferta_impuesto, demanda)['EC'])
EP_impuesto = float(exc_libre['EP']) - (eq_libre['Q*'] - eq_impuesto['Q*']) * Ps

# Pérdida de bienestar
DWL = exc_libre['ES'] - EC_impuesto - EP_impuesto - recaudacion

print(f"SIN IMPUESTO:")
print(f"  P* = ${eq_libre['P*']:.2f}, Q* = {eq_libre['Q*']:.2f}")
print(f"  ES = ${exc_libre['ES']:.2f}")

print(f"\\nCON IMPUESTO ($10/unidad):")
print(f"  Pc = ${Pc:.2f} (pagan consumidores)")
print(f"  Ps = ${Ps:.2f} (reciben productores)")
print(f"  Q* = {eq_impuesto['Q*']:.2f}")
print(f"  Recaudación = ${recaudacion:.2f}")
print(f"  DWL = ${DWL:.2f}")

print(f"\\nINCIDENCIA DEL IMPUESTO:")
print(f"  Consumidores pagan: ${Pc - eq_libre['P*']:.2f} más")
print(f"  Productores pierden: ${eq_libre['P*'] - Ps:.2f}")
```

### Análisis Completo de Comercio Internacional

```python
from oikos import BienEconomico, FPP, Ricardiano

# Definir bienes
tela = BienEconomico("Tela", "metros")
vino = BienEconomico("Vino", "litros")

# Crear FPPs
fpp_espana = FPP(tela, vino, max_bien1=100, max_bien2=50, nombre_pais="España")
fpp_colombia = FPP(tela, vino, max_bien1=80, max_bien2=120, nombre_pais="Colombia")

# Crear modelo
modelo = Ricardiano(
    pais1="España",
    pais2="Colombia",
    bien1=tela,
    bien2=vino,
    fpp1=fpp_espana,
    fpp2=fpp_colombia
)

# PASO 1: Situación sin comercio (Autarquía)
print("=" * 60)
print("PASO 1: AUTARQUÍA (SIN COMERCIO)")
print("=" * 60)

modelo.establecerProduccionSinComercio(
    pais1_bien1=50,   # España: 50 tela, 25 vino
    pais1_bien2=25,
    pais2_bien1=40,   # Colombia: 40 tela, 60 vino
    pais2_bien2=60
)

print("\nConsumo sin comercio:")
print(f"  España:   {50} tela, {25} vino")
print(f"  Colombia: {40} tela, {60} vino")
print(f"  TOTAL:    {50+40} tela, {25+60} vino")

# PASO 2: Análisis de ventajas
print("\n" + "=" * 60)
print("PASO 2: ANÁLISIS DE VENTAJAS COMPARATIVAS")
print("=" * 60)

# Costos de oportunidad
co_tela_esp = fpp_espana.costoOportunidad(tela)
co_tela_col = fpp_colombia.costoOportunidad(tela)
co_vino_esp = fpp_espana.costoOportunidad(vino)
co_vino_col = fpp_colombia.costoOportunidad(vino)

print("\nCostos de Oportunidad:")
print(f"  Tela:")
print(f"    España:   {co_tela_esp:.2f} litros de Vino por metro")
print(f"    Colombia: {co_tela_col:.2f} litros de Vino por metro")
print(f"    → España tiene MENOR CO en Tela ✓")

print(f"\n  Vino:")
print(f"    España:   {co_vino_esp:.2f} metros de Tela por litro")
print(f"    Colombia: {co_vino_col:.2f} metros de Tela por litro")
print(f"    → Colombia tiene MENOR CO en Vino ✓")

vc = modelo.ventajaComparativa()
print(f"\nVentajas Comparativas:")
print(f"  Tela → {vc['Tela']} debe especializarse en Tela")
print(f"  Vino → {vc['Vino']} debe especializarse en Vino")

# PASO 3: Especialización y comercio
print("\n" + "=" * 60)
print("PASO 3: ESPECIALIZACIÓN Y COMERCIO")
print("=" * 60)

modelo.establecerEspecializacionCompleta()

print("\nProducción con especialización:")
print(f"  España:   {100} tela, {0} vino (especialización total en Tela)")
print(f"  Colombia: {0} tela, {120} vino (especialización total en Vino)")
print(f"  TOTAL:    {100} tela, {120} vino")

print("\n¡La producción mundial AUMENTÓ!")
print(f"  Tela: {90} → {100} (+{10} metros)")
print(f"  Vino: {85} → {120} (+{35} litros)")

# Establecer comercio
modelo.establecerComercio(
    exportador="España",
    bien_exportado=tela,
    cantidad_exportada=40
)

# PASO 4: Ganancias del comercio
print("\n" + "=" * 60)
print("PASO 4: GANANCIAS DEL COMERCIO")
print("=" * 60)

ganancias = modelo.gananciaComercio()

print("\nConsumo CON comercio:")
for pais in ["España", "Colombia"]:
    cons = modelo.consumo_con_comercio[pais]
    print(f"  {pais}: {cons['Tela']:.1f} tela, {cons['Vino']:.1f} vino")

print("\nGanancias absolutas:")
for pais in ["España", "Colombia"]:
    print(f"\n  {pais}:")
    for bien in ["Tela", "Vino"]:
        gan = ganancias[pais][bien]
        if gan > 0:
            print(f"    {bien}: +{gan:.1f} ✓")
        else:
            print(f"    {bien}: {gan:.1f}")

print("\n" + "=" * 60)
print("CONCLUSIÓN: ¡AMBOS PAÍSES GANAN CON EL COMERCIO!")
print("=" * 60)

# Mostrar análisis completo con tablas bonitas
print("\n")
modelo.mostrarAnalisis()

# Graficar
print("\nGenerando gráficos...")
modelo.graficarComercio()
```

---

## FAQ

### ¿Cómo leo ecuaciones de libros de texto?

```python
# Forma 1: Copiar directamente
demanda = Demanda("Q^d = 100 - 2P")  # Funciona

# Forma 2: Simplificada (sin superíndices)
demanda = Demanda("Q = 100 - 2P")    # Más simple

# Ambas son equivalentes
```

### ¿Puedo usar variables con subíndices?

```python
# Sí, pero evita el guión bajo _ (puede causar problemas)
consumo = "C = 200 + 0.8 Y_d"  # OK pero no ideal

# Mejor: usa paréntesis
consumo = "C = 200 + 0.8(Y - T)"  # ✅ Recomendado
```

### ¿Qué hacer si mi ecuación no parsea?

```python
# Problema común: División
demanda = "Q = 100 - P/2"  # ✅ Funciona

# Problema: Notación ambigua
demanda = "Q = 100 - P ÷ 2"  # ❌ No funciona

# Solución: usa /
demanda = "Q = 100 - P/2"  # ✅
```

### ¿Cómo incluyo parámetros externos?

```python
# Opción 1: Usar f-strings
M = 1000  # Ingreso del consumidor
demanda = Demanda(f"Q = 100 - 2P + 0.01*{M}")

# Opción 2: Dejar como variable simbólica
demanda = Demanda("Q = 100 - 2P + 0.01M")
# (Esto requiere sustituir M después)
```

### ¿Los gráficos se guardan automáticamente?

```python
# No, pero es fácil guardarlos:
fig, ax = lienzo.graficar(mostrar=False)
fig.savefig("mi_grafico.png", dpi=300, bbox_inches='tight')

# Formatos disponibles: png, pdf, svg, eps
```

---

## Referencia de API

### Clases Principales

#### `Consumidor`
- `__init__(utilidad: str, ingreso: float, precio_bien1: float, precio_bien2: float)`
- `demandarOptima() -> Dict[str, float]`
- `utilidadAlcanzada(x: float, y: float) -> float`
- `curvaIndiferencia(nivel_utilidad: float, bien: str) -> List[Tuple[float, float]]`
- `restriccionPresupuestaria() -> str`
- `cambiarPrecio(bien: str, nuevo_precio: float)`
- `cambiarIngreso(nuevo_ingreso: float)`
- `graficar(mostrar: bool = True)`

#### `Demanda`
- `__init__(ecuacion: str)`
- `cantidad(precio: float) -> float`
- `precio(cantidad: float) -> float`
- `elasticidadPrecio(precio: float, cantidad: float) -> float`
- `interpretarElasticidad(precio: float, cantidad: float) -> str`

#### `Oferta`
- `__init__(ecuacion: str)`
- `cantidad(precio: float) -> float`
- `precio(cantidad: float) -> float`
- `elasticidadPrecio(precio: float, cantidad: float) -> float`
- `interpretarElasticidad(precio: float, cantidad: float) -> str`

#### `ISLM`
- `__init__()`
- `equilibrio(consumo, inversion, demandaDinero, gastoPublico, impuestos, ofertaMonetaria, nivelPrecios=1.0) -> Dict`
- `politicaFiscal(tipo, magnitud, ...) -> Dict`
- `politicaMonetaria(tipo, magnitud, ...) -> Dict`
- `explicar() -> str`

#### `BienEconomico`
- `__init__(nombre: str, unidad: str = "unidades")`
- Representa un bien económico con su nombre y unidad de medida

#### `FPP`
- `__init__(bien1, bien2, max_bien1, max_bien2, nombre_pais="País")`
- `costoOportunidad(bien: BienEconomico) -> float`
- `produccionFactible(cantidad_bien1: float, cantidad_bien2: float) -> bool`
- `produccionBien2DadaBien1(cantidad_bien1: float) -> float`
- `graficar(punto_produccion=None, color=None, mostrar=True)`

#### `Ricardiano`
- `__init__(pais1, pais2, bien1, bien2, fpp1, fpp2)`
- `ventajaAbsoluta() -> Dict[str, str]`
- `ventajaComparativa() -> Dict[str, str]`
- `terminosIntercambio() -> Dict[str, Tuple[float, float]]`
- `establecerProduccionSinComercio(pais1_bien1, pais1_bien2, pais2_bien1, pais2_bien2)`
- `establecerEspecializacionCompleta()`
- `establecerComercio(exportador, bien_exportado, cantidad_exportada)`
- `gananciaComercio() -> Dict[str, Dict[str, float]]`
- `mostrarAnalisis()`
- `graficarFPPs(mostrar=True)`
- `graficarComercio(mostrar=True)`

#### `FactoresEspecificos`
- `__init__(nombre_pais, sector1, sector2, trabajo_total, capital1, capital2)`
- `asignarTrabajo(trabajo_sector1: float)`
- `produccion(alpha: float = 0.5) -> Tuple[float, float]`

#### `Lienzo`
- `__init__(estilo=None, cuadrantes="I", relacionAspecto="auto", matriz=None, dimensionMatriz=None, alinearEjes=False)`
- `cuadrante(fila: int, columna: int)`
- `configurarEtiquetas(etiquetaX=None, etiquetaY=None, titulo=None)`
- `configurarRango(rangoX=None, rangoY=None)`
- `agregar(funcion, etiqueta=None, color=None, ...)`
- `agregarPunto(x, y, etiqueta=None, color=None, ...)`
- `agregarLineaVertical(x, etiqueta=None, color=None, ...)`
- `agregarLineaHorizontal(y, etiqueta=None, color=None, ...)`
- `agregarRelleno(funcion1, funcion2=None, rangoX=None, ...)`
- `graficar(mostrar=True) -> (fig, ax)`

### Funciones Principales

#### `equilibrio(oferta, demanda) -> Dict`
Calcula el equilibrio de mercado.

**Returns**:
```python
{
    'P*': float,  # Precio de equilibrio
    'Q*': float   # Cantidad de equilibrio
}
```

#### `excedentes(oferta, demanda, precio=None, cantidad=None) -> Dict`
Calcula excedentes.

**Returns**:
```python
{
    'EC': float,  # Excedente del consumidor
    'EP': float,  # Excedente del productor
    'ES': float,  # Excedente social
    'P': float,   # Precio usado
    'Q': float    # Cantidad usada
}
```

### Colores Predefinidos

Importa desde `oikos.utilidades`:

```python
from oikos.utilidades import (
    ROJO, AZUL, VERDE, VERDE2,
    AMARILLO, NARANJA, MORADO,
    TURQUESA, CELESTE, ROSA
)

# Colores por defecto
COLOR_DEMANDA = ROJO    # Para curvas de demanda
COLOR_OFERTA = VERDE2   # Para curvas de oferta
```

### Excepciones

```python
ErrorOikos              # Excepción base
ErrorParseador          # Error al parsear ecuación
ErrorEquilibrio         # No existe equilibrio
ErrorValidacion         # Parámetro inválido
ErrorGrafico            # Error en visualización
```

---

## Contribuir

¿Quieres contribuir a OIKOS?

1. **Fork** el repositorio
2. Crea una **rama** para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** tus cambios (`git commit -m 'feat: añadir nueva funcionalidad'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un **Pull Request**

### Guía de estilo

- **Nombres en español**: Variables, funciones y clases en español (sin ñ)
- **camelCase**: Para variables y parámetros
- **CamelCase**: Para clases
- **Comentarios**: En español, explicando la economía detrás del código

---

## Licencia

MIT License - Ver archivo LICENSE para más detalles.

---

## Contacto

- **Autor**: Marcos Junior Hernández-Moreno
- **Email**: [tu-email]
- **GitHub**: https://github.com/marcosjuniorhernandez/economy
- **Documentación**: https://oikos.readthedocs.io/

---

## Citación

Si usas OIKOS en trabajos académicos, por favor cita:

```
Marcos Junior Hernández-Moreno (2024). OIKOS: Librería para Economía en Python.
Versión 0.3.0. https://github.com/marcosjuniorhernandez/economy
```

BibTeX:
```bibtex
@software{oikos2024,
  author = {Marcos Junior Hernández-Moreno},
  title = {OIKOS: Librería para Economía en Python},
  year = {2024},
  version = {0.3.0},
  url = {https://github.com/marcosjuniorhernandez/economy}
}
```

---

**¡Gracias por usar OIKOS!**

Si tienes preguntas, consulta la documentación online o envía tus sugerencias al correo iam.marcoshernandez@gmail.com con el asunto: OIKOS

---

Copyright (c) 2026 **Marcos Junior Hernández-Moreno** [![ORCID](https://img.shields.io/badge/ORCID-0000--0001--6109--6358-green?logo=orcid&logoColor=white)](https://orcid.org/0000-0001-6109-6358)