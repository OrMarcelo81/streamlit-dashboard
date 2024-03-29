# Dashboard de Ventas Retail

Este repositorio contiene un dashboard interactivo para el análisis de ventas retail, desarrollado en Python utilizando Streamlit y Plotly.

## Funcionalidades

- Visualización de métricas clave de ventas.
- Gráficos interactivos para análisis de ventas por producto y medio de pago, así como el total de ventas por día.
- Selección de mes para el análisis de datos.
- Predicción de tendencia de ventas utilizando regresión lineal.

## Cómo utilizar

1. Clona este repositorio en tu máquina local.
2. Asegúrate de tener Python y pip instalados.
3. Instala las dependencias utilizando el siguiente comando:
    ```
    pip install -r requirements.txt
    ```
4. Ejecuta la aplicación utilizando el siguiente comando:
    ```
    streamlit run app.py
    ```
5. Abre tu navegador web y ve a la dirección indicada por Streamlit para visualizar el dashboard.

## Estructura del código

- `app.py`: Contiene el código principal de la aplicación.
- `facturacion.db`: Base de datos SQLite que contiene los datos de ventas.
- `requirements.txt`: Lista de librerías necesarias.
- `generacion.py`: Script Python para la creación del dataset ficticio.

## Requisitos

- Python 3.6 o superior
- Bibliotecas Python especificadas en `requirements.txt`

## Créditos

Este proyecto fue desarrollado por Orlando Vázquez.

Si tienes alguna pregunta o sugerencia, no dudes en contactarme.
