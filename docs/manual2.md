# 📚 Manual Completo de OIKOS v0.3.0

**Librería para Economía en Python**

Autor: Marcos Jr.
Licencia: MIT
Documentación: https://oikos.readthedocs.io/en/latest/manual/

---

## 🎯 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Guía Rápida](#guía-rápida)
4. [Microeconomía](#microeconomía)
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
6. [Visualización](#visualización)
   - [Lienzo Simple](#lienzo-simple)
   - [Lienzo Matricial](#lienzo-matricial)
   - [Estilos Personalizados](#estilos-personalizados)
   - [Rellenos y Sombreado](#rellenos-y-sombreado)
7. [Utilidades](#utilidades)
   - [Parseador LaTeX](#parseador-latex)
   - [Validadores](#validadores)
   - [Decoradores](#decoradores)
8. [Ejemplos Avanzados](#ejemplos-avanzados)
9. [FAQ](#faq)
10. [Referencia de API](#referencia-de-api)

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
git clone https://github.com/tu-usuario/oikos.git
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
from oikos import Demanda, Oferta, equilibrio, Lienzo, ROJO, AZUL, VERDE

# 1. Crear funciones de demanda y oferta
demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")

# 2. Calcular el equilibrio
eq = equilibrio(oferta, demanda)
print(eq)  # {'P*': 24.0, 'Q*': 52.0}

# 3. Graficar el mercado
lienzo = Lienzo()
lienzo.configurarEtiquetas(
    etiquetaX="Cantidad",
    etiquetaY="Precio",
    titulo="Mi Primer Mercado"
)
lienzo.agregar(demanda, etiqueta="Demanda", color=ROJO)
lienzo.agregar(oferta, etiqueta="Oferta", color=AZUL)
lienzo.agregarPunto(eq['Q*'], eq['P*'], color=VERDE, dimension=12)
lienzo.graficar()
```

**¡Eso es todo!** Con 15 líneas de código ya tienes un análisis de mercado completo.

---

## Microeconomía

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

## Visualización

### Lienzo Simple

El `Lienzo` es la herramienta principal para crear gráficos económicos.

#### Uso básico

```python
from oikos import Lienzo, Demanda, Oferta, equilibrio, ROJO, AZUL, VERDE

# Crear mercado
demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")
eq = equilibrio(oferta, demanda)

# Crear lienzo
lienzo = Lienzo()

# Configurar ejes y título
lienzo.configurarEtiquetas(
    etiquetaX="Cantidad (unidades)",
    etiquetaY="Precio ($/unidad)",
    titulo="Mercado de Ejemplo"
)

# Agregar curvas
lienzo.agregar(demanda, etiqueta="Demanda", color=ROJO)
lienzo.agregar(oferta, etiqueta="Oferta", color=AZUL)

# Marcar equilibrio
lienzo.agregarPunto(
    x=eq['Q*'],
    y=eq['P*'],
    etiqueta=f"E₀ (Q={eq['Q*']:.0f}, P=${eq['P*']:.2f})",
    color=VERDE,
    dimension=12,
    mostrarNombre=True,
    nombre="$E_0$"  # LaTeX
)

# Líneas guía
lienzo.agregarLineaVertical(x=eq['Q*'], color='gray', estiloLinea='--')
lienzo.agregarLineaHorizontal(y=eq['P*'], color='gray', estiloLinea='--')

# Mostrar
lienzo.graficar()
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
lienzo.vista(1, 1)  # Fila 1, Columna 1
lienzo.configurarEtiquetas(titulo="Mercado A")
lienzo.agregar(demandaA, etiqueta="D", color=ROJO)
lienzo.agregar(ofertaA, etiqueta="S", color=AZUL)

# ========== PANEL (1, 2) ==========
lienzo.vista(1, 2)  # Fila 1, Columna 2
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
    dpi=150,                      # Resolución
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

#### `Lienzo`
- `__init__(estilo=None, cuadrantes="I", relacionAspecto="auto", matriz=None, dimensionMatriz=None, alinearEjes=False)`
- `vista(fila: int, columna: int)`
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

```python
ROJO = '#E74C3C'
AZUL = '#3498DB'
VERDE = '#2ECC71'
AMARILLO = '#F39C12'
NARANJA = '#E67E22'
MORADO = '#9B59B6'
TURQUESA = '#1ABC9C'
ROSA = '#FF69B4'
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

- **Autor**: Marcos Jr.
- **Email**: [tu-email]
- **GitHub**: https://github.com/tu-usuario/oikos
- **Documentación**: https://oikos.readthedocs.io/

---

## Citación

Si usas OIKOS en trabajos académicos, por favor cita:

```
Marcos Jr. (2024). OIKOS: Librería para Economía en Python.
Versión 0.3.0. https://github.com/tu-usuario/oikos
```

BibTeX:
```bibtex
@software{oikos2024,
  author = {Marcos Jr.},
  title = {OIKOS: Librería para Economía en Python},
  year = {2024},
  version = {0.3.0},
  url = {https://github.com/tu-usuario/oikos}
}
```

---

**¡Gracias por usar OIKOS!** 🎉

Si tienes preguntas, abre un issue en GitHub o consulta la documentación online.
