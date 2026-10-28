# GUIA 6: CORRECCIONES DEL DOCENTE APLICADAS AL MODELO

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
| 11 | **3FN** | Estados contradictorios entre ENTREGADO y EN RUTA | Se definieron dos procesos distintos: estado_envio es del pedido al cliente y estado_despacho es del CD al local. | Hoja 5_Estados |

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

## 3. Por que `estado_envio` y `estado_despacho` no se contradicen

| Campo | Tabla | Para que sirve | Valores permitidos | Ejemplo |
| :--- | :--- | :--- | :--- | :--- |
| **`estado_envio`** | `PEDIDO` | Como va la entrega del pedido al cliente. | PENDIENTE, ENVIADO, ENTREGADO | Pedido 9002 = ENTREGADO: el cliente ya recibio su compra. |
| **`estado_despacho`** | `SUMINISTRO` | Como va el traslado de mercaderia del CD al local. | PROGRAMADO, EN RUTA, ENTREGADO | Suministro 2 = EN RUTA: la carga sale del CD hacia el local. |

**El ejemplo que pidio el docente:** en el pedido **9002** el `estado_envio` es **ENTREGADO** porque el cliente ya recibio su compra, y el `estado_despacho` del suministro que lo abastecio es **EN RUTA** porque esa carga todavia va del centro de distribucion al local. Son dos cadenas distintas:

1. **Pedido:** cliente compra -> pedido `PENDIENTE` -> sale del almacen `ENVIADO` -> llega al cliente `ENTREGADO`.
2. **Suministro:** el CD programa el despacho `PROGRAMADO` -> sale `EN RUTA` -> llega al local `ENTREGADO`.

Un pedido puede estar entregado con mercaderia que estaba en stock, mientras el siguiente despacho sigue en camino.

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
| Elipse `Total (calculado)` en `CONTIENE` | **Eliminada** | Un atributo derivado no se dibuja como si fuera un dato guardado: el total se calcula en la vista. |
| Elipse `IGV` en `PEDIDO` | **Eliminada** | El IGV es el 18 % del total del pedido, tambien calculado. |
| Rombos M:N con flecha | `CONTIENE`, `ALMACENA` e `INCLUYE` **sin flecha** | La flecha solo tiene sentido en las 1:N, donde indica el lado "1". |
| Flechas de las 1:N sin punta clara | La punta toca siempre la **entidad del lado 1** (`CLIENTE`, `CATEGORIA`, `LOCAL`, `ALMACEN`, `SUMINISTRO`) | Se lee en el sentido de la cardinalidad y no al reves. |
| `INCLUYE` solo con `Cantidad` | `INCLUYE` con **`Talla` + `Color` + `Cantidad`**, los dos primeros en la clave | Un mismo producto puede viajar en varias tallas y colores dentro del mismo suministro. |
| `CONTIENE` sin almacen visible | `CONTIENE` muestra **`ID_Almacen`** | Explica de donde salio el par vendido (lo pidio el docente en la 2FN). |
