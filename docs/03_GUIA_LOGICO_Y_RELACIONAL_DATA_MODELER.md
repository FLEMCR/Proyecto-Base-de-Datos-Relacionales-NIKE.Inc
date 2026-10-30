# GUIA 3: MODELO LOGICO Y RELACIONAL EN ORACLE SQL DEVELOPER DATA MODELER

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
| PROVEE (1,N) | relacion `SUMINISTRO` → `PEDIDO` | FK `SUMINISTRO_id_suministro` en `PEDIDO` |
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
| `correo_e` | **`VARCHAR(80)`** | un correo real mide entre 25 y 45 caracteres; 80 deja margen sin reservar 255. |
| `nombre / nombre de producto` | **`VARCHAR(80)`** | entran nombres completos y nombres comerciales largos. |
| `direccion / direccion_local / ubicacion` | **`VARCHAR(120)`** | una direccion peruana con referencia y distrito llega a 90-120 caracteres. |
| `nombre_almacen / nombre_local / nombre de categoria` | **`VARCHAR(50)`** | son nombres cortos e institucionales. |
| `metodo_pago` | **`VARCHAR(30)`** | 'Tarjeta de Credito', 'Yape' o 'Transferencia' no pasan de 20. |
| `estado_envio / estado_despacho / estado` | **`VARCHAR(20)`** | listas cortas y controladas de cada proceso. |
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
