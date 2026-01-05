# Changelog

Esta página contiene una lista de los cambios realizados entre versiones. 

---
## **v0.2.1**
**Fecha:** 03 de enero, 2026  

Esta es una versión de mantenimiento lanzada para corregir un error crítico en la API de salida que impedía el despliegue correcto de resultados en la terminal y entornos interactivos.

### Correcciones
    * **Exportación y Renderizado**
        * Se resolvió un conflicto de nombres en `ok.write` donde la función se importaba incorrectamente como `show`.
        * Restauración de la compatibilidad total con el motor de renderizado para visualización de equilibrios y multiplicadores.
    * **Estabilidad del Sistema**
        * Corrección de la persistencia de datos en la salida de consola para Jupyter Notebooks y terminales estándar.

### De interés para desarrolladores
* Ajuste en el espacio de nombres (namespace) del módulo de ```utils```para asegurar la consistencia con la documentación de la v0.2.0.

---
## v0.2.0
**Fecha:** 03 de enero, 2026

Esta versión representa un salto significativo desde la validación de concepto hacia una herramienta de modelado técnica robusta. Se introduce el paradigma de **Programación Orientada a Objetos (POO)**, soporte para ecuaciones no lineales y el primer motor de **Macroeconomía (IS-LM)**.

### Nuevas funciones
    * **Análisis Macroeconómico**
        * Implementación del modelo **IS-LM** para equilibrio simultáneo en mercados de bienes y dinero.
        * Adición de un motor de cálculo de multiplicadores fiscales y monetarios automáticos.
        * Soporte para determinación de nivel de ingreso ($Y^*$) y tasa de interés ($r^*$) de equilibrio.
    * **Motor Microeconómico Avanzado**
        * Transición a clases globales: `Demand`, `Supply` e `ISLM`.
        * Soporte para **funciones no lineales** y ecuaciones hiperbólicas mediante procesamiento de *strings*.
        * Nuevo sistema de interpretación semántica de **elasticidades** (`getPriceInterpretation`).
    * **Sintaxis y Lógica**
        * Implementación de entrada de ecuaciones mediante **Raw Strings** (`r"..."`) para mayor flexibilidad.
        * Resolución automática de variables despejadas tanto en $P$ como en $Q$.

### Documentación
    * Adición de ejemplos de implementación para modelos de economía cerrada.
    * Guía detallada sobre el uso de variables reservadas en macroeconomía ($Y, r, T$).
    * Actualización de la referencia de API para reflejar el nuevo paradigma de clases.

### Cambios importantes
    * **Migración a Clases (POO):** Las funciones globales de la v0.1.0 han sido depreciadas. Ahora toda la lógica se encapsula en objetos (ej. `ok.Demand`).
    * **Sintaxis de Ecuaciones:** Es obligatorio el uso de *Raw Strings* para definir curvas, permitiendo al motor realizar despejes automáticos.
    * **Redefinición de `equilibrium()`:** El método ahora requiere parámetros nombrados y detecta automáticamente el contexto (Micro o Macro).

### De interés para desarrolladores
* Implementación de un motor de parseo de ecuaciones para soportar pendientes variables.
* Despliegue de variables reservadas vinculadas a la instancia del modelo para evitar colisiones de nombres.

### Otros cambios
    * Optimización del comando `ok.write()` para visualización de resultados complejos.

---
## **v0.1.0** 

**Fecha:** 
02 de enero, 2025

Esta es la versión inicial de **oikos**, una librería de Python diseñada para modelar y visualizar principios microeconómicos. El enfoque de esta versión es validar la lógica central de mercados lineales de oferta y demanda.

### Funciones

* **Motor de Mercado**
    * Implementación de las clases `Supply` y `Demand` para modelado lineal.
    * Adición de la función `equilibrium` para calcular el precio y la cantidad de equilibrio.
    * Implementación del método `.quantity(P)` para consultas puntuales de cantidad según el precio.
* **Sistema de Gráficos**
    * Adición de `marketGraph` para la visualización básica del equilibrio de mercado.
    * Implementación de `surplusGraph` para renderizar las áreas de excedente del consumidor y del productor.
* **Arquitectura Core**
    * Sistema de importación unificado mediante `oikos.microeconomics.market`.
    * Calibración manual de parámetros para variables exógenas.

### Documentación
    * Adición de instrucciones de instalación y ejemplos básicos de uso.
    * Implementación de soporte para notación $\LaTeX$ en la documentación económica.
    * Adición de una referencia de API completa para las funciones principales.

### De interés para desarrolladores
    * Estructura inicial del proyecto diseñada para el modelado experimental de baja fidelidad.
    * Lógica integrada entre el cálculo económico y el renderizado con Matplotlib.

### Otros cambios
    * Configuración inicial del repositorio y licencias.