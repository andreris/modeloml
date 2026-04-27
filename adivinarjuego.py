import streamlit as st
import random
import time

# 1. Configuración de la página
st.set_page_config(page_title="Juego de Emparejar", page_icon="🃏")

st.title("🃏 Encuentra las Parejas")
st.markdown("Haz clic en las cartas para encontrar los pares de emojis.")

# 2. Configuración inicial del juego
EMOJIS = list("🍎🐶🚀🌈💎👻🍀🔥" * 2)  # 8 parejas de emojis

def inicializar_juego():
    random.shuffle(EMOJIS)
    st.session_state.tablero = EMOJIS
    st.session_state.reveladas = []  # Índices de cartas volteadas actualmente
    st.session_state.encontradas = []  # Índices de parejas ya resueltas
    st.session_state.intentos = 0

# 3. Inicializar el estado si no existe
if "tablero" not in st.session_state:
    inicializar_juego()

# 4. Lógica del juego al hacer clic en una carta
def seleccionar_carta(idx):
    # Evitar clics en cartas ya encontradas o ya reveladas
    if idx in st.session_state.encontradas or idx in st.session_state.reveladas:
        return

    # Agregar la carta a las reveladas
    if len(st.session_state.reveladas) < 2:
        st.session_state.reveladas.append(idx)

    # Si hay dos cartas reveladas, comprobar si son iguales
    if len(st.session_state.reveladas) == 2:
        st.session_state.intentos += 1
        idx1, idx2 = st.session_state.reveladas
        
        if st.session_state.tablero[idx1] == st.session_state.tablero[idx2]:
            st.session_state.encontradas.extend([idx1, idx2])
            st.session_state.reveladas = []
            st.toast("¡Pareja encontrada! 🎉")
        else:
            # Si no coinciden, damos un pequeño tiempo para que el usuario las vea
            # (En Streamlit, esto requiere un truco de UI o simplemente esperar al siguiente clic)
            pass

# 5. Interfaz de Usuario (El Tablero)
# Creamos una cuadrícula de 4x4
filas = 4
columnas = 4

st.write(f"**Intentos:** {st.session_state.intentos} | **Parejas logradas:** {len(st.session_state.encontradas)//2} / 8")

# Si hay 2 cartas que no coinciden, las cerramos automáticamente en el siguiente clic
if len(st.session_state.reveladas) == 2:
    if st.button("Las cartas no coinciden. Haz clic aquí para continuar"):
        st.session_state.reveladas = []
        st.rerun()

# Dibujar el tablero
for i in range(filas):
    cols = st.columns(columnas)
    for j in range(columnas):
        idx = i * columnas + j
        
        # Determinar qué mostrar en el botón
        if idx in st.session_state.encontradas or idx in st.session_state.reveladas:
            etiqueta = st.session_state.tablero[idx]
            deshabilitado = True
        else:
            etiqueta = "❓"
            deshabilitado = False
        
        cols[j].button(
            etiqueta, 
            key=f"btn_{idx}", 
            on_click=seleccionar_carta, 
            args=(idx,),
            disabled=deshabilitado,
            use_container_width=True
        )

# 6. Condición de victoria
if len(st.session_state.encontradas) == len(EMOJIS):
    st.success(f"¡Felicidades! Completaste el juego en {st.session_state.intentos} intentos.")
    if st.button("Jugar de nuevo"):
        inicializar_juego()
        st.rerun()

# Estilos extra para que los botones parezcan cartas
st.markdown("""
    <style>
    div.stButton > button {
        height: 80px;
        font-size: 30px !important;
    }
    </style>
    """, unsafe_allow_html=True)
