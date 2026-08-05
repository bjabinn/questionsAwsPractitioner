import streamlit as st
import json
import glob
import time
from datetime import datetime, timedelta

# Configuración de la página
st.set_page_config(
    page_title="Examen de Certificaciones",
    page_icon="📝",
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
        background-color: #F0F7FF;
        color: #000000 !important;
        border: 2px solid #3399FF;
    }
    
    .stButton button[kind="primary"] {
        background-color: #0095ff;
        color: white !important;
    }
    
    /* Métricas */
    [data-testid="stMetricLabel"] {
        display: none !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #808080 !important;
        margin-top: -19px !important;
    }
    
    /* Etiquetas de los widgets: distintivo visual para accesibilidad */
    [data-testid="stWidgetLabel"] {
        border-left: 3px solid #0095FF;
        padding-left: 8px;
        margin-bottom: 4px;
    }

    [data-testid="stWidgetLabel"] p {
        font-weight: 600 !important;
        color: #000000 !important;
    }

    /* Selectbox (combo de certificación) */
    [data-testid="stSelectbox"] [role="group"] {
        background-color: #FFFFFF !important;
        border: 1px solid #999999 !important;
        border-radius: 4px !important;
    }

    [data-testid="stSelectbox"]:focus-within [role="group"] {
        border-color: #0095FF !important;
        box-shadow: 0 0 0 1px #0095FF !important;
    }

    [data-testid="stSelectbox"] input {
        color: #000000 !important;
    }

    [data-testid="stSelectbox"] svg {
        fill: #000000 !important;
    }

    /* Menú desplegable del selectbox (se renderiza en un portal aparte) */
    [role="listbox"] {
        background-color: #FFFFFF !important;
        border: 1px solid #CCCCCC !important;
    }

    [role="option"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    [role="option"]:hover,
    [role="option"][aria-selected="true"] {
        background-color: #F0F7FF !important;
    }

    /* Number input (número de preguntas) */
    [data-testid="stNumberInputContainer"] {
        background-color: #F5F5F5 !important;
        border: 1px solid #999999 !important;
        border-radius: 4px !important;
    }

    [data-testid="stNumberInputContainer"]:focus-within {
        border-color: #0095FF !important;
        box-shadow: 0 0 0 1px #0095FF !important;
    }

    [data-testid="stNumberInputField"] {
        background-color: transparent !important;
        color: #000000 !important;
    }

    /* Botones +/- del number input */
    [data-testid="stNumberInputStepDown"],
    [data-testid="stNumberInputStepUp"] {
        background-color: #F0F7FF !important;
        border: 1px solid #3399FF !important;
        border-radius: 4px !important;
        color: #000000 !important;
    }

    [data-testid="stNumberInputStepDown"]:hover,
    [data-testid="stNumberInputStepUp"]:hover {
        background-color: #0095FF !important;
    }

    [data-testid="stNumberInputStepDown"]:hover svg,
    [data-testid="stNumberInputStepUp"]:hover svg {
        fill: #FFFFFF !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #F0F0F0;
        color: #000000 !important;
    }
    
    [data-testid="stExpanderDetails"] {
        background-color: #FFFFFF !important;
    }
    
    [data-testid="stExpanderDetails"] p,
    [data-testid="stExpanderDetails"] div,
    [data-testid="stExpanderDetails"] span,
    [data-testid="stExpanderDetails"] strong,
    [data-testid="stExpanderDetails"] [data-testid="stMarkdownContainer"] {
        background-color: transparent !important;
        color: #000000 !important;
    }
    
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
    }
    
    /* Markdown */
    .element-container {
        color: #000000 !important;
    }

    /* Opciones de respuesta: alinear texto a la izquierda */
    .st-key-opciones_respuesta .stButton button,
    .st-key-opciones_respuesta .stButton button > div,
    .st-key-opciones_respuesta .stButton button > div > span {
        justify-content: flex-start !important;
        text-align: left !important;
    }

    .st-key-opciones_respuesta .stButton button p {
        text-align: left !important;
    }

    .st-key-opciones_respuesta [data-testid="stCheckbox"] label {
        justify-content: flex-start !important;
        text-align: left !important;
    }
    </style>
""", unsafe_allow_html=True)

# Cargar una certificación (metadata + preguntas) desde su fichero JSON
@st.cache_data
def cargar_certificacion(ruta_fichero):
    with open(ruta_fichero, 'r', encoding='utf-8') as f:
        return json.load(f)

# Descubrir certificaciones disponibles escaneando la carpeta preguntas/
# TTL corto para que una certificación añadida en caliente aparezca sin reiniciar el servidor
@st.cache_data(ttl=30)
def descubrir_certificaciones():
    certificaciones = []
    for ruta in sorted(glob.glob('preguntas/*.json')):
        data = cargar_certificacion(ruta)
        meta = data['certificacion']
        certificaciones.append({
            'id': meta['id'],
            'nombre': meta['nombre'],
            'codigo': meta.get('codigo', ''),
            'nota_corte': meta.get('nota_corte', 70),
            'duracion_minutos': meta.get('duracion_minutos', 90),
            'num_preguntas_examen': meta.get('num_preguntas_examen', 65),
            'ruta': ruta,
            'num_preguntas': len(data['preguntas']),
        })
    certificaciones.sort(key=lambda c: c['nombre'])
    return certificaciones

# Inicializar estado de la sesión
def inicializar_sesion():
    if 'iniciado' not in st.session_state:
        st.session_state.iniciado = False
    if 'pregunta_actual' not in st.session_state:
        st.session_state.pregunta_actual = 0
    if 'respuestas_usuario' not in st.session_state:
        st.session_state.respuestas_usuario = {}
    if 'tiempo_inicio_examen' not in st.session_state:
        st.session_state.tiempo_inicio_examen = None
    if 'finalizado' not in st.session_state:
        st.session_state.finalizado = False
    if 'num_preguntas' not in st.session_state:
        st.session_state.num_preguntas = 10
    if 'tiempo_total_minutos' not in st.session_state:
        st.session_state.tiempo_total_minutos = 90  # Tiempo total en minutos
    if 'preguntas_examen' not in st.session_state:
        st.session_state.preguntas_examen = []
    if 'cert_seleccionada_id' not in st.session_state:
        st.session_state.cert_seleccionada_id = None
    if 'cert_activa' not in st.session_state:
        st.session_state.cert_activa = None
    if 'nota_corte' not in st.session_state:
        st.session_state.nota_corte = 70

def navegar_pregunta(direccion):
    """Navegar entre preguntas"""
    nueva_posicion = st.session_state.pregunta_actual + direccion
    if 0 <= nueva_posicion < len(st.session_state.preguntas_examen):
        st.session_state.pregunta_actual = nueva_posicion

def seleccionar_respuesta(indice_pregunta, respuesta):
    """Guardar la respuesta del usuario"""
    st.session_state.respuestas_usuario[indice_pregunta] = respuesta

def seleccionar_respuesta_multiple(indice_pregunta, letra, estado):
    """Guardar respuestas múltiples del usuario"""
    if indice_pregunta not in st.session_state.respuestas_usuario:
        st.session_state.respuestas_usuario[indice_pregunta] = []
    
    respuestas = st.session_state.respuestas_usuario[indice_pregunta]
    
    if estado and letra not in respuestas:
        respuestas.append(letra)
    elif not estado and letra in respuestas:
        respuestas.remove(letra)
    
    st.session_state.respuestas_usuario[indice_pregunta] = respuestas

def es_pregunta_multiple(pregunta):
    """Verificar si una pregunta tiene múltiples respuestas correctas"""
    return ',' in pregunta['respuesta_correcta']

def calcular_resultado():
    """Calcular el resultado del examen"""
    correctas = 0
    total = len(st.session_state.preguntas_examen)
    
    for idx, pregunta in enumerate(st.session_state.preguntas_examen):
        respuesta_usuario = st.session_state.respuestas_usuario.get(idx)
        respuesta_correcta = pregunta['respuesta_correcta']
        
        # Verificar si es pregunta múltiple
        if es_pregunta_multiple(pregunta):
            # Comparar sets de respuestas
            respuestas_correctas_set = set(respuesta_correcta.split(','))
            respuestas_usuario_set = set(respuesta_usuario) if respuesta_usuario else set()
            
            if respuestas_correctas_set == respuestas_usuario_set:
                correctas += 1
        else:
            # Pregunta de una sola respuesta
            if respuesta_usuario == respuesta_correcta:
                correctas += 1
    
    return correctas, total

def mostrar_configuracion():
    """Mostrar pantalla de configuración del examen"""
    st.title("⚙️ Configura tu Examen")
    st.markdown("---")

    certificaciones = descubrir_certificaciones()

    if not certificaciones:
        st.error(
            "No se encontró ninguna certificación en la carpeta 'preguntas/'. "
            "Añade al menos un fichero JSON con el esquema esperado."
        )
        return

    nombres = [c['nombre'] for c in certificaciones]
    indice_por_defecto = 0
    if st.session_state.cert_seleccionada_id:
        for i, c in enumerate(certificaciones):
            if c['id'] == st.session_state.cert_seleccionada_id:
                indice_por_defecto = i
                break

    nombre_elegido = st.selectbox(
        "Certificación",
        nombres,
        index=indice_por_defecto
    )
    cert = next(c for c in certificaciones if c['nombre'] == nombre_elegido)
    st.session_state.cert_seleccionada_id = cert['id']

    col1, col2 = st.columns(2)

    with col1:
        num_preguntas_seleccionadas = st.number_input(
            "Número de preguntas",
            min_value=1,
            max_value=cert['num_preguntas'],
            value=min(65, cert['num_preguntas']),
            step=1,
            help=f"Hay {cert['num_preguntas']} preguntas disponibles"
        )
        st.session_state.num_preguntas = num_preguntas_seleccionadas
    
    with col2:
        # Calcular tiempo total proporcional al formato oficial de la certificación
        # (p.ej. AWS CLF-C02: 65 preguntas / 90 min; Claude CAF: 60 preguntas / 120 min)
        tiempo_total_minutos = (num_preguntas_seleccionadas / cert['num_preguntas_examen']) * cert['duracion_minutos']
        st.session_state.tiempo_total_minutos = tiempo_total_minutos
        
        # Calcular tiempo por pregunta en segundos (para uso interno)
        st.session_state.tiempo_por_pregunta = int((tiempo_total_minutos * 60) / num_preguntas_seleccionadas)
        
        # Mostrar tiempo total como métrica informativa (sin botones + y -)
        st.markdown("<div style='text-align: right;'><strong>Duración máxima del examen</strong></div>", unsafe_allow_html=True)
        
        # Formatear tiempo en minutos y segundos
        minutos_enteros = int(tiempo_total_minutos)
        segundos = int((tiempo_total_minutos - minutos_enteros) * 60)
        
        if segundos > 0:
            tiempo_formateado = f"{minutos_enteros}Min {segundos}segundos"
        else:
            tiempo_formateado = f"{minutos_enteros}Min"
        
        st.markdown(f"<div style='text-align: right; color: #808080; font-size: 2.5rem; margin-top: -19px;'>{tiempo_formateado}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.button("🚀 Comenzar Examen", use_container_width=True, type="primary"):
        # Seleccionar preguntas aleatorias de la certificación elegida
        import random
        todas_preguntas = cargar_certificacion(cert['ruta'])['preguntas']
        st.session_state.preguntas_examen = random.sample(
            todas_preguntas,
            st.session_state.num_preguntas
        )
        st.session_state.cert_activa = cert
        st.session_state.nota_corte = cert['nota_corte']
        st.session_state.iniciado = True
        st.session_state.tiempo_inicio_examen = time.time()
        st.rerun()

def mostrar_examen():
    """Mostrar la interfaz del examen"""
    pregunta_idx = st.session_state.pregunta_actual
    pregunta = st.session_state.preguntas_examen[pregunta_idx]
    
    # Header con información
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        nombre_cert = st.session_state.cert_activa['nombre']
        st.title(f"📝 Examen {nombre_cert} - Pregunta {pregunta_idx + 1} de {len(st.session_state.preguntas_examen)}")
    
    with col2:
        contestadas = len(st.session_state.respuestas_usuario)
        st.metric("Respondidas", f"{contestadas}/{len(st.session_state.preguntas_examen)}")
    
    with col3:
        # Temporizador global del examen
        tiempo_total_segundos = int(st.session_state.tiempo_total_minutos * 60)
        tiempo_transcurrido = int(time.time() - st.session_state.tiempo_inicio_examen)
        tiempo_restante = max(0, tiempo_total_segundos - tiempo_transcurrido)
        
        # Mostrar en minutos y segundos
        if tiempo_restante >= 60:
            mins = tiempo_restante // 60
            segs = tiempo_restante % 60
            tiempo_display = f"{mins}:{segs:02d}"
        else:
            tiempo_display = f"{tiempo_restante}s"
        
        # Cambiar color cuando queden menos de 5 minutos
        if tiempo_restante > 300:  # Más de 5 minutos
            st.metric("⏱️ Tiempo Restante", tiempo_display)
        else:
            st.metric("⏱️ Tiempo Restante", tiempo_display, delta="¡Apúrate!")
    
    st.markdown("---")
    
    # Mostrar pregunta
    st.markdown(f"### {pregunta['pregunta']}")
    st.markdown("")
    
    # Verificar si es pregunta múltiple
    es_multiple = es_pregunta_multiple(pregunta)
    
    # Mostrar opciones
    respuesta_actual = st.session_state.respuestas_usuario.get(pregunta_idx)
    
    # Las opciones vienen como diccionario {'A': '...', 'B': '...', etc}
    opciones = pregunta['opciones']
    
    with st.container(key="opciones_respuesta"):
        if es_multiple:
            # Usar checkboxes para preguntas múltiples
            respuestas_seleccionadas = respuesta_actual if isinstance(respuesta_actual, list) else []

            for letra in sorted(opciones.keys()):
                checked = letra in respuestas_seleccionadas
                nuevo_estado = st.checkbox(
                    f"**{letra})** {opciones[letra]}",
                    value=checked,
                    key=f"opcion_{pregunta_idx}_{letra}"
                )

                # Si el estado cambió, actualizar
                if nuevo_estado != checked:
                    seleccionar_respuesta_multiple(pregunta_idx, letra, nuevo_estado)
                    st.rerun()
        else:
            # Usar botones para preguntas de una sola respuesta
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
    col1, col2, col3 = st.columns([1, 1, 2])
    
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
                st.rerun()
    
    # Botón Finalizar Examen centrado
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ Finalizar Examen", use_container_width=True, type="primary"):
            st.session_state.finalizado = True
            st.rerun()

def mostrar_resultados():
    """Mostrar resultados del examen"""
    nombre_cert = st.session_state.cert_activa['nombre']
    nota_corte = st.session_state.nota_corte
    st.title(f"📊 Resultados del Examen - {nombre_cert}")
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
    if porcentaje > nota_corte:  # Solo aprueba si SUPERA la nota de corte de la certificación
        st.success(f"### 🎉 ¡APROBADO! - {porcentaje:.1f}%")
        st.balloons()
    else:
        st.error(f"### 😔 No Aprobado - {porcentaje:.1f}%")
        st.info(f"ℹ️ Necesitas superar el {nota_corte}% para aprobar")
    
    st.markdown("---")
    
    # Detalles de cada pregunta
    st.markdown("### 📝 Revisión Detallada")
    
    for idx, pregunta in enumerate(st.session_state.preguntas_examen):
        respuesta_usuario = st.session_state.respuestas_usuario.get(idx, "Sin responder")
        respuesta_correcta = pregunta['respuesta_correcta']
        
        # Verificar si es pregunta múltiple
        es_multiple = es_pregunta_multiple(pregunta)
        
        # Determinar si la respuesta es correcta
        if es_multiple:
            respuestas_correctas_set = set(respuesta_correcta.split(','))
            respuestas_usuario_set = set(respuesta_usuario) if isinstance(respuesta_usuario, list) else set()
            es_correcta = respuestas_correctas_set == respuestas_usuario_set
        else:
            es_correcta = respuesta_usuario == respuesta_correcta
        
        with st.expander(
            f"Pregunta {idx + 1} - {'✅ Correcta' if es_correcta else '❌ Incorrecta' if respuesta_usuario != 'Sin responder' else '⚠️ Sin responder'}"
        ):
            st.markdown(f"<div style='background-color: white; color: black; padding: 10px;'><strong>{pregunta['pregunta']}</strong></div>", unsafe_allow_html=True)
            st.markdown("")
            
            # Las opciones vienen como diccionario {'A': '...', 'B': '...', etc}
            opciones = pregunta['opciones']
            
            if es_multiple:
                # Para preguntas múltiples
                respuestas_correctas_list = respuesta_correcta.split(',')
                respuestas_usuario_list = respuesta_usuario if isinstance(respuesta_usuario, list) else []
                
                for letra in sorted(opciones.keys()):
                    es_correcta_opcion = letra in respuestas_correctas_list
                    usuario_marco = letra in respuestas_usuario_list
                    
                    if es_correcta_opcion and usuario_marco:
                        # Usuario marcó correctamente
                        st.success(f"✅ **{letra})** {opciones[letra]} (Correcta - Marcada)")
                    elif es_correcta_opcion and not usuario_marco:
                        # Usuario no marcó una correcta
                        st.warning(f"⚠️ **{letra})** {opciones[letra]} (Correcta - No marcada)")
                    elif not es_correcta_opcion and usuario_marco:
                        # Usuario marcó una incorrecta
                        st.error(f"❌ **{letra})** {opciones[letra]} (Incorrecta - Marcada)")
                    else:
                        # No es correcta y usuario no la marcó
                        st.markdown(f"**{letra})** {opciones[letra]}")
            else:
                # Para preguntas de una sola respuesta
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