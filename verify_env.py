"""
Script de verificación del entorno Big Data
"""
import sys

print("=" * 60)
print(f"🐍 Python Version: {sys.version.split()[0]}")
print("=" * 60)

# Lista de librerías críticas a verificar
libraries = [
    "pyspark",
    "pandas",
    "numpy",
    "jupyter",
    "matplotlib",
    "seaborn"
]

print("\n📦 Verificando Librerías:\n")

all_ok = True
for lib in libraries:
    try:
        # Importar la librería dinámicamente
        module = __import__(lib)
        # Intentar obtener la versión (algunas usan __version__, otras version)
        version = getattr(module, "__version__", getattr(module, "version", "Desconocida"))
        print(f"✅ {lib:<12} -> {version}")
    except ImportError:
        print(f"❌ {lib:<12} -> NO ENCONTRADA (Requiere instalación)")
        all_ok = False

print("\n" + "=" * 60)
if all_ok:
    print("🚀 ¡ENTORNO 100% VERIFICADO Y LISTO PARA BIG DATA!")
else:
    print("⚠️ Hay librerías faltantes. Revisa la instalación.")
print("=" * 60)