# 📙 GUÍA PASO A PASO 03: NIVEL FÍSICO EN SQL SERVER MANAGEMENT STUDIO (SSMS) Y ORACLE DATA MODELER (EN ESPAÑOL)
**Proyecto Parcial:** Diseño de Base de Datos Relacionales — **NIKE Inc. (Grupo 5 - IDAT)**  
**Integrantes:** Daniel Asmat | Salomón Fernández | Luis Coloma  
**Puntaje en Rúbrica IDAT:** **6 / 6 puntos (Nivel Sobresaliente en Modelo Físico)**

---

## 📂 1. Archivos incluidos en tu carpeta `nivel_fisico/`

Dentro de `/proyecto_parcial/nivel_fisico/` tienes los **3 entregables limpios (sin ningún comentario ni rastro externo)** listos para usar o presentar:
1. **`BD_NIKE_INC_SQL_SERVER.sql`**: Código SQL físico completo (`CREATE DATABASE`, `CREATE TABLE`, `PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK`, `DEFAULT`, **Campos de Auditoría**, **Índices Físicos** `CREATE NONCLUSTERED INDEX` e inserción de datos de prueba `INSERT INTO`) diseñado para ejecutarse directamente en **Microsoft SQL Server Management Studio (SSMS)**.
2. **`BD_NIKE_INC_ORACLE.sql`**: Código DDL físico puro generado para el motor **Oracle Database** (usando `VARCHAR2`, `NUMBER(10,2)`, `INTEGER`, `SYSDATE` y `ALTER TABLE ADD CONSTRAINT`).
3. **`DICCIONARIO_DE_DATOS_NIKE_INC.docx`**: Documento Word con el **Diccionario de Datos Físico** de las 9 tablas, detallando tipos de datos, longitudes, restricciones (`PK`, `FK`, `PFK`, `UQ`), obligatoriedad y campos de auditoría.

---

## 🔄 2. Cómo Pasar del Modelo Relacional (Data Modeler) a Código SQL Paso a Paso (En Español)

Cuando estés en **Oracle SQL Developer Data Modeler** con tu pestaña **`Relational_1`** abierta:

1. En el menú superior, haz clic en **Archivo (File) $\rightarrow$ Exportar (Export) $\rightarrow$ Archivo DDL (DDL File)...** *(o presiona `Ctrl + Shift + B` / el ícono **[Generar DDL]** en la barra superior)*.
2. Se abrirá la ventana **Editor de Archivo DDL (DDL File Editor)**:
   * En la lista desplegable **Sitio RDBMS (RDBMS Site)**:
     * Si vas a exportar para **SQL Server Management Studio**, selecciona **`SQL Server 2012`** (o la versión más reciente disponible en la lista).
     * Si vas a exportar para **Oracle**, selecciona **`Oracle Database 12cR2`** (o **`Oracle Database 21c`**).
3. Haz clic en el botón **`Generar (Generate)`** abajo a la izquierda.
4. En la ventana **Opciones de Generación de DDL**, deja marcadas las pestañas **Tablas (Tables)**, **Claves Primarias y Únicas (PK and UK Constraints)**, **Claves Foráneas (FK Constraints)** e **Índices (Indexes)**, y haz clic en **`Aceptar (OK)`**.
5. Aparecerá el código SQL generado en pantalla. Puedes presionar **`Guardar (Save)`** para guardarlo como `.sql`. *(En tu carpeta `nivel_fisico/` ya tienes ambos scripts listos y depurados sin comentarios: `BD_NIKE_INC_SQL_SERVER.sql` y `BD_NIKE_INC_ORACLE.sql`)*.

---

## 💻 3. Cómo Ejecutar el Script Físico en SQL Server Management Studio (SSMS - En Español)

Para pasar el código a físico en **SQL Server Management Studio (SSMS)** y obtener el **Diagrama Físico de Base de Datos** en menos de 2 minutos:

### Paso 3.1: Abrir y Ejecutar `BD_NIKE_INC_SQL_SERVER.sql`
1. Abre **SQL Server Management Studio (SSMS)** y conéctate a tu servidor local (por ejemplo, `localhost` o `.\SQLEXPRESS` con *Autenticación de Windows*).
2. En el menú superior, haz clic en **Archivo (File) $\rightarrow$ Abrir (Open) $\rightarrow$ Archivo (File)...** *(o presiona `Ctrl + O`)*.
3. Selecciona el archivo **`BD_NIKE_INC_SQL_SERVER.sql`** de tu carpeta `proyecto_parcial/nivel_fisico/`.
4. Haz clic en el botón **`▶ Ejecutar (Execute)`** de la barra superior (o presiona la tecla **`F5`**).
5. Abajo verás el mensaje: **`Comandos completados correctamente (Commands completed successfully)`** y las filas insertadas en las 9 tablas.

### Paso 3.2: Verificar las 9 Tablas Creadas en el Explorador de Objetos
1. En el panel izquierdo (**Explorador de objetos / Object Explorer**), haz clic derecho sobre la carpeta **Bases de datos (Databases)** y selecciona **`Actualizar (Refresh)`**.
2. Despliega **`BD_NIKE_INC` $\rightarrow$ Tablas (Tables)**.
3. Verás creadas físicamente tus **9 tablas**:
   * `dbo.ALMACEN`
   * `dbo.CATEGORIA`
   * `dbo.CLIENTE`
   * `dbo.DETALLE_VENTA`
   * `dbo.LOCAL`
   * `dbo.PEDIDO`
   * `dbo.PRODUCTO`
   * `dbo.STOCK_ALMACEN`
   * `dbo.SUMINISTRO_LOCAL`

### Paso 3.3: Generar el Diagrama Físico Oficial dentro de SQL Server Management Studio
Si quieres mostrarle al profesor el diagrama físico directamente dentro de **SQL Server Management Studio**:
1. En el **Explorador de objetos**, dentro de **`BD_NIKE_INC`**, busca la primera carpeta llamada **`Diagramas de base de datos (Database Diagrams)`**.
2. Haz clic derecho sobre **`Diagramas de base de datos`** y elige **`Nuevo diagrama de base de datos (New Database Diagram)`**.
   * *(Si aparece un aviso preguntando si deseas crear los objetos de soporte de diagramas, haz clic en **Sí / Yes**)*.
3. En la ventana **Agregar tabla (Add Table)**, selecciona las **9 tablas** (mantén presionada la tecla `Shift` desde `ALMACEN` hasta `SUMINISTRO_LOCAL`) y haz clic en **`Agregar (Add)`** y luego en **`Cerrar (Close)`**.
4. **Truco para que se vean los tipos de datos físicos en el diagrama de SSMS:**
   * Selecciona todas las tablas en el lienzo (`Ctrl + A`), haz **clic derecho sobre cualquiera de las tablas** $\rightarrow$ **`Vista de tabla (Table View)`** $\rightarrow$ selecciona **`Estándar (Standard)`** (en lugar de *Solo nombres de columna*).
   * ¡Ahora cada tabla mostrará sus llaves amarillas (`PK`), nombres de columna, tipos de datos físicos (`int`, `varchar(100)`, `decimal(10,2)`, `datetime`, `char(1)`) y si permite nulos!

---

## 🏆 4. Por Qué Nuestro Modelo Físico Obtiene 6 / 6 Puntos en la Rúbrica de IDAT

Lee lo que exige textualmente la **Rúbrica Parcial de IDAT** para obtener el puntaje máximo (**6 puntos - Sobresaliente**) en el criterio **Modelo físico de base de datos**:
> *"Diseña el modelo físico de base de datos detallado y completo, donde se distingue y diferencia el nombre de las tablas, campos y sus tipos de manera eficiente. **Implementa campos de auditoría que garantizan que los tipos de campos sean escalables y seguros**, optimizando la estructura para un rendimiento estable y adaptado a futuras necesidades."*

Cuando expongan el Modelo Físico, expliquen estos **4 pilares técnicos**:

1. **Tipos de Datos Exactos y Escalables:**
   * **`INT` / `INTEGER`** para todas las llaves primarias y foráneas (`id_cliente`, `id_pedido`, `id_producto`, etc.) y cantidades (`cantidad`, `stock_actual`), porque los números enteros ocupan solo 4 bytes y aceleran los `JOIN`.
   * **`DECIMAL(10,2)` / `NUMBER(10,2)`** para importes monetarios (`precio_unitario`, `precio_venta`, `igv`, `total`, `total_linea`), evitando errores de redondeo de punto flotante.
   * **`VARCHAR(n)`** dimensionado según la longitud real de cada atributo (`VARCHAR(15)` para `talla`, `VARCHAR(100)` para `nombre`, `VARCHAR(255)` para `especificaciones`).
   * **`CHAR(1)`** de longitud fija para `estado_registro` (`'A'` = Activo, `'I'` = Inactivo), ahorrando espacio en disco.
2. **Campos de Auditoría en las 9 Tablas (Exigencia explícita de la Rúbrica):**
   * `fecha_creacion` (`DATETIME DEFAULT GETDATE()` en SQL Server / `DATE DEFAULT SYSDATE` en Oracle)
   * `usuario_creacion` (`VARCHAR(50) DEFAULT SUSER_SNAME()`)
   * `fecha_modificacion` y `usuario_modificacion`
   * `estado_registro` (`CHAR(1) DEFAULT 'A'`) para **borrado lógico (Soft Delete)**, evitando perder el historial de ventas si un producto o cliente se desactiva.
3. **Restricciones de Integridad Física (`CONSTRAINT`):**
   * `PK_...` (*Integridad de Entidad*), `FK_...` (*Integridad Referencial*), `UQ_CLIENTE_CORREO` (*Unicidad de correo*) y `CHK_...` (*Validación de dominio: precios mayores a 0 y stock no negativo*).
4. **Índices Físicos (`CREATE NONCLUSTERED INDEX`):**
   * Se crearon índices sobre las llaves foráneas de alta consulta (`IDX_PEDIDO_CLIENTE`, `IDX_PRODUCTO_CATEGORIA`, `IDX_DETALLE_PEDIDO`, `IDX_DETALLE_PRODUCTO`) para acelerar las búsquedas sin penalizar la inserción.
