# Revision de tus 4 diagramas + donde va el punto 4

Revisado sobre: `Diagrama MER (NIKE) - GRUPO 5.png`, `Modelo_Logico.png`, `Modelo_Relacional.png`,
`Modelo_Fisico.png` y `MF_NIKE_INC.sql` (los que subiste).

---

## 1. Donde se declara el punto 4 ("un pedido se atiende con un solo suministro")

**No va en el Excel.** El Excel demuestra normalizacion (dependencias funcionales), no reglas de negocio.
Se declara en cinco sitios, de menor a mayor formalidad:

| # | Donde | Que escribir exactamente |
| :---: | :--- | :--- |
| 1 | **MER** | En el extremo de `PEDIDO` de la relacion `PROVEE`, escribir **`(1,1)`** y una nota al pie: *"Un PEDIDO se atiende con un solo SUMINISTRO, es decir, con un solo ALMACEN de origen y un solo LOCAL de destino."* |
| 2 | **Modelo logico** | Verbo `PROVEE` sobre la linea, con **`1` en el lado de `SUMINISTRO`** (barra) y **`1,1` en el lado de `PEDIDO`** (o `N` con la nota de unicidad). Nota al pie con la misma frase. |
| 3 | **Modelo relacional** | `SUMINISTRO_id_suministro` marcada como **FK + UK (unica)** en `PEDIDO`, y la nota al pie. En Data Modeler: clic derecho en la columna > **Create Unique Constraint**. |
| 4 | **Modelo fisico (DDL)** | `CONSTRAINT UQ_PEDIDO_SUMINISTRO UNIQUE (SUMINISTRO_id_suministro)` dentro del `CREATE TABLE PEDIDO`. |
| 5 | **PDF / informe** | Una lamina o seccion titulada **"Regla del suministro unico y equivalencia de estados"** (en el PDF que te deje es la pagina 3) y la fila correspondiente en la tabla de respuesta al docente. |

El `UNIQUE` es el que convierte la frase en una regla real: si alguien intenta asignar el mismo
suministro a dos pedidos, el motor lo rechaza.

---

## 2. Que cambia en el Excel y que cambia fuera del Excel

| Observacion del docente | Excel | MER | Logico | Relacional | Fisico / SQL | PDF |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 0FN/1FN: faltaban productos y cantidades del suministro | **si** | no | no | no | no | si (se explica) |
| 2FN incompleta (faltaban 4 tablas) | **si** | no | no | no | no | si (se explica) |
| 3FN: quitar `estado_envio` | **si** | **si** | **si** | **si** | **si** | si |
| 3FN: escribir la regla del suministro unico | no | **si** | **si** | **si** | **si** | **si** |

Conclusion: **no basta con cambiar el Excel.** El `estado_envio` y la regla del suministro unico tocan
los cuatro modelos y el script.

---

## 3. MER (`Diagrama MER (NIKE) - GRUPO 5.png`)

### Quitar
* [ ] La elipse **`Estado_envio`** de `PEDIDO` (punto 3 del docente). El estado del pedido se deduce del
      `estado_despacho` del suministro: PENDIENTE = PROGRAMADO, ENVIADO = EN RUTA, ENTREGADO = ENTREGADO.

### Agregar
* [ ] **Subrayar las PK**: `ID_CLIENTE`, `ID_PEDIDO`, `ID_SUMINISTRO`, `ID_CATEGORIA`, `ID_PRODUCTO`,
      `ID_ALMACEN`, `ID_LOCAL`. En tu imagen no estan subrayadas y el docente ya lo habia pedido.
* [ ] **`(1,1)`** en el extremo de `PEDIDO` de `PROVEE` + nota al pie del suministro unico.
* [ ] (Recomendado) elipses **punteadas** para los tres atributos que admiten NULL:
      `Telefono_secundario`, `Descripcion`, `Especificaciones`.

### Revisar
* [ ] La linea de `INCLUYE` hacia `PRODUCTO` pasa muy cerca de la de `ALMACENA`: separarlas para que no
      parezca que `INCLUYE` se une con `ALMACEN`.
* [ ] Confirmar que las flechas de las 1:N siguen apuntando al lado 1 (`CLIENTE`, `CATEGORIA`, `ALMACEN`,
      `LOCAL`, `SUMINISTRO`). En tu imagen se ven bien.
* [ ] **Ya esta correcto** lo que el docente pedia del camion: `INCLUYE` tiene `Talla`, `Cantidad` y
      `Color`. No tocar.

---

## 4. Modelo logico (`Modelo_Logico.png`)

### Quitar
* [ ] **`estado_envio`** de `PEDIDO`.

### Agregar
* [ ] **El nombre (verbo) de cada relacion.** En tu imagen no hay ninguno y es la observacion explicita
      del docente ("las relaciones no muestran nombre ni cardinalidad"): `REALIZA`, `CLASIFICA`, `PROVEE`,
      `RECIBE`, `ABASTECE`, `CONTIENE`, `INCLUYE`, `ALMACENA`.
* [ ] **Titulo a las tres cajas naranjas** con el verbo de la relacion (`CONTIENE`, `INCLUYE`, `ALMACENA`).
      Ahora parecen entidades sin nombre y el docente pidio que en el logico "no se visualicen las
      entidades intermediarias": si llevan el nombre de la relacion y no tienen clave propia, se leen
      como relacion con atributos, que es lo que son.
* [ ] Nota al pie del suministro unico (punto 4).

### Revisar cardinalidades
* [ ] `CLIENTE 1 → N PEDIDO` y `CATEGORIA 1 → N PRODUCTO`: bien.
* [ ] `SUMINISTRO 1 → N PEDIDO` (barra del lado `SUMINISTRO`, pata de gallo del lado `PEDIDO`):
      **hoy `SUMINISTRO` tiene tres patas de gallo en su borde derecho**; una de ellas corresponde a
      `PEDIDO` y esta mal: el lado 1 es `SUMINISTRO`.
* [ ] Las tres M:N (`CONTIENE`, `INCLUYE`, `ALMACENA`) deben tener **pata de gallo en los dos extremos**
      (muchos a muchos), no una barra en un lado.
* [ ] Orden y espacio: hay cajas flotando y lineas largas que cruzan; ordenarlas como el MER (ventas
      arriba, abastecimiento abajo).

---

## 5. Modelo relacional (`Modelo_Relacional.png`)

### Quitar
* [ ] **`PEDIDO.estado_envio`** `VARCHAR2(20)`.

### Agregar
* [ ] **`UQ_PEDIDO_SUMINISTRO UNIQUE (SUMINISTRO_id_suministro)`** en `PEDIDO` (punto 4).
* [ ] Nota al pie con la equivalencia de estados y la regla del suministro unico.

### Revisar
* [ ] Longitudes: `direccion VARCHAR2(150)` y `ubicacion VARCHAR2(100)` no coinciden con la tabla de
      longitudes de las guias (120). Elegir una medida y dejarla igual en modelo, DDL y guias.
* [ ] Lo demas esta bien: 10 tablas, 11 FK, 3 PK compuestas, sin `total` ni `igv`, sin vista.

---

## 6. Modelo fisico (`Modelo_Fisico.png` + `MF_NIKE_INC.sql`)

Tu script actual es el de la version anterior: **no tiene IDENTITY, DEFAULT, CHECK ni auditoria**, y
todavia trae `estado_envio`. Hay que regenerarlo.

### Quitar
* [ ] `PEDIDO.estado_envio` (y su `NOT NULL`).

### Agregar
* [ ] **`IDENTITY(1,1)`** en las 7 PK simples: `CLIENTE`, `CATEGORIA`, `ALMACEN`, `LOCAL`, `PRODUCTO`,
      `PEDIDO`, `SUMINISTRO`. Las 3 tablas de clave compuesta no lo llevan.
* [ ] **`UNIQUE (SUMINISTRO_id_suministro)`** en `PEDIDO`.
* [ ] **10 `DEFAULT`**: `PEDIDO.fecha`, `PEDIDO.metodo_pago`, `SUMINISTRO.fecha_suministro`,
      `SUMINISTRO.estado_despacho`, `PRODUCTO.estado`, `DETALLE_VENTA.cantidad`,
      `DETALLE_SUMINISTRO.cantidad`, `STOCK_ALMACEN.stock_actual`, `STOCK_ALMACEN.stock_minimo`.
* [ ] **10 `CHECK`**: cantidades `> 0`, precios `> 0`, `stock_actual >= 0`, `stock_minimo >= 0`,
      los dos catalogos de estado (`estado_despacho`, `estado` de `PRODUCTO`), formato de correo y
      formato de telefono.
* [ ] **4 columnas de auditoria en las 10 tablas**: `usuario_creacion`, `fecha_creacion`,
      `usuario_modificacion`, `fecha_modificacion`.
* [ ] Volver a generar el **diagrama de SSMS** despues de reejecutar el script, para que ahi se vean la
      llave de identidad, la columna unica y las columnas de auditoria.

---

## 7. Orden de trabajo (rápido)

1. **Excel** (30 min): 0FN y 1FN agregan productos y cantidades del suministro; 2FN se completa a 8
   tablas; 3FN borra `estado_envio` de `PEDIDO`.
2. **Data Modeler** (10 min): borrar el atributo `estado_envio` del `PEDIDO` logico (se borra solo en la
   tabla relacional al regenerar) y crear la restriccion unica sobre `SUMINISTRO_id_suministro`.
3. **Generate DDL** y agregar IDENTITY / DEFAULT / CHECK / auditoria (o definirlos en Data Modeler antes
   de generar).
4. **SSMS**: crear la base con el script nuevo y sacar el diagrama fisico actualizado.
5. **MER**: borrar `Estado_envio`, subrayar PK, agregar `(1,1)` y la nota del suministro unico.
6. **PDF**: portada + tabla de respuesta + lamina de la regla del suministro unico + una lamina por
   modelo (conceptual, logico, relacional y fisico).
