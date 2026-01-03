# Changelog

Todos los cambios relevantes de **oikos** se documentan en este archivo.

---

## v0.2.1 — Hotfix: Corrección de Exportación

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
## v0.1.0 — Versión inicial

**Fecha:**  02 Enero de 2025
Esta es la **primera versión pública de oikos**.  
El objetivo principal de esta versión fue **asegurar el nombre del proyecto** y validar un primer enfoque funcional para modelar conceptos básicos de microeconomía mediante Python.
La implementación fue deliberadamente simple y experimental, sin una arquitectura madura ni una API definitiva.
---

### Alcance general
- Modelo único de **oferta y demanda lineal**.
- Parámetros ingresados manualmente.
- Importaciones poco intuitivas comparadas con versiones posteriores.
- Sin separación clara entre lógica económica y visualización.
- Enfoque exclusivo en microeconomía básica.

---
### Funciones disponibles

La versión **v0.1.0** incluía únicamente **5 funciones**, todas orientadas a representar un mercado competitivo simple.

#### 1. Oferta lineal
Define una función de oferta de la forma:

\[
Q_s = a + bP
\]

**Representación económica:**  
Modela el comportamiento de los productores, donde la cantidad ofrecida aumenta a medida que sube el precio.

---

#### 2. Demanda lineal
Define una función de demanda de la forma:

\[
Q_d = c - dP
\]

**Representación económica:**  
Modela el comportamiento de los consumidores, donde la cantidad demandada disminuye cuando el precio aumenta.

---

#### 3. Equilibrio de mercado
Calcula el punto donde:

\[
Q_s = Q_d
\]

Devuelve el **precio de equilibrio** y la **cantidad de equilibrio**.

**Representación económica:**  
Corresponde al estado del mercado donde no existen fuerzas internas que empujen el precio al alza o a la baja.

---

#### 4. ```marketGraph(oferta, demanda)```
Genera una visualización básica del mercado mostrando:

- Curva de oferta
- Curva de demanda
- Punto de equilibrio

**Representación económica:**  
Permite observar gráficamente la interacción entre consumidores y productores en un mercado competitivo.
![Excendentes](docs/imgs/v0.1.0 (1).png)

---

#### 5. ```surplusGraph(oferta, demanda)

```python
surplusGraph(oferta, demanda)
```

Visualiza de forma simple:
![Excendentes](docs/imgs/v0.1.0 (2).png)