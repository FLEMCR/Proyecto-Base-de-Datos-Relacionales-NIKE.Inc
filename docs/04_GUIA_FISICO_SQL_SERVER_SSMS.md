# GUIA 4: MODELO FISICO EN SQL SERVER MANAGEMENT STUDIO (SSMS)

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

**Archivos en `nivel_fisico/`:** `BD_NIKE_INC_SQL_SERVER.sql` y `BD_NIKE_INC_ORACLE.sql`

---

## 1. Que es el modelo fisico y como se obtuvo

Es la construccion real de la base dentro del motor, usando el codigo generado desde el modelo relacional.

Al ejecutar **`BD_NIKE_INC_SQL_SERVER.sql`** en **SQL Server Management Studio (SSMS)**:

1. Se crea la base **`BD_NIKE_INC_F`** (`CREATE DATABASE`).
2. Se ejecutan **10 `CREATE TABLE`** con tipos fisicos exactos: `INTEGER`, `VARCHAR(n)`, `DECIMAL(10,2)` y `DATE`.
3. Se ejecutan **10 `PRIMARY KEY`** (una por tabla) y **11 `FOREIGN KEY ... ON DELETE NO ACTION`**.
4. **No se crea ninguna vista** y **no hay columnas calculadas**: el total de la linea se calcula en el `SELECT` cuando se necesita.
5. **Ninguna tabla guarda valores calculados:** no hay columna `total` en `DETALLE_VENTA` ni `igv` en `PEDIDO`.

El script de **Oracle** (`BD_NIKE_INC_ORACLE.sql`) hace lo mismo con `VARCHAR2(n)` y `NUMBER(10,2)`, y ademas deja los `DROP TABLE ... CASCADE CONSTRAINTS` al inicio para poder reejecutarlo sin borrar la base.

---

## 2. Como leer el diagrama fisico (lamina 11 de la presentacion)

En **Database Diagrams** de SSMS las 10 tablas aparecen conectadas:

* **Llave amarilla por tabla:** en `CLIENTE`, `PEDIDO`, `CATEGORIA`, `PRODUCTO`, `ALMACEN`, `LOCAL` y `SUMINISTRO` hay **1 llave** en su `id_...`.
* **Llaves compuestas:**
  * `DETALLE_VENTA`: **4 llaves** (`PEDIDO_id_pedido`, `PRODUCTO_id_producto`, `talla_elegida`, `color_elegido`).
  * `STOCK_ALMACEN`: **4 llaves** (`talla`, `color`, `ALMACEN_id_almacen`, `PRODUCTO_id_producto`).
  * `DETALLE_SUMINISTRO`: **4 llaves** (`SUMINISTRO_id_suministro`, `PRODUCTO_id_producto`, `talla`, `color`).
* **Lineas con llave e infinito (`∞`):** la punta con llave toca la tabla **padre** (lado 1) y la punta con `∞` toca la tabla **hija** (lado N). Entre `CLIENTE` (`1`) y `PEDIDO` (`N`) se lee: *"1 cliente puede tener muchos pedidos"*.
* **Columnas marcadas `NULL`:** solo **3** en todo el modelo (ver GUIA 5). Las claves y las foraneas nunca lo permiten.

---

## 3. Diferencia entre los dos scripts

| Tema | SQL Server | Oracle |
| :--- | :--- | :--- |
| Texto | `VARCHAR(n)` | `VARCHAR2(n)` |
| Importes | `DECIMAL(10,2)` | `NUMBER(10,2)` |
| Enteros | `INTEGER` | `NUMBER(10)` / `INTEGER` |
| Fechas | `DATE` | `DATE` |
| Datos calculados | se calculan en el `SELECT` | se calculan en el `SELECT` |
| Lotes | `GO` entre bloques | `/` o `;` |

Los dos scripts crean las **mismas 10 tablas**, las **mismas 12 relaciones** y la **misma vista**.

---

## 4. Pasos para ejecutar (SQL Server)

1. Abrir SSMS y conectarse con autenticacion de Windows.
2. **File > Open > File** y elegir `BD_NIKE_INC_SQL_SERVER.sql`.
3. Verificar que la base que se quiere crear no exista; si existe, ejecutar el `DROP` comentado al inicio.
4. **Execute** (`F5`). El script esta separado por `GO`, asi que crea base, tablas, claves y vista en orden.
5. Actualizar el explorador de objetos: `BD_NIKE_INC_F > Tables` debe mostrar **10 tablas** (no hay vistas).
6. Para ver el diagrama: clic derecho en **Database Diagrams > New Database Diagram**, agregar las 10 tablas y acomodarlas como en `MODELO_FISICO.png`.

---

## 5. Consultas para comprobar que quedo bien

```sql
-- 10 tablas
SELECT COUNT(*) AS tablas FROM sys.tables;

-- 11 claves foraneas
SELECT COUNT(*) AS foraneas FROM sys.foreign_keys;

-- columnas que admiten NULL (debe dar 3)
SELECT t.name AS tabla, c.name AS columna
FROM sys.columns c JOIN sys.tables t ON t.object_id = c.object_id
WHERE c.is_nullable = 1 ORDER BY t.name, c.column_id;

-- el total de la linea se calcula, no se guarda
SELECT TOP 5 d.PEDIDO_id_pedido, d.PRODUCTO_id_producto,
       d.cantidad * d.precio_unitario_aplicado AS total_linea
FROM DETALLE_VENTA d;
```
