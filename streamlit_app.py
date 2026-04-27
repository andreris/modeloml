import streamlit as st
import random

# 1. Configuración de la página
st.set_page_config(page_title="Ecuaciones de Primer Grado", page_icon="🔢")

st.title("🔢 Generador de Ecuaciones de Primer Grado")
st.markdown("Resuelve la ecuación para hallar el valor de **x**.")

# 2. Función para generar ecuaciones tipo ax + b = c
def generar_ecuacion():
    a = random.randint(1, 10)
    x = random.randint(-10, 10)
    b = random.randint(-10, 10)
    c = a * x + b
    return a, b, c, x

# 3. Inicializar el estado de la sesión (Session State)
# Esto evita que la ecuación cambie automáticamente al interactuar con la app
if "ecuacion" not in st.session_state:
    a, b, c, x_correcta = generar_ecuacion()
    st.session_state.ecuacion = {"a": a, "b": b, "c": c, "x": x_correcta}
    st.session_state.resultado = None

# 4. Lógica para generar una nueva ecuación
def nueva_pregunta():
    a, b, c, x_correcta = generar_ecuacion()
    st.session_state.ecuacion = {"a": a, "b": b, "c": c, "x": x_correcta}
    st.session_state.resultado = None

# 5. Mostrar la ecuación con formato matemático elegante
datos = st.session_state.ecuacion
signo_b = "+" if datos['b'] >= 0 else "-"
valor_b_abs = abs(datos['b'])

# Usamos LaTeX para que se vea profesional
st.subheader("Ecuación a resolver:")
st.latex(f"{datos['a']}x {signo_b} {valor_b_abs} = {datos['c']}")

# 6. Interfaz de usuario para la respuesta
respuesta_usuario = st.number_input("¿Cuál es el valor de x?", step=1, key="input_usuario")

col1, col2 = st.columns(2)

with col1:
    if st.button("Comprobar respuesta", use_container_width=True):
        if respuesta_usuario == datos['x']:
            st.session_state.resultado = "¡Correcto! 🎉"
        else:
            st.session_state.resultado = f"Casi... Inténtalo de nuevo. 🔍"

with col2:
    if st.button("Generar otra ecuación", on_click=nueva_pregunta, use_container_width=True):
        st.rerun()

# 7. Mostrar mensajes de retroalimentación
if st.session_state.resultado:
    if "¡Correcto!" in st.session_state.resultado:
        st.success(st.session_state.resultado)
        st.balloons()
    else:
        st.warning(st.session_state.resultado)

# Pie de página informativo
st.divider()
st.info("Tip: Recuerda que para despejar $x$, primero debes pasar el término independiente al otro lado con signo contrario.")
