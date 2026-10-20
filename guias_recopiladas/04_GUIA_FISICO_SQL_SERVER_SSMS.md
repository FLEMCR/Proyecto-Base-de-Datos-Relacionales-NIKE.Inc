# GUÍA 4: MODELO FÍSICO EN SQL SERVER MANAGEMENT STUDIO (SSMS)

**Archivos en `nivel_fisico/`:** `BD_NIKE_INC_SQL_SERVER.sql`, `BD_NIKE_INC_ORACLE.sql` y `DICCIONARIO_DE_DATOS_NIKE_INC.docx`  
**Grupo 5:** Daniel Asmat | Salomón Fernández | Luis Coloma | Pablo Rios

---

## 1. Qué es el Modelo Físico y cómo se obtuvo

El **Modelo Físico** es la construcción real de la base de datos dentro del motor **Microsoft SQL Server** (usando el código SQL generado desde nuestro Modelo Relacional en Data Modeler).

Al ejecutar el archivo **`BD_NIKE_INC_SQL_SERVER.sql`** dentro de **SQL Server Management Studio (SSMS)**:
1. Se crea la base de datos **`BD_NIKE_INC_F`**.
2. Se ejecutan los **9 `CREATE TABLE`** con sus tipos físicos exactos (`INTEGER`, `VARCHAR`, `DECIMAL(10,2)`, `DATETIME`, `DATE`) y sus restricciones `NOT NULL`.
3. Se ejecutan los **17 `ALTER TABLE`**:
   * **9 `PRIMARY KEY CLUSTERED`** (las llaves primarias de las 9 tablas).
   * **8 `FOREIGN KEY ... ON DELETE NO ACTION`** (las 8 líneas conectoras que garantizan la integridad referencial).

---

## 2. Cómo leer el Diagrama Físico en SQL Server (Página 6 de la Entrega)

Cuando abrimos **`Diagramas de base de datos` (`Database Diagrams`)** en SQL Server Management Studio, el diagrama muestra las 9 tablas conectadas:

* **El ícono de la Llave Amarilla (`🔑`) al costado de las columnas:**
  Indica qué columnas forman la **Clave Primaria (`PRIMARY KEY`)** de cada tabla:
  * En `CLIENTE`, `PEDIDO`, `DETALLE_VENTA`, `CATEGORIA`, `PRODUCTO`, `ALMACEN` y `LOCAL` hay **1 llave amarilla** en su respectivo `id_...`.
  * En **`STOCK_ALMACEN`** aparecen **4 llaves amarillas** (`talla`, `color`, `ALMACEN_id_almacen`, `PRODUCTO_id_producto`), confirmando que las 4 columnas juntas forman su clave primaria compuesta.
  * En **`SUMINISTRO_LOCAL`** aparecen **3 llaves amarillas** (`fecha_suministro`, `LOCAL_id_local`, `ALMACEN_id_almacen`), confirmando su clave primaria compuesta de 3 columnas.
* **Las líneas con Llave Amarilla (`🔑`) en una punta y símbolo Infinito (`∞`) en la otra:**
  * La punta con la **llave amarilla (`🔑`)** toca siempre a la **tabla Padre** (lado `1`, donde está la clave primaria original).
  * La punta con el símbolo **infinito (`∞`)** toca siempre a la **tabla Hija** (lado `Muchos` / `N`, donde está la clave foránea).
  * Por ejemplo, entre `CLIENTE` (`🔑`) y `PEDIDO` (`∞`) se lee: *"1 Cliente puede tener infinitos/muchos Pedidos"*.
