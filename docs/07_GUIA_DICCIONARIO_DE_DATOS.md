# GUIA 7: DICCIONARIO DE DATOS Y CIERRE DE LA ENTREGA

**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios
**Curso:** Disenio de Bases de Datos Relacionales - IDAT
**Docente:** Sergio Fernando Castillo Carrion

---

**Archivos que produce esta guia:**

| Archivo | Donde esta | Que es |
| :--- | :--- | :--- |
| `DICCIONARIO_DE_DATOS.xlsx` | `proyecto_parcial/` | Diccionario completo, seis hojas, listo para entregar |
| `DICCIONARIO_DE_DATOS.md` | `proyecto_parcial/` | La misma informacion en texto, para leer o pegar en el informe |
| `ENTREGA_MODELOS_NIKE_GRUPO_5.pdf` | `proyecto_parcial/` | PDF de entrega: **12 paginas**, con el diccionario en las paginas 5, 6 y 7 |

---

## 1. Que es un diccionario de datos y por que lo piden

El **modelo fisico** dice *como* esta hecha la base: tablas, tipos y restricciones. El **diccionario de datos** dice *que significa* cada cosa: para que existe cada columna, que valores acepta, quien la llena y que regla la protege.

Son dos documentos distintos y el segundo no se puede inventar de memoria: tiene que describir **exactamente** la base que se ejecuto. Por eso el diccionario de este proyecto **no se escribe a mano**: se genera leyendo el script `nivel_fisico/MF_NIKE_INC_CORREGIDO.sql`.

```
MF_NIKE_INC_CORREGIDO.sql  --->  generadores/diccionario.py  --->  DICCIONARIO_DE_DATOS.xlsx
   (la base real)                                                  DICCIONARIO_DE_DATOS.md
                                                                   (paginas 5-7 del PDF)
```

Consecuencia practica: **si cambias el script, vuelve a generar el diccionario**. Si no, el documento empieza a mentir (por ejemplo, sigue mostrando una columna que ya se borro).

---

## 2. Las seis hojas del Excel

| # | Hoja | Que muestra | Para que sirve en la exposicion |
| :---: | :--- | :--- | :--- |
| 1 | **Resumen** | Datos del grupo, motor, **cifras del modelo** (10 tablas, 88 columnas, 7 `IDENTITY`, 9 `DEFAULT` de negocio, 10 `CHECK`, 11 FK, 3 columnas opcionales, 0 vistas) y las **convenciones de nombres**. | Abre la conversacion: "esta es la base, estas son sus cifras". |
| 2 | **Diccionario** | Las **88 columnas** una por una: tabla, columna, tipo, `NULL`, clave (`PK` / `FK` / `PK + FK`), referencia, `IDENTITY`, `DEFAULT` y **descripcion de negocio**. | Es la hoja que se consulta cuando preguntan por una columna concreta. |
| 3 | **Claves foraneas** | Las **11 FK** con tabla hija, columna, tabla padre, columna referenciada y la regla de negocio. | Demuestra que las relaciones del MER estan implementadas. |
| 4 | **Restricciones** | Los **7 `IDENTITY`**, los **9 `DEFAULT`** de negocio y los **10 `CHECK`**, cada uno con su justificacion. | Es la prueba de lo que el docente califico en el fisico. |
| 5 | **Relaciones** | Las **8 relaciones** del MER con su cardinalidad y su lectura en palabras. | Conecta el conceptual con el fisico. |
| 6 | **Glosario** | `MER`, `PK`, `FK`, clave compuesta, `IDENTITY`, `DEFAULT`, `CHECK`, suministro, detalle, `Total`/`IGV`. | Evita que cada integrante explique distinto. |

Las **4 columnas de auditoria** (`usuario_creacion`, `fecha_creacion`, `usuario_modificacion`, `fecha_modificacion`) se repiten igual en las 10 tablas. En el Excel aparecen en gris al final de cada tabla; en el PDF y en el `.md` se explican **una sola vez** para no repetir la misma fila 40 veces.

---

## 3. Como se lee una fila del diccionario

Ejemplo real (hoja `Diccionario`):

| Tabla | Columna | Tipo | NULL | Clave | Referencia | IDENTITY | DEFAULT | Descripcion |
| :--- | :--- | :--- | :---: | :---: | :--- | :---: | :--- | :--- |
| PEDIDO | `SUMINISTRO_id_suministro` | `INT` | No | FK | `SUMINISTRO.id_suministro` | - | - | Suministro que atiende el pedido. Una sola columna obligatoria: por eso un pedido se atiende con un unico suministro. |
| DETALLE_VENTA | `cantidad` | `INT` | No | - | - | - | `1` | Unidades vendidas de ese producto, talla y color. Debe ser mayor que cero. |
| CLIENTE | `telefono_secundario` | `VARCHAR(15)` | **Si** | - | - | - | - | Celular alterno. Es opcional: hay clientes que solo dejan un numero. |
| CLIENTE | `id_cliente` | `INT` | No | PK | - | **Si** | - | Codigo unico del comprador. Lo genera la base. |

Como se leen las marcas:

* **`PK`**: identifica la fila. **`PK + FK`**: forma parte de una clave compuesta y ademas apunta a otra tabla (pasa en las tres tablas de detalle).
* **`NULL = Si`**: la unica forma en que una columna puede quedar vacia. En este modelo son solo tres.
* **`IDENTITY = Si`**: el valor no se escribe, lo genera SQL Server.
* **`DEFAULT`**: lo que la base pone sola si el `INSERT` no manda ese dato.

---

## 4. Las cifras oficiales del modelo

Estos son los numeros que hay que decir, y son los mismos en el diccionario, en el PDF, en el README y en las guias:

| Concepto | Numero | Donde se comprueba |
| :--- | :---: | :--- |
| Tablas | **10** | `SELECT COUNT(*) FROM sys.tables;` |
| Columnas | **88** (48 de negocio + 40 de auditoria) | hoja `Diccionario` |
| Claves primarias simples con `IDENTITY` | **7** | `WHERE c.is_identity = 1` |
| Claves primarias compuestas | **3** | `DETALLE_VENTA`, `STOCK_ALMACEN`, `DETALLE_SUMINISTRO` |
| Claves foraneas | **11** | `SELECT COUNT(*) FROM sys.foreign_keys;` |
| Restricciones `CHECK` | **10** | `SELECT COUNT(*) FROM sys.check_constraints;` |
| `DEFAULT` de negocio | **9** | `SELECT * FROM sys.default_constraints;` |
| Columnas que admiten `NULL` | **3** | `telefono_secundario`, `descripcion`, `especificaciones` |
| Vistas | **0** | `SELECT COUNT(*) FROM sys.views;` |
| Relaciones del MER | **8** | `REALIZA`, `CONTIENE`, `CLASIFICA`, `ALMACENA`, `PROVEE`, `ABASTECE`, `RECIBE`, `INCLUYE` |

---

## 5. Como se regenera (si cambia el script)

```bash
cd /home/user/generadores
python3 diccionario.py          # vuelve a leer el .sql y reescribe el xlsx, el md y el json
python3 pdf_entrega.py          # rehace el PDF con las paginas nuevas del diccionario
```

`diccionario.py` no guarda datos a mano: recorre el script y arma la estructura con expresiones regulares sobre:

* `CREATE TABLE` → nombre de tabla, columnas, tipos, `NULL`, `IDENTITY`, `DEFAULT`;
* `CONSTRAINT ... PRIMARY KEY` → clave primaria (simple o compuesta);
* `CONSTRAINT CK_... CHECK (...)` → validaciones (soporta las que ocupan dos lineas, como `CK_CLIENTE_TELEFONO`);
* `ALTER TABLE ... FOREIGN KEY` → las 11 claves foraneas.

Las **descripciones de negocio** si son texto escrito por el grupo (un diccionario tecnico no puede deducir para que sirve un `precio_unitario_aplicado`). Estan en el diccionario `DESC` al inicio de `diccionario.py`, y se pueden editar sin tocar nada mas.

---

## 6. Checklist antes de entregar

**Diccionario**

1. Abrir `DICCIONARIO_DE_DATOS.xlsx` y revisar que la hoja `Resumen` diga **10 tablas / 11 FK / 7 IDENTITY / 9 DEFAULT / 10 CHECK**.
2. Buscar en la hoja `Diccionario` las palabras **`total`**, **`igv`** y **`estado_envio`**: no debe aparecer ninguna como columna.
3. Confirmar que las **3 columnas opcionales** son las mismas del modelo (`telefono_secundario`, `descripcion`, `especificaciones`).
4. Confirmar que las 3 tablas de detalle muestran **`PK + FK`** y no llevan `IDENTITY`.

**Coherencia con los otros entregables**

5. El nombre de la base coincide en todos lados: **`NIKE_INC_BD`**.
6. El nombre del correo coincide en todos lados: **`correo_electronico`** (`VARCHAR(80)`).
7. Las longitudes del diccionario coinciden con el modelo relacional y con la GUIA 5.
8. Las 8 relaciones y sus cardinalidades coinciden con el MER y con el logico (`PROVEE` es `1:N`).

**PDF**

9. El PDF debe tener **12 paginas**: portada, respuestas al docente, regla del suministro, extracto del DDL, **diccionario (5, 6 y 7)**, y las cuatro laminas mas el cuadro final.
10. Las laminas van a tamano completo, una por pagina.

---

## 7. Que decir al presentar el diccionario

> *"El diccionario de datos esta generado a partir del script que realmente ejecutamos en SQL Server, no escrito aparte. Tiene seis hojas: el resumen con las cifras del modelo, las 88 columnas con su tipo y su significado, las 11 claves foraneas, las restricciones -- siete `IDENTITY`, nueve `DEFAULT` y diez `CHECK` --, las ocho relaciones con su cardinalidad y un glosario. Por eso cualquier pregunta sobre una columna se responde con este archivo, y cualquier cambio en el script obliga a regenerarlo para que no queden desalineados."*
