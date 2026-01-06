# Manual de Uso
Este manual de referencia detalla los módulos, funciones y variables incluidos en Oikos, describiendo lo que son y lo que hacen. Para obtener una lista de los cambios desde la última versión, consulte el [Registro de cambios](changelog.md).

Este documento también describe de manera detallada la **referencia técnica** de la librería **Oikos**, incluyendo su filosofía, estructura conceptual, módulos y convenciones de uso.

Oikos está diseñada para **economistas**, con un enfoque **analítico, simbólico y didáctico**, orientado a la representación de modelos económicos clásicos y modernos.

---

## 1. Filosofía de diseño

Oikos se basa en los siguientes principios:

- **Rigor económico**: los modelos respetan la teoría económica formal.
- **Claridad conceptual**: el código refleja directamente las ecuaciones económicas.
- **Enfoque simbólico**: uso de expresiones matemáticas antes que simulaciones numéricas.
- **Uso académico**: pensada para docencia, estudio y exploración teórica.


## 2. Convenciones generales

- Todas las variables económicas se representan como **objetos simbólicos**.
- Los modelos siguen la lógica:
  - Definición de variables
  - Definición de ecuaciones
  - Condiciones de equilibrio
- No se fuerza calibración empírica.
- La notación busca parecerse a la notación económica estándar.

---
## Conceptos previos a oikos
Para aprovechar al máximo las capacidades de documentación y visualización de **oikos**, se recomienda que el usuario posea conocimientos básicos de **LaTeX**. Dado que el proyecto busca una integración rigurosa entre la programación y la teoría económica, gran parte de la simbología y las definiciones de funciones (como la especificación de curvas de demanda $Q_d = a - bP$) utilizan este sistema de composición tipográfica.

Dominar LaTeX permitirá no solo interpretar correctamente las fórmulas generadas por el modelo, sino también personalizar los reportes y gráficos técnicos que el ecosistema produce. 

Para obtener más información sobre la sintaxis y el manejo de ecuaciones en $\LaTeX$, puede consultar el siguiente recurso: [Tutorial de Ecuaciones en LaTeX](https://manualdelatex.com/tutoriales/ecuaciones).

El motor de visualización de **oikos** procesa fórmulas complejas. Por ejemplo, el cálculo del Bienestar Total se define como:

```latex
\int_{0}^{Q^{*}} (P^{D}(Q) - P^{S}(Q)) \,dQ = EC + EP
```

Lo que está entendiendo la librería es:

\[
    \int_{0}^{Q^*} (P_d(Q) - P_s(Q)) \,dQ = EC + EP    
\]


## Microeconomía

### Clase `Demand` (Demanda)

Representa una función de demanda en un mercado.

#### Inicialización

```python
demanda = ok.Demand(formula)
```

**Parámetros:**
- `formula` (str): Ecuación de demanda en formato string. Puede estar expresada como:
  - `Q = f(P)` - Cantidad en función del precio
  - `P = f(Q)` - Precio en función de la cantidad

**Ejemplos:**

```python
# Demanda lineal
d1 = ok.Demand(r"Q = 120 - P")
d2 = ok.Demand(r"P = 120 - Q")

# Demanda elástica
d_elastica = ok.Demand(r"Q = 100 - 2P")

# Demanda inelástica
d_inelastica = ok.Demand(r"Q = 50 - 0.5P")

# Demanda no lineal (hiperbólica)
d_unitaria = ok.Demand(r"Q = 100/P")
```

#### Métodos

##### `getPriceInterpretation(Q, P)`

Calcula e interpreta la elasticidad precio de la demanda en un punto específico.

**Parámetros:**
- `Q` (float): Cantidad
- `P` (float): Precio

**Retorna:** Interpretación de la elasticidad (Elastic, Inelastic, Unitary) con el valor numérico.

**Ejemplo:**

```python
d = ok.Demand(r"Q = 100 - 2P")
interpretacion = d.getPriceInterpretation(20, 40)
# Output: "Elastic (-4.00)"
```

### Clase `Supply` (Oferta)

Representa una función de oferta en un mercado.

#### Inicialización

```python
oferta = ok.Supply(formula)
```

**Parámetros:**
- `formula` (str): Ecuación de oferta en formato string

**Ejemplos:**

```python
# Oferta lineal
s1 = ok.Supply(r"Q = 2P")
s2 = ok.Supply(r"Q = P")
```

#### Métodos

##### `priceElasticity(Q, P)`

Calcula la elasticidad precio de la oferta en un punto específico.

**Parámetros:**
- `Q` (float): Cantidad
- `P` (float): Precio

**Retorna:** Valor numérico de la elasticidad.

**Ejemplo:**

```python
s = ok.Supply(r"Q = P")
elasticidad = s.priceElasticity(10, 10)
# Output: 1.00
```

### Función `equilibrium(supply, demand)`

Calcula el punto de equilibrio del mercado donde oferta y demanda se intersectan.

**Parámetros:**
- `supply` (Supply): Objeto de tipo Supply
- `demand` (Demand): Objeto de tipo Demand

**Retorna:** Tupla `(Q*, P*)` con la cantidad y precio de equilibrio.

**Ejemplo:**

```python
demanda = ok.Demand(r"Q = 120 - P")
oferta = ok.Supply(r"Q = 2P")

equilibrio = ok.equilibrium(oferta, demanda)
print(equilibrio)
# Output: (80, 40)
```

---

## Macroeconomía

### Clase `ISLM`

Representa el modelo IS-LM para análisis macroeconómico de equilibrio en los mercados de bienes y dinero.

#### Inicialización

```python
modelo = ok.ISLM()
```

#### Atributos

- `output` (Y): Variable simbólica para el producto/ingreso nacional
- `interestRate` (r): Variable simbólica para la tasa de interés
- `govermentSpending` (T): Variable simbólica para el gasto gubernamental

#### Métodos

##### `equilibrium(consumptionFunction, investmentFunction, liquidityPreferenceFunction, gValue, tValue, mValue, pValue)`

Calcula el equilibrio IS-LM y los multiplicadores fiscales y monetarios.

**Parámetros:**
- `consumptionFunction` (str): Función de consumo C = f(Y, T)
- `investmentFunction` (str): Función de inversión I = f(r)
- `liquidityPreferenceFunction` (str): Función de preferencia por liquidez L = f(Y, r)
- `gValue` (float): Valor del gasto gubernamental (G)
- `tValue` (float): Valor de los impuestos (T)
- `mValue` (float): Valor de la oferta monetaria nominal (M)
- `pValue` (float): Valor del nivel de precios (P)

**Retorna:** Diccionario con:
- `Y*`: Producto de equilibrio
- `r*`: Tasa de interés de equilibrio
- `fiscal_multiplier`: Multiplicador fiscal
- `monetary_multiplier`: Multiplicador monetario

**Ejemplo:**

```python
modeloISLM = ok.ISLM()

# Definir variables simbólicas
Y = modeloISLM.output
r = modeloISLM.interestRate
T = modeloISLM.govermentSpending

# Definir funciones macroeconómicas
C = r"100 + 0.8 * (Y - T)"    # Consumo
I = r"150 - 1000 * r"         # Inversión
L = r"0.2 * Y - 500 * r"      # Demanda de dinero

# Calcular equilibrio
resultado = modeloISLM.equilibrium(
    consumptionFunction=C,
    investmentFunction=I,
    liquidityPreferenceFunction=L,
    gValue=100,
    tValue=100,
    mValue=1300,
    pValue=1
)

# Visualizar resultados
ok.escribir(resultado)
```

**Salida esperada:**

```
Y* = 4783.33 ; r* = -0.69 ; fiscal_multiplier = 1.67 ; monetary_multiplier = 3.33
```

---

## Función Auxiliar

### `escribir(result)`

Formatea y muestra resultados en formato LaTeX para Jupyter Notebook.

**Parámetros:**
- `result` (dict): Diccionario con resultados a mostrar

**Ejemplo:**

```python
ok.escribir(resultado)
```