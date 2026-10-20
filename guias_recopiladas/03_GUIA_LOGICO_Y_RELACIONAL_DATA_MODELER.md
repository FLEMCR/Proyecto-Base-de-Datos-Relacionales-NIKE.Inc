# GUÍA 3: CÓMO FUNCIONAN EL MODELO LÓGICO Y EL RELACIONAL EN ORACLE DATA MODELER

**Archivo del proyecto:** `nivel_logico/BD NIKE.Inc.dmd` (y su carpeta `BD NIKE.Inc/`)  
**Grupo 5:** Daniel Asmat | Salomón Fernández | Luis Coloma | Pablo Rios

---

## 1. Diferencia entre el Modelo Lógico y el Relacional

En **Oracle SQL Developer Data Modeler** trabajamos con dos pestañas que se conectan entre sí mediante el botón de **Ingeniería (`>>`)**:

1. **Pestaña `Logical` (Cajas Celestes):**
   * Aquí las **3 relaciones `(N,M)`** que teníamos en los rombos del Draw.io (`CONTIENE`, `ALMACENA` y `SUMINISTRA`) ya aparecen convertidas en **3 cajas más** (`DETALLE_VENTA`, `STOCK_ALMACEN` y `SUMINISTRO_LOCAL`), sumando las **9 entidades**.
   * En este nivel definimos qué datos son obligatorios (marcados con asterisco rojo **`*`**) y cuáles pueden quedar vacíos (como `descripcion` en Categoría, `especificaciones` en Producto o `estado_despacho` en Suministro Local).
2. **Pestaña `Relational_1` (Cajas Amarillas):**
   * Se genera automáticamente al presionar el botón **`Engineer to Relational Model (>>)`**.
   * Aquí aparecen las **llaves foráneas (`F` y `PF`)** con el nombre de la tabla padre adelante (por ejemplo `CLIENTE_id_cliente` o `CATEGORIA_id_categoria`) y las secciones inferiores donde se listan los nombres oficiales de las restricciones `PK` y `FK`.

---

## 2. Resumen rápido de las Claves Primarias Compuestas (`PF` + `P`)

Uno de los puntos más importantes de nuestro diseño está en las dos tablas de abajo (`STOCK_ALMACEN` y `SUMINISTRO_LOCAL`):

* **En `STOCK_ALMACEN`:**
  * Su clave primaria está formada por **4 columnas juntas**:
    * `P  * talla`
    * `P  * color`
    * `PF * ALMACEN_id_almacen`
    * `PF * PRODUCTO_id_producto`
  * **¿Qué significa `PF`?** Significa *Primary + Foreign Key* (es llave foránea porque viene de `ALMACEN` o `PRODUCTO`, pero al mismo tiempo forma parte de la llave primaria de `STOCK_ALMACEN`). Gracias a que marcamos la casilla **`Identificar` (`Identifying`)** en las flechas que entran a `STOCK_ALMACEN`, el almacén puede guardar el mismo producto en muchas tallas y colores sin que choquen los registros.
* **En `SUMINISTRO_LOCAL`:**
  * Su clave primaria está formada por **3 columnas juntas**:
    * `P  * fecha_suministro`
    * `PF * LOCAL_id_local`
    * `PF * ALMACEN_id_almacen`
  * Esto permite registrar que un mismo almacén abastezca a una misma tienda física en muchas fechas distintas.

---

## 3. Por qué usamos `DECIMAL (10,2)` y `Suprimir Regla: RESTRICT`

* **`DECIMAL (10,2)` en precios e IGV:**
  En `precio_unitario_base`, `precio_unitario_aplicado`, `igv` y `total` configuramos `Precision = 10` (hasta 10 dígitos en total) y `Scale = 2` (2 decimales para los céntimos en Soles, como `549.90`). No usamos `FLOAT` porque `FLOAT` es un tipo aproximado que redondea mal los centavos.
* **`Suprimir Regla: RESTRICT` (`ON DELETE NO ACTION`):**
  Todas las flechas tienen activada la regla `RESTRICT`. Esto impide que alguien borre por accidente un `CLIENTE`, una `CATEGORIA` o un `PRODUCTO` si ya tiene ventas o stock registrados, protegiendo el historial de la empresa.


---

## 📏 TABLA DE LONGITUDES `VARCHAR` JUSTAS Y NECESARIAS (SIN DESPERDICIO DE ESPACIO)

Siguiendo la indicación del profesor de asignar el tamaño justo y necesario a cada campo de texto:

| Tabla | Columna | Tamaño Ajustado | Justificación Técnica |
| :--- | :--- | :---: | :--- |
| **`CLIENTE`** | `nombre` | **`VARCHAR(80)`** | Suficiente para nombres y dos apellidos en Perú (antes `100`). |
| | `correo_e` | **`VARCHAR(80)`** | Tamaño justo para correos personales o corporativos (antes `100`). |
| | `telefono` | **`VARCHAR(15)`** | Obligatorio (`*`). Guarda los **9 dígitos** de Perú sin dejar espacios vacíos (al ser `VARCHAR` variable) y soporta hasta el tope mundial de **15 dígitos (norma ITU-T E.164)** si compra un extranjero. |
| | `telefono_secundario` | **`VARCHAR(15)`** | **Opcional (sin `*`)**. Permite registrar un segundo número de respaldo sin violar la 1FN. |
| | `direccion` | **`VARCHAR(150)`** | Unificado en `150` igual que `direccion_local` (antes `200`). |
| **`PEDIDO`** | `metodo_pago` | **`VARCHAR(30)`** | Cubre *"Tarjeta de Crédito"*, *"Yape / Plin"*, *"PagoEfectivo"* (antes `40`). |
| | `estado_envio` | **`VARCHAR(20)`** | Unificado en `20` con todos los campos de estado del modelo (antes `30`). |
| **`DETALLE_VENTA`** | `talla_elegida` | **`VARCHAR(10)`** | Unificado en `10` con `STOCK_ALMACEN.talla` para tallas como `"42"`, `"9.5 US"` o `"XXL"` (antes `15`). |
| **`CATEGORIA`** | `nombre` | **`VARCHAR(50)`** | Medida justa para el título de la categoría. |
| | `descripcion` | **`VARCHAR(150)`** | Opcional (sin `*`). Medida justa para una descripción breve. |
| **`PRODUCTO`** | `nombre` | **`VARCHAR(80)`** | Medida justa para el nombre comercial del modelo Nike (antes `120`). |
| | `especificaciones` | **`VARCHAR(150)`** | Opcional (sin `*`). Reemplaza el `255` por defecto por un tope preciso de `150`. |
| | `estado` | **`VARCHAR(20)`** | Unificado en `20` (*"DISPONIBLE"*, *"AGOTADO"*). |
| **`ALMACEN`** | `nombre_almacen` | **`VARCHAR(50)`** | Medida justa (*"CD Lima Norte"*). |
| | `ubicacion` | **`VARCHAR(100)`** | Medida justa para la dirección del Centro de Distribución. |
| **`STOCK_ALMACEN`** | `talla` | **`VARCHAR(10)`** | Unificado en `10` con `talla_elegida` (antes `15`). |
| | `color` | **`VARCHAR(30)`** | Medida justa para combinaciones de color como *"Negro / Blanco"* (antes `40`). |
| **`LOCAL`** | `nombre_local` | **`VARCHAR(50)`** | Medida justa (*"Nike Store Jockey Plaza"*). |
| | `direccion_local` | **`VARCHAR(150)`** | Unificado en `150` con la dirección del cliente. |
| **`SUMINISTRO_LOCAL`** | `estado_despacho` | **`VARCHAR(20)`** | Opcional (sin `*`). Unificado en `20` con los demás estados (antes `30`). |
