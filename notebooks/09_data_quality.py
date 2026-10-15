"""
Data Quality Validator: Implementación de Esquemas y Expectativas
=================================================================
Objetivo: Simular el comportamiento de 'Great Expectations' validando 
el esquema y las reglas de negocio de los datos crudos (Bronze).
"""

import pandas as pd
from pathlib import Path
from datetime import datetime

print("=" * 70)
print("🛡️ EJECUTANDO VALIDADOR DE CALIDAD DE DATOS")
print("=" * 70)

# 1. Cargar datos crudos (Bronze)
BASE_DIR = Path("C:/ProyectosPYT/bigdata-course")
bronze_path = BASE_DIR / "data" / "bronze" / "ventas_raw.csv"
df = pd.read_csv(bronze_path)

print(f"\n📂 Datos cargados desde Bronze: {len(df)} filas.")

# =========================================================================
# 2. DEFINICIÓN DEL ESQUEMA (Schema Validation)
# =========================================================================
print("\n📋 1. VALIDACIÓN DE ESQUEMA (Tipos de datos esperados):")

esquema_esperado = {
    "id": "int64",
    "producto": "object", # object en Pandas significa string
    "categoria": "object",
    "precio": "float64",
    "fecha": "object"
}

errores_esquema = 0
for columna, tipo in esquema_esperado.items():
    if columna in df.columns:
        tipo_real = str(df[columna].dtype)
        if tipo_real == tipo:
            print(f"   ✅ {columna:<12} | Esperado: {tipo:<8} | Real: {tipo_real}")
        else:
            print(f"   ❌ {columna:<12} | Esperado: {tipo:<8} | Real: {tipo_real} (¡Error!)")
            errores_esquema += 1
    else:
        print(f"   ❌ {columna:<12} | ¡La columna no existe en el archivo!")
        errores_esquema += 1

# =========================================================================
# 3. DEFINICIÓN DE EXPECTATIVAS (Business Rules Validation)
# =========================================================================
print("\n📏 2. VALIDACIÓN DE EXPECTATIVAS (Reglas de Negocio):")

expectativas = [
    {
        "nombre": "expect_column_values_to_not_be_null",
        "columna": "producto",
        "regla": df["producto"].notnull(),
        "descripcion": "El producto no puede estar vacío"
    },
    {
        "nombre": "expect_column_values_to_be_between",
        "columna": "precio",
        "regla": df["precio"] > 0,
        "descripcion": "El precio debe ser mayor a 0"
    },
    {
        "nombre": "expect_column_values_to_match_regex",
        "columna": "fecha",
        "regla": df["fecha"].str.match(r'^\d{4}-\d{2}-\d{2}$', na=False),
        "descripcion": "La fecha debe tener formato YYYY-MM-DD"
    }
]

total_fallas = 0
for exp in expectativas:
    fallas = (~exp["regla"]).sum()
    total_fallas += fallas
    
    if fallas == 0:
        print(f"   ✅ {exp['nombre']}")
        print(f"      ↳ {exp['descripcion']} (0 fallas)")
    else:
        print(f"   ️  {exp['nombre']}")
        print(f"      ↳ {exp['descripcion']} ({fallas} filas incumplen la regla)")

# =========================================================================
# 4. REPORTE DE CALIDAD (Data Quality Report)
# =========================================================================
print("\n" + "=" * 70)
print("📊 REPORTE DE CALIDAD DE DATOS (Data Docs)")
print("=" * 70)

total_reglas = len(esquema_esperado) + len(expectativas)
reglas_cumplidas = total_reglas - errores_esquema - (1 if total_fallas > 0 else 0) # Simplificación para el reporte
porcentaje_calidad = max(0, 100 - ((errores_esquema + total_fallas) / (len(df) * total_reglas)) * 100)

print(f"   • Fecha de validación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"   • Total de filas analizadas: {len(df)}")
print(f"   • Errores de Esquema: {errores_esquema}")
print(f"   • Fallas en Expectativas: {total_fallas}")
print(f"   •  SCORE DE CALIDAD: {porcentaje_calidad:.1f}%")

if porcentaje_calidad < 100:
    print("\n   🚨 ALERTA: Los datos NO están listos para pasar a la capa Silver.")
    print("   💡 Acción requerida: Revisar las filas marcadas como fallidas.")
else:
    print("\n   ✅ ÉXITO: Los datos cumplen con todos los estándares de calidad.")

print("=" * 70)