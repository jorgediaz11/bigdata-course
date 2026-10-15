"""
Spark SQL y DataFrames: Transformaciones y Acciones
===================================================
Objetivo: Crear un DataFrame, aplicar transformaciones (filter, groupBy, agg)
y ejecutar acciones (show, count, printSchema) para analizar datos.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg, desc

print("=" * 70)
print("🚀 INICIANDO ANÁLISIS DE DATOS CON SPARK DATAFRAMES")
print("=" * 70)

# 1. Crear la SparkSession
spark = SparkSession.builder \
    .appName("SparkDataFrames") \
    .master("local[*]") \
    .getOrCreate()

# 2. Datos de prueba (simulando un JSON o CSV de ventas)
datos_ventas = [
    {"id": 1, "producto": "Laptop", "categoria": "Electrónica", "precio": 1200, "ventas": 50},
    {"id": 2, "producto": "Smartphone", "categoria": "Electrónica", "precio": 800, "ventas": 120},
    {"id": 3, "producto": "Escritorio", "categoria": "Muebles", "precio": 300, "ventas": 30},
    {"id": 4, "producto": "Silla", "categoria": "Muebles", "precio": 150, "ventas": 80},
    {"id": 5, "producto": "Monitor", "categoria": "Electrónica", "precio": 400, "ventas": 60},
    {"id": 6, "producto": "Teclado", "categoria": "Electrónica", "precio": 100, "ventas": 200},
]

# 3. Crear el DataFrame
df = spark.createDataFrame(datos_ventas)

print("\n📊 1. ESQUEMA DEL DATAFRAME (printSchema):")
df.printSchema()

print("\n📋 2. VISTA PREVIA DE LOS DATOS (show):")
df.show(truncate=False)

# ---------------------------------------------------------
# TRANSFORMACIONES (Lazy Evaluation: solo se planifican)
# ---------------------------------------------------------

# A. Filtrar: Solo productos de "Electrónica" con precio > 500
df_filtrado = df.filter((col("categoria") == "Electrónica") & (col("precio") > 500))

# B. Seleccionar columnas específicas y crear una nueva (ingreso total)
df_ingresos = df_filtrado.select(
    "producto", 
    "precio", 
    "ventas",
    (col("precio") * col("ventas")).alias("ingreso_total")
)

# C. Agrupar y agregar: Suma de ventas y promedio de precio por categoría
df_agrupado = df.groupBy("categoria").agg(
    sum("ventas").alias("total_ventas"),
    avg("precio").alias("precio_promedio")
).orderBy(desc("total_ventas")) # Ordenar de mayor a menor

# ---------------------------------------------------------
# ACCIONES (Ejecutan el plan de Spark y traen resultados)
# ---------------------------------------------------------

print("\n🔍 3. RESULTADO DE FILTRADO Y CÁLCULO DE INGRESOS:")
df_ingresos.show(truncate=False)

print("\n📈 4. RESULTADO DE AGRUPACIÓN (Ventas totales por categoría):")
df_agrupado.show(truncate=False)

print("\n🔢 5. ACCIONES DE CONTEO:")
print(f"   • Total de filas en el DataFrame original: {df.count()}")
print(f"   • Total de filas después del filtrado: {df_filtrado.count()}")

# 6. Cerrar la sesión
spark.stop()
print("\n" + "=" * 70)
print("✅ ¡ANÁLISIS DE DATAFRAMES COMPLETADO EXITOSAMENTE!")
print("=" * 70)