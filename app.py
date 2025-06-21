import streamlit as st
import pandas as pd
import io
import unicodedata

# Función para normalizar texto: minúsculas + sin tildes
def normalizar(texto):
    texto = str(texto).lower()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto.strip()

# Configuración de página
st.set_page_config(
    page_title="PEI - Calculadora de Actividades",
    layout="wide"
)

st.title("📊 PEI - Calculadora de Actividades")

# Subir archivo
uploaded_file = st.file_uploader(
    "📂 Sube tu archivo Excel del PEI",
    type=["xlsx"]
)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 1️⃣ Total de actividades
    st.subheader("1️⃣ Total de Actividades Cargadas")
    total_actividades = len(df)
    st.success(f"Cantidad Total de Actividades: {total_actividades}")

    # 2️⃣ Cantidad de actividades por Objetivo Específico
    st.subheader("2️⃣ Cantidad de Actividades por Objetivo Específico")

    # Buscar columna que contenga "objetivo"
    objetivo_col = None
    for col in df.columns:
        if "objetivo" in normalizar(col):
            objetivo_col = col
            break

    if objetivo_col:
        # Normalizar la columna
        df['normalizado'] = df[objetivo_col].apply(normalizar)

        # Filtrar filas que contengan "actividades objetivo"
        filtro = df[df['normalizado'].str.contains("actividades objetivo", na=False)]

        if not filtro.empty:
            # Extraer número
            filtro["numero"] = filtro['normalizado'].str.extract(r'(\d+)')
            filtro["Objetivo"] = "Actividades Objetivo " + filtro["numero"]

            # Contar por objetivo
            resumen = filtro.groupby("Objetivo").size().reset_index(name="Cantidad").sort_values("Objetivo")

            # Mostrar limpio: Actividades Objetivo X = N
            for _, row in resumen.iterrows():
                st.write(f"{row['Objetivo']} = {row['Cantidad']}")

            # Exportar
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
            st.warning("⚠️ No se encontraron filas con 'Actividades Objetivo' (normalizado). Revisa el archivo.")
    else:
        st.error("⚠️ No se encontró ninguna columna con 'Objetivo' en el nombre. Revisa tu archivo.")
