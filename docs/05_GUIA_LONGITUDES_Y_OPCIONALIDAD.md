# GUIA 5: LONGITUDES JUSTAS Y COLUMNAS OPCIONALES

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
