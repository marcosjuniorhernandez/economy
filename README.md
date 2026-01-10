# Oikos

[![pypi version](https://img.shields.io/pypi/v/oikos?logo=pypi)](https://pypi.org/project/oikos/)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)
[![docs](https://readthedocs.org/projects/oikos/badge/?version=latest)](https://oikos.readthedocs.io/en/latest/manual/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Oikos** es una biblioteca Python diseñada para estudiantes, economistas y desarrolladores interesados en el análisis económico y la modelización de la teoría económica básica.

Aprovechando el cálculo simbólico, **oikos** permite resolver problemas de micro y macroeconomía tanto numérica como algebraicamente, facilitando el aprendizaje y la enseñanza de conceptos económicos fundamentales.

## Filosofía

En un mundo lleno de librerías económicas complejas y orientadas exclusivamente a la estadística avanzada, **oikos** nace con una misión diferente: **hacer que la teoría económica sea tangible, visual y sencilla.**

### Principios fundamentales

1. **Economía para Humanos**: No necesitas ser un experto en Python para modelar. Si puedes escribir la ecuación en un papel, puedes usar oikos.

2. **Fidelidad Académica**: Usamos la notación que encuentras en tus libros: α, β, γ, λ. El código debe leerse como un libro de texto.

3. **De la Micro a la Macro**: Un solo ecosistema para entender desde el excedente de un consumidor hasta el equilibrio general de una nación.

4. **Intuición sobre Datos**: Antes de correr regresiones, hay que entender los desplazamientos. oikos es tu tablero digital para experimentar con la teoría.

## Características principales

- **Resolución simbólica**: Impulsada por `SymPy` para resolver ecuaciones de equilibrio sin derivación manual
- **Microeconomía**: Calcula el excedente del consumidor/productor, las elasticidades y el equilibrio del mercado
- **Macroeconomía**: Modelos multiplicadores, marco IS-LM y análisis agregado
- **Teoría del Consumidor**: Optimización de utilidad, curvas de indiferencia y demandas hicksianas/marshallianas
- **Comercio Internacional**: Modelos ricardianos, ventajas comparativas, fronteras de posibilidades de producción
- **Visualización**: Gráficos profesionales listos para presentaciones académicas
- **Documentación matemática**: Compatibilidad total con LaTeX en nuestra documentación web oficial

## Instalación

### Desde PyPI (recomendado)

```bash
pip install oikos
```

### Desde el código fuente

```bash
git clone https://github.com/marcosjuniorhernandez/economy.git
cd economy
pip install -e .
```

### En Google Colab

```python
!pip install oikos
from oikos import *
```

### En Jupyter Notebook

```bash
# En una celda de código
!pip install oikos
```

Luego reinicia el kernel e importa:

```python
from oikos import *
```

### Requisitos

- Python 3.8 o superior
- Se recomienda el uso de cuadernos como Jupyter Notebook o JupyterLab

### Dependencias

oikos instala automáticamente:
- `numpy` - Cálculos numéricos
- `sympy` - Álgebra simbólica
- `scipy` - Optimización científica
- `latex2sympy2` - Parser LaTeX
- `matplotlib` - Gráficos
- `ipython` - Visualización mejorada
- `rich` - Tablas y salidas formateadas

## Ejemplo rápido

```python
from oikos import *

# Crear funciones de demanda y oferta
demanda = Demanda("Q = 100 - 2P")
oferta = Oferta("Q = -20 + 3P")

# Calcular el equilibrio
eq = equilibrio(oferta, demanda)
print(eq)  # {'P*': 24.0, 'Q*': 52.0}

# Calcular excedentes
exc = excedentes(oferta, demanda)
print(f"Excedente del Consumidor: {exc['EC']}")
print(f"Excedente del Productor: {exc['EP']}")
print(f"Excedente Social: {exc['ES']}")

# Graficar
demanda.graficar()
```

## Documentación

La documentación completa está disponible en:

[https://oikos.readthedocs.io/en/latest/manual/](https://oikos.readthedocs.io/en/latest/manual/)

Incluye:
- Guía de instalación
- Tutorial paso a paso
- Ejemplos completos de microeconomía
- Ejemplos completos de macroeconomía
- Referencia de API
- FAQ

## Licencia

Este software está licenciado bajo la [Licencia MIT](LICENSE).

Copyright (c) 2026 Marcos Junior Hernández-Moreno

Se concede permiso, de forma gratuita, a cualquier persona que obtenga una copia de este software y de los archivos de documentación asociados, para tratar el software sin restricción, incluyendo sin limitación los derechos de uso, copia, modificación, fusión, publicación, distribución, sublicencia y/o venta de copias del software.

## Contribuciones

¡Las contribuciones son bienvenidas! Si deseas contribuir a oikos:

- **Sugerencias**: Envía tus ideas y sugerencias
- **Correcciones**: Reporta bugs o errores en el código
- **Mejoras**: Propón nuevas características

Por favor, envía tus contribuciones al correo **iam.marcoshernandez@gmail.com** con el asunto: **OIKOS**

Para más detalles, consulta la [guía de contribución](https://oikos.readthedocs.io/en/latest/contributing/).

## Citación

Si usas oikos en trabajos académicos, por favor cita:

```
Marcos Junior Hernández-Moreno (2026). Oikos: Biblioteca para modelos económicos en Python.
Versión 0.3.0. https://github.com/marcosjuniorhernandez/economy
```

BibTeX:
```bibtex
@software{oikos2026,
  author = {Marcos Junior Hernández-Moreno},
  title = {Oikos: Biblioteca para modelos económicos en Python},
  year = {2026},
  version = {0.3.0},
  url = {https://github.com/marcosjuniorhernandez/economy}
}
```

## Soporte

- **Documentación**: [https://oikos.readthedocs.io/](https://oikos.readthedocs.io/)
- **Repositorio**: [https://github.com/marcosjuniorhernandez/economy](https://github.com/marcosjuniorhernandez/economy)
- **PyPI**: [https://pypi.org/project/oikos/](https://pypi.org/project/oikos/)
- **Email**: iam.marcoshernandez@gmail.com

---

Copyright (c) 2026 **Marcos Junior Hernández-Moreno** [![ORCID](https://img.shields.io/badge/ORCID-0000--0001--6109--6358-green?logo=orcid&logoColor=white)](https://orcid.org/0000-0001-6109-6358)
