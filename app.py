import streamlit as st
import time

# 1. CONFIGURACIÓN DEL CHASIS DE NAVEGACIÓN NATIVA
st.set_page_config(page_title="ChonpsLab", page_icon="⚛️", layout="centered")

# --- OPTIMIZADOR 1: MOTOR DE DIAGRAMAS VECTORIALES NATIVOS (SVG BAJO EN RAM) ---
@st.cache_data
def obtener_diagrama_vectorial(tipo_evento):
    """
    Base de datos gráfica congelada en caché. Genera estructuras vectoriales (SVG)
    diseñadas específicamente para el contraste en modo oscuro.
    """
    diagramas = {
        "polar": """
        <div style='display: flex; justify-content: center; align-items: center; width: 100%; height: 120px;'>
            <svg viewBox="0 0 240 120" width="100%" height="100%" style="background: transparent;">
                <circle cx="70" cy="60" r="28" fill="#ff5252" opacity="0.85"/>
                <text x="63" y="66" fill="white" font-weight="bold" font-family="sans-serif" font-size="16">O</text>
                <text x="35" y="35" fill="#ff5252" font-weight="bold" font-family="sans-serif" font-size="14">δ⁻</text>
                
                <circle cx="170" cy="60" r="14" fill="#00e5ff" opacity="0.85"/>
                <text x="164" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="12">H</text>
                <text x="175" y="35" fill="#00e5ff" font-weight="bold" font-family="sans-serif" font-size="14">δ⁺</text>
                
                <ellipse cx="105" cy="60" rx="60" ry="38" fill="none" stroke="#00e5ff" stroke-width="1.5" stroke-dasharray="4 3"/>
                <circle cx="115" cy="60" r="4" fill="#00e5ff"/>
                <circle cx="125" cy="60" r="4" fill="#00e5ff"/>
            </svg>
        </div>
        """,
        "apolar": """
        <div style='display: flex; justify-content: center; align-items: center; width: 100%; height: 120px;'>
            <svg viewBox="0 0 240 120" width="100%" height="100%" style="background: transparent;">
                <circle cx="70" cy="60" r="24" fill="#ffb142" opacity="0.85"/>
                <text x="63" y="66" fill="black" font-weight="bold" font-family="sans-serif" font-size="15">C</text>
                
                <circle cx="170" cy="60" r="14" fill="#00e5ff" opacity="0.85"/>
                <text x="164" y="65" fill="black" font-weight="bold" font-family="sans-serif" font-size="12">H</text>
                
                <ellipse cx="120" cy="60" rx="68" ry="32" fill="none" stroke="#b0bec5" stroke-width="1.5" stroke-dasharray="2 2"/>
                <circle cx="115" cy="60" r="4" fill="#ffffff"/>
                <circle cx="125" cy="60" r="4" fill="#ffffff"/>
            </svg>
        </div>
        """,
        "o2_gas": """
        <div style='display: flex; justify-content: center; align-items: center; width: 100%; height: 120px;'>
            <svg viewBox="0 0 240 120" width="100%" height="100%" style="background: transparent;">
                <circle cx="75" cy="60" r="24" fill="#ff5252" opacity="0.7"/>
                <text x="69" y="65" fill="white" font-weight="bold" font-family="sans-serif" font-size="14">O</text>
                
                <circle cx="165" cy="60" r="24" fill="#ff5252" opacity="0.7"/>
                <text x="159" y="65" fill="white" font-weight="bold" font-family="sans-serif" font-size="14">O</text>
                
                <line x1="105" y1="55" x2="135" y2="55" stroke="#ffffff" stroke-width="2"/>
                <line x1="105" y1="65" x2="135" y2="65" stroke="#ffffff" stroke-width="2"/>
            </svg>
        </div>
        """,
        "disociacion_agua": """
        <div style='display: flex; justify-content: center; align-items: center; width: 100%; height: 120px;'>
            <svg viewBox="0 0 260 120" width="100%" height="100%" style="background: transparent;">
                <g transform="translate(10, 0)">
                    <circle
