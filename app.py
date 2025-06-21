# app.py

import streamlit as st
import pandas as pd
import unicodedata
from io import BytesIO

# Función para normalizar texto (elimina tildes y pone minúsculas)
def normalizar(texto):
    texto = str(texto).lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto.strip()

# Configuración Streamlit
st.set_page_config(page_title="Calculadora PEI", page_icon="🎓", layout="wide")
st.title("🎓 Calculadora Cuantitativa PEI UCuyo")

# Subir archivo
uploaded_file = st.file_uploader(
    "📤 Sube tu archivo Excel exportado de Google Sheets",
    type=["xlsx"]
)

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Vista previa
    st.subheader("📑 Vista previa de los datos")
    st.dataframe(df)

    # 1️⃣ Total de actividades
    st.subheader("1️⃣ Total de Actividades Cargadas")
    total_actividades = len(df)
    st.success(f"**Total de actividades registradas:** {total_actividades}")

    # 2️⃣ Cantidad por Objetivo Específico
    st.subheader("2️⃣ Cantidad de Actividades por Objetivo Específico")
    actividades_cols = [
        col for col in df.columns
        if 'actividades objetivo' in normalizar(col)
    ]

    resumen_objetivos = []
    for col in actividades_cols:
        conteo = df[col].notna().sum()
        # Extraer número de objetivo si lo tiene
        num = ''.join(filter(str.isdigit, col))
        nombre_obj = f"Objetivo {num}" if num else col
        resumen_objetivos.append({
            "Objetivo Específico": nombre_obj,
            "Cantidad": int(conteo)
        })

    df_objetivos = pd.DataFrame(resumen_objetivos).sort_values("Objetivo Específico")
    st.dataframe(df_objetivos)

    # 3️⃣ Cantidad por Unidad Académica o Administrativa
    st.subheader("3️⃣ Cantidad de Actividades por Unidad Académica o Administrativa")
    unidad_col = [
        col for col in df.columns
        if 'unidad academica' in normalizar(col)
    ]
    if unidad_col:
        col_name = unidad_col[0]
        df_unidad = df[col_name].value_counts().reset_index()
        df_unidad.columns = ["Unidad Académica o Administrativa", "Cantidad"]
        st.dataframe(df_unidad)
    else:
        st.warning("⚠️ No se encontró la columna **Unidad Académica o Administrativa** en tu archivo.")

    # 4️⃣ Exportar resultados
    st.subheader("4️⃣ 📤 Exportar Resultados")
    def to_excel():
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name="Datos Originales", index=False)
            df_objetivos.to_excel(writer, sheet_name="Objetivos Específicos", index=False)
            if unidad_col:
                df_unidad.to_excel(writer, sheet_name="Unidades Académicas", index=False)
        output.seek(0)
        return output

    excel_data = to_excel()
    st.download_button(
        label="📥 Descargar resultados en Excel",
        data=excel_data,
        file_name="reporte_analisis_PEI.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.info("👆 Por favor sube un archivo Excel para comenzar el análisis.")
