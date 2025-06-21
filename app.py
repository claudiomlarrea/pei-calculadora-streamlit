
import streamlit as st
import pandas as pd

st.set_page_config(page_title="PEI Calculadora", layout="wide")

st.title("📊 PEI - Calculadora de Actividades")

# Subida de archivo
uploaded_file = st.file_uploader("📁 Sube tu archivo Excel exportado de Google Sheets", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Mostrar cantidad total de actividades (todas las filas)
    st.header("1️⃣ Total de Actividades Cargadas")
    st.success(f"**Cantidad Total de Actividades:** {len(df)}")

    # --- ANÁLISIS POR OBJETIVO ESPECÍFICO ---
    filtro_objetivos = df[df['Objetivo Específico'].str.startswith("Actividades Objetivo", na=False)]
    filtro_objetivos['Objetivo Resumido'] = filtro_objetivos['Objetivo Específico'].str.extract(r'(Objetivo \d+)')
    filtro_objetivos['Objetivo Resumido'] = "Actividades " + filtro_objetivos['Objetivo Resumido']
    resumen_objetivos = filtro_objetivos.groupby('Objetivo Resumido').size().reset_index(name='Cantidad')

    st.header("2️⃣ Cantidad de Actividades por Objetivo Específico")
    st.dataframe(resumen_objetivos)

    # --- ANÁLISIS POR UNIDAD ACADÉMICA O ADMINISTRATIVA ---
    st.header("3️⃣ Cantidad de Actividades por Unidad Académica o Administrativa")
    if 'Unidad Académica o Administrativa' in df.columns:
        resumen_unidad = df.groupby('Unidad Académica o Administrativa').size().reset_index(name='Cantidad')
        st.dataframe(resumen_unidad)
    else:
        st.warning("⚠️ La columna 'Unidad Académica o Administrativa' no se encontró en tu archivo.")

    # --- EXPORTAR RESULTADOS ---
    st.header("💾 Exportar Resultados")
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        resumen_objetivos.to_excel(writer, sheet_name='Por Objetivo', index=False)
        if 'Unidad Académica o Administrativa' in df.columns:
            resumen_unidad.to_excel(writer, sheet_name='Por Unidad', index=False)
    st.download_button("⬇️ Descargar todos los resultados (.xlsx)", data=output.getvalue(), file_name="resultados_pei.xlsx")
