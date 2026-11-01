
import paho.mqtt.client as paho
import streamlit as st
import json
import platform
import time

# ---------------- CONFIGURACIÓN ----------------

st.set_page_config(
    page_title="MQTT Control Center",
    page_icon="⚡",
    layout="wide"
)

broker = "157.230.214.127"
port = 1883

# ---------------- FUNCIONES MQTT ----------------

def on_publish(client, userdata, result):
    print("El dato ha sido publicado")

def enviar_mensaje(topic, data):
    try:
        client = paho.Client("GIT-BELEN")
        client.on_publish = on_publish
        client.connect(broker, port)

        message = json.dumps(data)
        result = client.publish(topic, message)
        result.wait_for_publish(timeout=5)

        client.disconnect()
        return True

    except Exception as e:
        st.error(f"Error de conexión MQTT: {e}")
        return False


# ---------------- ESTILOS VISUALES ----------------

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background:
        radial-gradient(circle at 10% 10%, #142b4b 0%, transparent 35%),
        radial-gradient(circle at 90% 80%, #25204b 0%, transparent 35%),
        #080d19;
    color: #f1f5f9;
}

/* Ocultar menú y footer */
#MainMenu, footer {
    visibility: hidden;
}

/* Contenedor principal */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Encabezado */
.header {
    text-align: center;
    padding: 30px 10px 35px 10px;
}

.header-icon {
    font-size: 48px;
    margin-bottom: 8px;
    filter: drop-shadow(0 0 15px #00d9ff);
}

.header h1 {
    color: white;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 3px;
    margin: 0;
}

.header p {
    color: #8ca3c4;
    font-size: 14px;
    letter-spacing: 3px;
    margin-top: 10px;
}

/* Etiquetas de sección */
.section-title {
    color: #a8bad5;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    margin: 15px 0;
}

/* Tarjetas */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(18, 30, 52, 0.78);
    border: 1px solid rgba(105, 150, 205, 0.2);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.25);
}

/* Botones */
.stButton > button {
    width: 100%;
    height: 58px;
    border-radius: 13px;
    border: 1px solid #355477;
    background: linear-gradient(135deg, #172d4c, #203e61);
    color: white;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 1px;
    transition: all 0.25s ease;
}

.stButton > button:hover {
    border-color: #00d9ff;
    color: #00e5ff;
    box-shadow: 0 0 20px rgba(0,217,255,0.2);
    transform: translateY(-2px);
}

/* Slider */
.stSlider [data-baseweb="slider"] > div > div {
    background-color: #00d9ff;
}

.stSlider label {
    color: #d6e4f5 !important;
}

/* Texto */
p, label {
    color: #d6e4f5;
}

/* Separadores */
hr {
    border-color: rgba(120,160,210,0.18);
}

/* Métrica */
.metric-value {
    color: #00e5ff;
    font-size: 34px;
    font-weight: 800;
}

.metric-label {
    color: #8ca3c4;
    font-size: 12px;
    letter-spacing: 2px;
}

/* Información inferior */
.footer-info {
    text-align: center;
    color: #627895;
    font-size: 12px;
    margin-top: 35px;
    letter-spacing: 1px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- ENCABEZADO ----------------

st.markdown("""
<div class="header">
    <div class="header-icon">⚡</div>
    <h1>MQTT CONTROL</h1>
    <p>SMART INTERFACE · REMOTE SYSTEM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------- CONTROL DIGITAL ----------------

st.markdown(
    '<div class="section-title">01 / CONTROL DIGITAL</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.markdown("### 🟢 Encender")
        st.markdown("Envía una señal de activación al dispositivo.")
        if st.button("⏻  ENCENDER", key="btn_on"):
            if enviar_mensaje("mqtt_b", {"Act1": "ON"}):
                st.success("Señal ON enviada correctamente")

with col2:
    with st.container(border=True):
        st.markdown("### 🔴 Apagar")
        st.markdown("Envía una señal de desactivación al dispositivo.")
        if st.button("⏻  APAGAR", key="btn_off"):
            if enviar_mensaje("mqtt_h", {"Act1": "OFF"}):
                st.success("Señal OFF enviada correctamente")


st.markdown("<br>", unsafe_allow_html=True)

# ---------------- CONTROL ANALÓGICO ----------------

st.markdown(
    '<div class="section-title">02 / CONTROL ANALÓGICO</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    col_title, col_value = st.columns([3, 1])

    with col_title:
        st.markdown("### 🎚️ Ajuste de intensidad")
        st.caption("Selecciona el valor que deseas transmitir al dispositivo.")

    with col_value:
        st.markdown(
            '<div class="metric-label">VALOR ACTUAL</div>',
            unsafe_allow_html=True
        )

    values = st.slider(
        "Selecciona el rango de valores",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

    st.markdown(
        f'<div class="metric-value">{values:.0f}%</div>',
        unsafe_allow_html=True
    )

    if st.button("➤  ENVIAR VALOR ANALÓGICO", key="btn_analog"):
        if enviar_mensaje("cmqtt_a", {"Analog": float(values)}):
            st.success(f"Valor {values:.0f} enviado correctamente")


# ---------------- INFORMACIÓN DEL SISTEMA ----------------

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.caption("CONEXIÓN MQTT")
    st.markdown("`157.230.214.127 : 1883`")

with col_b:
    st.caption("VERSIÓN DE PYTHON")
    st.markdown(f"`{platform.python_version()}`")

st.markdown("""
<div class="footer-info">
    MQTT CONTROL CENTER · REMOTE INTERFACE
</div>
""", unsafe_allow_html=True)
