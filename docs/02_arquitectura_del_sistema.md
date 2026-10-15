# 🏗️ 02. Arquitectura del Sistema

Este documento describe el flujo de datos, los componentes y las decisiones de diseño técnico del Pipeline End-to-End implementado en este proyecto.

## 🔄 Diagrama de Flujo de Datos (Pipeline Final)

El proyecto culmina con un sistema de streaming en tiempo real que sigue la siguiente arquitectura:

```text
┌─────────────────┐     JSON Events      ┌──────────────────
│   Productor     │ ───────────────────► │   Apache Kafka   │
│  (Python/Kafka) │   cada 2 segundos    │  (ventas_en_vivo)│
└─────────────────┘                      └────────┬─────────┘
                                                  │
                                                  ▼
                                         ┌──────────────────┐
                                         │  Consumidor      │
                                         │  (Micro-Batch)   │
                                         └────────┬─────────
                                                  │
                                                  ▼
                                         ┌──────────────────┐
                                         │    MongoDB       │
                                         │ (dashboard_ventas)│
                                         └──────────────────┘