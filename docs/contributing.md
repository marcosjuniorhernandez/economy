# Guía de Contribución

¡Gracias por tu interés en contribuir a **oikos**! Este documento proporciona las pautas para contribuir al proyecto.

## Formas de Contribuir

### 1. Reportar Bugs

Si encuentras un error en oikos, por favor repórtalo enviando un correo a:

**iam.marcoshernandez@gmail.com**

Con el asunto: **OIKOS**

Incluye en tu reporte:
- Descripción clara del problema
- Código para reproducir el error
- Versión de oikos que estás usando (`pip show oikos`)
- Versión de Python
- Sistema operativo

**Ejemplo de reporte:**

```
Asunto: OIKOS - Error al calcular equilibrio con demanda no lineal

Descripción:
Cuando intento calcular el equilibrio con una demanda de la forma Q = 100/P,
obtengo el siguiente error: [copiar error completo]

Código para reproducir:
```python
from oikos import *
demanda = Demanda("Q = 100/P")
oferta = Oferta("Q = -20 + 3P")
eq = equilibrio(oferta, demanda)
```

Versión de oikos: 0.3.0
Python: 3.10.5
OS: Windows 11
```

### 2. Sugerir Mejoras

¿Tienes ideas para nuevas funcionalidades o mejoras? Envíalas al mismo correo con:

- Descripción de la funcionalidad propuesta
- Caso de uso (¿para qué sirve?)
- Ejemplos de cómo se usaría

**Ejemplo de sugerencia:**

```
Asunto: OIKOS - Sugerencia: Agregar modelo de Cournot

Descripción:
Me gustaría que oikos incluyera el modelo de competencia de Cournot
para oligopolios, donde las empresas compiten en cantidades.

Caso de uso:
Útil para cursos de Organización Industrial y Microeconomía Intermedia.

Ejemplo de uso esperado:
```python
from oikos import Cournot
modelo = Cournot(n_empresas=2, demanda="P = 100 - Q", costo="C = 10q")
eq = modelo.equilibrio()
```
```

### 3. Corregir Documentación

Si encuentras errores tipográficos, gramaticales o conceptuales en la documentación,
también son bienvenidas las correcciones. Envía:

- Ubicación del error (página, sección)
- Error encontrado
- Corrección propuesta

### 4. Contribuir con Código

Si deseas contribuir con código (correcciones, mejoras, nuevas funcionalidades),
por favor sigue estas pautas:

#### Estilo de Código

**oikos** sigue convenciones específicas para mantener la coherencia:

##### Nomenclatura

- **Variables y parámetros**: `camelCase`
  ```python
  precioEquilibrio = 24.0
  cantidadDemandada = 100
  ```

- **Clases**: `CamelCase`
  ```python
  class Demanda:
      pass

  class ISLM:
      pass
  ```

- **Funciones**: `camelCase`
  ```python
  def equilibrio(oferta, demanda):
      pass

  def calcularExcedente():
      pass
  ```

- **Constantes**: `MAYUSCULAS_CON_GUION_BAJO`
  ```python
  ROJO = '#E74C3C'
  VERDE2 = '#2ECC71'
  ```

##### Idioma

- **Todo en español**: Variables, funciones, clases, comentarios
- **Evitar la letra ñ**: Por compatibilidad con editores y sistemas
- **Acentos permitidos**: En comentarios y docstrings

**Ejemplo:**

```python
# ✅ CORRECTO
def calcularElasticidadPrecio(precio, cantidad):
    """
    Calcula la elasticidad precio de la demanda.

    La elasticidad mide la sensibilidad de la cantidad demandada
    ante cambios en el precio.
    """
    elasticidad = (dQ / dP) * (precio / cantidad)
    return elasticidad

# ❌ INCORRECTO (inglés)
def calculate_price_elasticity(price, quantity):
    elasticity = (dQ / dP) * (price / quantity)
    return elasticity

# ❌ INCORRECTO (snake_case)
def calcular_elasticidad_precio(precio, cantidad):
    elasticidad = (dQ / dP) * (precio / cantidad)
    return elasticidad
```

##### Comentarios

Los comentarios deben explicar **la economía** detrás del código, no solo qué hace:

```python
# ✅ CORRECTO - Explica el concepto económico
# El excedente del consumidor es el área entre la curva de demanda
# y el precio de mercado. Representa el beneficio que obtienen los
# consumidores al pagar menos de lo que estarían dispuestos a pagar.
excedente_consumidor = integrate(demanda - precio_mercado, (Q, 0, Q_equilibrio))

# ❌ INCORRECTO - Solo describe el código
# Integrar la diferencia entre demanda y precio
excedente_consumidor = integrate(demanda - precio_mercado, (Q, 0, Q_equilibrio))
```

##### Estructura de Clases

```python
class NombreClase:
    """
    Descripción de la clase y su propósito económico.

    Parámetros
    ----------
    parametro1 : tipo
        Descripción del parámetro
    parametro2 : tipo
        Descripción del parámetro

    Ejemplos
    --------
    >>> from oikos import NombreClase
    >>> modelo = NombreClase(parametro1="valor")
    >>> resultado = modelo.metodo()
    """

    def __init__(self, parametro1, parametro2):
        self.parametro1 = parametro1
        self.parametro2 = parametro2

    def metodo(self):
        """
        Descripción breve del método.

        Returns
        -------
        tipo
            Descripción del valor retornado
        """
        # Implementación
        pass
```

#### Proceso de Contribución

1. **Contacto Inicial**: Envía un correo describiendo tu propuesta de contribución

2. **Discusión**: Se discutirá la propuesta para asegurar que se alinea con los objetivos del proyecto

3. **Implementación**: Desarrolla tu contribución siguiendo las pautas de estilo

4. **Envío**: Envía tu código al correo en un formato acordado (puede ser un parche, archivo .py, o repositorio fork)

5. **Revisión**: El código será revisado y se te proporcionará retroalimentación

6. **Integración**: Una vez aprobado, el código será integrado a la librería

## Prioridades del Proyecto

Actualmente, **oikos v0.3.1** se enfoca en:

### Alta Prioridad
- Corrección de bugs en funcionalidades existentes
- Mejoras en la documentación y ejemplos
- Optimización de rendimiento
- Compatibilidad con diferentes versiones de Python

### Prioridad Media
- Nuevos modelos macroeconómicos (OA-DA, Solow, etc.)
- Extensiones a teoría del consumidor
- Mejoras en visualización

### Baja Prioridad
- Modelos econométricos (eso es trabajo de statsmodels/scikit-learn)
- Análisis de series temporales avanzado
- Machine learning aplicado a economía

## Código de Conducta

Al contribuir a oikos, te comprometes a:

- Ser respetuoso con todos los colaboradores
- Proporcionar retroalimentación constructiva
- Aceptar críticas constructivas
- Priorizar el beneficio de la comunidad educativa
- Mantener un ambiente inclusivo y acogedor

## Reconocimiento

Todos los contribuidores serán reconocidos en:
- El archivo AUTHORS en el repositorio
- La sección de agradecimientos en la documentación
- Los mensajes de lanzamiento de nuevas versiones

## Licencia

Al contribuir a oikos, aceptas que tus contribuciones serán licenciadas bajo la misma licencia MIT que el proyecto.

## Contacto

Para cualquier pregunta sobre contribuciones:

**Email**: iam.marcoshernandez@gmail.com
**Asunto**: OIKOS - [Tu consulta]

---

¡Gracias por ayudar a hacer que la economía sea más accesible para todos!

---

Copyright (c) 2026 **Marcos Junior Hernández-Moreno** [![ORCID](https://img.shields.io/badge/ORCID-0000--0001--6109--6358-green?logo=orcid&logoColor=white)](https://orcid.org/0000-0001-6109-6358)
