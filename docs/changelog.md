# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [0.2.1] - 2026-01-03

### Corregido
- **Exportación y renderizado**: Conflicto de nombres en `ok.write()` que se importaba incorrectamente como `show`, causando errores en la visualización de resultados
- **Compatibilidad de salida**: Restaurada la compatibilidad completa con el motor de renderizado para equilibrios y multiplicadores
- **Persistencia de datos**: Corregida la salida en consola para Jupyter Notebooks y terminales estándar
- **Namespace del módulo**: Ajustado el espacio de nombres de `utils` para consistencia con la documentación v0.2.0

---

## [0.2.0] - 2026-01-03

Versión mayor que introduce **Programación Orientada a Objetos**, soporte para ecuaciones no lineales y análisis macroeconómico.

### Añadido

#### Macroeconomía
- **Modelo IS-LM** para equilibrio simultáneo en mercados de bienes y dinero
- Cálculo automático de multiplicadores fiscales y monetarios
- Determinación de nivel de ingreso de equilibrio ($Y^*$) y tasa de interés de equilibrio ($r^*$)
- Clase `ISLM` con variables reservadas (`output`, `interestRate`, `govermentSpending`)

#### Microeconomía Avanzada
- **Clases globales**: `Demand`, `Supply` e `ISLM` reemplazan las funciones globales
- **Ecuaciones no lineales**: Soporte para funciones hiperbólicas y curvas complejas
- **Interpretación semántica**: Método `getPriceInterpretation()` para análisis de elasticidades
- **Motor de parseo**: Procesamiento automático de ecuaciones mediante Raw Strings (`r"..."`)
- **Resolución flexible**: Detección automática de variables despejadas en $P$ o $Q$

#### Documentación
- Ejemplos completos de modelos de economía cerrada
- Guía de uso de variables reservadas en macroeconomía
- Referencia de API actualizada con paradigma POO
- Ejemplos de implementación para ecuaciones no lineales

### Cambiado
- **[BREAKING]** Migración completa a Programación Orientada a Objetos
  - Las funciones globales de v0.1.0 están **depreciadas**
  - Toda la lógica ahora se encapsula en clases
  - Ejemplo: `ok.Demand(r"Q = 100 - 2P")` en lugar de funciones independientes
- **[BREAKING]** Sintaxis de ecuaciones requiere Raw Strings obligatoriamente
- **[BREAKING]** Método `equilibrium()` rediseñado con parámetros nombrados y detección automática de contexto (Micro/Macro)

### Mejorado
- Optimización de `ok.write()` para visualización de resultados complejos
- Motor de parseo permite pendientes variables y ecuaciones dinámicas
- Sistema de variables reservadas evita colisiones de nombres en modelos

---

## [0.1.0] - 2025-01-02

Lanzamiento inicial de **oikos** - Validación de concepto para modelado microeconómico.

### Añadido

#### Motor de Mercado
- Clases `Supply` y `Demand` para modelado lineal básico
- Función `equilibrium()` para cálculo de precio y cantidad de equilibrio
- Método `.quantity(P)` para consultas puntuales

#### Visualización
- Función `marketGraph()` para gráficos de equilibrio de mercado
- Función `surplusGraph()` para renderizar excedentes del consumidor y productor
- Integración con Matplotlib para renderizado

#### Infraestructura
- Sistema de importación unificado mediante `oikos.microeconomics.market`
- Estructura modular del proyecto

#### Documentación
- Guía de instalación y configuración
- Ejemplos básicos de uso
- Referencia completa de API
- Configuración de repositorio y licencias

---

## Leyenda de Tipos de Cambio

- **Añadido**: Para funcionalidades nuevas
- **Cambiado**: Para cambios en funcionalidades existentes
- **Depreciado**: Para funcionalidades que serán removidas
- **Removido**: Para funcionalidades removidas
- **Corregido**: Para corrección de bugs
- **Seguridad**: Para vulnerabilidades de seguridad
- **[BREAKING]**: Cambios que rompen compatibilidad hacia atrás

---
