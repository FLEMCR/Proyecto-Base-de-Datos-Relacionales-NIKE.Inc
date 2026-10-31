# GUIA COMPLETA DEL PROYECTO - BD NIKE Inc. (Grupo 05)


**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

Esta guia reune las **siete** guias del proyecto en un solo documento. Cada una tambien esta
como archivo suelto en esta misma carpeta (`01_...md` a `07_...md`).

| Guia | Tema |
| :--- | :--- |
| 1 | Entender el proyecto y leer el diagrama M.E.R. (Draw.io) |
| 2 | Normalizacion 0FN, 1FN, 2FN y 3FN en Excel |
| 3 | Modelo logico y relacional en Oracle Data Modeler (Barker) |
| 4 | Modelo fisico en SQL Server (SSMS) con IDENTITY, DEFAULT, CHECK y auditoria |
| 5 | Longitudes justas y columnas opcionales |
| 6 | Correcciones del docente aplicadas en las tres revisiones |
| 7 | Diccionario de datos y cierre de la entrega |

---


## 1. De que trata el proyecto

Imagina como funciona **NIKE en el Peru** (Lima, Arequipa, Trujillo). La operacion tiene dos mitades que se conectan entre si:

1. **Ventas (Nike Direct):** un cliente compra zapatillas o ropa. Necesitamos saber **quien es**, **que pedido hizo** (metodo de pago, estado del envio, fecha) y **que productos van dentro** (talla, color, cantidad, precio aplicado).
2. **Almacenes y abastecimiento (Supply Chain):** la mercaderia se guarda en **Almacenes** (centros de distribucion) controlando **stock por talla y color** con un minimo de reposicion, y desde ahi salen **Suministros** que abastecen a los **Locales** (tiendas fisicas).

El disenio queda en **10 tablas**, **11 claves foraneas** y **3 columnas opcionales**.

---

## 2. Decisiones clave (y por que no hicimos otra cosa)

* **Telefono como `VARCHAR(15)`, nunca `INTEGER`.**
  En Peru el celular tiene 9 digitos (`987654321`) y no guardamos el prefijo `+51`. Con `INTEGER` un fijo como `014456789` pierde el cero de adelante. Ademas un telefono no se suma ni se multiplica, y `INTEGER` solo se usa para eso. Los 15 caracteres cubren el tope internacional (E.164) si compra un cliente extranjero.
* **Dos telefonos, pero en dos columnas.** No se puede escribir `"987654321, 945112233"` en una celda porque rompe la 1FN. La solucion del modelo es `telefono` (obligatorio) y `telefono_secundario` (opcional, admite `NULL`). Asi los pedidos 9001 y 9003 conservan sus dos numeros y el 9002 queda con `NULL`.
* **`PRODUCTO` guarda el modelo, no el par fisico.** El Nike Air Force 1 en 10 tallas y 4 colores serian 40 filas repetidas. Por eso `PRODUCTO` tiene una fila por modelo y las variantes viven en `STOCK_ALMACEN` (`talla`, `color`) y en `DETALLE_VENTA` (`talla_elegida`, `color_elegido`).
* **`precio_unitario_base` vs `precio_unitario_aplicado`.** En `PRODUCTO` esta el precio de lista de hoy; en `DETALLE_VENTA` queda el precio del dia de la venta. Si Nike sube el precio, las boletas antiguas no cambian.
* **`ALMACEN`, no `INVENTARIO`.** La entidad es el centro de distribucion; el inventario es el stock que guarda (`STOCK_ALMACEN`).
* **Un solo metodo de pago por celda.** `PEDIDO.metodo_pago` guarda `Tarjeta de Credito`, `Tarjeta de Debito`, `Yape` o `Transferencia`. El pedido 9002 quedo con `Yape` (antes decia `Yape / Plin`, que son dos valores en una celda).
* **Nada calculado se guarda ni se dibuja.** `Total` e `IGV` **no estan en el diagrama**: el total de la linea se obtiene multiplicando `cantidad` por `precio_unitario_aplicado` y el IGV es el 18 % de esa suma, siempre en la consulta. Si se dibujaran, aunque fuera punteados, quedarian como atributos del modelo y despues habria que justificar por que no se migran.

---

## 3. Como se lee el Diagrama M.E.R.

En `nivel_conceptual/` estan el archivo editable **`Diagrama MER (NIKE) - GRUPO 5.drawio`** y su imagen **`.png`**, con las figuras por defecto de Draw.io (negro sobre blanco, sin colores personalizados). El titulo es **"Diagrama M.E.R - NIKE. Inc"** con el subtitulo **"Ventas y Almacenes"**.

**1. Rectangulos = 7 entidades:** `CLIENTE`, `PEDIDO`, `CATEGORIA`, `PRODUCTO`, `ALMACEN`, `LOCAL` y `SUMINISTRO`.

**2. Rombos = 8 relaciones.**

| Relacion | Cardinalidad | Une | Se lee asi |
| :--- | :---: | :--- | :--- |
| **REALIZA** | (1,N) | CLIENTE - PEDIDO | Un CLIENTE realiza muchos PEDIDOS. |
| **CONTIENE** | (M,N) | PEDIDO - PRODUCTO | Un PEDIDO contiene muchos PRODUCTOS, de un ALMACEN y con una talla y un color. |
| **CLASIFICA** | (1,N) | CATEGORIA - PRODUCTO | Una CATEGORIA clasifica muchos PRODUCTOS. |
| **ALMACENA** | (M,N) | PRODUCTO - ALMACEN | Un ALMACEN guarda muchos PRODUCTOS por talla y color. |
| **PROVEE** | (1,N) | PEDIDO - SUMINISTRO | Un SUMINISTRO provee a muchos PEDIDOS. |
| **ABASTECE** | (1,N) | ALMACEN - SUMINISTRO | Un ALMACEN abastece muchos SUMINISTROS. |
| **RECIBE** | (1,N) | LOCAL - SUMINISTRO | Un LOCAL recibe muchos SUMINISTROS. |
| **INCLUYE** | (M,N) | SUMINISTRO - PRODUCTO | Un SUMINISTRO incluye muchos PRODUCTOS con su cantidad, talla y color. |

**3. Elipses = atributos.** Las claves van **subrayadas**: `ID_CLIENTE`, `ID_PEDIDO`, `ID_CATEGORIA`, `ID_PRODUCTO`, `ID_ALMACEN`, `ID_LOCAL` e **`ID_SUMINISTRO`** (atributo nuevo, porque la fecha ya no sirve como clave: podian salir dos despachos el mismo dia).

**En los rombos M:N se subrayan los atributos que forman la clave compuesta de la tabla intermedia.** `Talla_elegida` + `Color_elegido` en **CONTIENE** (junto a `Cantidad` y `Precio_unitario_aplicado`); `Talla` + `Color` en **INCLUYE** (junto a `Cantidad`); `Talla` + `Color` en **ALMACENA** (junto a `Stock_actual` y `Stock_minimo`).

**Ojo con la diferencia:** una relacion M:N **no tiene clave propia** (no se escribe un `ID_DETALLE`, porque eso la convierte en entidad), pero **si tiene clave compuesta**: la forman las claves de las dos entidades mas los atributos que distinguen una ocurrencia de otra (talla y color). Eso es lo que queda subrayado en el rombo y lo que en el relacional aparece como PK de `DETALLE_VENTA`, `DETALLE_SUMINISTRO` y `STOCK_ALMACEN`.

**4. Leyenda y convenciones del dibujo:**

* rectangulo = entidad, rombo = relacion, elipse = atributo;
* atributo **subrayado = PK** en las entidades y **clave compuesta** en los rombos M:N;
* elipse **con borde punteado = atributo que admite `NULL`**: `Telefono_secundario (opcional)`, `Descripcion (opcional)` y `Especificaciones (opcional)`;
* `(1,N)` y `(M,N)` = cardinalidad escrita al lado del rombo;
* la **flecha** de cada relacion 1:N apunta siempre a la entidad del lado **1**;
* los rombos **M:N (CONTIENE, ALMACENA, INCLUYE) no llevan flecha**: se resuelven despues como tablas.

**5. La regla de oro del diagrama: `ALMACEN` solo se une con `SUMINISTRO` y con `PRODUCTO`.**

* Con `SUMINISTRO` a traves de **ABASTECE** (1,N): el almacen abastece al suministro.
* Con `PRODUCTO` a traves de **ALMACENA** (M,N): el almacen guarda el stock por talla y color.
* **No existe ninguna linea entre `ALMACEN` y la venta.** La linea vendida (`CONTIENE`) no guarda el almacen de origen: la mercaderia que se vendio salio del stock del local o del centro de distribucion, y ese movimiento ya esta descrito por `SUMINISTRO`.

**6. Como se lee el diagrama de un vistazo.** El dibujo esta ordenado en dos zonas:

* **Zona de ventas (arriba):** `CLIENTE - REALIZA - PEDIDO - CONTIENE - PRODUCTO - CLASIFICA - CATEGORIA`.
* **Zona de abastecimiento (abajo):** `LOCAL - RECIBE - SUMINISTRO - ABASTECE - ALMACEN`, con `INCLUYE` (los productos que lleva el suministro), `PROVEE` (el suministro que atendio cada pedido) y `ALMACENA` a la derecha.
* Los dos mundos se cruzan con **PROVEE** (de `PEDIDO` hacia `SUMINISTRO`) e **INCLUYE** (de `SUMINISTRO` hacia `PRODUCTO`).
* En el modelo relacional solo cambian tres cosas: los **rombos M:N** pasan a ser tablas (`CONTIENE` -> `DETALLE_VENTA`, `ALMACENA` -> `STOCK_ALMACEN`, `INCLUYE` -> `DETALLE_SUMINISTRO`) y los **rombos 1:N** pasan a ser claves foraneas.

**7. `CONTIENE` es binaria** entre `PEDIDO` y `PRODUCTO`: la linea vendida solo necesita la talla, el color, la cantidad y el precio aplicado.

**8. Por que en `CONTIENE` estan `Talla_elegida` y `Color_elegido` aunque no se subrayen.** El stock se guarda por **talla y color** (`ALMACENA`). Si la linea de venta solo dijera la talla, no se sabria de que fila de stock salio el par. Los dos quedan en el rombo como **datos de la relacion** y en el modelo relacional forman parte de la clave compuesta de `DETALLE_VENTA`. Lo que **no** existe es un `ID_DETALLE`: un atributo asi dentro de un rombo M:N lo convierte en entidad, y eso es lo que observo el docente. Lo que si hay es la **clave compuesta** del rombo (pedido + producto + talla + color), que es la que se subraya.

**9. Nombre cambiado: `DESPACHA` ya no existe.** La relacion entre `ALMACEN` y `SUMINISTRO` se llama **`ABASTECE`** (el almacen abastece al suministro) y la que une `PEDIDO` con `SUMINISTRO` se llama **`PROVEE`** (el suministro provee al pedido). Antes estaba al reves y confundia al leer el diagrama.

---

## 4. Como replicar el diagrama en Draw.io (paso a paso)

1. Abrir <https://app.diagrams.net> (no hace falta cuenta) y crear un diagrama en blanco.
2. **Figuras:** arrastrar 7 rectangulos (`General > Rectangle`) y 8 rombos (`General > Rhombus`). Dejar el estilo por defecto (blanco, borde negro) y escribir el nombre en mayusculas.
3. **Atributos:** arrastrar elipses (`General > Ellipse`) alrededor de cada entidad. Para el atributo opcional: seleccionar la elipse y en el panel derecho poner el **borde en linea punteada**.
4. **PK subrayada:** doble clic en la elipse, seleccionar el texto y `Ctrl+U`.
5. **Unir elipse y entidad:** pasar el mouse por el borde de la elipse y arrastrar el conector hasta la entidad. En la barra de formato elegir **conector ortogonal** (`Waypoints > Orthogonal`) y en `Line > Arrows` dejarlo en **None**.
6. **Relaciones:** unir entidad y rombo con lineas rectas. En las 1:N activar la flecha solo en el extremo que toca la entidad del lado 1 (`Line > Arrows > Classic`). En `CONTIENE`, `ALMACENA` e `INCLUYE` dejar `Arrows = None`.
7. **Cardinalidades:** agregar una caja de texto al lado de cada rombo con `(1,N)` o `(M,N)` (`Text` en la paleta).
8. **Titulo:** caja de texto "Diagrama M.E.R - NIKE. Inc" en 30 pt negrita y debajo "Ventas y Almacenes" en 20 pt.
9. **Exportar:** `File > Export as > PNG`, con **fondo blanco activado** (`Background: white`) y **zoom 300 %** para que el texto se lea al proyectar; reemplazar el `.png` de `nivel_conceptual/`. La imagen que se entrega mide **4800 x 3540 px**, en fondo blanco.
10. **Una diapositiva por modelo:** conceptual, logico, relacional y fisico van cada uno en su propia lamina, con la imagen a tamano completo (nunca dos modelos en la misma diapositiva ni la imagen reducida).

### Misma idea en Lucidchart

* Paleta **Flowchart**: `Process` para entidades, `Decision` para rombos, `Terminator`/`Circle` para atributos.
* Unir con `Line`, y en el panel de la linea elegir **Arrow = None** (o flecha solo en el extremo del lado 1) y **Line type = Elbow** para los atributos.
* La opcion **Format > Text > Underline** deja la PK subrayada.

---

## 5. Longitudes justas y necesarias (resumen)

| Campo | Tipo definitivo | Por que esa medida |
| :--- | :---: | :--- |
| `telefono / telefono_secundario` | **`VARCHAR(15)`** | 9 digitos en Peru; 15 es el tope internacional (E.164) para un cliente extranjero que compra en el pais. |
| `correo_electronico` | **`VARCHAR(80)`** | un correo real mide entre 25 y 45 caracteres; 80 deja margen sin reservar 255. |
| `nombre / nombre de producto` | **`VARCHAR(80)`** | entran nombres completos y nombres comerciales largos. |
| `direccion / direccion_local` | **`VARCHAR(150)`** | una direccion peruana con referencia y distrito llega a 90-120 caracteres. |
| `nombre_almacen / nombre_local / nombre de categoria` | **`VARCHAR(50)`** | son nombres cortos e institucionales. |
| `metodo_pago` | **`VARCHAR(30)`** | 'Tarjeta de Credito', 'Yape' o 'Transferencia' no pasan de 20. |
| `estado_despacho / estado` | **`VARCHAR(20)`** | listas cortas y controladas; el estado del envio no se guarda porque se deduce del despacho. |
| `talla / talla_elegida y color / color_elegido` | **`VARCHAR(10) y VARCHAR(30)`** | talla guarda 42, 41 o M; color guarda Negro, Blanco o Azul Marino. |
| `cantidad, stock_actual, stock_minimo` | **`INTEGER`** | son unidades enteras: no necesitan decimales. |
| `precio_unitario_base / precio_unitario_aplicado` | **`DECIMAL(10,2)`** | 8 enteros y 2 decimales: alcanza para millones de soles y evita el redondeo del FLOAT. |

El detalle completo, columna por columna, esta en la **GUIA 5**.

---

## 6. Correcciones del docente que se ven en el MER

* **`SUMINISTRO` es entidad** con su propio `ID_SUMINISTRO` (antes todo el despacho era una sola relacion con fecha).
* **`INCLUYE`** responde a la observacion de que `SUMINISTRO` solo tenia fecha y estado: ahora el despacho **dice que productos lleva, en que talla y color y cuantas unidades**, cada uno con su `Cantidad`, `Talla` y `Color`. Ese es su objetivo de distribucion.
* **`PROVEE`** une el pedido con el suministro que lo abastecio (de ahi sale `PEDIDO.SUMINISTRO_id_suministro`, **obligatorio**).
* **`ABASTECE`** une el almacen con el suministro que despacha (de ahi sale `SUMINISTRO.ALMACEN_id_almacen`).
* Los **colores** del stock son `Negro`, `Blanco` y `Azul Marino`, los mismos de la tabla general.
* `DETALLE_VENTA` lleva **`Color_elegido`** ademas de `Talla_elegida`.
* **`Total` e `IGV` no estan** en el diagrama: son calculos y se obtienen en la consulta.
* **No existe `ID_DETALLE`** dentro de `CONTIENE`: lo subrayado son los atributos de la clave compuesta (talla y color).
* **La venta no guarda el almacen**: esa informacion vive en `SUMINISTRO` y en `STOCK_ALMACEN`.

El listado completo de las 11 observaciones y donde se aplico cada una esta en la **GUIA 6**.

---

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

---

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

**Carpeta:** `nivel_logico/BD NIKE.Inc/` + archivo **`BD NIKE.Inc.dmd`**  
**Laminas:** `MODELO_LOGICO.png` (Barker, solo entidades y relaciones) y `MODELO_RELACIONAL.png` (las 10 tablas con sus 11 FK)

---

## 1. Que hay en la carpeta del Data Modeler

El proyecto de Data Modeler es una **carpeta**, no un archivo suelto:

```
nivel_logico/
├── BD NIKE.Inc.dmd          <- archivo que se abre desde Data Modeler
└── BD NIKE.Inc/             <- carpeta con los XML del disenio
    ├── logical/             <- entidades, atributos y relaciones del modelo logico
    ├── rel/                 <- tablas, claves foraneas e indices del modelo relacional
    └── ...
```

Para abrirlo: **File > Open** en Oracle SQL Developer Data Modeler y elegir **`BD NIKE.Inc.dmd`**. Si se copia solo el `.dmd` sin la carpeta, el programa abre el proyecto vacio.

---

## 2. La regla del docente: el logico NO muestra las intermedias

> *"En el modelo logico solo se configura; aun no se visualizan las entidades intermediarias."*

Eso significa que en la lamina del **logico** se ven **7 entidades** (`CLIENTE`, `CATEGORIA`, `ALMACEN`, `LOCAL`, `PRODUCTO`, `PEDIDO`, `SUMINISTRO`) y sus relaciones, **nada mas**. Las tres relaciones de muchos a muchos del MER quedan **configuradas** en el proyecto, pero se materializan recien cuando se genera el **relacional**:

| En el MER | Se configura en el logico | Aparece como tabla en el RELACIONAL |
| :--- | :--- | :--- |
| REALIZA (1,N) | relacion `CLIENTE` → `PEDIDO` | FK `CLIENTE_id_cliente` en `PEDIDO` |
| CLASIFICA (1,N) | relacion `CATEGORIA` → `PRODUCTO` | FK `CATEGORIA_id_categoria` en `PRODUCTO` |
| PROVEE (1,N) | relacion `SUMINISTRO` → `PEDIDO` | FK `SUMINISTRO_id_suministro` en `PEDIDO`, **obligatoria**: una sola columna, asi cada pedido se atiende con un solo suministro (un almacen y un local) |
| ABASTECE (1,N) | relacion `ALMACEN` → `SUMINISTRO` | FK `ALMACEN_id_almacen` en `SUMINISTRO` |
| RECIBE (1,N) | relacion `LOCAL` → `SUMINISTRO` | FK `LOCAL_id_local` en `SUMINISTRO` |
| CONTIENE (M,N) | relacion M:N `PEDIDO` ↔ `PRODUCTO` | tabla **`DETALLE_VENTA`** (2 FK) |
| ALMACENA (M,N) | relacion M:N `PRODUCTO` ↔ `ALMACEN` | tabla **`STOCK_ALMACEN`** (2 FK) |
| INCLUYE (M,N) | relacion M:N `SUMINISTRO` ↔ `PRODUCTO` | tabla **`DETALLE_SUMINISTRO`** (2 FK) |

Resultado: **7 entidades y 8 relaciones en el logico → 10 tablas y 11 claves foraneas en el relacional**.

### Por que el rombo si lleva atributos subrayados

* Una relacion M:N **no tiene clave propia**: no se escribe un `ID_DETALLE`, porque al darle un identificador el rombo se vuelve una entidad (eso fue justo lo que observo el docente en el MER).
* Pero **si tiene clave compuesta**: la forman las claves de las dos entidades (`PEDIDO` + `PRODUCTO`) mas los atributos que distinguen una ocurrencia de otra (`talla_elegida` + `color_elegido`).
* Esos atributos son los que van **subrayados** dentro del rombo, y son los que en el relacional aparecen como **PK de `DETALLE_VENTA`**. Lo mismo pasa con `talla` + `color` en `INCLUYE` y en `ALMACENA`.

**`ALMACEN` solo se relaciona con `SUMINISTRO` (ABASTECE) y con `PRODUCTO` (ALMACENA)**: no existe ninguna clave de almacen en la venta.

---

## 3. Como se lee el modelo logico en Barker (`MODELO_LOGICO.png`)

La lamina se lee en el mismo orden que el MER:

| Relacion | Cardinalidad | Lectura |
| :--- | :---: | :--- |
| `CLIENTE` → `PEDIDO` | 1 : N | Un cliente realiza uno o muchos pedidos; cada pedido es de un solo cliente. |
| `CATEGORIA` → `PRODUCTO` | 1 : N | Una categoria clasifica uno o muchos productos. |
| `SUMINISTRO` → `PEDIDO` | 1 : N | Un suministro provee uno o muchos pedidos. |
| `ALMACEN` → `SUMINISTRO` | 1 : N | Un almacen abastece uno o muchos suministros. |
| `LOCAL` → `SUMINISTRO` | 1 : N | Un local recibe uno o muchos suministros. |
| `PEDIDO` ↔ `PRODUCTO` (**CONTIENE**) | M : N | Un pedido contiene muchos productos y un producto esta en muchos pedidos; el rombo lleva `talla_elegida`, `color_elegido`, `cantidad` y `precio_unitario_aplicado`. |
| `SUMINISTRO` ↔ `PRODUCTO` (**INCLUYE**) | M : N | Un suministro incluye muchos productos; el rombo lleva `talla`, `color` y `cantidad`. |
| `PRODUCTO` ↔ `ALMACEN` (**ALMACENA**) | M : N | Un almacen guarda muchos productos; el rombo lleva `talla`, `color`, `stock_actual` y `stock_minimo`. |

Convenciones del dibujo:

* **`1` con raya:** el lado "uno y solo uno" (la entidad maestra).
* **`N` con pata de gallo:** el lado "uno o muchos" (la entidad que recibe la clave foranea).
* **`M` y `N`:** las relaciones de muchos a muchos, con el rombo y sus atributos.
* **Cada relacion lleva su verbo** (`REALIZA`, `CLASIFICA`, `PROVEE`, `ABASTECE`, `RECIBE`, `CONTIENE`, `INCLUYE`, `ALMACENA`) escrito sobre la linea o dentro del rombo, mas la cardinalidad en los extremos. El PNG original mide **4120 x 2260 px**: insertalo a tamano completo, una lamina por modelo.
* **Sin marcas de "origen opcional":** todas las relaciones son obligatorias, como pidio el docente.
* **Sin vistas y sin columnas calculadas:** no hay `total` ni `igv` en ninguna entidad.

---

## 4. Las 11 claves foraneas (modelo relacional)

| Restriccion | Tabla hija (N) | Columna | Tabla padre (1) | Columna PK |
| :--- | :--- | :--- | :--- | :--- |
| PEDIDO_CLIENTE_FK | PEDIDO | CLIENTE_id_cliente | CLIENTE | id_cliente |
| PEDIDO_SUMINISTRO_FK | PEDIDO | SUMINISTRO_id_suministro | SUMINISTRO | id_suministro |
| DETALLE_VENTA_PEDIDO_FK | DETALLE_VENTA | PEDIDO_id_pedido | PEDIDO | id_pedido |
| DETALLE_VENTA_PRODUCTO_FK | DETALLE_VENTA | PRODUCTO_id_producto | PRODUCTO | id_producto |
| PRODUCTO_CATEGORIA_FK | PRODUCTO | CATEGORIA_id_categoria | CATEGORIA | id_categoria |
| STOCK_ALMACEN_ALMACEN_FK | STOCK_ALMACEN | ALMACEN_id_almacen | ALMACEN | id_almacen |
| STOCK_ALMACEN_PRODUCTO_FK | STOCK_ALMACEN | PRODUCTO_id_producto | PRODUCTO | id_producto |
| SUMINISTRO_ALMACEN_FK | SUMINISTRO | ALMACEN_id_almacen | ALMACEN | id_almacen |
| SUMINISTRO_LOCAL_FK | SUMINISTRO | LOCAL_id_local | LOCAL | id_local |
| DETALLE_SUMINISTRO_SUMINISTRO_FK | DETALLE_SUMINISTRO | SUMINISTRO_id_suministro | SUMINISTRO | id_suministro |
| DETALLE_SUMINISTRO_PRODUCTO_FK | DETALLE_SUMINISTRO | PRODUCTO_id_producto | PRODUCTO | id_producto |

Todas son **1:N** y todas son **obligatorias**. En `MODELO_RELACIONAL.png` cada linea sale del lado 1 (raya) y llega con pata de gallo al lado N, con el verbo y la cardinalidad escritos en la linea.

---

## 5. Como se marca cada cosa en Data Modeler

* **`P` (PK):** se activa con el boton de llave en la columna o marcando el atributo como identificador de la entidad.
* **`F` (FK):** no se escribe a mano; se genera al dibujar la **relacion 1:N**. La columna aparece con el nombre `TABLA_id`.
* **`PFK`:** columna que forma parte de la clave compuesta **y** ademas es clave foranea (`DETALLE_VENTA`, `STOCK_ALMACEN`, `DETALLE_SUMINISTRO`).
* **`*` obligatorio:** la casilla **Optional** del atributo queda desmarcada (equivale a `NOT NULL`).
* **`o` opcional:** la casilla **Optional** queda marcada solo en `telefono_secundario`, `descripcion` y `especificaciones`.
* **Origen opcional:** NO se marca en ninguna relacion.
* **Tipos en la vista relacional:** `VARCHAR2(n)` para texto y `NUMBER(10,2)` para importes, con **Size** y **Precision/Scale** definidos a mano (nunca 255 por defecto).
* **Nada calculado se almacena:** `DETALLE_VENTA` no tiene `total` y `PEDIDO` no tiene `igv`. Tampoco hay vista: el total de la linea se calcula multiplicando `cantidad` por `precio_unitario_aplicado` cuando se consulta.

---

## 6. Columnas que admiten `NULL` (3 en total)

| Tabla | Columna | Por que puede quedar vacia |
| :--- | :--- | :--- |
| `CLIENTE` | `telefono_secundario` | No todos los clientes dejan un segundo numero de contacto. |
| `CATEGORIA` | `descripcion` | Una categoria puede crearse solo con su nombre. |
| `PRODUCTO` | `especificaciones` | No todos los modelos tienen la ficha tecnica cargada. |

Todo lo demas es `NOT NULL`; las claves y las foraneas **nunca** admiten `NULL`.

---

## 7. Longitudes que se ven en el modelo relacional

| Campo | Tipo definitivo | Por que esa medida |
| :--- | :---: | :--- |
| `telefono / telefono_secundario` | **`VARCHAR(15)`** | 9 digitos en Peru; 15 es el tope internacional (E.164) para un cliente extranjero que compra en el pais. |
| `correo_electronico` | **`VARCHAR(80)`** | un correo real mide entre 25 y 45 caracteres; 80 deja margen sin reservar 255. |
| `nombre / nombre de producto` | **`VARCHAR(80)`** | entran nombres completos y nombres comerciales largos. |
| `direccion / direccion_local / ubicacion` | **`VARCHAR(120)`** | una direccion peruana con referencia y distrito llega a 90-120 caracteres. |
| `nombre_almacen / nombre_local / nombre de categoria` | **`VARCHAR(50)`** | son nombres cortos e institucionales. |
| `metodo_pago` | **`VARCHAR(30)`** | 'Tarjeta de Credito', 'Yape' o 'Transferencia' no pasan de 20. |
| `estado_despacho / estado` | **`VARCHAR(20)`** | listas cortas y controladas; el estado del envio no se guarda porque se deduce del despacho. |
| `talla / talla_elegida y color / color_elegido` | **`VARCHAR(10)` y `VARCHAR(30)`** | talla guarda 42, 41 o M; color guarda Negro, Blanco o Azul Marino. |
| `cantidad, stock_actual, stock_minimo` | **`INTEGER`** | son unidades enteras: no necesitan decimales. |
| `precio_unitario_base / precio_unitario_aplicado` | **`DECIMAL(10,2)`** | 8 enteros y 2 decimales: alcanza para millones de soles y evita el redondeo del FLOAT. |

---

## 8. Que revisar antes de exportar

1. Que el **logico** muestre solo las 7 entidades y sus 8 relaciones, sin tablas intermedias.
2. Que cada relacion del logico tenga **verbo + `1` + `N`** y que el PNG se inserte a tamano completo.
3. Que al generar el **relacional** aparezcan las **10 tablas** y las **11 FK**, con PK compuesta en `DETALLE_VENTA`, `STOCK_ALMACEN` y `DETALLE_SUMINISTRO`.
4. Que `PEDIDO` **no** tenga columna `igv` y que `DETALLE_VENTA` **no** tenga columna `total` ni ninguna columna de almacen.
5. Que ningun `VARCHAR2` quede en `255` y ningun importe quede en `NUMBER` sin precision.
6. Guardar el proyecto y verificar que la carpeta `BD NIKE.Inc/` tenga los XML (si falta, el `.dmd` viaja incompleto).

---

## 9. Del logico al relacional y al fisico (lo haces tu, en este orden)

1. **Logico** (esta guia): 7 entidades con atributos, PK marcada y 8 relaciones **configuradas** (las M:N como rombo con sus atributos).
2. **Relacional:** boton **Engineer to Relational Model** (`>>`). Aparecen las 10 tablas con tipos, `P` / `F` / `PF` y las restricciones `TABLA_PK` y `TABLA_PADRE_FK`; ahi si se ven las intermedias.
3. **Fisico:** genera el DDL desde el relacional y ejecutalo en SSMS. Antes de exportar, agrega lo que la capa fisica necesita y que el docente califico: **IDENTITY**, **DEFAULT**, **CHECK** y los **4 campos de auditoria** (ver GUIA 4).
4. **Una lamina por modelo:** conceptual, logico, relacional y fisico van en diapositivas separadas, con la imagen a tamano completo.

---

## 10. Cardinalidad: donde se pone el `1` y donde el pie de gallo

La regla que resuelve el 90% de las dudas en Data Modeler:

> **Donde va la FK (la tabla hija) se dibuja el pie de gallo (N). Donde va la PK referenciada (la tabla padre) se dibuja la barra (1).**

| Relacion | Padre (barra `1`) | Hijo (pie de gallo `N`) | FK que la sostiene |
| :--- | :--- | :--- | :--- |
| `REALIZA` | `CLIENTE` | `PEDIDO` | `PEDIDO.CLIENTE_id_cliente` |
| `CLASIFICA` | `CATEGORIA` | `PRODUCTO` | `PRODUCTO.CATEGORIA_id_categoria` |
| `PROVEE` | `SUMINISTRO` | `PEDIDO` | `PEDIDO.SUMINISTRO_id_suministro` |
| `ABASTECE` | `ALMACEN` | `SUMINISTRO` | `SUMINISTRO.ALMACEN_id_almacen` |
| `RECIBE` | `LOCAL` | `SUMINISTRO` | `SUMINISTRO.LOCAL_id_local` |
| `CONTIENE` | `PEDIDO` | `PRODUCTO` | (M:N, se materializa en `DETALLE_VENTA`) |
| `ALMACENA` | `PRODUCTO` | `ALMACEN` | (M:N, se materializa en `STOCK_ALMACEN`) |
| `INCLUYE` | `SUMINISTRO` | `PRODUCTO` | (M:N, se materializa en `DETALLE_SUMINISTRO`) |

### 10.1 El error tipico: el pie de gallo al reves en `PROVEE`

Si en el logico el pie de gallo mira a `SUMINISTRO`, el modelo esta diciendo *"muchos suministros atienden un pedido"*, que no es el negocio. Debe quedar:

* `SUMINISTRO` con la barra (`1`)
* `PEDIDO` con el pie de gallo (`N`)
* lectura: **un suministro atiende uno o muchos pedidos; cada pedido se atiende con un solo suministro.**

Esa ultima frase se cumple con una sola columna obligatoria (`PEDIDO.SUMINISTRO_id_suministro NOT NULL`). **No** se escribe `(1,1)` junto al rombo ni se agrega un `UNIQUE`: el estilo del curso usa solo `1:N` y `M:N`, y un `UNIQUE` sobre esa columna convertiria la relacion en `1:1`, que no es lo que el docente pidio.

### 10.2 Donde se cambia la cardinalidad (y donde no)

| Cosa | Donde se edita | Como |
| :--- | :--- | :--- |
| Cardinalidad de la relacion | **Modelo logico**, doble clic en la linea de la relacion (`General > Cardinalidad`) | origen y destino: `1` o `N` |
| Verbo de la relacion | **Modelo logico**, relacion (`General > Nombre`) | `REALIZA`, `PROVEE`, ... |
| Nombre de la FK | **Modelo relacional**, propiedades de la columna FK | se deja `TABLA_PADRE_FK` |
| `NOT NULL` de la FK | **Modelo relacional**, columna FK (`Obligatoria`) | activado = obligatoria |

En el dialogo de **propiedades de la clave foranea** no se configura la cardinalidad: esa informacion la hereda del modelo logico y se deduce de donde se coloco la columna. Cambiarla ahi no es posible, y renombrar la FK para que diga `PROVEE` no aporta nada: el nombre de la relacion (`PROVEE`) y el de la restriccion (`PEDIDO_SUMINISTRO_FK`) son dos objetos distintos y no tienen que coincidir.

### 10.3 Del logico al relacional sin romper lo que ya funciona

* **Haz una copia del `.dmd`** antes de tocar el boton **Engineer to Relational Model** (`>>`).
* Reingenierizar sobre un relacional que ya existe puede **duplicar** las tablas de las relaciones `M:N` (`DETALLE_VENTA`, `STOCK_ALMACEN`, `DETALLE_SUMINISTRO`).
* Si solo hay que borrar una columna (`estado_envio`), **borrala a mano** en el relacional; no hace falta reingenierizar todo.
* Lo que se genera en el relacional es el **esqueleto** del fisico: despues se agregan `IDENTITY`, `DEFAULT`, `CHECK` y auditoria (ver GUIA 4).

---

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

**Archivos en `nivel_fisico/`:** `MF_NIKE_INC_CORREGIDO.sql` (el que se ejecuta), `BD_NIKE_INC_SQL_SERVER.sql`, `BD_NIKE_INC_ORACLE.sql` y la lamina `MODELO_FISICO.png`

---

## 1. Que es el modelo fisico y como se obtuvo

Es la construccion real de la base dentro del motor, usando el codigo generado desde el modelo relacional.

Al ejecutar **`BD_NIKE_INC_SQL_SERVER.sql`** en **SQL Server Management Studio (SSMS)**:

1. Se crea la base **`NIKE_INC_BD`** (`CREATE DATABASE`).
2. Se ejecutan **10 `CREATE TABLE`** con tipos fisicos exactos: `INT`, `VARCHAR(n)`, `DECIMAL(10,2)` y `DATE`.
3. Se ejecutan **10 `PRIMARY KEY`** (una por tabla) y **11 `FOREIGN KEY ... ON DELETE NO ACTION`**.
4. **No se crea ninguna vista** y **no hay columnas calculadas**: el total de la linea se calcula en el `SELECT` cuando se necesita.
5. **Ninguna tabla guarda valores calculados:** no hay columna `total` en `DETALLE_VENTA` ni `igv` en `PEDIDO`.

El script de **Oracle** (`BD_NIKE_INC_ORACLE.sql`) hace lo mismo con `VARCHAR2(n)`, `NUMBER(10,2)` y `GENERATED BY DEFAULT ON NULL AS IDENTITY`, y deja los `DROP TABLE ... CASCADE CONSTRAINTS` al inicio para poder reejecutarlo.

---

## 2. Lo que el docente pidio y donde esta resuelto

La revision anterior decia: *"No se ven IDENTITY, DEFAULT, CHECK ni campos de auditoria."* En el script actual los cuatro ya estan:

| Lo que pidio | Donde esta | Cuantos |
| :--- | :--- | :--- |
| **IDENTITY** | `id_...` de `CLIENTE`, `CATEGORIA`, `ALMACEN`, `LOCAL`, `PRODUCTO`, `PEDIDO` y `SUMINISTRO`: `INT IDENTITY(1,1)` | 7 columnas |
| **DEFAULT** | estados, fechas, cantidad y stock que nacen con valor | 9 de negocio |
| **CHECK** | cantidades, precios, los catalogos de estados, correo y telefono | 10 restricciones |
| **Auditoria** | `usuario_creacion`, `fecha_creacion`, `usuario_modificacion`, `fecha_modificacion` en las 10 tablas | 40 columnas |

### 2.1 IDENTITY

Solo en las **claves primarias simples**. Las tres tablas con clave compuesta (`DETALLE_VENTA`, `STOCK_ALMACEN`, `DETALLE_SUMINISTRO`) **no llevan IDENTITY**: sus columnas son claves foraneas, talla y color, y la numeracion no tendria sentido.

```sql
CREATE TABLE CLIENTE (
    id_cliente          INT IDENTITY(1,1) NOT NULL,
    ...
    CONSTRAINT CLIENTE_PK PRIMARY KEY (id_cliente)
);
```

En Oracle el equivalente es `NUMBER(10) GENERATED BY DEFAULT ON NULL AS IDENTITY`.

### 2.2 DEFAULT (9 de negocio + 20 de auditoria)

| Tabla | Columna | Valor por omision | Motivo |
| :--- | :--- | :--- | :--- |
| PEDIDO | fecha | `CAST(GETDATE() AS DATE)` | si no se envia, queda el dia de la venta |
| PEDIDO | metodo_pago | `'Tarjeta de Credito'` | es el medio mas usado en la tienda online |
| SUMINISTRO | fecha_suministro | `CAST(GETDATE() AS DATE)` | queda el dia del despacho |
| SUMINISTRO | estado_despacho | `'PROGRAMADO'` | todo despacho nuevo nace programado |
| PRODUCTO | estado | `'DISPONIBLE'` | todo modelo nuevo entra disponible |
| DETALLE_VENTA | cantidad | `1` | una linea sin cantidad vale una unidad |
| DETALLE_SUMINISTRO | cantidad | `1` | una linea sin cantidad vale una unidad |
| STOCK_ALMACEN | stock_actual | `0` | arranca en cero |
| STOCK_ALMACEN | stock_minimo | `0` | arranca en cero |

### 2.3 CHECK (10)

| Restriccion | Tabla | Condicion |
| :--- | :--- | :--- |
| CK_DETALLE_VENTA_CANTIDAD | DETALLE_VENTA | `cantidad > 0` |
| CK_DETALLE_VENTA_PRECIO | DETALLE_VENTA | `precio_unitario_aplicado > 0` |
| CK_DETALLE_SUMINISTRO_CANTIDAD | DETALLE_SUMINISTRO | `cantidad > 0` |
| CK_PRODUCTO_PRECIO | PRODUCTO | `precio_unitario_base > 0` |
| CK_PRODUCTO_ESTADO | PRODUCTO | `estado IN ('DISPONIBLE','AGOTADO','DESCONTINUADO')` |
| CK_STOCK_ALMACEN_ACTUAL | STOCK_ALMACEN | `stock_actual >= 0` |
| CK_STOCK_ALMACEN_MINIMO | STOCK_ALMACEN | `stock_minimo >= 0` |
| CK_SUMINISTRO_ESTADO | SUMINISTRO | `estado_despacho IN ('PROGRAMADO','EN RUTA','ENTREGADO')` |
| CK_CLIENTE_CORREO | CLIENTE | el correo tiene el formato `texto@texto.dominio` |
| CK_CLIENTE_TELEFONO | CLIENTE | solo digitos, entre 6 y 15 caracteres |

El unico catalogo de estado de proceso es `estado_despacho` (PROGRAMADO, EN RUTA, ENTREGADO), que describe el **traslado del centro de distribucion al local**. El estado del pedido **no se guarda**: se deduce de ese catalogo (PENDIENTE = PROGRAMADO, ENVIADO = EN RUTA, ENTREGADO = ENTREGADO). `estado` de `PRODUCTO` es otra cosa: si el modelo esta disponible para la venta.

### 2.4 Campos de auditoria (4 columnas x 10 tablas)

```sql
usuario_creacion        VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
fecha_creacion          DATETIME    DEFAULT GETDATE()   NOT NULL,
usuario_modificacion    VARCHAR(30),
fecha_modificacion      DATETIME,
```

* `usuario_creacion` y `fecha_creacion` se llenan **solas** en el `INSERT`: no hay que escribirlas.
* `usuario_modificacion` y `fecha_modificacion` nacen en **NULL** y las llena el proceso o *trigger* que actualiza la fila; asi se distingue una fila que nunca se toco.
* En Oracle los equivalentes son `USER` y `SYSTIMESTAMP`.

---

## 3. Como leer la lamina del modelo fisico (`MODELO_FISICO.png`)

En **Database Diagrams** de SSMS las 10 tablas aparecen conectadas:

* **Llave amarilla por tabla:** en `CLIENTE`, `PEDIDO`, `CATEGORIA`, `PRODUCTO`, `ALMACEN`, `LOCAL` y `SUMINISTRO` hay **1 llave** en su `id_...`.
* **Llaves compuestas:**
  * `DETALLE_VENTA`: **4 llaves** (`PEDIDO_id_pedido`, `PRODUCTO_id_producto`, `talla_elegida`, `color_elegido`).
  * `STOCK_ALMACEN`: **4 llaves** (`talla`, `color`, `ALMACEN_id_almacen`, `PRODUCTO_id_producto`).
  * `DETALLE_SUMINISTRO`: **4 llaves** (`SUMINISTRO_id_suministro`, `PRODUCTO_id_producto`, `talla`, `color`).
* **Lineas con llave e infinito (`∞`):** la punta con llave toca la tabla **padre** (lado 1) y la punta con `∞` toca la tabla **hija** (lado N).
* **Columnas marcadas `NULL`:** solo **3** en todo el modelo (ver GUIA 5). Las claves y las foraneas nunca lo permiten.
* La fila de auditoria aparece **separada por una linea** al final de cada tabla, para que se note que no es parte del negocio.

---

## 4. Diferencia entre los dos scripts

| Tema | SQL Server | Oracle |
| :--- | :--- | :--- |
| Texto | `VARCHAR(n)` | `VARCHAR2(n)` |
| Importes | `DECIMAL(10,2)` | `NUMBER(10,2)` |
| Enteros | `INT` | `NUMBER(10)` |
| Fechas | `DATE` | `DATE` |
| Autonumerico | `INT IDENTITY(1,1)` | `GENERATED BY DEFAULT ON NULL AS IDENTITY` |
| Fecha del dia | `CAST(GETDATE() AS DATE)` | `SYSDATE` |
| Usuario de la sesion | `SYSTEM_USER` | `USER` |
| Validacion de telefono y correo | `LIKE` / `LEN` | `REGEXP_LIKE` |
| Lotes | `GO` entre bloques | `/` o `;` |

Los dos scripts crean las **mismas 10 tablas**, las **mismas 11 relaciones**, los **mismos 9 DEFAULT** de negocio (mas los de auditoria), los **mismos 10 CHECK** y las **mismas 40 columnas de auditoria**. Ninguno crea vistas.

---

## 5. Pasos para ejecutar (SQL Server)

Se puede ejecutar cualquiera de los dos scripts de SQL Server; hacen lo mismo:

| Script | Para que sirve |
| :--- | :--- |
| **`MF_NIKE_INC_CORREGIDO.sql`** | Es el DDL que genero Data Modeler, **corregido**: mismos nombres y tipos del grupo, con el `CREATE DATABASE` arreglado y con IDENTITY, DEFAULT, CHECK y auditoria agregados. |
| `BD_NIKE_INC_SQL_SERVER.sql` | Version equivalente escrita por el grupo, con los mismos 10 objetos y las mismas restricciones. |

1. Abrir SSMS y conectarse con autenticacion de Windows.
2. **File > Open > File** y elegir `MF_NIKE_INC_CORREGIDO.sql`.
3. El script empieza con `IF DB_ID('NIKE_INC_BD') IS NOT NULL DROP DATABASE NIKE_INC_BD;`, asi que se puede reejecutar sin borrar nada a mano.
4. **Execute** (`F5`). Esta separado por `GO`: crea la base, las 10 tablas con sus PK y CHECK, y al final las 11 FK.
5. Al final del script vienen las **consultas de comprobacion**: ejecutalas y compara con los numeros esperados de la seccion 6.
6. Actualizar el explorador de objetos: `NIKE_INC_BD > Tables` debe mostrar **10 tablas** (no hay vistas).
7. **Solo cuando la base ya existe y esta completa**, crear el diagrama: clic derecho en **Database Diagrams > New Database Diagram**, agregar las 10 tablas, acomodarlas como en `MODELO_FISICO.png` y usar **Copy Diagram to Clipboard** para pegarlo en Paint y guardar el PNG.

### 5.1 El error mas comun: `CREATE NIKE_INC_BD` no es SQL

```sql
CREATE NIKE_INC_BD      -- error 102: Incorrect syntax near 'NIKE_INC_BD'
```

`CREATE` siempre necesita decir **que** se crea:

```sql
CREATE DATABASE NIKE_INC_BD;
GO
USE NIKE_INC_BD;
GO
```

Si esa primera linea falla, `USE` tampoco encuentra la base y todo lo que sigue se intenta crear en `master`. Por eso el error aparece en cascada y parece que el script entero estuviera mal, cuando en realidad es una sola palabra.

Otros motivos del mismo sintoma:

| Sintoma | Causa | Solucion |
| :--- | :--- | :--- |
| `Incorrect syntax near 'GO'` | `GO` no es T-SQL, es separador de lotes de SSMS | ejecutarlo en SSMS o quitar los `GO` |
| `CREATE DATABASE permission denied` | el usuario no tiene permiso `dbcreator` | pedir al administrador o usar una base existente |
| `Database 'NIKE_INC_BD' already exists` | se ejecuto dos veces sin el `DROP` | dejar el bloque `IF DB_ID(...)` del inicio |
| `The DELETE statement conflicted with the REFERENCE` | se intenta borrar la base con SSMS abierto dentro de ella | cambiarse a `master` antes de ejecutar (`USE master;`) |

### 5.2 Orden obligatorio antes de sacar la lamina

1. Ejecutar el script completo.
2. Comprobar los seis conteos de la seccion 6.
3. **Despues** crear el diagrama (si se crea antes, la lamina sale sin las columnas de auditoria).
4. Copiar el diagrama y guardarlo como `MODELO_FISICO.png`.
5. Ese PNG es el que va a la entrega y al PDF.

---

## 6. Consultas para comprobar que quedo bien

```sql
-- 10 tablas y ninguna vista
SELECT COUNT(*) AS tablas FROM sys.tables;
SELECT COUNT(*) AS vistas FROM sys.views;          -- debe dar 0

-- 11 claves foraneas
SELECT COUNT(*) AS foraneas FROM sys.foreign_keys;

-- columnas con IDENTITY (debe dar 7)
SELECT t.name AS tabla, c.name AS columna
FROM sys.columns c JOIN sys.tables t ON t.object_id = c.object_id
WHERE c.is_identity = 1 ORDER BY t.name;

-- restricciones CHECK (debe dar 10)
SELECT name FROM sys.check_constraints ORDER BY name;

-- columnas que admiten NULL (debe dar 3)
SELECT t.name AS tabla, c.name AS columna
FROM sys.columns c JOIN sys.tables t ON t.object_id = c.object_id
WHERE c.is_nullable = 1 AND c.name NOT LIKE '%modificacion'
ORDER BY t.name, c.column_id;

-- valores por omision de negocio (debe dar 9)
SELECT OBJECT_NAME(parent_object_id) AS tabla, name
FROM sys.default_constraints ORDER BY tabla, name;

-- nombres y columnas que NO deben existir (las tres consultas dan 0 filas)
SELECT name FROM sys.tables   WHERE name IN ('TOTAL', 'IGV');
SELECT name FROM sys.columns  WHERE name IN ('total', 'igv', 'estado_envio');

-- el total de la linea se calcula, no se guarda
SELECT TOP 5 d.PEDIDO_id_pedido, d.PRODUCTO_id_producto,
       d.cantidad * d.precio_unitario_aplicado AS total_linea
FROM DETALLE_VENTA d;
```

---

## 7. Que decir en la exposicion

> *"El DDL mantiene las 10 tablas y las 11 claves foraneas del modelo relacional, y agrega lo propio del motor: `IDENTITY` en las claves simples para que el codigo se genere solo, `DEFAULT` para los estados y las fechas de arranque, diez `CHECK` que impiden cantidades negativas, precios en cero, estados fuera de catalogo y telefonos o correos mal escritos, y cuatro campos de auditoria por tabla. Ninguna tabla guarda el total ni el IGV: se calculan en la consulta."*

---

## 8. Diccionario de datos (entregable aparte)

El modelo fisico se documenta con **`DICCIONARIO_DE_DATOS.xlsx`** (en la raiz de `proyecto_parcial/`), que se genera leyendo el propio script `MF_NIKE_INC_CORREGIDO.sql`: si el script cambia, el diccionario cambia con el. Tiene seis hojas:

| Hoja | Que contiene |
| :--- | :--- |
| **Resumen** | Datos del proyecto, cifras del modelo (10 tablas, 88 columnas, 11 FK, 10 CHECK...) y convenciones de nombres. |
| **Diccionario** | Las **88 columnas** (48 de negocio + 40 de auditoria) con tipo, si admite `NULL`, clave, referencia, `IDENTITY`, `DEFAULT` y su significado en lenguaje del negocio. |
| **Claves foraneas** | Las 11 FK con tabla hija, columna, tabla padre y la regla de negocio que hacen cumplir. |
| **Restricciones** | Las 7 columnas con `IDENTITY`, los 9 `DEFAULT` de negocio y los 10 `CHECK`, cada uno con su justificacion. |
| **Relaciones** | Las 8 relaciones del modelo con su cardinalidad y su lectura en palabras. |
| **Glosario** | Terminos del proyecto: `MER`, `PK`, `FK`, clave compuesta, `IDENTITY`, suministro, detalle, etc. |

Tambien existe la version en texto **`DICCIONARIO_DE_DATOS.md`** y las tres primeras paginas del diccionario van dentro de **`ENTREGA_MODELOS_NIKE_GRUPO_5.pdf`** (paginas 5, 6 y 7).

**Como usarlo en la exposicion:** si preguntan "que guarda `precio_unitario_aplicado`" o "por que `correo_electronico` mide 80", la respuesta esta en la hoja `Diccionario`; si preguntan "que impide que se venda cantidad cero", esta en `Restricciones`.

---

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

Aqui se explica **por que** cada campo mide lo que mide y **por que** solo tres columnas aceptan un valor vacio.

---

## 1. Longitudes justas y necesarias

El profesor pidio no dejar los tamanios por defecto de la herramienta (`VARCHAR(255)`, `NUMBER` sin precision). Cada medida se calculo con el dato real:

| Campo | Tipo definitivo | Por que esa medida |
| :--- | :---: | :--- |
| `telefono / telefono_secundario` | **`VARCHAR(15)`** | 9 digitos en Peru; 15 es el tope internacional (E.164) para un cliente extranjero que compra en el pais. |
| `correo_electronico` | **`VARCHAR(80)`** | un correo real mide entre 25 y 45 caracteres; 80 deja margen sin reservar 255. |
| `nombre / nombre de producto` | **`VARCHAR(80)`** | entran nombres completos y nombres comerciales largos. |
| `direccion / direccion_local` | **`VARCHAR(150)`** | una direccion peruana con referencia y distrito llega a 90-120 caracteres. |
| `nombre_almacen / nombre_local / nombre de categoria` | **`VARCHAR(50)`** | son nombres cortos e institucionales. |
| `metodo_pago` | **`VARCHAR(30)`** | 'Tarjeta de Credito', 'Yape', 'Plin' o 'Transferencia' no pasan de 20. |
| `estado_despacho / estado` | **`VARCHAR(20)`** | listas cortas y controladas; el estado del envio no se guarda porque se deduce del despacho. |
| `talla / talla_elegida y color / color_elegido` | **`VARCHAR(10) y VARCHAR(30)`** | talla guarda 42, 41 o M; color guarda Negro, Blanco o Azul Marino. |
| `cantidad, stock_actual, stock_minimo` | **`INTEGER`** | son unidades enteras: no necesitan decimales. |
| `precio_unitario_base / precio_unitario_aplicado` | **`DECIMAL(10,2)`** | 8 enteros y 2 decimales: alcanza para millones de soles y evita el redondeo del FLOAT. |

---

## 2. Reglas que se aplicaron

* **Texto (`VARCHAR`):** la medida es la del dato mas largo que existe hoy **mas un margen razonable**, nunca `255`.
* **Enteros (`INTEGER`):** solo para lo que se cuenta o se suma (`cantidad`, `stock_actual`, `stock_minimo`, `id_...`).
* **Importes (`DECIMAL(10,2)`):** 8 enteros y 2 decimales alcanzan para millones de soles y evitan el redondeo del `FLOAT`.
* **Fechas (`DATE`):** `fecha` del pedido, `fecha_suministro`.
* **Estados:** listas cortas y controladas (`VARCHAR(20)`), nunca texto libre.

---

## 3. Columnas que admiten `NULL` (3)

| Tabla | Columna | Por que puede quedar vacia |
| :--- | :--- | :--- |
| `CLIENTE` | `telefono_secundario` | No todos los clientes dejan un segundo numero de contacto. |
| `CATEGORIA` | `descripcion` | Una categoria puede crearse solo con su nombre. |
| `PRODUCTO` | `especificaciones` | No todos los modelos tienen la ficha tecnica cargada. |

**Regla general:** una columna es opcional solo cuando el dato **puede no existir** en el momento de registrar la fila. Ninguna clave, ninguna foranea obligatoria y ningun importe admiten `NULL`.

---

## 4. Como se ve esa opcionalidad en cada entregable

| Entregable | Como se marca |
| :--- | :--- |
| MER conceptual | El atributo sin subrayar y la nota de la leyenda; `Telefono_secundario` es el caso visible. |
| Modelo logico | Atributo **sin `*`** (casilla *Optional* marcada). |
| Modelo relacional | Columna con la marca **`o`** y sin la marca `*`. |
| Modelo fisico | Columna sin `NOT NULL` en el `CREATE TABLE`. |
| Modelo logico (Barker) | Marca **`o`** a la izquierda del atributo opcional. |

---

## 5. Datos calculados: no se guardan

* **total de la linea** = `cantidad x precio_unitario_aplicado` (se calcula en la consulta).
* **total del pedido** = `SUM(cantidad x precio_unitario_aplicado)` de sus lineas.
* **IGV** = `total del pedido x 0.18`.

Guardar el IGV en `PEDIDO` (o el total en `DETALLE_VENTA`) obligaba a digitarlos y permitia que quedaran distintos del calculo real. Por eso ninguna de las 10 tablas tiene esas columnas y el modelo no necesita ninguna vista.

---

## 6. Checklist de coherencia

* [ ] Las **10 tablas** tienen las mismas columnas en el Excel, en el modelo logico (`.dmd` y `MODELO_LOGICO.png`) y en los scripts.
* [ ] No queda ningun `VARCHAR(255)` ni `NUMBER` sin precision.
* [ ] Las **3** columnas opcionales son las mismas en todos los entregables.
* [ ] `PEDIDO` no tiene `igv` y `DETALLE_VENTA` no tiene `total`.
* [ ] Las **11 claves foraneas** tienen el mismo nombre en el Data Modeler y en los dos scripts.
* [ ] **`ALMACEN` solo aparece en `SUMINISTRO` y en `STOCK_ALMACEN`**: no hay columna de almacen en `DETALLE_VENTA`.
* [ ] Los telefonos son `VARCHAR(15)` y los metodos de pago guardan **un solo valor** por fila.

---

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

El docente reviso el Excel de normalizacion y dejo **11 observaciones escritas**. Este documento es la respuesta punto por punto: que observo, que se cambio y donde se puede verificar en la entrega.

---

## 1. Las 11 observaciones

| Nro | Punto | Lo que observo el docente | Como se corrigio | Donde se ve |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **PK** | STOCK_ALMACEN con PK de 4 campos | Se mantiene igual: el docente confirmo que es correcta (falso positivo). | STOCK_ALMACEN (talla, color, almacen, producto) |
| 2 | **PK** | SUMINISTRO_LOCAL no permitia dos despachos el mismo dia | Se creo SUMINISTRO con id_suministro como PK y se agrego DETALLE_SUMINISTRO con producto y cantidad. | SUMINISTRO + DETALLE_SUMINISTRO |
| 3 | **1FN** | 'Yape / Plin' eran dos metodos en una celda | Se dejo un solo metodo por fila: el pedido 9002 queda con 'Yape'. | PEDIDO.metodo_pago |
| 4 | **1FN** | Se cambiaron los colores del stock | Se restauraron los datos de la tabla general: Negro, Blanco y Azul Marino. | STOCK_ALMACEN.color |
| 5 | **1FN** | PK de un solo campo en DETALLE_VENTA | Ahora la PK es compuesta: pedido + producto + talla + color, para que la 2FN si cambie algo. | DETALLE_VENTA (4 columnas PK) |
| 6 | **2FN** | CLIENTE separado antes de tiempo | En 2FN los datos del cliente se quedan dentro de PEDIDO; la separacion se hace recien en 3FN. | Hoja 3_Segunda_Forma_Normal_2FN |
| 7 | **2FN** | Se perdia que almacen abastecio la mercaderia | Se resuelve con `SUMINISTRO.ALMACEN_id_almacen` (ABASTECE): el almacen no se conecta con la venta. | SUMINISTRO.ALMACEN_id_almacen |
| 8 | **2FN** | Se perdia que suministro corresponde a cada pedido | PEDIDO guarda SUMINISTRO_id_suministro, **obligatoria** (la relacion PROVEE no es opcional). | PEDIDO.SUMINISTRO_id_suministro |
| 9 | **3FN** | total e igv se pueden calcular | Se **eliminaron las dos columnas**: el total de la linea y el igv del pedido se calculan cuando se consulta. | Ninguna tabla |
| 10 | **3FN** | DETALLE_VENTA guardaba talla pero no color | Se agrego color_elegido, porque el stock se maneja por talla y color. | DETALLE_VENTA.color_elegido |
| 11 | **3FN** | Estados contradictorios entre ENTREGADO y EN RUTA | Queda **un solo estado de proceso** (`estado_despacho` en `SUMINISTRO`); el estado del pedido se deduce de el y no se guarda. | PEDIDO y SUMINISTRO |

---

## 2. Que cambio en el modelo, en resumen

| Antes | Ahora |
| :--- | :--- |
| 9 tablas | **10 tablas** (aparecen `SUMINISTRO` y `DETALLE_SUMINISTRO`) |
| 8 claves foraneas | **11 claves foraneas** |
| `SUMINISTRO_LOCAL` con PK `(fecha_suministro, almacen, local)` | `SUMINISTRO` con PK `id_suministro` + `DETALLE_SUMINISTRO` |
| `DETALLE_VENTA` con `id_detalle` | PK compuesta `(pedido, producto, talla, color)` |
| `DETALLE_VENTA` sin color | `color_elegido` en la PK |
| `PEDIDO.igv` guardado | **Sin columna `igv`**: se calcula al consultar |
| `total` digitado | **Sin columna `total`**: se calcula al consultar |
| `metodo_pago` = `Yape / Plin` | `Yape` (un valor por celda) |
| Colores del stock cambiados | `Negro`, `Blanco`, `Azul Marino` |
| 4 columnas con `NULL` | **3** columnas con `NULL` (`telefono_secundario`, `descripcion`, `especificaciones`) |

---

## 3. Por que el pedido ya no guarda su propio estado

En la revision final el docente observo que `estado_envio` se deducia del estado del suministro: **PENDIENTE = PROGRAMADO**, **ENVIADO = EN RUTA**, **ENTREGADO = ENTREGADO**. Es un dato derivado, asi que **se elimino de `PEDIDO`** en todos los niveles.

| Estado del pedido (deducido) | `SUMINISTRO.estado_despacho` | Que significa |
| :--- | :--- | :--- |
| PENDIENTE | PROGRAMADO | El despacho aun no sale del centro de distribucion. |
| ENVIADO | EN RUTA | La mercaderia ya salio y va camino al local. |
| ENTREGADO | ENTREGADO | El local recibio la mercaderia y el pedido quedo atendido. |

Asi queda **un solo catalogo de estado de proceso** (`estado_despacho`: PROGRAMADO, EN RUTA, ENTREGADO) y no hay dos columnas que puedan contradecirse. `PRODUCTO.estado` es otra cosa: si el modelo esta disponible para la venta (DISPONIBLE, AGOTADO, DESCONTINUADO).

---

## 4. Donde se verifica cada correccion

| Entregable | Que revisar |
| :--- | :--- |
| Excel de normalizacion | Hoja `0_Correcciones_Docente` (las 11), `5_Estados` y la 3FN con 10 tablas. |
| MER (`.drawio` y `.png`) | Entidad `SUMINISTRO` con `ID_SUMINISTRO` subrayado, rombos `INCLUYE`, `PROVEE` y `ABASTECE`, flechas de las 1:N apuntando al lado 1, `Color_elegido` en `CONTIENE` y ninguna elipse `Total` ni `IGV`. |
| Modelo logico y relacional (`.dmd`) | 10 entidades, 11 relaciones obligatorias, PK compuestas, `SUMINISTRO_id_suministro` en `PEDIDO` y ninguna columna de almacen en `DETALLE_VENTA`. |
| Scripts SQL | 10 `CREATE TABLE` y 11 `FOREIGN KEY`, sin columnas calculadas ni vistas. |
| Modelo logico (`MODELO_LOGICO.png`) | 10 entidades, 11 relaciones 1:N, `ALMACEN` unido solo a `SUMINISTRO` y `STOCK_ALMACEN`. |
| Presentacion (PDF) | Lamina 8 "Correcciones del docente aplicadas al modelo" y lamina 13 "Como se marca cada opcion". |

---

## 5. Consultas de verificacion

```sql
-- Debe devolver 10
SELECT COUNT(*) FROM sys.tables;

-- Debe devolver 11
SELECT COUNT(*) FROM sys.foreign_keys;

-- Debe devolver 3
SELECT COUNT(*) FROM sys.columns WHERE is_nullable = 1;

-- El total no se guarda: se calcula
SELECT PEDIDO_id_pedido, cantidad * precio_unitario_aplicado AS total_linea FROM DETALLE_VENTA;

-- La PK de la linea vendida tiene 4 columnas
SELECT c.name FROM sys.index_columns ic
JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id
WHERE ic.object_id = OBJECT_ID('DETALLE_VENTA') AND ic.is_included_column = 0
ORDER BY ic.key_ordinal;
```

---

## 6. Si el docente pregunta "que paso con el suministro"

La version anterior usaba la **fecha** como clave del suministro. Eso tenia dos fallos: **no se podian registrar dos despachos el mismo dia** y **no se sabia que productos llevaba cada despacho**. La solucion fue separar la **cabecera** (`SUMINISTRO`: quien despacha, quien recibe, fecha y estado) del **detalle** (`DETALLE_SUMINISTRO`: producto y cantidad), que es el mismo patron que ya se usaba en las ventas con `PEDIDO` y `DETALLE_VENTA`.

---

## 7. Ajustes hechos despues de la revision del diagrama

Estos cambios no vienen de una observacion escrita, salieron al revisar el propio MER y se aplicaron en **todos** los entregables:

| Antes | Ahora | Por que |
| :--- | :--- | :--- |
| Rombo `DESPACHA` entre `ALMACEN` y `SUMINISTRO` | Rombo **`ABASTECE`** (el almacen abastece al suministro) | El nombre `DESPACHA` se confundia con el estado del pedido; `ABASTECE` describe el sentido real de la relacion. |
| `PROVEE` marcada como opcional | `PROVEE` es **1:N obligatoria** (`PEDIDO.SUMINISTRO_id_suministro` es `NOT NULL`) | Todo pedido sale de un suministro; si la FK fuera opcional se perderia la trazabilidad del despacho. |
| `Total` e `IGV` | **Fuera del modelo, en los cuatro niveles** | Son calculos: se obtienen en la consulta y no deben existir como atributo. |
| `Total` e `IGV` | **No existen en ningun nivel** | Son calculos: se obtienen multiplicando `cantidad` por `precio_unitario_aplicado` y aplicando el 18 %. |
| Rombos M:N con flecha | `CONTIENE`, `ALMACENA` e `INCLUYE` **sin flecha** | La flecha solo tiene sentido en las 1:N, donde indica el lado "1". |
| Flechas de las 1:N sin punta clara | La punta toca siempre la **entidad del lado 1** (`CLIENTE`, `CATEGORIA`, `LOCAL`, `ALMACEN`, `SUMINISTRO`) | Se lee en el sentido de la cardinalidad y no al reves. |
| `INCLUYE` solo con `Cantidad` | `INCLUYE` con **`Talla` + `Color` + `Cantidad`**, los dos primeros en la clave | Un mismo producto puede viajar en varias tallas y colores dentro del mismo suministro. |
| `CONTIENE` mostraba `ID_Almacen` | **`ALMACEN` solo se relaciona con `SUMINISTRO` y `PRODUCTO`** | El almacen de origen de la venta se sigue por `SUMINISTRO`; una FK de almacen en la linea duplicaba el dato. |
| `ID_DETALLE` dentro de `CONTIENE` | **Fuera**; se subrayan talla y color | Un identificador propio convierte el rombo en entidad; la clave compuesta si pertenece a la relacion. |

---

## 8. Revision por niveles (MER 3/5, logico 2/5, relacional 3/4, fisico 3/6)

Esta es la revision que el docente hizo sobre el **PDF anterior** y lo que se hizo en cada frente.

| Nivel | Observacion | Como quedo |
| :--- | :--- | :--- |
| **MER** | `Total` (en CONTIENE) e `IGV` (en PEDIDO) son calculables | **Se quitaron del diagrama**: un calculo no es un atributo del modelo. El total se obtiene multiplicando `cantidad` por precio y el IGV es el 18 % de la suma, en la consulta. |
| **MER** | `ID_DETALLE` no debe estar dentro de una relacion M:N porque la convierte en entidad | No hay ningun `ID_DETALLE`. **Lo que se subraya dentro del rombo es la clave compuesta** (talla y color), no un identificador propio. |
| **MER** | SUMINISTRA solo tiene fecha y estado: no dice que productos ni cuantos se envian | El despacho se detalla en **`INCLUYE`** (`Talla`, `Color`, `Cantidad`) y en el relacional en **`DETALLE_SUMINISTRO`**. |
| **MER** | Subrayen las PK, exporten en fondo blanco y con mayor resolucion, un modelo por diapositiva | PK subrayadas solo en entidades; PNG **4800 x 3540 px en fondo blanco**; conceptual, logico, relacional y fisico van en laminas separadas. |
| **Logico** | Las relaciones no muestran nombre ni cardinalidad | `MODELO_LOGICO.png` escribe **el verbo sobre cada linea** y las etiquetas **`1` y `N`** en los extremos. |
| **Logico** | En el logico solo se configura, no se visualizan las entidades intermedias | La lamina muestra **7 entidades y sus relaciones**; las tres M:N quedan configuradas y aparecen recien en `MODELO_RELACIONAL.png`. |
| **Relacional** | `DETALLE_VENTA.total` contradice la 3FN | **No existe la columna**: se calcula `cantidad x precio_unitario_aplicado` en la consulta. La 3FN del Excel ya no muestra ningun calculo. |
| **Relacional** | Faltan los ejemplos de normalizacion de 0FN a 3FN | El Excel tiene las cuatro hojas `0FN`, `1FN`, `2FN` y `3FN` con los mismos datos, y coinciden con los diagramas (10 tablas, 11 FK). |
| **Fisico** | No se ven IDENTITY, DEFAULT, CHECK ni campos de auditoria | El DDL los trae: **7 `IDENTITY`**, **10 `DEFAULT`**, **11 `CHECK`** y **4 campos de auditoria en las 10 tablas** (ver GUIA 4). |
| **Fisico** | Corrijan los apuntes anteriores y generen de vuelta el DDL | Los dos scripts (SQL Server y Oracle) se regeneraron completos desde el modelo corregido. |

### Como se responde en la exposicion

> *"Los cuatro modelos estan separados. En el conceptual no dibujamos ningun atributo calculado y subrayamos la clave compuesta dentro de los rombos de muchos a muchos, sin darles un identificador propio. En el logico solo configuramos las relaciones con su verbo y su cardinalidad, y las de muchos a muchos van como relacion con sus atributos, no como tabla intermedia. En el relacional esas relaciones ya se materializan en diez tablas con once claves foraneas, sin ninguna columna calculada. Y en el fisico agregamos `IDENTITY`, `DEFAULT`, `CHECK` y auditoria en todas las tablas."*

---

## 9. Ultima revision: 0FN, 1FN, 2FN y 3FN

| Fase | Observacion | Como quedo |
| :--- | :--- | :--- |
| **0FN y 1FN** | Los productos y cantidades del suministro aparecen recien en 2FN | La tabla general ya trae `productos_suministrados` y `cantidades_suministradas` (20, 15, 25 y 40 unidades) y la 1FN los deja atomicos por fila, con producto, talla y color. La 2FN sale de ahi. |
| **2FN** | Esta incompleta: faltan PRODUCTO (con su categoria), ALMACEN, LOCAL y STOCK_ALMACEN | La hoja 2FN tiene **8 tablas**: PEDIDO, DETALLE_VENTA, PRODUCTO (con los datos de su categoria), SUMINISTRO, DETALLE_SUMINISTRO, ALMACEN, LOCAL y STOCK_ALMACEN. Todo lo de la 1FN queda en alguna tabla. |
| **3FN** | `estado_envio` se deduce del estado del suministro | Se **elimino la columna** de `PEDIDO` en el Excel, el MER, el logico, el relacional y el DDL. |
| **3FN** | Dejen escrito que un pedido se atiende con un solo suministro (un almacen y un local) | Escrito en el MER, en el logico, en el relacional y en el fisico. En la base se cumple con `PEDIDO.SUMINISTRO_id_suministro`: una sola columna obligatoria. |

### El PDF de entrega

`ENTREGA_MODELOS_NIKE_GRUPO_5.pdf` (en la raiz de `proyecto_parcial/`) trae **12 paginas**: portada, la respuesta punto por punto a estas observaciones, la regla del suministro unico con la tabla de equivalencia de estados, un extracto del DDL, el **diccionario de datos** (paginas 5, 6 y 7) y **una lamina por modelo** (conceptual, logico, relacional y fisico), mas el cuadro de paso de un nivel al siguiente. El diccionario completo, con las seis hojas, va aparte en `DICCIONARIO_DE_DATOS.xlsx`.

---

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios
**Curso:** Disenio de Bases de Datos Relacionales - IDAT
**Docente:** Sergio Fernando Castillo Carrion

---

**Archivos que produce esta guia:**

| Archivo | Donde esta | Que es |
| :--- | :--- | :--- |
| `DICCIONARIO_DE_DATOS.xlsx` | `proyecto_parcial/` | Diccionario completo, seis hojas, listo para entregar |
| `DICCIONARIO_DE_DATOS.md` | `proyecto_parcial/` | La misma informacion en texto, para leer o pegar en el informe |
| `ENTREGA_MODELOS_NIKE_GRUPO_5.pdf` | `proyecto_parcial/` | PDF de entrega: **12 paginas**, con el diccionario en las paginas 5, 6 y 7 |

---

## 1. Que es un diccionario de datos y por que lo piden

El **modelo fisico** dice *como* esta hecha la base: tablas, tipos y restricciones. El **diccionario de datos** dice *que significa* cada cosa: para que existe cada columna, que valores acepta, quien la llena y que regla la protege.

Son dos documentos distintos y el segundo no se puede inventar de memoria: tiene que describir **exactamente** la base que se ejecuto. Por eso el diccionario de este proyecto **no se escribe a mano**: se genera leyendo el script `nivel_fisico/MF_NIKE_INC_CORREGIDO.sql`.

```
MF_NIKE_INC_CORREGIDO.sql  --->  generadores/diccionario.py  --->  DICCIONARIO_DE_DATOS.xlsx
   (la base real)                                                  DICCIONARIO_DE_DATOS.md
                                                                   (paginas 5-7 del PDF)
```

Consecuencia practica: **si cambias el script, vuelve a generar el diccionario**. Si no, el documento empieza a mentir (por ejemplo, sigue mostrando una columna que ya se borro).

---

## 2. Las seis hojas del Excel

| # | Hoja | Que muestra | Para que sirve en la exposicion |
| :---: | :--- | :--- | :--- |
| 1 | **Resumen** | Datos del grupo, motor, **cifras del modelo** (10 tablas, 88 columnas, 7 `IDENTITY`, 9 `DEFAULT` de negocio, 10 `CHECK`, 11 FK, 3 columnas opcionales, 0 vistas) y las **convenciones de nombres**. | Abre la conversacion: "esta es la base, estas son sus cifras". |
| 2 | **Diccionario** | Las **88 columnas** una por una: tabla, columna, tipo, `NULL`, clave (`PK` / `FK` / `PK + FK`), referencia, `IDENTITY`, `DEFAULT` y **descripcion de negocio**. | Es la hoja que se consulta cuando preguntan por una columna concreta. |
| 3 | **Claves foraneas** | Las **11 FK** con tabla hija, columna, tabla padre, columna referenciada y la regla de negocio. | Demuestra que las relaciones del MER estan implementadas. |
| 4 | **Restricciones** | Los **7 `IDENTITY`**, los **9 `DEFAULT`** de negocio y los **10 `CHECK`**, cada uno con su justificacion. | Es la prueba de lo que el docente califico en el fisico. |
| 5 | **Relaciones** | Las **8 relaciones** del MER con su cardinalidad y su lectura en palabras. | Conecta el conceptual con el fisico. |
| 6 | **Glosario** | `MER`, `PK`, `FK`, clave compuesta, `IDENTITY`, `DEFAULT`, `CHECK`, suministro, detalle, `Total`/`IGV`. | Evita que cada integrante explique distinto. |

Las **4 columnas de auditoria** (`usuario_creacion`, `fecha_creacion`, `usuario_modificacion`, `fecha_modificacion`) se repiten igual en las 10 tablas. En el Excel aparecen en gris al final de cada tabla; en el PDF y en el `.md` se explican **una sola vez** para no repetir la misma fila 40 veces.

---

## 3. Como se lee una fila del diccionario

Ejemplo real (hoja `Diccionario`):

| Tabla | Columna | Tipo | NULL | Clave | Referencia | IDENTITY | DEFAULT | Descripcion |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: | :--- | :--- |
| PEDIDO | `SUMINISTRO_id_suministro` | `INT` | No | FK | `SUMINISTRO.id_suministro` | - | - | Suministro que atiende el pedido. Una sola columna obligatoria: por eso un pedido se atiende con un unico suministro. |
| DETALLE_VENTA | `cantidad` | `INT` | No | - | - | - | `1` | Unidades vendidas de ese producto, talla y color. Debe ser mayor que cero. |
| CLIENTE | `telefono_secundario` | `VARCHAR(15)` | **Si** | - | - | - | - | Celular alterno. Es opcional: hay clientes que solo dejan un numero. |
| CLIENTE | `id_cliente` | `INT` | No | PK | - | **Si** | - | Codigo unico del comprador. Lo genera la base. |

Como se leen las marcas:

* **`PK`**: identifica la fila. **`PK + FK`**: forma parte de una clave compuesta y ademas apunta a otra tabla (pasa en las tres tablas de detalle).
* **`NULL = Si`**: la unica forma en que una columna puede quedar vacia. En este modelo son solo tres.
* **`IDENTITY = Si`**: el valor no se escribe, lo genera SQL Server.
* **`DEFAULT`**: lo que la base pone sola si el `INSERT` no manda ese dato.

---

## 4. Las cifras oficiales del modelo

Estos son los numeros que hay que decir, y son los mismos en el diccionario, en el PDF, en el README y en las guias:

| Concepto | Numero | Donde se comprueba |
| :--- | :---: | :--- |
| Tablas | **10** | `SELECT COUNT(*) FROM sys.tables;` |
| Columnas | **88** (48 de negocio + 40 de auditoria) | hoja `Diccionario` |
| Claves primarias simples con `IDENTITY` | **7** | `WHERE c.is_identity = 1` |
| Claves primarias compuestas | **3** | `DETALLE_VENTA`, `STOCK_ALMACEN`, `DETALLE_SUMINISTRO` |
| Claves foraneas | **11** | `SELECT COUNT(*) FROM sys.foreign_keys;` |
| Restricciones `CHECK` | **10** | `SELECT COUNT(*) FROM sys.check_constraints;` |
| `DEFAULT` de negocio | **9** | `SELECT * FROM sys.default_constraints;` |
| Columnas que admiten `NULL` | **3** | `telefono_secundario`, `descripcion`, `especificaciones` |
| Vistas | **0** | `SELECT COUNT(*) FROM sys.views;` |
| Relaciones del MER | **8** | `REALIZA`, `CONTIENE`, `CLASIFICA`, `ALMACENA`, `PROVEE`, `ABASTECE`, `RECIBE`, `INCLUYE` |

---

## 5. Como se regenera (si cambia el script)

```bash
cd /home/user/generadores
python3 diccionario.py          # vuelve a leer el .sql y reescribe el xlsx, el md y el json
python3 pdf_entrega.py          # rehace el PDF con las paginas nuevas del diccionario
```

`diccionario.py` no guarda datos a mano: recorre el script y arma la estructura con expresiones regulares sobre:

* `CREATE TABLE` → nombre de tabla, columnas, tipos, `NULL`, `IDENTITY`, `DEFAULT`;
* `CONSTRAINT ... PRIMARY KEY` → clave primaria (simple o compuesta);
* `CONSTRAINT CK_... CHECK (...)` → validaciones (soporta las que ocupan dos lineas, como `CK_CLIENTE_TELEFONO`);
* `ALTER TABLE ... FOREIGN KEY` → las 11 claves foraneas.

Las **descripciones de negocio** si son texto escrito por el grupo (un diccionario tecnico no puede deducir para que sirve un `precio_unitario_aplicado`). Estan en el diccionario `DESC` al inicio de `diccionario.py`, y se pueden editar sin tocar nada mas.

---

## 6. Checklist antes de entregar

**Diccionario**

1. Abrir `DICCIONARIO_DE_DATOS.xlsx` y revisar que la hoja `Resumen` diga **10 tablas / 11 FK / 7 IDENTITY / 9 DEFAULT / 10 CHECK**.
2. Buscar en la hoja `Diccionario` las palabras **`total`**, **`igv`** y **`estado_envio`**: no debe aparecer ninguna como columna.
3. Confirmar que las **3 columnas opcionales** son las mismas del modelo (`telefono_secundario`, `descripcion`, `especificaciones`).
4. Confirmar que las 3 tablas de detalle muestran **`PK + FK`** y no llevan `IDENTITY`.

**Coherencia con los otros entregables**

5. El nombre de la base coincide en todos lados: **`NIKE_INC_BD`**.
6. El nombre del correo coincide en todos lados: **`correo_electronico`** (`VARCHAR(80)`).
7. Las longitudes del diccionario coinciden con el modelo relacional y con la GUIA 5.
8. Las 8 relaciones y sus cardinalidades coinciden con el MER y con el logico (`PROVEE` es `1:N`).

**PDF**

9. El PDF debe tener **12 paginas**: portada, respuestas al docente, regla del suministro, extracto del DDL, **diccionario (5, 6 y 7)**, y las cuatro laminas mas el cuadro final.
10. Las laminas van a tamano completo, una por pagina.

---

## 7. Que decir al presentar el diccionario

> *"El diccionario de datos esta generado a partir del script que realmente ejecutamos en SQL Server, no escrito aparte. Tiene seis hojas: el resumen con las cifras del modelo, las 88 columnas con su tipo y su significado, las 11 claves foraneas, las restricciones -- siete `IDENTITY`, nueve `DEFAULT` y diez `CHECK` --, las ocho relaciones con su cardinalidad y un glosario. Por eso cualquier pregunta sobre una columna se responde con este archivo, y cualquier cambio en el script obliga a regenerarlo para que no queden desalineados."*

---
