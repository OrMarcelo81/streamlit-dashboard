import pandas as pd
import sqlite3
import plotly.express as px
import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta
from sklearn.linear_model import LinearRegression

# configuración general de la página web
st.set_page_config(
    page_title="Reporte de Ventas",
    page_icon="📈",
    layout="wide",
)

# datos de ventas
@st.cache_data
def get_data() -> pd.DataFrame:
    # Conexión a la base de datos
    conn = sqlite3.connect('facturacion.db')
    # Datos de ventas
    data = pd.read_sql_query("select * from facturacion", conn)
    conn.commit()
    conn.close()
    return data

df = get_data()

# titulo de dashboard
st.title("Dashboard de Ventas Retail")

# Extraer los meses únicos de la columna de fecha
meses_unicos = pd.to_datetime(df['fecha']).dt.strftime('%Y-%m').unique()

# Permitir al usuario seleccionar el mes
mesSeleccionado = st.selectbox("Seleccionar un Mes", meses_unicos, index=len(meses_unicos)-1)

# Convertir la cadena de mes seleccionado en un objeto de fecha
fechaSeleccionada = datetime.strptime(mesSeleccionado, "%Y-%m")

# Restar un mes al objeto de fecha para obtener el mes anterior
fechaMesAnterior = fechaSeleccionada - relativedelta(months=1)

# Filtrar el DataFrame para obtener datos del mes anterior
totalVentasMesAnterior = df[pd.to_datetime(df['fecha']).dt.strftime('%Y-%m') == fechaMesAnterior.strftime("%Y-%m")]['total_pagado'].sum()
cntClientesMesAnterior = len(df[pd.to_datetime(df['fecha']).dt.strftime('%Y-%m') == fechaMesAnterior.strftime("%Y-%m")]['cliente'].unique())
cntLibrosMesAnterior = df[(pd.to_datetime(df['fecha']).dt.strftime('%Y-%m') == fechaMesAnterior.strftime("%Y-%m")) & (df['producto'] == 'libro')]['cantidad'].sum()

# Filtrar el DataFrame para obtener datos del mes seleccionado
totalVentasMes = df[pd.to_datetime(df['fecha']).dt.strftime('%Y-%m') == mesSeleccionado]['total_pagado'].sum()
cntClientesMes = len(df[pd.to_datetime(df['fecha']).dt.strftime('%Y-%m') == mesSeleccionado]['cliente'].unique())
cntLibrosMes = df[(pd.to_datetime(df['fecha']).dt.strftime('%Y-%m') == mesSeleccionado) & (df['producto'] == 'libro')]['cantidad'].sum()
ventasPorGenero = df[(pd.to_datetime(df['fecha']).dt.strftime('%Y-%m') == mesSeleccionado) & (df['producto'] == 'libro')].groupby('genero')['cantidad'].sum()
generoMasVendido = ventasPorGenero.idxmax()

# creating a single-element container
placeholder_counter = st.empty()
placeholder = st.empty()

# dataframe filter
df = df[pd.to_datetime(df['fecha']).dt.strftime('%Y-%m') == mesSeleccionado]

with placeholder.container():
    # create three columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(
        label="💰 Total Ventas del Mes",
        value='{:,.0f}'.format(totalVentasMes).replace(',', '.'),
        delta='{:,.0f}'.format(int(totalVentasMes - totalVentasMesAnterior)).replace(',', '.'),
    )
    
    kpi2.metric(
        label="🧍🏽🧍🏻‍♀️ Cantidad Clientes",
        value='{:,.0f}'.format(cntClientesMes).replace(',', '.'),
        delta='{:,.0f}'.format(int(cntClientesMes - cntClientesMesAnterior)).replace(',', '.'),
    )

    kpi3.metric(
        label="🧮 Cantidad Libros Vendidos",
        value='{:,.0f}'.format(cntLibrosMes).replace(',', '.'),
        delta='{:,.0f}'.format(int(cntLibrosMes - cntLibrosMesAnterior)).replace(',', '.'),
    )

    kpi4.metric(
        label="📙 Género Top Ventas",
        value=generoMasVendido,
        #delta=0,
    )

    st.divider()

    # create two columns for charts
    fig_col1, fig_col2 = st.columns(2)
    with fig_col1:
        st.markdown("### Ventas por Produto y Medio de Pago")

        # Calcular el total vendido por cada medio de pago para cada producto
        df_porcentaje = df.groupby(['producto', 'medio_pago'])['total_pagado'].sum().reset_index()
        df_porcentaje['porcentaje'] = df_porcentaje.groupby('producto')['total_pagado'].transform(lambda x: x / x.sum() * 100)

        # Ordenar las barras por el porcentaje vendido
        df_porcentaje = df_porcentaje.sort_values(by=['producto', 'porcentaje'], ascending=[True, False])

        # Crear el gráfico de barras horizontales apiladas
        fig1 = px.bar(df_porcentaje, x='porcentaje', y='producto', color='medio_pago',
                      labels={'porcentaje': 'Porcentaje Vendido (%)', 
                              'producto': 'Producto', 
                              'medio_pago': 'Medio de Pago'
                             },
                      orientation='h', barmode='stack', 
                      category_orders={'producto': df_porcentaje['producto'].unique()}
                     )

        # Ajustar el texto en el centro de cada barra
        fig1.update_traces(texttemplate='%{x:.1f}%', textposition='inside')

        # Mostrar el gráfico en la aplicación Streamlit
        st.plotly_chart(fig1)

    with fig_col2:
        st.markdown("### Total de Ventas por Día")

        # Convertir la columna de fecha a tipo datetime si aún no lo está
        df['fecha'] = pd.to_datetime(df['fecha'])

        # Agrupar los datos por día y sumar el total_pagado
        df_ventas_por_dia = df.groupby(df['fecha'].dt.date)['total_pagado'].sum().reset_index()

        # Convertir las fechas a números enteros para la regresión lineal
        df_ventas_por_dia['fecha_int'] = df_ventas_por_dia['fecha'].apply(lambda x: x.toordinal())

        # Entrenar el modelo de regresión lineal
        model = LinearRegression()
        model.fit(df_ventas_por_dia[['fecha_int']], df_ventas_por_dia['total_pagado'])

        # Predecir los valores de ventas para las fechas existentes
        df_ventas_por_dia['ventas_predichas'] = model.predict(df_ventas_por_dia[['fecha_int']])

        # Crear el histograma con la línea de tendencia
        fig2 = px.bar(df_ventas_por_dia, x='fecha', y='total_pagado', labels={'fecha': 'Fecha', 'total_pagado': 'Total Ventas'})
        fig2.add_scatter(x=df_ventas_por_dia['fecha'], y=df_ventas_por_dia['ventas_predichas'], mode='lines', name='Línea de Tendencia', marker_color='red')

        # Mostrar el histograma en la aplicación Streamlit
        st.plotly_chart(fig2)

    st.divider()

    with st.container():
        st.markdown("### Datos")
        st.dataframe(df)
    
