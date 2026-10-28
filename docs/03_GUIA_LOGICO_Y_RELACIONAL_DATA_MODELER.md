# GUIA 3: MODELO LOGICO Y RELACIONAL EN ORACLE SQL DEVELOPER DATA MODELER

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

**Carpeta:** `nivel_logico/BD NIKE.Inc/` + archivo **`BD NIKE.Inc.dmd`**  
**Imagen:** `MODELO_LOGICO.png` (notacion Barker, ordenada igual que el MER)

---

## 1. Que hay en la carpeta del Data Modeler

El proyecto de Data Modeler es una **carpeta**, no un archivo suelto:

```
nivel_logico/
├── BD NIKE.Inc.dmd          <- archivo que se abre desde Data Modeler
└── BD NIKE.Inc/             <- carpeta con los XML del disenio
    ├── relational/          <- tablas, claves foraneas e indices del modelo relacional
    ├── logical/             <- entidades, atributos y relaciones del modelo logico
    ├── diagram/             <- posiciones de las cajas en la lamina
    └── ...
```

Para abrirlo: **File > Open** en Oracle SQL Developer Data Modeler y elegir **`BD NIKE.Inc.dmd`**. Si se copia solo el `.dmd` sin la carpeta, el programa abre el proyecto vacio.

---

## 2. Del modelo conceptual al logico

Las relaciones del MER se convierten en tablas (las de muchos a muchos) o en claves foraneas (las de uno a muchos):

| En el MER | En el modelo logico/relacional |
| :--- | :--- |
| REALIZA (1,N) | FK `CLIENTE_id_cliente` en `PEDIDO` |
| CLASIFICA (1,N) | FK `CATEGORIA_id_categoria` en `PRODUCTO` |
| CONTIENE (M,N) | Tabla **`DETALLE_VENTA`** + FK a `PEDIDO` y `PRODUCTO` |
| ALMACENA (N,M) | Tabla **`STOCK_ALMACEN`** con PK de 4 campos |
| ABASTECE (1,N) | FK `ALMACEN_id_almacen` en `SUMINISTRO` |
| RECIBE (1,N) | FKs `LOCAL_id_local` en `SUMINISTRO` |
| PROVEE (1,N) | FK `SUMINISTRO_id_suministro` en `PEDIDO` (obligatoria) |
| INCLUYE (N,M) | Tabla **`DETALLE_SUMINISTRO`** |

Quedan **10 tablas** y **11 claves foraneas**. Nota importante: **`ALMACEN` solo se relaciona con `SUMINISTRO` (ABASTECE) y con `PRODUCTO` (ALMACENA)**; no hay ninguna FK de almacen en la venta.

---

## 3. Las 11 claves foraneas

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

Todas son relaciones **1:N**. Las N:M del MER ya estan resueltas por `DETALLE_VENTA`, `STOCK_ALMACEN` y `DETALLE_SUMINISTRO`.

---

## 4. Como se marca cada cosa en Data Modeler

* **`P` (PK):** se activa con el boton de llave en la columna o marcando el atributo como identificador de la entidad.
* **`F` (FK):** no se escribe a mano; se genera al dibujar la **relacion 1:N**. La columna aparece con el nombre `TABLA_id`.
* **`PFK`:** columna que forma parte de la clave compuesta **y** ademas es clave foranea (`DETALLE_VENTA`, `STOCK_ALMACEN`, `DETALLE_SUMINISTRO`).
* **`*` obligatorio:** la casilla **Optional** del atributo queda desmarcada (equivale a `NOT NULL`).
* **`o` opcional:** la casilla **Optional** queda marcada solo en `telefono_secundario`, `descripcion` y `especificaciones`. En el fisico significa que la columna acepta `NULL`.
* **Origen opcional:** NO se marca. Todas las relaciones son obligatorias; el docente indico que esa casilla no hace falta.
* **Tipos en la vista relacional:** `VARCHAR2(n)` para texto y `NUMBER(10,2)` para importes, con **Size** y **Precision/Scale** definidos a mano (nunca 255 por defecto).
* **Nada calculado se almacena:** `DETALLE_VENTA` no tiene `total` y `PEDIDO` no tiene `igv`. Tampoco hay vista: el total de la linea se calcula multiplicando `cantidad` por `precio_unitario_aplicado` cuando se consulta.

---

## 5. Columnas que admiten `NULL` (3 en total)

| Tabla | Columna | Por que puede quedar vacia |
| :--- | :--- | :--- |
| `CLIENTE` | `telefono_secundario` | No todos los clientes dejan un segundo numero de contacto. |
| `CATEGORIA` | `descripcion` | Una categoria puede crearse solo con su nombre. |
| `PRODUCTO` | `especificaciones` | No todos los modelos tienen la ficha tecnica cargada. |

Todo lo demas es `NOT NULL`; las claves y las foraneas **nunca** admiten `NULL`.

---

## 6. Longitudes que se ven en el modelo relacional

| Campo | Tipo definitivo | Por que esa medida |
| :--- | :---: | :--- |
| `telefono / telefono_secundario` | **`VARCHAR(15)`** | 9 digitos en Peru; 15 es el tope internacional (E.164) para un cliente extranjero que compra en el pais. |
| `correo_e` | **`VARCHAR(80)`** | un correo real mide entre 25 y 45 caracteres; 80 deja margen sin reservar 255. |
| `nombre / nombre de producto` | **`VARCHAR(80)`** | entran nombres completos y nombres comerciales largos. |
| `direccion / direccion_local` | **`VARCHAR(150)`** | una direccion peruana con referencia y distrito llega a 90-120 caracteres. |
| `nombre_almacen / nombre_local / nombre de categoria` | **`VARCHAR(50)`** | son nombres cortos e institucionales. |
| `metodo_pago` | **`VARCHAR(30)`** | 'Tarjeta de Credito', 'Yape', 'Plin' o 'Transferencia' no pasan de 20. |
| `estado_envio / estado_despacho / estado` | **`VARCHAR(20)`** | listas cortas y controladas de cada proceso. |
| `talla / talla_elegida y color / color_elegido` | **`VARCHAR(10) y VARCHAR(30)`** | talla guarda 42, 41 o M; color guarda Negro, Blanco o Azul Marino. |
| `cantidad, stock_actual, stock_minimo` | **`INTEGER`** | son unidades enteras: no necesitan decimales. |
| `precio_unitario_base / precio_unitario_aplicado` | **`DECIMAL(10,2)`** | 8 enteros y 2 decimales: alcanza para millones de soles y evita el redondeo del FLOAT. |

---

## 7. Que revisar antes de exportar

1. Que las 10 tablas tengan **PK** y que `DETALLE_VENTA`, `STOCK_ALMACEN` y `DETALLE_SUMINISTRO` muestren su **PK compuesta**.
2. Que `PEDIDO` **no** tenga columna `igv` y que `DETALLE_VENTA` **no** tenga columna `total`.
3. Que `PEDIDO` muestre `SUMINISTRO_id_suministro` (obligatoria), que `DETALLE_SUMINISTRO` muestre su PK de 4 campos (`suministro`, `producto`, `talla`, `color`) y que **`DETALLE_VENTA` no tenga ninguna columna de almacen**.
4. Que ningun `VARCHAR2` quede en `255` y ningun importe quede en `NUMBER` sin precision.
5. Guardar el proyecto y verificar que la carpeta `BD NIKE.Inc/` tenga los XML (si falta, el `.dmd` viaja incompleto).

---

## 8. Como se lee el modelo logico en Barker (`MODELO_LOGICO.png`)

El dibujo va ordenado igual que el MER:

```
CLIENTE -- PEDIDO -- DETALLE_VENTA -- PRODUCTO -- CATEGORIA
              |
           SUMINISTRO -- DETALLE_SUMINISTRO
              |                  |
            LOCAL            ALMACEN -- STOCK_ALMACEN
```

* **El `1` va del lado uno y la pata de gallo del lado muchos.** Se lee: *un CLIENTE hace muchos PEDIDOS*.
* **`ALMACEN` aparece una sola vez en la zona baja**, unido a `SUMINISTRO` (a traves de la FK `ALMACEN_id_almacen`) y a `STOCK_ALMACEN` (por `ALMACEN_id_almacen` + `PRODUCTO_id_producto`).
* **No hay ninguna linea entre `ALMACEN` y `DETALLE_VENTA`.**
* Las relaciones son **obligatorias**: la casilla *Optional* del origen queda desmarcada y las FK son `NOT NULL`.
* Las tres M:N del MER ya estan resueltas como tablas: `DETALLE_VENTA`, `STOCK_ALMACEN` y `DETALLE_SUMINISTRO`.

---

## 9. Del logico al relacional y al fisico (lo haces tu, en este orden)

1. **Logico** (esta guia): entidades con atributos, PK marcada y relaciones 1:N / M:N.
2. **Relacional:** boton **Engineer to Relational Model** (`>>`) en Data Modeler. Aparecen las tablas con tipos, `P` / `F` / `PF`, y las restricciones `TABLA_PK` y `TABLA_PADRE_FK`. Revisa que no aparezca ninguna columna de almacen en `DETALLE_VENTA`.
3. **Fisico:** genera el DDL desde el relacional y ejecutalo en SSMS. El modelo no necesita vistas ni columnas calculadas.
