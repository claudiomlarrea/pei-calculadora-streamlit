import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="PEI - Calculadora de Actividades", layout="wide")

st.title("📊 PEI - Calculadora de Actividades")

uploaded_file = st.file_uploader("📂 Sube tu archivo Excel del PEI", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    st.subheader("1️⃣ Total de Actividades Cargadas")
    st.success(f"Cantidad Total de Actividades: {len(df)}")

    # -----------------------------
    # Encontrar columna de Objetivo
    # -----------------------------
    objetivo_col = None
    for col in df.columns:
        if "Objetivo" in col:
            objetivo_col = col
            break

    if objetivo_col:
        # Filtrar solo actividades objetivo
        filtro_obj = df[df[objetivo_col].astype(str).str.startswith("Actividades Objetivo", na=False)].copy()

        # Extraer número de objetivo
        filtro_obj["Número Objetivo"] = filtro_obj[objetivo_col].str.extract(r'Actividades Objetivo (\d+)')
        resumen = filtro_obj.groupby("Número Objetivo").size().reset_index(name="Cantidad")
        resumen = resumen.sort_values("Número Objetivo")
        resumen["Objetivo"] = "Actividades Objetivo " + resumen["Número Objetivo"]
        resumen = resumen[["Objetivo", "Cantidad"]]

        st.subheader("2️⃣ Cantidad de Actividades por Objetivo Específico")
        st.dataframe(resumen, use_container_width=True)

        # ----------------------------------
        # Exportar resultado como archivo Excel
        # ----------------------------------
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            resumen.to_excel(writer, sheet_name='Resumen Objetivos', index=False)
            writer.save()
        st.download_button(
            label="📥 Descargar Resumen en Excel",
            data=output.getvalue(),
            file_name="resumen_objetivos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("⚠️ No se encontró una columna que contenga la palabra 'Objetivo'. Verifica tu archivo Excel.")
