# 📚 03. Diccionario de Datos y Gobernanza

Este documento establece el diccionario de datos del proyecto, definiendo el esquema, los tipos de datos y las reglas de calidad (Gobernanza) aplicadas en cada etapa del pipeline.

##  1. Capa Bronze (Datos Crudos / Ingesta)
**Origen:** Tópico de Kafka `ventas_en_vivo` (Productor Python).
**Almacenamiento local:** `data/bronze/ventas_raw.csv`

Esta capa contiene los datos tal como son generados por la fuente, sin ninguna transformación. Incluye intencionalmente datos "sucios" para probar la resiliencia del sistema.

| Campo | Tipo de Dato | Descripción | Notas de Calidad |
|-------|:------------:|-------------|------------------|
| `id_venta` | `int` | Identificador único y secuencial de la transacción. | Generado automáticamente por el productor. |
| `producto` | `str` | Nombre del artículo vendido (ej. "Laptop", "Silla"). | **Puede venir como `None`** (simula error de sistema POS). |
| `categoria` | `str` | Categoría de negocio a la que pertenece el producto. | Valores: Electrónica, Muebles, Accesorios. |
| `precio` | `float` | Monto monetario de la venta individual. | **Puede venir negativo** (ej. `-50.0`, simula error de devolución). |
| `timestamp` | `str` | Fecha y hora exacta en que se generó el evento. | Formato: `YYYY-MM-DD HH:MM:SS`. |

---

## 🥇 2. Capa Gold (Datos Agregados / Consumo)
**Destino:** Base de datos MongoDB, colección `dashboard_ventas`.
**Almacenamiento local:** `data/gold/ventas_por_categoria.csv`

Esta capa contiene los datos limpios, validados y agregados, listos para ser consumidos por herramientas de Business Intelligence (BI) o dashboards.

| Campo | Tipo de Dato | Descripción | Regla de Negocio |
|-------|:------------:|-------------|------------------|
| `_id` | `ObjectId` | Identificador único generado automáticamente por MongoDB. | Clave primaria del documento. |
| `categoria` | `str` | Categoría de negocio agrupada (ej. "Electrónica"). | Clave de agrupación (Group By). |
| `ingreso_total` | `float` | Suma acumulada de todos los precios válidos para la categoría. | Se actualiza incrementalmente usando `$inc`. |
| `total_ventas` | `int` | Conteo acumulado de transacciones válidas para la categoría. | Se actualiza incrementalmente usando `$inc`. |

---

## ️ 3. Reglas de Calidad (Data Quality & Governance)

Las siguientes reglas de gobernanza se aplican en tiempo real durante la fase de **Micro-Batch Processing** (Capa Silver lógica) antes de que los datos lleguen a la Capa Gold. Si un registro viola estas reglas, es descartado y no afecta los reportes de negocio.

### Reglas de Negocio (Business Rules)
1. **Integridad de Entidad:** `producto IS NOT NULL`
   * *Motivo:* No se puede registrar una venta si no se identifica el artículo.
2. **Validez de Monto:** `precio > 0`
   * *Motivo:* Los precios negativos o cero distorsionan los ingresos totales y no representan una venta válida en este contexto.

### Validación de Esquema (Schema Validation)
* Los tipos de datos deben coincidir estrictamente con la definición de la Capa Bronze (ej. `precio` debe ser numérico, `timestamp` debe ser un string con formato de fecha).

---

##  4. Linaje de Datos (Data Lineage)

Para garantizar la trazabilidad, el flujo de los datos sigue estrictamente este linaje:

```text
[Kafka Producer] 
   │ (Evento JSON crudo)
   ▼
[Kafka Topic: ventas_en_vivo] 
   │ (Polling cada 5s)
   ▼
[Micro-Batch Processor] ──► Aplica Reglas de Calidad (Filtra nulos y negativos)
   │ (Agregación: SUM y COUNT)
   ▼
[MongoDB: dashboard_ventas] ──► (Upsert con $inc para acumulación en tiempo real)