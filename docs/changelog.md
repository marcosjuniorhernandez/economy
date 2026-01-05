# Changelog

Esta página contiene una lista de los cambios realizados entre versiones. 

---

## **v0.2.1**
[Hotfix: Corrección de Exportación]

**Fecha:** 03 Enero de 2026  
Esta es una versión de mantenimiento para corregir un error crítico en la API de salida.

### Cambios realizados
- **Corrección en `ok.write`:** Se resolvió un conflicto de nombres donde la función de escritura se importaba incorrectamente como `show`, rompiendo la compatibilidad con el motor de renderizado.
- **Estabilidad:** Se restauró la capacidad de visualizar resultados de equilibrio y multiplicadores en la terminal y notebooks.

---

## v0.2.0 — Expansión Analítica y Macroeconómica

**Fecha:** 03 Enero de 2026

Esta versión representa un salto significativo desde la validación de concepto hacia una herramienta de modelado técnica. Se introducen **clases orientadas a objetos**, soporte para **ecuaciones no lineales** y el primer motor de **macroeconomía (IS-LM)**.

---

### Alcance general
- **Paradigma de Clases:** Transición de funciones simples a objetos `Demand`, `Supply` e `ISLM` para una gestión robusta de atributos.
- **Análisis de Elasticidades:** Capacidad de interpretar automáticamente el tipo de elasticidad (elástica, inelástica, unitaria) en puntos específicos.
- **Flexibilidad en Ecuaciones:** Soporte para funciones no lineales (ej. demandas hiperbólicas $Q = 100/P$) y resolución de variables despejadas tanto en $P$ como en $Q$.
- **Introducción a la Macroeconomía:** Implementación del equilibrio simultáneo en el mercado de bienes y dinero.
- **Cálculo de Multiplicadores:** Determinación automática de multiplicadores fiscales y monetarios para análisis de política económica.

---

### Nuevas Funcionalidades y Mejoras

#### 1. Gestión de Elasticidades (`getPriceInterpretation`)
El motor ahora no solo calcula el valor numérico, sino que devuelve una interpretación semántica de la sensibilidad del mercado.

**Representación económica:** Permite identificar si un bien es de lujo, de primera necesidad o si el ingreso total se maximiza (elasticidad unitaria) en un precio dado.



#### 2. Soporte para Funciones No Lineales
A diferencia de la v0.1.0, ahora es posible definir curvas con pendientes variables, permitiendo modelos de utilidad marginal o comportamientos de mercado más realistas.

#### 3. Modelo IS-LM (`ok.ISLM`)
Se añade la capacidad de resolver el equilibrio general de una economía cerrada en el corto plazo mediante la interacción de la curva IS (mercado de bienes) y la curva LM (mercado de dinero).



**Representación económica:** Encuentra el nivel de ingreso ($Y^*$) y la tasa de interés ($r^*$) de equilibrio.

#### 4. Motor de Multiplicadores
Calcula automáticamente el impacto de las políticas económicas:
- **Fiscal:** Efecto de variaciones en el gasto público sobre el PIB.
- **Monetario:** Efecto de variaciones en la oferta de dinero sobre el ingreso real.

---

### Ejemplo de implementación (v0.2.0)

```python
import oikos as ok

# 1. Instanciar el modelo macroeconómico
modeloISLM = ok.ISLM()
Y, r, T = modeloISLM.output, modeloISLM.interestRate, modeloISLM.govermentSpending

# 2. Definir funciones económicas
C = "100 + 0.8 * (Y - T)"   # Consumo
I = "150 - 1000 * r"       # Inversión
L = "0.2 * Y - 500 * r"    # Demanda de dinero

# 3. Calcular equilibrio
resultado = modeloISLM.equilibrium(
    consumptionFunction=C,
    investmentFunction=I,
    liquidityPreferenceFunction=L,
    gValue=100, tValue=100, mValue=1300, pValue=1
)

ok.write(resultado)
```

---

### ⚠️ Breaking Changes (Cambios Críticos)

Esta versión introduce cambios estructurales que **no son compatibles** con scripts de la v0.1.0:

#### 1. Migración a Clases (POO)
Ya no se utilizan funciones globales. Ahora la lógica se encapsula en objetos.
* **Antes:** `demanda = demandaLineal(...)`
* **Ahora:** `demanda = ok.Demand(r"Q = ...")`

#### 2. Definición mediante Strings
Las ecuaciones ahora deben ingresarse como **Raw Strings** (`r"..."`). Esto permite al motor de **oikos** procesar funciones no lineales y despejes automáticos (ej. `r"Q = 100/P"`).

#### 3. Sintaxis del Equilibrio
El método `ok.equilibrium()` ahora detecta automáticamente si estás comparando objetos de Oferta/Demanda o si estás resolviendo el modelo IS-LM, requiriendo los objetos o funciones correspondientes como parámetros nombrados.

#### 4. Variables Reservadas en Macro
Para el modelo IS-LM, es obligatorio asignar los símbolos de la instancia a variables locales (`Y = modelo.output`, `r = modelo.interestRate`) para que el motor reconozca los componentes de las funciones de Consumo, Inversión y Dinero.

---
## **v0.1.0** 
[Versión inicial]

**Fecha:** 
02 Enero de 2025

El objetivo central de este lanzamiento es consolidar la identidad del proyecto y validar la viabilidad técnica de modelar principios microeconómicos mediante Python. Se trata de un modelo de baja fidelidad diseñado para testear la arquitectura lógica inicial.

La implementación se presenta como un prototipo experimental; prioriza la demostración de conceptos básicos sobre la robustez arquitectónica o la definición de una librería final.

### Alcance general
1. Implementación de un modelo único de oferta y demanda lineal, optimizado para el cálculo de equilibrios estáticos.
2. Gestión manual de parámetros, lo que permite una calibración directa de las variables exógenas por parte del analista.
3. Estructura de importación ```from oikos.microeconomics.market import Demand, Supply, equilibrium```, diseñada para un acceso a las funciones principales en esta etapa temprana.
4. Arquitectura integrada, donde la lógica económica y la visualización de datos operan de forma conjunta para reducir la fricción inicial.
5. Especialización en microeconomía básica, con un enfoque centrado en los fundamentos de la teoría del mercado.

### Funciones disponibles
La versión **v0.1.0** incluye únicamente **6 funciones**, todas orientadas a representar un mercado competitivo simple.

#### 1. Oferta lineal
Define una función de oferta de la forma:

\[
    Q_s = c + dP
\]

**Representación económica:**  
Modela el comportamiento de los productores, donde la cantidad ofrecida aumenta a medida que sube el precio.

```python
from oikos.microeconomics.market import Supply

demanda = Supply(0, 2)
```

#### 2. Demanda lineal
Define una función de demanda de la forma:

\[
    Q_d = a - bP
\]

**Representación económica:**  
Modela el comportamiento de los consumidores, donde la cantidad demandada disminuye cuando el precio aumenta.

```python
from oikos.microeconomics.market import Demand

demanda = Demand(120, 1)
```

#### 3. Equilibrio de mercado

\[
    Q^{S} = Q^{D}
\]

Devuelve el **precio de equilibrio** y la **cantidad de equilibrio**.

**Representación económica:**  
Corresponde al estado del mercado donde no existen fuerzas internas que empujen el precio al alza o a la baja.

```python
from oikos.microeconomics.market import Supply, Demand, equilibrium

oferta = Supply(0, 2)
demanda = Demand(120, 1)

equilibrium(oferta, demanda)
```

OUTPUT: ```>>> (40.0, 80.0)```

#### 4. `oferta.quantity(12)`
Retorna la cantidad ofrecida a un nivel de precios determinado.

```python
# Ejemplo de consulta puntual
oferta.quantity(12)
```

### Otras funcionalidades 
#### 5. ```marketGraph(oferta, demanda)```
Genera una visualización básica del mercado que integra los elementos fundamentales del equilibrio:

```python
from oikos.graphs import marketGraph

marketGraph(oferta, demanda)
```

* **Curva de oferta:** Representación de la disposición a vender.
* **Curva de demanda:** Representación de la disposición a pagar.
* **Punto de equilibrio:** Intersección que determina el precio y cantidad de vaciado del mercado.

**Representación económica:** Esta función permite observar gráficamente la interacción entre agentes (consumidores y productores) en un mercado competitivo, facilitando el análisis visual de la eficiencia del equilibrio.

![Equilibrio](imgs/v0.1.0_(1).png)

#### 6. ```surplusGraph(oferta, demanda)```

```python
from oikos.graphs import surplusGraph

surplusGraph(oferta, demanda)
```

**Representación económica:**
- Excedente del Consumidor ($EC$): Representa el ahorro acumulado de los agentes cuya valoración subjetiva (disposición a pagar) es superior al precio de mercado ($P^*$). Es la medida del beneficio neto del consumidor.

- Excedente del Productor ($EP$): Refleja la renta económica de los productores cuyos costos marginales son inferiores al precio de venta. Representa la ganancia monetaria por encima del costo de producción.

Visualiza de forma simple:
![Excendentes](imgs/v0.1.0_(2).png)

### Documentación
Se agregaron instrucciones de instalación, tutoriales, ejemplos y referencias de API más claras.