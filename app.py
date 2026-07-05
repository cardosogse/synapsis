import streamlit as st
import time

# Configuración de la página
st.set_page_config(page_title="Synapsis AI", page_icon="🔐", layout="centered")

# Simulación de Base de Datos en la memoria del Servidor
if "tokens_activos" not in st.session_state:
    st.session_state["tokens_activos"] = {} # Formato: {"codigo": "session_id_actual"}

# Lista de códigos válidos (Suscripciones de 30 días)
CODIGOS_VALIDOS = ["KAIZEN-MES-SUSCRIPCION", "VET-ELITE-30DAYS", "SYNAPSIS-PRO"]

# Generar un ID único para la pestaña/dispositivo actual si no existe
if "mi_session_id" not in st.session_state:
    st.session_state["mi_session_id"] = str(time.time())

# Variables de estado de la aplicación
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "codigo_ingresado" not in st.session_state:
    st.session_state["codigo_ingresado"] = ""

# --- SISTEMA DE VERIFICACIÓN EN TIEMPO REAL (EL BLINDAJE) ---
if st.session_state["autenticado"]:
    codigo = st.session_state["codigo_ingresado"]
    # Si el ID de esta pestaña ya no coincide con el último que se registró en el servidor...
    if st.session_state["tokens_activos"].get(codigo) != st.session_state["mi_session_id"]:
        st.session_state["autenticado"] = False
        st.error("🚨 SUSPENSIÓN POR PIRATERÍA: Se detectó doble inicio de sesión simultáneo. Tu acceso en este dispositivo ha sido revocado.")
        st.info("💡 Cada suscripción mensual es individual. Para usar Synapsis en múltiples pantallas, adquiere una licencia adicional.")
        st.stop()

# --- INTERFAZ DE USUARIO ---
if not st.session_state["autenticado"]:
    st.title("🔐 Synapsis")
    st.subheader("Acceso a la Suscripción Mensual")
    st.write("Introduce tu código de licencia vigente de 30 días para sincronizarte con el Tutor de Inteligencia Artificial.")
    
    codigo_input = st.text_input("Código de Licencia:", type="password", placeholder="Introduce tu código aquí...")
    
    if st.button("Validar e Ingresar"):
        if codigo_input in CODIGOS_VALIDOS:
            # Registrar que este dispositivo es el dueño MÁS RECIENTE del código
            st.session_state["tokens_activos"][codigo_input] = st.session_state["mi_session_id"]
            st.session_state["autenticado"] = True
            st.session_state["codigo_ingresado"] = codigo_input
            st.success("¡Licencia validada correctamente! Sincronizando...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Código inválido o suscripción expirada. Verifica tu pago mensual.")
else:
    # --- CONTENIDO DE TU PLATAFORMA (FASE COMERCIAL) ---
    st.title("🧠 Synapsis: Tutor de Élite")
    st.success(class_name="¡Conexión Blindada y Segura!")
    
    st.sidebar.title("📚 Módulos de Biología")
    modulo = st.sidebar.radio("Selecciona tu unidad:", ["Fase 1: Introducción Teórica", "Fase 2: Rigor Técnico", "Fase 3: Evaluación Virtual"])
    
    if modulo == "Fase 1: Introducción Teórica":
        st.header("🔬 Unidad 1: Biología Celular y Molecular")
        st.write("Bienvenido al andamiaje pedagógico automatizado. Aquí inicia tu entrenamiento científico.")
        if st.button("Avanzar a Fase 2"):
            st.info("Navegando al siguiente bloque técnico...")
            
    elif modulo == "Fase 2: Rigor Técnico":
        st.header("🧪 Fase 2: Análisis Clínico y Veterinario")
        st.write("Contenido exclusivo de alta especialización para la facultad. Analizando estructuras moleculares avanzadas.")
        
    elif modulo == "Fase 3: Evaluación Virtual":
        st.header("📊 Fase 3: Simulador de Examen")
        st.write("Pon a prueba tus conocimientos con el motor de IA adaptativo.")

    # Botón visible para actualizar el estado del cliente y validar que no haya piratas
    if st.button("🔄 Sincronizar Estado"):
        st.rerun()
