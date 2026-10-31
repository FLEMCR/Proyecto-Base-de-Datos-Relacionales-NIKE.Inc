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
