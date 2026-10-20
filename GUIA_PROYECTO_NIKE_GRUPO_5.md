# GUÍA 1: CÓMO ENTENDER EL PROYECTO NIKE PERÚ Y EL DIAGRAMA M.E.R. (DRAW.IO)

**Proyecto:** Diseño de Base de Datos Relacional para NIKE Inc. (Operación Nacional en Perú)  
**Grupo 5:** Daniel Asmat | Salomón Fernández | Luis Coloma | Pablo Rios

---

## 1. De qué trata nuestro proyecto (Explicado de forma sencilla)

Imagina cómo funciona **NIKE en todo el Perú** (tanto en Lima como en provincias como Arequipa, Trujillo o Cusco). Su operación diaria tiene dos grandes mitades que necesitan conectarse entre sí:

1. **El área de Ventas (*Nike Direct*):**
   * Un cliente entra a comprar zapatillas o ropa deportiva.
   * Para venderle, necesitamos saber **quién es el cliente**, **qué pedido está haciendo** (con qué medio de pago pagó, como Tarjeta o Yape/Plin, cuánto es el IGV del 18% en Perú y en qué estado va su envío) y **qué productos exactos van dentro de su compra** (qué talla eligió, cuántas unidades compró, qué precio se le aplicó y cuánto suma esa línea).
2. **El área de Almacenes y Abastecimiento (*Supply Chain*):**
   * Antes de poder vender o enviar algo, Nike guarda miles de cajas en grandes **Almacenes** (Centros de Distribución en Lima Norte, Villa El Salvador, Arequipa, Trujillo).
   * En esos almacenes los productos se controlan por **lotes de talla y color** (para saber cuántos pares quedan de la talla 42 color negro y cuál es el stock mínimo antes de quedarse sin mercadería).
   * Además, desde esos almacenes salen camiones que **suministran mercadería hacia los Locales** (las tiendas físicas de Nike en centros comerciales como Jockey Plaza, Mall Aventura Arequipa o Mallplaza Trujillo) en determinadas fechas.

---

## 2. Decisiones clave que tomamos para adaptarlo a la realidad de Perú (y evitar errores futuros)

Al diseñar la base de datos pensamos en los casos reales que ocurren en Perú para que el modelo no falle después:

* **Caso 1: El teléfono de 9 dígitos en Perú (`VARCHAR` vs `INTEGER`)**
  * En Perú los celulares tienen **9 dígitos** (empiezan con `9`, por ejemplo `987654321`) y como la base de datos es a nivel nacional no necesitamos guardar el prefijo `+51`.
  * **¿Por qué le pusimos `VARCHAR(20)` y NO `INTEGER`?**
    En bases de datos hay una regla práctica: solo se usa `INTEGER` cuando vas a hacer sumas o multiplicaciones con ese número (como `cantidad` o `stock_actual`). Con un teléfono nunca haces sumas. Además, si un cliente o proveedor registra un teléfono fijo con código de ciudad de Perú (por ejemplo `014456789` en Lima o `054234567` en Arequipa), el tipo `INTEGER` **borra automáticamente el cero de adelante** (`14456789`), malogrando el dato. Con `VARCHAR` el número queda intacto.
* **Caso 2: ¿Qué pasa si un usuario tiene 2 teléfonos?**
  * En la vida real una persona puede tener dos celulares. Sin embargo, en bases de datos (como vimos en la Clase 4 de Normalización), **no se pueden meter dos teléfonos en una misma celda** (`"987654321, 945112233"`) ni tampoco crear columnas `telefono1` y `telefono2` porque eso rompe la Primera Forma Normal (1FN).
  * Si quisiéramos guardar varios teléfonos por cliente, tendríamos que crear una tabla adicional solo para teléfonos. Por eso, como **regla de negocio de Nike Perú**, definimos que cada cuenta de cliente registra únicamente su **número celular titular de 9 dígitos** (el que usa para validar sus pagos por Yape/Plin/Banca y recibir la llamada del courier).
* **Caso 3: No crear un ID distinto para cada par físico de zapatillas**
  * Si el modelo *Nike Air Force 1* viene en 10 tallas y 4 colores, sería un error crear 40 productos repetidos en la tabla `PRODUCTO`.
  * Por eso en `PRODUCTO` solo guardamos el **modelo general del catálogo** una sola vez, y las variantes de **`talla` y `color`** las manejamos en el stock del almacén (`STOCK_ALMACEN`) y la **`talla_elegida`** en el detalle de cada compra (`DETALLE_VENTA`).
* **Caso 4: Por qué diferenciamos `Precio_unitario_base` y `Precio_unitario_aplicado`**
  * En `PRODUCTO` guardamos el `Precio_unitario_base` (lo que cuesta el producto hoy en el catálogo, por ejemplo `S/ 549.90`).
  * Pero en la venta (`CONTIENE` / `DETALLE_VENTA`) guardamos el `Precio_unitario_aplicado`. ¿Por qué? Porque si el próximo mes Nike sube el precio del catálogo a `S/ 599.90` o si ese día hubo un descuento del 20%, las boletas antiguas no deben alterarse: deben conservar el precio exacto al que se vendió ese día.

---

## 3. Cómo se lee el Diagrama M.E.R. en Draw.io

En la carpeta `nivel_conceptual/` están el archivo editable **`Diagrama MER (NIKE) - GRUPO 5.drawio`** y su imagen **`.png`**, hechos con las figuras clásicas por defecto de Draw.io (en blanco y negro):

1. **Rectángulos (Las 6 Entidades principales):**
   * `CLIENTE`, `PEDIDO`, `CATEGORIA`, `PRODUCTO`, `ALMACEN` y `LOCAL`.
2. **Rombos (Las 5 Relaciones que conectan todo):**
   * **`REALIZA (1,N)`:** Un `CLIENTE` realiza muchos `PEDIDO`s.
   * **`CONTIENE (N,M)`:** Un `PEDIDO` contiene varios `PRODUCTO`s. Como esta relación es de muchos a muchos `(N,M)`, tiene sus propios óvalos colgados arriba: `ID_DETALLE`, `Talla_elegida`, `Cantidad`, `Precio_unitario_aplicado` y `Total`.
   * **`CLASIFICA (1,N)`:** Una `CATEGORIA` clasifica a muchos `PRODUCTO`s.
   * **`ALMACENA (N,M)`:** Un `ALMACEN` guarda muchos `PRODUCTO`s. Tiene colgados a la derecha los óvalos del lote: `Talla`, `Color`, `Stock_actual` y `Stock_minimo`.
   * **`SUMINISTRA (N,M)`:** Un `ALMACEN` abastece a varios `LOCAL`es. Tiene colgados a la derecha los óvalos del envío: `Fecha_suministro` y `Estado_despacho`.


---

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


---

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
