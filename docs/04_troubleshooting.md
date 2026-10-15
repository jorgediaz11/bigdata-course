# 🛠️ 04. Guía de Solución de Problemas (Troubleshooting)

Documentación de los errores reales encontrados durante el desarrollo y sus soluciones. Esto demuestra capacidad de debugging y adaptación.

## 1. Error: `UnsatisfiedLinkError: NativeIO$Windows.access0` en PySpark
**Síntoma:** Al intentar escribir archivos o iniciar Spark Streaming en Windows, el proceso falla con un error de Java relacionado con `winutils.exe` o `hadoop.dll`.

**Causa:** Spark intenta usar librerías nativas de Hadoop para gestionar permisos de archivos en Windows, las cuales no están presentes o están bloqueadas por el sistema operativo.

**Solución Aplicada:**
1. Se descargaron `winutils.exe` y `hadoop.dll` compatibles con Hadoop 3.x en `C:\hadoop\bin`.
2. Se estableció la variable de entorno: `$env:HADOOP_HOME = "C:\hadoop"`.
3. **Mejora Arquitectónica Final:** Para el pipeline de producción local, se migró la lógica de streaming de *Spark Structured Streaming* a un **Micro-Batch en Python puro** (`kafka-python` + `pandas`). Esto elimina la dependencia de las librerías nativas de Java/Hadoop en la escritura, haciendo el pipeline 100% estable en entornos Windows locales.

## 2. Error: `PermissionError: [Errno 13]` al escribir CSV
**Síntoma:** Pandas o Spark no pueden sobrescribir un archivo en la carpeta `data/`.
**Causa:** Un proceso anterior de Python/Spark no se cerró correctamente y dejó el archivo bloqueado por el sistema operativo.
**Solución:** El script incluye una validación previa: `if bronze_path.exists(): bronze_path.unlink()` para liberar y limpiar el archivo antes de la escritura.