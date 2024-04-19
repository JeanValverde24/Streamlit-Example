import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

productos = {
    'Articulos': ['Cremalleras', 'Baterías', 'Faros', 'Radiadores'],
    'Stock': [250, 46, 25, 145],
    'Pre. Und': [275.00, 180.00, 90.00, 150.00]
}
productos_df = pd.DataFrame(productos)

ventas = {
    'Mes': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo'],
    'Cremalleras': [7425, 6325, 11550, 5225, 4125],
    'Baterías': [900, 1440, 1260, 2160, 1980],
    'Faros': [720, 270, 450, 270, 360],
    'Radiadores': [3300, 4650, 2700, 3600, 1950]
}
ventas_df = pd.DataFrame(ventas)

precios = {'Cremalleras': 275.00, 'Baterías': 180.00, 'Faros': 90.00, 'Radiadores': 150.00}
ventas_df['Ingresos'] = (ventas_df.drop('Mes', axis=1) * pd.Series(precios)).sum(axis=1)
ventas_df['Egresos'] = 0.6 * ventas_df['Ingresos']

st.set_page_config(page_title="Ventas de Autopartes", layout="wide")

st.title("Ventas de Autopartes")

st.subheader("Tabla de Productos y Stock")
st.table(productos_df)

st.subheader("Tabla de Ventas por Mes (en S/)")
st.table(ventas_df.drop(['Ingresos', 'Egresos'], axis=1).applymap(lambda x: f"S/ {x:,.2f}" if isinstance(x, (int, float)) else x))

st.subheader("Ingresos y Egresos por Mes (en S/)")
fig, ax = plt.subplots()
sns.barplot(data=ventas_df[['Mes', 'Ingresos', 'Egresos']].melt(id_vars='Mes'), x='Mes', y='value', hue='variable', ax=ax)
ax.set_xlabel('Mes')
ax.set_ylabel('Monto (S/)')
st.pyplot(fig)

st.subheader("Distribución de Ingresos por Artículo (Enero) (en S/)")
fig, ax = plt.subplots()
ax.pie(ventas_df.iloc[0, 1:5], labels=ventas_df.columns[1:5], autopct='%1.1f%%')
ax.axis('equal')
st.pyplot(fig)

st.subheader("Tendencia de Ventas (en S/)")
fig, ax = plt.subplots()
for col in ventas_df.columns[1:5]:
    ax.plot(ventas_df['Mes'], ventas_df[col], marker='o', label=col)
ax.set_xlabel('Mes')
ax.set_ylabel('Monto (S/)')
ax.legend()
st.pyplot(fig)

st.subheader("Producto más vendido y menos vendido por Mes")
fig, ax = plt.subplots(2, 1, figsize=(10, 10))

ventas_df.drop(['Ingresos', 'Egresos'], axis=1).set_index('Mes').idxmax(axis=1).value_counts().plot(kind='bar', ax=ax[0], color='blue')
ax[0].set_title('Producto más vendido')
ax[0].set_xlabel('Artículo')
ax[0].set_ylabel('Cantidad Vendida')

ventas_df.drop(['Ingresos', 'Egresos'], axis=1).set_index('Mes').idxmin(axis=1).value_counts().plot(kind='bar', ax=ax[1], color='red')
ax[1].set_title('Producto menos vendido')
ax[1].set_xlabel('Artículo')
ax[1].set_ylabel('Cantidad Vendida')

plt.tight_layout()
st.pyplot(fig)

st.subheader("Resumen de Ventas (en S/)")
col1, col2, col3 = st.columns(3)
col1.metric("Ingresos Totales", f"S/ {ventas_df['Ingresos'].sum():,.2f}")
col2.metric("Egresos Totales", f"S/ {ventas_df['Egresos'].sum():,.2f}")
col3.metric("Ganancia Neta", f"S/ {ventas_df['Ingresos'].sum() - ventas_df['Egresos'].sum():,.2f}")
