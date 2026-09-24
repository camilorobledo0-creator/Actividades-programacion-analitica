# %%
import pandas as pd
import numpy as np

url = "https://raw.githubusercontent.com/plotly/datasets/master/supermarket_Sales.csv"

data = pd.read_csv(url)

data = data.rename(columns={
    'Tax 5%': 'Tax',
    'Cost of goods sold': 'Cogs',
    'Gross margin percentage': 'Gross margin pct',
    'Customer stratification rating': 'Rating'
})

data.columns = (
    data.columns
    .str.strip()
    .str.lower()
    .str.replace(' ', '_')
)


# %%
# 1. Dimensiones del DataFrame
# Complete la instrucción para conocer el número de filas y de columnas.
print(data.shape)


# %%
# 2. Columnas, tipos y primeras filas
# Muestre los nombres de las columnas, el tipo de dato de cada una y las tres primeras ventas registradas.
print(data.columns)
print(data.dtypes)
print(data.head(3))


# %%
# 3. Seleccionar varias columnas
# Construya un subconjunto que contenga únicamente product_line, quantity y total.
resultado = data[['product_line', 'quantity', 'total']]
print(resultado.head())


# %%
# 4. ¿Series o DataFrame?
# Antes de ejecutar, anote qué objeto devuelve cada línea. Después compruébelo.
print(type(data['total']))
print(type(data[['total']]))


# %%
# 5. loc y iloc sobre la misma celda
# Las dos instrucciones deben mostrar la línea de producto de la fila con índice 7.
print(data.loc[7, 'product_line'])
print(data.iloc[7, 5])


# %%
# 6. Una sola condición
# Conserve únicamente las ventas de más de ocho unidades y cuente cuántas son.
mascara = data['quantity'] > 8
resultado = data[mascara]
print(resultado.shape[0])


# %%
# 7. Dos condiciones al tiempo
# Obtenga únicamente las ventas de la sucursal C cuyo total sea mayor de 300 USD.
mascara = (data['branch'] == 'C') & (data['total'] > 300)
resultado = data[mascara]
print(resultado.shape)


# %%
# 8. Corregir un filtro por categorías
# Reescriba el filtro con una sola llamada que reciba la lista de líneas de producto.
mascara = data['product_line'].isin(['Food and beverages', 'Fashion accessories'])
print(data[mascara].shape[0])


# %%
# 9. Rango de valores y columnas elegidas
# Obtenga las ventas de las sucursales A y C cuyo total se encuentre entre 200 y 500 USD,
# mostrando solamente branch, product_line, quantity y total.
mascara = (data['branch'].isin(['A', 'C'])) & (data['total'].between(200, 500))
resultado = data.loc[mascara, ['branch', 'product_line', 'quantity', 'total']]
print(resultado.head())


# %%
# 10. Valor de cada unidad vendida
# Cree la columna valor_unitario dividiendo el total entre la cantidad.
data['valor_unitario'] = data['total'] / data['quantity']
print(data['valor_unitario'].head(3).round(2))


# %%
# 11. Clasificar cada venta
# Marque como volumen las ventas de seis unidades o más y como menor todas las demás.
data['tipo_compra'] = np.where(
    data['quantity'] >= 6,
    'volumen',
    'menor'
)
print(data['tipo_compra'].value_counts())


# %%
# 12. ¿Cuánto ingreso genera cada sucursal?
# Complete la agrupación que responde la pregunta.
resumen = (
    data
    .groupby('branch')['total']
    .sum()
)

print(resumen.round(2))


# %%
# 13. ¿Cuántas facturas registra cada método de pago?
# Complete la columna sobre la que se cuenta y la operación correspondiente.
resumen = (
    data
    .groupby('payment')['invoice_id']
    .count()
)

print(resumen)


# %%
# 14. Varias métricas por método de pago
# ¿Cuántas facturas, cuántas unidades y cuánto ingreso deja cada método de pago?
resumen = (
    data
    .groupby('payment')
    .agg(
        facturas=('invoice_id', 'size'),
        unidades=('quantity', 'sum'),
        ingreso=('total', 'sum')
    )
    .reset_index()
)

print(resumen.round(2))


# %%
# 15. Agregar la zona de cada sucursal
# Integre la información de las sucursales conservando todas las ventas.
sucursales = pd.DataFrame({
    'branch': ['A', 'B', 'C'],
    'zona': ['Centro', 'Norte', 'Sur']
})

resultado = data.merge(
    sucursales,
    on='branch',
    how='left'
)

print(resultado.shape)
print(resultado[['branch', 'city', 'zona', 'total']].head())


# %%
# 16. La sucursal líder entre los clientes Member
# Considere únicamente las ventas de clientes de tipo Member.
# Determine qué sucursal genera el mayor ingreso total y cuál es su ticket promedio.

member = data[data['customer_type'] == 'Member']

resumen = (
    member
    .groupby('branch')
    .agg(
        facturas=('invoice_id', 'size'),
        ingreso=('total', 'sum')
    )
    .reset_index()
)

resumen['ticket_promedio'] = resumen['ingreso'] / resumen['facturas']

resumen = resumen.sort_values('ingreso', ascending=False)

print(resumen.round(2))


# %%
# Autoevaluación rápida

# 1. ¿Puedo distinguir entre una Series y un DataFrame?
# Sí, una Series representa una sola columna y un DataFrame representa una tabla.

# 2. ¿Puedo seleccionar filas y columnas usando loc?
# Sí, loc permite seleccionar datos utilizando etiquetas.

# 3. ¿Puedo construir filtros con una o varias condiciones?
# Sí, puedo utilizar una o varias condiciones para filtrar los datos.

# 4. ¿Puedo usar groupby para responder una pregunta sobre los datos?
# Sí, groupby permite agrupar datos y calcular resúmenes.

# 5. ¿Puedo explicar qué problema resuelve merge?
# Sí, merge permite integrar información de dos tablas mediante una clave común.
