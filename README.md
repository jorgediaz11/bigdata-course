# Big Data Course — Proyecto integrador

Ejercicios prácticos de Big Data con Python, MongoDB, Apache Spark y Kafka. El proyecto recorre desde la conexión a una base de datos y el análisis con DataFrames hasta el procesamiento de eventos y la arquitectura de medallón (Bronze, Silver y Gold).

> **Nota:** es un proyecto educativo. La arquitectura de medallón y el pipeline final son demostraciones, no una configuración lista para producción.

## Contenido

- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Servicios con Docker](#servicios-con-docker)
- [Ejercicios](#ejercicios)
- [Pipeline de streaming](#pipeline-de-streaming)
- [Datos y resultados](#datos-y-resultados)

## Tecnologías

| Área | Tecnologías |
| --- | --- |
| Lenguaje y análisis | Python, Pandas, NumPy |
| Procesamiento distribuido | Apache Spark (PySpark) |
| Streaming | Apache Kafka y Zookeeper (imágenes de Confluent) |
| Base de datos | MongoDB |
| Visualización | Matplotlib y Seaborn |
| Contenedores | Docker Compose |
| Entorno interactivo | Jupyter y IPython kernel |
| Orquestación opcional | Apache NiFi |

Las dependencias de Python del entorno de aprendizaje están declaradas en [`requirements.txt`](requirements.txt). Las versiones no están fijadas en ese archivo.

## Estructura del proyecto

```text
.
├── data/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docker-compose.yml              # MongoDB
├── docker-compose.kafka.yml        # Kafka y Zookeeper
├── docker-compose.nifi.yml         # NiFi opcional
├── notebooks/                      # Ejercicios en scripts Python
├── requirements.txt
├── results/                        # Resultados y gráficos
├── src/
│   └── streaming/
│       └── kafka_producer.py
└── verify_env.py
```

## Requisitos

- Python instalado.
- Docker Desktop (o Docker Engine con Docker Compose).
- Java compatible con la versión de PySpark instalada, para ejecutar los ejercicios de Spark.
- Git, si se clona el repositorio.

## Instalación

Desde la carpeta del proyecto, crea y activa un entorno virtual en Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Para comprobar las dependencias principales:

```powershell
python verify_env.py
```

El verificador comprueba PySpark, Pandas, NumPy, Jupyter, Matplotlib y Seaborn. Los ejercicios de integración con Kafka y MongoDB también requieren paquetes que no están incluidos en `requirements.txt`; instálalos si vas a ejecutar esos ejercicios:

```powershell
python -m pip install kafka-python pymongo
```

## Servicios con Docker

Inicia solo MongoDB:

```powershell
docker compose up -d
```

Inicia Kafka y Zookeeper en otra terminal:

```powershell
docker compose -f docker-compose.kafka.yml up -d
```

NiFi es opcional:

```powershell
docker compose -f docker-compose.nifi.yml up -d
```

Para detener cada conjunto de servicios, ejecuta `docker compose down` con los mismos archivos `-f` usados al iniciarlo. MongoDB expone el puerto `27017`, Kafka el `9092` y NiFi el `8080`. Consulta los archivos Compose para revisar la configuración local de cada servicio.

## Ejercicios

Los archivos de `notebooks/` son scripts `.py` y se ejecutan desde la raíz del proyecto. Por ejemplo:

```powershell
python notebooks/01_mongo_connection.py
python notebooks/03_spark_dataframes.py
```

| Archivo | Tema |
| --- | --- |
| `hello_bigdata.py` | Primer DataFrame con PySpark |
| `01_mongo_connection.py` | Conexión e ingesta en MongoDB |
| `02_spark_config.py` | Configuración de Spark |
| `03_spark_dataframes.py` | DataFrames y transformaciones |
| `04_spark_optimization.py` | Planes de ejecución y caché |
| `05_spark_io.py` | Lectura y escritura de datos |
| `06_spark_streaming.py` | Lectura de Kafka con Spark Structured Streaming |
| `07_medallion_architecture.py` | Capas Bronze, Silver y Gold con Pandas |
| `08_data_visualization.py` | Visualización de datos agregados |
| `09_data_quality.py` | Validaciones de esquema y reglas de calidad |
| `10_final_pipeline.py` | Micro-lotes de Kafka a MongoDB |

Algunos ejercicios de datos y visualización usan rutas locales definidas dentro de sus scripts. Si el proyecto está en otra ubicación, revisa y ajusta esas rutas antes de ejecutarlos.

## Pipeline de streaming

El pipeline final consume eventos del tópico `ventas_en_vivo`, filtra registros con datos inválidos, agrega ventas por categoría y actualiza MongoDB. Para probarlo:

1. Inicia MongoDB y Kafka con los comandos anteriores.
2. En una terminal, inicia el productor:

   ```powershell
   python src/streaming/kafka_producer.py
   ```

3. En otra terminal, ejecuta el consumidor y procesador:

   ```powershell
   python notebooks/10_final_pipeline.py
   ```

El productor envía eventos continuamente; detén cada proceso con `Ctrl+C`. El ejercicio `06_spark_streaming.py` es una alternativa que lee el tópico y muestra agregaciones con Spark.

## Datos y resultados

El ejercicio de medallón genera archivos intermedios en `data/bronze/`, `data/silver/` y `data/gold/`. Los gráficos y otros resultados se guardan en `results/`. Estas salidas pueden depender de los datos y de la ubicación configurada en cada script.

## 📂 Documentación Detallada

Para información técnica profunda, consulta la carpeta `docs/`:
- 🛠️ [01. Guía de Instalación](docs/01_guia_instalacion.md)
- 🏗️ [02. Arquitectura del Sistema](docs/02_arquitectura_del_sistema.md)
- 📚 [03. Diccionario de Datos y Gobernanza](docs/03_diccionario_de_datos.md)
- 🛠️ [04. Guía de Solución de Problemas](docs/04_troubleshooting.md)