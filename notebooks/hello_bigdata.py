"""
Hello Big Data - Primer script con PySpark
==========================================
Objetivo: Verificar que el motor de Spark se inicia correctamente,
crear un DataFrame y ejecutar una transformación básica.
"""

# 1. Importar las clases necesarias de PySpark
from pyspark.sql import SparkSession

print("=" * 60)
print("🚀 INICIANDO MOTOR APACHE SPARK...")
print("=" * 60)

# 2. Crear la SparkSession (el punto de entrada a cualquier programa Spark)
spark = SparkSession.builder \
    .appName("HelloBigData") \
    .master("local[*]") \
    .getOrCreate()

print("✅ SparkSession creada exitosamente.")
print(f"   • Versión de Spark: {spark.version}")
print(f"   • Núcleos de CPU en uso: local[*] (todos los disponibles)")

# 3. Crear datos de prueba (simulando datos de ventas)
data = [
    ("Laptop", "Electrónica", 1200),
    ("Smartphone", "Electrónica", 800),
    ("Escritorio", "Muebles", 300),
    ("Silla", "Muebles", 150),
    ("Tablet", "Electrónica", 500)
]

columns = ["producto", "categoria", "precio"]

# 4. Convertir los datos en un DataFrame de Spark
df = spark.createDataFrame(data, columns)

print("\n DATAFRAME CREADO (Vista previa):")
df.show()

# 5. Ejecutar una operación de Big Data (Agrupar y sumar precios por categoría)
print("🔍 EJECUTANDO TRANSFORMACIÓN: Suma de precios por categoría...")
df.groupBy("categoria").sum("precio").show()

# 6. Detener la SparkSession (liberar recursos)
spark.stop()
print("=" * 60)
print("✅ ¡FELICITACIONES! Tu primer pipeline de Big Data se ejecutó correctamente.")
print("=" * 60)