# Diccionario de datos | BD NIKE Inc. - Grupo 05

Documento de referencia del **modelo fisico** entregado. Se genera leyendo `nivel_fisico/MF_NIKE_INC_CORREGIDO.sql`, asi que lo que dice aqui es exactamente lo que existe en SQL Server despues de ejecutar el script.

| Dato | Valor |
| :--- | :--- |
| Curso | Disenio de Bases de Datos Relacionales - IDAT |
| Docente | Sergio Fernando Castillo Carrion |
| Integrantes | Daniel Asmat, Salomon Fernandez, Luis Coloma, Pablo Rios |
| Motor | Microsoft SQL Server |
| Base de datos | `NIKE_INC_BD` |
| Tablas | 10 |
| Columnas totales | 88 (de negocio: 48, de auditoria: 40) |
| Claves foraneas | 11 |
| Claves primarias | 7 simples con `IDENTITY` + 3 compuestas |
| Restricciones `CHECK` | 10 |
| Columnas que admiten NULL | 3 (`telefono_secundario`, `descripcion`, `especificaciones`) |
| Vistas | 0 |

## Como leer el diccionario

| Columna | Significado |
| :--- | :--- |
| **Clave** | `PK` = clave primaria, `FK` = clave foranea, `PK + FK` = forma parte de la clave compuesta y ademas apunta a otra tabla. |
| **Admite NULL** | `No` = obligatorio; `Si` = opcional. |
| **DEFAULT** | Valor que pone la base cuando el `INSERT` no envia el dato. |
| **Descripcion** | Que guarda la columna, en lenguaje del negocio. |

Las cuatro columnas de auditoria (`usuario_creacion`, `fecha_creacion`, `usuario_modificacion`, `fecha_modificacion`) se repiten igual en las 10 tablas; en cada tabla se listan al final y no se vuelven a explicar.

## 1. Resumen de tablas

| # | Tabla | Rol | Columnas | Clave primaria | Proposito |
| :---: | :--- | :--- | :---: | :--- | :--- |
| 1 | `CLIENTE` | Maestra | 10 | `id_cliente` | Comprador que realiza pedidos. |
| 2 | `CATEGORIA` | Maestra | 7 | `id_categoria` | Linea comercial que clasifica los productos. |
| 3 | `ALMACEN` | Maestra | 7 | `id_almacen` | Centro de distribucion que guarda stock y abastece locales. |
| 4 | `LOCAL` | Maestra | 7 | `id_local` | Tienda fisica que recibe mercaderia. |
| 5 | `PRODUCTO` | Maestra | 10 | `id_producto` | Catalogo de modelos de Nike. |
| 6 | `PEDIDO` | Transaccional | 9 | `id_pedido` | Cabecera de la venta: cliente, fecha, pago y suministro que la atiende. |
| 7 | `SUMINISTRO` | Transaccional | 9 | `id_suministro` | Despacho de un almacen a un local, con su estado. |
| 8 | `STOCK_ALMACEN` | Detalle | 10 | `talla`, `color`, `PRODUCTO_id_producto`, `ALMACEN_id_almacen` | Unidades por producto, talla y color en cada almacen. |
| 9 | `DETALLE_VENTA` | Detalle | 10 | `talla_elegida`, `color_elegido`, `PEDIDO_id_pedido`, `PRODUCTO_id_producto` | Lineas vendidas: producto, talla, color, cantidad y precio aplicado. |
| 10 | `DETALLE_SUMINISTRO` | Detalle | 9 | `color`, `PRODUCTO_id_producto`, `SUMINISTRO_id_suministro`, `talla` | Lineas despachadas: producto, talla, color y cantidad. |

## 2. Diccionario por tabla

### CLIENTE  (maestra)

*Comprador que realiza pedidos.*

Clave primaria: `id_cliente`  (simple, con `IDENTITY(1,1)`)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `id_cliente` | `INT` | No | PK | - | - | Codigo unico del comprador. Lo genera la base (IDENTITY). |
| `nombre` | `VARCHAR(80)` | No | - | - | - | Nombre y apellido del cliente que compra en tienda o en linea. |
| `correo_electronico` | `VARCHAR(80)` | No | - | - | - | Correo de contacto; es el dato por donde llega la boleta y el aviso de despacho. |
| `telefono` | `VARCHAR(15)` | No | - | - | - | Celular principal, solo digitos (9 en Peru). |
| `telefono_secundario` | `VARCHAR(15)` | Si | - | - | - | Celular o fijo alterno. Es opcional: hay clientes que solo dejan un numero. |
| `direccion` | `VARCHAR(120)` | No | - | - | - | Direccion de entrega con distrito y referencia, a nivel nacional. |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

Validaciones (`CHECK`):

- `CK_CLIENTE_CORREO`: `correo_electronico LIKE '%_@_%._%'`
- `CK_CLIENTE_TELEFONO`: `telefono NOT LIKE '%[^0-9]%' AND LEN(telefono) BETWEEN 6 AND 15)`

### CATEGORIA  (maestra)

*Linea comercial que clasifica los productos.*

Clave primaria: `id_categoria`  (simple, con `IDENTITY(1,1)`)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `id_categoria` | `INT` | No | PK | - | - | Codigo unico de la linea comercial. Lo genera la base (IDENTITY). |
| `nombre` | `VARCHAR(50)` | No | - | - | - | Nombre de la linea comercial: Calzado Running, Calzado Urbano, Indumentaria Deportiva. |
| `descripcion` | `VARCHAR(150)` | Si | - | - | - | Detalle breve de que productos entran en la linea. Es opcional. |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

### ALMACEN  (maestra)

*Centro de distribucion que guarda stock y abastece locales.*

Clave primaria: `id_almacen`  (simple, con `IDENTITY(1,1)`)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `id_almacen` | `INT` | No | PK | - | - | Codigo unico del centro de distribucion. Lo genera la base (IDENTITY). |
| `nombre_almacen` | `VARCHAR(50)` | No | - | - | - | Nombre del centro de distribucion: CD Lima Norte, CD Trujillo Norte. |
| `ubicacion` | `VARCHAR(120)` | No | - | - | - | Direccion o zona donde opera el centro de distribucion. |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

### LOCAL  (maestra)

*Tienda fisica que recibe mercaderia.*

Clave primaria: `id_local`  (simple, con `IDENTITY(1,1)`)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `id_local` | `INT` | No | PK | - | - | Codigo unico de la tienda fisica. Lo genera la base (IDENTITY). |
| `nombre_local` | `VARCHAR(50)` | No | - | - | - | Nombre comercial de la tienda: Nike Store Jockey Plaza, Mall Arequipa, Mallplaza Trujillo. |
| `direccion_local` | `VARCHAR(120)` | No | - | - | - | Direccion de la tienda que recibe la mercaderia. |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

### PRODUCTO  (maestra)

*Catalogo de modelos de Nike.*

Clave primaria: `id_producto`  (simple, con `IDENTITY(1,1)`)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `id_producto` | `INT` | No | PK | - | - | Codigo unico del modelo (SKU). Lo genera la base (IDENTITY). |
| `nombre` | `VARCHAR(80)` | No | - | - | - | Nombre comercial del modelo: Air Zoom Pegasus 40, Air Force 1, Dri-FIT Academy. |
| `especificaciones` | `VARCHAR(150)` | Si | - | - | - | Material, tecnologia y detalles del modelo. Es opcional. |
| `precio_unitario_base` | `DECIMAL(10,2)` | No | - | - | - | Precio de lista en soles, sin IGV ni descuentos. Nunca se guarda un total. |
| `estado` | `VARCHAR(20)` | No | - | - | `'DISPONIBLE'` | Situacion comercial del modelo: DISPONIBLE, AGOTADO o DESCONTINUADO. |
| `CATEGORIA_id_categoria` | `INT` | No | FK | `CATEGORIA.id_categoria` | - | Linea comercial a la que pertenece el modelo (FK a CATEGORIA). |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

Validaciones (`CHECK`):

- `CK_PRODUCTO_PRECIO`: `precio_unitario_base > 0`
- `CK_PRODUCTO_ESTADO`: `estado IN ('DISPONIBLE', 'AGOTADO', 'DESCONTINUADO'))`

### PEDIDO  (transaccional)

*Cabecera de la venta: cliente, fecha, pago y suministro que la atiende.*

Clave primaria: `id_pedido`  (simple, con `IDENTITY(1,1)`)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `id_pedido` | `INT` | No | PK | - | - | Codigo unico de la venta. Lo genera la base (IDENTITY). |
| `fecha` | `DATE` | No | - | - | `CAST(GETDATE() AS DATE)` | Dia en que se registro la venta. |
| `metodo_pago` | `VARCHAR(30)` | No | - | - | `'Tarjeta de Credito'` | Forma de pago: Tarjeta de Credito, Yape, Transferencia o Efectivo. |
| `SUMINISTRO_id_suministro` | `INT` | No | FK | `SUMINISTRO.id_suministro` | - | Suministro que atiende el pedido. Una sola columna obligatoria: por eso un pedido se atiende con un unico suministro (FK a SUMINISTRO). |
| `CLIENTE_id_cliente` | `INT` | No | FK | `CLIENTE.id_cliente` | - | Cliente que compra (FK a CLIENTE). |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

### SUMINISTRO  (transaccional)

*Despacho de un almacen a un local, con su estado.*

Clave primaria: `id_suministro`  (simple, con `IDENTITY(1,1)`)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `id_suministro` | `INT` | No | PK | - | - | Codigo unico del despacho de almacen a local. Lo genera la base (IDENTITY). |
| `fecha_suministro` | `DATE` | No | - | - | `CAST(GETDATE() AS DATE)` | Dia en que sale la mercaderia del centro de distribucion. |
| `estado_despacho` | `VARCHAR(20)` | No | - | - | `'PROGRAMADO'` | Como va el traslado: PROGRAMADO, EN RUTA o ENTREGADO. De aqui se deduce el estado del pedido, sin guardarlo dos veces. |
| `ALMACEN_id_almacen` | `INT` | No | FK | `ALMACEN.id_almacen` | - | Almacen que abastece el suministro (FK a ALMACEN). |
| `LOCAL_id_local` | `INT` | No | FK | `LOCAL.id_local` | - | Local que recibe el suministro (FK a LOCAL). |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

Validaciones (`CHECK`):

- `CK_SUMINISTRO_ESTADO`: `estado_despacho IN ('PROGRAMADO', 'EN RUTA', 'ENTREGADO'))`

### STOCK_ALMACEN  (detalle)

*Unidades por producto, talla y color en cada almacen.*

Clave primaria: `talla`, `color`, `PRODUCTO_id_producto`, `ALMACEN_id_almacen`  (compuesta: la combinacion de esas columnas es unica)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `talla` | `VARCHAR(10)` | No | PK | - | - | Talla disponible en el almacen. Forma parte de la clave compuesta. |
| `color` | `VARCHAR(30)` | No | PK | - | - | Color disponible en el almacen. Forma parte de la clave compuesta. |
| `stock_actual` | `INT` | No | - | - | `0` | Unidades que el almacen tiene hoy de esa talla y color. |
| `stock_minimo` | `INT` | No | - | - | `0` | Umbral de reposicion: por debajo se genera un nuevo suministro. |
| `PRODUCTO_id_producto` | `INT` | No | PK + FK | `PRODUCTO.id_producto` | - | Modelo al que corresponde el stock (FK a PRODUCTO). |
| `ALMACEN_id_almacen` | `INT` | No | PK + FK | `ALMACEN.id_almacen` | - | Almacen donde esta el stock (FK a ALMACEN). |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

Validaciones (`CHECK`):

- `CK_STOCK_ALMACEN_ACTUAL`: `stock_actual >= 0`
- `CK_STOCK_ALMACEN_MINIMO`: `stock_minimo >= 0)`

### DETALLE_VENTA  (detalle)

*Lineas vendidas: producto, talla, color, cantidad y precio aplicado.*

Clave primaria: `talla_elegida`, `color_elegido`, `PEDIDO_id_pedido`, `PRODUCTO_id_producto`  (compuesta: la combinacion de esas columnas es unica)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `talla_elegida` | `VARCHAR(10)` | No | PK | - | - | Talla que pidio el cliente en esa linea. Forma parte de la clave compuesta. |
| `color_elegido` | `VARCHAR(30)` | No | PK | - | - | Color que pidio el cliente en esa linea. Forma parte de la clave compuesta. |
| `cantidad` | `INT` | No | - | - | `1` | Unidades vendidas de ese producto, talla y color. Debe ser mayor que cero. |
| `precio_unitario_aplicado` | `DECIMAL(10,2)` | No | - | - | - | Precio cobrado en el momento de la venta (puede tener descuento). No se calcula un total. |
| `PEDIDO_id_pedido` | `INT` | No | PK + FK | `PEDIDO.id_pedido` | - | Pedido al que pertenece la linea (FK a PEDIDO). |
| `PRODUCTO_id_producto` | `INT` | No | PK + FK | `PRODUCTO.id_producto` | - | Modelo vendido (FK a PRODUCTO). |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

Validaciones (`CHECK`):

- `CK_DETALLE_VENTA_CANTIDAD`: `cantidad > 0`
- `CK_DETALLE_VENTA_PRECIO`: `precio_unitario_aplicado > 0)`

### DETALLE_SUMINISTRO  (detalle)

*Lineas despachadas: producto, talla, color y cantidad.*

Clave primaria: `color`, `PRODUCTO_id_producto`, `SUMINISTRO_id_suministro`, `talla`  (compuesta: la combinacion de esas columnas es unica)

| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |
| :--- | :--- | :---: | :---: | :--- | :--- | :--- |
| `talla` | `VARCHAR(10)` | No | PK | - | - | Talla despachada en el suministro. Forma parte de la clave compuesta. |
| `color` | `VARCHAR(30)` | No | PK | - | - | Color despachado en el suministro. Forma parte de la clave compuesta. |
| `cantidad` | `INT` | No | - | - | `1` | Unidades despachadas de ese producto, talla y color. Debe ser mayor que cero. |
| `PRODUCTO_id_producto` | `INT` | No | PK + FK | `PRODUCTO.id_producto` | - | Modelo incluido en el suministro (FK a PRODUCTO). |
| `SUMINISTRO_id_suministro` | `INT` | No | PK + FK | `SUMINISTRO.id_suministro` | - | Suministro al que pertenece la linea (FK a SUMINISTRO). |
| `usuario_creacion` | `VARCHAR(30)` | No | - | - | `SYSTEM_USER` | Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER). |
| `fecha_creacion` | `DATETIME` | No | - | - | `GETDATE()` | Momento del insert. Se llena solo (DEFAULT GETDATE()). |
| `usuario_modificacion` | `VARCHAR(30)` | Si | - | - | - | Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion. |
| `fecha_modificacion` | `DATETIME` | Si | - | - | - | Momento del ultimo cambio. Queda vacio hasta la primera actualizacion. |

Validaciones (`CHECK`):

- `CK_DETALLE_SUMINISTRO_CANTIDAD`: `cantidad > 0)`

## 3. Claves foraneas (11)

| # | Restriccion | Tabla hija | Columna | Tabla padre | Columna referenciada |
| :---: | :--- | :--- | :--- | :--- | :--- |
| 1 | `DETALLE_SUMINISTRO_PRODUCTO_FK` | `DETALLE_SUMINISTRO` | `PRODUCTO_id_producto` | `PRODUCTO` | `id_producto` |
| 2 | `DETALLE_SUMINISTRO_SUMINISTRO_FK` | `DETALLE_SUMINISTRO` | `SUMINISTRO_id_suministro` | `SUMINISTRO` | `id_suministro` |
| 3 | `DETALLE_VENTA_PEDIDO_FK` | `DETALLE_VENTA` | `PEDIDO_id_pedido` | `PEDIDO` | `id_pedido` |
| 4 | `DETALLE_VENTA_PRODUCTO_FK` | `DETALLE_VENTA` | `PRODUCTO_id_producto` | `PRODUCTO` | `id_producto` |
| 5 | `PEDIDO_CLIENTE_FK` | `PEDIDO` | `CLIENTE_id_cliente` | `CLIENTE` | `id_cliente` |
| 6 | `PEDIDO_SUMINISTRO_FK` | `PEDIDO` | `SUMINISTRO_id_suministro` | `SUMINISTRO` | `id_suministro` |
| 7 | `PRODUCTO_CATEGORIA_FK` | `PRODUCTO` | `CATEGORIA_id_categoria` | `CATEGORIA` | `id_categoria` |
| 8 | `STOCK_ALMACEN_ALMACEN_FK` | `STOCK_ALMACEN` | `ALMACEN_id_almacen` | `ALMACEN` | `id_almacen` |
| 9 | `STOCK_ALMACEN_PRODUCTO_FK` | `STOCK_ALMACEN` | `PRODUCTO_id_producto` | `PRODUCTO` | `id_producto` |
| 10 | `SUMINISTRO_ALMACEN_FK` | `SUMINISTRO` | `ALMACEN_id_almacen` | `ALMACEN` | `id_almacen` |
| 11 | `SUMINISTRO_LOCAL_FK` | `SUMINISTRO` | `LOCAL_id_local` | `LOCAL` | `id_local` |

## 4. Relaciones y cardinalidad

| Relacion | Cardinalidad | Une | Regla de negocio |
| :--- | :---: | :--- | :--- |
| `REALIZA` | (1,N) | CLIENTE - PEDIDO | Un cliente realiza muchos pedidos y cada pedido pertenece a un solo cliente. |
| `CONTIENE` | (M,N) | PEDIDO - PRODUCTO | Un pedido contiene muchos productos (con talla, color, cantidad y precio) y un producto aparece en muchos pedidos. |
| `CLASIFICA` | (1,N) | CATEGORIA - PRODUCTO | Una categoria clasifica muchos productos y cada producto tiene una sola categoria. |
| `ALMACENA` | (M,N) | PRODUCTO - ALMACEN | Un almacen almacena muchos productos por talla y color, y un producto esta en varios almacenes. |
| `PROVEE` | (1,N) | PEDIDO - SUMINISTRO | Un suministro provee a muchos pedidos y cada pedido se atiende con un solo suministro. |
| `ABASTECE` | (1,N) | ALMACEN - SUMINISTRO | Un almacen abastece muchos suministros y cada suministro sale de un solo almacen. |
| `RECIBE` | (1,N) | LOCAL - SUMINISTRO | Un local recibe muchos suministros y cada suministro llega a un solo local. |
| `INCLUYE` | (M,N) | SUMINISTRO - PRODUCTO | Un suministro incluye muchos productos (con talla, color y cantidad) y un producto va en muchos suministros. |

> **`PROVEE` es 1:N.** Un suministro atiende muchos pedidos y cada pedido se atiende con un solo suministro. En la base eso se cumple con una sola columna obligatoria (`PEDIDO.SUMINISTRO_id_suministro`); no se agrega `UNIQUE` ni se escribe `(1,1)`.

## 5. Reglas fijas del modelo

1. **Nada calculado:** no existen columnas `Total` ni `IGV`; se obtienen al consultar.
2. **Nada repetido:** `PEDIDO` no guarda `estado_envio`; se lee de `SUMINISTRO.estado_despacho`.
3. **Sin vistas:** el modelo se resuelve con tablas y claves foraneas.
4. **`ALMACEN`** solo se relaciona con `SUMINISTRO` (`ABASTECE`) y con `PRODUCTO` (`ALMACENA`).
5. **Opcionales:** solo `telefono_secundario`, `descripcion` y `especificaciones`.
6. **Auditoria:** las 10 tablas llevan las mismas 4 columnas.
7. **Longitudes justas:** ningun `VARCHAR(255)` por omision.

## 6. Glosario

| Termino | Significado |
| :--- | :--- |
| **MER** | Modelo Entidad-Relacion. Vista conceptual en notacion Chen: entidades, atributos y rombos. |
| **Modelo logico** | Misma informacion en notacion Barker: entidades, verbo de la relacion y cardinalidad. No muestra columnas FK. |
| **Modelo relacional** | Tablas con sus columnas, claves primarias y claves foraneas. Ya se puede leer en SQL. |
| **Modelo fisico** | El script que corre en SQL Server, con IDENTITY, DEFAULT, CHECK y columnas de auditoria. |
| **PK** | Primary Key. Columna o conjunto de columnas que identifica de forma unica una fila. |
| **FK** | Foreign Key. Columna que apunta a la PK de otra tabla y hace cumplir la relacion. |
| **Clave compuesta** | PK formada por varias columnas. Aparece en DETALLE_VENTA, STOCK_ALMACEN y DETALLE_SUMINISTRO. |
| **IDENTITY(1,1)** | La base genera el numero solo: empieza en 1 y sube de 1 en 1. Solo en las 7 PK simples. |
| **DEFAULT** | Valor que la base pone sola cuando el INSERT no envia el dato. |
| **CHECK** | Regla que la base valida en cada INSERT y UPDATE. Si no se cumple, rechaza la fila. |
| **Auditoria** | Cuatro columnas iguales en las 10 tablas que dicen quien creo o cambio la fila y cuando. |
| **Suministro** | Despacho de mercaderia de un centro de distribucion (ALMACEN) a una tienda (LOCAL). |
| **Detalle** | Tabla que resuelve una relacion de muchos a muchos y guarda los datos propios del movimiento. |
| **Talla / Color** | Atributos que convierten un modelo en unidades vendibles; junto con el producto forman la clave del detalle. |
| **Total / IGV** | No existen como columnas: son calculos que se hacen al consultar, no datos que se guarden. |
| **estado_envio** | Columna eliminada en 3FN: el estado del pedido se deduce de SUMINISTRO.estado_despacho. |
