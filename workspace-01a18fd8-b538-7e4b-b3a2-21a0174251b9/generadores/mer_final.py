# -*- coding: utf-8 -*-
"""MER de NIKE Inc. con la composicion del diagrama aprobado por el grupo.

- 1:N (REALIZA, CLASIFICA, RECIBE, ABASTECE, PROVEE): flecha hacia la entidad "1".
- M:N (CONTIENE, ALMACENA, INCLUYE): rombo con sus atributos y SIN flechas.
- Sin atributos calculados (no hay Total ni IGV).
Genera .png y .drawio, y verifica que no haya lineas cruzando figuras.
"""
import math
import os
import sys
import xml.sax.saxutils as sx

# ------------------------------------------------------------------ geometria
# entidades y rombos: nombre -> (x, y, w, h)
FIG = {
    "CATEGORIA":  (1150, 148, 110, 46),
    "CLIENTE":    (100, 424, 115, 46),
    "PEDIDO":     (525, 424, 115, 46),
    "CONTIENE":   (850, 400, 90, 90),
    "PRODUCTO":   (1170, 418, 115, 46),
    "CLASIFICA":  (1168, 266, 80, 80),
    "PROVEE":     (545, 590, 80, 80),
    "INCLUYE":    (895, 620, 84, 84),
    "SUMINISTRO": (455, 815, 115, 46),
    "ABASTECE":   (655, 800, 80, 80),
    "ALMACEN":    (860, 815, 115, 46),
    "ALMACENA":   (1160, 800, 84, 84),
    "RECIBE":     (280, 808, 76, 76),
    "LOCAL":      (100, 815, 110, 46),
}
ENTIDADES = ["CLIENTE", "PEDIDO", "PRODUCTO", "CATEGORIA", "ALMACEN", "LOCAL", "SUMINISTRO"]
ROMBOS = ["REALIZA", "CONTIENE", "CLASIFICA", "ALMACENA", "PROVEE", "ABASTECE", "RECIBE", "INCLUYE"]
FIG["REALIZA"] = (352, 405, 80, 80)

# lineas de la estructura: (a, b, punta)
#   punta = nombre de la figura hacia la que se dibuja la flecha (lado "1") o None
ENLACES = [
    ("CLIENTE", "REALIZA", None),
    ("REALIZA", "PEDIDO", "CLIENTE"),
    ("PEDIDO", "CONTIENE", None),
    ("CONTIENE", "PRODUCTO", None),
    ("PRODUCTO", "CLASIFICA", None),
    ("CLASIFICA", "CATEGORIA", "CATEGORIA"),
    ("PRODUCTO", "ALMACENA", None),
    ("ALMACENA", "ALMACEN", None),
    ("PEDIDO", "PROVEE", None),
    ("PROVEE", "SUMINISTRO", "SUMINISTRO"),
    ("ALMACEN", "ABASTECE", None),
    ("ABASTECE", "SUMINISTRO", "ALMACEN"),
    ("SUMINISTRO", "RECIBE", None),
    ("RECIBE", "LOCAL", "LOCAL"),
    ("SUMINISTRO", "INCLUYE", None),
    ("INCLUYE", "PRODUCTO", None),
]

CARD = {  # texto y posicion respecto al centro del rombo
    "REALIZA":   ("(1,N)", 0, 68),
    "CONTIENE":  ("(M,N)", 0, 66),
    "CLASIFICA": ("(1,N)", 66, 0),
    "ALMACENA":  ("(M,N)", 72, 0),
    "PROVEE":    ("(1,N)", 66, 0),
    "ABASTECE":  ("(1,N)", 0, 62),
    "RECIBE":    ("(1,N)", 0, -60),
    "INCLUYE":   ("(M,N)", 72, 0),
}

# atributos: duenno -> [(texto, pk, opcional, x, y)]   (x, y) = centro de la elipse
ATR = {
    "CLIENTE": [
        ("ID_CLIENTE", True, False, 225, 290),
        ("Nombre", False, False, 345, 330),
        ("Telefono", False, False, 105, 330),
        ("Correo_e", False, False, 105, 378),
        ("Telefono_secundario (opcional)", False, True, 108, 238),
        ("Direccion", False, False, 350, 226),
    ],
    "PEDIDO": [
        ("ID_PEDIDO", True, False, 665, 296),
        ("Fecha", False, False, 725, 258),
        ("Metodo_pago", False, False, 600, 338),
    ],
    "CONTIENE": [
        ("Talla_elegida", True, False, 1006, 208),
        ("Color_elegido", True, False, 1030, 330),
        ("Cantidad", False, False, 1030, 250),
        ("Precio_unitario_aplicado", False, False, 834, 342),
    ],
    "PRODUCTO": [
        ("ID_PRODUCTO", True, False, 1290, 385),
        ("Nombre", False, False, 1405, 393),
        ("Estado", False, False, 1330, 545),
        ("Especificaciones (opcional)", False, True, 1470, 433),
        ("Precio_unitario_base", False, False, 1470, 480),
    ],
    "CATEGORIA": [
        ("ID_CATEGORIA", True, False, 1250, 60),
        ("Nombre", False, False, 1112, 60),
        ("Descripcion (opcional)", False, True, 1000, 20),
    ],
    "INCLUYE": [
        ("Talla", True, False, 800, 578),
        ("Cantidad", False, False, 800, 620),
        ("Color", True, False, 800, 662),
    ],
    "SUMINISTRO": [
        ("ID_SUMINISTRO", True, False, 470, 955),
        ("Fecha_suministro", False, False, 447, 906),
        ("Estado_despacho", False, False, 600, 925),
    ],
    "ALMACEN": [
        ("ID_ALMACEN", True, False, 960, 935),
        ("Nombre_almacen", False, False, 900, 990),
        ("Ubicacion", False, False, 830, 905),
    ],
    "ALMACENA": [
        ("Talla", True, False, 1155, 930),
        ("Color", True, False, 1150, 975),
        ("Stock_actual", False, False, 1270, 930),
        ("Stock_minimo", False, False, 1270, 975),
    ],
    "LOCAL": [
        ("ID_LOCAL", True, False, 60, 935),
        ("Nombre_local", False, False, 135, 985),
        ("Direccion_local", False, False, 215, 935),
    ],
}

TITULO = "Diagrama M.E.R - NIKE. Inc"
SUBTITULO = "Ventas y Almacenes"
ESCALA = 3.0


def caja(n):
    return FIG[n]


def centro(n):
    x, y, w, h = FIG[n]
    return x + w / 2.0, y + h / 2.0


def ancho(txt):
    return max(96, int(len(txt) * 7.4) + 30)


# --------------------------------------------------------------- verificar
def choca(p0, p1, caja_r, tol=6):
    x, y, w, h = caja_r
    for k in range(101):
        t = k / 100.0
        px = p0[0] + (p1[0] - p0[0]) * t
        py = p0[1] + (p1[1] - p0[1]) * t
        if x + tol < px < x + w - tol and y + tol < py < y + h - tol:
            return True
    return False


def elipses():
    out = []
    for owner, lista in ATR.items():
        for txt, pk, opc, x, y in lista:
            out.append((owner, txt, x, y, ancho(txt), 40))
    return out


def verificar():
    fallos = []
    els = elipses()
    for i in range(len(els)):
        _, t1, x1, y1, w1, h1 = els[i]
        for j in range(i + 1, len(els)):
            _, t2, x2, y2, w2, h2 = els[j]
            if abs(x1 - x2) < (w1 + w2) / 2 - 4 and abs(y1 - y2) < (h1 + h2) / 2 - 4:
                fallos.append("elipses encimadas: %s / %s" % (t1, t2))
    # atributos contra figuras
    for owner, t, x, y, w, h in els:
        for n in FIG:
            if n == owner:
                continue
            fx, fy, fw, fh = FIG[n]
            if (x + w / 2 > fx - 4 and x - w / 2 < fx + fw + 4 and
                    y + h / 2 > fy - 4 and y - h / 2 < fy + fh + 4):
                fallos.append("la elipse %s se monta sobre %s" % (t, n))
    # lineas de estructura contra figuras
    for a, b, _ in ENLACES:
        ca, cb = centro(a), centro(b)
        for n in FIG:
            if n in (a, b):
                continue
            if choca(ca, cb, FIG[n], tol=8):
                fallos.append("la linea %s-%s cruza %s" % (a, b, n))
    return sorted(set(fallos))


# ------------------------------------------------------------------- dibujo
def trazo_atributo(d, X, Y, duenno, atr):
    """Conector ortogonal: del atributo a una linea comun (peine) y de ahi a la entidad."""
    x, y = atr
    cx, cy = centro(duenno)
    fx, fy, fw, fh = FIG[duenno]
    if duenno in ENTIDADES:
        arriba = y < fy
        bus = (fy - 26) if arriba else (fy + fh + 26)
        d.line([X(x), Y(y + (20 if arriba else -20)), X(x), Y(bus)], fill="black", width=1)
    else:
        n = math.hypot(x - cx, y - cy) or 1
        px, py = cx + (x - cx) / n * (fw * 0.40), cy + (y - cy) / n * (fh * 0.40)
        d.line([X(x), Y(y + (20 if y < cy else -20)), X(px), Y(py)], fill="black", width=1)


def peines(d, X, Y):
    """Dibuja la linea comun (bus) y la bajada a la entidad para cada entidad."""
    for n in ENTIDADES:
        arriba = [a for a in ATR.get(n, []) if a[4] < FIG[n][1]]
        abajo = [a for a in ATR.get(n, []) if a[4] >= FIG[n][1]]
        fx, fy, fw, fh = FIG[n]
        for grupo, bus, borde in ((arriba, fy - 26, fy), (abajo, fy + fh + 26, fy + fh)):
            if not grupo:
                continue
            xs = [a[3] for a in grupo]
            x0, x1 = min(xs), max(xs)
            d.line([X(x0), Y(bus), X(x1), Y(bus)], fill="black", width=1)
            entrada = min(max((x0 + x1) / 2.0, fx + 18), fx + fw - 18)
            d.line([X(entrada), Y(bus), X(entrada), Y(borde)], fill="black", width=1)


def borde_destino(a, b, destino):
    """Punto del borde de la figura destino en la direccion del segmento."""
    x, y, w, h = FIG[destino]
    cx, cy = centro(destino)
    vx, vy = cx - a[0], cy - a[1]
    if vx == 0 and vy == 0:
        return cx, cy
    t = min(
        (w / 2.0) / abs(vx) if vx else 1e9,
        (h / 2.0) / abs(vy) if vy else 1e9,
    )
    return cx - vx * t, cy - vy * t


def dibujar_png(ruta, escala=ESCALA):
    from PIL import Image, ImageDraw, ImageFont
    F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    f_ent = ImageFont.truetype(FB, int(14 * escala))
    f_rel = ImageFont.truetype(F, int(13 * escala))
    f_atr = ImageFont.truetype(F, int(12.5 * escala))
    f_tit = ImageFont.truetype(FB, int(32 * escala))
    f_sub = ImageFont.truetype(F, int(21 * escala))
    f_ley = ImageFont.truetype(F, int(12 * escala))
    f_leyb = ImageFont.truetype(FB, int(13 * escala))
    W = int(1600 * escala)
    H = int(1250 * escala)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    def X(v):
        return v * escala

    def Y(v):
        return v * escala

    d.text((X(232), Y(26)), TITULO, font=f_tit, fill="black")
    d.text((X(370), Y(112)), SUBTITULO, font=f_sub, fill="black")

    # atributos (elipses + trazo ortogonal)
    for duenno, lista in ATR.items():
        for txt, pk, opc, x, y in lista:
            trazo_atributo(d, X, Y, duenno, (x, y))
    peines(d, X, Y)
    for duenno, lista in ATR.items():
        for txt, pk, opc, x, y in lista:
            w, h = ancho(txt), 40
            if opc:
                # borde punteado = atributo que admite NULL
                paso, cx0 = 9, x - w / 2
                import math as _m
                for k in range(int(w / paso)):
                    a1 = 2 * _m.pi * (k / (w / paso))
                    a2 = 2 * _m.pi * ((k + 0.55) / (w / paso))
                    d.line([X(cx0 + (w / 2) * (1 + _m.cos(a1))), Y(y + (h / 2) * _m.sin(a1)),
                            X(cx0 + (w / 2) * (1 + _m.cos(a2))), Y(y + (h / 2) * _m.sin(a2))],
                           fill="black", width=max(1, int(1.1 * escala)))
            else:
                d.ellipse([X(x - w / 2), Y(y - h / 2), X(x + w / 2), Y(y + h / 2)],
                          fill="white", outline="black", width=max(1, int(1.1 * escala)))
            tw = d.textlength(txt, font=f_atr)
            d.text((X(x) - tw / 2, Y(y) - 6 * escala), txt, font=f_atr, fill="black")
            if pk:
                d.line([X(x) - tw / 2, Y(y) + 5.5 * escala, X(x) + tw / 2, Y(y) + 5.5 * escala],
                       fill="black", width=max(1, int(1.0 * escala)))

    # estructura
    flechas = []
    for a, b, punta in ENLACES:
        c1, c2 = centro(a), centro(b)
        d.line([X(c1[0]), Y(c1[1]), X(c2[0]), Y(c2[1])], fill="black", width=max(1, int(1.2 * escala)))
        if punta:
            flechas.append((a, b, punta))

    for n in ENTIDADES:
        x, y, w, h = FIG[n]
        d.rectangle([X(x), Y(y), X(x + w), Y(y + h)], fill="white", outline="black",
                    width=max(1, int(1.3 * escala)))
        tw = d.textlength(n, font=f_ent)
        d.text((X(x + w / 2) - tw / 2, Y(y + h / 2) - 7 * escala), n, font=f_ent, fill="black")
    for n in ROMBOS:
        x, y, w, h = FIG[n]
        pts = [(X(x + w / 2), Y(y)), (X(x + w), Y(y + h / 2)), (X(x + w / 2), Y(y + h)), (X(x), Y(y + h / 2))]
        d.polygon(pts, fill="white", outline="black")
        d.line(pts + [pts[0]], fill="black", width=max(1, int(1.3 * escala)))
        tw = d.textlength(n, font=f_rel)
        d.text((X(x + w / 2) - tw / 2, Y(y + h / 2) - 6 * escala), n, font=f_rel, fill="black")

    # puntas de flecha al final, para que ninguna figura las tape
    for a, b, punta in flechas:
        c1, c2 = centro(a), centro(b)
        origen = c1 if b == punta else c2
        destino = borde_destino(origen, None, punta)
        ang = math.atan2(destino[1] - origen[1], destino[0] - origen[0])
        L, A = 15, math.radians(24)
        p0 = (destino[0] - L * math.cos(ang - A), destino[1] - L * math.sin(ang - A))
        p1 = (destino[0] - L * math.cos(ang + A), destino[1] - L * math.sin(ang + A))
        d.polygon([(X(destino[0]), Y(destino[1])), (X(p0[0]), Y(p0[1])), (X(p1[0]), Y(p1[1]))],
                  fill="black")

    for rel, (txt, dx, dy) in CARD.items():
        cx, cy = centro(rel)
        tw = d.textlength(txt, font=f_rel)
        d.text((X(cx + dx) - tw / 2, Y(cy + dy) - 6 * escala), txt, font=f_rel, fill="black")

    # ---------------------------------------------------------- leyenda
    ly = 1006
    d.rectangle([X(60), Y(ly), X(1540), Y(ly + 190)], fill="white", outline="black",
                width=max(1, int(1.2 * escala)))
    d.text((X(78), Y(ly + 10)), "COMO LEER EL DIAGRAMA", font=f_leyb, fill="black")
    filas = [
        ("Entidad", "rectangulo", "Atributo", "elipse"),
        ("PK subrayada", "en entidades y en los rombos M:N", "Elipse punteada",
         "atributo que admite NULL"),
        ("(1,N)", "flecha hacia el lado 1", "(M,N)",
         "sin flecha, se resuelve en el relacional"),
    ]
    for k, (a, b, c, e) in enumerate(filas):
        yy = ly + 36 + k * 26
        d.text((X(84), Y(yy)), "\u2022 " + a + ":", font=f_ley, fill="black")
        d.text((X(330), Y(yy)), b, font=f_ley, fill="black")
        d.text((X(760), Y(yy)), "\u2022 " + c + ":", font=f_ley, fill="black")
        d.text((X(1030), Y(yy)), e, font=f_ley, fill="black")
    d.text((X(84), Y(ly + 118)),
           "INCLUYE detalla que productos, en que talla y color y cuantas unidades se envian al local; "
           "ALMACENA detalla el stock por talla y color.", font=f_ley, fill="black")
    d.text((X(84), Y(ly + 140)),
           "En los rombos M:N se subrayan talla y color porque, junto con las claves de las dos "
           "entidades, forman la clave compuesta de la tabla intermedia. No hay atributo calculado: "
           "el total de la linea se obtiene multiplicando cantidad por precio.", font=f_ley, fill="black")
    d.text((X(84), Y(ly + 160)),
           "PROVEE es 1:N: un SUMINISTRO atiende muchos PEDIDOS y cada PEDIDO se atiende con un solo "
           "SUMINISTRO, es decir, con un solo ALMACEN y un solo LOCAL. El estado del envio se deduce "
           "del estado del despacho.", font=f_ley, fill="black")

    img.save(ruta)
    return img.size


# ------------------------------------------------------------------ draw.io
def escribir_drawio(ruta):
    partes, ids = [], {}
    for i, n in enumerate(ENTIDADES + ROMBOS, 1):
        ids[n] = "f-%d" % i
        x, y, w, h = FIG[n]
        if n in ENTIDADES:
            estilo = "rounded=0;whiteSpace=wrap;html=1;fontSize=13;fontStyle=1;"
        else:
            estilo = "rhombus;whiteSpace=wrap;html=1;fontSize=11;"
        partes.append('<mxCell id="%s" value="%s" style="%s" vertex="1" parent="1">'
                      '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" /></mxCell>'
                      % (ids[n], sx.escape(n), estilo, x, y, w, h))
    k = 0
    for a, b, punta in ENLACES:
        k += 1
        estilo = "endArrow=classic;html=1;rounded=0;" if punta else "endArrow=none;html=1;rounded=0;"
        partes.append('<mxCell id="l-%d" style="%s" edge="1" parent="1" source="%s" target="%s">'
                      '<mxGeometry relative="1" as="geometry" />'
                      '<mxPoint x="%.1f" y="%.1f" as="targetPoint" />%s</mxCell>'
                      % (k, estilo, ids[a], ids[b], 0, 0, ""))
    k = 0
    for duenno, lista in ATR.items():
        for txt, pk, opc, x, y in lista:
            k += 1
            estilo = "ellipse;whiteSpace=wrap;html=1;fontSize=10;"
            if pk:
                estilo += "fontStyle=4;"
            if opc:
                estilo += "dashed=1;"
            w, h = ancho(txt), 40
            partes.append('<mxCell id="a-%d" value="%s" style="%s" vertex="1" parent="1">'
                          '<mxGeometry x="%d" y="%d" width="%d" height="%d" as="geometry" /></mxCell>'
                          % (k, sx.escape(txt), estilo, x - w // 2, y - h // 2, w, h))
            partes.append('<mxCell id="al-%d" style="endArrow=none;html=1;edgeStyle=orthogonalEdgeStyle;'
                          'rounded=0;" edge="1" parent="1" source="%s" target="a-%d">'
                          '<mxGeometry relative="1" as="geometry" /></mxCell>' % (k, ids[duenno], k))
    for rel, (txt, dx, dy) in CARD.items():
        cx, cy = centro(rel)
        partes.append('<mxCell id="c-%s" value="%s" style="text;html=1;align=center;fontSize=11;" '
                      'vertex="1" parent="1"><mxGeometry x="%.1f" y="%.1f" width="60" height="18" '
                      'as="geometry" /></mxCell>' % (rel, txt, cx + dx - 30, cy + dy - 9))
    partes.append('<mxCell id="tit" value="%s" style="text;html=1;align=left;fontSize=30;fontStyle=1;" '
                  'vertex="1" parent="1"><mxGeometry x="232" y="20" width="700" height="40" '
                  'as="geometry" /></mxCell>' % TITULO)
    partes.append('<mxCell id="sub" value="%s" style="text;html=1;align=left;fontSize=20;" vertex="1" '
                  'parent="1"><mxGeometry x="370" y="105" width="500" height="30" as="geometry" />'
                  '</mxCell>' % SUBTITULO)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n<mxfile host="app.diagrams.net" '
           'modified="2026-10-06T18:15:22.000Z" agent="Mozilla/5.0" version="21.6.8" type="device">'
           '<diagram id="nike-mer-01" name="MER NIKE"><mxGraphModel dx="1600" dy="1080" grid="1" '
           'gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" '
           'pageScale="1" pageWidth="1600" pageHeight="1080" shadow="0"><root><mxCell id="0" />'
           '<mxCell id="1" parent="0" />' + "".join(partes) +
           '</root></mxGraphModel></diagram></mxfile>')
    open(ruta, "w", encoding="utf-8").write(xml)


def main():
    dst = os.environ.get("MER_DIR", "/home/user/proyecto_parcial/nivel_conceptual")
    fallos = verificar()
    print("verificacion:", len(fallos), "problemas")
    for f in fallos:
        print("   ", f)
    if fallos and "--forzar" not in sys.argv:
        return 1
    os.makedirs(dst, exist_ok=True)
    print("png:", dibujar_png(os.path.join(dst, "Diagrama MER (NIKE) - GRUPO 5.png")))
    escribir_drawio(os.path.join(dst, "Diagrama MER (NIKE) - GRUPO 5.drawio"))
    print("ok ->", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
