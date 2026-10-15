"""
Visualización de Datos: Reporte Automatizado desde la Capa Gold
===============================================================
Objetivo: Leer los datos agregados de la capa Gold y generar 
un gráfico profesional automatizado usando Seaborn y Matplotlib.
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path

print("=" * 70)
print("📈 GENERANDO REPORTE VISUAL AUTOMATIZADO DESDE LA CAPA GOLD")
print("=" * 70)

# 1. Definir rutas
BASE_DIR = Path("C:/ProyectosPYT/bigdata-course")
GOLD_PATH = BASE_DIR / "data" / "gold" / "ventas_por_categoria.csv"
RESULTS_DIR = BASE_DIR / "results"

# Asegurar que la carpeta de resultados existe
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# 2. Leer los datos de la capa Gold
print(f"\n📂 Leyendo datos desde: {GOLD_PATH}")
df_gold = pd.read_csv(GOLD_PATH)
print("   ✅ Datos cargados correctamente.")
print(df_gold.to_string(index=False))

# 3. Configurar el estilo del gráfico (Seaborn)
sns.set_theme(style="whitegrid", palette="muted")
plt.figure(figsize=(10, 6))

# 4. Crear el gráfico de barras
# Usamos 'ingreso_total' en el eje Y y 'categoria' en el eje X
bar_plot = sns.barplot(
    data=df_gold, 
    x="categoria", 
    y="ingreso_total", 
    hue="categoria", 
    palette="Blues_r", 
    legend=False
)

# 5. Personalizar el gráfico
plt.title("Ingresos Totales por Categoría de Producto", fontsize=16, fontweight='bold', pad=15)
plt.xlabel("Categoría", fontsize=12)
plt.ylabel("Ingreso Total ($)", fontsize=12)

# Añadir las etiquetas de valor encima de cada barra
for p in bar_plot.patches:
    bar_plot.annotate(f"${p.get_height():.2f}", 
                      (p.get_x() + p.get_width() / 2., p.get_height()), 
                      ha='center', va='bottom', fontsize=11, fontweight='bold')

# 6. Guardar el gráfico como imagen en la carpeta results
output_path = RESULTS_DIR / "dashboard_ingresos.png"
plt.tight_layout()
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"\n💾 Gráfico guardado exitosamente en: {output_path}")

print("\n" + "=" * 70)
print("✅ ¡REPORTE VISUAL GENERADO EXITOSAMENTE!")
print("   Abre la carpeta 'results' en VSCode para ver tu dashboard.")
print("=" * 70)

# Opcional: Mostrar el gráfico en pantalla (descomenta la siguiente línea si quieres verlo)
# plt.show()