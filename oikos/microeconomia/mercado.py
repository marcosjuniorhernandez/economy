"""
Módulo de mercado - Demanda, Oferta y Equilibrio.

Este módulo contiene las clases fundamentales para análisis de mercados:
- Demanda: Función de demanda del mercado
- Oferta: Función de oferta del mercado  
- equilibrio(): Calcula el punto donde se cruzan oferta y demanda
"""

from sympy import symbols, solve, diff, lambdify, integrate
from typing import Dict, Optional, Tuple
from ..nucleo.base import MercadoBase
from ..nucleo.excepciones import ErrorEquilibrio, ErrorValidacion
from ..utilidades.parseador import translatex
from ..utilidades.decoradores import ayuda, explicacion
from ..utilidades.validadores import validarPositivo, validarNoNegativo


@ayuda(
    descripcionEconomica="""
    La Demanda representa la relación entre el precio de un bien y la cantidad
    que los consumidores están dispuestos a comprar en un periodo determinado.
    
    Por la Ley de la Demanda, existe una relación inversa entre precio y cantidad:
    cuando el precio sube, la cantidad demandada baja (ceteris paribus).
    """,
    supuestos=[
        "Preferencias del consumidor constantes",
        "Ingreso del consumidor constante",
        "Precios de bienes relacionados constantes",
        "Expectativas de precio futuro constantes",
        "Número de compradores constante"
    ],
)

class Demanda:
    """
    Representa la función de demanda de un bien o servicio.
    
    La demanda puede expresarse como Q = f(P) o P = f(Q).
    
    Args:
        ecuacion: Ecuación de demanda en formato LaTeX
                 Ejemplos: "Q = 100 - 2P", "P = 50 - 0.5Q"
    
    Attributes:
        expresion: Expresión simbólica de SymPy
        P: Símbolo del precio
        Q: Símbolo de la cantidad
        
    Ejemplo:
        >>> # Demanda lineal simple
        >>> demanda = Demanda("Q = 100 - 2P")
        >>> 
        >>> # Calcular cantidad demandada a un precio
        >>> q = demanda.cantidad(precio=10)
        >>> print(q)  # 80
        >>>
        >>> # Calcular elasticidad precio
        >>> e = demanda.elasticidadPrecio(precio=10, cantidad=80)
        >>> print(e)  # -0.25 (inelástica)
    """
    
    def __init__(self, ecuacion: str):
        """
        Inicializa la función de demanda.
        
        Args:
            ecuacion: Ecuación en LaTeX (ej: "Q = 100 - 2P")
        """
        # Definimos los símbolos económicos
        self.P = symbols('P')  # Precio
        self.Q = symbols('Q')  # Cantidad
        
        # Parseamos la ecuación
        self.expresion = translatex(ecuacion)
        
        # Guardamos la ecuación original
        self.ecuacionOriginal = ecuacion
    
    @explicacion("Calcula la cantidad demandada dado un precio específico")
    def cantidad(self, precio: float) -> float:
        """
        Calcula la cantidad demandada a un precio dado.

        Args:
            precio: Precio del bien (debe ser positivo)

        Returns:
            Cantidad demandada

        Raises:
            ErrorValidacion: Si el precio es negativo o si la ecuación no tiene solución real
        """
        precio = validarPositivo(precio, "precio")

        # Despejamos Q en función de P
        solucion = solve(self.expresion, self.Q)

        if not solucion:
            raise ErrorValidacion("demanda", "No se pudo despejar la cantidad")

        # Sustituimos el precio
        cantidadExpresion = solucion[0]
        cantidadSimbolica = cantidadExpresion.subs(self.P, precio)

        # Forzar evaluación numérica y filtrar complejos
        from sympy import re, im, N
        cantidadSimbolica = N(cantidadSimbolica)

        # Verificar si tiene parte imaginaria
        parteImaginaria = im(cantidadSimbolica)
        if abs(float(parteImaginaria)) > 1e-10:
            raise ErrorValidacion(
                "demanda",
                f"La cantidad para P={precio} es un número complejo. "
                "Esto indica que la ecuación de demanda no es válida para este precio."
            )

        # Tomar solo la parte real
        cantidadValor = float(re(cantidadSimbolica))

        # La cantidad no puede ser negativa
        return max(0, cantidadValor)
    
    @explicacion("Calcula el precio dado una cantidad específica")
    def precio(self, cantidad: float) -> float:
        """
        Calcula el precio al que se demanda una cantidad específica.

        También conocido como "precio de reserva" o "disposición a pagar".

        Args:
            cantidad: Cantidad del bien (debe ser no negativa)

        Returns:
            Precio correspondiente

        Raises:
            ErrorValidacion: Si la cantidad es negativa o si la ecuación no tiene solución real
        """
        cantidad = validarNoNegativo(cantidad, "cantidad")

        # Despejamos P en función de Q
        solucion = solve(self.expresion, self.P)

        if not solucion:
            raise ErrorValidacion("demanda", "No se pudo despejar el precio")

        # Sustituimos la cantidad
        precioExpr = solucion[0]
        precioSimbolico = precioExpr.subs(self.Q, cantidad)

        # Forzar evaluación numérica y filtrar complejos
        from sympy import re, im, N
        precioSimbolico = N(precioSimbolico)

        # Verificar si tiene parte imaginaria
        parteImaginaria = im(precioSimbolico)
        if abs(float(parteImaginaria)) > 1e-10:
            raise ErrorValidacion(
                "demanda",
                f"El precio para Q={cantidad} es un número complejo. "
                "Esto indica que la ecuación de demanda no es válida para esta cantidad."
            )

        # Tomar solo la parte real
        precioValor = float(re(precioSimbolico))

        return max(0, precioValor)
    
    @explicacion("""
    Calcula la elasticidad precio de la demanda en un punto.
    
    La elasticidad mide el cambio porcentual en cantidad demandada
    ante un cambio del 1% en el precio:
    
    ε = (dQ/dP) × (P/Q)
    
    Interpretación:
    - |ε| > 1: Demanda elástica (sensible al precio)
    - |ε| < 1: Demanda inelástica (poco sensible al precio)
    - |ε| = 1: Elasticidad unitaria
    """)

    def elasticidadPrecio(self, precio: float, cantidad: float) -> float:
        """
        Calcula la elasticidad precio de la demanda.

        Args:
            precio: Precio en el punto de evaluación
            cantidad: Cantidad en el punto de evaluación

        Returns:
            Elasticidad precio (número negativo para demanda normal)

        Raises:
            ErrorValidacion: Si cantidad o precio son cero o negativos
        """
        precio = validarPositivo(precio, "precio")
        cantidad = validarPositivo(cantidad, "cantidad")

        # Despejamos Q como función de P
        solucionCantidad = solve(self.expresion, self.Q)

        if not solucionCantidad:
            raise ErrorValidacion("demanda", "No se pudo calcular elasticidad")

        cantidadExpresion = solucionCantidad[0]

        # Derivamos Q respecto a P
        derivada = diff(cantidadExpresion, self.P)

        # Evaluamos la derivada en el precio dado
        derivada_valor = float(derivada.subs(self.P, precio))

        # Validamos que cantidad no sea cero (ya validado por validarPositivo)
        # Calculamos elasticidad: (dQ/dP) × (P/Q)
        elasticidad = derivada_valor * (precio / cantidad)

        return elasticidad
    
    def interpretarElasticidad(self, precio: float, cantidad: float) -> str:
        """
        Interpreta la elasticidad precio de forma económica.
        
        Args:
            precio: Precio en el punto
            cantidad: Cantidad en el punto
            
        Returns:
            Interpretación textual de la elasticidad
        """
        e = self.elasticidadPrecio(precio, cantidad)
        abs_e = abs(e)
        
        if abs_e > 1:
            tipo = "ELÁSTICA"
            explicacion = "Los consumidores son muy sensibles al precio"
        elif abs_e < 1:
            tipo = "INELÁSTICA"
            explicacion = "Los consumidores son poco sensibles al precio"
        else:
            tipo = "UNITARIA"
            explicacion = "La sensibilidad al precio es proporcional"
        
        return f"Demanda {tipo} (ε = {e:.2f}): {explicacion}"
    
    def graficar(self, rango: tuple = None, color: str = None, etiqueta: str = None):
        """
        Grafica la curva de demanda.

        Args:
            rango: (Q_min, Q_max) rango de cantidades a graficar
            color: Color de la curva
            etiqueta: Etiqueta para la leyenda

        Returns:
            Lienzo con la gráfica

        Ejemplo:
            >>> demanda = Demanda("Q = 100 - 2P")
            >>> demanda.graficar()
        """
        from ..utilidades.visuales import Lienzo, ROJO

        lienzo = Lienzo()
        lienzo.configurarEtiquetas(
            etiquetaX="Cantidad (Q)",
            etiquetaY="Precio (P)",
            titulo="Curva de Demanda"
        )
        lienzo.agregar(
            self,
            etiqueta=etiqueta or "Demanda",
            color=color or ROJO,
            rangoPersonalizado=rango
        )
        lienzo.graficar()
        return lienzo

    def __repr__(self):
        return f"Demanda('{self.ecuacionOriginal}')"

    def __str__(self):
        from sympy import latex
        return f"Demanda: {latex(self.expresion)}"


@ayuda(
    descripcionEconomica="""
    La Oferta representa la relación entre el precio de un bien y la cantidad
    que los productores están dispuestos a vender en un periodo determinado.
    
    Por la Ley de la Oferta, existe una relación directa entre precio y cantidad:
    cuando el precio sube, la cantidad ofrecida también sube (ceteris paribus).
    """,
    supuestos=[
        "Tecnología de producción constante",
        "Precios de los insumos constantes",
        "Precios de bienes relacionados constantes",
        "Expectativas de precio futuro constantes",
        "Número de vendedores constante"
    ],
)

class Oferta:
    """
    Representa la función de oferta de un bien o servicio.
    
    La oferta puede expresarse como Q = f(P) o P = f(Q).
    
    Args:
        ecuacion: Ecuación de oferta en formato LaTeX
                 Ejemplos: "Q = -20 + 3P", "P = 10 + 0.5Q"
    
    Attributes:
        expresion: Expresión simbólica de SymPy
        P: Símbolo del precio
        Q: Símbolo de la cantidad
        
    Ejemplo:
        >>> # Oferta lineal simple
        >>> oferta = Oferta("Q = -20 + 3P")
        >>> 
        >>> # Calcular cantidad ofrecida a un precio
        >>> q = oferta.cantidad(precio=15)
        >>> print(q)  # 25
        >>>
        >>> # Calcular elasticidad precio
        >>> e = oferta.elasticidadPrecio(precio=15, cantidad=25)
        >>> print(e)  # 1.8 (elástica)
    """
    
    def __init__(self, ecuacion: str):
        """
        Inicializa la función de oferta.
        
        Args:
            ecuacion: Ecuación en LaTeX (ej: "Q = -20 + 3P")
        """
        # Definimos los símbolos económicos
        self.P = symbols('P')  # Precio
        self.Q = symbols('Q')  # Cantidad
        
        # Parseamos la ecuación
        self.expresion = translatex(ecuacion)
        
        # Guardamos la ecuación original
        self.ecuacionOriginal = ecuacion
    
    @explicacion("Calcula la cantidad ofrecida dado un precio específico")
    def cantidad(self, precio: float) -> float:
        """
        Calcula la cantidad ofrecida a un precio dado.

        Args:
            precio: Precio del bien (debe ser positivo)

        Returns:
            Cantidad ofrecida

        Raises:
            ErrorValidacion: Si el precio es negativo o si la ecuación no tiene solución real
        """
        precio = validarPositivo(precio, "precio")

        # Despejamos Q en función de P
        solucion = solve(self.expresion, self.Q)

        if not solucion:
            raise ErrorValidacion("oferta", "No se pudo despejar la cantidad")

        # Sustituimos el precio
        cantidadExpresion = solucion[0]
        cantidadSimbolica = cantidadExpresion.subs(self.P, precio)

        # Forzar evaluación numérica y filtrar complejos
        from sympy import re, im, N
        cantidadSimbolica = N(cantidadSimbolica)

        # Verificar si tiene parte imaginaria
        parteImaginaria = im(cantidadSimbolica)
        if abs(float(parteImaginaria)) > 1e-10:
            raise ErrorValidacion(
                "oferta",
                f"La cantidad para P={precio} es un número complejo. "
                "Esto indica que la ecuación de oferta no es válida para este precio."
            )

        # Tomar solo la parte real
        cantidadValor = float(re(cantidadSimbolica))

        # La cantidad no puede ser negativa
        return max(0, cantidadValor)
    
    @explicacion("Calcula el precio dado una cantidad específica")
    def precio(self, cantidad: float) -> float:
        """
        Calcula el precio al que se ofrece una cantidad específica.

        También conocido como "precio mínimo de oferta" o "costo marginal".

        Args:
            cantidad: Cantidad del bien (debe ser no negativa)

        Returns:
            Precio correspondiente

        Raises:
            ErrorValidacion: Si la cantidad es negativa o si la ecuación no tiene solución real
        """
        cantidad = validarNoNegativo(cantidad, "cantidad")

        # Despejamos P en función de Q
        solucion = solve(self.expresion, self.P)

        if not solucion:
            raise ErrorValidacion("oferta", "No se pudo despejar el precio")

        # Sustituimos la cantidad
        precioExpr = solucion[0]
        precioSimbolico = precioExpr.subs(self.Q, cantidad)

        # Forzar evaluación numérica y filtrar complejos
        from sympy import re, im, N
        precioSimbolico = N(precioSimbolico)

        # Verificar si tiene parte imaginaria
        parteImaginaria = im(precioSimbolico)
        if abs(float(parteImaginaria)) > 1e-10:
            raise ErrorValidacion(
                "oferta",
                f"El precio para Q={cantidad} es un número complejo. "
                "Esto indica que la ecuación de oferta no es válida para esta cantidad."
            )

        # Tomar solo la parte real
        precioValor = float(re(precioSimbolico))

        return max(0, precioValor)
    
    @explicacion("""
    Calcula la elasticidad precio de la oferta en un punto.
    
    La elasticidad mide el cambio porcentual en cantidad ofrecida
    ante un cambio del 1% en el precio:
    
    η = (dQ/dP) × (P/Q)
    
    Interpretación:
    - η > 1: Oferta elástica (productores responden fácilmente)
    - η < 1: Oferta inelástica (productores responden difícilmente)
    - η = 1: Elasticidad unitaria
    """)

    def elasticidadPrecio(self, precio: float, cantidad: float) -> float:
        """
        Calcula la elasticidad precio de la oferta.

        Args:
            precio: Precio en el punto de evaluación
            cantidad: Cantidad en el punto de evaluación

        Returns:
            Elasticidad precio (número positivo para oferta normal)

        Raises:
            ErrorValidacion: Si cantidad o precio son cero o negativos
        """
        precio = validarPositivo(precio, "precio")
        cantidad = validarPositivo(cantidad, "cantidad")

        # Despejamos Q como función de P
        solucionCantidad = solve(self.expresion, self.Q)

        if not solucionCantidad:
            raise ErrorValidacion("oferta", "No se pudo calcular elasticidad")

        cantidadExpresion = solucionCantidad[0]

        # Derivamos Q respecto a P
        derivada = diff(cantidadExpresion, self.P)

        # Evaluamos la derivada en el precio dado
        derivada_valor = float(derivada.subs(self.P, precio))

        # Validamos que cantidad no sea cero (ya validado por validarPositivo)
        # Calculamos elasticidad: (dQ/dP) × (P/Q)
        elasticidad = derivada_valor * (precio / cantidad)

        return elasticidad
    
    def interpretarElasticidad(self, precio: float, cantidad: float) -> str:
        """
        Interpreta la elasticidad precio de forma económica.
        
        Args:
            precio: Precio en el punto
            cantidad: Cantidad en el punto
            
        Returns:
            Interpretación textual de la elasticidad
        """
        n = self.elasticidadPrecio(precio, cantidad)
        
        if n > 1:
            tipo = "ELÁSTICA"
            explicacion = "Los productores pueden aumentar fácilmente la producción"
        elif n < 1:
            tipo = "INELÁSTICA"
            explicacion = "Los productores tienen dificultad para aumentar la producción"
        else:
            tipo = "UNITARIA"
            explicacion = "La respuesta de la producción es proporcional al precio"
        
        return f"Oferta {tipo} (η = {n:.2f}): {explicacion}"
    
    def graficar(self, rango: tuple = None, color: str = None, etiqueta: str = None):
        """
        Grafica la curva de oferta.

        Args:
            rango: (Q_min, Q_max) rango de cantidades a graficar
            color: Color de la curva
            etiqueta: Etiqueta para la leyenda

        Returns:
            Lienzo con la gráfica

        Ejemplo:
            >>> oferta = Oferta("Q = -20 + 3P")
            >>> oferta.graficar()
        """
        from ..utilidades.visuales import Lienzo, VERDE2

        lienzo = Lienzo()
        lienzo.configurarEtiquetas(
            etiquetaX="Cantidad (Q)",
            etiquetaY="Precio (P)",
            titulo="Curva de Oferta"
        )
        lienzo.agregar(
            self,
            etiqueta=etiqueta or "Oferta",
            color=color or VERDE2,
            rangoPersonalizado=rango
        )
        lienzo.graficar()
        return lienzo

    def __repr__(self):
        return f"Oferta('{self.ecuacionOriginal}')"

    def __str__(self):
        from sympy import latex
        return f"Oferta: {latex(self.expresion)}"


@ayuda(
    descripcionEconomica="""
    El Equilibrio de Mercado ocurre cuando la cantidad demandada iguala
    la cantidad ofrecida. En este punto:
    
    - No hay exceso de demanda (escasez)
    - No hay exceso de oferta (excedente)
    - El precio no tiene presión para cambiar
    - Se maximiza el bienestar social (bajo competencia perfecta)
    """,
    supuestos=[
        "Mercado competitivo (muchos compradores y vendedores)",
        "Información perfecta",
        "Libre entrada y salida",
        "Producto homogéneo",
        "Precio flexible"
    ],
)

def equilibrio(oferta: Oferta, demanda: Demanda) -> Dict[str, float]:
    """
    Calcula el equilibrio de mercado donde se cruzan oferta y demanda.
    
    El equilibrio se encuentra resolviendo el sistema:
        Q_d = Q_s (cantidad demandada = cantidad ofrecida)
        P_d = P_s (precio de demanda = precio de oferta)
    
    Args:
        oferta: Función de oferta del mercado
        demanda: Función de demanda del mercado
        
    Returns:
        Diccionario con:
            - 'P*': Precio de equilibrio
            - 'Q*': Cantidad de equilibrio
            
    Raises:
        ErrorEquilibrio: Si no existe equilibrio o no es único
        
    Ejemplo:
        >>> demanda = Demanda("Q = 100 - 2P")
        >>> oferta = Oferta("Q = -20 + 3P")
        >>> eq = equilibrio(oferta, demanda)
        >>> print(eq)
        >>> # {'P*': 24.0, 'Q*': 52.0}
        >>>
        >>> # Mostrar resultados bonitos
        >>> from oikos.utilidades import escribir
        >>> escribir(eq, "Equilibrio de Mercado")
    """
    # Extraemos las expresiones de oferta y demanda
    expresion_oferta = oferta.expresion
    expresion_demanda = demanda.expresion
    
    # Resolvemos el sistema de ecuaciones
    P, Q = symbols('P Q')
    
    try:
        soluciones = solve(
            [expresion_oferta, expresion_demanda],
            [Q, P],
            dict=True
        )
    except Exception as e:
        raise ErrorEquilibrio(f"No se pudo resolver el sistema: {str(e)}")
    
    if not soluciones:
        raise ErrorEquilibrio(
            "No existe equilibrio para este mercado. "
            "Verifica que las curvas se crucen."
        )

    # CORRECCIÓN: Filtrar soluciones con valores positivos (Q > 0 y P > 0)
    # En economía, solo nos interesan equilibrios con cantidades y precios positivos
    soluciones_validas = []
    for sol in soluciones:
        from sympy import re, im, N
        q_val = N(sol[Q])
        p_val = N(sol[P])

        # Verificar que sean reales (no complejos)
        if abs(float(im(q_val))) < 1e-10 and abs(float(im(p_val))) < 1e-10:
            q_real = float(re(q_val))
            p_real = float(re(p_val))

            # Solo considerar soluciones con P > 0 y Q > 0
            if q_real > 0 and p_real > 0:
                soluciones_validas.append(sol)

    if len(soluciones_validas) == 0:
        raise ErrorEquilibrio(
            "No existe equilibrio con valores positivos para este mercado. "
            "Verifica que las curvas se crucen en el primer cuadrante (P > 0, Q > 0)."
        )

    if len(soluciones_validas) > 1:
        raise ErrorEquilibrio(
            f"Existen {len(soluciones_validas)} equilibrios con valores positivos. "
            "Este caso requiere análisis adicional."
        )

    # Usar la única solución válida
    solucion = soluciones_validas[0]

    # Verificar que las soluciones sean números reales
    cantidad_sym = solucion[Q]
    precio_sym = solucion[P]

    # Forzar evaluación numérica
    from sympy import re, im, N
    cantidad_sym = N(cantidad_sym)
    precio_sym = N(precio_sym)

    # Verificar si tienen parte imaginaria
    parte_imaginaria_q = im(cantidad_sym)
    parte_imaginaria_p = im(precio_sym)

    if abs(float(parte_imaginaria_q)) > 1e-10:
        raise ErrorEquilibrio(
            "El equilibrio calculado tiene una cantidad compleja. "
            "Las curvas de oferta y demanda no se cruzan en un punto real. "
            "Verifica las ecuaciones."
        )

    if abs(float(parte_imaginaria_p)) > 1e-10:
        raise ErrorEquilibrio(
            "El equilibrio calculado tiene un precio complejo. "
            "Las curvas de oferta y demanda no se cruzan en un punto real. "
            "Verifica las ecuaciones."
        )

    # Tomar solo las partes reales
    cantidadEquilibrio = float(re(cantidad_sym))
    precioEquilibrio = float(re(precio_sym))

    # Validamos que sean valores positivos
    if cantidadEquilibrio < 0 or precioEquilibrio < 0:
        raise ErrorEquilibrio(
            f"El equilibrio calculado tiene valores negativos: "
            f"P* = {precioEquilibrio:.4f}, Q* = {cantidadEquilibrio:.4f}. "
            f"Verifica las ecuaciones de oferta y demanda."
        )

    return {
        'P*': precioEquilibrio,
        'Q*': cantidadEquilibrio
    }


def excedentes(oferta: Oferta,
               demanda: Demanda,
               precio: Optional[float] = None,
               cantidad: Optional[float] = None) -> Dict[str, float]:
    """
    Calcula los excedentes del consumidor y productor en equilibrio libre.

    El excedente del consumidor (EC) es el área entre la curva de demanda
    y el precio de mercado. El excedente del productor (EP) es el área entre
    el precio de mercado y la curva de oferta.

    Si no se especifica precio/cantidad, usa el equilibrio de libre mercado.

    IMPORTANTE: Esta función calcula excedentes para mercados libres.
    Para calcular excedentes con intervenciones del gobierno (impuestos,
    subsidios, precios máximos, precios mínimos), debes:
    1. Calcular el nuevo equilibrio con la intervención
    2. Pasar el nuevo precio y cantidad a esta función
    3. Calcular también la pérdida irrecuperable de eficiencia (deadweight loss)

    Args:
        oferta: Función de oferta
        demanda: Función de demanda
        precio: Precio al cual calcular (None = equilibrio libre)
        cantidad: Cantidad al cual calcular (None = equilibrio libre)

    Returns:
        Diccionario con:
            - 'EC': Excedente del consumidor
            - 'EP': Excedente del productor
            - 'ES': Excedente social (EC + EP)
            - 'P': Precio usado
            - 'Q': Cantidad usada

    Ejemplo:
        >>> # Excedentes en equilibrio libre
        >>> demanda = Demanda("Q = 100 - 2P")
        >>> oferta = Oferta("Q = -20 + 3P")
        >>> exc = excedentes(oferta, demanda)
        >>> print(f"EC: {exc['EC']}, EP: {exc['EP']}")
        >>>
        >>> # Excedentes con precio máximo
        >>> precio_maximo = 20
        >>> cantidad_con_control = oferta.cantidad(precio_maximo)
        >>> exc_control = excedentes(oferta, demanda, precio_maximo, cantidad_con_control)
        >>> # Para calcular pérdida irrecuperable, compara exc_control['ES'] con exc['ES']
    """
    # Si no se especifican, usar equilibrio
    if precio is None or cantidad is None:
        eq = equilibrio(oferta, demanda)
        precio = eq['P*']
        cantidad = eq['Q*']

    P, Q = symbols('P Q')

    try:
        # Despejamos P en función de Q para ambas curvas
        # Demanda: P_d(Q)
        solucion_demanda = solve(demanda.expresion, P)
        if not solucion_demanda:
            raise ErrorValidacion("demanda", "No se pudo despejar P de la demanda")
        precio_demanda = solucion_demanda[0]

        # Oferta: P_s(Q)
        solucion_oferta = solve(oferta.expresion, P)
        if not solucion_oferta:
            raise ErrorValidacion("oferta", "No se pudo despejar P de la oferta")
        precio_oferta = solucion_oferta[0]

        # Excedente del Consumidor: ∫[0 to Q*] (P_d(Q) - P*) dQ
        # Simplificado: ∫[0 to Q*] P_d(Q) dQ - P* × Q*
        integral_demanda = integrate(precio_demanda, (Q, 0, cantidad))
        excedenteConsumidor = float(integral_demanda - precio * cantidad)

        # Excedente del Productor: ∫[0 to Q*] (P* - P_s(Q)) dQ
        # Simplificado: P* × Q* - ∫[0 to Q*] P_s(Q) dQ
        integral_oferta = integrate(precio_oferta, (Q, 0, cantidad))
        excedenteProductor = float(precio * cantidad - integral_oferta)

        # Excedente Social
        excedente_social = excedenteConsumidor + excedenteProductor

        return {
            'EC': round(excedenteConsumidor, 2),
            'EP': round(excedenteProductor, 2),
            'ES': round(excedente_social, 2),
            'P': precio,
            'Q': cantidad
        }

    except Exception as e:
        raise ErrorValidacion(
            "excedentes",
            f"No se pudieron calcular los excedentes: {str(e)}"
        )