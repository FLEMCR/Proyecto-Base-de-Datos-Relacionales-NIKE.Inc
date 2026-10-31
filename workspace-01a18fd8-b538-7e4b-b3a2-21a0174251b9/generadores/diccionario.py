# -*- coding: utf-8 -*-
"""Diccionario de datos del proyecto NIKE Inc. - Grupo 05.

Se construye LEYENDO el script que realmente se ejecuta en SQL Server
(nivel_fisico/MF_NIKE_INC_CORREGIDO.sql), de modo que el diccionario nunca
puede quedar distinto del modelo fisico entregado.

Salidas:
  * /home/user/proyecto_parcial/DICCIONARIO_DE_DATOS.xlsx   (6 hojas)
  * /home/user/proyecto_parcial/DICCIONARIO_DE_DATOS.md     (version legible)
  * /home/user/generadores/_diccionario.json                (para el PDF)
"""
import json
import re

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

SCRIPT = "/home/user/proyecto_parcial/nivel_fisico/MF_NIKE_INC_CORREGIDO.sql"
XLSX = "/home/user/proyecto_parcial/DICCIONARIO_DE_DATOS.xlsx"
MD = "/home/user/proyecto_parcial/DICCIONARIO_DE_DATOS.md"
JSON = "/home/user/generadores/_diccionario.json"

# --------------------------------------------------------------------------
# Descripcion de negocio de cada columna: (tabla, columna) manda; si no esta,
# se usa la descripcion generica del nombre de la columna.
# --------------------------------------------------------------------------
DESC = {
    ("CLIENTE", "id_cliente"): "Codigo unico del comprador. Lo genera la base (IDENTITY).",
    ("CLIENTE", "nombre"): "Nombre y apellido del cliente que compra en tienda o en linea.",
    ("CLIENTE", "correo_electronico"): "Correo de contacto; es el dato por donde llega la boleta y el aviso de despacho.",
    ("CLIENTE", "telefono"): "Celular principal, solo digitos (9 en Peru).",
    ("CLIENTE", "telefono_secundario"): "Celular o fijo alterno. Es opcional: hay clientes que solo dejan un numero.",
    ("CLIENTE", "direccion"): "Direccion de entrega con distrito y referencia, a nivel nacional.",
    ("CATEGORIA", "id_categoria"): "Codigo unico de la linea comercial. Lo genera la base (IDENTITY).",
    ("CATEGORIA", "nombre"): "Nombre de la linea comercial: Calzado Running, Calzado Urbano, Indumentaria Deportiva.",
    ("CATEGORIA", "descripcion"): "Detalle breve de que productos entran en la linea. Es opcional.",
    ("ALMACEN", "id_almacen"): "Codigo unico del centro de distribucion. Lo genera la base (IDENTITY).",
    ("ALMACEN", "nombre_almacen"): "Nombre del centro de distribucion: CD Lima Norte, CD Trujillo Norte.",
    ("ALMACEN", "ubicacion"): "Direccion o zona donde opera el centro de distribucion.",
    ("LOCAL", "id_local"): "Codigo unico de la tienda fisica. Lo genera la base (IDENTITY).",
    ("LOCAL", "nombre_local"): "Nombre comercial de la tienda: Nike Store Jockey Plaza, Mall Arequipa, Mallplaza Trujillo.",
    ("LOCAL", "direccion_local"): "Direccion de la tienda que recibe la mercaderia.",
    ("PRODUCTO", "id_producto"): "Codigo unico del modelo (SKU). Lo genera la base (IDENTITY).",
    ("PRODUCTO", "nombre"): "Nombre comercial del modelo: Air Zoom Pegasus 40, Air Force 1, Dri-FIT Academy.",
    ("PRODUCTO", "especificaciones"): "Material, tecnologia y detalles del modelo. Es opcional.",
    ("PRODUCTO", "precio_unitario_base"): "Precio de lista en soles, sin IGV ni descuentos. Nunca se guarda un total.",
    ("PRODUCTO", "estado"): "Situacion comercial del modelo: DISPONIBLE, AGOTADO o DESCONTINUADO.",
    ("PRODUCTO", "CATEGORIA_id_categoria"): "Linea comercial a la que pertenece el modelo (FK a CATEGORIA).",
    ("PEDIDO", "id_pedido"): "Codigo unico de la venta. Lo genera la base (IDENTITY).",
    ("PEDIDO", "fecha"): "Dia en que se registro la venta.",
    ("PEDIDO", "metodo_pago"): "Forma de pago: Tarjeta de Credito, Yape, Transferencia o Efectivo.",
    ("PEDIDO", "SUMINISTRO_id_suministro"): "Suministro que atiende el pedido. Una sola columna obligatoria: por eso un pedido se atiende con un unico suministro (FK a SUMINISTRO).",
    ("PEDIDO", "CLIENTE_id_cliente"): "Cliente que compra (FK a CLIENTE).",
    ("SUMINISTRO", "id_suministro"): "Codigo unico del despacho de almacen a local. Lo genera la base (IDENTITY).",
    ("SUMINISTRO", "fecha_suministro"): "Dia en que sale la mercaderia del centro de distribucion.",
    ("SUMINISTRO", "estado_despacho"): "Como va el traslado: PROGRAMADO, EN RUTA o ENTREGADO. De aqui se deduce el estado del pedido, sin guardarlo dos veces.",
    ("SUMINISTRO", "ALMACEN_id_almacen"): "Almacen que abastece el suministro (FK a ALMACEN).",
    ("SUMINISTRO", "LOCAL_id_local"): "Local que recibe el suministro (FK a LOCAL).",
    ("DETALLE_VENTA", "talla_elegida"): "Talla que pidio el cliente en esa linea. Forma parte de la clave compuesta.",
    ("DETALLE_VENTA", "color_elegido"): "Color que pidio el cliente en esa linea. Forma parte de la clave compuesta.",
    ("DETALLE_VENTA", "cantidad"): "Unidades vendidas de ese producto, talla y color. Debe ser mayor que cero.",
    ("DETALLE_VENTA", "precio_unitario_aplicado"): "Precio cobrado en el momento de la venta (puede tener descuento). No se calcula un total.",
    ("DETALLE_VENTA", "PEDIDO_id_pedido"): "Pedido al que pertenece la linea (FK a PEDIDO).",
    ("DETALLE_VENTA", "PRODUCTO_id_producto"): "Modelo vendido (FK a PRODUCTO).",
    ("STOCK_ALMACEN", "talla"): "Talla disponible en el almacen. Forma parte de la clave compuesta.",
    ("STOCK_ALMACEN", "color"): "Color disponible en el almacen. Forma parte de la clave compuesta.",
    ("STOCK_ALMACEN", "stock_actual"): "Unidades que el almacen tiene hoy de esa talla y color.",
    ("STOCK_ALMACEN", "stock_minimo"): "Umbral de reposicion: por debajo se genera un nuevo suministro.",
    ("STOCK_ALMACEN", "PRODUCTO_id_producto"): "Modelo al que corresponde el stock (FK a PRODUCTO).",
    ("STOCK_ALMACEN", "ALMACEN_id_almacen"): "Almacen donde esta el stock (FK a ALMACEN).",
    ("DETALLE_SUMINISTRO", "talla"): "Talla despachada en el suministro. Forma parte de la clave compuesta.",
    ("DETALLE_SUMINISTRO", "color"): "Color despachado en el suministro. Forma parte de la clave compuesta.",
    ("DETALLE_SUMINISTRO", "cantidad"): "Unidades despachadas de ese producto, talla y color. Debe ser mayor que cero.",
    ("DETALLE_SUMINISTRO", "PRODUCTO_id_producto"): "Modelo incluido en el suministro (FK a PRODUCTO).",
    ("DETALLE_SUMINISTRO", "SUMINISTRO_id_suministro"): "Suministro al que pertenece la linea (FK a SUMINISTRO).",
    ("AUD", "usuario_creacion"): "Usuario de la base que inserto la fila. Se llena solo (DEFAULT SYSTEM_USER).",
    ("AUD", "fecha_creacion"): "Momento del insert. Se llena solo (DEFAULT GETDATE()).",
    ("AUD", "usuario_modificacion"): "Usuario del ultimo cambio. Queda vacio hasta la primera actualizacion.",
    ("AUD", "fecha_modificacion"): "Momento del ultimo cambio. Queda vacio hasta la primera actualizacion.",
}

GENERIC = {
    "nombre": "Nombre descriptivo del registro.",
    "descripcion": "Detalle ampliado del registro. Es opcional.",
    "fecha": "Fecha del hecho que registra la tabla.",
    "cantidad": "Unidades del movimiento.",
    "estado": "Estado del registro dentro de una lista controlada.",
    "talla": "Talla del producto.",
    "color": "Color del producto.",
}

AUD = ["usuario_creacion", "fecha_creacion", "usuario_modificacion", "fecha_modificacion"]

REL_NEGOCIO = {
    "REALIZA": "Un cliente realiza muchos pedidos y cada pedido pertenece a un solo cliente.",
    "CONTIENE": "Un pedido contiene muchos productos (con talla, color, cantidad y precio) y un producto aparece en muchos pedidos.",
    "CLASIFICA": "Una categoria clasifica muchos productos y cada producto tiene una sola categoria.",
    "ALMACENA": "Un almacen almacena muchos productos por talla y color, y un producto esta en varios almacenes.",
    "PROVEE": "Un suministro provee a muchos pedidos y cada pedido se atiende con un solo suministro.",
    "ABASTECE": "Un almacen abastece muchos suministros y cada suministro sale de un solo almacen.",
    "RECIBE": "Un local recibe muchos suministros y cada suministro llega a un solo local.",
    "INCLUYE": "Un suministro incluye muchos productos (con talla, color y cantidad) y un producto va en muchos suministros.",
}

REL_CARD = {
    "REALIZA": "(1,N)", "CONTIENE": "(M,N)", "CLASIFICA": "(1,N)", "ALMACENA": "(M,N)",
    "PROVEE": "(1,N)", "ABASTECE": "(1,N)", "RECIBE": "(1,N)", "INCLUYE": "(M,N)",
}

GLOSARIO = [
    ("MER", "Modelo Entidad-Relacion. Vista conceptual en notacion Chen: entidades, atributos y rombos."),
    ("Modelo logico", "Misma informacion en notacion Barker: entidades, verbo de la relacion y cardinalidad. No muestra columnas FK."),
    ("Modelo relacional", "Tablas con sus columnas, claves primarias y claves foraneas. Ya se puede leer en SQL."),
    ("Modelo fisico", "El script que corre en SQL Server, con IDENTITY, DEFAULT, CHECK y columnas de auditoria."),
    ("PK", "Primary Key. Columna o conjunto de columnas que identifica de forma unica una fila."),
    ("FK", "Foreign Key. Columna que apunta a la PK de otra tabla y hace cumplir la relacion."),
    ("Clave compuesta", "PK formada por varias columnas. Aparece en DETALLE_VENTA, STOCK_ALMACEN y DETALLE_SUMINISTRO."),
    ("IDENTITY(1,1)", "La base genera el numero solo: empieza en 1 y sube de 1 en 1. Solo en las 7 PK simples."),
    ("DEFAULT", "Valor que la base pone sola cuando el INSERT no envia el dato."),
    ("CHECK", "Regla que la base valida en cada INSERT y UPDATE. Si no se cumple, rechaza la fila."),
    ("Auditoria", "Cuatro columnas iguales en las 10 tablas que dicen quien creo o cambio la fila y cuando."),
    ("Suministro", "Despacho de mercaderia de un centro de distribucion (ALMACEN) a una tienda (LOCAL)."),
    ("Detalle", "Tabla que resuelve una relacion de muchos a muchos y guarda los datos propios del movimiento."),
    ("Talla / Color", "Atributos que convierten un modelo en unidades vendibles; junto con el producto forman la clave del detalle."),
    ("Total / IGV", "No existen como columnas: son calculos que se hacen al consultar, no datos que se guarden."),
    ("estado_envio", "Columna eliminada en 3FN: el estado del pedido se deduce de SUMINISTRO.estado_despacho."),
]


# --------------------------------------------------------------------------
# 1. Lectura del script fisico
# --------------------------------------------------------------------------
def _partes(cuerpo):
    """Parte el cuerpo del CREATE TABLE por comas de nivel 0 y une lineas partidas."""
    piezas, buf, prof = [], "", 0
    for ch in cuerpo:
        if ch == "(":
            prof += 1
        elif ch == ")":
            prof -= 1
        if ch == "," and prof == 0:
            piezas.append(buf)
            buf = ""
        else:
            buf += ch
    piezas.append(buf)
    return [re.sub(r"\s+", " ", p).strip() for p in piezas if p.strip()]


def leer_script():
    sql = open(SCRIPT, encoding="utf-8").read()
    sql = re.sub(r"--[^\n]*", "", sql)          # fuera comentarios
    tablas = {}

    for m in re.finditer(r"CREATE TABLE (\w+)\s*\((.*?)\n\s*GO", sql, re.S):
        nombre, cuerpo = m.group(1), m.group(2)
        columnas, pk, checks = [], [], []
        for l in _partes(cuerpo):
            if not l:
                continue
            if l.startswith("CONSTRAINT") and "PRIMARY KEY" in l:
                # solo el contenido del primer parentesis balanceado (fuera el WITH ...)
                resto_pk, prof_pk, dentro = "", 0, False
                for ch in l.split("PRIMARY KEY", 1)[1]:
                    if ch == "(":
                        prof_pk += 1
                        if prof_pk == 1:
                            dentro = True
                            continue
                    elif ch == ")":
                        prof_pk -= 1
                        if prof_pk == 0:
                            break
                    if dentro:
                        resto_pk += ch
                pk = [c.strip() for c in resto_pk.split(",")]
                continue
            mch = re.match(r"CONSTRAINT (\w+) CHECK \((.*)\)$", l, re.S)
            if mch:
                checks.append((mch.group(1), re.sub(r"\s+", " ", mch.group(2)).strip()))
                continue
            if l.startswith(("CONSTRAINT", "WITH", "ALLOW", ")")):
                continue
            mcol = re.match(r"(\w+)\s+(VARCHAR|INT|INTEGER|NUMERIC|DECIMAL|DATETIME|SMALLDATETIME|DATE|CHAR)\s*(?:\(([\d, ]+)\))?(.*)", l, re.S)
            if not mcol:
                continue
            col, tipo, largo, resto = mcol.group(1), mcol.group(2), mcol.group(3), mcol.group(4)
            ident = "IDENTITY" in resto.upper()
            default = None
            md = re.search(r"DEFAULT\s+(.+?)\s+NOT NULL", resto, re.S) or re.search(r"DEFAULT\s+(.+)$", resto, re.S)
            if md:
                default = re.sub(r"\s+", " ", md.group(1)).strip()
            columnas.append({
                "col": col,
                "tipo": re.sub(r"\s+", " ", (tipo + ("(" + largo.replace(" ", "") + ")" if largo else ""))),
                "nulo": "NOT NULL" not in resto.upper(),
                "identity": ident,
                "default": default,
            })
        tablas[nombre] = {"nombre": nombre, "columnas": columnas, "pk": pk, "checks": checks}

    fks = []
    for m in re.finditer(r"ALTER TABLE (\w+)\s+ADD CONSTRAINT (\w+) FOREIGN KEY \((\w+)\)\s+"
                         r"REFERENCES (\w+) \((\w+)\)", sql, re.S):
        fks.append({"nombre": m.group(2), "hija": m.group(1), "col": m.group(3),
                    "padre": m.group(4), "col_padre": m.group(5)})
    return tablas, fks


def ordenar(tablas, fks):
    """Orden de despliegue: maestras primero, luego transaccionales, luego detalle."""
    orden = ["CLIENTE", "CATEGORIA", "ALMACEN", "LOCAL", "PRODUCTO", "PEDIDO",
             "SUMINISTRO", "STOCK_ALMACEN", "DETALLE_VENTA", "DETALLE_SUMINISTRO"]
    return [tablas[n] for n in orden if n in tablas], fks


# --------------------------------------------------------------------------
# 2. Armado de las filas del diccionario
# --------------------------------------------------------------------------
def filas_diccionario(tablas, fks):
    filas = []
    for t in tablas:
        for c in t["columnas"]:
            nombre = t["nombre"]
            fk = [f for f in fks if f["hija"] == nombre and f["col"] == c["col"]]
            clave = ""
            if c["col"] in t["pk"]:
                clave = "PK"
            if fk:
                clave = (clave + " + FK") if clave else "FK"
            desc = DESC.get((nombre, c["col"]))
            if desc is None:
                if c["col"] in AUD:
                    desc = DESC[("AUD", c["col"])]
                else:
                    desc = GENERIC.get(c["col"], "Dato propio de la tabla %s." % nombre)
            filas.append({
                "tabla": nombre,
                "columna": c["col"],
                "tipo": c["tipo"],
                "nulo": "Si" if c["nulo"] else "No",
                "clave": clave,
                "referencia": ("%s.%s" % (fk[0]["padre"], fk[0]["col_padre"])) if fk else "",
                "identity": "Si" if c["identity"] else "",
                "default": c["default"] or "",
                "descripcion": desc,
                "auditoria": c["col"] in AUD,
            })
    return filas


# --------------------------------------------------------------------------
# 3. Excel
# --------------------------------------------------------------------------
AZUL = "1F4E79"
CLARO = "DCE6F1"
GRIS = "F2F2F2"


def _titulo(ws, texto, fila=1, ancho=8):
    ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=ancho)
    cel = ws.cell(row=fila, column=1, value=texto)
    cel.font = Font(bold=True, size=14, color="FFFFFF")
    cel.fill = PatternFill("solid", fgColor=AZUL)
    cel.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[fila].height = 24


def _cabecera(ws, valores, fila):
    for j, v in enumerate(valores, start=1):
        cel = ws.cell(row=fila, column=j, value=v)
        cel.font = Font(bold=True, size=10, color="FFFFFF")
        cel.fill = PatternFill("solid", fgColor=AZUL)
        cel.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[fila].height = 30


def construir_xlsx(tablas, fks, filas):
    fina = Side(style="thin", color="BFBFBF")
    borde = Border(left=fina, right=fina, top=fina, bottom=fina)
    wb = Workbook()

    # ---- hoja 1: resumen
    ws = wb.active
    ws.title = "Resumen"
    ws.sheet_view.showGridLines = False
    _titulo(ws, "DICCIONARIO DE DATOS  |  BD NIKE Inc. - Grupo 05", 1, 6)
    ws["A3"] = "Proyecto"
    ws["B3"] = "Base de datos de ventas y almacenes de Nike a nivel nacional - Peru"
    ws["A4"] = "Curso"
    ws["B4"] = "Disenio de Bases de Datos Relacionales - IDAT"
    ws["A5"] = "Docente"
    ws["B5"] = "Sergio Fernando Castillo Carrion"
    ws["A6"] = "Integrantes"
    ws["B6"] = "Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios"
    ws["A7"] = "Motor"
    ws["B7"] = "Microsoft SQL Server (script MF_NIKE_INC_CORREGIDO.sql)"
    ws["A8"] = "Base de datos"
    ws["B8"] = "NIKE_INC_BD"
    for r in range(3, 9):
        ws.cell(row=r, column=1).font = Font(bold=True)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")

    ws["A10"] = "Cifras del modelo"
    ws["A10"].font = Font(bold=True, size=12, color=AZUL)
    ncols = len(filas)
    nchecks = sum(len(t["checks"]) for t in tablas)
    nident = sum(1 for f in filas if f["identity"])
    ndef = sum(1 for f in filas if f["default"] and not f["auditoria"])
    cifras = [
        ("Tablas", len(tablas)),
        ("Columnas totales", ncols),
        ("Columnas de negocio", len([f for f in filas if not f["auditoria"]])),
        ("Columnas de auditoria (4 por tabla)", len([f for f in filas if f["auditoria"]])),
        ("Claves primarias simples (IDENTITY)", nident),
        ("Claves primarias compuestas", len([t for t in tablas if len(t["pk"]) > 1])),
        ("Claves foraneas", len(fks)),
        ("Restricciones CHECK", nchecks),
        ("Valores por omision de negocio (DEFAULT)", ndef),
        ("Columnas que admiten NULL", len([f for f in filas if f["nulo"] == "Si" and not f["auditoria"]])),
        ("Vistas", 0),
    ]
    _cabecera(ws, ["Concepto", "Valor"], 11)
    for i, (k, v) in enumerate(cifras, start=12):
        ws.cell(row=i, column=1, value=k).border = borde
        c = ws.cell(row=i, column=2, value=v)
        c.border = borde
        c.alignment = Alignment(horizontal="center")

    ws["A25"] = "Tablas del modelo"
    ws["A25"].font = Font(bold=True, size=12, color=AZUL)
    _cabecera(ws, ["#", "Tabla", "Rol", "Proposito", "Columnas", "PK"], 26)
    rol = {
        "CLIENTE": ("Maestra", "Comprador que realiza pedidos."),
        "CATEGORIA": ("Maestra", "Linea comercial que clasifica los productos."),
        "ALMACEN": ("Maestra", "Centro de distribucion que guarda stock y abastece locales."),
        "LOCAL": ("Maestra", "Tienda fisica que recibe mercaderia."),
        "PRODUCTO": ("Maestra", "Catalogo de modelos de Nike."),
        "PEDIDO": ("Transaccional", "Cabecera de la venta: cliente, fecha, pago y suministro que la atiende."),
        "SUMINISTRO": ("Transaccional", "Despacho de un almacen a un local."),
        "STOCK_ALMACEN": ("Detalle", "Unidades por producto, talla y color en cada almacen."),
        "DETALLE_VENTA": ("Detalle", "Lineas vendidas: producto, talla, color, cantidad y precio aplicado."),
        "DETALLE_SUMINISTRO": ("Detalle", "Lineas despachadas: producto, talla, color y cantidad."),
    }
    for i, t in enumerate(tablas, start=27):
        r, p = rol.get(t["nombre"], ("", ""))
        vals = [i - 26, t["nombre"], r, p, len(t["columnas"]), ", ".join(t["pk"])]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=i, column=j, value=v)
            c.border = borde
            c.alignment = Alignment(wrap_text=True, vertical="top",
                                    horizontal="center" if j in (1, 5) else "left")

    ws["A39"] = "Convenciones de nomenclatura"
    ws["A39"].font = Font(bold=True, size=12, color=AZUL)
    conv = [
        ("Tablas", "Nombre en MAYUSCULAS y en singular: CLIENTE, PEDIDO, DETALLE_VENTA."),
        ("Columnas", "minusculas con guion bajo: precio_unitario_base, fecha_suministro."),
        ("Clave primaria", "id_<tabla> en las tablas maestras; en los detalles la PK es la combinacion de sus columnas."),
        ("Clave foranea", "<TABLA_PADRE>_id_<padre>: PEDIDO_CLIENTE_FK sobre la columna CLIENTE_id_cliente."),
        ("Restricciones", "PK_<tabla>, <TABLA>_<PADRE>_FK, CK_<tabla>_<columna>."),
        ("Sinonimos prohibidos", "No se usa INVENTARIO (se usa ALMACEN) ni Total/IGV como columnas."),
    ]
    for i, (k, v) in enumerate(conv, start=40):
        ws.cell(row=i, column=1, value=k).font = Font(bold=True)
        c = ws.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=i, start_column=2, end_row=i, end_column=6)

    for col, ancho in zip("ABCDEF", [22, 46, 14, 58, 11, 34]):
        ws.column_dimensions[col].width = ancho

    # ---- hoja 2: diccionario
    ws = wb.create_sheet("Diccionario")
    ws.sheet_view.showGridLines = False
    _titulo(ws, "DICCIONARIO DE DATOS - columna por columna", 1, 9)
    enc = ["Tabla", "Columna", "Tipo de dato", "Admite NULL", "Clave", "Referencia (FK)",
           "IDENTITY", "DEFAULT", "Descripcion"]
    _cabecera(ws, enc, 2)
    ws.freeze_panes = "A3"
    fila = 3
    for t in tablas:
        ws.merge_cells(start_row=fila, start_column=1, end_row=fila, end_column=9)
        c = ws.cell(row=fila, column=1,
                    value="%s   (PK: %s  |  %d columnas)" % (t["nombre"], ", ".join(t["pk"]), len(t["columnas"])))
        c.font = Font(bold=True, size=10, color=AZUL)
        c.fill = PatternFill("solid", fgColor=CLARO)
        fila += 1
        for f in [x for x in filas if x["tabla"] == t["nombre"]]:
            vals = [f["tabla"], f["columna"], f["tipo"], f["nulo"], f["clave"],
                    f["referencia"], f["identity"], f["default"], f["descripcion"]]
            for j, v in enumerate(vals, start=1):
                cel = ws.cell(row=fila, column=j, value=v)
                cel.border = borde
                cel.alignment = Alignment(wrap_text=True, vertical="top",
                                          horizontal="center" if j in (3, 4, 5, 7) else "left")
                cel.font = Font(size=9, bold=(j == 2))
                if f["auditoria"]:
                    cel.fill = PatternFill("solid", fgColor=GRIS)
            fila += 1
    for col, ancho in zip("ABCDEFGHI", [18, 26, 14, 12, 10, 26, 10, 26, 62]):
        ws.column_dimensions[col].width = ancho

    # ---- hoja 3: claves foraneas
    ws = wb.create_sheet("Claves foraneas")
    ws.sheet_view.showGridLines = False
    _titulo(ws, "CLAVES FORANEAS (11) - que relacion hace cumplir cada una", 1, 7)
    _cabecera(ws, ["#", "Restriccion", "Tabla hija (donde esta la FK)", "Columna",
                   "Tabla padre (referenciada)", "Columna referenciada", "Regla de negocio"], 2)
    for i, f in enumerate(fks, start=3):
        rel = None
        for nombre, par in [("CLASIFICA", "PRODUCTO"), ("REALIZA", "CLIENTE"), ("PROVEE", "SUMINISTRO"),
                            ("ABASTECE", "ALMACEN"), ("RECIBE", "LOCAL"), ("CONTIENE", "PEDIDO"),
                            ("ALMACENA", "ALMACEN"), ("INCLUYE", "SUMINISTRO")]:
            if f["padre"] == par:
                rel = nombre
                break
        vals = [i - 2, f["nombre"], f["hija"], f["col"], f["padre"], f["col_padre"],
                REL_NEGOCIO.get(rel, "")]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=i, column=j, value=v)
            c.border = borde
            c.alignment = Alignment(wrap_text=True, vertical="top",
                                    horizontal="center" if j in (1, 7) else "left")
            c.font = Font(size=9)
    for col, ancho in zip("ABCDEFG", [6, 36, 22, 22, 24, 20, 60]):
        ws.column_dimensions[col].width = ancho

    # ---- hoja 4: restricciones
    ws = wb.create_sheet("Restricciones")
    ws.sheet_view.showGridLines = False
    _titulo(ws, "RESTRICCIONES: IDENTITY, DEFAULT y CHECK", 1, 6)
    fila = 3
    ws.cell(row=3, column=1, value="IDENTITY (7) - la base genera el numero").font = Font(bold=True, size=11, color=AZUL)
    _cabecera(ws, ["Tabla", "Columna", "Definicion", "Para que sirve"], 4)
    fila = 5
    for f in [x for x in filas if x["identity"]]:
        vals = [f["tabla"], f["columna"], "IDENTITY(1,1)", "Codigo unico generado por la base; no se ingresa a mano."]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=fila, column=j, value=v)
            c.border = borde
            c.font = Font(size=9)
        fila += 1

    fila += 1
    ws.cell(row=fila, column=1, value="DEFAULT - valores por omision (%d)" % ndef).font = Font(bold=True, size=11, color=AZUL)
    fila += 1
    _cabecera(ws, ["Tabla", "Columna", "Valor por omision", "Justificacion"], fila)
    fila += 1
    for f in [x for x in filas if x["default"] and not x["auditoria"]]:
        justif = {
            ("PEDIDO", "fecha"): "Si no se envia la fecha, se registra el dia de la venta.",
            ("PEDIDO", "metodo_pago"): "Es el medio de pago mas usado en la tienda online.",
            ("SUMINISTRO", "fecha_suministro"): "Si no se envia la fecha, se registra el dia del despacho.",
            ("SUMINISTRO", "estado_despacho"): "Todo despacho nuevo nace PROGRAMADO.",
            ("PRODUCTO", "estado"): "Todo modelo nuevo entra DISPONIBLE.",
            ("DETALLE_VENTA", "cantidad"): "Una linea sin cantidad explicita equivale a una unidad.",
            ("DETALLE_SUMINISTRO", "cantidad"): "Una linea sin cantidad explicita equivale a una unidad.",
            ("STOCK_ALMACEN", "stock_actual"): "Un producto recien registrado en el almacen arranca en cero.",
            ("STOCK_ALMACEN", "stock_minimo"): "Sin minimo definido, el almacen arranca en cero.",
        }.get((f["tabla"], f["columna"]), "")
        vals = [f["tabla"], f["columna"], f["default"], justif]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=fila, column=j, value=v)
            c.border = borde
            c.font = Font(size=9)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        fila += 1

    fila += 1
    ws.cell(row=fila, column=1, value="CHECK - reglas de validacion (%d)" % nchecks).font = Font(bold=True, size=11, color=AZUL)
    fila += 1
    _cabecera(ws, ["Restriccion", "Tabla", "Expresion", "Que impide en la practica"], fila)
    fila += 1
    explica = {
        "CK_DETALLE_VENTA_CANTIDAD": "No se puede vender 0 ni una cantidad negativa.",
        "CK_DETALLE_SUMINISTRO_CANTIDAD": "No se puede despachar 0 ni una cantidad negativa.",
        "CK_DETALLE_VENTA_PRECIO": "El precio aplicado siempre debe ser mayor que cero.",
        "CK_PRODUCTO_PRECIO": "El precio de lista siempre debe ser mayor que cero.",
        "CK_STOCK_ALMACEN_ACTUAL": "El stock no puede quedar en negativo.",
        "CK_STOCK_ALMACEN_MINIMO": "El minimo de reposicion no puede ser negativo.",
        "CK_SUMINISTRO_ESTADO_DESPACHO": "Solo acepta PROGRAMADO, EN RUTA o ENTREGADO.",
        "CK_SUMINISTRO_ESTADO": "Solo acepta PROGRAMADO, EN RUTA o ENTREGADO.",
        "CK_PRODUCTO_ESTADO": "Solo acepta DISPONIBLE, AGOTADO o DESCONTINUADO.",
        "CK_CLIENTE_CORREO": "El correo debe tener la forma texto@texto.dominio.",
        "CK_CLIENTE_TELEFONO": "El telefono solo admite digitos, entre 6 y 15.",
    }
    for t in tablas:
        for nombre, expr in t["checks"]:
            vals = [nombre, t["nombre"], expr, explica.get(nombre, "")]
            for j, v in enumerate(vals, start=1):
                c = ws.cell(row=fila, column=j, value=v)
                c.border = borde
                c.font = Font(size=9)
                c.alignment = Alignment(wrap_text=True, vertical="top")
            fila += 1
    for col, ancho in zip("ABCD", [34, 22, 56, 54]):
        ws.column_dimensions[col].width = ancho

    # ---- hoja 5: relaciones
    ws = wb.create_sheet("Relaciones")
    ws.sheet_view.showGridLines = False
    _titulo(ws, "RELACIONES DEL MODELO (8) - lectura en MER, logico y relacional", 1, 5)
    _cabecera(ws, ["#", "Relacion", "Cardinalidad", "Tablas que une", "Regla de negocio"], 2)
    pares = [("REALIZA", "CLIENTE", "PEDIDO"), ("CONTIENE", "PEDIDO", "PRODUCTO"),
             ("CLASIFICA", "CATEGORIA", "PRODUCTO"), ("ALMACENA", "PRODUCTO", "ALMACEN"),
             ("PROVEE", "PEDIDO", "SUMINISTRO"), ("ABASTECE", "ALMACEN", "SUMINISTRO"),
             ("RECIBE", "LOCAL", "SUMINISTRO"), ("INCLUYE", "SUMINISTRO", "PRODUCTO")]
    for i, (rel, a, b) in enumerate(pares, start=3):
        vals = [i - 2, rel, REL_CARD[rel], "%s - %s" % (a, b), REL_NEGOCIO[rel]]
        for j, v in enumerate(vals, start=1):
            c = ws.cell(row=i, column=j, value=v)
            c.border = borde
            c.font = Font(size=9)
            c.alignment = Alignment(wrap_text=True, vertical="top", horizontal="center" if j in (1, 3) else "left")
    for col, ancho in zip("ABCDE", [6, 18, 16, 34, 76]):
        ws.column_dimensions[col].width = ancho

    # ---- hoja 6: glosario
    ws = wb.create_sheet("Glosario")
    ws.sheet_view.showGridLines = False
    _titulo(ws, "GLOSARIO - terminos usados en el proyecto", 1, 3)
    _cabecera(ws, ["Termino", "Significado"], 2)
    for i, (k, v) in enumerate(GLOSARIO, start=3):
        ws.cell(row=i, column=1, value=k).font = Font(bold=True, size=10)
        c = ws.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        for j in (1, 2):
            ws.cell(row=i, column=j).border = borde
    ws.column_dimensions["A"].width = 24
    ws.column_dimensions["B"].width = 110

    wb.save(XLSX)
    return XLSX


# --------------------------------------------------------------------------
# 4. Markdown
# --------------------------------------------------------------------------
def construir_md(tablas, fks, filas):
    L = []
    A = L.append
    A("# Diccionario de datos | BD NIKE Inc. - Grupo 05")
    A("")
    A("Documento de referencia del **modelo fisico** entregado. Se genera leyendo "
      "`nivel_fisico/MF_NIKE_INC_CORREGIDO.sql`, asi que lo que dice aqui es exactamente lo "
      "que existe en SQL Server despues de ejecutar el script.")
    A("")
    A("| Dato | Valor |")
    A("| :--- | :--- |")
    A("| Curso | Disenio de Bases de Datos Relacionales - IDAT |")
    A("| Docente | Sergio Fernando Castillo Carrion |")
    A("| Integrantes | Daniel Asmat, Salomon Fernandez, Luis Coloma, Pablo Rios |")
    A("| Motor | Microsoft SQL Server |")
    A("| Base de datos | `NIKE_INC_BD` |")
    A("| Tablas | %d |" % len(tablas))
    A("| Columnas totales | %d (de negocio: %d, de auditoria: %d) |"
      % (len(filas), len([f for f in filas if not f["auditoria"]]),
         len([f for f in filas if f["auditoria"]])))
    A("| Claves foraneas | %d |" % len(fks))
    A("| Claves primarias | %d simples con `IDENTITY` + %d compuestas |"
      % (sum(1 for f in filas if f["identity"]), len([t for t in tablas if len(t["pk"]) > 1])))
    A("| Restricciones `CHECK` | %d |" % sum(len(t["checks"]) for t in tablas))
    A("| Columnas que admiten NULL | 3 (`telefono_secundario`, `descripcion`, `especificaciones`) |")
    A("| Vistas | 0 |")
    A("")
    A("## Como leer el diccionario")
    A("")
    A("| Columna | Significado |")
    A("| :--- | :--- |")
    A("| **Clave** | `PK` = clave primaria, `FK` = clave foranea, `PK + FK` = forma parte de la clave compuesta y ademas apunta a otra tabla. |")
    A("| **Admite NULL** | `No` = obligatorio; `Si` = opcional. |")
    A("| **DEFAULT** | Valor que pone la base cuando el `INSERT` no envia el dato. |")
    A("| **Descripcion** | Que guarda la columna, en lenguaje del negocio. |")
    A("")
    A("Las cuatro columnas de auditoria (`usuario_creacion`, `fecha_creacion`, "
      "`usuario_modificacion`, `fecha_modificacion`) se repiten igual en las %d tablas; en cada "
      "tabla se listan al final y no se vuelven a explicar." % len(tablas))
    A("")

    A("## 1. Resumen de tablas")
    A("")
    A("| # | Tabla | Rol | Columnas | Clave primaria | Proposito |")
    A("| :---: | :--- | :--- | :---: | :--- | :--- |")
    rol = {
        "CLIENTE": ("Maestra", "Comprador que realiza pedidos."),
        "CATEGORIA": ("Maestra", "Linea comercial que clasifica los productos."),
        "ALMACEN": ("Maestra", "Centro de distribucion que guarda stock y abastece locales."),
        "LOCAL": ("Maestra", "Tienda fisica que recibe mercaderia."),
        "PRODUCTO": ("Maestra", "Catalogo de modelos de Nike."),
        "PEDIDO": ("Transaccional", "Cabecera de la venta: cliente, fecha, pago y suministro que la atiende."),
        "SUMINISTRO": ("Transaccional", "Despacho de un almacen a un local, con su estado."),
        "STOCK_ALMACEN": ("Detalle", "Unidades por producto, talla y color en cada almacen."),
        "DETALLE_VENTA": ("Detalle", "Lineas vendidas: producto, talla, color, cantidad y precio aplicado."),
        "DETALLE_SUMINISTRO": ("Detalle", "Lineas despachadas: producto, talla, color y cantidad."),
    }
    for i, t in enumerate(tablas, start=1):
        r, p = rol[t["nombre"]]
        A("| %d | `%s` | %s | %d | `%s` | %s |"
          % (i, t["nombre"], r, len(t["columnas"]), "`, `".join(t["pk"]), p))
    A("")

    A("## 2. Diccionario por tabla")
    for t in tablas:
        r, p = rol[t["nombre"]]
        A("")
        A("### %s  (%s)" % (t["nombre"], r.lower()))
        A("")
        A("*%s*" % p)
        A("")
        comp = ("  (compuesta: la combinacion de esas columnas es unica)"
                if len(t["pk"]) > 1 else "  (simple, con `IDENTITY(1,1)`)")
        A("Clave primaria: `%s`%s" % ("`, `".join(t["pk"]), comp))
        A("")
        A("| Columna | Tipo | NULL | Clave | Referencia | DEFAULT | Descripcion |")
        A("| :--- | :--- | :---: | :---: | :--- | :--- | :--- |")
        for f in [x for x in filas if x["tabla"] == t["nombre"]]:
            A("| `%s` | `%s` | %s | %s | %s | %s | %s |"
              % (f["columna"], f["tipo"], f["nulo"], f["clave"] or "-",
                 ("`%s`" % f["referencia"]) if f["referencia"] else "-",
                 ("`%s`" % f["default"]) if f["default"] else "-",
                 f["descripcion"]))
        if t["checks"]:
            A("")
            A("Validaciones (`CHECK`):")
            A("")
            for nombre, expr in t["checks"]:
                A("- `%s`: `%s`" % (nombre, expr))
    A("")

    A("## 3. Claves foraneas (11)")
    A("")
    A("| # | Restriccion | Tabla hija | Columna | Tabla padre | Columna referenciada |")
    A("| :---: | :--- | :--- | :--- | :--- | :--- |")
    for i, f in enumerate(fks, start=1):
        A("| %d | `%s` | `%s` | `%s` | `%s` | `%s` |"
          % (i, f["nombre"], f["hija"], f["col"], f["padre"], f["col_padre"]))
    A("")

    A("## 4. Relaciones y cardinalidad")
    A("")
    A("| Relacion | Cardinalidad | Une | Regla de negocio |")
    A("| :--- | :---: | :--- | :--- |")
    for rel, a, b in [("REALIZA", "CLIENTE", "PEDIDO"), ("CONTIENE", "PEDIDO", "PRODUCTO"),
                      ("CLASIFICA", "CATEGORIA", "PRODUCTO"), ("ALMACENA", "PRODUCTO", "ALMACEN"),
                      ("PROVEE", "PEDIDO", "SUMINISTRO"), ("ABASTECE", "ALMACEN", "SUMINISTRO"),
                      ("RECIBE", "LOCAL", "SUMINISTRO"), ("INCLUYE", "SUMINISTRO", "PRODUCTO")]:
        A("| `%s` | %s | %s - %s | %s |" % (rel, REL_CARD[rel], a, b, REL_NEGOCIO[rel]))
    A("")
    A("> **`PROVEE` es 1:N.** Un suministro atiende muchos pedidos y cada pedido se atiende con un "
      "solo suministro. En la base eso se cumple con una sola columna obligatoria "
      "(`PEDIDO.SUMINISTRO_id_suministro`); no se agrega `UNIQUE` ni se escribe `(1,1)`.")
    A("")

    A("## 5. Reglas fijas del modelo")
    A("")
    A("1. **Nada calculado:** no existen columnas `Total` ni `IGV`; se obtienen al consultar.")
    A("2. **Nada repetido:** `PEDIDO` no guarda `estado_envio`; se lee de `SUMINISTRO.estado_despacho`.")
    A("3. **Sin vistas:** el modelo se resuelve con tablas y claves foraneas.")
    A("4. **`ALMACEN`** solo se relaciona con `SUMINISTRO` (`ABASTECE`) y con `PRODUCTO` (`ALMACENA`).")
    A("5. **Opcionales:** solo `telefono_secundario`, `descripcion` y `especificaciones`.")
    A("6. **Auditoria:** las 10 tablas llevan las mismas 4 columnas.")
    A("7. **Longitudes justas:** ningun `VARCHAR(255)` por omision.")
    A("")

    A("## 6. Glosario")
    A("")
    A("| Termino | Significado |")
    A("| :--- | :--- |")
    for k, v in GLOSARIO:
        A("| **%s** | %s |" % (k, v))
    A("")
    open(MD, "w", encoding="utf-8").write("\n".join(L))
    return MD


def main():
    tablas, fks = leer_script()
    tablas, fks = ordenar(tablas, fks)
    filas = filas_diccionario(tablas, fks)
    print("tablas:", len(tablas), "| columnas:", len(filas), "| fk:", len(fks),
          "| checks:", sum(len(t["checks"]) for t in tablas),
          "| identity:", sum(1 for f in filas if f["identity"]),
          "| default negocio:", sum(1 for f in filas if f["default"] and not f["auditoria"]),
          "| nullables:", [f["tabla"] + "." + f["columna"] for f in filas if f["nulo"] == "Si" and not f["auditoria"]])
    construir_xlsx(tablas, fks, filas)
    construir_md(tablas, fks, filas)
    json.dump({"tablas": [t["nombre"] for t in tablas], "filas": filas},
              open(JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("xlsx ->", XLSX)
    print("md   ->", MD)


if __name__ == "__main__":
    main()
