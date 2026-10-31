# Proyecto Parcial - Base de Datos NIKE Inc. (Grupo 5)

Repositorio del proyecto parcial del curso de **Disenio de Base de Datos Relacionales** (IDAT). El modelo abarca el proceso de ventas, pedidos, control de stock en almacenes y suministro a locales fisicos de Nike a nivel nacional en el Peru.

## Integrantes - Grupo 5

- Daniel Asmat
- Salomon Fernandez
- Luis Coloma
- Pablo Rios

**Docente:** Sergio Fernando Castillo Carrion

## Estructura del repositorio

- **`nivel_conceptual/`**: diagrama M.E.R. (notacion Chen) editable en Draw.io (`.drawio`) y exportado en imagen (`.png`), con las PK subrayadas, los atributos opcionales punteados y las flechas de las 1:N apuntando al lado 1.
- **`normalizacion/`**: Excel `NORMALIZACION_BD_NIKE_GRUPO_5.xlsx` con cuatro hojas: `0FN` (tabla general con los productos y cantidades suministradas), `1FN` (un valor por celda), `2FN` (**8 tablas**) y `3FN` (las 10 tablas del modelo).
- **`nivel_logico/`**: proyecto de Oracle SQL Developer Data Modeler (`BD NIKE.Inc.dmd` y su carpeta de modelo) y las laminas **`MODELO_LOGICO.png`** (Barker: solo entidades y relaciones, con verbo y cardinalidad) y **`MODELO_RELACIONAL.png`** (las 10 tablas con las 11 claves foraneas).
- **`nivel_fisico/`**: **`MF_NIKE_INC_CORREGIDO.sql`** (el script que se ejecuta en SQL Server: el DDL de Data Modeler con el `CREATE DATABASE` arreglado y con lo propio del fisico), mas `BD_NIKE_INC_SQL_SERVER.sql`, `BD_NIKE_INC_ORACLE.sql` y la lamina **`MODELO_FISICO.png`**. 10 tablas, 11 claves foraneas, **7 IDENTITY**, **9 DEFAULT** de negocio, **10 CHECK** y **4 campos de auditoria** por tabla; sin vistas ni columnas calculadas.

- **`CUADRO_DE_MODELOS.png`**: lamina de apoyo que resume que cambia en cada nivel (conceptual, logico, relacional y fisico).

- **`DICCIONARIO_DE_DATOS.xlsx`**: diccionario de datos del modelo fisico, generado leyendo `MF_NIKE_INC_CORREGIDO.sql`. Seis hojas: `Resumen`, `Diccionario` (las 88 columnas), `Claves foraneas` (11), `Restricciones` (IDENTITY, DEFAULT y CHECK), `Relaciones` y `Glosario`.
- **`DICCIONARIO_DE_DATOS.md`**: la misma informacion en texto, para leer o citar en el informe.

Las guias de armado estan fuera de esta carpeta, en **`guias/`** (siete guias, `01_...md` a `07_...md`, mas la guia completa `GUIA_PROYECTO_NIKE_GRUPO_5.md`).

## Las 8 relaciones del MER

| Relacion | Cardinalidad | Une |
| :--- | :---: | :--- |
| REALIZA | (1,N) | CLIENTE - PEDIDO |
| CONTIENE | (M,N) | PEDIDO - PRODUCTO |
| CLASIFICA | (1,N) | CATEGORIA - PRODUCTO |
| ALMACENA | (M,N) | PRODUCTO - ALMACEN |
| PROVEE | (1,N) | PEDIDO - SUMINISTRO |
| ABASTECE | (1,N) | ALMACEN - SUMINISTRO |
| RECIBE | (1,N) | LOCAL - SUMINISTRO |
| INCLUYE | (M,N) | SUMINISTRO - PRODUCTO |

## Tablas del modelo (3FN)

1. `CLIENTE`
2. `CATEGORIA`
3. `ALMACEN`
4. `LOCAL`
5. `PRODUCTO`
6. `PEDIDO`
7. `SUMINISTRO`
8. `DETALLE_VENTA`
9. `STOCK_ALMACEN`
10. `DETALLE_SUMINISTRO`

**11 claves foraneas** y **3 columnas opcionales** (`telefono_secundario`, `descripcion`, `especificaciones`). Ninguna tabla guarda valores calculados (`Total` e `IGV` no existen en ningun nivel) y el modelo no necesita vistas. **`ALMACEN` solo se relaciona con `SUMINISTRO` (ABASTECE) y con `PRODUCTO` (ALMACENA)**.

## Correcciones del docente

Las **11 observaciones** escritas en el Excel de normalizacion estan aplicadas en el MER, en el Excel y en el modelo logico, y documentadas en `guias/06_GUIA_CORRECCIONES_DOCENTE.md`.

## Entrega en PDF

**`ENTREGA_MODELOS_NIKE_GRUPO_5.pdf`** (**12 paginas**): respuesta a las observaciones del docente, la regla del suministro unico con la tabla de equivalencia de estados, un extracto del DDL, el **diccionario de datos** (paginas 5, 6 y 7) y una lamina por modelo (conceptual, logico, relacional y fisico), mas el cuadro de paso de un nivel al siguiente.

## Como se regenera todo

```bash
cd /home/user/generadores
python3 mer_final.py && python3 barker.py && python3 relacional.py && python3 fisico.py
python3 cadena.py && python3 sql_final.py && python3 xlsx_final.py
python3 diccionario.py      # diccionario (lee el .sql corregido)
python3 pdf_entrega.py      # PDF de 12 paginas
python3 guias_concat.py     # guia completa a partir de 01..07
```

El nombre de la base es **`NIKE_INC_BD`** y el correo del cliente se llama **`correo_electronico`** (`VARCHAR(80)`) en todos los niveles.

## Revision por niveles

| Nivel | Lamina | Que muestra |
| :--- | :--- | :--- |
| Conceptual (MER) | `nivel_conceptual/Diagrama MER (NIKE) - GRUPO 5.png` | 7 entidades, 8 relaciones, PK subrayadas (tambien la clave compuesta dentro de los rombos M:N); sin `Total` ni `IGV` |
| Logico | `nivel_logico/MODELO_LOGICO.png` | 7 entidades y 8 relaciones con verbo y cardinalidad; las M:N van como relacion (rombo) con sus atributos, no como tabla |
| Relacional | `nivel_logico/MODELO_RELACIONAL.png` | 10 tablas y 11 claves foraneas; las M:N ya resueltas |
| Fisico | `nivel_fisico/MODELO_FISICO.png` | las 10 tablas con IDENTITY, DEFAULT, CHECK y auditoria |

Cada modelo va en su **propia lamina** y las imagenes se entregan a tamano completo (el MER mide 4800 x 3540 px, en fondo blanco).

## Herramientas utilizadas

- **Draw.io** (diagrama M.E.R. conceptual)
- **Microsoft Excel** (proceso de normalizacion 0FN, 1FN, 2FN y 3FN)
- **Oracle SQL Developer Data Modeler** (modelado logico y relacional)
- **SQL Server Management Studio - SSMS** (implementacion fisica y diagrama de base de datos)
