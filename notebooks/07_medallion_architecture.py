"""
Arquitectura de Medalla: Bronze -> Silver -> Gold (Versión Pandas)
==================================================================
Objetivo: Simular un pipeline de Data Lake moderno usando Pandas.
En producción real se usaría PySpark, pero Pandas es 100% estable en Windows
y nos permite enfocarnos en el concepto de transformación de datos.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("🏆 INICIANDO PIPELINE DE ARQUITECTURA DE MEDALLA")
print("=" * 70)

# 1. Definir rutas absolutas
BASE_DIR = Path("C:/ProyectosPYT/bigdata-course")
BRONZE_DIR = BASE_DIR / "data" / "bronze"
SILVER_DIR = BASE_DIR / "data" / "silver"
GOLD_DIR = BASE_DIR / "data" / "gold"

# Crear carpetas si no existen
BRONZE_DIR.mkdir(parents=True, exist_ok=True)
SILVER_DIR.mkdir(parents=True, exist_ok=True)
GOLD_DIR.mkdir(parents=True, exist_ok=True)

# =========================================================================
# NIVEL 1: BRONZE (Ingesta Cruda)
# =========================================================================
print("\n🥉 1. NIVEL BRONZE: Ingesta de datos crudos...")

datos_crudos = [
    (1, "laptop", "electronica", 1200.50, "2023-10-01"),
    (2, "SMARTPHONE", "Electronica", 800.00, "2023-10-02"),
    (3, None, "muebles", 300.00, "2023-10-03"),       # Producto nulo (error)
    (4, "silla", "Muebles", 150.75, "2023-10-04"),
    (5, "monitor", "electronica", -50.00, "2023-10-05") # Precio negativo (error)
]

df_bronze = pd.DataFrame(datos_crudos, columns=["id", "producto", "categoria", "precio", "fecha"])
bronze_path = BRONZE_DIR / "ventas_raw.csv"

if bronze_path.exists():
    bronze_path.unlink()

df_bronze.to_csv(bronze_path, index=False)
print(f"   ✅ Datos crudos guardados en {bronze_path}")
print(f"   • Total de filas: {len(df_bronze)}")

# =========================================================================
# NIVEL 2: SILVER (Limpieza y Validación)
# =========================================================================
print("\n 2. NIVEL SILVER: Limpieza y validación...")

# Leemos desde Bronze
df_silver = pd.read_csv(bronze_path)

# Reglas de calidad:
# 1. Eliminar filas donde 'producto' sea nulo
# 2. Eliminar filas donde 'precio' sea <= 0
# 3. Estandarizar 'categoria' a mayúsculas
# 4. Estandarizar 'producto' a formato título
df_silver = df_silver.dropna(subset=["producto"])
df_silver = df_silver[df_silver["precio"] > 0]
df_silver["categoria"] = df_silver["categoria"].str.upper()
df_silver["producto"] = df_silver["producto"].str.title()
df_silver["fecha_procesamiento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"   • Filas originales en Bronze: {len(df_bronze)}")
print(f"   • Filas válidas en Silver: {len(df_silver)}")
print(f"   • Filas eliminadas (datos sucios): {len(df_bronze) - len(df_silver)}")

# Guardamos en Silver como CSV (en producción sería Parquet)
silver_path = SILVER_DIR / "ventas_clean.csv"
df_silver.to_csv(silver_path, index=False)
print(f"   ✅ Datos limpios guardados en {silver_path}")

# =========================================================================
# NIVEL 3: GOLD (Agregación para Negocio)
# =========================================================================
print("\n🥇 3. NIVEL GOLD: Agregación para negocio...")

# Leemos desde Silver
df_gold = pd.read_csv(silver_path)

# Agregamos: Ventas totales y precio promedio por categoría
df_gold_agg = df_gold.groupby("categoria").agg(
    ingreso_total=("precio", "sum"),
    precio_promedio=("precio", "mean"),
    total_productos=("producto", "count")
).reset_index()

print("   • Resumen de negocio por categoría:")
print(df_gold_agg.to_string(index=False))

# Guardamos en Gold
gold_path = GOLD_DIR / "ventas_por_categoria.csv"
df_gold_agg.to_csv(gold_path, index=False)
print(f"\n   ✅ Datos agregados guardados en {gold_path}")

# =========================================================================
# CIERRE
# =========================================================================
print("\n" + "=" * 70)
print("✅ ¡ARQUITECTURA DE MEDALLA COMPLETADA EXITOSAMENTE!")
print("   Revisa las carpetas:")
print("   • data/bronze/ventas_raw.csv (datos crudos)")
print("   • data/silver/ventas_clean.csv (datos limpios)")
print("   • data/gold/ventas_por_categoria.csv (datos agregados)")
print("=" * 70)