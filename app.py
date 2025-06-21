import streamlit as st
import pandas as pd
import io

# -------------------------------
# Configuración de la página
# -------------------------------
st.set_page_config(
    page_title="Calculadora PEI UCU",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Calculadora PEI - Universidad Católica de Cuyo")
st.write("""
Sube la hoja de cálculo **Excel** exportada desde Google Sheets para analizar:
- 🔢 Total de actividades
- 🎯 Cantidad de actividades por **Objetivo Específico**
- 🏛️ Cantidad de actividades por **Unidad Académica o Administrativa**
- 💾 Exportar todos los resultados en un solo archivo Excel
""")

# -------------------------------
# Subir archivo
# -------------------------------
uploaded_file = st.file_uploader(
    "📁 **Sube tu archivo Excel:**",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Archivo cargado correctamente.")

    st.subheader("📌 Vista previa de los datos")
    st.dataframe(df.head())

    # -------------------------------
    # 1️⃣ Total de actividades
    # -------------------------------
    st.markdown("## 🔢 Total de Actividades Cargadas")
    total_actividades = df.shape[0]
    st.metric("Total de Actividades", total_actividades)

    # -------------------------------
    # 2️⃣ Cantidad por Objetivo Específico
    # -------------------------------
    st.markdown("## 🎯 Cantidad de Actividades por Objetivo Específico")

    objetivos_cols = [col for col in df.columns if 'Objetivo' in col]
    resumen_objetivos = []

    for col in objetivos_cols:
        suma = pd.to_numeric(df[col], errors='coerce').fillna(0).sum()
        resumen_objetivos.append({"Objetivo": col, "Cantidad": int(suma)})

    df_objetivos = pd.DataFrame(resumen_objetivos)
    st.dataframe(df_objetivos, use_container_width=True)

    # -------------------------------
    # 3️⃣ Cantidad por Unidad Académica o Administrativa
    # -------------------------------
    st.markdown("## 🏛️ Cantidad de Actividades por Unidad Académica o Administrativa")

    col_unidad = "Unidad Académica o Administrativa"

    if col_unidad in df.columns:
        df_unidades = df.groupby(col_unidad).size().reset_index(name="Cantidad de Actividades")
        st.dataframe(df_unidades, use_container_width=True)
    else:
        st.warning(f"⚠️ La columna **{col_unidad}** no se encontró en tu archivo.")

    # -------------------------------
    # 4️⃣ Botón de Exportar Resultados
    # -------------------------------
    st.markdown("## 💾 Exportar Resultados")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Hoja 1: Resumen General
        pd.DataFrame({"Indicador": ["Total de Actividades"], "Valor": [total_actividades]}).to_excel(
            writer, sheet_name="Resumen General", index=False)
        # Hoja 2: Por Objetivo
        df_objetivos.to_excel(writer, sheet_name="Por Objetivo", index=False)
        # Hoja 3: Por Unidad
        if col_unidad in df.columns:
            df_unidades.to_excel(writer, sheet_name="Por Unidad", index=False)
        # Hoja 4: Datos originales
        df.to_excel(writer, sheet_name="Datos Originales", index=False)

    st.download_button(
        label="📥 Descargar todos los resultados (.xlsx)",
        data=output.getvalue(),
        file_name="Resumen_PEI.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👉 Por favor, sube primero tu archivo Excel para ver los análisis.")
