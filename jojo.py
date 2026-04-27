import streamlit as st
import joblib
import numpy as np

# Configuración de la página
st.set_page_config(page_title="Clasificador de Iris", page_icon="🌸")

# Título y descripción
st.title("🌸 Clasificador de Especies de Iris")
st.markdown("""
Esta aplicación utiliza modelos de Machine Learning (KNN y SVM) para predecir la especie de una flor Iris 
basándose en sus medidas.
""")

# Función para cargar los modelos (usamos cache para no recargar en cada clic)
@st.cache_resource
def cargar_modelos():
    knn = joblib.load('modelo_iris_knn.pkl')
    svm = joblib.load('modelo_iris_svm.pkl')
    return knn, svm

try:
    modelo_knn, modelo_svm = cargar_modelos()
except Exception as e:
    st.error(f"Error al cargar los modelos: {e}")
    st.stop()

# --- Barra lateral para configuración ---
st.sidebar.header("Configuración")
opcion_modelo = st.sidebar.radio(
    "Selecciona el modelo a utilizar:",
    ("KNN (K-Nearest Neighbors)", "SVM (Support Vector Machine)")
)

# --- Interfaz de entrada de datos ---
st.header("Ingresa las medidas de la flor")

col1, col2 = st.columns(2)

with col1:
    sepal_length = st.number_input("Largo del Sépalo (cm)", min_value=0.0, max_value=10.0, value=5.4, step=0.1)
    sepal_width = st.number_input("Ancho del Sépalo (cm)", min_value=0.0, max_value=10.0, value=3.9, step=0.1)

with col2:
    petal_length = st.number_input("Largo del Pétalo (cm)", min_value=0.0, max_value=10.0, value=1.7, step=0.1)
    petal_width = st.number_input("Ancho del Pétalo (cm)", min_value=0.0, max_value=10.0, value=0.4, step=0.1)

# Botón de predicción
if st.button("Clasificar Iris"):
    # Preparar los datos para el modelo
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    
    # Seleccionar modelo
    modelo_actual = modelo_knn if "KNN" in opcion_modelo else modelo_svm
    
    # Realizar predicción
    prediccion = modelo_actual.predict(input_data)[0]
    
    # Mapeo de resultados (ajusta según cómo entrenaste tu modelo, 
    # usualmente: 0=Setosa, 1=Versicolor, 2=Virginica)
    especies = {0: "Setosa", 1: "Versicolor", 2: "Virginica"}
    resultado = especies.get(prediccion, "Desconocida")
    
    # Mostrar resultado
    st.divider()
    st.subheader(f"Resultado:")
    if resultado == "Setosa":
        st.success(f"La especie predicha es: **Iris {resultado}** 🌸")
    elif resultado == "Versicolor":
        st.info(f"La especie predicha es: **Iris {resultado}** 🌼")
    else:
        st.warning(f"La especie predicha es: **Iris {resultado}** 🌺")

    st.write(f"Modelo utilizado: {opcion_modelo.split('(')[0]}")
