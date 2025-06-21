import streamlit as st
import pandas as pd
import io

# ------------------------------------------
# Configurar la página
# ------------------------------------------
st.set_page_config(
    page_title="Calculadora PEI UCU",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Calculadora PEI - Universidad Católica de Cuyo")

# ------------------------------------------
# Subir archivo Excel
# ------------------------------------------
uploaded_file = st.file_uploader(
    "📁 Sube tu archivo Excel exportado desde Google Sheets",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Archivo cargado correctamente.")
    
    # Normalizar nombres de columnas para búsqueda robusta
    df.columns = [col.strip().lower().replace("  ", " ") for col in df.columns]

    st.subheader("👀 Vista previa de los datos")
    st.dataframe(df.head())

    # ------------------------------------------
    # 1️⃣ Total de actividades = total de filas
    # ------------------------------------------
    total_actividades = df.shape[0]
    st.markdown("## 🔢 Total de Actividades")
    st.metric("Cantidad total", total_actividades)

    # ------------------------------------------
    # 2️⃣ Cantidad por Objetivo Específico
    # ------------------------------------------
    st.markdown("## 🎯 Actividades por Objetivo Específico")

    # Filtrar columnas válidas: que contengan 'actividades objetivo'
    actividades_cols = [col for col in df.columns if 'actividades objetivo' in col]

    resultados_obj = []
    for col in actividades_cols:
        suma = pd.to_numeric(df[col], errors='coerce').fillna(0).sum()
        resultados_obj.append({
            "Objetivo": col.title(),
            "Cantidad": int(suma)
        })

    df_objetivos = pd.DataFrame(resultados_obj)
    st.dataframe(df_objetivos)

    # ------------------------------------------
    # 3️⃣ Cantidad por Unidad Académica o Administrativa
    # ------------------------------------------
    st.markdown("## 🏛️ Actividades por Unidad Académica o Administrativa")

    # Detectar la columna correcta ignorando mayúsculas y espacios
    col_unidad = [col for col in df.columns if "unidad académica" in col or "unidad academica" in col or "unidad" in col]

    if col_unidad:
        col_unidad = col_unidad[0]
        df_unidades = df.groupby(col_unidad).size().reset_index(name="Cantidad de Actividades")
        st.dataframe(df_unidades)
    else:
        st.warning("⚠️ No se encontró la columna 'Unidad Académica o Administrativa'. Revisa el nombre exacto.")

    # ------------------------------------------
    # 4️⃣ Exportar resultados
    # ------------------------------------------
    st.markdown("## 💾 Exportar Resultados a Excel")

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        pd.DataFrame({"Indicador": ["Total de Actividades"], "Valor": [total_actividades]}).to_excel(
            writer, sheet_name="Resumen General", index=False)
        df_objetivos.to_excel(writer, sheet_name="Por Objetivo", index=False)
        if col_unidad:
            df_unidades.to_excel(writer, sheet_name="Por Unidad", index=False)
        df.to_excel(writer, sheet_name="Datos Originales", index=False)

    st.download_button(
        label="📥 Descargar todos los resultados (.xlsx)",
        data=output.getvalue(),
        file_name="Resumen_PEI.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("🔑 Por favor, sube primero tu archivo Excel para realizar el análisis.")
