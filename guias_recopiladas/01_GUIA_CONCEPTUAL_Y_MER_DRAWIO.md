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
