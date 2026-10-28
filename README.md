# Proyecto Parcial - Base de Datos NIKE Inc. (Grupo 5)

Repositorio del proyecto parcial del curso de **Disenio de Base de Datos Relacionales** (IDAT). El modelo abarca el proceso de ventas, pedidos, control de stock en almacenes y suministro a locales fisicos de Nike a nivel nacional en el Peru.

## Integrantes - Grupo 5

- Daniel Asmat
- Salomon Fernandez
- Luis Coloma
- Pablo Rios

**Docente:** Sergio Fernando Castillo Carrion

## Estructura del repositorio

- **`nivel_conceptual/`**: diagrama M.E.R. (notacion Chen) editable en Draw.io (`.drawio`) y exportado en imagen (`.png`), con las PK subrayadas, los atributos opcionales punteados y las flechas de las 1:N apuntando al lado 1.
- **`normalizacion/`**: Excel `NORMALIZACION_BD_NIKE_GRUPO_5.xlsx` con cuatro hojas: `0FN`, `1FN`, `2FN` y `3FN` (las 10 tablas).
- **`nivel_logico/`**: proyecto de Oracle SQL Developer Data Modeler (`BD NIKE.Inc.dmd` y su carpeta de modelo) y la lamina **`MODELO_LOGICO.png`** en notacion Barker, ordenada igual que el MER.
- **`nivel_fisico/`**: scripts de creacion (`BD_NIKE_INC_SQL_SERVER.sql` y `BD_NIKE_INC_ORACLE.sql`), 10 tablas y 11 claves foraneas, sin vistas ni columnas calculadas.

Las guias de armado estan fuera de esta carpeta, en **`guias/`** (una sola copia de cada una, mas la guia completa).

## Las 8 relaciones del MER

| Relacion | Cardinalidad | Une |
| :--- | :---: | :--- |
| REALIZA | (1,N) | CLIENTE - PEDIDO |
| CONTIENE | (M,N) | PEDIDO - PRODUCTO |
| CLASIFICA | (1,N) | CATEGORIA - PRODUCTO |
| ALMACENA | (M,N) | PRODUCTO - ALMACEN |
| PROVEE | (1,N) | PEDIDO - SUMINISTRO |
| ABASTECE | (1,N) | ALMACEN - SUMINISTRO |
| RECIBE | (1,N) | LOCAL - SUMINISTRO |
| INCLUYE | (M,N) | SUMINISTRO - PRODUCTO |

## Tablas del modelo (3FN)

1. `CLIENTE`
2. `CATEGORIA`
3. `ALMACEN`
4. `LOCAL`
5. `PRODUCTO`
6. `PEDIDO`
7. `SUMINISTRO`
8. `DETALLE_VENTA`
9. `STOCK_ALMACEN`
10. `DETALLE_SUMINISTRO`

**11 claves foraneas** y **3 columnas opcionales** (`telefono_secundario`, `descripcion`, `especificaciones`). Ninguna tabla guarda valores calculados y el modelo no necesita vistas. **`ALMACEN` solo se relaciona con `SUMINISTRO` (ABASTECE) y con `PRODUCTO` (ALMACENA)**.

## Correcciones del docente

Las **11 observaciones** escritas en el Excel de normalizacion estan aplicadas en el MER, en el Excel y en el modelo logico, y documentadas en `guias/06_GUIA_CORRECCIONES_DOCENTE.md`.

## Herramientas utilizadas

- **Draw.io** (diagrama M.E.R. conceptual)
- **Microsoft Excel** (proceso de normalizacion 0FN, 1FN, 2FN y 3FN)
- **Oracle SQL Developer Data Modeler** (modelado logico y relacional)
- **SQL Server Management Studio - SSMS** (implementacion fisica y diagrama de base de datos)
