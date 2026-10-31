# -*- coding: utf-8 -*-
"""Laminas del modelo logico, relacional y fisico (estilo Oracle Data Modeler simplificado).

Se dibujan las 10 tablas del modelo final con sus PK / FK / PFK, los tipos de dato
segun el motor y las notas de restricciones. No hay columnas calculadas.
"""
import os

from PIL import Image, ImageDraw, ImageFont

import modelo_final as M

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

ESC = 2  # 1570 x 848 -> 3140 x 1696


def HEX(c):
    return "#" + c

# marco de colores por marca
COL_MARCA = {"PK": ("#F2C200", "#000000", "PK"), "PFK": ("#C58AF9", "#000000", "PFK"),
             "FK": ("#E8A33D", "#000000", "FK"), "-": ("#DDDDDD", "#666666", "")}
AZUL_CAB = "#BFD7EA"
BEIGE_CAB = "#F6E3B4"
GRIS_BORDE = "#8A9399"

POS = {  # tabla: (x, y, ancho)
    "CATEGORIA": (960, 170, 250),
    "CLIENTE": (20, 330, 250),
    "PEDIDO": (330, 330, 250),
    "DETALLE_VENTA": (630, 330, 250),
    "PRODUCTO": (960, 330, 250),
    "LOCAL": (20, 600, 250),
    "SUMINISTRO": (330, 600, 250),
    "DETALLE_SUMINISTRO": (630, 600, 250),
    "ALMACEN": (960, 600, 250),
    "STOCK_ALMACEN": (1240, 600, 260),
}

# (columna, filas): se dibujan 2 filas de ejemplo por tabla clave
FILAS = {
    "CLIENTE": [1, 2, 3, 4, 5, 6],
    "PEDIDO": [1, 2, 3, 4, 5, 6],
    "DETALLE_VENTA": [1, 2, 3, 4, 5, 6, 7],
    "CATEGORIA": [1, 2, 3],
    "PRODUCTO": [1, 2, 3, 4, 5, 6],
    "LOCAL": [1, 2, 3],
    "SUMINISTRO": [1, 2, 3, 4, 5],
    "DETALLE_SUMINISTRO": [1, 2, 3, 4, 5],
    "ALMACEN": [1, 2, 3],
    "STOCK_ALMACEN": [1, 2, 3, 4, 5, 6],
}
NOTAS = {
    "CLIENTE": ["CLIENTE_PK (id_cliente)"],
    "PEDIDO": ["PEDIDO_PK (id_pedido)", "CLIENTE_FK (CLIENTE_id_cliente)",
               "SUMINISTRO_FK", "   (SUMINISTRO_id_suministro)"],
    "DETALLE_VENTA": ["DETALLE_VENTA_PK:", "   PEDIDO_id_pedido,", "   PRODUCTO_id_producto,",
                      "   talla_elegida, color_elegido", "ALMACEN_FK"],
    "CATEGORIA": ["CATEGORIA_PK (id_categoria)"],
    "PRODUCTO": ["PRODUCTO_PK (id_producto)", "CATEGORIA_FK",
                 "   (CATEGORIA_id_categoria)"],
    "LOCAL": ["LOCAL_PK (id_local)"],
    "SUMINISTRO": ["SUMINISTRO_PK (id_suministro)", "ALMACEN_FK (ALMACEN_id_almacen)",
                   "LOCAL_FK (LOCAL_id_local)"],
    "DETALLE_SUMINISTRO": ["DETALLE_SUMINISTRO_PK:", "   SUMINISTRO_id_suministro,",
                           "   PRODUCTO_id_producto,", "   talla, color",
                           "SUMINISTRO_FK / PRODUCTO_FK"],
    "ALMACEN": ["ALMACEN_PK (id_almacen)"],
    "STOCK_ALMACEN": ["STOCK_ALMACEN_PK: talla, color,", "   ALMACEN_id_almacen,",
                      "   PRODUCTO_id_producto", "ALMACEN_FK / PRODUCTO_FK"],
}

# relaciones: (padre, columna en el hijo, hijo, puntos de la ruta)
LINEAS = [
    ("CLIENTE", "CLIENTE_id_cliente", "PEDIDO", None),
    ("LOCAL", "LOCAL_id_local", "SUMINISTRO", None),
    ("PEDIDO", "PEDIDO_id_pedido", "DETALLE_VENTA", None),
    ("PRODUCTO", "PRODUCTO_id_producto", "DETALLE_VENTA", None),
    ("SUMINISTRO", "SUMINISTRO_id_suministro", "DETALLE_SUMINISTRO", None),
    ("ALMACEN", "ALMACEN_id_almacen", "STOCK_ALMACEN", None),
    ("CATEGORIA", "CATEGORIA_id_categoria", "PRODUCTO", None),
    ("SUMINISTRO", "SUMINISTRO_id_suministro", "PEDIDO", None),
    ("ALMACEN", "ALMACEN_id_almacen", "DETALLE_VENTA", [(760, 548), (760, 566), (1000, 566), (1000, 600)]),
    ("PRODUCTO", "PRODUCTO_id_producto", "DETALLE_SUMINISTRO",
     [(880, 650), (935, 650), (935, 516), (1010, 516), (1010, 506)]),
    ("ALMACEN", "ALMACEN_id_almacen", "SUMINISTRO", [(500, 758), (500, 822), (1030, 822), (1030, 698)]),
    ("PRODUCTO", "PRODUCTO_id_producto", "STOCK_ALMACEN",
     [(1130, 506), (1130, 546), (1370, 546), (1370, 600)]),
]

TITULOS = {
    "logico": ("MODELO LOGICO  |  NIKE Inc. - Grupo 05", "Oracle SQL Developer Data Modeler"),
    "relacional": ("MODELO RELACIONAL  |  NIKE Inc. - Grupo 05", "Oracle SQL Developer Data Modeler"),
    "fisico": ("MODELO FISICO  |  NIKE Inc. - Grupo 05", "SQL Server / SSMS  -  base NIKE_INC_BD"),
}

LEYENDA = {
    "logico": ["COMO LEER EL MODELO LOGICO",
               "PK  identificador principal de la entidad.",
               "FK  clave foranea: apunta a la PK de otra tabla.",
               "PFK  columna de la clave compuesta que ademas es foranea.",
               "OPCIONAL / NULL solo en telefono_secundario, descripcion",
               "y especificaciones.",
               "Las 3 relaciones M:N ya estan resueltas como tablas: CONTIENE,"
               " ALMACENA e INCLUYE.",
               "No hay columnas calculadas: el total de la linea y el IGV",
               "se calculan en la vista VW_PEDIDO_TOTALES.",
               "1 = lado uno, N = lado muchos."],
    "relacional": ["COMO LEER EL MODELO RELACIONAL",
                   "PK  clave primaria  |  FK  clave foranea  |  PFK  parte de la PK y FK.",
                   "Los nombres de las foraneas son TABLA_id.",
                   "DETALLE_VENTA tiene PK compuesta de 4 columnas: pedido,"
                   " producto, talla y color.",
                   "DETALLE_SUMINISTRO tiene PK compuesta de 4 columnas: suministro,"
                   " producto, talla y color.",
                   "STOCK_ALMACEN tiene PK compuesta de 4 columnas: talla, color,"
                   " almacen y producto.",
                   "VARCHAR2 y NUMBER(10,2) son los tipos de Oracle.",
                   "No hay columnas calculadas: total e IGV viven en la vista."],
    "fisico": ["COMO LEER EL MODELO FISICO",
               "INTEGER  unidades enteras (cantidad, stock, llaves).",
               "VARCHAR(n)  texto con longitud justa y necesaria.",
               "DECIMAL(10,2)  importes en soles con dos decimales.",
               "DATE  fecha del pedido y fecha del suministro.",
               "NULL  solo en telefono_secundario, descripcion y especificaciones.",
               "Las 12 claves foraneas se crean con ON DELETE NO ACTION.",
               "Total e IGV se calculan en VW_PEDIDO_TOTALES: no son columnas."],
}


def tipo(col, modo):
    nombre, tipo_dato, largo, marca, opc = col
    if tipo_dato == "VARCHAR":
        return ("VARCHAR2(%d)" % largo) if modo != "fisico" else ("VARCHAR(%d)" % largo)
    if tipo_dato == "DECIMAL":
        return ("NUMBER(10,2)" if modo == "relacional" else "DECIMAL(10,2)")
    if tipo_dato == "INTEGER":
        return "INTEGER"
    return "DATE"


def alto(tab, modo):
    n = len(FILAS[tab])
    h = 26 + n * 18 + 6
    if modo != "logico":
        h += 12 * len(NOTAS[tab])
    else:
        h += 12 * len(NOTAS[tab])
    return h


def dibujar(modo, ruta, W=1570, H=848):
    titulo, subtitulo = TITULOS[modo]
    img = Image.new("RGB", (W * ESC, H * ESC), "white")
    d = ImageDraw.Draw(img)
    f_tit = ImageFont.truetype(FB, 20 * ESC)
    f_sub = ImageFont.truetype(F, 12 * ESC)
    f_ley = ImageFont.truetype(F, 10 * ESC)
    f_leyb = ImageFont.truetype(FB, 10.5 * ESC)
    f_cab = ImageFont.truetype(FB, 12.5 * ESC)
    f_col = ImageFont.truetype(F, 11 * ESC)
    f_colb = ImageFont.truetype(FB, 11 * ESC)
    f_tip = ImageFont.truetype(FM, 9.5 * ESC)
    f_not = ImageFont.truetype(F, 8.6 * ESC)
    f_mar = ImageFont.truetype(FB, 8.5 * ESC)

    def E(v):
        return v * ESC

    # franja de titulo
    d.rectangle([0, 0, E(W), E(40)], fill=HEX("0B0B0B"))
    d.text((E(20), E(11)), titulo, font=f_tit, fill=HEX("FFFFFF"))
    tw = d.textlength(subtitulo, font=f_sub)
    d.text((E(W - 20) - tw, E(15)), subtitulo, font=f_sub, fill=HEX("D9D9D9"))

    # leyenda
    lx, ly = 20, 60
    for i, t in enumerate(LEYENDA[modo]):
        d.text((E(lx), E(ly + i * 15)), t, font=f_leyb if i == 0 else f_ley, fill=HEX("101010"))

    # tablas
    caja = {}
    for tab in M.ORDER:
        x, y, w = POS[tab]
        cols = M.TABLES[tab]["cols"]
        mostrar = [cols[i - 1] for i in FILAS[tab]]
        h = alto(tab, modo)
        caja[tab] = (x, y, w, h)
        cab = AZUL_CAB if modo == "logico" else BEIGE_CAB
        if tab == "STOCK_ALMACEN":
            cab = "#C6E0B4" if modo == "logico" else BEIGE_CAB
        d.rectangle([E(x), E(y), E(x + w), E(y + h)], fill="#FCFCFD", outline=GRIS_BORDE)
        d.rectangle([E(x), E(y), E(x + w), E(y + 26)], fill=cab, outline=GRIS_BORDE)
        tw = d.textlength(tab, font=f_cab)
        d.text((E(x + w / 2) - tw / 2, E(y + 6)), tab, font=f_cab, fill=HEX("10233A"))
        yy = y + 26
        for col in mostrar:
            nombre, tdat, largo, marca, opc = col
            d.rectangle([E(x), E(yy), E(x + w), E(yy + 18)], outline=HEX("E3E8EB"))
            fg, tx, et = COL_MARCA[marca if marca else "-"]
            if et:
                d.rectangle([E(x + 4), E(yy + 3), E(x + 4 + 26), E(yy + 15)], fill=fg)
                twm = d.textlength(et, font=f_mar)
                d.text((E(x + 4 + 13) - twm / 2, E(yy + 4)), et, font=f_mar, fill=tx)
                nx = x + 36
            else:
                nx = x + 10
            ancho_tipo = 0
            if modo != "logico":
                ancho_tipo = d.textlength(tipo(col, modo), font=f_tip) / ESC + (34 if opc else 0) + 10
            disp = (x + w - 8) - nx - ancho_tipo
            fuente = f_colb if marca else f_col
            for tam in (11, 10.4, 9.8, 9.2, 8.6):
                fuente = ImageFont.truetype(FB if marca else F, tam * ESC)
                if d.textlength(nombre, font=fuente) / ESC <= disp:
                    break
            d.text((E(nx), E(yy + 3)), nombre, font=fuente, fill=HEX("101621"))
            # a la derecha: tipo de dato (relacional y fisico) o marca de NULL
            if modo == "logico":
                if opc:
                    et2 = "OPCIONAL / NULL"
                    tw2 = d.textlength(et2, font=f_tip)
                    d.text((E(x + w - 8) - tw2, E(yy + 3)), et2, font=f_tip, fill=HEX("8A6D3B"))
            else:
                tp = tipo(col, modo)
                tw2 = d.textlength(tp, font=f_tip)
                d.text((E(x + w - 8) - tw2, E(yy + 3)), tp, font=f_tip, fill=HEX("1B2A38"))
                if opc:
                    d.text((E(x + w - 8) - tw2 - E(34), E(yy + 3)), "NULL", font=f_tip, fill=HEX("8A6D3B"))
            yy += 18
        yy += 4
        for nota in NOTAS[tab]:
            d.text((E(x + 4), E(yy)), nota, font=f_not, fill=HEX("2E3A45"))
            yy += 12

    # relaciones
    def punto_union(tab, col, otro_caja):
        """Punto sobre el borde de la tabla mas cercano a la tabla destino."""
        x, y, w, h = caja[tab]
        ox, oy, ow, oh = otro_caja
        cx, cy = x + w / 2, y + h / 2
        ocx, ocy = ox + ow / 2, oy + oh / 2
        if abs(ocx - cx) > abs(ocy - cy):
            return (x + w, cy) if ocx > cx else (x, cy)
        return (x + w / 2, y + h) if ocy > cy else (x + w / 2, y)

    def cabeza(x, y, hacia, muchos):
        """Simbolo de cardinalidad: pata de gallo (muchos) o raya (uno)."""
        dx, dy = hacia
        # se separa del borde siguiendo el sentido del trazo (nunca hacia adentro)
        if dx:
            x += 15 * dx
        else:
            y += 15 * dy
        if not muchos:
            if dx:
                d.line([E(x), E(y - 8), E(x), E(y + 8)], fill=HEX("1B2A38"), width=ESC * 2)
            else:
                d.line([E(x - 8), E(y), E(x + 8), E(y)], fill=HEX("1B2A38"), width=ESC * 2)
            return
        if dx:  # entrada horizontal
            s = 1 if dx > 0 else -1
            for k in (-6, 0, 6):
                d.line([E(x), E(y), E(x - s * 12), E(y + k)], fill=HEX("1B2A38"), width=ESC * 2)
        else:
            s = 1 if dy > 0 else -1
            for k in (-6, 0, 6):
                d.line([E(x), E(y), E(x + k), E(y - s * 12)], fill=HEX("1B2A38"), width=ESC * 2)

    for padre, col, hijo, camino in LINEAS:
        cp, ch = caja[padre], caja[hijo]
        if camino is None:
            if padre == "CATEGORIA":
                p = (cp[0] + cp[2] / 2, cp[1] + cp[3])
                q = (ch[0] + ch[2] / 2, ch[1])
                d.line([E(p[0]), E(p[1]), E(q[0]), E(q[1])], fill=HEX("1B2A38"), width=ESC * 2)
                cabeza(p[0], p[1], (0, 1), False)
                cabeza(q[0], q[1], (0, -1), True)
                continue
            if padre == "SUMINISTRO" and hijo == "PEDIDO":
                p = (ch[0] + ch[2] / 2, ch[1] + ch[3])
                q = (cp[0] + cp[2] / 2, cp[1])
                d.line([E(p[0]), E(p[1]), E(q[0]), E(q[1])], fill=HEX("1B2A38"), width=ESC * 2)
                cabeza(p[0], p[1], (0, 1), True)
                cabeza(q[0], q[1], (0, -1), False)
                continue
            p = punto_union(padre, None, ch)
            q = punto_union(hijo, None, cp)
            d.line([E(p[0]), E(p[1]), E(q[0]), E(q[1])], fill=HEX("1B2A38"), width=ESC * 2)
            cabeza(p[0], p[1], (1 if q[0] > p[0] else -1, 0), False)
            cabeza(q[0], q[1], (1 if p[0] > q[0] else -1, 0), True)
            continue
        pts = camino
        d.line([(E(a), E(b)) for a, b in pts], fill=HEX("1B2A38"), width=ESC * 2, joint="curve")
        cabeza(pts[-1][0], pts[-1][1], (0, -1 if pts[-1][1] > pts[-2][1] else 1), True)
        cabeza(pts[0][0], pts[0][1], (0, 1 if pts[1][1] > pts[0][1] else -1), False)

    img.save(ruta)
    return ruta, img.size


def main():
    nivel_logico = M.PROJ + "/nivel_logico/"
    nivel_fisico = M.PROJ + "/nivel_fisico/"
    os.makedirs(nivel_logico, exist_ok=True)
    print(dibujar("logico", nivel_logico + "MODELO_LOGICO.png", H=848))
    # las de relacion/fisico son mas altas: se les agrega aire abajo
    print(dibujar("relacional", nivel_logico + "MODELO_RELACIONAL.png", H=903))
    print(dibujar("fisico", nivel_fisico + "MODELO_FISICO.png", H=903))
    # lamina conjunta para el nivel conceptual / anexos: logico + relacional
    a = Image.open(nivel_logico + "MODELO_LOGICO.png")
    b = Image.open(nivel_logico + "MODELO_RELACIONAL.png")
    H = a.height + b.height
    placa = Image.new("RGB", (max(a.width, b.width), H), "white")
    placa.paste(a, (0, 0))
    placa.paste(b, (0, a.height))
    placa.save(nivel_logico + "ORACLE_DATA_MODELER_NIKE_GRUPO_5.png")
    print("placa", placa.size)


if __name__ == "__main__":
    main()
