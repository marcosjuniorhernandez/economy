"""
Modelo IS-LM - Equilibrio de corto plazo en economía cerrada.

El modelo IS-LM (Inversión-Ahorro / Liquidez-Dinero) analiza
el equilibrio simultáneo del mercado de bienes y del mercado monetario.
"""

from sympy import symbols, solve, diff
from typing import Dict, Optional
from ..nucleo.base import ModeloEconomico
from ..nucleo.excepciones import ErrorEquilibrio
from ..utilidades.parseador import translatex
from ..utilidades.decoradores import ayuda, explicacion


@ayuda(
    descripcionEconomica="""
    El modelo IS-LM representa el equilibrio macroeconómico de corto plazo
    en una economía cerrada. Combina:
    
    - Curva IS: Equilibrio en el mercado de bienes (Y = C + I + G)
    - Curva LM: Equilibrio en el mercado de dinero (M/P = L(Y, i))
    
    El modelo permite analizar los efectos de políticas fiscales y monetarias
    sobre el producto (Y) y la tasa de interés (i).
    """,
    supuestos=[
        "Economía cerrada (sin sector externo)",
        "Precios fijos en el corto plazo",
        "Desempleo (economía por debajo del pleno empleo)",
        "Tasa de interés flexible",
        "Expectativas estáticas"
    ],
)

class ISLM(ModeloEconomico):
    """
    Modelo IS-LM de equilibrio macroeconómico.
    
    Analiza el equilibrio simultáneo de:
    - Mercado de bienes (IS)
    - Mercado de dinero (LM)
    
    Ejemplo:
        >>> modelo = ISLM()
        >>> resultados = modelo.equilibrio(
        ...     consumo="C = 100 + 0.8(Y - T)",
        ...     inversion="I = 300 - 20r",
        ...     demandaDinero="L = 0.2Y - 10r",
        ...     gastoPublico=200,
        ...     impuestos=150,
        ...     ofertaMonetaria=200,
        ...     nivelPrecios=1
        ... )
        >>> escribir(resultados, "Equilibrio IS-LM")
    """
    
    def __init__(self):
        """Inicializa el modelo IS-LM."""
        super().__init__()

        # Definir símbolos económicos
        self.Y = symbols('Y')      # Producto/Ingreso
        self.i = symbols('i')      # Tasa de interés
        self.C = symbols('C')      # Consumo
        self.I = symbols('I')      # Inversión
        self.G = symbols('G')      # Gasto público
        self.T = symbols('T')      # Impuestos
        self.M = symbols('M')      # Oferta monetaria
        self.P = symbols('P')      # Nivel de precios
        self.L = symbols('L')      # Demanda de dinero

    def _detectarCaso(self, expresionDemandaDinero) -> str:
        """
        Detecta si la demanda de dinero corresponde al caso clásico o keynesiano.

        CASO CLÁSICO: L no depende de i → LM es vertical
        CASO KEYNESIANO: L sí depende de i → LM tiene pendiente positiva
        TRAMPA DE LIQUIDEZ: Cuando sensibilidad a i es infinita → LM horizontal

        Args:
            expresionDemandaDinero: Expresión simbólica de L

        Returns:
            'CLASICO' o 'KEYNESIANO' o 'TRAMPA_LIQUIDEZ'
        """
        # Verificar si la tasa de interés está en la expresión
        simbolos = expresionDemandaDinero.free_symbols
        tieneI = self.i in simbolos

        if not tieneI:
            # Si L no depende de i → Caso Clásico (LM vertical)
            return 'CLASICO'
        else:
            # Derivar respecto a i para ver la sensibilidad
            sensibilidad = diff(expresionDemandaDinero, self.i)

            # En el caso keynesiano normal, ∂L/∂i es negativa (más i, menos demanda de dinero)
            # Trampa de liquidez ocurre cuando esta sensibilidad es extremadamente alta
            # (en términos absolutos)
            # Por ahora, solo detectamos si es keynesiano (tiene sensibilidad a i)
            return 'KEYNESIANO'
    
    @explicacion("""
    Calcula el equilibrio macroeconómico resolviendo simultáneamente
    las ecuaciones IS y LM. También calcula los multiplicadores de política.
    """)
    def equilibrio(self,
                  consumo: str,
                  inversion: str,
                  demandaDinero: str,
                  gastoPublico: float,
                  impuestos,  # Puede ser float o str (función de Y)
                  ofertaMonetaria: float,
                  nivelPrecios: float = 1.0) -> Dict[str, float]:
        """
        Calcula el equilibrio IS-LM (donde se cruzan las curvas IS y LM).

        GUÍA PARA ECONOMISTAS:
        Este método hace 3 cosas:
        1. Encuentra el punto donde Oferta = Demanda en el mercado de bienes (curva IS)
        2. Encuentra el punto donde Oferta = Demanda de dinero (curva LM)
        3. Resuelve ambas ecuaciones simultáneamente para encontrar Y* y i*

        Args:
            consumo: Cómo gastan las familias según su ingreso disponible
                    Ejemplo: "C = 200 + 0.8(Y - T)" significa que consumen 200 de forma autónoma
                    más 80% de su ingreso disponible (Y-T es ingreso después de impuestos)

            inversion: Cuánto invierten las empresas según la tasa de interés
                      Ejemplo: "I = 1000 - 50i" significa que si i=0% invierten 1000,
                      pero por cada 1% que sube i, la inversión cae en 50 unidades

            demandaDinero: Cuánto dinero quiere la gente tener en efectivo
                          Ejemplo: "L = 0.25Y - 50i" significa que quieren más dinero
                          cuando tienen más ingreso (Y), pero menos cuando i es alta

            gastoPublico: Cuánto gasta el gobierno (G) en bienes y servicios
            impuestos: Cuánto recauda el gobierno (T). Puede ser:
                      - Un número (impuesto de suma fija): impuestos=150
                      - Una función (impuesto proporcional): impuestos='T = 100 + 0.2Y'
            ofertaMonetaria: Cuánto dinero hay circulando en la economía (M)
            nivelPrecios: Nivel general de precios (P), normalmente = 1

        Returns:
            Diccionario con los valores de equilibrio:
                - 'Y*': Producto/Ingreso de equilibrio (PIB de corto plazo)
                - 'i*': Tasa de interés de equilibrio
                - 'β': Multiplicador fiscal (cuánto aumenta Y si G sube en 1)
                - 'γ': Multiplicador monetario (cuánto aumenta Y si M sube en 1)
                - 'C*': Consumo total en equilibrio
                - 'I*': Inversión total en equilibrio
                - 'T*': Impuestos en equilibrio (si T es función, se calcula; si es constante, se devuelve)

        Raises:
            ErrorEquilibrio: Si las curvas no se cruzan (no hay equilibrio)
        """
        # ========== PASO 1: PARSEAR LAS ECUACIONES ==========
        # Convertimos las ecuaciones de texto LaTeX a expresiones matemáticas
        # que Python puede manipular
        ecuacionConsumo = translatex(consumo)
        ecuacionInversion = translatex(inversion)
        ecuacionDemandaDinero = translatex(demandaDinero)

        # Extraemos el lado derecho de cada ecuación (después del "=")
        # Por ejemplo, de "C = 200 + 0.8Y" extraemos "200 + 0.8Y"
        expresionConsumo = ecuacionConsumo.rhs if hasattr(ecuacionConsumo, 'rhs') else ecuacionConsumo
        expresionInversion = ecuacionInversion.rhs if hasattr(ecuacionInversion, 'rhs') else ecuacionInversion
        expresionDemandaDinero = ecuacionDemandaDinero.rhs if hasattr(ecuacionDemandaDinero, 'rhs') else ecuacionDemandaDinero

        # ========== PASO 1.5: MANEJAR IMPUESTOS (FUNCIÓN O CONSTANTE) ==========
        # Los impuestos pueden ser:
        # - Una constante: impuestos=150 (impuesto de suma fija)
        # - Una función: impuestos='T = 100 + 0.2Y' (impuesto proporcional al ingreso)
        if isinstance(impuestos, str):
            # El usuario pasó una función, parseamos
            ecuacionImpuestos = translatex(impuestos)
            expresionImpuestos = ecuacionImpuestos.rhs if hasattr(ecuacionImpuestos, 'rhs') else ecuacionImpuestos
            # Sustituimos T por su expresión en la función de consumo
            expresionConsumo = expresionConsumo.subs(self.T, expresionImpuestos)
            valorNumericoImpuestos = None  # Lo calcularemos después del equilibrio
        else:
            # Es una constante numérica
            expresionImpuestos = impuestos
            valorNumericoImpuestos = impuestos

        # ========== PASO 2: NORMALIZAR LA TASA DE INTERÉS ==========
        # Permitimos que el usuario use 'r' (por compatibilidad) pero internamente usamos 'i'
        # 'i' representa la tasa de interés NOMINAL (la tasa real 'r' se verá en otros modelos)
        for expresion in [expresionConsumo, expresionInversion, expresionDemandaDinero]:
            simbolos = expresion.free_symbols
            for simbolo in simbolos:
                nombreSimbolo = str(simbolo)
                # Si el usuario escribió 'r', lo convertimos a 'i' internamente
                if nombreSimbolo == 'r':
                    expresionConsumo = expresionConsumo.subs(simbolo, self.i)
                    expresionInversion = expresionInversion.subs(simbolo, self.i)
                    expresionDemandaDinero = expresionDemandaDinero.subs(simbolo, self.i)

        # ========== PASO 2.5: DETECTAR CASO ECONÓMICO (CLÁSICO VS KEYNESIANO) ==========
        casoEconomico = self._detectarCaso(expresionDemandaDinero)

        # ========== PASO 3: PLANTEAR LAS CONDICIONES DE EQUILIBRIO ==========
        # Curva IS: En el mercado de bienes, Oferta = Demanda
        # Esto es: Y = C + I + G (el producto debe igualar al gasto total)
        # La reorganizamos como: Y - C - I - G = 0
        ecuacionIS = self.Y - expresionConsumo - expresionInversion - self.G

        # Curva LM: En el mercado de dinero, Oferta = Demanda
        # Esto es: M/P = L(Y, i) (oferta real de dinero = demanda de dinero)
        # La reorganizamos como: L - M/P = 0
        ecuacionLM = expresionDemandaDinero - (self.M / self.P)

        # ========== PASO 4: RESOLVER EL SISTEMA DE ECUACIONES ==========
        # Resolvemos simultáneamente IS y LM para encontrar Y* e i*
        try:
            solucionSimbolica = solve(
                [ecuacionIS, ecuacionLM],  # Las dos ecuaciones
                (self.Y, self.i)           # Las dos incógnitas
            )
        except Exception as error:
            raise ErrorEquilibrio(f"No se pudo resolver el sistema IS-LM: {str(error)}")

        if not solucionSimbolica:
            raise ErrorEquilibrio("No existe equilibrio IS-LM para estos parámetros")

        # Extraemos las expresiones simbólicas de Y* e i*
        expresionYestrella = solucionSimbolica[self.Y]
        expresionIestrella = solucionSimbolica[self.i]

        # ========== PASO 5: CALCULAR MULTIPLICADORES ==========
        # El multiplicador fiscal (k) nos dice cuánto cambia Y si G cambia en 1
        # Por ejemplo, si k=2, entonces un aumento de G en 100 aumenta Y en 200
        multiplicadorFiscal = diff(expresionYestrella, self.G)

        # El multiplicador monetario (m) nos dice cuánto cambia Y si M cambia en 1
        multiplicadorMonetario = diff(expresionYestrella, self.M)

        # ========== PASO 6: SUSTITUIR VALORES NUMÉRICOS ==========
        # Reemplazamos las variables G, M, P por sus valores concretos
        # Si T es constante, también lo sustituimos; si es función, ya está integrado
        valoresNumericos = {
            self.G: gastoPublico,
            self.M: ofertaMonetaria,
            self.P: nivelPrecios
        }

        # Solo agregamos T a los valores si es constante (no función)
        if valorNumericoImpuestos is not None:
            valoresNumericos[self.T] = valorNumericoImpuestos

        # Calculamos Y* e i* numéricamente
        Yestrella = float(expresionYestrella.subs(valoresNumericos))
        iestrella = float(expresionIestrella.subs(valoresNumericos))

        # Si T era una función, calculamos su valor en el equilibrio
        if valorNumericoImpuestos is None:
            valorNumericoImpuestos = float(expresionImpuestos.subs(self.Y, Yestrella))

        # ========== PASO 7: CALCULAR C* E I* DE EQUILIBRIO ==========
        # Ahora que conocemos Y* e i*, podemos calcular cuánto se consume
        # y cuánto se invierte en equilibrio
        valoresCompletos = {**valoresNumericos, self.Y: Yestrella, self.i: iestrella}

        Cestrella = float(expresionConsumo.subs(valoresCompletos))
        Iestrella = float(expresionInversion.subs(valoresCompletos))

        # ========== RETORNAR RESULTADOS ==========
        return {
            'Y*': Yestrella,                                                  # Producto de equilibrio
            'i*': iestrella,                                                  # Tasa de interés de equilibrio
            'β': float(multiplicadorFiscal.subs(valoresNumericos)),       # Multiplicador fiscal
            'γ': float(multiplicadorMonetario.subs(valoresNumericos)),   # Multiplicador monetario
            'C*': Cestrella,                                                  # Consumo de equilibrio
            'I*': Iestrella,                                                  # Inversión de equilibrio
            'T*': valorNumericoImpuestos,                                     # Impuestos en equilibrio
            'caso': casoEconomico                                             # 'CLASICO' o 'KEYNESIANO'
        }
    
    def resolver(self) -> Dict[str, float]:
        """Implementación del método abstracto."""
        # Este método requiere parámetros, usar equilibrio() directamente
        raise NotImplementedError("Usa el método equilibrio() con los parámetros requeridos")
    
    def explicar(self) -> str:
        """Explicación del modelo IS-LM."""
        return """
        El modelo IS-LM muestra cómo se determina el ingreso (Y) y la tasa de interés (i)
        en el corto plazo cuando los precios son rígidos.

        - La curva IS representa combinaciones de (Y, i) donde el mercado de bienes está en equilibrio
        - La curva LM representa combinaciones de (Y, i) donde el mercado de dinero está en equilibrio
        - El equilibrio ocurre donde se cruzan ambas curvas

        Política Fiscal Expansiva (↑G):
            → IS se desplaza a la derecha
            → ↑Y, ↑i
            → Puede causar efecto expulsión o "crowding-out" de la inversión privada

        Política Monetaria Expansiva (↑M):
            → LM se desplaza a la derecha
            → ↑Y, ↓i
            → Estimula inversión privada
        """

    def politicaMonetaria(self,
                         tipo: str,
                         magnitud: float,
                         consumo: str,
                         inversion: str,
                         demandaDinero: str,
                         gastoPublico: float,
                         impuestos: float,
                         ofertaMonetariaInicial: float,
                         nivelPrecios: float = 1.0) -> Dict[str, any]:
        """
        Simula el efecto de una política monetaria en el equilibrio IS-LM.

        GUÍA PARA ECONOMISTAS:
        Este método te permite ver qué pasa cuando el Banco Central:
        - EXPANDE la oferta monetaria (M↑): "imprime dinero" o baja la tasa de interés
        - CONTRAE la oferta monetaria (M↓): "retira dinero" o sube la tasa de interés

        En el gráfico IS-LM, esto desplaza la curva LM:
        - Política EXPANSIVA → LM se mueve a la DERECHA → Y↑ y i↓
        - Política CONTRACTIVA → LM se mueve a la IZQUIERDA → Y↓ y i↑

        Args:
            tipo: "EXPANSIVA" (para estimular economía) o "CONTRACTIVA" (para frenarla)
            magnitud: Cuánto cambia M (por ejemplo, 100 = inyectar 100 unidades de dinero)
            consumo, inversion, demandaDinero: Las ecuaciones de comportamiento (igual que equilibrio)
            gastoPublico, impuestos: Variables fiscales (G y T)
            ofertaMonetariaInicial: Cuánto dinero hay ANTES de la política
            nivelPrecios: Nivel de precios (normalmente = 1)

        Returns:
            Diccionario completo con:
                - 'tipo': EXPANSIVA o CONTRACTIVA
                - 'equilibrioInicial': Valores de Y*, i*, C*, I* ANTES del cambio
                - 'equilibrioFinal': Valores de Y*, i*, C*, I* DESPUÉS del cambio
                - 'cambios': Los Deltas (ΔY, Δr, ΔC, ΔI, ΔM)
                - 'efectoExpulsion': False (política monetaria NO causa crowding-out normalmente)

        Ejemplo:
            >>> modelo = ISLM()
            >>> resultado = modelo.politicaMonetaria(
            ...     tipo="EXPANSIVA",
            ...     magnitud=50,  # El BC inyecta 50 unidades
            ...     consumo="C = 200 + 0.8(Y - 150)",
            ...     inversion="I = 300 - 20i",
            ...     demandaDinero="L = 0.2Y - 10i",
            ...     gastoPublico=200,
            ...     impuestos=150,
            ...     ofertaMonetariaInicial=200
            ... )
            >>> print(f"El PIB aumentó en: {resultado['cambios'][r'$\\Delta Y$']}")
        """
        # Validar que el tipo sea correcto
        tipoNormalizado = tipo.upper()
        if tipoNormalizado not in ["EXPANSIVA", "CONTRACTIVA"]:
            raise ValueError("El tipo debe ser 'EXPANSIVA' o 'CONTRACTIVA'")

        # ========== PASO 1: CALCULAR EQUILIBRIO INICIAL (ANTES DE LA POLÍTICA) ==========
        equilibrioInicial = self.equilibrio(
            consumo=consumo,
            inversion=inversion,
            demandaDinero=demandaDinero,
            gastoPublico=gastoPublico,
            impuestos=impuestos,
            ofertaMonetaria=ofertaMonetariaInicial,
            nivelPrecios=nivelPrecios
        )

        # ========== PASO 2: APLICAR LA POLÍTICA MONETARIA ==========
        # Si es EXPANSIVA: el Banco Central inyecta dinero (M aumenta)
        # Si es CONTRACTIVA: el Banco Central retira dinero (M disminuye)
        if tipoNormalizado == "EXPANSIVA":
            ofertaMonetariaFinal = ofertaMonetariaInicial + magnitud
        else:  # CONTRACTIVA
            ofertaMonetariaFinal = ofertaMonetariaInicial - magnitud

        # ========== PASO 3: CALCULAR NUEVO EQUILIBRIO (DESPUÉS DE LA POLÍTICA) ==========
        equilibrioFinal = self.equilibrio(
            consumo=consumo,
            inversion=inversion,
            demandaDinero=demandaDinero,
            gastoPublico=gastoPublico,
            impuestos=impuestos,
            ofertaMonetaria=ofertaMonetariaFinal,
            nivelPrecios=nivelPrecios
        )

        # ========== PASO 4: CALCULAR LOS CAMBIOS (DELTAS) ==========
        # Comparamos el equilibrio final con el inicial
        cambios = {
            r'$\\Delta Y$': equilibrioFinal['Y*'] - equilibrioInicial['Y*'],   # Cambio en PIB
            r'$\\Delta i$': equilibrioFinal['i*'] - equilibrioInicial['i*'],   # Cambio en tasa de interés
            r'$\\Delta C$': equilibrioFinal['C*'] - equilibrioInicial['C*'],   # Cambio en consumo
            r'$\\Delta I$': equilibrioFinal['I*'] - equilibrioInicial['I*'],   # Cambio en inversión
            r'$\\Delta M$': magnitud if tipoNormalizado == "EXPANSIVA" else -magnitud  # Cambio en M
        }

        # ========== RETORNAR RESULTADOS COMPLETOS ==========
        return {
            'tipo': tipoNormalizado,
            'equilibrioInicial': equilibrioInicial,
            'equilibrioFinal': equilibrioFinal,
            'cambios': cambios,
            # Nota: Política monetaria normalmente NO causa efecto expulsión
            # (la inversión sube porque r baja en política expansiva)
            'efectoExpulsion': cambios[r'$\\Delta I$'] < 0
        }

    def politicaFiscal(self,
                      tipo: str,
                      magnitud: float,
                      consumo: str,
                      inversion: str,
                      demandaDinero: str,
                      gastoPublicoInicial: float,
                      impuestos: float,
                      ofertaMonetaria: float,
                      nivelPrecios: float = 1.0) -> Dict[str, any]:
        """
        Simula el efecto de una política fiscal en el equilibrio IS-LM.

        GUÍA PARA ECONOMISTAS:
        Este método te permite ver qué pasa cuando el Gobierno:
        - EXPANDE el gasto (G↑): construye más carreteras, contrata profesores, etc.
        - CONTRAE el gasto (G↓): reduce inversión pública, despide funcionarios, etc.

        En el gráfico IS-LM, esto desplaza la curva IS:
        - Política EXPANSIVA → IS se mueve a la DERECHA → Y↑ y i↑
        - Política CONTRACTIVA → IS se mueve a la IZQUIERDA → Y↓ y i↓

        EFECTO EXPULSIÓN (Crowding-out):
        Cuando G↑, el PIB sube (Y↑) pero también sube i↑
        → Al subir r, la inversión privada (I) cae
        → El aumento de Y es MENOR que el esperado por el multiplicador
        Este método detecta automáticamente si hay crowding-out.

        Args:
            tipo: "EXPANSIVA" (para estimular economía) o "CONTRACTIVA" (para frenarla)
            magnitud: Cuánto cambia G (ej: 100 = gobierno gasta 100 unidades más)
            consumo, inversion, demandaDinero: Las ecuaciones de comportamiento
            gastoPublicoInicial: Cuánto gasta el gobierno ANTES de la política
            impuestos, ofertaMonetaria: Otras variables (T y M)
            nivelPrecios: Nivel de precios (normalmente = 1)

        Returns:
            Diccionario completo con:
                - 'tipo': EXPANSIVA o CONTRACTIVA
                - 'equilibrioInicial': Valores ANTES del cambio
                - 'equilibrioFinal': Valores DESPUÉS del cambio
                - 'cambios': Los Deltas (ΔY, Δr, ΔC, ΔI, ΔG)
                - 'efectoExpulsion': True si I cae cuando G sube (crowding-out)
                - 'proporcionExpulsion': Qué % del gasto público "expulsa" inversión privada

        Ejemplo:
            >>> modelo = ISLM()
            >>> resultado = modelo.politicaFiscal(
            ...     tipo="EXPANSIVA",
            ...     magnitud=100,  # Gobierno gasta 100 más
            ...     consumo="C = 200 + 0.8(Y - 150)",
            ...     inversion="I = 300 - 20i",
            ...     demandaDinero="L = 0.2Y - 10i",
            ...     gastoPublicoInicial=200,
            ...     impuestos=150,
            ...     ofertaMonetaria=200
            ... )
            >>> if resultado['efectoExpulsion']:
            ...     print("¡Cuidado! Hay crowding-out")
            ...     print(f"Por cada $1 que gasta el gobierno, la inversión privada cae ${resultado['proporcionExpulsion']:.2f}")
        """
        # Validar que el tipo sea correcto
        tipoNormalizado = tipo.upper()
        if tipoNormalizado not in ["EXPANSIVA", "CONTRACTIVA"]:
            raise ValueError("El tipo debe ser 'EXPANSIVA' o 'CONTRACTIVA'")

        # ========== PASO 1: CALCULAR EQUILIBRIO INICIAL (ANTES DE LA POLÍTICA) ==========
        equilibrioInicial = self.equilibrio(
            consumo=consumo,
            inversion=inversion,
            demandaDinero=demandaDinero,
            gastoPublico=gastoPublicoInicial,
            impuestos=impuestos,
            ofertaMonetaria=ofertaMonetaria,
            nivelPrecios=nivelPrecios
        )

        # ========== PASO 2: APLICAR LA POLÍTICA FISCAL ==========
        # Si es EXPANSIVA: el gobierno gasta más (G aumenta)
        # Si es CONTRACTIVA: el gobierno gasta menos (G disminuye)
        if tipoNormalizado == "EXPANSIVA":
            gastoPublicoFinal = gastoPublicoInicial + magnitud
        else:  # CONTRACTIVA
            gastoPublicoFinal = gastoPublicoInicial - magnitud

        # ========== PASO 3: CALCULAR NUEVO EQUILIBRIO (DESPUÉS DE LA POLÍTICA) ==========
        equilibrioFinal = self.equilibrio(
            consumo=consumo,
            inversion=inversion,
            demandaDinero=demandaDinero,
            gastoPublico=gastoPublicoFinal,
            impuestos=impuestos,
            ofertaMonetaria=ofertaMonetaria,
            nivelPrecios=nivelPrecios
        )

        # ========== PASO 4: CALCULAR LOS CAMBIOS (DELTAS) ==========
        cambios = {
            r'$\\Delta Y$': equilibrioFinal['Y*'] - equilibrioInicial['Y*'],   # Cambio en PIB
            r'$\\Delta i$': equilibrioFinal['i*'] - equilibrioInicial['i*'],   # Cambio en tasa de interés
            r'$\\Delta C$': equilibrioFinal['C*'] - equilibrioInicial['C*'],   # Cambio en consumo
            r'$\\Delta I$': equilibrioFinal['I*'] - equilibrioInicial['I*'],   # Cambio en inversión
            r'$\\Delta G$': magnitud if tipoNormalizado == "EXPANSIVA" else -magnitud  # Cambio en G
        }

        # ========== PASO 5: DETECTAR EFECTO EXPULSIÓN (CROWDING-OUT) ==========
        # Hay efecto expulsión cuando:
        # - Política EXPANSIVA (G↑) pero la inversión privada CAE (I↓)
        # - Política CONTRACTIVA (G↓) pero la inversión privada SUBE (I↑)
        hayEfectoExpulsion = False
        if tipoNormalizado == "EXPANSIVA" and cambios[r'$\\Delta I$'] < 0:
            # G subió pero I bajó → hay crowding-out
            hayEfectoExpulsion = True
        elif tipoNormalizado == "CONTRACTIVA" and cambios[r'$\\Delta I$'] > 0:
            # G bajó pero I subió → hay crowding-out inverso
            hayEfectoExpulsion = True

        # Calcular qué proporción del gasto público "expulsa" inversión privada
        # Por ejemplo, si proporcion=0.5, significa que por cada $1 que gasta
        # el gobierno, la inversión privada cae $0.50
        if hayEfectoExpulsion and cambios[r'$\\Delta G$'] != 0:
            proporcionExpulsion = abs(cambios[r'$\\Delta I$'] / cambios[r'$\\Delta G$'])
        else:
            proporcionExpulsion = 0

        # ========== RETORNAR RESULTADOS COMPLETOS ==========
        return {
            'tipo': tipoNormalizado,
            'equilibrioInicial': equilibrioInicial,
            'equilibrioFinal': equilibrioFinal,
            'cambios': cambios,
            'efectoExpulsion': hayEfectoExpulsion,
            'proporcionExpulsion': proporcionExpulsion
        }

    def graficar(self,
                consumo: str,
                inversion: str,
                demandaDinero: str,
                gastoPublico: float,
                impuestos: float,
                ofertaMonetaria: float,
                nivelPrecios: float = 1.0):
        """
        Grafica las curvas IS y LM mostrando el equilibrio.

        Args:
            Los mismos parámetros que equilibrio()

        Returns:
            Lienzo con el gráfico IS-LM

        Ejemplo:
            >>> modelo = ISLM()
            >>> modelo.graficar(
            ...     consumo="C = 200 + 0.8(Y - 150)",
            ...     inversion="I = 300 - 20i",
            ...     demandaDinero="L = 0.2Y - 10i",
            ...     gastoPublico=200,
            ...     impuestos=150,
            ...     ofertaMonetaria=200
            ... )
        """
        from ..utilidades.visuales import Lienzo, ROJO, AZUL, VERDE2
        from sympy import solve, lambdify
        import numpy as np

        # Calcular equilibrio
        eq = self.equilibrio(
            consumo=consumo,
            inversion=inversion,
            demandaDinero=demandaDinero,
            gastoPublico=gastoPublico,
            impuestos=impuestos,
            ofertaMonetaria=ofertaMonetaria,
            nivelPrecios=nivelPrecios
        )

        # Parsear ecuaciones
        ecuacionConsumo = translatex(consumo)
        ecuacionInversion = translatex(inversion)
        ecuacionDemandaDinero = translatex(demandaDinero)

        expresionConsumo = ecuacionConsumo.rhs if hasattr(ecuacionConsumo, 'rhs') else ecuacionConsumo
        expresionInversion = ecuacionInversion.rhs if hasattr(ecuacionInversion, 'rhs') else ecuacionInversion
        expresionDemandaDinero = ecuacionDemandaDinero.rhs if hasattr(ecuacionDemandaDinero, 'rhs') else ecuacionDemandaDinero

        # Normalizar tasa de interés
        for expresion in [expresionConsumo, expresionInversion, expresionDemandaDinero]:
            simbolos = expresion.free_symbols
            for simbolo in simbolos:
                if str(simbolo) == 'r':
                    expresionConsumo = expresionConsumo.subs(simbolo, self.i)
                    expresionInversion = expresionInversion.subs(simbolo, self.i)
                    expresionDemandaDinero = expresionDemandaDinero.subs(simbolo, self.i)

        # Curva IS: Y - C - I - G = 0
        ecuacionIS = self.Y - expresionConsumo - expresionInversion - self.G
        # Despejar i en función de Y para la curva IS
        solucionIS = solve(ecuacionIS.subs({self.G: gastoPublico, self.T: impuestos}), self.i)

        # Curva LM: L - M/P = 0
        ecuacionLM = expresionDemandaDinero - (self.M / self.P)
        # Despejar i en función de Y para la curva LM
        solucionLM = solve(ecuacionLM.subs({self.M: ofertaMonetaria, self.P: nivelPrecios}), self.i)

        # Crear funciones graficables
        if solucionIS:
            func_IS = lambdify(self.Y, solucionIS[0], 'numpy')
        if solucionLM:
            func_LM = lambdify(self.Y, solucionLM[0], 'numpy')

        # Crear lienzo
        lienzo = Lienzo()
        lienzo.configurarEtiquetas(
            etiquetaX="Producto (Y)",
            etiquetaY="Tasa de interés (i)",
            titulo="Modelo IS-LM"
        )

        # Rango de Y para graficar
        Y_min = max(0, eq['Y*'] * 0.5)
        Y_max = eq['Y*'] * 1.5
        valores_Y = np.linspace(Y_min, Y_max, 500)

        # Graficar IS
        if solucionIS:
            valores_i_IS = func_IS(valores_Y)
            # Filtrar valores negativos
            mask_IS = valores_i_IS >= 0
            lienzo.agregar(
                (valores_Y[mask_IS], valores_i_IS[mask_IS]),
                etiqueta="IS",
                color=ROJO
            )

        # Graficar LM
        if solucionLM:
            valores_i_LM = func_LM(valores_Y)
            # Filtrar valores negativos
            mask_LM = valores_i_LM >= 0
            lienzo.agregar(
                (valores_Y[mask_LM], valores_i_LM[mask_LM]),
                etiqueta="LM",
                color=AZUL
            )

        # Marcar equilibrio
        lienzo.agregarPunto(
            eq['Y*'], eq['i*'],
            etiqueta="Equilibrio",
            color=VERDE2,
            mostrarNombre=True,
            nombre=f"E (Y*={eq['Y*']:.1f}, i*={eq['i*']:.2f})"
        )

        lienzo.graficar()
        return lienzo