import streamlit as st
import time

# 1. CONFIGURACIÓN DE LA PÁGINA (Chasis del SaaS)
st.set_page_config(page_title="Synapsis AI", page_icon="🧠", layout="centered")

# --- BITÁCORA GLOBAL COMPARTIDA (EL MURO DE ACERO ANTIPIRATERÍA) ---
# Obliga al servidor a registrar los inicios de sesión a nivel mundial
@st.cache_resource
def obtener_base_datos_global():
    return {}  # Formato: {"codigo_licencia": "session_id_del_ultimo_dispositivo"}

base_datos_global = obtener_base_datos_global()

# DICCIONARIO DE LICENCIAS VIGENTES: Define el nivel y el precio implícito del producto
CODIGOS_VIGENTES = {
    "SYNAPSIS-KIDS": "Secundaria",
    "SYNAPSIS-PREPA": "Preparatoria",
    "SYNAPSIS-PRO": "Universidad"
}

# Generar un identificador único para la pestaña/dispositivo actual
if "mi_session_id" not in st.session_state:
    st.session_state["mi_session_id"] = str(time.time())

# Estados locales de control de sesión
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "codigo_ingresado" not in st.session_state:
    st.session_state["codigo_ingresado"] = ""
if "nivel_educativo" not in st.session_state:
    st.session_state["nivel_educativo"] = ""

# --- VARIABLES DE ESTADO DE LA SIMULACIÓN (GAMIFICACIÓN UNIFICADA) ---
if "vidas" not in st.session_state:
    st.session_state["vidas"] = 3
if "puntos" not in st.session_state:
    st.session_state["puntos"] = 0
if "simulacion_ejecutada" not in st.session_state:
    st.session_state["simulacion_ejecutada"] = False
if "resultado_texto" not in st.session_state:
    st.session_state["resultado_texto"] = ""
if "estado_celula" not in st.session_state:
    st.session_state["estado_celula"] = "Normal"

# --- CONTROLADOR DE PIRATERÍA GLOBAL ---
if st.session_state["autenticado"]:
    codigo = st.session_state["codigo_ingresado"]
    # Si otra pantalla/IP reclama el trono para este mismo código, se expulsa esta pestaña de inmediato
    if base_datos_global.get(codigo) != st.session_state["mi_session_id"]:
        st.session_state["autenticado"] = False
        st.error("🚨 SUSPENSIÓN POR PIRATERÍA: Se detectó doble inicio de sesión simultáneo. Tu acceso en este dispositivo ha sido revocado.")
        st.info("💡 Cada suscripción mensual es individual. Para usar Synapsis en múltiples pantallas, adquiere una licencia adicional.")
        st.stop()

# --- INTERFAZ DE ACCESO (EL MURO) ---
if not st.session_state["autenticado"]:
    st.title("🔐 Synapsis")
    st.subheader("Acceso Automatizado a la Suscripción Mensual")
    st.write("Introduce tu código de licencia vigente de 30 días para sincronizar tu entorno de simulación.")
    
    codigo_input = st.text_input("Código de Licencia:", type="password", placeholder="SYNAPSIS-...")
    
    if st.button("Validar e Ingresar"):
        codigo_limpio = codigo_input.strip().upper()
        if codigo_limpio in CODIGOS_VIGENTES:
            # Reclamar el trono global en el servidor
            base_datos_global[codigo_limpio] = st.session_state["mi_session_id"]
            
            # Registrar estados locales
            st.session_state["autenticado"] = True
            st.session_state["codigo_ingresado"] = codigo_limpio
            st.session_state["nivel_educativo"] = CODIGOS_VIGENTES[codigo_limpio]
            
            st.success(f"¡Licencia validada! Nivel detectado: {st.session_state['nivel_educativo']}. Sincronizando...")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Código inválido o suscripción expirada. Verifica tu pago mensual.")
else:
    # --- INTERFAZ CORE DEL SOFTWARE (UN SOLO VISTAZO) ---
    nivel = st.session_state["nivel_educativo"]
    
    st.title(f"🧠 Synapsis — Entrenador de Ciencias")
    st.caption(f"Licencia Activa: {st.session_state['codigo_ingresado']} | Perfil: {nivel}")
    
    # Barra lateral con el estado de gamificación
    with st.sidebar:
        st.header("📋 Estatus del Alumno")
        st.metric(label="❤️ Vidas Restantes", value=st.session_state.vidas)
        st.metric(label="🏆 Puntos Obtenidos", value=st.session_state.puntos)
        st.write("---")
        if st.button("🚪 Cerrar Sesión de Forma Segura"):
            if st.session_state["codigo_ingresado"] in base_datos_global:
                del base_datos_global[st.session_state["codigo_ingresado"]]
            st.session_state["autenticado"] = False
            st.rerun()

    # --- NÚCLEO CENTRAL DEL MOTOR: LA CÉLULA Y EL MEDIO ---
    st.header("🔬 Simulador Analítico: La Célula y el Equilibrio de Membrana")
    st.write("Manipula el entorno químico que rodea a la célula para observar la consecuencia física en tiempo real.")
    st.write("---")

    # Sistema de Game Over General
    if st.session_state.vidas <= 0:
        st.error("💀 **¡Colapso del Sistema Celular!** Has agotado tus vidas debido a desequilibrios críticos en tus soluciones. El simulador se ha bloqueado.")
        if st.button("♻️ Reiniciar Sistema y Recuperar Vidas"):
            st.session_state.vidas = 3
            st.session_state.puntos = 0
            st.session_state.simulacion_ejecutada = False
            st.session_state.estado_celula = "Normal"
            st.rerun()
    else:
        # CONTROLES INTERACTIVOS SEGMENTADOS AUTOMÁTICAMENTE POR CÓDIGO
        st.subheader("🎛️ Panel de Control de Variables")
        
        if nivel == "Secundaria":
            st.info("🎯 **Modo Exploración Simple:** Aprende cómo el agua y la sal cambian la forma de la célula.")
            opcion_medio = st.radio("¿Cuánta sal le agregas al agua que rodea a la célula?", 
                                    ["Poca sal (Agua casi pura)", "Cantidad normal (Equilibrio)", "Mucha sal (Agua muy concentrada)"])
            
        elif nivel == "Preparatoria":
            st.info("📚 **Modo Examen de Bachillerato:** Predice el comportamiento del Gradiente de Concentración y el Transporte Pasivo.")
            opcion_medio = st.selectbox("Selecciona el tipo de solución que inyectarás al contenedor de la célula:",
                                        ["Solución Hipotónica (Baja concentración de solutos)", 
                                         "Solución Isotónica (Igual concentración de solutos)", 
                                         "Solución Hipertónica (Alta concentración de solutos)"])
            
        elif nivel == "Universidad":
            st.info("🧪 **Modo Consola Analítica / Tronco Común:** Diagnóstico biofísico de alta especialización.")
            # Selección de Modelo Biológico (La constante osmótica)
            modelo_bio = st.selectbox("Establece el Modelo Biológico de Referencia:",
                                      ["Humano (Plasmática basal: 290 mOsm/L)", 
                                       "Veterinario - Canino (Plasmática basal: 300 mOsm/L)"])
            
            # Selector de Soluciones Médicas Reales
            opcion_medio = st.select_slider("Selecciona la sustancia química de infusión intravenosa:",
                                            options=["Cloruro de Sodio (NaCl) al 0.45%", 
                                                     "Cloruro de Sodio (NaCl) al 0.9%", 
                                                     "Cloruro de Sodio (NaCl) al 3%"])

        # --- EL CEREBRO LOCAL (MOTOR LÓGICO DE PYTHON) ---
        # Procesa la entrada sin importar el nivel y determina el comportamiento matemático oculto
        if st.button("🚀 Ejecutar Simulación Dinámica"):
            st.session_state.simulacion_ejecutada = True
            
            # Lógica determinista mapeando las tres entradas al mismo motor biológico
            es_hipotonico = "Poca sal" in opcion_medio or "Hipotónica" in opcion_medio or "0.45%" in opcion_medio
            es_isotonico = "normal" in opcion_medio or "Isotónica" in opcion_medio or "0.9%" in opcion_medio
            es_hipertonico = "Mucha sal" in opcion_medio or "Hipertónica" in opcion_medio or "3%" in opcion_medio
            
            if es_hipotonico:
                st.session_state.estado_celula = "Hinchada / Rompiéndose"
                if nivel == "Secundaria":
                    st.session_state.resultado_texto = "¡El agua entró a la célula como un globo inflado de más! Esto pasa porque el agua busca diluir la sal de adentro."
                    st.session_state.puntos += 50
                elif nivel == "Preparatoria":
                    st.session_state.resultado_texto = "¡Fenómeno de Lisis Celular! El agua se mueve a favor de su gradiente (de menor a mayor concentración de solutos) mediante transporte pasivo."
                    st.session_state.puntos += 100
                elif nivel == "Universidad":
                    st.session_state.resultado_texto = "CRÍTICO: El gradiente osmótico efectivo forzó un flujo neto de agua hacia el espacio intracelular. Se confirma riesgo de Hemólisis Intravascular por infusión de solución marcadamente hipotónica."
                    st.session_state.puntos += 150
                    
            elif es_isotonico:
                st.session_state.estado_celula = "Normal / Estable"
                st.session_state.resultado_texto = "¡Equilibrio perfecto! El flujo neto de agua es cero. La célula conserva su arquitectura y estabilidad homeostática funcional."
                st.session_state.puntos += 50
                
            elif es_hipertonico:
                st.session_state.estado_celula = "Deshidratada / Arrugada"
                if nivel == "Secundaria":
                    st.session_state.resultado_texto = "La célula perdió su agua y se arrugó por completo. La sal de afuera jaló el agua de adentro."
                    st.session_state.vidas -= 1
                elif nivel == "Preparatoria":
                    st.session_state.resultado_texto = "¡Fenómeno de Crenación Celular! El medio externo tiene mayor presión osmótica, obligando a la célula a deshidratarse."
                    st.session_state.vidas -= 1
                elif nivel == "Universidad":
                    st.session_state.resultado_texto = "ALERTA CLÍNICA: Choque osmótico celular. La alta concentración de sodio en el medio extracelular provoca la salida drástica de agua celular. Riesgo de deshidratación celular severa."
                    st.session_state.vidas -= 1
            
            st.rerun()

        # DISPLAY DE RESULTADOS (El Microscopio e Indicadores Virtuales)
        if st.session_state.simulacion_ejecutada:
            st.write("---")
            st.subheader("📊 Monitores del Microscopio Virtual")
            
            # Mostrar métricas del estado celular actual
            col1, col2 = st.columns(2)
            col1.metric(label="Morfología de la Célula", value=st.session_state.estado_celula)
            
            if "Normal" in st.session_state.estado_celula:
                st.success(st.session_state.resultado_texto)
            elif "Hinchada" in st.session_state.estado_celula:
                st.warning(st.session_state.resultado_texto)
            else:
                st.error(st.session_state.resultado_texto)
                
            if st.button("🔄 Sincronizar y Limpiar Tablero"):
                st.session_state.simulacion_ejecutada = False
                st.rerun()

    # Patrullaje manual opcional para el usuario
    st.write("---")
    if st.button("🔄 Verificar Estado de Conexión"):
        st.rerun()
