"""
PySpark Streaming Consumer: Procesamiento en Tiempo Real
========================================================
Objetivo: Leer un stream de Kafka, parsear el JSON y 
calcular agregaciones en tiempo real (ventana continua).
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, avg, count
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType

print("=" * 70)
print("⚡ INICIANDO SPARK STREAMING CONSUMER...")
print("=" * 70)

# 1. Crear SparkSession con los paquetes de Kafka integrados
# Nota: Es crucial incluir spark-sql-kafka para que Spark pueda leer de Kafka
spark = SparkSession.builder \
    .appName("SparkStreamingKafka") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .config("spark.kafka.bootstrap.servers", "localhost:9092") \
    .getOrCreate()

# Reducir la verbosidad de los logs de Spark para ver mejor nuestra salida
spark.sparkContext.setLogLevel("ERROR")

# 2. Definir el esquema de los datos JSON que esperamos recibir
schema = StructType([
    StructField("id_venta", IntegerType(), True),
    StructField("producto", StringType(), True),
    StructField("categoria", StringType(), True),
    StructField("precio", DoubleType(), True),
    StructField("timestamp", StringType(), True)
])

# 3. Leer el stream desde Kafka
print("📡 Conectando al tópico 'ventas_en_vivo' en Kafka...")
df_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ventas_en_vivo") \
    .option("startingOffsets", "latest") \
    .load()

# 4. Transformar los datos: Extraer el valor (que viene en bytes) y parsear el JSON
df_parsed = df_stream.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")

# 5. Agregación en tiempo real: Conteo y precio promedio por categoría
df_aggregado = df_parsed.groupBy("categoria").agg(
    count("id_venta").alias("total_ventas"),
    avg("precio").alias("precio_promedio")
)

# 6. Escribir el resultado en la consola (modo 'complete' muestra toda la tabla actualizada)
print("\n📊 PROCESANDO STREAM EN TIEMPO REAL (Se actualizará cada 3 segundos):")
print("   (Abre otra terminal y ejecuta el 'kafka_producer.py' para ver los datos fluir)")
print("-" * 70)

query = df_aggregado.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .trigger(processingTime="3 seconds") \
    .start()

# Mantener el stream activo hasta que el usuario presione Ctrl+C
try:
    query.awaitTermination()
except KeyboardInterrupt:
    print("\n🛑 Spark Streaming detenido por el usuario.")
    query.stop()