# Proyecto Parcial - Base de Datos NIKE Inc. (Grupo 5)

Repositorio del proyecto parcial del curso de **Disenio de Base de Datos Relacionales** (IDAT). El modelo abarca el proceso de ventas, pedidos, control de stock en almacenes y suministro a locales fisicos de Nike a nivel nacional en el Peru.

## Integrantes - Grupo 5

- Daniel Asmat
- Salomon Fernandez
- Luis Coloma
- Pablo Rios

## Estructura del Repositorio

- **`nivel_conceptual/`**: Diagrama Entidad-Relacion (notacion Chen) editable en Draw.io (`.drawio`) y exportado en imagen (`.png`).
- **`normalizacion/`**: Archivo Excel (`NORMALIZACION_BD_NIKE_GRUPO_5.xlsx`) con el desarrollo desde la Tabla General sin normalizar (`0FN`) pasando por `1FN`, `2FN` hasta llegar a las 9 tablas en `3FN`.
- **`nivel_logico/`**: Proyecto de Oracle SQL Developer Data Modeler (`BD NIKE.Inc.dmd` y su carpeta de modelo) con el Modelo Logico y el Modelo Relacional.
- **`nivel_fisico/`**: Scripts de creacion de tablas y restricciones (`BD_NIKE_INC_SQL_SERVER.sql` y `BD_NIKE_INC_ORACLE.sql`) junto con el Diccionario de Datos (`.docx`).
- **`ENTREGA DE MODELO LOGICO_RELACIONAL GRUPO-5.pdf`**:Informe consolidado con la propuesta, el diagrama conceptual, los modelos logico/relacional y el diagrama fisico en SQL Server.

## Tablas del Modelo (3FN)

1. `CLIENTE`
2. `PEDIDO`
3. `DETALLE_VENTA`
4. `CATEGORIA`
5. `PRODUCTO`
6. `ALMACEN`
7. `STOCK_ALMACEN`
8. `LOCAL`
9. `SUMINISTRO_LOCAL`

## Herramientas Utilizadas

- **Draw.io** (Diagrama MER Conceptual)
- **Microsoft Excel** (Proceso de Normalizacion 1FN, 2FN y 3FN)
- **Oracle SQL Developer Data Modeler** (Modelado Logico y Relacional)
- **SQL Server Management Studio - SSMS** (Implementacion Fisica y Diagrama de Base de Datos)
