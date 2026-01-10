# Changelog

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---
## [0.3.1] - 2026-01-10
Correción en el nombre del paquete de Oikos a oikos.

## [0.3.0] - 2026-01-10

Versión mayor que expande significativamente la librería con **Teoría del Consumidor** y **Comercio Internacional**, además de mejoras arquitectónicas profundas.

### Añadido

#### Arquitectura y Sistema de Tipos
- **Sistema de excepciones personalizado**: Jerarquía completa de excepciones (`ErrorOikos`, `ErrorValidacion`, `ErrorEquilibrio`, `ErrorParseador`, `ErrorGrafico`)
- **Clases base abstractas**: `FuncionEconomica`, `MercadoBase`, `ModeloEconomico` para garantizar consistencia en toda la API
- **Decoradores de documentación**: `@ayuda` y `@explicacion` para enriquecer clases y métodos con contexto económico
- **Sistema de validadores**: Funciones reutilizables (`validarPositivo`, `validarNoNegativo`, `validarRango`, `validarPropension`)
- **Dataclasses especializadas**: `BienEconomico` para representar productos con nombre y unidad

#### Teoría del Consumidor
- **Clase principal `Consumidor`**: Representa un agente económico que maximiza su utilidad sujeto a restricción presupuestaria
  - Métodos: `demandarOptima()`, `utilidadAlcanzada()`, `curvaIndiferencia()`, `restriccionPresupuestaria()`
  - Soporte para cambios en precios e ingreso: `cambiarPrecio()`, `cambiarIngreso()`
  - Análisis de tipos de bienes (normales vs inferiores)
  - Método `.graficar()` para visualización de restricción presupuestaria y curvas de indiferencia
- **Funciones de utilidad**: Clase base `FuncionUtilidad` con métodos para utilidad marginal, TMS y curvas de indiferencia
- **Funciones implementadas**: `CobbDouglas`, `SustitutosPerfectos`, `ComplementariosPerfectos`, `CuasiLineal`, `CES`, `StoneGeary`, `ConcavaRaiz`
- **Tipos de bienes**: `BienNeutral`, `BienMalo`, `PreferenciasSaciadas`
- **Restricción presupuestaria**: Clase `RestriccionPresupuestaria` con cálculo de recta y pendiente
- **Optimización del consumidor**: Clase `EleccionOptima` que resuelve maximización de utilidad sujeto a restricción
- **Curvas de indiferencia**: Clase `CurvaIndiferencia` para graficar niveles de utilidad constante

#### Comercio Internacional
- **Frontera de Posibilidades de Producción**: Clase `FPP` con cálculo de costo de oportunidad y ventaja comparativa
- **Modelo Ricardiano**: Clase `Ricardiano` para análisis de comercio con ventajas comparativas
- **Modelo de Factores Específicos**: Clase `FactoresEspecificos` para economías de dos sectores
- **Integración con Rich**: Tablas formateadas para comparación de países y ventajas
- **Análisis de términos de intercambio**: Cálculo automático de precios relativos en comercio

#### Visualización Avanzada
- **Sistema de canvas mejorado**: Clase `Lienzo` con soporte para cuadrantes cartesianos múltiples
- **Lienzo matricial**: Gráficos en grilla (matriz n×m) con `matriz=(filas, columnas)` y `alinearEjes`
- **Constantes de dirección**: `ARRIBA`, `ABAJO`, `IZQUIERDA`, `DERECHA` para anotaciones
- **Paleta expandida**: 17 colores predefinidos (agregados `AMARILLO2`, `AZUL2`, `ROJO2`, `CIAN`, `LIMA`, `CORAL`, `VIOLETA`)
- **EstiloGrafico**: Dataclass para personalización completa de parámetros visuales
- **Método `graficoRapido()`**: Wrapper para gráficos simples de una sola línea

#### Parser y Herramientas Simbólicas
- **Función `despejar()`**: Despeja variables de ecuaciones simbólicas
- **Función `extraerVariables()`**: Extrae todas las variables de una expresión
- **Mejoras en `translatex()`**: Manejo robusto de ecuaciones con múltiples variables y paréntesis
- **Función `escribir()`**: Renderizado LaTeX mejorado para ecuaciones y resultados

### Mejorado

#### Optimización de Rendimiento
- **Caching de expresiones simbólicas**: Las funciones de demanda/oferta cachean sus expresiones parseadas
- **Evaluación numérica lazy**: Uso de `lambdify` para evaluaciones rápidas repetidas
- **Validación temprana**: Los validadores lanzan excepciones específicas antes de cálculos costosos

#### Experiencia del Desarrollador
- **Type hints completos**: Anotaciones de tipo en todas las firmas de funciones para mejor IDE support
- **Docstrings en formato NumPy**: Documentación consistente con ejemplos y tipos de parámetros
- **Mensajes de error descriptivos**: Excepciones personalizadas con contexto económico
- **Namespace limpio**: `__all__` bien definido con 70+ símbolos exportados

#### API de Microeconomía
- **Método `.graficar()`**: Ahora disponible directamente en `Demanda` y `Oferta`
- **Cálculo de elasticidades**: Métodos `.elasticidadPrecio()` y `.interpretarElasticidad()`
- **Función `excedentes()`**: Cálculo robusto de EC, EP y ES con integración simbólica

### Cambiado

- **Requisito de Python**: Ahora requiere Python 3.8+ (anteriormente 3.7+)
- **Dependencia agregada**: `scipy` para optimización numérica en teoría del consumidor
- **Estructura de imports**: Reorganización de módulos (`oikos.microeconomia.consumidor`, `oikos.microeconomia.comercio`)
- **Firma de `Lienzo.__init__`**: Nuevos parámetros `matriz`, `dimensionMatriz`, `alinearEjes` para gráficos matriciales

### Depreciado

- Ninguna depreciación en esta versión (todas las APIs de v0.2.x siguen soportadas)

### Seguridad

- **Validación de entrada**: Todas las funciones públicas validan parámetros para prevenir valores no económicos
- **Manejo seguro de división por cero**: Guards en cálculos de elasticidades y costos de oportunidad
- **Sanitización de expresiones**: El parser rechaza código arbitrario, solo acepta expresiones matemáticas

---

## [0.2.1] - 2026-01-03

### Corregido
- **Exportación y renderizado**: Conflicto de nombres en `ok.escribir()` que se importaba incorrectamente como `show`, causando errores en la visualización de resultados
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
- Optimización de `ok.escribir()` para visualización de resultados complejos
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

Copyright (c) 2026 **Marcos Junior Hernández-Moreno** [![ORCID](https://img.shields.io/badge/ORCID-0000--0001--6109--6358-green?logo=orcid&logoColor=white)](https://orcid.org/0000-0001-6109-6358)
