# app.py

import streamlit as st
import pandas as pd
import re
from io import BytesIO

# Configuración de página
st.set_page_config(page_title="Calculadora PEI", page_icon="🎓", layout="wide")

st.title("🎓 PEI - Calculadora de Actividades")

# 📤 Subir archivo Excel
uploaded_file = st.file_uploader("📤 Sube tu archivo Excel exportado de Google Sheets", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # 📑 Mostrar DataFrame original
    st.subheader("📑 Vista previa de los datos")
    st.dataframe(df)

    # 1️⃣ Total de actividades
    st.subheader("1️⃣ Total de Actividades Cargadas")
    total_actividades = len(df)
    st.success(f"**Cantidad Total de Actividades: {total_actividades}**")

    # 2️⃣ Cantidad por Objetivo Específico
    st.subheader("2️⃣ Cantidad de Actividades por Objetivo Específico")
    actividades_cols = [col for col in df.columns if 'actividades objetivo' in col.lower()]
    resumen_objetivos = []
    for col in actividades_cols:
        conteo = df[col].notna().sum()
        # Extraer solo el primer número que aparezca usando regex
        match = re.search(r'\d+', col)
        if match:
            num = match.group(0)
        else:
            num = ""
        nombre_obj = f"Objetivo {num}" if num else col
        resumen_objetivos.append({
            "Objetivo Específico": nombre_obj,
            "Cantidad": int(conteo)
        })
    df_objetivos = pd.DataFrame(resumen_objetivos)
    st.dataframe(df_objetivos)

    # 3️⃣ Cantidad por Unidad Académica o Administrativa
    st.subheader("3️⃣ Cantidad de Actividades por Unidad Académica o Administrativa")
    unidad_col = [col for col in df.columns if 'unidad académica' in col.lower()]
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
# 5️⃣ Interpretación y Conclusiones
st.subheader("5️⃣ 📊 Interpretación y Conclusiones")

with st.expander("Ver interpretación general"):
    st.markdown(f"""
    ✅ **Interpretación:**
    - Se registraron un total de **{total_actividades}** actividades en el plan institucional.
    - El análisis muestra la distribución de actividades por objetivos específicos y por unidades académicas o administrativas.
    - La mayor concentración se observa en los objetivos con más actividades (por ejemplo: {df_objetivos.sort_values('Cantidad', ascending=False).iloc[0]['Objetivo Específico']}).

    📝 **Conclusión:**
    - Este análisis cuantitativo permite identificar las áreas con mayor carga de planificación y aquellas que podrían requerir refuerzo o revisión estratégica.
    - Se recomienda evaluar la coherencia entre los objetivos más cargados y los recursos disponibles en cada unidad académica.
    """)
