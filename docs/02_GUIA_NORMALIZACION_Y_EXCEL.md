# GUIA 2: NORMALIZACION Y EXCEL (0FN, 1FN, 2FN y 3FN)

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

**Archivo:** `normalizacion/NORMALIZACION_BD_NIKE_GRUPO_5.xlsx`, con **cuatro hojas**: `0FN`, `1FN`, `2FN` y `3FN`.

---

## 1. Para que sirve el Excel

El profesor pide demostrar en un Excel como seria la empresa si llevara todo en **una sola hoja gigante** (**Tabla General**) y como, aplicando las formas normales, esa hoja se parte paso a paso hasta las **10 tablas** del modelo.

El Excel es la prueba de que las tablas no aparecieron de la nada: cada una se justifica con lo que se elimino en cada fase.

---

## 2. Formato del archivo (igual en las cuatro hojas)

| Elemento | Como se ve |
| :--- | :--- |
| **Titulo de la hoja** | Barra morada `#7030A0` con solo el nombre de la forma normal: `TABLA GENERAL / UNIVERSAL (SIN NORMALIZAR - 0FN)`, `TABLAS 1FN`, `TABLAS 2FN` o `TABLAS 3FN`. |
| **Titulo de tabla** | Banda **verde** `#00B050` con `TABLA : NOMBRE` en blanco y negrita. |
| **Cabecera de columnas** | Fondo **azul oscuro** `#1F4E79` con el nombre de la columna y su marca: `id_cliente (PK)`, `CLIENTE_id_cliente (FK)`, `PEDIDO_id_pedido (PK/FK)`. Texto blanco, negrita, centrado. |
| **Celdas de clave** | Fondo **crema** `#FFF2CC` para los valores de PK y FK (no se pinta la cabecera de crema). |
| **Datos normales** | Fondo blanco con texto normal. |
| **Telefonos y celdas con varios valores (0FN y 1FN)** | Fondo salmon `#FDE9D9` con el numero en **rojo** `#C00000`, para mostrar el atributo multivaluado que se separa en la 1FN. |
| **`NULL`** | Texto gris en cursiva: es la columna opcional que no tiene dato. |

No hay hojas de "correcciones" ni de "estados": **todo eso esta dentro de las tablas y en las guias 5 y 6**. El Excel solo muestra el proceso de normalizacion.

---

## 3. Hoja `0FN`: Tabla General

22 columnas con todo mezclado: `id_pedido`, `fecha`, datos del cliente, `telefonos_cliente` (dos numeros en una celda), `productos_comprados` (varios productos en una celda), `categorias`, `tallas`, `colores`, `cantidades`, `precios_aplicados`, `almacen`, `stock (talla/color/actual/minimo)`, datos del local, `fecha_suministro`, `estado_despacho` y el `igv` digitado a mano.

**Problemas que se ven en la hoja:** celdas con varios valores, datos del cliente repetidos en cada fila, ningun identificador claro de la linea vendida y datos calculados escritos a mano.

---

## 4. Hoja `1FN`: un valor por celda

Se abre **una fila por cada linea vendida** y se separan telefonos, productos, categorias, tallas, colores, cantidades y precios. La hoja queda con una sola tabla de **34 columnas**.

**Correcciones del docente aplicadas aqui:**

* `Yape / Plin` → **`Yape`** en el pedido 9002 (un solo metodo por fila).
* Los colores del stock vuelven a los datos de la tabla general: **`Negro`**, **`Blanco`** y **`Azul Marino`**.
* La PK **no es un `id_detalle` inventado**: la clave de la linea es **`id_pedido` + `id_producto` + `talla_elegida` + `color_elegido`**.

**Problema que aun queda:** dependencias parciales (el nombre del producto depende del producto, no del pedido completo).

---

## 5. Hoja `2FN`: cada atributo depende de toda la clave

1. **`PEDIDO`** — cabecera. Los datos del cliente **se quedan aqui** (sacarlos es trabajo de la 3FN). Tambien guarda **`SUMINISTRO_id_suministro`**.
2. **`DETALLE_VENTA`** — PK compuesta `id_pedido` + `id_producto` + `talla_elegida` + `color_elegido`, con `cantidad` y `precio_unitario_aplicado`.
3. **`SUMINISTRO`** — cabecera del despacho: `id_suministro`, `fecha_suministro`, `estado_despacho`, `ALMACEN_id_almacen` y `LOCAL_id_local`. Los productos y las cantidades que lleva el camion estan en `DETALLE_SUMINISTRO`, y **esos datos ya vienen desde la tabla general (0FN)** en las columnas `productos_suministrados` y `cantidades_suministradas`.
4. **`DETALLE_SUMINISTRO`** — PK `id_suministro` + `id_producto` + `talla` + `color`, mas `cantidad`.

**Problema que aun queda:** dependencias transitivas (el nombre del cliente depende de `id_cliente`, el nombre de la categoria depende de `id_categoria`).

---

## 6. Hoja `3FN`: las 10 tablas

`CLIENTE` sale de `PEDIDO` y `CATEGORIA` sale de `PRODUCTO`. Ya no queda ninguna dependencia transitiva.

| Nro | Tabla | Clave primaria | Claves foraneas |
| :---: | :--- | :--- | :--- |
| 1 | `CLIENTE` | `id_cliente` | - |
| 2 | `CATEGORIA` | `id_categoria` | - |
| 3 | `ALMACEN` | `id_almacen` | - |
| 4 | `LOCAL` | `id_local` | - |
| 5 | `PRODUCTO` | `id_producto` | `CATEGORIA_id_categoria` |
| 6 | `PEDIDO` | `id_pedido` | `CLIENTE_id_cliente`, `SUMINISTRO_id_suministro` |
| 7 | `SUMINISTRO` | `id_suministro` | `ALMACEN_id_almacen`, `LOCAL_id_local` |
| 8 | `DETALLE_VENTA` | `PEDIDO_id_pedido` + `PRODUCTO_id_producto` + `talla_elegida` + `color_elegido` | (las dos primeras son FK) |
| 9 | `STOCK_ALMACEN` | `ALMACEN_id_almacen` + `PRODUCTO_id_producto` + `talla` + `color` | (las dos primeras son FK) |
| 10 | `DETALLE_SUMINISTRO` | `SUMINISTRO_id_suministro` + `PRODUCTO_id_producto` + `talla` + `color` | (las dos primeras son FK) |

**Correcciones del docente aplicadas aqui:**

* **No existe columna `total`** en `DETALLE_VENTA` y **no existe columna `igv`** en `PEDIDO`.
* **`DETALLE_VENTA.color_elegido`** se agrego porque el stock se maneja por talla **y** color.
* **`DETALLE_VENTA` ya no guarda `ALMACEN_id_almacen`**: el almacen solo se relaciona con `SUMINISTRO` y con `PRODUCTO`.
* **`STOCK_ALMACEN` conserva su PK de 4 campos** (el docente confirmo que estaba bien).

---

## 7. Como replicar el Excel a mano

1. **Cuatro hojas** con estos nombres exactos: `0FN`, `1FN`, `2FN` y `3FN`.
2. **Titulo:** combinar `A1:H1`, escribir solo la forma normal (`TABLAS 3FN`) y aplicar relleno `#7030A0` con letra blanca de 18 pt, negrita y cursiva.
3. **Banda de tabla:** combinar la fila donde empieza cada tabla, escribir `TABLA : NOMBRE` y aplicar relleno `#00B050` con letra blanca de 13 pt negrita. Dejar una fila vacia entre tablas.
4. **Cabecera:** escribir el nombre de la columna con su marca (`id_cliente (PK)`, `CLIENTE_id_cliente (FK)`) y pintar la fila de **azul oscuro `#1F4E79`** con letra blanca, negrita y centrada (alto 30). No pintar la cabecera de crema.
5. **Celdas de clave:** solo los valores de PK y FK van con fondo **crema `#FFF2CC`** y texto en negrita.
6. **Bordes:** contorno fino gris `#BFBFBF` en todas las celdas de la tabla (`Inicio > Bordes > Todos los bordes`).
7. **Columnas:** la de la clave entre 22 y 26 de ancho; las de texto largo (`direccion`, `descripcion`) entre 30 y 40.
8. **Inmovilizar** la primera columna en `0FN` y `1FN` (`Vista > Inmovilizar paneles`) para no perder el `id` al desplazarse.
9. **Ocultar cuadricula** (`Vista > quitar Mostrar cuadricula`) para que se vean solo las tablas.

---

## 8. Checklist antes de entregar el Excel

* [ ] Cuatro hojas: `0FN`, `1FN`, `2FN` y `3FN`, sin hojas de correcciones ni de estados.
* [ ] La 0FN muestra las celdas con varios valores y el igv digitado.
* [ ] La 1FN tiene **un valor por celda** y la PK compuesta de 4 columnas.
* [ ] La 2FN mantiene los datos del cliente dentro de `PEDIDO`.
* [ ] La 3FN tiene exactamente **10 tablas**, cada una con su banda `TABLA : ...` y **sin** columnas `total` ni `igv`.
* [ ] Las cabeceras son azul oscuro y las celdas de PK/FK crema.

---

## Fases del Excel, hoja por hoja

| Hoja | Que contiene | De donde sale |
| :--- | :--- | :--- |
| **0FN** | La tabla general: los 3 pedidos con todo mezclado, incluidos los **productos suministrados**, las **cantidades suministradas**, el almacen, el stock, el local y el estado del despacho. | Es la tabla de partida del negocio. |
| **1FN** | La misma informacion con **un solo valor por celda**: una fila por cada linea vendida y por cada linea suministrada. | De la 0FN, separando las listas. |
| **2FN** | **8 tablas**: `PEDIDO`, `DETALLE_VENTA`, `PRODUCTO` (con los datos de su categoria), `SUMINISTRO`, `DETALLE_SUMINISTRO`, `ALMACEN`, `LOCAL` y `STOCK_ALMACEN`. | De la 1FN, separando por dependencia funcional. |
| **3FN** | **10 tablas**: se separan `CLIENTE` (de `PEDIDO`) y `CATEGORIA` (de `PRODUCTO`). | De la 2FN, quitando las dependencias transitivas. |

**Nada se inventa entre fases:** los productos y las cantidades del suministro ya estan en la 0FN, la 1FN los deja atomicos y la 2FN los reparte en `SUMINISTRO` (cabecera) y `DETALLE_SUMINISTRO` (detalle). Todo dato de la 1FN queda en alguna tabla de la 2FN.

### Que cambio en la 3FN

* **`PEDIDO` ya no tiene `estado_envio`.** Ese estado se deduce del `estado_despacho` del suministro que atiende el pedido:

| Estado del pedido (deducido) | `estado_despacho` | Que significa |
| :--- | :--- | :--- |
| PENDIENTE | PROGRAMADO | El despacho aun no sale del centro de distribucion. |
| ENVIADO | EN RUTA | La mercaderia ya salio y va camino al local. |
| ENTREGADO | ENTREGADO | El local recibio la mercaderia y el pedido quedo atendido. |

* **Un pedido se atiende con un solo suministro**: `PEDIDO.SUMINISTRO_id_suministro` es obligatoria y unica, y como cada suministro tiene un almacen y un local, el pedido queda ligado a **un almacen y un local** sin repetir esos datos.
