# -*- coding: utf-8 -*-
"""Modelo relacional: las 10 tablas con sus PK, FK y las 11 relaciones resueltas.

Es el paso siguiente al modelo logico: aqui las tres relaciones M:N del MER ya
aparecen como tablas (DETALLE_VENTA, STOCK_ALMACEN y DETALLE_SUMINISTRO).
Cada linea sale del lado 1 y llega con pata de gallo al lado muchos, con el
nombre del verbo y la cardinalidad.
"""
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/user/generadores")
import modelo_final as M

F = "/home/user/fonts/DejaVuSans.ttf"
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

NEGRO, AZUL, GRIS, BORDE = "#111417", "#1F4E79", "#5A646B", "#7E878D"
CREMA, CREMA_B = "#FFF2CC", "#D8C48A"

W, H, ESC = 2290, 1050, 2
CW = 320
Y1, Y2 = 120, 560
POS = {
    "CLIENTE": (24, Y1), "PEDIDO": (504, Y1), "DETALLE_VENTA": (984, Y1),
    "PRODUCTO": (1464, Y1), "CATEGORIA": (1944, Y1),
    "LOCAL": (24, Y2), "SUMINISTRO": (504, Y2), "DETALLE_SUMINISTRO": (984, Y2),
    "ALMACEN": (1464, Y2), "STOCK_ALMACEN": (1944, Y2),
}

# (padre, hija, verbo, ruta completa desde el borde del padre hasta el borde de la hija)
REL = [
    ("CLIENTE", "PEDIDO", "REALIZA", [(344, 205), (504, 205)]),
    ("PEDIDO", "DETALLE_VENTA", "CONTIENE", [(824, 200), (984, 200)]),
    ("PRODUCTO", "DETALLE_VENTA", "CONTIENE", [(1464, 200), (1304, 200)]),
    ("CATEGORIA", "PRODUCTO", "CLASIFICA", [(1944, 171), (1784, 171)]),
    ("LOCAL", "SUMINISTRO", "RECIBE", [(344, 620), (504, 620)]),
    ("SUMINISTRO", "DETALLE_SUMINISTRO", "INCLUYE", [(824, 640), (984, 640)]),
    ("ALMACEN", "STOCK_ALMACEN", "ALMACENA", [(1784, 640), (1944, 640)]),
    ("SUMINISTRO", "PEDIDO", "PROVEE", [(654, 560), (654, 299)]),
    ("PRODUCTO", "DETALLE_SUMINISTRO", "INCLUYE",
     [(1554, 281), (1554, 330), (1134, 330), (1134, 560)]),
    ("PRODUCTO", "STOCK_ALMACEN", "ALMACENA",
     [(1694, 281), (1694, 450), (2174, 450), (2174, 560)]),
    ("ALMACEN", "SUMINISTRO", "ABASTECE",
     [(1614, 663), (1614, 790), (554, 790), (554, 701)]),
]


def alto(tab):
    return 32 + 19 * len(M.TABLES[tab]["cols"]) + 14


def caja(tab):
    x, y = POS[tab]
    return x, y, CW, alto(tab)


def marca(col):
    nombre, tipo, largo, m, opc = col
    if m == "PFK":
        return "PK,FK"
    return {"PK": "PK", "FK": "FK"}.get(m, "o" if opc else "*")


def tipo_txt(col):
    nombre, t, largo, m, opc = col
    if t == "VARCHAR":
        return "VARCHAR(%d)" % largo
    if t == "DECIMAL":
        return "DECIMAL(%d,%d)" % largo
    return t


def dibujar(salida):
    img = Image.new("RGB", (W * ESC, H * ESC), "white")
    d = ImageDraw.Draw(img)
    f_tit = ImageFont.truetype(FB, 26 * ESC)
    f_sub = ImageFont.truetype(F, 12.5 * ESC)
    f_ent = ImageFont.truetype(FB, 12.5 * ESC)
    f_atr = ImageFont.truetype(F, 10 * ESC)
    f_atrb = ImageFont.truetype(FB, 10 * ESC)
    f_mar = ImageFont.truetype(FB, 8 * ESC)
    f_tip = ImageFont.truetype(FM, 9 * ESC)
    f_rel = ImageFont.truetype(FB, 11 * ESC)
    f_card = ImageFont.truetype(FB, 12 * ESC)
    f_ley = ImageFont.truetype(F, 10.5 * ESC)
    f_leyb = ImageFont.truetype(FB, 11.5 * ESC)

    def E(v):
        return v * ESC

    d.text((E(24), E(26)), "MODELO RELACIONAL - BD NIKE Inc. (Grupo 05)", font=f_tit, fill=NEGRO)
    d.text((E(24), E(60)),
           "Las 10 tablas, sus claves y las 11 relaciones ya resueltas: cada relacion M:N del MER es "
           "ahora una tabla intermedia.", font=f_sub, fill=GRIS)

    def barra(x, y, vertical):
        if vertical:
            d.line([E(x - 9), E(y), E(x + 9), E(y)], fill=NEGRO, width=2 * ESC)
        else:
            d.line([E(x), E(y - 9), E(x), E(y + 9)], fill=NEGRO, width=2 * ESC)

    def gallo(x, y, vertical, sentido):
        if vertical:
            vx, vy = x, y - sentido * 13
            for dx in (-11, 0, 11):
                d.line([E(vx), E(vy), E(x + dx), E(y)], fill=NEGRO, width=2 * ESC)
        else:
            vx, vy = x - sentido * 13, y
            for dy in (-11, 0, 11):
                d.line([E(vx), E(vy), E(x), E(y + dy)], fill=NEGRO, width=2 * ESC)

    def texto(x, y, txt, fuente, color=NEGRO, centro=False):
        tw = d.textlength(txt, font=fuente)
        d.text((E(x) - (tw / 2 if centro else 0), E(y)), txt, font=fuente, fill=color)

    for padre, hija, verbo, pts in REL:
        d.line([(E(a), E(b)) for a, b in pts], fill=NEGRO, width=2 * ESC, joint="curve")
        # extremo del padre: lado 1 (raya)
        (x1, y1), (x2, y2) = pts[0], pts[1]
        if abs(x1 - x2) < 1:                      # tramo vertical
            barra(x1, y1 + (10 if y2 > y1 else -10), vertical=True)
            texto(x1 + 10, y1 + (16 if y2 > y1 else -28), "1", f_card)
        else:                                     # tramo horizontal
            barra(x1 + (10 if x2 > x1 else -10), y1, vertical=False)
            texto(x1 + (16 if x2 > x1 else -24), y1 - 24, "1", f_card)
        # extremo de la hija: lado N (pata de gallo)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        if abs(x1 - x2) < 1:
            gallo(x2, y2, vertical=True, sentido=-1 if y2 > y1 else 1)
            texto(x2 + 10, y2 - 30 if y2 > y1 else y2 + 16, "N", f_card)
        else:
            gallo(x2, y2, vertical=False, sentido=1 if x2 > x1 else -1)
            texto(x2 - (26 if x2 > x1 else -12), y2 - 24, "N", f_card)
        # nombre del verbo sobre el tramo mas largo de la ruta
        mejor, largo = 0, -1
        for i in range(len(pts) - 1):
            L = abs(pts[i][0] - pts[i + 1][0]) + abs(pts[i][1] - pts[i + 1][1])
            if L > largo:
                mejor, largo = i, L
        (ax, ay), (bx, by) = pts[mejor], pts[mejor + 1]
        tw = d.textlength(verbo, font=f_rel)
        if abs(ax - bx) < 1:                       # tramo vertical
            mx, my = ax, (ay + by) / 2.0
            d.rectangle([E(mx + 8), E(my - 9), E(mx + tw + 14), E(my + 9)], fill="white")
            texto(mx + 11, my - 8, verbo, f_rel)
        else:                                      # tramo horizontal
            mx, my = (ax + bx) / 2.0, ay
            d.rectangle([E(mx - tw / 2 - 8), E(my - 10), E(mx + tw / 2 + 8), E(my + 10)],
                        fill="white")
            texto(mx, my - 9, verbo, f_rel, centro=True)

    for tab in POS:
        x, y, w, h = caja(tab)
        d.rectangle([E(x), E(y), E(x + w), E(y + h)], fill="white", outline=BORDE, width=2 * ESC)
        d.rectangle([E(x), E(y), E(x + w), E(y + 32)], fill=AZUL, outline=BORDE, width=2 * ESC)
        tw = d.textlength(tab, font=f_ent)
        d.text((E(x + w / 2) - tw / 2, E(y + 9)), tab, font=f_ent, fill="white")
        yy = y + 38
        for col in M.TABLES[tab]["cols"]:
            mk = marca(col)
            if mk != "*" and mk != "o":
                ancho = 46 if mk == "PK,FK" else (28 if mk == "FK" else 26)
                d.rectangle([E(x + 8), E(yy - 1), E(x + 8 + ancho), E(yy + 15)], fill=CREMA,
                            outline=CREMA_B)
                tw = d.textlength(mk, font=f_mar)
                d.text((E(x + 8 + ancho / 2) - tw / 2, E(yy + 1)), mk, font=f_mar, fill=NEGRO)
                x0, fuente = x + 8 + ancho + 9, f_atrb
            else:
                d.text((E(x + 14), E(yy + 1)), mk, font=f_mar, fill=GRIS)
                x0, fuente = x + 34, f_atr
            d.text((E(x0), E(yy)), col[0], font=fuente, fill=NEGRO)
            t = tipo_txt(col)
            tw = d.textlength(t, font=f_tip)
            d.text((E(x + w - 12) - tw, E(yy + 1)), t, font=f_tip, fill=GRIS)
            yy += 19

    # leyenda
    ly = 850
    d.text((E(24), E(ly)), "COMO LEER", font=f_leyb, fill=NEGRO)
    filas = [("1", "uno y solo uno: el lado de la tabla maestra (con la raya)"),
             ("N", "uno o muchos: el lado de la tabla que guarda la clave foranea (pata de gallo)"),
             ("PK / FK", "clave primaria y clave foranea; PK,FK es clave compuesta y ademas foranea"),
             ("* / o", "obligatorio / admite NULL (solo telefono_secundario, descripcion y especificaciones)")]
    yy = ly + 24
    for a, b in filas:
        texto(30, yy, a, f_rel)
        texto(130, yy, b, f_ley, GRIS)
        yy += 22
    d.text((E(24), E(ly + 118)),
           "Ninguna tabla guarda valores calculados: el total de la linea (cantidad x "
           "precio_unitario_aplicado) y el IGV (18 %) se calculan en las consultas.",
           font=f_ley, fill=GRIS)
    d.text((E(24), E(ly + 140)),
           "PEDIDO.SUMINISTRO_id_suministro es una sola columna obligatoria: cada pedido se atiende con "
           "un solo suministro, o sea con un almacen y un local.", font=f_ley, fill=GRIS)
    d.text((E(24), E(ly + 162)),
           "PEDIDO no guarda estado_envio: se deduce del estado_despacho del suministro "
           "(PENDIENTE = PROGRAMADO, ENVIADO = EN RUTA, ENTREGADO = ENTREGADO).", font=f_ley, fill=GRIS)

    img.save(salida)
    return img.size


def verificar():
    problemas = []
    cajas = {t: caja(t) for t in POS}

    def dentro(px, py, c, tol=4):
        x, y, w, h = c
        return x + tol < px < x + w - tol and y + tol < py < y + h - tol

    for padre, hija, verbo, pts in REL:
        for i in range(len(pts) - 1):
            for t, c in cajas.items():
                if t in (padre, hija):
                    continue
                choque = False
                for k in range(0, 101):
                    px = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * k / 100.0
                    py = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * k / 100.0
                    if dentro(px, py, c):
                        choque = True
                        break
                if choque:
                    problemas.append("%s-%s (%s) cruza %s" % (padre, hija, verbo, t))
    nombres = list(POS)
    for i in range(len(nombres)):
        for j in range(i + 1, len(nombres)):
            a, b = cajas[nombres[i]], cajas[nombres[j]]
            if (a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and
                    a[1] < b[1] + b[3] and b[1] < a[1] + a[3]):
                problemas.append("%s y %s se enciman" % (nombres[i], nombres[j]))
    return problemas


if __name__ == "__main__":
    print("verificacion:", verificar() or "sin problemas")
    print(dibujar(M.PROJ + "/nivel_logico/MODELO_RELACIONAL.png"))
