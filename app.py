import streamlit as st
import time

# 1. CONFIGURACIÓN DEL CHASIS SAAS
st.set_page_config(page_title="Synapsis PRO - Seguridad Élite", page_icon="⚛️", layout="centered")

# --- BITÁCORA GLOBAL COMPARTIDA (EL MURO DE ACERO ANTIPIRATERÍA) ---
@st.cache_resource
def obtener_base_datos_global():
    return {}  # Formato: {"codigo_licencia": "session_id_del_ultimo_dispositivo"}

base_datos_global = obtener_base_datos_global()

# Licencias autorizadas para el Tronco Común Universitario
CODIGOS_VIGENTES = ["SYNAPSIS-PRO", "VET-BIOQUIMICA-2026", "MED-ELITE-30DAYS"]

# Generar identificador único de dispositivo/pestaña basado en tiempo de alta precisión
if "mi_session_id" not in st.session_state:
    st.session_state["mi_session_id"] = str(time.time_ns())

# Estados de control de acceso locales
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "codigo_ingresado" not in st.session_state:
    st.session_state["codigo_ingresado"] = ""

# --- VARIABLES DE ESTADO DE LA SIMULACIÓN ---
if "vidas" not in st.session_state:
    st.session_state["vidas"] = 3
if "puntos" not in st.session_state:
    st.session_state["puntos"] = 0
if "caso_actual" not in st.session_state:
    st.session_state["caso_actual"] = 1
if "resultado_evaluacion" not in st.session_state:
    st.session_state["resultado_evaluacion"] = None

# --- FUNCIÓN COLECTORA DE PATRULLAJE AUTOMÁTICO (EL RADAR INVISIBLE) ---
def verificar_bloqueo_pirateria():
    """Verifica instantáneamente si este dispositivo ha perdido el derecho de sesión."""
    if st.session_state["autenticado"]:
        codigo = st.session_state["codigo_ingresado"]
        id_actual_en_servidor = base_datos_global.get(codigo)
        
        # Si otro ID reclamó el trono en el servidor, este dispositivo se bloquea de inmediato
        if id_actual_en_servidor != st.session_state["mi_session_id"]:
            st.session_state["autenticado"] = False
            st.session_state["codigo_ingresado"] = ""
            st.error("🚨 SUSPENSIÓN POR PIRATERÍA: Se detectó doble inicio de sesión simultáneo. Tu acceso en este dispositivo ha sido revocado automáticamente.")
            st.info("💡 Cada suscripción mensual es individual. Para usar Synapsis en múltiples pantallas, adquiere una licencia adicional.")
            st.stop()

# --- FRAGMENTO DE REFRESCO EN SEGUNDO PLANO (AUTOMATIZACIÓN TOTAL) ---
@st.fragment(run_every=5)
def radar_seguridad_pasivo():
    """Ejecuta un escaneo silencioso en el servidor cada 5 segundos sin molestar al alumno."""
    if st.session_state["autenticado"]:
        codigo = st.session_state["codigo_ingresado"]
        if base_datos_global.get(codigo) != st.session_state["mi_session_id"]:
            st.rerun() # Fuerza el refresco de la app completa para detonar la expulsión

# --- INTERFAZ DE ACCESO (EL MURO) ---
if not st.session_state["autenticado"]:
    st.title("🔐 Synapsis PRO")
    st.subheader("Acceso a la Plataforma de Especialización Biomédica")
    st.write("Introduce tu código de suscripción de 30 días para sincronizarte con el entorno de Tronco Común.")
    
    codigo_input = st.text_input("Código de Licencia Válido:", type="password", placeholder="SYNAPSIS-PRO")
    
    if st.button("Validar e Ingresar"):
        codigo_limpio = codigo_input.strip().upper()
        if codigo_limpio in CODIGOS_VIGENTES:
            # Sobreescribir el servidor con NUESTRO ID único de pestaña (Expulsa al anterior)
            base_datos_global[codigo_limpio] = st.session_state["mi_session_id"]
            
            st.session_state["autenticado"] = True
            st.session_state["codigo_ingresado"] = codigo_limpio
            st.success("Licencia verificada con éxito. Sincronizando radar de seguridad...")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("❌ Código inválido o suscripción expirada. Verifica tu pago.")
else:
    # ACTIVAR EL RADAR PASIVO: Escanea el servidor en background cada 5 segundos
    radar_seguridad_pasivo()
    
    # EJECUTAR INTERCEPTOR: Bloquea el renderizado si el radar detecta anomalías
    verificar_bloqueo_pirateria()

    # --- INTERFAZ CORE: BIENVENIDO AL SIMULADOR ---
    st.title("⚛️ Synapsis: Especialización en Bioquímica")
    st.caption(f"Consola de Tronco Común | Licencia Protegida: {st.session_state['codigo_ingresado']}")
    
    # Panel lateral de estatus
    with st.sidebar:
        st.header("📋 Panel de Evaluación")
        st.metric(label="❤️ Vidas Restantes", value=st.session_state.vidas)
        st.metric(label="🏆 Puntos de Rigor Científico", value=st.session_state.puntos)
        st.write("---")
        if st.button("🚪 Cerrar Sesión"):
            if st.session_state["codigo_ingresado"] in base_datos_global:
                # Al salir legalmente, liberamos el código en el servidor
                if base_datos_global[st.session_state["codigo_ingresado"]] == st.session_state["mi_session_id"]:
                    del base_datos_global[st.session_state["codigo_ingresado"]]
            st.session_state["autenticado"] = False
            st.rerun()

    st.header("🔬 Bloque 0: Fundamentos Químicos de la Materia Viva")
    st.write("Módulo de homologación nacional para ciencias de la salud. El sistema se está patrullando automáticamente.")
    st.write("---")

    # Sistema de Game Over
    if st.session_state.vidas <= 0:
        st.error("💀 **¡Inestabilidad Estructural Total!** Has cometido demasiados errores conceptuales básicos en química. El simulador se ha bloqueado.")
        if st.button("♻️ Reiniciar Bloque 0"):
            st.session_state.vidas = 3
            st.session_state.puntos = 0
            st.session_state.caso_actual = 1
            st.session_state.resultado_evaluacion = None
            st.rerun()
            
    # Condición de Victoria
    elif st.session_state.caso_actual > 2:
        st.balloons()
        st.success(f"🏆 **¡Módulo Completado!** Tienes las bases sólidas para avanzar.")
        if st.button("♻️ Volver a Evaluar"):
            st.session_state.caso_actual = 1
            st.session_state.puntos = 0
            st.session_state.vidas = 3
            st.session_state.resultado_evaluacion = None
            st.rerun()
            
    else:
        # --- DESAFÍO 1: LA DEFINICIÓN DE BIOQUÍMICA ---
        if st.session_state.caso_actual == 1:
            st.subheader("📋 Desafío 1: El Objeto de Estudio de la Bioquímica")
            pregunta = st.radio(
                "¿Cuál es la definición operacional más precisa de la Bioquímica en ciencias de la salud?",
                [
                    "Estudia la anatomía celular macroscópica mediante el uso de microscopía óptica.",
                    "Es la disciplina molecular que estudia los componentes químicos de los seres vivos, sus estructuras, funciones y las reacciones químicas (metabolismo) que sustentan la vida.",
                    "Analiza las fuerzas mecánicas de los músculos en animales."
                ],
                key="fund_caso_1"
            )
            
            if st.button("Confirmar Análisis", key="btn_fund_1"):
                verificar_bloqueo_pirateria()  # Patrullaje extra antes de procesar puntos
                if "disciplina molecular" in pregunta:
                    st.session_state.resultado_evaluacion = ("correcto", "¡Correcto! La bioquímica opera a nivel molecular explicando cómo la materia genera vida.")
                    st.session_state.puntos += 100
                else:
                    st.session_state.resultado_evaluacion = ("incorrecto", "Error de concepto. Eso describe a la histología o a la biomecánica.")
                    st.session_state.vidas -= 1

        # --- DESAFÍO 2: LA ELECTRONEGATIVIDAD ---
        elif st.session_state.caso_actual == 2:
            st.subheader("📋 Desafío 2: Comportamiento Atómico y Electronegatividad")
            pregunta = st.radio(
                "¿Qué ocurre cuando el Oxígeno altamente electronegativo se enlaza con el Hidrógeno?",
                [
                    "Los electrones se comparten de manera perfectamente simétrica, creando una molécula apolar.",
                    "Se genera un enlace covalente polar, donde el Oxígeno jala los electrones con más fuerza, acumulando una densidad de carga parcialmente negativa.",
                    "El Hidrógeno destruye el núcleo del Oxígeno."
                ],
                key="fund_caso_2"
            )
            
            if st.button("Confirmar Análisis", key="btn_fund_2"):
                verificar_bloqueo_pirateria()  # Patrullaje extra antes de procesar puntos
                if "covalente polar" in pregunta:
                    st.session_state.resultado_evaluacion = ("correcto", "¡Soberbio! Esa asimetría es el origen de los dipolos moleculares que permiten al agua disolver biomoléculas.")
                    st.session_state.puntos += 100
                else:
                    st.session_state.resultado_evaluacion = ("incorrecto", "Incorrecto. Si fuera simétrica el enlace sería no polar (como C-H).")
                    st.session_state.vidas -= 1

        # Despliegue de retroalimentación
        if st.session_state.resultado_evaluacion:
            tipo, mensaje = st.session_state.resultado_evaluacion
            if tipo == "correcto":
                st.success(mensaje)
                if st.button("Siguiente Desafío ➡️"):
                    st.session_state.caso_actual += 1
                    st.session_state.resultado_evaluacion = None
                    st.rerun()
            else:
                st.error(mensaje)
                if st.button("Analizar Error y Continuar 🔄"):
                    st.session_state.resultado_evaluacion = None
                    st.rerun()
