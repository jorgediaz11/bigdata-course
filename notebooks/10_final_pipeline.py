"""
PROYECTO FINAL: Pipeline End-to-End (Kafka -> Python Micro-Batch -> MongoDB)
============================================================================
Objetivo: Consumir un stream de Kafka en micro-lotes, aplicar gobernanza de datos,
agregar los resultados y escribirlos dinámicamente en MongoDB.
"""

import json
import time
import pandas as pd
from kafka import KafkaConsumer
from pymongo import MongoClient, UpdateOne

print("=" * 70)
print("🚀 INICIANDO PIPELINE MAESTRO DE BIG DATA (MICRO-BATCH)")
print("=" * 70)

# 1. Configuración de Kafka y MongoDB
KAFKA_TOPIC = "ventas_en_vivo"
MONGO_URI = "mongodb://admin:admin123@localhost:27017/"
DB_NAME = "bigdata_course"
COLLECTION_NAME = "dashboard_ventas"

# Inicializar consumidor de Kafka
print(f"📡 Conectando a Kafka y escuchando el tópico '{KAFKA_TOPIC}'...")
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True
)

# Inicializar cliente de MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

print("⚡ PROCESANDO STREAM EN TIEMPO REAL (Micro-lotes cada 5 segundos)...")
print("   (Asegúrate de que 'kafka_producer.py' esté corriendo en otra terminal)")
print("-" * 70)

try:
    batch_id = 1
    while True:
        # 2. Recopilar datos durante una ventana de tiempo (simulando un micro-batch)
        batch_data = []
        start_time = time.time()
        
        while time.time() - start_time < 5.0: # Ventana de 5 segundos
            message = consumer.poll(timeout_ms=1000)
            for tp, messages in message.items():
                for msg in messages:
                    batch_data.append(msg.value)
        
        # Si no hay datos en este lote, continuar al siguiente
        if not batch_data:
            continue
            
        # 3. GOBERNANZA DE DATOS: Cargar en Pandas y aplicar reglas de calidad
        df = pd.DataFrame(batch_data)
        
        # Regla A: El producto no puede ser nulo
        df_clean = df.dropna(subset=["producto"])
        
        # Regla B: El precio debe ser mayor a 0
        df_clean = df_clean[df_clean["precio"] > 0]
        
        filas_filtradas = len(df) - len(df_clean)
        if filas_filtradas > 0:
            print(f"   🛡️ Gobernanza: {filas_filtradas} registros sucios filtrados del Batch {batch_id}.")

        # 4. AGREGACIÓN: Suma de ingresos y conteo de ventas por categoría
        if not df_clean.empty:
            df_agg = df_clean.groupby("categoria").agg(
                ingreso_total=("precio", "sum"),
                total_ventas=("id_venta", "count")
            ).reset_index()
            
            # 5. ESCRITURA EN MONGODB: Upsert (Actualizar si existe, Insertar si no)
            operations = []
            for _, row in df_agg.iterrows():
                operations.append(
                    UpdateOne(
                        {"categoria": row["categoria"]},
                        {
                            "$inc": {
                                "ingreso_total": float(row["ingreso_total"]),
                                "total_ventas": int(row["total_ventas"])
                            }
                        },
                        upsert=True
                    )
                )
            
            if operations:
                collection.bulk_write(operations)
                print(f"   ✅ Batch {batch_id} procesado: {len(operations)} categorías actualizadas en MongoDB.")
        
        batch_id += 1

except KeyboardInterrupt:
    print("\n🛑 Pipeline detenido por el usuario.")
finally:
    consumer.close()
    client.close()
    print("🔌 Conexiones a Kafka y MongoDB cerradas correctamente.")