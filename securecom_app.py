import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import random

# ─── Configuración ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SecureCom Colombia — Cifrado de Mensajes",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.hero {
    background: linear-gradient(135deg, #0A0F1E 0%, #0D2137 50%, #0A1628 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(0,255,170,0.15);
}
.hero::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(0,255,170,0.08) 0%, transparent 70%);
    border-radius: 50%;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(0,180,255,0.06) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-grid {
    position: absolute;
    top:0; left:0; right:0; bottom:0;
    background-image: linear-gradient(rgba(0,255,170,0.03) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(0,255,170,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}
.hero h1 { color: #fff; font-size: 2rem; font-weight: 700; margin: 0; font-family: 'IBM Plex Mono', monospace; }
.hero p  { color: #8BAAC4; font-size: 0.95rem; margin: 0.4rem 0 0 0; }
.hero .badge {
    display: inline-block;
    background: rgba(0,255,170,0.1);
    border: 1px solid rgba(0,255,170,0.4);
    color: #00FFAA;
    padding: 0.2rem 0.8rem;
    border-radius: 4px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-top: 0.8rem;
    font-family: 'IBM Plex Mono', monospace;
    letter-spacing: 0.05em;
}

.kpi-card {
    background: #0D1B2A;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    border: 1px solid rgba(0,255,170,0.12);
    text-align: center;
    transition: border-color 0.2s, transform 0.2s;
}
.kpi-card:hover { border-color: rgba(0,255,170,0.35); transform: translateY(-2px); }
.kpi-card.green  { border-top: 3px solid #00FFAA; }
.kpi-card.blue   { border-top: 3px solid #00B4FF; }
.kpi-card.red    { border-top: 3px solid #FF4D6D; }
.kpi-card.gold   { border-top: 3px solid #FFB347; }
.kpi-label { font-size: 0.7rem; font-weight: 700; color: #4A7090; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'IBM Plex Mono', monospace; }
.kpi-value { font-size: 1.7rem; font-weight: 700; color: #E8F4FF; line-height: 1.1; margin: 0.3rem 0; font-family: 'IBM Plex Mono', monospace; }
.kpi-sub   { font-size: 0.75rem; color: #4A7090; font-family: 'IBM Plex Mono', monospace; }

.theory-card {
    background: #0D1B2A;
    border-radius: 12px;
    padding: 1.3rem 1.5rem;
    border: 1px solid rgba(0,180,255,0.15);
    margin-bottom: 1rem;
    color: #B8D4E8;
}
.theory-card b { color: #E8F4FF; }

.formula-block {
    background: #060D16;
    border: 1px solid rgba(0,255,170,0.25);
    border-radius: 8px;
    padding: 0.9rem 1.3rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.95rem;
    color: #00FFAA;
    font-weight: 600;
    text-align: center;
    margin: 0.6rem 0;
    letter-spacing: 0.02em;
}

.step-card {
    background: #0D1B2A;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    border-left: 4px solid #00B4FF;
    margin-bottom: 0.7rem;
    color: #B8D4E8;
}
.step-card b { color: #E8F4FF; }
.step-card.success { border-left-color: #00FFAA; }
.step-card.danger  { border-left-color: #FF4D6D; }
.step-card.gold    { border-left-color: #FFB347; }

.alert-success {
    background: rgba(0,255,170,0.07);
    border: 1px solid rgba(0,255,170,0.3);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #00FFAA;
    font-size: 0.88rem;
    margin: 0.5rem 0;
    font-family: 'IBM Plex Mono', monospace;
}
.alert-danger {
    background: rgba(255,77,109,0.07);
    border: 1px solid rgba(255,77,109,0.3);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #FF4D6D;
    font-size: 0.88rem;
    margin: 0.5rem 0;
    font-family: 'IBM Plex Mono', monospace;
}
.alert-info {
    background: rgba(0,180,255,0.07);
    border: 1px solid rgba(0,180,255,0.25);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #7EC8E3;
    font-size: 0.88rem;
    margin: 0.5rem 0;
}
.alert-gold {
    background: rgba(255,179,71,0.07);
    border: 1px solid rgba(255,179,71,0.3);
    border-radius: 10px;
    padding: 0.9rem 1.1rem;
    color: #FFB347;
    font-size: 0.88rem;
    margin: 0.5rem 0;
}

.tab-intro {
    background: linear-gradient(135deg, #0D1B2A, #091420);
    border-radius: 10px;
    padding: 0.9rem 1.2rem;
    font-size: 0.9rem;
    color: #8BAAC4;
    margin-bottom: 1rem;
    border-left: 4px solid #00B4FF;
}
.tab-intro b { color: #E8F4FF; }

.section-header {
    font-size: 1rem;
    font-weight: 700;
    color: #E8F4FF;
    padding: 0.4rem 0;
    margin: 0.8rem 0 0.5rem 0;
    font-family: 'IBM Plex Mono', monospace;
    border-bottom: 1px solid rgba(0,255,170,0.1);
    padding-bottom: 0.4rem;
}

.cipher-box {
    background: #060D16;
    border: 1px solid rgba(0,255,170,0.2);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.05rem;
    color: #00FFAA;
    text-align: center;
    letter-spacing: 0.15em;
    word-break: break-all;
    margin: 0.8rem 0;
}

.euclides-step {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 0.8rem;
    border-bottom: 1px solid rgba(0,180,255,0.08);
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    color: #8BAAC4;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #060D16 0%, #0A1628 100%);
    border-right: 1px solid rgba(0,255,170,0.1);
}
div[data-testid="stSidebar"] * { color: #8BAAC4 !important; }
div[data-testid="stSidebar"] hr { border-color: rgba(0,255,170,0.1) !important; }
div[data-testid="stSidebar"] .stSlider > div > div { background: rgba(0,255,170,0.15) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Helpers matemáticos ───────────────────────────────────────────────────────
def euclides(a, b):
    """Retorna (mcd, pasos) con cada iteración registrada."""
    pasos = []
    while b != 0:
        q, r = divmod(a, b)
        pasos.append((a, b, q, r))
        a, b = b, r
    return a, pasos

def euclides_extendido(a, b):
    """Retorna (mcd, x, y) tal que ax + by = mcd."""
    if b == 0:
        return a, 1, 0
    mcd, x1, y1 = euclides_extendido(b, a % b)
    return mcd, y1, x1 - (a // b) * y1

def inverso_modular(a, n):
    mcd, x, _ = euclides_extendido(a % n, n)
    if mcd != 1:
        return None
    return x % n

def es_primo(n):
    if n < 2: return False
    if n < 4: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def texto_a_numeros(texto, modo='posicion'):
    """Convierte texto a lista de enteros. modo='posicion': A=0..Z=25, modo='ascii': valor ASCII."""
    resultado = []
    for c in texto.upper():
        if c.isalpha():
            resultado.append(ord(c) - ord('A'))
    return resultado

def cifrado_afin(valores, a, b, n=26):
    return [(a * p + b) % n for p in valores]

def descifrado_afin(valores, a, b, n=26):
    a_inv = inverso_modular(a, n)
    if a_inv is None:
        return None
    return [(a_inv * (c - b)) % n for c in valores]

def numeros_a_texto(valores):
    return ''.join(chr(v + ord('A')) for v in valores)

def generar_claves_rsa(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    # Buscar e coprimo con phi
    e_candidatos = []
    for e in range(2, phi):
        if math.gcd(e, phi) == 1:
            e_candidatos.append(e)
        if len(e_candidatos) >= 10:
            break
    if not e_candidatos:
        return None
    e = e_candidatos[2] if len(e_candidatos) > 2 else e_candidatos[0]
    d = inverso_modular(e, phi)
    return {'n': n, 'phi': phi, 'e': e, 'd': d, 'p': p, 'q': q}

def cifrar_rsa(m, e, n):
    return pow(m, e, n)

def descifrar_rsa(c, d, n):
    return pow(c, d, n)

def residuo_modular(valores, k):
    return sum(valores) % k

COLORES = {
    'green':  '#00FFAA',
    'blue':   '#00B4FF',
    'red':    '#FF4D6D',
    'gold':   '#FFB347',
    'purple': '#A78BFA',
    'dark':   '#060D16',
    'mid':    '#0D1B2A',
    'text':   '#E8F4FF',
    'muted':  '#4A7090',
}

ALFAB = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
<div class="hero-grid"></div>
<h1>🔐 SecureCom Colombia S.A.S.</h1>
<p>Sistema de cifrado de mensajes internos · Teoría de Números aplicada a criptografía</p>
<span class="badge">🎓 Fundación Universitaria Compensar · Teoría de Números · 2026</span>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔒 Panel de control")
    st.markdown("---")

    st.markdown("### 🔑 Enfoque 1 — MCD")
    modulo_n = st.number_input("Módulo n (tamaño alfabeto)", 2, 100, 26, 1)
    clave_mcd = st.number_input("Clave a validar", 1, 1000, 15, 1)

    st.markdown("---")
    st.markdown("### 🧮 Enfoque 1 — Cifrado afín")
    clave_a = st.number_input("Clave multiplicativa a", 1, 100, 5, 1)
    clave_b = st.number_input("Desplazamiento b", 0, 100, 3, 1)
    mensaje_input = st.text_input("Mensaje a cifrar", "HOLA SECURECOM")

    st.markdown("---")
    st.markdown("### 🔢 Enfoque 2 — RSA")
    primo_p = st.number_input("Número primo p", 2, 500, 11, 1)
    primo_q = st.number_input("Número primo q", 2, 500, 17, 1)
    mensaje_rsa = st.number_input("Mensaje numérico M", 0, 10000, 42, 1)

    st.markdown("---")
    st.markdown("### 📋 Enfoque 3 — Integridad")
    modulo_k = st.number_input("Módulo k (hash)", 2, 100, 7, 1)
    mensaje_integ = st.text_input("Mensaje original", "HOLA")
    mensaje_recv = st.text_input("Mensaje recibido", "HOLA")

    st.markdown("---")
    st.caption("🔐 SecureCom Colombia · Teoría de Números · 2026")

# ─── Cálculos previos ──────────────────────────────────────────────────────────
mcd_val, pasos_euclides = euclides(int(clave_mcd), int(modulo_n))
clave_valida = (mcd_val == 1)

# Cifrado afín
msg_limpio = ''.join(c for c in mensaje_input.upper() if c.isalpha())
vals_plano  = texto_a_numeros(msg_limpio)
mcd_a, _ = euclides(int(clave_a), int(modulo_n))
cifrado_valido = (mcd_a == 1) and len(vals_plano) > 0
if cifrado_valido:
    vals_cifrados   = cifrado_afin(vals_plano, int(clave_a), int(clave_b), int(modulo_n))
    vals_descifrados = descifrado_afin(vals_cifrados, int(clave_a), int(clave_b), int(modulo_n))
    texto_cifrado   = numeros_a_texto(vals_cifrados)
    texto_desc      = numeros_a_texto(vals_descifrados) if vals_descifrados else "—"
    a_inv = inverso_modular(int(clave_a), int(modulo_n))
else:
    texto_cifrado = "—"
    texto_desc    = "—"
    a_inv = None

# RSA
p_es_primo = es_primo(int(primo_p))
q_es_primo = es_primo(int(primo_q))
rsa_ok = p_es_primo and q_es_primo and primo_p != primo_q
claves_rsa = generar_claves_rsa(int(primo_p), int(primo_q)) if rsa_ok else None
if claves_rsa and int(mensaje_rsa) < claves_rsa['n']:
    c_rsa = cifrar_rsa(int(mensaje_rsa), claves_rsa['e'], claves_rsa['n'])
    m_desc_rsa = descifrar_rsa(c_rsa, claves_rsa['d'], claves_rsa['n'])
else:
    c_rsa = None
    m_desc_rsa = None

# Integridad
vals_orig = texto_a_numeros(mensaje_integ)
vals_recv = texto_a_numeros(mensaje_recv)
r_orig = residuo_modular(vals_orig, int(modulo_k)) if vals_orig else 0
r_recv = residuo_modular(vals_recv, int(modulo_k)) if vals_recv else 0
integridad_ok = (r_orig == r_recv) and len(vals_orig) > 0

# ─── KPIs globales ─────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
kpis = [
    (c1, "green",  "Estado de clave MCD",  "✓ VÁLIDA" if clave_valida else "✗ INVÁLIDA",  f"MCD({clave_mcd},{modulo_n}) = {mcd_val}"),
    (c2, "blue",   "Cifrado afín",         "✓ ACTIVO" if cifrado_valido else "✗ ERROR",   f"a={clave_a}, b={clave_b}, n={modulo_n}"),
    (c3, "gold",   "Módulo RSA (n)",       f"{claves_rsa['n']}" if claves_rsa else "—",    f"p={primo_p} × q={primo_q}"),
    (c4, "green" if integridad_ok else "red", "Integridad del mensaje", "✓ ÍNTEGRO" if integridad_ok else "✗ ALTERADO", f"R={r_orig} vs R'={r_recv}"),
    (c5, "blue",   "Tamaño del alfabeto",  f"n = {modulo_n}",           f"{modulo_n} caracteres"),
]
for col, cls, label, val, sub in kpis:
    with col:
        st.markdown(f"""
        <div class="kpi-card {cls}">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "🔑 MCD y Validación",
    "🔤 Cifrado Afín",
    "🔢 RSA",
    "📋 Integridad Modular",
    "📊 Comparativo",
    "📚 Marco Teórico",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — MCD Y VALIDACIÓN DE CLAVE
# ══════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown("""
    <div class="tab-intro">
    🔑 <b>Enfoque 1 — Control de acceso mediante MCD.</b><br>
    Antes de permitir que un empleado use una clave para cifrar o descifrar mensajes, el sistema verifica
    matemáticamente que esa clave sea <b>coprima</b> con el módulo n del alfabeto. Si MCD(clave, n) = 1,
    la clave es válida y el cifrado afín funciona correctamente. Si MCD ≠ 1, la función de cifrado
    no es biyectiva y el descifrado es imposible — el acceso se rechaza automáticamente.
    </div>""", unsafe_allow_html=True)

    col_alg, col_res = st.columns([3, 2])

    with col_alg:
        st.markdown('<div class="section-header">📐 Algoritmo de Euclides — paso a paso</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#060D16;border:1px solid rgba(0,180,255,0.2);border-radius:10px;
                    padding:1rem 1.3rem;margin-bottom:0.8rem;color:#8BAAC4;font-size:0.88rem;">
        <b style="color:#E8F4FF;">¿Qué hace el Algoritmo de Euclides?</b><br><br>
        Calcula el MCD(a, b) usando la propiedad: <span style="color:#00FFAA;font-family:monospace;">MCD(a, b) = MCD(b, a mod b)</span><br>
        Se repite hasta que el residuo es 0. El último divisor no nulo es el MCD.<br><br>
        En el cifrado afín, necesitamos que <span style="color:#00FFAA;font-family:monospace;">MCD(a, n) = 1</span> 
        para que exista el inverso multiplicativo de <i>a</i> módulo <i>n</i>, lo que garantiza que el descifrado sea posible.
        </div>""", unsafe_allow_html=True)

        # Tabla de pasos del algoritmo
        if pasos_euclides:
            filas_euc = []
            for i, (a_, b_, q_, r_) in enumerate(pasos_euclides):
                filas_euc.append({
                    'Iteración': i + 1,
                    'Dividendo (a)': a_,
                    'Divisor (b)': b_,
                    'Cociente (q)': q_,
                    'Residuo (r)': r_,
                    'Expresión': f"{a_} = {b_} × {q_} + {r_}"
                })
            df_euc = pd.DataFrame(filas_euc)
            st.dataframe(df_euc, hide_index=True, use_container_width=True)
        else:
            st.markdown(f'<div class="alert-success">MCD({clave_mcd}, {modulo_n}) = {clave_mcd} directamente (b = 0)</div>', unsafe_allow_html=True)

        # Traza manual
        st.markdown('<div class="section-header">🖊️ Desarrollo manual completo</div>', unsafe_allow_html=True)
        pasos_html = ""
        a_tmp, b_tmp = int(clave_mcd), int(modulo_n)
        if a_tmp < b_tmp:
            a_tmp, b_tmp = b_tmp, a_tmp
        for i, (a_, b_, q_, r_) in enumerate(pasos_euclides):
            color = '#00FFAA' if r_ == 0 else '#8BAAC4'
            final = " ← MCD" if r_ == 0 else ""
            pasos_html += f"""
            <div style="display:flex;align-items:center;padding:0.35rem 0.8rem;
                        border-bottom:1px solid rgba(0,180,255,0.07);
                        font-family:'IBM Plex Mono',monospace;font-size:0.84rem;color:{color};">
                <span style="color:#4A7090;width:2rem;">{i+1}.</span>
                <span>{a_} = {b_} × {q_} + <b style="color:{color};">{r_}</b>{final}</span>
            </div>"""
        pasos_html += f"""
        <div style="padding:0.5rem 0.8rem;font-family:'IBM Plex Mono',monospace;
                    font-size:0.9rem;color:#00FFAA;margin-top:0.3rem;">
            → MCD({clave_mcd}, {modulo_n}) = <b>{mcd_val}</b>
        </div>"""
        st.markdown(f'<div style="background:#060D16;border:1px solid rgba(0,255,170,0.15);border-radius:10px;overflow:hidden;">{pasos_html}</div>', unsafe_allow_html=True)

    with col_res:
        st.markdown('<div class="section-header">🎯 Resultado de la validación</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="formula-block">MCD({clave_mcd}, {modulo_n}) = {mcd_val}</div>', unsafe_allow_html=True)

        if clave_valida:
            st.markdown(f"""
            <div class="alert-success">
            ✓ <b>ACCESO PERMITIDO</b><br><br>
            La clave <b>{clave_mcd}</b> es coprima con el módulo <b>{modulo_n}</b>.<br>
            MCD = 1 → los números no comparten factores comunes.<br><br>
            El cifrado afín con esta clave es <b>biyectivo</b>: cada texto plano
            produce un texto cifrado único, y el descifrado es siempre posible.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-danger">
            ✗ <b>ACCESO DENEGADO</b><br><br>
            La clave <b>{clave_mcd}</b> NO es coprima con el módulo <b>{modulo_n}</b>.<br>
            MCD = {mcd_val} → comparten el factor {mcd_val}.<br><br>
            El cifrado afín con esta clave <b>no es biyectivo</b>: el descifrado
            es matemáticamente imposible o ambiguo.
            </div>""", unsafe_allow_html=True)

        # Tabla de claves válidas e inválidas
        st.markdown('<div class="section-header">📋 Claves coprimas con n={}</div>'.format(modulo_n), unsafe_allow_html=True)
        validas   = [k for k in range(1, min(modulo_n*2, 52)) if math.gcd(k, modulo_n) == 1]
        invalidas = [k for k in range(1, min(modulo_n*2, 52)) if math.gcd(k, modulo_n) != 1]
        df_claves = pd.DataFrame({
            'Claves VÁLIDAS (MCD=1)': validas[:10] + ['...'] if len(validas) > 10 else validas,
            'Claves INVÁLIDAS (MCD≠1)': (invalidas[:10] + ['...'] if len(invalidas) > 10 else invalidas) + [''] * max(0, min(10, len(validas)) - min(10, len(invalidas)))
        })
        st.dataframe(df_claves, hide_index=True, use_container_width=True)

        # Gráfica: qué claves son válidas
        ks = list(range(1, modulo_n + 1))
        colores_k = ['#00FFAA' if math.gcd(k, modulo_n) == 1 else '#FF4D6D' for k in ks]
        fig_mcd = go.Figure(go.Bar(
            x=ks, y=[1]*len(ks),
            marker_color=colores_k,
            hovertext=[f"k={k} | MCD({k},{modulo_n})={math.gcd(k,modulo_n)} | {'✓' if math.gcd(k,modulo_n)==1 else '✗'}" for k in ks],
            hoverinfo='text'
        ))
        fig_mcd.add_vline(x=int(clave_mcd), line=dict(color='#FFB347', width=3, dash='dash'))
        fig_mcd.update_layout(
            title=f"Claves coprimas (verde ✓) vs. inválidas (rojo ✗) para n={modulo_n}",
            xaxis_title="Valor de la clave",
            yaxis_visible=False,
            plot_bgcolor='#060D16', paper_bgcolor='#0D1B2A',
            font=dict(color='#8BAAC4', family='IBM Plex Mono'),
            height=200, margin=dict(l=20, r=20, t=50, b=40),
            title_font=dict(color='#E8F4FF', size=12)
        )
        st.plotly_chart(fig_mcd, use_container_width=True)
        st.markdown(f"""
        <div class="alert-info">
        📌 La barra naranja marca tu clave actual ({clave_mcd}).
        Verde = coprima con n={modulo_n} → válida para cifrado afín.
        Roja = comparte factor con n → inválida.
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 2 — CIFRADO AFÍN
# ══════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown(f"""
    <div class="tab-intro">
    🔤 <b>Cifrado afín — ¿cómo funciona?</b><br>
    El cifrado afín transforma cada letra del mensaje usando la congruencia
    <b>C ≡ (a·P + b) (mod n)</b>, donde P es el valor numérico de la letra (A=0, B=1, ..., Z=25),
    <b>a</b> es la clave multiplicativa (debe ser coprima con n), <b>b</b> es el desplazamiento,
    y <b>n</b> es el tamaño del alfabeto.<br><br>
    El descifrado usa el inverso multiplicativo de <i>a</i>: <b>P ≡ a⁻¹ · (C − b) (mod n)</b>.
    Este inverso solo existe si MCD(a, n) = 1 — conectando directamente con el Enfoque 1.
    </div>""", unsafe_allow_html=True)

    # ── Visualización del cifrado letra a letra ──────────────────────────────
    if cifrado_valido and vals_plano:
        # Construir HTML de tarjetas fuera del f-string para evitar conflictos de comillas
        tarjetas_html = ""
        for letra_p, letra_c in zip(msg_limpio, texto_cifrado):
            tarjetas_html += (
                '<div style="display:flex;flex-direction:column;align-items:center;'
                'gap:0.3rem;min-width:52px;">'
                '<div style="background:#0D1B2A;border:1px solid rgba(255,255,255,0.12);'
                'border-radius:8px;width:44px;height:44px;display:flex;align-items:center;'
                'justify-content:center;font-family:IBM Plex Mono,monospace;font-size:1.2rem;'
                'font-weight:700;color:#E8F4FF;">' + letra_p + '</div>'
                '<div style="color:#4A7090;font-size:0.75rem;font-family:monospace;">&#8595;</div>'
                '<div style="background:#060D16;border:1px solid rgba(0,255,170,0.4);'
                'border-radius:8px;width:44px;height:44px;display:flex;align-items:center;'
                'justify-content:center;font-family:IBM Plex Mono,monospace;font-size:1.2rem;'
                'font-weight:700;color:#00FFAA;">' + letra_c + '</div>'
                '</div>'
            )

        resumen_html = (
            '<span style="color:#E8F4FF;font-weight:700;">' + msg_limpio + '</span>'
            '<span style="color:#4A7090;"> &nbsp;&#10230;&nbsp; </span>'
            '<span style="color:#00FFAA;font-weight:700;">' + texto_cifrado + '</span>'
            '<span style="color:#4A7090;"> &nbsp;&#10230;&nbsp; </span>'
            '<span style="color:#E8F4FF;font-weight:700;">' + texto_desc + '</span>'
            '<span style="color:#4A7090;"> &#10003; descifrado correcto</span>'
        )

        header_html = (
            '&#128292; CIFRADO VISUAL &nbsp;|&nbsp; a=' + str(clave_a) +
            ', b=' + str(clave_b) + ', n=' + str(modulo_n) +
            ' &nbsp;|&nbsp; <span style="color:#E8F4FF;">texto plano</span>'
            ' &nbsp;&#8594;&nbsp; <span style="color:#00FFAA;">texto cifrado</span>'
        )

        st.markdown(
            '<div style="background:#060D16;border:1px solid rgba(0,255,170,0.15);'
            'border-radius:12px;padding:1.2rem 1.4rem;margin-bottom:1rem;">'
            '<div style="color:#4A7090;font-size:0.7rem;font-family:IBM Plex Mono,monospace;'
            'letter-spacing:0.08em;margin-bottom:0.9rem;">' + header_html + '</div>'
            '<div style="display:flex;flex-wrap:wrap;gap:0.6rem;align-items:flex-start;">'
            + tarjetas_html +
            '</div>'
            '<div style="margin-top:0.9rem;font-family:IBM Plex Mono,monospace;font-size:0.84rem;">'
            + resumen_html +
            '</div>'
            '</div>',
            unsafe_allow_html=True
        )

    if not cifrado_valido:
        st.markdown(f"""
        <div class="alert-danger">
        ✗ <b>Configuración inválida:</b> {'La clave a=' + str(clave_a) + ' no es coprima con n=' + str(modulo_n) + ' → MCD(' + str(clave_a) + ',' + str(modulo_n) + ')=' + str(math.gcd(int(clave_a),int(modulo_n))) + '. Cambia la clave en el panel izquierdo.' if math.gcd(int(clave_a),int(modulo_n)) != 1 else 'El mensaje está vacío.'}
        </div>""", unsafe_allow_html=True)
    else:
        col_c1, col_c2 = st.columns([3, 2])

        with col_c1:
            st.markdown('<div class="section-header">📝 Proceso de cifrado letra por letra</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#060D16;border:1px solid rgba(0,180,255,0.15);border-radius:10px;
                        padding:0.8rem 1rem;margin-bottom:0.8rem;color:#8BAAC4;font-size:0.85rem;">
            <b style="color:#E8F4FF;">Parámetros activos:</b>&nbsp;
            a = <span style="color:#00FFAA;">{clave_a}</span> &nbsp;|&nbsp;
            b = <span style="color:#FFB347;">{clave_b}</span> &nbsp;|&nbsp;
            n = <span style="color:#00B4FF;">{modulo_n}</span> &nbsp;|&nbsp;
            a⁻¹ (mod {modulo_n}) = <span style="color:#A78BFA;">{a_inv}</span>
            </div>""", unsafe_allow_html=True)

            # Tabla letra por letra
            filas_cifrado = []
            for i, (letra, p, c) in enumerate(zip(msg_limpio, vals_plano, vals_cifrados)):
                operacion = f"({clave_a}·{p} + {clave_b}) mod {modulo_n} = {(clave_a*p + clave_b)} mod {modulo_n}"
                filas_cifrado.append({
                    'Pos': i+1,
                    'Plano': letra,
                    'P (valor)': p,
                    'Operación': operacion,
                    'C (resultado)': c,
                    'Cifrado': chr(c + ord('A'))
                })
            df_cifrado = pd.DataFrame(filas_cifrado)
            st.dataframe(df_cifrado, hide_index=True, use_container_width=True)

            # Descifrado
            st.markdown('<div class="section-header">🔓 Verificación del descifrado</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#060D16;border:1px solid rgba(0,180,255,0.15);border-radius:10px;
                        padding:0.8rem 1rem;margin-bottom:0.5rem;color:#8BAAC4;font-size:0.85rem;">
            Fórmula de descifrado: <span style="color:#00FFAA;font-family:monospace;">P ≡ {a_inv}·(C − {clave_b}) (mod {modulo_n})</span>
            </div>""", unsafe_allow_html=True)
            filas_desc = []
            if vals_descifrados:
                for i, (c, p_rec) in enumerate(zip(vals_cifrados, vals_descifrados)):
                    letra_rec = chr(p_rec + ord('A'))
                    op = f"{a_inv}·({c} − {clave_b}) mod {modulo_n} = {a_inv*(c-clave_b)} mod {modulo_n}"
                    filas_desc.append({
                        'Cifrado': chr(c + ord('A')),
                        'C (valor)': c,
                        'Operación': op,
                        'P recuperado': p_rec,
                        'Original': letra_rec,
                        '¿Correcto?': '✓' if letra_rec == msg_limpio[i] else '✗'
                    })
                st.dataframe(pd.DataFrame(filas_desc), hide_index=True, use_container_width=True)

        with col_c2:
            st.markdown('<div class="section-header">📨 Resultado del cifrado</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div style="text-align:center;padding:0.3rem 0;color:#4A7090;font-size:0.75rem;
                        font-family:'IBM Plex Mono',monospace;letter-spacing:0.1em;">MENSAJE ORIGINAL</div>
            <div class="cipher-box" style="color:#E8F4FF;">{msg_limpio}</div>
            <div style="text-align:center;padding:0.5rem;color:#4A7090;font-size:1.2rem;">↓</div>
            <div style="text-align:center;padding:0.3rem 0;color:#4A7090;font-size:0.75rem;
                        font-family:'IBM Plex Mono',monospace;letter-spacing:0.1em;">MENSAJE CIFRADO</div>
            <div class="cipher-box">{texto_cifrado}</div>
            <div style="text-align:center;padding:0.5rem;color:#4A7090;font-size:1.2rem;">↓</div>
            <div style="text-align:center;padding:0.3rem 0;color:#4A7090;font-size:0.75rem;
                        font-family:'IBM Plex Mono',monospace;letter-spacing:0.1em;">DESCIFRADO (verificación)</div>
            <div class="cipher-box" style="color:#E8F4FF;">{texto_desc}</div>""",
            unsafe_allow_html=True)

            st.markdown(f"""
            <div class="alert-success" style="margin-top:0.8rem;">
            ✓ <b>Cifrado correcto</b><br>
            "{msg_limpio}" → "{texto_cifrado}" → "{texto_desc}"<br>
            El mensaje se recupera idéntico al original. ✓
            </div>""" if texto_desc == msg_limpio else f"""
            <div class="alert-danger" style="margin-top:0.8rem;">
            ✗ Error en el proceso de descifrado.
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-header">🗺️ Tabla de sustitución</div>', unsafe_allow_html=True)
            st.markdown("""
            <div style="background:#060D16;border:1px solid rgba(0,180,255,0.1);border-radius:8px;
                        padding:0.6rem 0.8rem;color:#4A7090;font-size:0.78rem;margin-bottom:0.5rem;">
            Cada letra del alfabeto y su equivalente cifrado con los parámetros actuales:
            </div>""", unsafe_allow_html=True)
            tabla_sust = []
            for k in range(0, modulo_n, 1):
                if k < 26:
                    c_val = (int(clave_a) * k + int(clave_b)) % int(modulo_n)
                    tabla_sust.append({'Plano': ALFAB[k], 'P': k, '→ C': c_val, 'Cifrado': ALFAB[c_val] if c_val < 26 else str(c_val)})
            st.dataframe(pd.DataFrame(tabla_sust), hide_index=True, use_container_width=True, height=300)

            # Inverso multiplicativo — cómo se calcula
            with st.expander("🔍 ¿Cómo se calcula a⁻¹ (Euclides Extendido)?"):
                mcd_ext, x_ext, y_ext = euclides_extendido(int(clave_a), int(modulo_n))
                st.markdown(f"""
                <div style="background:#060D16;border:1px solid rgba(0,255,170,0.15);border-radius:8px;
                            padding:0.9rem 1.1rem;font-family:'IBM Plex Mono',monospace;
                            font-size:0.84rem;color:#8BAAC4;">
                El Algoritmo de Euclides Extendido encuentra x, y tal que:<br>
                <span style="color:#00FFAA;">{clave_a}·x + {modulo_n}·y = MCD({clave_a},{modulo_n})</span><br><br>
                Resultado: x = <b style="color:#00FFAA;">{x_ext}</b>, y = {y_ext}<br>
                Verificación: {clave_a}·{x_ext} + {modulo_n}·{y_ext} = {int(clave_a)*x_ext + int(modulo_n)*y_ext}<br><br>
                Inverso modular: a⁻¹ = {x_ext} mod {modulo_n} = <b style="color:#00FFAA;">{(x_ext % int(modulo_n))}</b><br>
                Verificación: {clave_a} × {a_inv} mod {modulo_n} = {(int(clave_a) * a_inv) % int(modulo_n)} ✓
                </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 3 — RSA
# ══════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown("""
    <div class="tab-intro">
    🔢 <b>Enfoque 2 — Generación de claves RSA.</b><br>
    El algoritmo RSA basa su seguridad en la dificultad de factorizar el producto de dos números primos grandes.
    Se elige p y q primos, se calcula <b>n = p·q</b> (clave pública) y <b>φ(n) = (p−1)(q−1)</b> (función de Euler).
    La clave de cifrado <b>e</b> debe ser coprima con φ(n), y la clave de descifrado <b>d</b> es el inverso de e módulo φ(n).
    Un atacante que conozca solo n no puede factorizarlo eficientemente si p y q son suficientemente grandes.
    </div>""", unsafe_allow_html=True)

    if not rsa_ok:
        st.markdown(f"""
        <div class="alert-danger">
        ✗ <b>Configuración inválida:</b>
        {'p=' + str(primo_p) + ' no es primo.' if not p_es_primo else ''}
        {'q=' + str(primo_q) + ' no es primo.' if not q_es_primo else ''}
        {'p y q deben ser distintos.' if p_es_primo and q_es_primo and primo_p == primo_q else ''}
        Ajusta los valores en el panel izquierdo.
        </div>""", unsafe_allow_html=True)
    else:
        col_r1, col_r2 = st.columns([3, 2])

        with col_r1:
            st.markdown('<div class="section-header">🔨 Construcción del par de claves RSA</div>', unsafe_allow_html=True)

            pasos_rsa = [
                ("1. Seleccionar dos primos p y q",
                 f"p = {primo_p}  (primo: ✓)   q = {primo_q}  (primo: ✓)",
                 f"Ambos son primos — solo divisibles por 1 y por sí mismos."),
                ("2. Calcular n = p · q  (módulo público)",
                 f"n = {primo_p} × {primo_q} = {claves_rsa['n']}",
                 f"n es el módulo usado en el cifrado y descifrado. Es público."),
                ("3. Calcular φ(n) = (p−1)(q−1)  (función de Euler)",
                 f"φ({claves_rsa['n']}) = ({primo_p}−1) × ({primo_q}−1) = {primo_p-1} × {primo_q-1} = {claves_rsa['phi']}",
                 f"φ(n) cuenta los enteros en [1,n] coprimos con n. Es secreto."),
                ("4. Elegir e tal que 1 < e < φ(n) y MCD(e, φ(n)) = 1",
                 f"e = {claves_rsa['e']}   →   MCD({claves_rsa['e']}, {claves_rsa['phi']}) = {math.gcd(claves_rsa['e'], claves_rsa['phi'])} ✓",
                 f"e es la clave pública de cifrado. Puede conocerla cualquiera."),
                ("5. Calcular d = e⁻¹ (mod φ(n))  (clave privada)",
                 f"d = {claves_rsa['d']}   →   {claves_rsa['e']} × {claves_rsa['d']} mod {claves_rsa['phi']} = {(claves_rsa['e'] * claves_rsa['d']) % claves_rsa['phi']} ✓",
                 f"d es la clave privada de descifrado. Solo la conoce el receptor."),
            ]

            for titulo, formula, nota in pasos_rsa:
                st.markdown(f"""
                <div style="background:#0D1B2A;border-radius:10px;padding:1rem 1.3rem;
                            border-left:4px solid #00B4FF;margin-bottom:0.7rem;">
                <b style="color:#E8F4FF;font-family:'IBM Plex Mono',monospace;">{titulo}</b><br>
                <div style="background:#060D16;border:1px solid rgba(0,255,170,0.2);border-radius:7px;
                            padding:0.6rem 1rem;margin:0.5rem 0;font-family:'IBM Plex Mono',monospace;
                            font-size:0.9rem;color:#00FFAA;">{formula}</div>
                <span style="color:#8BAAC4;font-size:0.82rem;">{nota}</span>
                </div>""", unsafe_allow_html=True)

            # Simulación de cifrado/descifrado
            if c_rsa is not None:
                st.markdown('<div class="section-header">📨 Simulación: cifrar y descifrar M={}</div>'.format(mensaje_rsa), unsafe_allow_html=True)
                sim_pasos = [
                    ("Cifrado: C = Mᵉ mod n",
                     f"C = {mensaje_rsa}^{claves_rsa['e']} mod {claves_rsa['n']} = {c_rsa}",
                     "Usa la clave pública (e, n). Cualquiera puede cifrar.", "#00B4FF"),
                    ("Descifrado: M = Cᵈ mod n",
                     f"M = {c_rsa}^{claves_rsa['d']} mod {claves_rsa['n']} = {m_desc_rsa}",
                     "Usa la clave privada (d, n). Solo el receptor puede descifrar.", "#00FFAA"),
                    ("Verificación",
                     f"M recuperado = {m_desc_rsa} {'= M original ✓' if m_desc_rsa == int(mensaje_rsa) else '≠ M original ✗'}",
                     "El mensaje se recupera idéntico al original." if m_desc_rsa == int(mensaje_rsa) else "Error en el proceso.", "#FFB347"),
                ]
                for titulo, formula, nota, color in sim_pasos:
                    st.markdown(f"""
                    <div style="background:#0D1B2A;border-radius:10px;padding:0.9rem 1.2rem;
                                border-left:4px solid {color};margin-bottom:0.6rem;">
                    <b style="color:#E8F4FF;font-family:'IBM Plex Mono',monospace;">{titulo}</b><br>
                    <div style="background:#060D16;border:1px solid rgba(0,255,170,0.15);border-radius:7px;
                                padding:0.5rem 1rem;margin:0.4rem 0;font-family:'IBM Plex Mono',monospace;
                                font-size:0.9rem;color:{color};">{formula}</div>
                    <span style="color:#8BAAC4;font-size:0.82rem;">{nota}</span>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-gold">⚠️ M debe ser menor que n={claves_rsa["n"]} para poder cifrarse correctamente.</div>', unsafe_allow_html=True)

        with col_r2:
            st.markdown('<div class="section-header">🗝️ Resumen del par de claves</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:#060D16;border:1px solid rgba(0,255,170,0.2);border-radius:12px;padding:1.3rem;">
            <div style="color:#4A7090;font-size:0.7rem;font-family:'IBM Plex Mono',monospace;
                        letter-spacing:0.1em;margin-bottom:0.4rem;">CLAVE PÚBLICA (compartir)</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.1rem;color:#00FFAA;">
                (e, n) = ({claves_rsa['e']}, {claves_rsa['n']})
            </div>
            <br>
            <div style="color:#4A7090;font-size:0.7rem;font-family:'IBM Plex Mono',monospace;
                        letter-spacing:0.1em;margin-bottom:0.4rem;">CLAVE PRIVADA (secreto)</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:1.1rem;color:#FF4D6D;">
                (d, n) = ({claves_rsa['d']}, {claves_rsa['n']})
            </div>
            <br>
            <div style="color:#4A7090;font-size:0.7rem;font-family:'IBM Plex Mono',monospace;
                        letter-spacing:0.1em;margin-bottom:0.4rem;">FACTORES SECRETOS</div>
            <div style="font-family:'IBM Plex Mono',monospace;font-size:0.95rem;color:#A78BFA;">
                p = {primo_p},  q = {primo_q}
            </div>
            </div>""", unsafe_allow_html=True)

            # Gráfica: seguridad según tamaño de n
            ns = [p*q for p in range(3,30,2) for q in range(p+2,32,2) if es_primo(p) and es_primo(q)]
            ns = sorted(set(ns))[:30]
            fig_sec = go.Figure(go.Scatter(
                x=list(range(len(ns))), y=ns,
                mode='lines+markers',
                line=dict(color=COLORES['blue'], width=2),
                marker=dict(size=5, color=COLORES['blue']),
                fill='tozeroy', fillcolor='rgba(0,180,255,0.05)'
            ))
            fig_sec.add_hline(y=claves_rsa['n'], line=dict(color=COLORES['green'], dash='dash', width=2))
            fig_sec.add_annotation(
                x=len(ns)*0.6, y=claves_rsa['n']*1.1,
                text=f"n actual = {claves_rsa['n']}",
                font=dict(color=COLORES['green'], size=10, family='IBM Plex Mono'),
                showarrow=False, bgcolor='rgba(13,27,42,0.8)'
            )
            fig_sec.update_layout(
                title="n = p×q para distintos pares de primos",
                plot_bgcolor='#060D16', paper_bgcolor='#0D1B2A',
                font=dict(color='#8BAAC4', family='IBM Plex Mono'),
                height=220, margin=dict(l=30, r=20, t=45, b=35),
                xaxis=dict(title="Par de primos", color='#4A7090'),
                yaxis=dict(title="n", color='#4A7090'),
                title_font=dict(color='#E8F4FF', size=11)
            )
            st.plotly_chart(fig_sec, use_container_width=True)
            st.markdown(f"""
            <div class="alert-info">
            📌 <b>¿Por qué es seguro RSA?</b><br>
            Un atacante que conozca n={claves_rsa['n']} tendría que encontrar p y q factorizando n.
            Con primos pequeños (p={primo_p}, q={primo_q}) es trivial, pero con primos de 1024+ bits
            la factorización tomaría más tiempo que la edad del universo con hardware actual.
            </div>""", unsafe_allow_html=True)

            # Tabla de todos los e válidos
            st.markdown('<div class="section-header">📋 Exponentes e válidos (coprimos con φ(n))</div>', unsafe_allow_html=True)
            e_validos = [e for e in range(2, min(claves_rsa['phi'], 50)) if math.gcd(e, claves_rsa['phi']) == 1]
            df_e = pd.DataFrame({'e válido': e_validos[:15], 'd correspondiente': [inverso_modular(e, claves_rsa['phi']) for e in e_validos[:15]]})
            st.dataframe(df_e, hide_index=True, use_container_width=True, height=250)


# ══════════════════════════════════════════════════════════════════════
# TAB 4 — INTEGRIDAD MODULAR
# ══════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("""
    <div class="tab-intro">
    📋 <b>Enfoque 3 — Verificación de integridad con residuos modulares.</b><br>
    Antes de enviar un mensaje, el sistema calcula un <b>residuo modular</b> R ≡ suma(M) (mod k)
    que actúa como "huella matemática" del contenido. Si el mensaje es alterado durante la transmisión,
    el receptor calcula R' y detecta la diferencia: R ≠ R' significa que el mensaje fue modificado.
    Este mecanismo protege la <b>integridad</b> de la información, complementando el cifrado.
    </div>""", unsafe_allow_html=True)

    col_i1, col_i2 = st.columns([3, 2])

    with col_i1:
        st.markdown('<div class="section-header">📨 Proceso completo: envío y recepción</div>', unsafe_allow_html=True)

        # Mensaje original
        st.markdown(f"""
        <div style="background:#060D16;border:1px solid rgba(0,180,255,0.2);border-radius:10px;
                    padding:1rem 1.3rem;margin-bottom:0.8rem;">
        <div style="color:#4A7090;font-size:0.72rem;font-family:'IBM Plex Mono',monospace;
                    letter-spacing:0.08em;margin-bottom:0.6rem;">PASO 1 — CONVERTIR MENSAJE A VALORES NUMÉRICOS (A=0, B=1, ...)</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.9rem;color:#E8F4FF;">
            Mensaje: "<span style="color:#00FFAA;">{mensaje_integ.upper()}</span>"<br>
            Valores: {' + '.join([f'{ALFAB[v]}={v}' for v in vals_orig]) if vals_orig else '—'}
        </div>
        </div>""", unsafe_allow_html=True)

        suma_orig = sum(vals_orig)
        st.markdown(f"""
        <div style="background:#060D16;border:1px solid rgba(0,180,255,0.2);border-radius:10px;
                    padding:1rem 1.3rem;margin-bottom:0.8rem;">
        <div style="color:#4A7090;font-size:0.72rem;font-family:'IBM Plex Mono',monospace;
                    letter-spacing:0.08em;margin-bottom:0.6rem;">PASO 2 — CALCULAR RESIDUO R ≡ SUMA(M) (mod {modulo_k})</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.9rem;color:#E8F4FF;">
            Suma = {' + '.join(str(v) for v in vals_orig) if vals_orig else '0'} = <span style="color:#FFB347;">{suma_orig}</span><br>
            R = {suma_orig} mod {modulo_k} = <span style="color:#00FFAA;font-size:1.1rem;">{r_orig}</span>
        </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#060D16;border:1px solid rgba(0,180,255,0.2);border-radius:10px;
                    padding:1rem 1.3rem;margin-bottom:0.8rem;">
        <div style="color:#4A7090;font-size:0.72rem;font-family:'IBM Plex Mono',monospace;
                    letter-spacing:0.08em;margin-bottom:0.6rem;">PASO 3 — RECEPTOR RECALCULA R' DEL MENSAJE RECIBIDO</div>
        <div style="font-family:'IBM Plex Mono',monospace;font-size:0.9rem;color:#E8F4FF;">
            Mensaje recibido: "<span style="color:{'#00FFAA' if integridad_ok else '#FF4D6D'};">{mensaje_recv.upper()}</span>"<br>
            Valores: {' + '.join([f'{ALFAB[v]}={v}' for v in vals_recv]) if vals_recv else '—'}<br>
            Suma = {sum(vals_recv)}<br>
            R' = {sum(vals_recv)} mod {modulo_k} = <span style="color:{'#00FFAA' if integridad_ok else '#FF4D6D'};font-size:1.1rem;">{r_recv}</span>
        </div>
        </div>""", unsafe_allow_html=True)

        # Resultado
        if integridad_ok:
            st.markdown(f"""
            <div class="alert-success">
            ✓ <b>MENSAJE ÍNTEGRO</b><br>
            R = {r_orig} = R' = {r_recv} → Los residuos coinciden.<br>
            El mensaje recibido es idéntico al enviado. No hubo alteración.
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-danger">
            ✗ <b>MENSAJE ALTERADO — ALERTA DE SEGURIDAD</b><br>
            R = {r_orig} ≠ R' = {r_recv} → Los residuos no coinciden.<br>
            El contenido del mensaje fue modificado durante la transmisión.
            SecureCom rechaza el mensaje automáticamente.
            </div>""", unsafe_allow_html=True)

        # Tabla detallada
        st.markdown('<div class="section-header">📋 Comparación carácter a carácter</div>', unsafe_allow_html=True)
        n_max = max(len(vals_orig), len(vals_recv))
        filas_integ = []
        for i in range(n_max):
            o = vals_orig[i] if i < len(vals_orig) else '—'
            r_c = vals_recv[i] if i < len(vals_recv) else '—'
            match = '✓' if o == r_c else '✗'
            filas_integ.append({
                'Pos': i+1,
                'Enviado': ALFAB[o] if isinstance(o, int) else o,
                'Valor enviado': o,
                'Recibido': ALFAB[r_c] if isinstance(r_c, int) else r_c,
                'Valor recibido': r_c,
                '¿Igual?': match
            })
        st.dataframe(pd.DataFrame(filas_integ), hide_index=True, use_container_width=True)

    with col_i2:
        st.markdown('<div class="section-header">🎯 Resumen de integridad</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#060D16;border:1px solid rgba(0,255,170,0.15);border-radius:12px;padding:1.3rem;margin-bottom:0.8rem;">
        <div style="text-align:center;font-family:'IBM Plex Mono',monospace;">
            <div style="color:#4A7090;font-size:0.7rem;letter-spacing:0.1em;margin-bottom:0.3rem;">RESIDUO ORIGINAL</div>
            <div style="font-size:2.5rem;font-weight:700;color:#00FFAA;">{r_orig}</div>
            <div style="color:#4A7090;font-size:0.8rem;">R ≡ {sum(vals_orig)} (mod {modulo_k})</div>
            <br>
            <div style="color:#4A7090;font-size:1.5rem;">{'=' if integridad_ok else '≠'}</div>
            <br>
            <div style="color:#4A7090;font-size:0.7rem;letter-spacing:0.1em;margin-bottom:0.3rem;">RESIDUO RECIBIDO</div>
            <div style="font-size:2.5rem;font-weight:700;color:{'#00FFAA' if integridad_ok else '#FF4D6D'};">{r_recv}</div>
            <div style="color:#4A7090;font-size:0.8rem;">R' ≡ {sum(vals_recv)} (mod {modulo_k})</div>
        </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="alert-info">
        📌 <b>¿Por qué funciona?</b><br><br>
        Cualquier cambio en el mensaje (una letra diferente, una letra más o una menos)
        cambia la suma de los valores y, con alta probabilidad, cambia el residuo modular.<br><br>
        Con módulo k={modulo_k}, hay {modulo_k} posibles residuos.
        La probabilidad de que una alteración no sea detectada es 1/{modulo_k} ≈ {1/modulo_k:.1%}.<br><br>
        Para mayor seguridad se usa un k grande (en sistemas reales se usan funciones hash
        con módulos de 2²⁵⁶ o mayores).
        </div>""", unsafe_allow_html=True)

        # Visualización: qué residuos genera cada suma posible
        sumas = list(range(0, modulo_k * 4 + 1))
        residuos = [s % modulo_k for s in sumas]
        fig_mod = go.Figure()
        fig_mod.add_trace(go.Scatter(
            x=sumas, y=residuos,
            mode='lines+markers',
            line=dict(color=COLORES['blue'], width=1.5),
            marker=dict(size=4, color=COLORES['blue']),
        ))
        fig_mod.add_hline(y=r_orig, line=dict(color=COLORES['green'], dash='dash', width=2))
        if not integridad_ok:
            fig_mod.add_hline(y=r_recv, line=dict(color=COLORES['red'], dash='dash', width=2))
        fig_mod.update_layout(
            title=f"Patrón cíclico de residuos mod {modulo_k}",
            xaxis_title="Suma de valores", yaxis_title="Residuo (mod k)",
            plot_bgcolor='#060D16', paper_bgcolor='#0D1B2A',
            font=dict(color='#8BAAC4', family='IBM Plex Mono'),
            height=220, margin=dict(l=40, r=20, t=45, b=40),
            title_font=dict(color='#E8F4FF', size=11)
        )
        st.plotly_chart(fig_mod, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 5 — COMPARATIVO
# ══════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("""
    <div class="tab-intro">
    📊 <b>Cuadro comparativo de las tres soluciones.</b><br>
    Cada solución ataca una dimensión diferente de la seguridad: la primera garantiza que las
    claves sean matemáticamente válidas (<b>control de acceso</b>), la segunda protege el contenido
    del mensaje (<b>confidencialidad</b>) y la tercera verifica que el mensaje no fue modificado
    (<b>integridad</b>). Juntas conforman una propuesta de seguridad completa para SecureCom Colombia.
    </div>""", unsafe_allow_html=True)

    # Tabla comparativa principal
    comparativo = {
        'Criterio': [
            'Objetivo principal',
            'Concepto matemático',
            'Herramienta clave',
            'Nivel de complejidad',
            'Tipo de seguridad',
            'Aplicación en el sistema',
            'Ventaja principal',
            'Limitación principal',
            'Estado con config. actual',
        ],
        '🔑 Enfoque 1 — MCD': [
            'Validar claves de acceso',
            'Divisibilidad y MCD',
            'Algoritmo de Euclides',
            '🟢 Bajo',
            'Autenticación',
            'Control de acceso al cifrado',
            'Rápido y computacionalmente barato',
            'No protege el contenido directamente',
            '✓ VÁLIDA' if clave_valida else '✗ INVÁLIDA',
        ],
        '🔢 Enfoque 2 — RSA': [
            'Cifrar mensajes de forma asimétrica',
            'Números primos y factorización',
            'Función de Euler φ(n)',
            '🔴 Alto',
            'Confidencialidad',
            'Cifrado y descifrado de mensajes',
            'Seguridad probada en sistemas reales',
            'Costoso computacionalmente con n grandes',
            f'✓ n={claves_rsa["n"]}' if rsa_ok else '✗ Configuración inválida',
        ],
        '📋 Enfoque 3 — Residuos': [
            'Verificar integridad del mensaje',
            'Congruencias modulares',
            'Residuo modular R ≡ M (mod k)',
            '🟡 Medio',
            'Integridad',
            'Verificación anti-tampering',
            'Detecta cualquier modificación',
            'No cifra el mensaje por sí solo',
            '✓ ÍNTEGRO' if integridad_ok else '✗ ALTERADO',
        ],
    }
    df_comp = pd.DataFrame(comparativo)
    st.dataframe(df_comp, hide_index=True, use_container_width=True, height=380)

    st.markdown("<br>", unsafe_allow_html=True)
    col_v1, col_v2 = st.columns(2)

    with col_v1:
        # Radar de capacidades
        categorias = ['Complejidad\nmatemática', 'Nivel de\nseguridad', 'Velocidad\nde cómputo', 'Facilidad\nde impl.', 'Cobertura\nde riesgo']
        sol1 = [2, 3, 5, 5, 2]
        sol2 = [5, 5, 2, 3, 4]
        sol3 = [3, 3, 5, 4, 3]

        radar_series = [
            ('MCD (Sol. 1)',      sol1, COLORES['green'], 'rgba(0,255,170,0.12)'),
            ('RSA (Sol. 2)',      sol2, COLORES['blue'],  'rgba(0,180,255,0.12)'),
            ('Residuos (Sol. 3)',sol3, COLORES['gold'],  'rgba(255,179,71,0.12)'),
        ]
        fig_radar = go.Figure()
        for nombre, vals, color, fillcol in radar_series:
            fig_radar.add_trace(go.Scatterpolar(
                r=vals + [vals[0]],
                theta=categorias + [categorias[0]],
                fill='toself',
                name=nombre,
                line=dict(color=color, width=2),
                fillcolor=fillcol,
                opacity=0.9
            ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 5], color='#4A7090', gridcolor='rgba(0,180,255,0.1)'),
                angularaxis=dict(color='#8BAAC4', gridcolor='rgba(0,180,255,0.1)'),
                bgcolor='#060D16'
            ),
            paper_bgcolor='#0D1B2A',
            font=dict(color='#8BAAC4', family='IBM Plex Mono'),
            legend=dict(font=dict(color='#E8F4FF')),
            title=dict(text="Perfil de capacidades por solución", font=dict(color='#E8F4FF', size=13)),
            height=380, margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col_v2:
        # Diagrama de flujo — construido con concatenación simple para evitar
        # conflictos de comillas con st.markdown / unsafe_allow_html
        def _paso(borde, texto, icono, titulo, sub=""):
            s = ('<div style="background:#0D1B2A;border:1px solid ' + borde + ';border-radius:8px;'
                 'padding:0.65rem 1rem;color:' + texto + ';font-size:0.83rem;line-height:1.5;">'
                 + icono + ' <b>' + titulo + '</b>'
                 + ('<br><span style="color:#4A7090;font-size:0.77rem;">' + sub + '</span>' if sub else '')
                 + '</div>')
            return s

        def _flecha(label=""):
            t = ' ' + label if label else ''
            return '<div style="text-align:center;color:#4A7090;font-size:0.95rem;padding:0.05rem;">&#8595;' + t + '</div>'

        _pasos = (
            _paso('#00FFAA', '#00FFAA', '&#128228;', 'Empleado escribe mensaje en texto plano') +
            _flecha() +
            _paso('#00B4FF', '#7EC8E3', '&#128273;', 'Sol. 1 &mdash; MCD: verificar coprimalidad',
                  'MCD(clave, n) = 1 &rarr; continuar &nbsp;|&nbsp; &ne; 1 &rarr; rechazar clave') +
            _flecha('MCD = 1') +
            _paso('#FFB347', '#FFB347', '&#128290;', 'Sol. 2 &mdash; RSA: cifrar con clave p&uacute;blica (e, n)',
                  'C = M&#7497; mod n &rarr; solo el receptor con d puede descifrar') +
            _flecha() +
            _paso('#A78BFA', '#A78BFA', '&#128203;', 'Sol. 3 &mdash; Residuo: calcular R = suma(M) mod k',
                  'R se adjunta al mensaje cifrado como checksum de integridad') +
            _flecha('transmisi&oacute;n por red') +
            _paso('#A78BFA', '#A78BFA', '&#128203;', 'Receptor: verificar R&#39; = suma(M&#8347;) mod k',
                  'R &ne; R&#39; &rarr; alerta de alteraci&oacute;n, mensaje rechazado') +
            _flecha("R = R'") +
            _paso('#00FFAA', '#00FFAA', '&#128275;', 'Descifrar con clave privada (d, n): M = C&#7496; mod n') +
            _flecha() +
            '<div style="background:#0D1B2A;border:1px solid #00FFAA;border-radius:8px;'
            'padding:0.65rem 1rem;color:#E8F4FF;font-size:0.83rem;'
            'text-align:center;font-weight:600;">&#9989; Mensaje entregado: confidencial e &iacute;ntegro</div>'
        )

        _flujo_html = (
            '<div style="background:#060D16;border:1px solid rgba(0,255,170,0.15);'
            'border-radius:12px;padding:1.2rem 1.4rem;">'
            '<div style="color:#E8F4FF;font-weight:700;margin-bottom:0.8rem;font-size:0.9rem;">'
            '&#128260; Flujo integrado del sistema SecureCom</div>'
            '<div style="display:flex;flex-direction:column;gap:0.35rem;">'
            + _pasos +
            '</div></div>'
        )
        st.markdown(_flujo_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# TAB 6 — MARCO TEÓRICO
# ══════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("""
    <div class="tab-intro">
    📚 <b>Marco teórico — conceptos fundamentales.</b><br>
    Esta pestaña recoge los fundamentos matemáticos que sustentan las tres soluciones propuestas.
    Cada concepto se presenta con su definición formal, su papel en la criptografía y su conexión
    directa con el sistema implementado para SecureCom Colombia S.A.S.
    </div>""", unsafe_allow_html=True)

    conceptos = [
        {
            "titulo": "1. Tríada de la seguridad",
            "color": COLORES['green'],
            "cuerpo": """
            La seguridad de la información se sostiene sobre tres pilares complementarios:<br><br>
            <b>Confidencialidad:</b> Solo personas autorizadas pueden leer el mensaje. → <i>Enfoque 2 (RSA)</i><br>
            <b>Integridad:</b> El mensaje no fue modificado durante la transmisión. → <i>Enfoque 3 (Residuos)</i><br>
            <b>Disponibilidad:</b> La información es accesible cuando se necesita. → <i>Sistema en su conjunto</i><br><br>
            Un ataque de <b>sniffing</b> compromete los tres pilares simultáneamente: el atacante puede leer
            (confidencialidad), modificar (integridad) y redirigir (disponibilidad) los mensajes.
            """,
            "formula": "CIA: Confidentiality · Integrity · Availability"
        },
        {
            "titulo": "2. Máximo Común Divisor y Algoritmo de Euclides",
            "color": COLORES['blue'],
            "cuerpo": """
            El MCD(a, b) es el mayor entero que divide exactamente a ambos. Se calcula de forma
            eficiente con el <b>Algoritmo de Euclides</b>, basado en la propiedad:<br><br>
            Si <b>MCD(a, n) = 1</b>, los números son <b>coprimos</b>. Esta condición es necesaria para:<br>
            &bull; Que el cifrado afín sea biyectivo (cada texto plano tiene un único cifrado)<br>
            &bull; Que exista el inverso multiplicativo a⁻¹ (mod n), necesario para descifrar<br>
            &bull; Que el exponente e en RSA sea válido para generar un par de claves funcional
            """,
            "formula": "MCD(a, b) = MCD(b, a mod b) → repite hasta residuo = 0"
        },
        {
            "titulo": "3. Congruencias y aritmética modular",
            "color": COLORES['gold'],
            "cuerpo": """
            Dos enteros a y b son <b>congruentes módulo n</b> si (a − b) es divisible por n:<br><br>
            En criptografía, la aritmética modular permite que las operaciones "den vuelta" dentro
            de un conjunto finito (el alfabeto de n letras). Esto hace que el cifrado sea compacto
            y manejable computacionalmente, sin importar cuán grande sea el exponente.<br><br>
            La función <b>pow(M, e, n)</b> en Python calcula Mᵉ mod n eficientemente usando
            <i>exponenciación modular rápida</i> (cuadrados sucesivos), evitando overflow.
            """,
            "formula": "a ≡ b (mod n)  ⟺  n | (a − b)  ⟺  a mod n = b mod n"
        },
        {
            "titulo": "4. Números primos y factorización",
            "color": COLORES['purple'],
            "cuerpo": """
            Un número primo p es divisible solo por 1 y por sí mismo. Son la base de RSA porque:<br><br>
            &bull; <b>Multiplicar</b> dos primos p y q para obtener n = p·q es trivialmente rápido<br>
            &bull; <b>Factorizar</b> n para encontrar p y q es computacionalmente intractable si p, q son grandes<br><br>
            Esta <b>asimetría computacional</b> (fácil en una dirección, imposible en la otra) es la
            esencia de la criptografía de clave pública. Con primos de 2048 bits, los mejores
            algoritmos de factorización actuales tardarían más que la edad del universo.
            """,
            "formula": "n = p · q  →  Fácil · Inviable de invertir si p,q son grandes"
        },
        {
            "titulo": "5. Inverso multiplicativo e identidad de Bézout",
            "color": COLORES['red'],
            "cuerpo": """
            El inverso multiplicativo de a módulo n es el entero a⁻¹ tal que:<br>
            <b>a · a⁻¹ ≡ 1 (mod n)</b><br><br>
            Existe si y solo si <b>MCD(a, n) = 1</b> (condición de coprimalidad). Se calcula con
            el <b>Algoritmo de Euclides Extendido</b>, que además de calcular el MCD expresa:<br>
            <b>MCD(a, n) = a·x + n·y</b> (identidad de Bézout)<br><br>
            Si MCD = 1, entonces x = a⁻¹ (mod n). Este inverso es esencial para:<br>
            &bull; Descifrar el cifrado afín: P = a⁻¹·(C − b) mod n<br>
            &bull; Calcular la clave privada RSA: d = e⁻¹ (mod φ(n))
            """,
            "formula": "a · a⁻¹ ≡ 1 (mod n)  ←  requiere MCD(a, n) = 1"
        },
    ]

    for concepto in conceptos:
        with st.expander(concepto["titulo"], expanded=False):
            st.markdown(f"""
            <div style="background:#060D16;border-radius:10px;padding:1.2rem 1.4rem;
                        color:#B8D4E8;font-size:0.9rem;line-height:1.7;border-left:4px solid {concepto['color']};">
            {concepto['cuerpo']}
            </div>""", unsafe_allow_html=True)
            st.markdown(f'<div class="formula-block">{concepto["formula"]}</div>', unsafe_allow_html=True)


# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#2A4560; font-size:0.8rem; padding:0.5rem;
            font-family:"IBM Plex Mono",monospace;'>
🔐 SecureCom Colombia S.A.S. · Cifrado de Mensajes Internos ·
Fundación Universitaria Compensar · Teoría de Números · 2026<br>
<span style='color:#00FFAA;'>MCD · Cifrado Afín · RSA · Residuos Modulares</span>
</div>
""", unsafe_allow_html=True)
