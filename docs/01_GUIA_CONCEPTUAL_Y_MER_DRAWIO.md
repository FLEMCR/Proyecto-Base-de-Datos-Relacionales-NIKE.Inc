# GUIA 1: ENTENDER EL PROYECTO NIKE PERU Y EL DIAGRAMA M.E.R. (DRAW.IO)

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

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
| `correo_e` | **`VARCHAR(80)`** | un correo real mide entre 25 y 45 caracteres; 80 deja margen sin reservar 255. |
| `nombre / nombre de producto` | **`VARCHAR(80)`** | entran nombres completos y nombres comerciales largos. |
| `direccion / direccion_local` | **`VARCHAR(150)`** | una direccion peruana con referencia y distrito llega a 90-120 caracteres. |
| `nombre_almacen / nombre_local / nombre de categoria` | **`VARCHAR(50)`** | son nombres cortos e institucionales. |
| `metodo_pago` | **`VARCHAR(30)`** | 'Tarjeta de Credito', 'Yape' o 'Transferencia' no pasan de 20. |
| `estado_envio / estado_despacho / estado` | **`VARCHAR(20)`** | listas cortas y controladas de cada proceso. |
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
