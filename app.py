
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Calculadora PEI UCU", page_icon="📊", layout="wide")

st.title("📊 Calculadora PEI - Universidad Católica de Cuyo")
st.subheader("Análisis Cuantitativo de Actividades del Plan Estratégico Institucional")

# Cargar datos
df = pd.read_csv("pei_data.csv")

st.success("✅ Datos cargados correctamente.")

# Mostrar tabla
st.dataframe(df)

# Cálculos principales
columns_objetivos = [col for col in df.columns if 'Objetivo' in col]

totales = df[columns_objetivos].sum()
total_general = totales.sum()

st.metric("🔢 Total de Actividades", int(total_general))

# Por Objetivo
st.write("### 📈 Actividades por Objetivo")
for obj in columns_objetivos:
    st.write(f"- **{obj}**: {}".format(int(df[obj].sum())))

# Filtro por Unidad Académica
unidad = st.selectbox("Selecciona Unidad Académica", sorted(df['Unidad Académica'].unique()))
df_unidad = df[df['Unidad Académica'] == unidad]
total_unidad = df_unidad[columns_objetivos].sum().sum()

st.write(f"### 📌 Total Actividades para {unidad}: **{}**".format(int(total_unidad)))

# Descarga filtrada
csv_filtered = df_unidad.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descargar Datos Filtrados",
    data=csv_filtered,
    file_name=f"{unidad}_PEI.csv",
    mime='text/csv'
)

# Descargar general
csv_all = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Descargar Todos los Datos",
    data=csv_all,
    file_name="PEI_Completo.csv",
    mime='text/csv'
)
