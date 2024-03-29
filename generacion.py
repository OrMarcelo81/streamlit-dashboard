import sqlite3
import random
import names
from datetime import datetime, timedelta

# Conexión a la base de datos
conn = sqlite3.connect('facturacion.db')
cursor = conn.cursor()

# Crear tabla de ventas si no existe
cursor.execute('''CREATE TABLE IF NOT EXISTS facturacion (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    numero_factura TEXT,
                    cliente TEXT,
                    producto TEXT,
                    genero TEXT,
                    cantidad INTEGER,
                    precio INTEGER,
                    descuento INTEGER,
                    total_pagado INTEGER,
                    medio_pago TEXT
                )''')
conn.commit()

# Función para generar números de factura
def generar_numero_factura():
    numero = 0
    while True:
        numero += 1
        yield f"{numero:06d}"

# Definir función generadora de fechas de emisión de factura
def generar_fecha_emision(fecha_inicial):
    fecha_actual = fecha_inicial
    while True:
        minutos_aleatorios = random.randint(60, 180)
        fecha_actual += timedelta(minutes=minutos_aleatorios)
        yield fecha_actual

# Fecha factura
fecha_inicial = datetime(2024, 1, 1)
fecha_emision = generar_fecha_emision(fecha_inicial)

# Definir productos
productos = {
    "libro": ["literatura", "educativo", "suspenso", "fantasia"],
    "oficina": ["lapiz", "cuaderno"],
    "obsequio": ["vaso", "rompecabezas", "juegos de mesa"]
}

total_facturas = 1500
nroFactura = generar_numero_factura()

# Generar registros de ventas
for i in range(total_facturas):
    # Generar nueva factura
    if i == 0:
        numero_factura = f"001-001-{next(nroFactura)}"
        fecha = next(fecha_emision)
        cliente = names.get_full_name()
        medio_pago = random.choices(['efectivo', 'tarjeta', 'QR', 'transferencia'], weights=[0.65, 0.20, 0.10, 0.05])[0]
    elif random.randint(1, 3) in [1, 3]:
        numero_factura = f"001-001-{next(nroFactura)}"
        fecha = next(fecha_emision)
        cliente = names.get_full_name()
        medio_pago = random.choices(['efectivo', 'tarjeta', 'QR', 'transferencia'], weights=[0.65, 0.20, 0.10, 0.05])[0]

    # Generar producto
    producto = random.choices(list(productos.keys()), weights=[0.80, 0.15, 0.05])[0]

    # Generar genero
    if producto == 'libro':
        genero = random.choices(productos['libro'], weights=[0.55, 0.15, 0.10, 0.20])[0]
    elif producto == 'oficina':
        genero = random.choices(productos['oficina'], weights=[0.30, 0.70])[0]
    else:
        genero = random.choices(productos['obsequio'], weights=[0.20, 0.35, 0.45])[0]

    # Generar precio y cantidad
    if producto == 'libro':
        precio = round(random.randint(70000, 400000) / 10000) * 10000
    elif producto == 'oficina':
        if genero == 'lapiz':
            precio = round(random.randint(5000, 25000) / 1000) * 1000
        else:
            precio = round(random.randint(15000, 75000) / 1000) * 1000
    else:
        if genero == 'vaso':
            precio = round(random.randint(25000, 75000) / 1000) * 1000
        else:
            precio = round(random.randint(35000, 230000) / 1000) * 1000
        
    cantidad = random.choices([1, 2, 3, 4, 5], weights=[0.45, 0.30, 0.15, 0.06, 0.04])[0]

    # Calcular descuento y total pagado
    if medio_pago == 'efectivo':
        descuento = (precio * cantidad) * 0.1
    elif medio_pago in ['tarjeta', 'QR']:
        descuento = (precio * cantidad) * 0.2
    else:
        descuento = (precio * cantidad) * 0.3
    
    total_pagado = (precio * cantidad) - descuento

    # Insertar registro en la tabla de facturación
    cursor.execute('''INSERT INTO facturacion (fecha, numero_factura, cliente, producto, genero, cantidad, precio, descuento, total_pagado, medio_pago) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (fecha, numero_factura, cliente, producto, genero, cantidad, precio, descuento, total_pagado, medio_pago))

# Confirmar cambios y cerrar conexión
conn.commit()
conn.close()
