import streamlit as st
import json
import time
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Examen AWS Cloud Practitioner",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para tema claro
st.markdown("""
    <style>
    /* Forzar tema claro */
    .stApp {
        background-color: #FFFFFF;
        color: #000000;
    }
    
    /* Encabezados en negro */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }
    
    /* Texto en negro */
    p, div, span, label {
        color: #000000 !important;
    }
    
    /* Botones con mejor contraste */
    .stButton button {
        background-color: #0066CC;
        color: white !important;
    }
    
    .stButton button[kind="primary"] {
        background-color: #FF9900;
        color: white !important;
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        color: #000000 !important;
    }
    
    /* Input fields */
    .stNumberInput input {
        background-color: #F5F5F5;
        color: #000000 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #F0F0F0;
        color: #000000 !important;
    }
    
    /* Markdown */
    .element-container {
        color: #000000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar preguntas desde JSON
@st.cache_data
def cargar_preguntas():
    with open('preguntas_aws.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    # El archivo JSON contiene directamente una lista de preguntas
    return data

# Inicializar estado de la sesión
def inicializar_sesion():
    if 'iniciado' not in st.session_state:
        st.session_state.iniciado = False
    if 'pregunta_actual' not in st.session_state:
        st.session_state.pregunta_actual = 0
    if 'respuestas_usuario' not in st.session_state:
        st.session_state.respuestas_usuario = {}
    if 'tiempo_inicio_pregunta' not in st.session_state:
        st.session_state.tiempo_inicio_pregunta = None
    if 'finalizado' not in st.session_state:
        st.session_state.finalizado = False
    if 'num_preguntas' not in st.session_state:
        st.session_state.num_preguntas = 10
    if 'tiempo_por_pregunta' not in st.session_state:
        st.session_state.tiempo_por_pregunta = 83  # 1 minuto 23 segundos
    if 'preguntas_examen' not in st.session_state:
        st.session_state.preguntas_examen = []

def navegar_pregunta(direccion):
    """Navegar entre preguntas"""
    nueva_posicion = st.session_state.pregunta_actual + direccion
    if 0 <= nueva_posicion < len(st.session_state.preguntas_examen):
        st.session_state.pregunta_actual = nueva_posicion
        st.session_state.tiempo_inicio_pregunta = time.time()

def seleccionar_respuesta(indice_pregunta, respuesta):
    """Guardar la respuesta del usuario"""
    st.session_state.respuestas_usuario[indice_pregunta] = respuesta

def calcular_resultado():
    """Calcular el resultado del examen"""
    correctas = 0
    total = len(st.session_state.preguntas_examen)
    
    for idx, pregunta in enumerate(st.session_state.preguntas_examen):
        respuesta_usuario = st.session_state.respuestas_usuario.get(idx)
        if respuesta_usuario == pregunta['respuesta_correcta']:
            correctas += 1
    
    return correctas, total

def mostrar_configuracion():
    """Mostrar pantalla de configuración del examen"""
    st.title("⚙️ Configuración del Examen AWS")
    st.markdown("---")
    
    todas_preguntas = cargar_preguntas()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.num_preguntas = st.number_input(
            "Número de preguntas",
            min_value=1,
            max_value=len(todas_preguntas),
            value=10,
            step=1,
            help=f"Hay {len(todas_preguntas)} preguntas disponibles"
        )
    
    with col2:
        st.session_state.tiempo_por_pregunta = st.number_input(
            "Tiempo por pregunta (segundos)",
            min_value=10,
            max_value=300,
            value=83,  # 1 minuto 23 segundos por defecto
            step=1,
            help="Tiempo límite para responder cada pregunta (por defecto: 1min 23seg)"
        )
    
    st.markdown("---")
    
    if st.button("🚀 Comenzar Examen", use_container_width=True, type="primary"):
        # Seleccionar preguntas aleatorias
        import random
        st.session_state.preguntas_examen = random.sample(
            todas_preguntas, 
            st.session_state.num_preguntas
        )
        st.session_state.iniciado = True
        st.session_state.tiempo_inicio_pregunta = time.time()
        st.rerun()

def mostrar_examen():
    """Mostrar la interfaz del examen"""
    pregunta_idx = st.session_state.pregunta_actual
    pregunta = st.session_state.preguntas_examen[pregunta_idx]
    
    # Header con información
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.title(f"☁️ Examen AWS - Pregunta {pregunta_idx + 1} de {len(st.session_state.preguntas_examen)}")
    
    with col2:
        contestadas = len(st.session_state.respuestas_usuario)
        st.metric("Respondidas", f"{contestadas}/{len(st.session_state.preguntas_examen)}")
    
    with col3:
        # Temporizador
        tiempo_transcurrido = int(time.time() - st.session_state.tiempo_inicio_pregunta)
        tiempo_restante = max(0, st.session_state.tiempo_por_pregunta - tiempo_transcurrido)
        
        if tiempo_restante > 10:
            st.metric("⏱️ Tiempo", f"{tiempo_restante}s")
        else:
            st.metric("⏱️ Tiempo", f"{tiempo_restante}s", delta="¡Apúrate!")
    
    st.markdown("---")
    
    # Mostrar pregunta
    st.markdown(f"### {pregunta['pregunta']}")
    st.markdown("")
    
    # Mostrar opciones
    respuesta_actual = st.session_state.respuestas_usuario.get(pregunta_idx)
    
    # Las opciones vienen como diccionario {'A': '...', 'B': '...', etc}
    opciones = pregunta['opciones']
    for letra in sorted(opciones.keys()):
        if st.button(
            f"**{letra})** {opciones[letra]}",
            key=f"opcion_{pregunta_idx}_{letra}",
            use_container_width=True,
            type="primary" if respuesta_actual == letra else "secondary"
        ):
            seleccionar_respuesta(pregunta_idx, letra)
            st.rerun()
    
    st.markdown("---")
    
    # Navegación
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if pregunta_idx > 0:
            if st.button("⬅️ Anterior", use_container_width=True):
                navegar_pregunta(-1)
                st.rerun()
    
    with col2:
        if pregunta_idx < len(st.session_state.preguntas_examen) - 1:
            if st.button("➡️ Siguiente", use_container_width=True):
                navegar_pregunta(1)
                st.rerun()
    
    with col4:
        if st.button("✅ Finalizar Examen", use_container_width=True, type="primary"):
            st.session_state.finalizado = True
            st.rerun()
    
    # Mapa de preguntas
    st.markdown("---")
    st.markdown("### 🗺️ Mapa de Preguntas")
    
    # Mostrar botones para todas las preguntas
    cols = st.columns(10)
    for idx in range(len(st.session_state.preguntas_examen)):
        col_idx = idx % 10
        with cols[col_idx]:
            respondida = idx in st.session_state.respuestas_usuario
            es_actual = idx == pregunta_idx
            
            emoji = "✅" if respondida else "⭕"
            tipo = "primary" if es_actual else ("secondary" if respondida else "secondary")
            
            if st.button(
                f"{emoji} {idx + 1}",
                key=f"nav_{idx}",
                use_container_width=True,
                type=tipo if es_actual else "secondary"
            ):
                st.session_state.pregunta_actual = idx
                st.session_state.tiempo_inicio_pregunta = time.time()
                st.rerun()

def mostrar_resultados():
    """Mostrar resultados del examen"""
    st.title("📊 Resultados del Examen")
    st.markdown("---")
    
    correctas, total = calcular_resultado()
    porcentaje = (correctas / total) * 100
    
    # Métricas principales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("✅ Respuestas Correctas", correctas)
    
    with col2:
        st.metric("❌ Respuestas Incorrectas", total - correctas)
    
    with col3:
        st.metric("📈 Porcentaje", f"{porcentaje:.1f}%")
    
    # Calificación
    st.markdown("---")
    if porcentaje > 70:  # Solo aprueba si SUPERA el 70%
        st.success(f"### 🎉 ¡APROBADO! - {porcentaje:.1f}%")
        st.balloons()
    else:
        st.error(f"### 😔 No Aprobado - {porcentaje:.1f}%")
        st.info("ℹ️ Necesitas superar el 70% para aprobar")
    
    st.markdown("---")
    
    # Detalles de cada pregunta
    st.markdown("### 📝 Revisión Detallada")
    
    for idx, pregunta in enumerate(st.session_state.preguntas_examen):
        respuesta_usuario = st.session_state.respuestas_usuario.get(idx, "Sin responder")
        respuesta_correcta = pregunta['respuesta_correcta']
        es_correcta = respuesta_usuario == respuesta_correcta
        
        with st.expander(
            f"Pregunta {idx + 1} - {'✅ Correcta' if es_correcta else '❌ Incorrecta' if respuesta_usuario != 'Sin responder' else '⚠️ Sin responder'}"
        ):
            st.markdown(f"**{pregunta['pregunta']}**")
            st.markdown("")
            
            # Las opciones vienen como diccionario {'A': '...', 'B': '...', etc}
            opciones = pregunta['opciones']
            for letra in sorted(opciones.keys()):
                if letra == respuesta_correcta:
                    st.success(f"✅ **{letra})** {opciones[letra]} (Correcta)")
                elif letra == respuesta_usuario and respuesta_usuario != respuesta_correcta:
                    st.error(f"❌ **{letra})** {opciones[letra]} (Tu respuesta)")
                else:
                    st.markdown(f"**{letra})** {opciones[letra]}")
    
    st.markdown("---")
    
    # Botones de acción
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Realizar Nuevo Examen", use_container_width=True, type="primary"):
            # Reiniciar todo
            st.session_state.clear()
            st.rerun()
    
    with col2:
        if st.button("⚙️ Cambiar Configuración", use_container_width=True):
            st.session_state.iniciado = False
            st.session_state.finalizado = False
            st.session_state.pregunta_actual = 0
            st.session_state.respuestas_usuario = {}
            st.rerun()

# Programa principal
def main():
    inicializar_sesion()
    
    if not st.session_state.iniciado:
        mostrar_configuracion()
    elif st.session_state.finalizado:
        mostrar_resultados()
    else:
        mostrar_examen()
        # Auto-refresh cada segundo para actualizar el temporizador
        time.sleep(0.1)
        st.rerun()

if __name__ == "__main__":
    main()