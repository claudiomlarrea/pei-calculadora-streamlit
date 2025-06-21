import streamlit as st
import pandas as pd
import io

# Título principal
st.title("📊 PEI - Calculadora de Actividades")

# Subida de archivo
uploaded_file = st.file_uploader("Sube el archivo Excel del PEI", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Mostrar total de actividades cargadas
    total_actividades = len(df)
    st.subheader("1️⃣ Total de Actividades Cargadas")
    st.success(f"Cantidad Total de Actividades: {total_actividades}")

    # Filtrar solo las filas que comienzan con 'Actividades Objetivo'
    col_objetivo = [col for col in df.columns if 'Objetivo Específico' in col or 'Objetivo' in col][0]
    filtro_objetivos = df[df[col_objetivo].astype(str).str.startswith("Actividades Objetivo", na=False)]

    # Extraer número de objetivo y contar actividades por objetivo
    filtro_objetivos["Objetivo Número"] = filtro_objetivos[col_objetivo].str.extract(r'Actividades Objetivo (\d+)')
    resumen_objetivos = filtro_objetivos.groupby("Objetivo Número").size().reset_index(name="Cantidad")
    resumen_objetivos = resumen_objetivos.sort_values(by="Objetivo Número")

    # Mostrar tabla de actividades por objetivo específico
    st.subheader("2️⃣ Cantidad de Actividades por Objetivo Específico")
    resumen_objetivos["Descripción"] = "Actividades Objetivo " + resumen_objetivos["Objetivo Número"]
    resumen_objetivos = resumen_objetivos[["Descripción", "Cantidad"]].rename(columns={"Descripción": "Objetivo Específico"})
    st.table(resumen_objetivos)

    # Mostrar cantidad de actividades por Unidad Académica o Administrativa
    col_unidad = [col for col in df.columns if 'Unidad Académica o Administrativa' in col][0]
    resumen_unidad = df.groupby(col_unidad).size().reset_index(name="Cantidad")
    st.subheader("3️⃣ Cantidad de Actividades por Unidad Académica o Administrativa")
    st.table(resumen_unidad)

    # Exportar resultados a Excel
    st.subheader("💾 Exportar Resultados")
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        resumen_objetivos.to_excel(writer, sheet_name='Por Objetivo', index=False)
        resumen_unidad.to_excel(writer, sheet_name='Por Unidad', index=False)
    output.seek(0)
    st.download_button("📥 Descargar resultados (.xlsx)", data=output, file_name="resultados_PEI.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
