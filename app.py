import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Calculadora PEI UCU", page_icon="📊", layout="wide")

st.title("📊 Calculadora PEI - Universidad Católica de Cuyo")
st.write("Sube la hoja de cálculo Excel descargada de Google Sheets para analizar las actividades del Plan Estratégico Institucional.")

# 1️⃣ Subir archivo Excel
uploaded_file = st.file_uploader("📁 Sube tu archivo Excel aquí:", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Archivo cargado correctamente.")

    st.subheader("📌 Vista previa de los datos")
    st.dataframe(df)

    # 2️⃣ Total de actividades
    total_actividades = df.shape[0]
    st.metric("🔢 Total de Actividades Cargadas", total_actividades)

    # 3️⃣ Actividades por Objetivo
    st.subheader("🎯 Cantidad de Actividades por Objetivo Específico")
    objetivos_cols = [col for col in df.columns if 'Objetivo' in col]
    resumen_objetivos = {}
    for obj in objetivos_cols:
        resumen_objetivos[obj] = int(df[obj].sum())
    st.write(resumen_objetivos)

    # 4️⃣ Actividades por Unidad Académica
    st.subheader("🏛️ Cantidad de Actividades por Unidad Académica o Administrativa")
    if 'Unidad Académica' in df.columns:
        resumen_unidades = df.groupby('Unidad Académica').size().reset_index(name='Cantidad de Actividades')
        st.dataframe(resumen_unidades)
    else:
        st.warning("⚠️ No se encontró la columna 'Unidad Académica' en tu archivo.")

    # 5️⃣ Exportar resultados a Excel
    st.subheader("💾 Exportar Resumen a Excel")

    # Crear DataFrames de resumen
    df_objetivos = pd.DataFrame(list(resumen_objetivos.items()), columns=['Objetivo', 'Cantidad'])
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_objetivos.to_excel(writer, index=False, sheet_name='Por Objetivo')
        if 'Unidad Académica' in df.columns:
            resumen_unidades.to_excel(writer, index=False, sheet_name='Por Unidad')
        df.to_excel(writer, index=False, sheet_name='Datos Originales')
    processed_data = output.getvalue()

    st.download_button(
        label="📥 Descargar Resumen en Excel",
        data=processed_data,
        file_name='Resumen_PEI.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
else:
    st.info("👉 Por favor, sube primero tu archivo Excel para comenzar el análisis.")

