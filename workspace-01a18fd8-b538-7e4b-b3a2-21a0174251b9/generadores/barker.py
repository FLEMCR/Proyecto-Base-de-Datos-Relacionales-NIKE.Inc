# -*- coding: utf-8 -*-
"""Modelo logico en notacion Barker.

  * 7 entidades y sus relaciones. Las tres relaciones M:N del MER (CONTIENE,
    INCLUYE, ALMACENA) se dibujan COMO RELACIONES -no como tablas-, con su verbo,
    su cardinalidad M / N y los atributos que le pertenecen (talla, color,
    cantidad, precio). Asi el logico solo configura y no muestra intermedias.
  * En esas relaciones se subrayan talla y color: junto con las claves de las dos
    entidades forman la clave compuesta de la tabla que aparece en el relacional.
  * Las 1:N van con "1" del lado uno (raya) y "N" del lado muchos (pata de gallo).
  * Sin atributos calculados, sin vistas y sin marcas de origen opcional.
"""
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/user/generadores")
import modelo_final as M

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

NEGRO, AZUL, GRIS, BORDE = "#111417", "#1F4E79", "#5A646B", "#7E878D"
CREMA, CREMA_B, VERDE = "#FFF2CC", "#D8C48A", "#EDF3E7"

W, H, ESC = 2060, 1130, 2
CW = 300

# entidad -> (x, y)
POS = {
    "CLIENTE": (20, 150),
    "PEDIDO": (460, 150),
    "PRODUCTO": (1240, 150),
    "CATEGORIA": (1700, 150),
    "LOCAL": (20, 700),
    "SUMINISTRO": (460, 700),
    "ALMACEN": (1240, 700),
}

# relaciones 1:N: (padre, hija, verbo, puntos desde el borde del padre hasta el de la hija)
UNO_A_MUCHOS = [
    ("CLIENTE", "PEDIDO", "REALIZA", [(320, 220), (460, 220)]),
    ("CATEGORIA", "PRODUCTO", "CLASIFICA", [(1700, 220), (1540, 220)]),
    ("PEDIDO", "SUMINISTRO", "PROVEE", [(600, 310), (600, 700)]),
    ("LOCAL", "SUMINISTRO", "RECIBE", [(320, 770), (460, 770)]),
    ("SUMINISTRO", "ALMACEN", "ABASTECE",
     [(610, 841), (610, 961), (1190, 961), (1190, 780), (1240, 780)]),
]

# relaciones M:N: (entidad_a, entidad_b, verbo, rombo (x,y,w,h), ruta A->rombo, ruta rombo->B,
#                   atributos (nombre, forma_parte_de_la_clave, x, y))
MUCHOS_A_MUCHOS = [
    ("PEDIDO", "PRODUCTO", "CONTIENE", (900, 150, 200, 140),
     [(760, 220), (900, 220)], [(1100, 220), (1240, 220)],
     [("talla_elegida", True, 1000, 332), ("color_elegido", True, 1000, 378),
      ("cantidad", False, 1000, 424), ("precio_unitario_aplicado", False, 1000, 470)]),
    ("SUMINISTRO", "PRODUCTO", "INCLUYE", (900, 700, 200, 140),
     [(760, 770), (900, 770)], [(1100, 770), (1112, 770), (1112, 350), (1320, 350), (1320, 310)],
     [("talla", True, 1000, 560), ("color", True, 1000, 606), ("cantidad", False, 1000, 652)]),
    ("PRODUCTO", "ALMACEN", "ALMACENA", (1300, 420, 200, 140),
     [(1400, 310), (1400, 420)], [(1400, 560), (1400, 700)],
     [("talla", True, 1660, 430), ("color", True, 1660, 476),
      ("stock_actual", False, 1660, 522), ("stock_minimo", False, 1660, 568)]),
]


def alto(tab):
    return 32 + 19 * len(M.TABLES[tab]["cols"]) + 14


def caja(tab):
    x, y = POS[tab]
    return x, y, CW, alto(tab)


def centro(tab):
    x, y, w, h = caja(tab)
    return x + w / 2.0, y + h / 2.0


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
    f_ent = ImageFont.truetype(FB, 13 * ESC)
    f_atr = ImageFont.truetype(F, 11 * ESC)
    f_atrb = ImageFont.truetype(FB, 11 * ESC)
    f_mar = ImageFont.truetype(FB, 8.5 * ESC)
    f_tip = ImageFont.truetype(FM, 9.5 * ESC)
    f_rel = ImageFont.truetype(FB, 11.5 * ESC)
    f_card = ImageFont.truetype(FB, 13 * ESC)
    f_ley = ImageFont.truetype(F, 10.5 * ESC)
    f_leyb = ImageFont.truetype(FB, 11.5 * ESC)
    f_ficha = ImageFont.truetype(F, 10 * ESC)
    f_fichab = ImageFont.truetype(FB, 10 * ESC)

    def E(v):
        return v * ESC

    def texto(x, y, txt, fuente, color=NEGRO, centro_x=False):
        tw = d.textlength(txt, font=fuente)
        d.text((E(x) - (tw / 2 if centro_x else 0), E(y)), txt, font=fuente, fill=color)

    d.text((E(40), E(26)), "MODELO LOGICO - BD NIKE Inc. (Grupo 05)", font=f_tit, fill=NEGRO)
    d.text((E(40), E(62)),
           "Notacion Barker. Las relaciones de muchos a muchos se escriben como relacion, con su verbo, "
           "su cardinalidad M / N y sus propios atributos.", font=f_sub, fill=GRIS)

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

    def verbo_en(p0, p1, txt):
        (ax, ay), (bx, by) = p0, p1
        tw = d.textlength(txt, font=f_rel)
        if abs(ax - bx) < 1:
            mx, my = ax, (ay + by) / 2.0
            d.rectangle([E(mx + 9), E(my - 9), E(mx + tw + 15), E(my + 9)], fill="white")
            texto(mx + 12, my - 8, txt, f_rel)
        else:
            mx, my = (ax + bx) / 2.0, ay
            d.rectangle([E(mx - tw / 2 - 8), E(my - 30), E(mx + tw / 2 + 8), E(my - 12)],
                        fill="white")
            texto(mx, my - 29, txt, f_rel, centro_x=True)

    # ------------------------------------------------------- relaciones 1:N
    for padre, hija, verbo, pts in UNO_A_MUCHOS:
        d.line([(E(a), E(b)) for a, b in pts], fill=NEGRO, width=2 * ESC, joint="curve")
        (x1, y1), (x2, y2) = pts[0], pts[1]
        if abs(x1 - x2) < 1:                          # arranca vertical
            barra(x1, y1 + (10 if y2 > y1 else -10), vertical=True)
            texto(x1 + 10, y1 + (16 if y2 > y1 else -30), "1", f_card)
        else:
            s = 1 if x2 > x1 else -1
            barra(x1 + 10 * s, y1, vertical=False)
            texto(x1 + (14 if s > 0 else -26), y1 + 10, "1", f_card)
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        if abs(x1 - x2) < 1:                          # llega vertical
            gallo(x2, y2, vertical=True, sentido=-1 if y2 > y1 else 1)
            texto(x2 + 10, y2 - 32 if y2 > y1 else y2 + 16, "N", f_card)
        else:
            s = 1 if x2 > x1 else -1
            gallo(x2, y2, vertical=False, sentido=s)
            texto(x2 - (26 if s > 0 else -8), y2 + 10, "N", f_card)
        # verbo sobre el tramo mas largo
        mejor, largo = 0, -1
        for i in range(len(pts) - 1):
            L = abs(pts[i][0] - pts[i + 1][0]) + abs(pts[i][1] - pts[i + 1][1])
            if L > largo:
                mejor, largo = i, L
        verbo_en(pts[mejor], pts[mejor + 1], verbo)

    # ------------------------------------------------------- relaciones M:N
    for (a, b, verbo, rombo, ruta_a, ruta_b, atributos) in MUCHOS_A_MUCHOS:
        rx, ry, rw, rh = rombo
        cx, cy = rx + rw / 2.0, ry + rh / 2.0
        d.line([(E(p[0]), E(p[1])) for p in ruta_a], fill=NEGRO, width=2 * ESC)
        d.line([(E(p[0]), E(p[1])) for p in ruta_b], fill=NEGRO, width=2 * ESC, joint="curve")
        # cardinalidad M del lado de la entidad A y N del lado de la entidad B
        ax, ay = ruta_a[0]
        texto(ax + 14, ay - 30, "M", f_card)
        bx, by = ruta_b[-1]
        px, py = ruta_b[-2]
        if abs(px - bx) > 1:
            texto(bx - (30 if bx > px else -14), by - 30, "N", f_card)
        else:
            texto(bx + 14, by + (12 if by < py else -34), "N", f_card)
        # atributos de la relacion, conectados al rombo
        for nombre, es_clave, x, y in atributos:
            ancho = max(96, int(len(nombre) * 7.0) + 30)
            alto_e = 34
            if abs(x - cx) < 6:
                d.line([E(x), E(y + (alto_e / 2 if y < cy else -alto_e / 2)), E(x),
                        E(cy + (rh / 2.0 if y < cy else -rh / 2.0))], fill=NEGRO, width=ESC)
            else:
                d.line([E(x), E(y), E(cx + (rw / 2.0 if x > cx else -rw / 2.0)), E(y)],
                       fill=NEGRO, width=ESC)
            d.ellipse([E(x - ancho / 2), E(y - alto_e / 2), E(x + ancho / 2), E(y + alto_e / 2)],
                      fill="white", outline=NEGRO, width=max(1, ESC))
            tw = d.textlength(nombre, font=f_atr)
            d.text((E(x) - tw / 2, E(y) - 7 * ESC), nombre, font=f_atr, fill=NEGRO)
            if es_clave:
                d.line([E(x) - tw / 2, E(y) + 6 * ESC, E(x) + tw / 2, E(y) + 6 * ESC],
                       fill=NEGRO, width=max(1, ESC))
        # rombo con el verbo
        pts = [(E(cx), E(ry)), (E(rx + rw), E(cy)), (E(cx), E(ry + rh)), (E(rx), E(cy))]
        d.polygon(pts, fill="white", outline=NEGRO)
        d.line(pts + [pts[0]], fill=NEGRO, width=2 * ESC)
        texto(cx, cy - 8, verbo, f_rel, centro_x=True)

    # ------------------------------------------------------------ entidades
    for tab in POS:
        x, y, w, h = caja(tab)
        d.rectangle([E(x), E(y), E(x + w), E(y + h)], fill="white", outline=BORDE, width=2 * ESC)
        d.rectangle([E(x), E(y), E(x + w), E(y + 32)], fill=AZUL, outline=BORDE, width=2 * ESC)
        texto(x + w / 2, y + 9, tab, f_ent, "white", centro_x=True)
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
            texto(x0, yy, col[0], fuente)
            t = tipo_txt(col)
            tw = d.textlength(t, font=f_tip)
            d.text((E(x + w - 12) - tw, E(yy + 1)), t, font=f_tip, fill=GRIS)
            yy += 19

    # -------------------------------------------------------------- leyenda
    ly = 1000
    d.text((E(40), E(ly)), "COMO LEER", font=f_leyb, fill=NEGRO)
    filas = [
        ("1", "uno y solo uno (raya):  cada PEDIDO es de un solo CLIENTE"),
        ("N", "uno o muchos (pata de gallo):  un CLIENTE realiza uno o muchos PEDIDOS"),
        ("M / N", "muchos a muchos:  el rombo lleva sus propios atributos"),
        ("subrayado", "en las entidades: PK.  En un rombo M:N: atributo que forma la clave compuesta"),
    ]
    yy = ly + 22
    for a, b in filas:
        texto(44, yy, a, f_rel)
        texto(170, yy, b, f_ley, GRIS)
        yy += 20
    texto(40, ly + 118, "PROVEE (1:N): un SUMINISTRO atiende muchos PEDIDOS y cada PEDIDO se atiende con uno solo.", f_ley, GRIS)
    texto(40, ly + 138, "El estado del envio no se guarda: se deduce del estado del despacho del suministro.", f_ley, GRIS)

    img.save(salida)
    return img.size


def verificar():
    problemas = []
    cajas = {t: caja(t) for t in POS}
    rombos = [(m[3][0], m[3][1], m[3][2], m[3][3]) for m in MUCHOS_A_MUCHOS]
    fichas = []
    for m in MUCHOS_A_MUCHOS:
        for nombre, es_clave, x, y in m[6]:
            ancho = max(96, int(len(nombre) * 7.0) + 30)
            fichas.append((x - ancho / 2, y - 17, ancho, 34))

    def choca(p0, p1, c, tol=4):
        x, y, w, h = c
        for k in range(101):
            px = p0[0] + (p1[0] - p0[0]) * k / 100.0
            py = p0[1] + (p1[1] - p0[1]) * k / 100.0
            if x + tol < px < x + w - tol and y + tol < py < y + h - tol:
                return True
        return False

    tramos = []
    for padre, hija, verbo, pts in UNO_A_MUCHOS:
        for i in range(len(pts) - 1):
            tramos.append(("1:N " + verbo, pts[i], pts[i + 1]))
    for a, b, verbo, rombo, ra, rb, attrs in MUCHOS_A_MUCHOS:
        tramos.append(("M:N " + verbo + " (A)", ra[0], ra[1]))
        for i in range(len(rb) - 1):
            tramos.append(("M:N " + verbo + " (B)", rb[i], rb[i + 1]))

    for nombre, p0, p1 in tramos:
        for t, c in cajas.items():
            if choca(p0, p1, c):
                problemas.append("%s cruza la caja %s" % (nombre, t))
        for i, r in enumerate(rombos):
            if choca(p0, p1, r, tol=8):
                problemas.append("%s cruza el rombo %d" % (nombre, i))
        for i, f in enumerate(fichas):
            if choca(p0, p1, f, tol=6):
                problemas.append("%s cruza la ficha %d" % (nombre, i))

    # cajas / rombos / fichas que se encimen entre si
    bloques = [("caja " + t, c) for t, c in cajas.items()]
    bloques += [("rombo %d" % i, r) for i, r in enumerate(rombos)]
    bloques += [("ficha %d" % i, f) for i, f in enumerate(fichas)]
    for i in range(len(bloques)):
        for j in range(i + 1, len(bloques)):
            (na, a), (nb, b) = bloques[i], bloques[j]
            if (a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and
                    a[1] < b[1] + b[3] and b[1] < a[1] + a[3]):
                problemas.append("%s y %s se enciman" % (na, nb))
    return problemas


if __name__ == "__main__":
    print("verificacion:", verificar() or "sin problemas")
    print(dibujar(M.PROJ + "/nivel_logico/MODELO_LOGICO.png"))
