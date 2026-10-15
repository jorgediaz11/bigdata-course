"""
Verificación de Configuración de PySpark
========================================
Objetivo: Confirmar que PySpark se comunica correctamente con Java 
y mostrar la configuración por defecto de la SparkSession.
"""
import os
from pyspark.sql import SparkSession

print("=" * 60)
print("⚙️ VERIFICANDO CONFIGURACIÓN DE PYSPARK")
print("=" * 60)

# 1. Verificar variable de entorno JAVA_HOME
java_home = os.environ.get("JAVA_HOME", "No establecida (usando PATH del sistema)")
print(f"📍 JAVA_HOME detectado: {java_home}")

# 2. Crear SparkSession con configuración explícita para desarrollo local
spark = SparkSession.builder \
    .appName("ConfiguracionPySpark") \
    .master("local[*]") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

print("\n✅ SparkSession creada exitosamente.")
print(f"   • Versión de Spark: {spark.version}")
print(f"   • Modo de ejecución (Master): {spark.sparkContext.master}")

# Obtener configuración clave del contexto de Spark
sc = spark.sparkContext
print(f"   • Núcleos de CPU disponibles (defaultParallelism): {sc.defaultParallelism}")
print(f"   • Interfaz Web de Spark (Spark UI): {sc.uiWebUrl}")

print("\n" + "=" * 60)
print("✅ ¡CONFIGURACIÓN LOCAL VERIFICADA CORRECTAMENTE!")
print("=" * 60)

# 3. Cerrar la sesión para liberar recursos
spark.stop()
print("🔌 SparkSession cerrada.")