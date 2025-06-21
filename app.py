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

    # Buscar columna que contenga "Objetivo"
    objetivo_col = None
    for col in df.columns:
        if "objetivo" in col.lower():
            objetivo_col = col
            break

    if objetivo_col:
        # Filtrar filas que contienen "Actividades Objetivo"
        filtro = df[df[objetivo_col].astype(str).str.contains("Actividades Objetivo", case=False, na=False)].copy()

        if not filtro.empty:
            # Extraer número de objetivo
            filtro["Número"] = filtro[objetivo_col].str.extract(r'(\d+)')

            # Generar nombre limpio
            filtro["Objetivo"] = "Actividades Objetivo " + filtro["Número"]

            # Contar ocurrencias por objetivo
            resumen = filtro.groupby("Objetivo").size().reset_index(name="Cantidad").sort_values("Objetivo")

            # Mostrar en forma simple: Actividades Objetivo X = cantidad
            for _, row in resumen.iterrows():
                st.write(f"{row['Objetivo']} = {row['Cantidad']}")

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
            st.warning("⚠️ No se encontraron filas con 'Actividades Objetivo' en la columna detectada.")
    else:
        st.error("⚠️ No se encontró ninguna columna con 'Objetivo' en el nombre. Verifica tu archivo.")
