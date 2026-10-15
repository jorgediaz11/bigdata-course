"""
Kafka Producer: Simulación de Datos en Tiempo Real para el Proyecto Final
"""
import json
import time
import random
from kafka import KafkaProducer

print("=" * 60)
print("🚀 INICIANDO PRODUCTOR DE KAFKA (PROYECTO FINAL)")
print("=" * 60)

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic_name = "ventas_en_vivo"
productos = ["Laptop", "Smartphone", "Monitor", "Teclado", "Silla", "Escritorio"]
categorias = ["Electrónica", "Electrónica", "Electrónica", "Accesorios", "Muebles", "Muebles"]

print(f"📡 Enviando datos al tópico: '{topic_name}' (Presiona Ctrl+C para detener)")

try:
    contador = 1
    while True:
        idx = random.randint(0, len(productos) - 1)
        
        # Simulamos occasionalmente datos "sucios" para probar la gobernanza en Spark
        if random.random() < 0.1: # 10% de probabilidad de dato sucio
            precio = -50.00 # Precio negativo (será filtrado por Spark)
            producto = None # Producto nulo (será filtrado por Spark)
        else:
            precio = round(random.uniform(50.0, 1500.0), 2)
            producto = productos[idx]

        evento = {
            "id_venta": contador,
            "producto": producto,
            "categoria": categorias[idx],
            "precio": precio,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        producer.send(topic_name, value=evento)
        print(f"   ✅ Enviado: {evento['producto']} | ${evento['precio']}")
        
        contador += 1
        time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 Productor detenido.")
finally:
    producer.flush()
    producer.close()