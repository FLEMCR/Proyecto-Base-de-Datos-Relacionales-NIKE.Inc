# GUÍA 2: PROCESO DE NORMALIZACIÓN EN EXCEL (DE LA TABLA GENERAL A LAS 9 TABLAS)

**Archivo Excel de trabajo:** `normalizacion/NORMALIZACION_BD_NIKE_GRUPO_5.xlsx`  
**Grupo 5:** Daniel Asmat | Salomón Fernández | Luis Coloma | Pablo Rios

---

## 1. ¿Para qué sirve este archivo Excel y por qué lo pidió el profesor?

Antes de pasar a programas técnicos como Oracle Data Modeler o SQL Server, el profesor pide comprobar en un **Excel** cómo sería si la empresa llevara todo su control en una sola hoja de cálculo gigante (**Tabla General**) y cómo, aplicando las **3 Formas Normales (1FN, 2FN y 3FN)** vistas en las Clases 4 y 6, esa tabla desordenada se va dividiendo paso a paso hasta convertirse exactamente en nuestras **9 tablas limpias**.

Esto sirve como prueba de que **no nos falta ni nos sobra ninguna columna** y evita tener que corregir después el modelo Lógico o el Físico.

---

## 2. Recorrido por las 4 pestañas de nuestro archivo Excel

Si abres el archivo **`NORMALIZACION_BD_NIKE_GRUPO_5.xlsx`**, verás 4 hojas en la parte inferior que muestran la transformación paso a paso con datos reales de Nike en Perú (Lima, Arequipa y Trujillo):

### Pestaña 1: `1_Tabla_General_0FN` (La tabla con problemas, sin normalizar)
Aquí simulamos el reporte en bruto que llevaba la empresa en una sola tabla. Tiene tres problemas graves (resaltados en color salmón suave en el Excel):
1. **Dos teléfonos en una misma celda:** El cliente Carlos Mendoza tiene anotado `"987654321, 945112233"` en una sola casilla.
2. **Varios productos mezclados en una sola fila:** En el pedido `9001`, dentro de la celda de productos dice `"1001 - Nike Air Zoom Pegasus 40, 1002 - Nike Air Force 1 07"`, y en tallas dice `"42, 41"`.
3. **Anomalías de inserción, actualización y borrado:** Como todo está mezclado en una sola hoja, no podríamos registrar un producto nuevo en el almacén si todavía nadie lo ha comprado (anomalía de inserción), y si borráramos el pedido de Lucía Paredes perderíamos también los datos de la tienda de Arequipa (anomalía de eliminación).

---

### Pestaña 2: `2_Primera_Forma_Normal_1FN` — *"Un espacio, un dato"*
**Regla aplicada:** En cada celda debe haber **un único valor atómico** (prohibido separar cosas con comas dentro de una casilla y prohibido crear columnas repetidas como `producto1, producto2` o `telefono1, telefono2`).
* **Qué cambia en el Excel:**
  * El pedido `9001` que tenía 2 zapatillas juntas ahora se divide en **2 filas individuales** (una fila para las *Pegasus 40* talla 42 y otra fila para las *Air Force 1* talla 41).
  * El teléfono del cliente queda como un **único celular titular de 9 dígitos** (`987654321`).
* **Qué problema sigue existiendo en esta pestaña:**
  * Aunque cada celda ya tiene un solo dato, mira cuántas veces se repite `"Carlos Mendoza"`, `"cmendoza@gmail.com"`, `"Av. Javier Prado 1240"` y `"CD Lima Norte"` en cada fila. A eso se le llama **dependencia parcial**, y lo resolvemos en la siguiente pestaña.

---

### Pestaña 3: `3_Segunda_Forma_Normal_2FN` — *"Si se repite, va aparte"*
**Regla aplicada:** Todo dato que se repite porque depende solo de una parte de la clave (por ejemplo, el nombre del cliente depende solo de `id_cliente`, no del producto que compró) se saca a su propia tabla.
* **Qué cambia en el Excel:**
  La tabla gigante se divide en bloques independientes:
  1. **`CLIENTE`:** Guarda una sola vez a Carlos Mendoza (`id_cliente = 1`) y a Lucía Paredes (`id_cliente = 2`).
  2. **`PEDIDO`:** Guarda la cabecera de la compra (`id_pedido`, `fecha`, `metodo_pago`, `igv`, `estado_envio`) y solo se queda con el número `CLIENTE_id_cliente (FK)` para saber quién compró.
  3. **`DETALLE_VENTA`:** Guarda cada línea comprada (`id_detalle`, `talla_elegida`, `cantidad`, `precio_unitario_aplicado`, `total`) conectada a `PEDIDO_id_pedido` y `PRODUCTO_id_producto`.
  4. **`PRODUCTO`:** Guarda una sola vez cada modelo de catálogo.
  5. **`ALMACEN` y `STOCK_ALMACEN`:** Separan los datos fijos del Centro de Distribución (`id_almacen`, `nombre_almacen`, `ubicacion`) del inventario por lotes (`talla`, `color`, `stock_actual`, `stock_minimo`). Aquí se ve claramente por qué la clave primaria de `STOCK_ALMACEN` son las **4 columnas juntas** (`talla`, `color`, `ALMACEN_id_almacen`, `PRODUCTO_id_producto`): porque el stock actual depende tanto de qué almacén es, como de qué producto, qué talla y qué color es.
  6. **`LOCAL` y `SUMINISTRO_LOCAL`:** Separan las tiendas físicas de los despachos recibidos por fecha (`fecha_suministro`, `LOCAL_id_local`, `ALMACEN_id_almacen`).

* **Qué detalle falta pulir al mirar la tabla `PRODUCTO` en esta pestaña 3:**
  * Dentro de `PRODUCTO` todavía están metidas las columnas `id_categoria`, `nombre_categoria` (`"Calzado Urbano"`) y `descripcion_categoria`. Si hubiera 500 zapatillas urbanas, repetiríamos 500 veces la descripción de esa categoría. Eso es una **dependencia transitiva** (el nombre de la categoría no depende del producto, sino de `id_categoria`), y se resuelve en la última pestaña.

---

### Pestaña 4: `4_Tercera_Forma_Normal_3FN` — *"Cada cosa donde pertenece"*
**Regla aplicada:** Ninguna columna normal puede depender de otra columna que no sea la clave primaria de su tabla (cero dependencias transitivas y cero totales redundantes).
* **Qué cambia en el Excel:**
  * Sacamos los datos de la categoría a su propia tabla nueva llamada **`CATEGORIA`** (`id_categoria`, `nombre`, `descripcion`), y dentro de **`PRODUCTO`** dejamos únicamente el enlace **`CATEGORIA_id_categoria (FK)`**.
  * Además, comprobamos por qué **`total` va únicamente en `DETALLE_VENTA`** y no en `PEDIDO`: porque el total de un pedido es simplemente la suma de las filas de su detalle, evitando guardar un cálculo duplicado.
* **Resultado final en la Pestaña 4:**
  Quedan exactamente las **9 tablas definitivas** (`CLIENTE`, `PEDIDO`, `DETALLE_VENTA`, `CATEGORIA`, `PRODUCTO`, `ALMACEN`, `STOCK_ALMACEN`, `LOCAL`, `SUMINISTRO_LOCAL`) con las mismas columnas que están en tu Oracle Data Modeler y en tu SQL Server.
