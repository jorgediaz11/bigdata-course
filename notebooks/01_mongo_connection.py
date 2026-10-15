"""
Prueba de Conexión e Ingesta a MongoDB
======================================
Objetivo: Conectar Python con el contenedor Docker de MongoDB,
insertar documentos JSON (simulando datos de Big Data) y consultarlos.
"""

from pymongo import MongoClient
from datetime import datetime

print("=" * 60)
print("🔌 INTENTANDO CONEXIÓN A MONGODB...")
print("=" * 60)

# 1. Cadena de conexión (URI) con las credenciales del docker-compose.yml
uri = "mongodb://admin:admin123@localhost:27017/"

try:
    # 2. Establecer la conexión
    client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    
    # Forzar una conexión para verificar que funciona
    client.admin.command('ping')
    print("✅ ¡Conexión exitosa a MongoDB!")
    
    # 3. Seleccionar (o crear) una base de datos y una colección
    db = client["bigdata_course"]
    collection = db["ventas"]
    print(f"   • Base de datos: {db.name}")
    print(f"   • Colección: {collection.name}")

    # 4. Preparar datos de prueba (formato JSON / Diccionarios de Python)
    datos_ventas = [
        {
            "producto": "Laptop Gamer",
            "categoria": "Electrónica",
            "precio": 1500.00,
            "fecha": datetime.now(),
            "metadata": {"garantia_anos": 2, "stock": 15}
        },
        {
            "producto": "Silla Ergonómica",
            "categoria": "Muebles",
            "precio": 350.50,
            "fecha": datetime.now(),
            "metadata": {"garantia_anos": 5, "stock": 42}
        },
        {
            "producto": "Monitor 4K",
            "categoria": "Electrónica",
            "precio": 450.00,
            "fecha": datetime.now(),
            "metadata": {"garantia_anos": 3, "stock": 8}
        }
    ]

    # 5. Insertar los datos en la colección
    print("\n📥 INSERTANDO DOCUMENTOS...")
    resultado = collection.insert_many(datos_ventas)
    print(f"   • {len(resultado.inserted_ids)} documentos insertados correctamente.")

    # 6. Consultar los datos (Lectura)
    print("\n🔍 CONSULTANDO DATOS (Todos los registros):")
    print("-" * 60)
    for doc in collection.find():
        print(f"📦 {doc['producto']} | {doc['categoria']} | ${doc['precio']} | Stock: {doc['metadata']['stock']}")
    print("-" * 60)

    # 7. Consulta con filtro
    print("\n🔍 CONSULTA CON FILTRO (Solo 'Electrónica'):")
    filtro = {"categoria": "Electrónica"}
    electronicos = list(collection.find(filtro))
    print(f"   • Se encontraron {len(electronicos)} productos electrónicos.")

    print("\n" + "=" * 60)
    print("✅ ¡PIPELINE DE INGESTA NoSQL COMPLETADO EXITOSAMENTE!")
    print("=" * 60)

except Exception as e:
    print(f"❌ Error de conexión: {e}")
    print("💡 Verifica que el contenedor Docker 'bigdata-mongo' esté corriendo (docker ps).")

finally:
    if 'client' in locals():
        client.close()
        print("\n🔌 Conexión a MongoDB cerrada.")