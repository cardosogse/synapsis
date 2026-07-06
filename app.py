import streamlit as st
import time

# 1. CONFIGURACIÓN DEL CHASIS DE NAVEGACIÓN
st.set_page_config(page_title="SynapsisLab", page_icon="🧠", layout="centered")

# --- ESTILOS CSS NATIVOS PARA ERGONOMÍA VISUAL PREMIUM ---
st.markdown("""
<style>
    /* Estilos globales de tipografía y fondos */
    .main-title {
        text-align: center; 
        color: #0288d1; 
        font-size: 3.8rem; 
        font-weight: 800; 
        letter-spacing: 3px;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center; 
        font-style: italic; 
        color: #666; 
        font-size: 1.1rem; 
        font-weight: 400;
        margin-top: 0px;
        margin-bottom: 5px;
    }
    .question-hook {
        text-align: center; 
        color: #0288d1; 
        font-size: 1.2rem; 
        font-weight: 600; 
        margin-top: 0px;
        margin-bottom: 25px;
    }
    /* Contenedores de la interfaz del Laboratorio */
    .console-header {
        background-color: #f8f9fa;
        border-left: 5px solid #0288d1;
        padding: 15px;
        border-radius: 4px;
        margin-bottom: 20px;
    }
    .spectrometer-card-success {
        background-color: #e8f5e9;
        border: 1px solid #c8e6c9;
        border-left: 6px solid #4caf50;
        padding: 20px;
        border-radius: 6px;
        margin-top: 15px;
    }
    .spectrometer-card-error {
        background-color: #ffebee;
        border: 1px solid #ffcdd2;
        border-left: 6px solid #f44336;
        padding: 20px;
        border-radius: 6px;
        margin-top: 15px;
    }
    .spectrometer-title {
        color: #333;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 8px;
    }
    /* Monitor de la barra lateral */
    .sidebar-monitor {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 12px;
        border-radius: 4px;
        margin-bottom: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- BITÁCORA GLOBAL COMPARTIDA (EL MURO DE ACERO ANTIPIRATERÍA) ---
@st.cache_resource
def obtener_base_datos_global():
    return {}  # Estructura: {"codigo_licencia": "session_id_del_ultimo_dispositivo"}

base_datos_global = obtener_base_datos_global()

# Licencias autorizadas para el Tronco Común de Ciencias de la Salud
CODIGOS_VIGENTES = ["SYNAPSIS-PRO", "VET-BIOQUIMICA-2026", "MED-ELITE-30DAYS"]

# Generar un ID único por pestaña de forma segura
if "mi_session_id" not in st.session_state:
    st.session_state["mi_session_id"] = str(time.time_ns())

# Estados locales de control de sesión
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
if "codigo_ingresado" not in st.session_state:
    st.session_state["codigo_ingresado"] = ""

# --- VARIABLES DE ESTADO LOCAL DEL LABORATORIO ---
if "vidas" not in st.session_state:
    st.session_state["vidas"] = 3
if "puntos" not in st.session_state:
    st.session_state["puntos"] = 0
if "bloque_actual" not in st.session_state:
    st.session_state["bloque_actual"] = 0  
if "simulacion_ejecutada" not in st.session_state:
    st.session_state["simulacion_ejecutada"] = False
if "resultado_texto" not in st.session_state:
    st.session_state["resultado_texto"] = ""
if "estado_sistema" not in st.session_state:
    st.session_state["estado_sistema"] = "En Espera"

# --- RADAR PASIVO DE PIRATERÍA (Background Polling optimizado) ---
@st.fragment(run_every=5)
def radar_seguridad_pasivo():
    if st.session_state["autenticado"]:
        codigo = st.session_state["codigo_ingresado"]
        if codigo in base_datos_global and base_datos_global[codigo] != st.session_state["mi_session_id"]:
            st.rerun()

def verificar_bloqueo_pirateria():
    if st.session_state["autenticado"]:
        codigo = st.session_state["codigo_ingresado"]
        if codigo in base_datos_global:
            if base_datos_global[codigo] != st.session_state["mi_session_id"]:
                st.session_state["autenticado"] = False
                st.session_state["codigo_ingresado"] = ""
                st.error("🚨 SUSPENSIÓN POR PIRATERÍA: Se detectó un doble inicio de sesión simultáneo. Tu acceso en este dispositivo ha sido revocado automáticamente.")
                st.stop()
        else:
            base_datos_global[codigo] = st.session_state["mi_session_id"]

# ========================================================
# --- FACHADA DE ACCESO PÚBLICA (DISEÑO GEOMÉTRICO LIMPIO) ---
# ========================================================
if not st.session_state["autenticado"]:
    st.markdown("<h1 class='main-title'>SYNAPSIS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-title'>Aprende rápido. Rompe las barreras biológicas.</p>", unsafe_style=True)
    st.markdown("<p class='question-hook'>¿Listo para aprender rápido con tu laboratorio digital?</p>", unsafe_style=True)
    
    st.write("---")
    
    # Contenedor estético para el Arte Digital de Redes Neuronales
    st.markdown("""
    <div style='background-color: #f1f8e9; border: 1px dashed #8bc34a; padding: 20px; text-align: center; border-radius: 4px; color: #33691e; font-size: 0.95rem; font-weight: 500;'>
        [Módulo de Interconexión Sináptica: Animación de Redes Neuronales Nativas en Desarrollo]
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <br>
    <h3 style='color: #333; font-weight: 600;'>Sincronización del Entorno Analítico</h3>
    Introduzca su clave de acceso individual de 30 días para validar el estado de matrícula y activar los reactores digitales de tronco común.
    """, unsafe_allow_html=True)
    
    codigo_input = st.text_input("Licencia de Acceso Digital (Token Único):", type="password", placeholder="Introduzca el código de suscripción...")
    
    if st.button("Activar Reactores Moleculares", use_container_width=True):
        codigo_limpio = codigo_input.strip().upper()
        if codigo_limpio in CODIGOS_VIGENTES:
            base_datos_global[codigo_limpio] = st.session_state["mi_session_id"]
            st.session_state["autenticado"] = True
            st.session_state["codigo_ingresado"] = codigo_limpio
            st.success("Conexión establecida con éxito. Sincronizando interfaz...")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Código de licencia inválido o expirado. Verifique su suscripción mensual.")

# ========================================================
# --- CONSOLA PRIVADA DE ESTUDIANTES (SynapsisLab) ---
# ========================================================
else:
    radar_seguridad_pasivo()
    verificar_bloqueo_pirateria()

    # Encabezado Ergonómico de la Consola
    st.markdown("""
    <div class='console-header'>
        <h2 style='margin:0; color: #01579b; font-weight: 700;'>SynapsisLab: Consola de Simulación</h2>
        <span style='color: #555; font-size: 0.85rem;'>Entorno Clínico Protegido | Matrícula Activa: {}</span>
    </div>
    """.format(st.session_state['codigo_ingresado']), unsafe_allow_html=True)
    
    # Barra lateral — Monitor de Signos Homeostáticos del Alumno
    with st.sidebar:
        st.markdown("<h3 style='color: #333; font-weight:600; margin-bottom:15px;'>Monitor de Estado</h3>", unsafe_allow_html=True)
        
        st.markdown("<div class='sidebar-monitor'><span style='font-size:0.8rem; color:#666; text-transform:uppercase;'>Estabilidad (Vidas)</span><br><b style='font-size:1.6rem; color:#d32f2f;'>{} / 3</b></div>".format(st.session_state.vidas), unsafe_allow_html=True)
        st.markdown("<div class='sidebar-monitor'><span style='font-size:0.8rem; color:#666; text-transform:uppercase;'>Rigor (Puntos)</span><br><b style='font-size:1.6rem; color:#1976d2;'>{}</b></div>".format(st.session_state.puntos), unsafe_allow_html=True)
        
        st.write("---")
        st.markdown("<h4 style='color: #333; font-weight:600;'>Navegación Curricular</h4>", unsafe_allow_html=True)
        
        # Selector de bloques temáticos integrados
        if st.sidebar.button("Bloque 0: Fundamentos Químicos", use_container_width=True):
            st.session_state.bloque_actual = 0
            st.session_state.simulacion_ejecutada = False
            st.rerun()
        if st.sidebar.button("Bloque 1: Agua y Equilibrio del pH", use_container_width=True):
            st.session_state.bloque_actual = 1
            st.session_state.simulacion_ejecutada = False
            st.rerun()
            
        st.write("---")
        if st.button("Desconectar Sesión de Forma Segura", use_container_width=True):
            if st.session_state["codigo_ingresado"] in base_datos_global:
                if base_datos_global[st.session_state["codigo_ingresado"]] == st.session_state["mi_session_id"]:
                    del base_datos_global[st.session_state["codigo_ingresado"]]
            st.session_state["autenticado"] = False
            st.rerun()

    # SISTEMA LOGICIAL DE CONTROL DE ESTADO (Game Over)
    if st.session_state.vidas <= 0:
        st.markdown("""
        <div class='spectrometer-card-error'>
            <div class='spectrometer-title' style='color:#c62828;'>Falla Homeostática Crítica</div>
            El sistema ha entrado en inestabilidad irreversible debido a decisiones experimentales erróneas. El reactor se ha bloqueado.
        </div>
        """, unsafe_allow_html=True)
        if st.button("Inyectar Nuevos Reactores Extracelulares y Reiniciar", use_container_width=True):
            st.session_state.vidas = 3
            st.session_state.puntos = 0
            st.session_state.simulacion_ejecutada = False
            st.session_state.estado_sistema = "En Espera"
            st.rerun()
            
    else:
        # ========================================================
        # --- DESPLIEGUE CONTINUO: BLOQUE 0 (FUNDAMENTOS) ---
        # ========================================================
        if st.session_state.bloque_actual == 0:
            st.subheader("Ficha de Protocolo 0: Enlaces y Electronegatividad")
            
            with st.expander("Ver Sustento Teórico del Enlace Bioquímico", expanded=True):
                st.markdown("""
                Los sistemas vivos están estructurados a partir del ensamblaje de bioelementos primarios (**CHON**). 
                La interacción espacial de estos átomos depende estrictamente de su **Electronegatividad** (la fuerza molecular para atraer electrones).
                * **Oxígeno (3.44) y Nitrógeno (3.04):** Elementos con alta densidad y ambición electrónica en sistemas biológicos.
                * **Carbono (2.55) y Hidrógeno (2.20):** Elementos con baja fuerza de atracción.
                
                **Consecuencias en la materia viva:**
                1. **Enlace Covalente Polar:** Ocurre al unir elementos con gran diferencia de electronegatividad (ej. O-H). Los electrones se desplazan asimétricamente, generando un **dipolo eléctrico** (pequeños imanes). Es la base hidrofílica que permite al agua interactuar con solutos.
                2. **Enlace Covalente No Polar:** Los electrones se comparten simétricamente (ej. C-H) debido a fuerzas similares. El enlace es eléctricamente neutro e hidrofóbico (base estructural de las membranas lipídicas).
                """)

            st.write("---")
            st.markdown("<h3 style='color:#333; font-weight:600;'>Reactor de Enlaces Moleculares</h3>", unsafe_allow_html=True)
            st.write("Configure la combinación atómica elemental del ensayo analítico:")
            
            col1, col2 = st.columns(2)
            with col1:
                atomo_1 = st.selectbox("Elemento Primario del Núcleo:", ["Oxígeno (Fuerza: 3.44)", "Carbono (Fuerza: 2.55)"])
            with col2:
                atomo_2 = st.selectbox("Elemento de Interacción Orbital:", ["Hidrógeno (Fuerza: 2.20)", "Oxígeno (Fuerza: 3.44)"])
                
            if st.button("Disparar Reacción Térmica", use_container_width=True):
                st.session_state.simulacion_ejecutada = True
                verificar_bloqueo_pirateria()
                
                es_polar = "Oxígeno" in atomo_1 and "Hidrógeno" in atomo_2
                es_apolar = "Carbono" in atomo_1 and "Hidrógeno" in atomo_2
                es_error = "Oxígeno" in atomo_1 and "Oxígeno" in atomo_2
                
                if es_polar:
                    st.session_state.estado_sistema = "Enlace Covalente Polar (Dipolo Eléctrico Activo)"
                    st.session_state.resultado_texto = "Análisis molecular impecable. La asimetría en la densidad electrónica deforma la nube orbital. El Oxígeno retiene la carga parcial negativa y el Hidrógeno la positiva, estructurando el dipolo que fundamenta los puentes de hidrógeno."
                    st.session_state.puntos += 100
                elif es_apolar:
                    st.session_state.estado_sistema = "Enlace Covalente No Polar (Geometría Simétrica)"
                    st.session_state.resultado_texto = "Configuración correcta. Las fuerzas del Carbono y el Hidrógeno se equilibran en el centro geométrico del enlace. La AWSencia de cargas netas produce un compuesto hidrofóbico, componente clave para la estabilidad de las bicapas lipídicas corporales."
                    st.session_state.puntos += 100
                elif es_error:
                    st.session_state.estado_sistema = "Molécula Gaseosa Homogénea (O2)"
                    st.session_state.resultado_texto = "Conflicto de variables en fluidos. Ambos átomos poseen idéntica afinidad electrónica, compartiendo el par de electrones de forma perfectamente simétrica. Produce oxígeno molecular (O₂), vital para la fosforilación oxidativa celular, pero incapaz de disolverse o interactuar de forma dipolar con solventes orgánicos. Pérdida de estabilidad estructural."
                    st.session_state.vidas -= 1
                st.rerun()

        # ========================================================
        # --- DESPLIEGUE CONTINUO: BLOQUE 1 (AGUA Y PH) ---
        # ========================================================
        elif st.session_state.bloque_actual == 1:
            st.subheader("Ficha de Protocolo 1: Dinámica del Agua y Equilibrio del pH")
            
            with st.expander("Ver Sustento Teórico de la Disociación Iónica", expanded=True):
                st.markdown("""
                El agua ($H_2O$) representa el disolvente universal de la homeostasis biológica. Debido a su carácter dipolar (repasado en el Bloque 0), tiene la capacidad de disociarse de forma reversible en **iones hidronio ($H^+$)** y **iones oxhidrilo ($OH^-$)**.
                
                $$\gamma: H_2O \rightleftharpoons H^+ + OH^-$$
                
                La concentración libre de estos iones de hidrógeno determina el **pH** del medio interno. El rango de estabilidad vital de la sangre se ubica estrictamente entre **7.35 y 7.45**. Desviaciones fuera de estos límites alteran la carga eléctrica de los aminoácidos y desnaturalizan las enzimas del metabolismo. Para evitarlo, el cuerpo utiliza **sistemas amortiguadores o tampón**, siendo el principal el sistema de **Bicarbonato / Ácido Carbónico**.
                """)

            st.write("---")
            st.markdown("<h3 style='color:#333; font-weight:600;'>Analizador de Amortiguación Extracelular</h3>", unsafe_allow_html=True)
            st.write("Inyecte soluciones analíticas en el plasma químico simulado:")
            
            solucion_inyectada = st.selectbox(
                "Seleccione la solución de infusión y el estado del medio interno:",
                [
                    "Ácido Clorhídrico (HCl) puro inyectado en Agua Destilada neutra",
                    "Ácido Clorhídrico (HCl) inyectado en Plasma con Amortiguador Bicarbonato (HCO3-)",
                    "Hidróxido de Sodio (NaOH) puro inyectado en Plasma sin sistemas amortiguadores"
                ]
            )
            
            if st.button("Confirmar Infusión Química", use_container_width=True):
                st.session_state.simulacion_ejecutada = True
                verificar_bloqueo_pirateria()
                
                if "Agua Destilada" in solucion_inyectada:
                    st.session_state.estado_sistema = "Acidosis Plasmática Crítica (pH = 2.0)"
                    st.session_state.resultado_texto = "Falla del medio interno. El HCl es un ácido fuerte que se disocia por completo liberando un exceso masivo de protones (H+). Al carecer de un sistema tampón que capture estos iones, el pH colapsa de forma instantánea, provocando la pérdida de la estructura terciaria de las proteínas funcionales."
                    st.session_state.vidas -= 1
                elif "Amortiguador Bicarbonato" in solucion_inyectada:
                    st.session_state.estado_sistema = "Homeostasis Sanguínea Estable (pH = 7.4)"
                    st.session_state.resultado_texto = "Compensación química exitosa. Siguiendo el principio de Le Chatelier, las moléculas de Bicarbonato capturan el exceso de protones del ácido fuerte, convirtiéndolos en Ácido Carbónico débil. Este se disocia rápidamente en agua y CO₂, permitiendo la eliminación del exceso de acidez por vía respiratoria."
                    st.session_state.puntos += 150
                elif "Hidróxido de Sodio" in solucion_inyectada:
                    st.session_state.estado_sistema = "Alcalosis Metabólica Severa (pH = 11.0)"
                    st.session_state.resultado_texto = "Desequilibrio catiónico. El NaOH libera grupos oxhidrilo (OH-) que secuestran los protones libres del sistema. Sin amortiguadores que cedan H+ para compensar la pérdida, el pH se dispara críticamente hacia la alcalinidad, rompiendo los puentes de hidrógeno intra-moleculares."
                    st.session_state.vidas -= 1
                st.rerun()

        # ========================================================
        # --- ESPECTRÓMETRO DIGITAL (MONITOR DE SALIDA UNIFICADO) ---
        # ========================================================
        if st.session_state.simulacion_ejecutada:
            st.write("---")
            
            es_error_sistema = "Molécula Gaseosa" in st.session_state.estado_sistema or "Crítica" in st.session_state.estado_sistema or "Severa" in st.session_state.estado_sistema
            
            if es_error_sistema:
                st.markdown(f"""
                <div class='spectrometer-card-error'>
                    <div class='spectrometer-title' style='color:#c62828;'>Lectura del Espectrómetro: Anomalía en el Medio</div>
                    <strong style='font-size:1.1rem; color:#b71c1c;'>Estatus: {st.session_state.estado_sistema}</strong><br><br>
                    {st.session_state.resultado_texto}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='spectrometer-card-success'>
                    <div class='spectrometer-title' style='color:#2e7d32;'>Lectura del Espectrómetro: Estabilidad Óptima</div>
                    <strong style='font-size:1.1rem; color:#1b5e20;'>Estatus: {st.session_state.estado_sistema}</strong><br><br>
                    {st.session_state.resultado_texto}
                </div>
                """, unsafe_allow_html=True)
                
            st.write("")
            if st.button("Limpiar Cámara de Inyección del Reactor", use_container_width=True):
                st.session_state.simulacion_ejecutada = False
                st.rerun()

    st.write("---")
    if st.button("Sincronizar Canales de Red Electroquímica"):
        st.rerun()
