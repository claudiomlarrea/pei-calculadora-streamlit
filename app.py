import streamlit as st
import pandas as pd
import io

# Configuración de la página
st.set_page_config(
    page_title="PEI - Calculadora de Actividades",
    layout="wide"
)

st.title("📊 PEI - Calculadora de Actividades")

# Subir archivo Excel
uploaded_file = st.file_uploader(
    "📂 Sube tu archivo Excel del PEI",
    type=["xlsx"]
)

if uploaded_file:
    # Leer archivo
    df = pd.read_excel(uploaded_file)

    # 1️⃣ Total de actividades
    st.subheader("1️⃣ Total de Actividades Cargadas")
    total_actividades = len(df)
    st.success(f"Cantidad Total de Actividades: {total_actividades}")

    # 2️⃣ Cantidad de actividades por Objetivo Específico
    st.subheader("2️⃣ Cantidad de Actividades por Objetivo Específico")

    # Identificar columna con la palabra 'Objetivo'
    objetivo_col = None
    for col in df.columns:
        if "Objetivo" in col:
            objetivo_col = col
            break

    if objetivo_col:
        # Filtrar solo filas que empiecen con "Actividades Objetivo"
        filtro = df[df[objetivo_col].astype(str).str.startswith("Actividades Objetivo", na=False)].copy()

        # Extraer número
        filtro["Número"] = filtro[objetivo_col].str.extract(r'(\d+)')

        # Construir nombre corto
        filtro["Objetivo"] = "Actividades Objetivo " + filtro["Número"]

        # Resumir
        resumen = filtro.groupby("Objetivo").size().reset_index(name="Cantidad").sort_values("Objetivo")

        st.dataframe(resumen, use_container_width=True)

        # 3️⃣ Exportar resultados
        st.subheader("3️⃣ Exportar Resultados")

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            resumen.to_excel(writer, sheet_name="Resumen Objetivos", index=False)

        st.download_button(
            label="📥 Descargar Resumen en Excel",
            data=output.getvalue(),
            file_name="resumen_objetivos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    else:
        st.error("⚠️ No se encontró una columna con la palabra 'Objetivo'. Verifica tu archivo Excel.")
