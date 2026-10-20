# GUÍA 02: NIVEL LÓGICO Y RELACIONAL EN ORACLE SQL DEVELOPER DATA MODELER — PROYECTO NIKE INC. (GRUPO 5)

**Curso:** Diseño de Base de Datos Relacionales (IDAT)  
**Integrantes:** Daniel Asmat | Salomón Fernández | Luis Coloma | Pablo Rios

---

## 1. PASO DE M.E.R. CONCEPTUAL A MODELO LÓGICO (9 ENTIDADES)

En **Oracle SQL Developer Data Modeler** (pestaña **`Logical`**, cajas celestes), las 6 entidades fuertes del M.E.R. se mantienen y las **3 relaciones muchos a muchos `(N,M)`** (`CONTIENE`, `ALMACENA` y `SUMINISTRA`) se transforman en **3 entidades asociativas/intermedias** (`DETALLE_VENTA`, `STOCK_ALMACEN` y `SUMINISTRO_LOCAL`), dando un total de **9 cajas celestes**:

### Tabla exacta de configuración de Atributos en el Modelo Lógico

| Entidad | Atributo | Tipo Lógico | Tamaño / Precisión | Escala (`Scale`) | Clave / Obligatorio |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **`CLIENTE`** | `id_cliente` | `Integer` | - | - | **`P *`** (`Primary UID`) |
| | `nombre` | `VARCHAR` | `100` | - | **`*`** (`Mandatory`) |
| | `correo_e` | `VARCHAR` | `100` | - | **`*`** (`Mandatory`) |
| | `telefono` | `VARCHAR` | `20` | - | **`*`** (`Mandatory`) |
| | `direccion` | `VARCHAR` | `200` | - | **`*`** (`Mandatory`) |
| **`PEDIDO`** | `id_pedido` | `Integer` | - | - | **`P *`** (`Primary UID`) |
| | `fecha` | `Datetime` / `Date` | - | - | **`*`** (`Mandatory`) |
| | `metodo_pago` | `VARCHAR` | `40` | - | **`*`** (`Mandatory`) |
| | `igv` | `DECIMAL` | `10` | **`2`** | **`*`** (`Mandatory`) |
| | `estado_envio` | `VARCHAR` | `30` | - | **`*`** (`Mandatory`) |
| **`DETALLE_VENTA`** | `id_detalle` | `Integer` | - | - | **`P *`** (`Primary UID`) |
| | `talla_elegida` | `VARCHAR` | `15` | - | **`*`** (`Mandatory`) |
| | `cantidad` | `Integer` | - | - | **`*`** (`Mandatory`) |
| | `precio_unitario_aplicado` | `DECIMAL` | `10` | **`2`** | **`*`** (`Mandatory`) |
| | `total` | `DECIMAL` | `10` | **`2`** | **`*`** (`Mandatory`) |
| **`CATEGORIA`** | `id_categoria` | `Integer` | - | - | **`P *`** (`Primary UID`) |
| | `nombre` | `VARCHAR` | `50` | - | **`*`** (`Mandatory`) |
| | `descripcion` | `VARCHAR` | `150` | - | Opcional (sin `*`) |
| **`PRODUCTO`** | `id_producto` | `Integer` | - | - | **`P *`** (`Primary UID`) |
| | `nombre` | `VARCHAR` | `120` | - | **`*`** (`Mandatory`) |
| | `especificaciones` | `VARCHAR` | `255` | - | Opcional (sin `*`) |
| | `precio_unitario_base` | `DECIMAL` | `10` | **`2`** | **`*`** (`Mandatory`) |
| | `estado` | `VARCHAR` | `20` | - | **`*`** (`Mandatory`) |
| **`ALMACEN`** | `id_almacen` | `Integer` | - | - | **`P *`** (`Primary UID`) |
| | `nombre_almacen` | `VARCHAR` | `50` | - | **`*`** (`Mandatory`) |
| | `ubicacion` | `VARCHAR` | `100` | - | **`*`** (`Mandatory`) |
| **`STOCK_ALMACEN`** | `talla` | `VARCHAR` | `15` | - | **`P *`** (`Primary UID`) |
| | `color` | `VARCHAR` | `40` | - | **`P *`** (`Primary UID`) |
| | `stock_actual` | `Integer` | - | - | **`*`** (`Mandatory`) |
| | `stock_minimo` | `Integer` | - | - | **`*`** (`Mandatory`) |
| **`LOCAL`** | `id_local` | `Integer` | - | - | **`P *`** (`Primary UID`) |
| | `nombre_local` | `VARCHAR` | `50` | - | **`*`** (`Mandatory`) |
| | `direccion_local` | `VARCHAR` | `150` | - | **`*`** (`Mandatory`) |
| **`SUMINISTRO_LOCAL`** | `fecha_suministro` | `Date` | - | - | **`P *`** (`Primary UID`) |
| | `estado_despacho` | `VARCHAR` | `30` | - | Opcional (sin `*`) |

---

## 2. CONFIGURACIÓN DE LAS 8 RELACIONES EN EL MODELO LÓGICO

1. **`CLIENTE` (1) ──> `PEDIDO` (N):** Relación `1:N` no identificadora (`Suprimir Regla: RESTRICT`). Crea `CLIENTE_id_cliente` (`F *`) en `PEDIDO`.
2. **`PEDIDO` (1) ──> `DETALLE_VENTA` (N):** Relación `1:N` no identificadora (`Suprimir Regla: RESTRICT`). Crea `PEDIDO_id_pedido` (`F *`) en `DETALLE_VENTA`.
3. **`PRODUCTO` (1) ──> `DETALLE_VENTA` (N):** Relación `1:N` no identificadora (`Suprimir Regla: RESTRICT`). Crea `PRODUCTO_id_producto` (`F *`) en `DETALLE_VENTA`.
4. **`CATEGORIA` (1) ──> `PRODUCTO` (N):** Relación `1:N` no identificadora (`Suprimir Regla: RESTRICT`). Crea `CATEGORIA_id_categoria` (`F *`) en `PRODUCTO`.
5. **`ALMACEN` (1) ──> `STOCK_ALMACEN` (N):** Relación `1:N` **IDENTIFICADORA** (casilla **`Identificar` / `Identifying` marcada**). Crea `ALMACEN_id_almacen` (**`PF *`**) en `STOCK_ALMACEN`.
6. **`PRODUCTO` (1) ──> `STOCK_ALMACEN` (N):** Relación `1:N` **IDENTIFICADORA** (casilla **`Identificar` / `Identifying` marcada**). Crea `PRODUCTO_id_producto` (**`PF *`**) en `STOCK_ALMACEN`.
7. **`ALMACEN` (1) ──> `SUMINISTRO_LOCAL` (N):** Relación `1:N` **IDENTIFICADORA** (casilla **`Identificar` / `Identifying` marcada**). Crea `ALMACEN_id_almacen` (**`PF *`**) en `SUMINISTRO_LOCAL`.
8. **`LOCAL` (1) ──> `SUMINISTRO_LOCAL` (N):** Relación `1:N` **IDENTIFICADORA** (casilla **`Identificar` / `Identifying` marcada**). Crea `LOCAL_id_local` (**`PF *`**) en `SUMINISTRO_LOCAL`.

---

## 3. INGENIERÍA AL MODELO RELACIONAL (`Engineer to Relational Model >>`) SIN COLUMNAS DUPLICADAS `...1`

* **¿Por qué salían antes columnas terminadas en `1` (`CLIENTE_id_cliente1`, etc.)?**
  Porque si se edita el modelo Lógico y se vuelve a presionar `Engineer to Relational Model (>>)` sobre un `Relational_1` que ya tenía tablas creadas, Data Modeler duplica las llaves foráneas agregándoles un `1` al final.
* **Procedimiento limpio aplicado:**
  1. Ir a `Relational_1`, seleccionar todo (`Ctrl + A`) y eliminar (`Supr`).
  2. Regresar a `Logical` y presionar **`Engineer to Relational Model (>>)`** $ightarrow$ **`Engineer`**.
  3. El modelo Relacional (cajas amarillas) se genera 100% limpio con una sola llave foránea por relación y con las claves primarias compuestas `PF` + `P` en `STOCK_ALMACEN` y `SUMINISTRO_LOCAL`.
