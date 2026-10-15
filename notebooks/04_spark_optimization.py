"""
Optimización en Spark: Catalyst y Caching
=========================================
Objetivo: Visualizar el plan de ejecución de Catalyst y 
comprender cómo el caching mejora el rendimiento en iteraciones.
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum

print("=" * 70)
print("⚡ OPTIMIZACIÓN DE CONSULTAS EN SPARK")
print("=" * 70)

spark = SparkSession.builder \
    .appName("SparkOptimization") \
    .master("local[*]") \
    .getOrCreate()

# 1. Crear un DataFrame de prueba
datos = [
    {"id": 1, "categoria": "A", "valor": 100},
    {"id": 2, "categoria": "B", "valor": 200},
    {"id": 3, "categoria": "A", "valor": 150},
    {"id": 4, "categoria": "C", "valor": 300},
]
df = spark.createDataFrame(datos)

# ---------------------------------------------------------
# PARTE A: El Optimizador Catalyst (.explain)
# ---------------------------------------------------------
print("\n🔍 1. PLAN DE EJECUCIÓN (Catalyst Optimizer):")
print("   Vamos a filtrar 'categoria == A' y sumar 'valor'.")

df_optimizado = df.filter(col("categoria") == "A").agg(sum("valor").alias("total"))

# .explain(True) muestra: Lógico Analizado, Lógico Optimizado y Plan Físico
df_optimizado.explain(True)

print("\n💡 NOTA: Observa cómo Catalyst 'empuja' el filtro (Filter) antes de la agregación (Aggregate).")
print("   Esto significa que Spark reduce los datos lo antes posible, ahorrando recursos.")

# ---------------------------------------------------------
# PARTE B: Caching y Persistencia
# ---------------------------------------------------------
print("\n💾 2. PRUEBA DE CACHING:")

# Creamos un DataFrame que usaremos múltiples veces
df_pesado = df.filter(col("valor") > 50)

# SIN CACHE: Spark recalcula todo cada vez que llamamos una acción
print("   • Primera acción (count) SIN cache...")
print(f"     Resultado: {df_pesado.count()}")

print("   • Segunda acción (sum) SIN cache... (Spark vuelve a evaluar el filtro)")
print(f"     Resultado: {df_pesado.agg(sum('valor')).collect()[0][0]}")

# CON CACHE: Le decimos a Spark que guarde el resultado en memoria
print("\n   • Aplicando .cache() al DataFrame...")
df_pesado.cache()

# La PRIMERA acción después de .cache() materializa los datos en memoria
print("   • Primera acción CON cache (materializando en memoria)...")
print(f"     Resultado: {df_pesado.count()}")

# La SEGUNDA acción lee directamente de la memoria (mucho más rápido en datasets grandes)
print("   • Segunda acción CON cache (leyendo de memoria RAM)...")
print(f"     Resultado: {df_pesado.agg(sum('valor')).collect()[0][0]}")

# Limpiar el cache cuando ya no se necesita (buena práctica)
spark.catalog.clearCache()
print("\n   • Caché liberado correctamente.")

# 3. Cerrar sesión
spark.stop()
print("\n" + "=" * 70)
print("✅ ¡OPTIMIZACIÓN DE SPARK COMPLETADA EXITOSAMENTE!")
print("=" * 70)