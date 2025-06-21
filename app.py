# app.py

import streamlit as st
import pandas as pd
import re
from io import BytesIO

# ✅ Configuración final de página
st.set_page_config(page_title="Calculadora Cuantitativa PEI UCCuyo", page_icon="🎓", layout="wide")

st.title("🎓 Calculadora Cuantitativa PEI UCCuyo")

# 📤 Subir archivo Excel
uploaded_file = st.file_uploader("📤 Sube tu archivo Excel exportado de Google Sheets", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # 📑 Mostrar DataFrame original
    st.subheader("📑 Vista previa de los datos")
    st.dataframe(df)

    # 1️⃣ Total de actividades (filas)
    st.subheader("1️⃣ Total de Actividades Cargadas")
    total_actividades = len(df)
    st.success(f"**Cantidad Total de Actividades:** {total_actividades}")

    # 2️⃣ Cantidad por Objetivo Específico
    st.subheader("2️⃣ Cantidad de Actividades por Objetivo Específico")
    actividades_cols = [col for col in df.columns if 'actividades objetivo' in col.lower()]
    resumen_objetivos = []
    for col in actividades_cols:
        conteo = df[col].notna().sum()
        # Extraer número con regex
        match = re.search(r'\d+', col)
        num = match.group(0) if match else ""
        nombre_obj = f"Objetivo {num}" if num else col
        resumen_objetivos.append({
            "Objetivo Específico": nombre_obj,
            "Cantidad": int(conteo)
        })
    df_objetivos = pd.DataFrame(resumen_objetivos)
    st.dataframe(df_objetivos)

    # Mostrar suma de asignaciones
    total_asignaciones = df_objetivos['Cantidad'].sum()
    st.info(f"📌 **Total de asignaciones a objetivos:** {total_asignaciones} "
            f"(nota: una actividad puede estar asignada a más de un objetivo, "
            f"por lo que este total puede ser mayor que el total de actividades).")

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

    # 4️⃣ Interpretación y Conclusiones
    st.subheader("4️⃣ 📌 Interpretación y Conclusiones")
    st.info(
        f"""
        - Se registraron **{total_actividades}** actividades totales.
        - La suma de asignaciones a objetivos (**{total_asignaciones}**) refleja que algunas actividades impactan en más de un objetivo estratégico.
        - Esta herramienta cuantitativa ayuda a verificar la distribución de actividades por unidad y objetivo, 
          facilitando el monitoreo y la mejora del Plan Estratégico Institucional (PEI) de la UCCuyo.
        """
    )

    # 5️⃣ Exportar resultados
    st.subheader("5️⃣ 📤 Exportar Resultados")
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
