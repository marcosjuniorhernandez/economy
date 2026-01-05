# Manual de referencia
Este manual de referencia detalla los módulos, funciones y variables incluidos en Manim, describiendo lo que son y lo que hacen. Para obtener una lista de los cambios desde la última versión, consulte el [Registro de cambios](changelog.md).

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