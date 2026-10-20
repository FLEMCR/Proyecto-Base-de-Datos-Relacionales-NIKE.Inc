# GUÍA 03: NIVEL FÍSICO EN SQL SERVER MANAGEMENT STUDIO (SSMS) — PROYECTO NIKE INC. (GRUPO 5)

**Curso:** Diseño de Base de Datos Relacionales (IDAT)  
**Integrantes:** Daniel Asmat | Salomón Fernández | Luis Coloma | Pablo Rios

---

## 1. EXPORTACIÓN DEL DDL DESDE ORACLE DATA MODELER

1. En la pestaña **`Relational_1`** de Oracle Data Modeler, presionar el botón **`Generar DDL` (`Generate DDL`)** o `Ctrl + Shift + G`.
2. En **`Sitio de Base de Datos` (`Database Site`)**, elegir **`SQL Server 2012`**.
3. Hacer clic en **`Generar` (`Generate`)** $ightarrow$ **`Aceptar`**.
4. Verificar al final del script el resumen:
   * `CREATE TABLE: 9`
   * `ALTER TABLE: 17` (9 Primary Keys + 8 Foreign Keys)
   * `ERRORS: 0` / `WARNINGS: 0`

---

## 2. EJECUCIÓN Y DIAGRAMA FÍSICO EN SQL SERVER MANAGEMENT STUDIO (SSMS)

1. Abrir **SQL Server Management Studio (SSMS)** y hacer clic en **`Nueva consulta` (`New Query`)**.
2. Si existía una versión anterior de la base de datos en el **`Explorador de objetos`**, hacer clic derecho sobre ella $ightarrow$ **`Eliminar` (`Delete`)** marcando la casilla **`Cerrar conexiones existentes` (`Close existing connections`)**.
3. Al inicio de la nueva consulta, escribir:
   ```sql
   CREATE DATABASE BD_NIKE_INC_F;
   GO
   USE BD_NIKE_INC_F;
   GO
   ```
4. Pegar debajo el script DDL generado por Data Modeler y presionar **`F5` (`Ejecutar`)**.
5. En el **`Explorador de objetos`**, hacer clic derecho sobre **`Bases de datos`** $ightarrow$ **`Actualizar` (`Refresh`)**.
6. Desplegar **`BD_NIKE_INC_F`** $ightarrow$ clic derecho en **`Diagramas de base de datos` (`Database Diagrams`)** $ightarrow$ **`Nuevo diagrama de base de datos`**.
7. Seleccionar las **9 tablas** (`ALMACEN`, `CATEGORIA`, `CLIENTE`, `DETALLE_VENTA`, `LOCAL`, `PEDIDO`, `PRODUCTO`, `STOCK_ALMACEN`, `SUMINISTRO_LOCAL`), hacer clic en **`Agregar`** y luego en **`Cerrar`**.

---

## 3. VERIFICACIÓN DE LLAVES EN EL DIAGRAMA FÍSICO DE SQL SERVER

* **Tablas Maestras y Transaccionales con PK simple (1 llave amarilla):**
  * `CLIENTE` (`id_cliente`)
  * `CATEGORIA` (`id_categoria`)
  * `PRODUCTO` (`id_producto`)
  * `PEDIDO` (`id_pedido`)
  * `DETALLE_VENTA` (`id_detalle`)
  * `ALMACEN` (`id_almacen`)
  * `LOCAL` (`id_local`)
* **Tablas Asociativas con PK Compuesta (múltiples llaves amarillas):**
  * **`STOCK_ALMACEN` (4 llaves amarillas):** `talla`, `color`, `ALMACEN_id_almacen`, `PRODUCTO_id_producto`.
  * **`SUMINISTRO_LOCAL` (3 llaves amarillas):** `fecha_suministro`, `LOCAL_id_local`, `ALMACEN_id_almacen`.
