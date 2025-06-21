import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Calculadora PEI UCU", page_icon="📊", layout="wide")

st.title("📊 Calculadora PEI - Universidad Católica de Cuyo")
st.write("Sube la hoja de cálculo Excel descargada de Google Sheets para analizar las actividades del Plan Estratégico Institucional.")

# 1️⃣ Subida de archivo Excel
uploaded_file = st.file_uploader("📁 Sube tu archivo Excel aquí:", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Archivo cargado correctamente.")

    st.subheader("📌 Vista previa de los datos")
    st.dataframe(df)

    # 2️⃣ Total de actividades
    total_actividades = df.shape[0]
    st.metric("🔢 Total de Actividades Cargadas", total_actividades)

    # 3️⃣ Actividades por Objetivo robusto
    st.subheader("🎯 Cantidad de Actividades por Objetivo Específico")

    objetivos_cols = [col for col in df.columns if 'Objetivo' in col]
    resumen_objetivos = {}

    for obj in objetivos_cols:
        # Asegurarse de que sean valores numéricos
        resumen_objetivos[obj] = pd.to_numeric(df[obj], errors='coerce').sum()

    df_objetivos = pd.DataFrame(list(resumen_objetivos.items()), columns=['Objetivo', 'Cantidad'])
    st.dataframe(df_objetivos)

    # 4️⃣ Actividades por Unidad Académica
    st.subheader("🏛️ Cantidad de Actividades por Unidad Académica o Administrativa")

    if 'Unidad Académica' in df.columns:
        df_unidades = df.groupby('Unidad Académica').size().reset_index(name='Cantidad de Actividades')
        st.dataframe(df_unidades)
    else:
        st.warning("⚠️ No se encontró la columna 'Unidad Académica' en tu archivo.")

    # 5️⃣ Botón Exportar resultados
    st.subheader("💾 Exportar Resultados a Excel")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Hoja 1: Resumen General
        pd.DataFrame({'Indicador': ['Total de Actividades'], 'Valor': [total_actividades]}).to_excel(writer, index=False, sheet_name='Resumen General')

        # Hoja 2: Por Objetivo
        df_objetivos.to_excel(writer, index=False, sheet_name='Por Objetivo')

        # Hoja 3: Por Unidad
        if 'Unidad Académica' in df.columns:
            df_unidades.to_excel(writer, index=False, sheet_name='Por Unidad')

    st.download_button(
        label="📥 Descargar Resultados en Excel",
        data=output.getvalue(),
        file_name="Resumen_PEI.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👉 Por favor, sube primero tu archivo Excel para comenzar el análisis.")
