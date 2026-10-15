"""
Spark I/O: Lectura y Escritura de Datos
=======================================
Objetivo: Aprender a leer y escribir datos en los formatos 
más utilizados en Big Data: CSV, JSON y Parquet.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col

print("=" * 70)
print("📂 SPARK I/O: MANEJO DE FORMATOS DE DATOS")
print("=" * 70)

# 1. Crear la SparkSession
spark = SparkSession.builder \
    .appName("SparkIO") \
    .master("local[*]") \
    .getOrCreate()

# Datos de prueba
datos = [
    (1, "Laptop", "Electrónica", 1200),
    (2, "Smartphone", "Electrónica", 800),
    (3, "Escritorio", "Muebles", 300),
    (4, "Silla", "Muebles", 150)
]
columnas = ["id", "producto", "categoria", "precio"]
df = spark.createDataFrame(datos, columnas)

print("\n📊 DataFrame original creado:")
df.show()

# ---------------------------------------------------------
# ESCRITURA DE DATOS
# ---------------------------------------------------------

# 2. Guardar como CSV
print("💾 Guardando como CSV...")
df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv("data/raw/ventas.csv")
print("   ✅ CSV guardado en data/raw/ventas.csv")

# 3. Guardar como JSON
print("💾 Guardando como JSON...")
df.write \
    .mode("overwrite") \
    .json("data/raw/ventas.json")
print("   ✅ JSON guardado en data/raw/ventas.json")

# 4. Guardar como Parquet (El estándar de Big Data)
print(" Guardando como Parquet...")
df.write \
    .mode("overwrite") \
    .parquet("data/processed/ventas.parquet")
print("   ✅ Parquet guardado en data/processed/ventas.parquet")

# ---------------------------------------------------------
# LECTURA DE DATOS
# ---------------------------------------------------------

# 5. Leer desde Parquet
print("\n Leyendo desde Parquet...")
df_leido = spark.read.parquet("data/processed/ventas.parquet")

print("   • Esquema del archivo Parquet leído:")
df_leido.printSchema()

print("   • Vista previa de los datos leídos:")
df_leido.show()

# 6. Operación simple sobre los datos leídos
print("🔍 Filtrando productos de 'Electrónica' desde el Parquet leído:")
df_leido.filter(col("categoria") == "Electrónica").show()

# 7. Cerrar sesión
spark.stop()
print("\n" + "=" * 70)
print("✅ ¡SPARK I/O COMPLETADO EXITOSAMENTE!")
print("=" * 70)