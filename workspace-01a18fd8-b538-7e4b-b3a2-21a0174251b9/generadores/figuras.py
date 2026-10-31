# -*- coding: utf-8 -*-
"""Figuras auxiliares: MER con leyenda (para el informe) y mapa numerado de relaciones."""
from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
PROJ = "/home/user/proyecto_parcial"

LEYENDA = [
    ("COMO LEER EL DIAGRAMA", ""),
    ("Rectangulo = entidad     Rombo = relacion     Elipse = atributo", ""),
    ("Atributo subrayado = PK     Elipse punteada = atributo opcional (Telefono_secundario)", ""),
    ("(1,N) y (M,N) = cardinalidad.  La flecha de cada relacion 1:N apunta a la entidad del lado 1;", ""),
    ("los rombos M:N (CONTIENE, ALMACENA e INCLUYE) no llevan flecha.", ""),
    ("REALIZA  un CLIENTE realiza muchos PEDIDOS", ""),
    ("CONTIENE  un PEDIDO contiene muchos PRODUCTOS (talla, color, cantidad y almacen de origen)", ""),
    ("CLASIFICA  una CATEGORIA clasifica muchos PRODUCTOS", ""),
    ("ALMACENA  un ALMACEN almacena muchos PRODUCTOS por talla y color", ""),
    ("PROVEE  un SUMINISTRO provee a muchos PEDIDOS", ""),
    ("ABASTECE  un ALMACEN abastece muchos SUMINISTROS", ""),
    ("RECIBE  un LOCAL recibe muchos SUMINISTROS", ""),
    ("INCLUYE  un SUMINISTRO incluye muchos PRODUCTOS con talla, color y cantidad", ""),
    ("Sin atributos calculados: el total de la linea y el IGV del pedido se obtienen de la vista", ""),
    ("VW_PEDIDO_TOTALES.", ""),
]


def mer_con_leyenda(salida):
    mer = Image.open(PROJ + "/nivel_conceptual/Diagrama MER (NIKE) - GRUPO 5.png").convert("RGB")
    W = 2400
    mer = mer.resize((W, int(mer.height * W / mer.width)), Image.LANCZOS)
    alto_leyenda = 20 + len(LEYENDA) * 34 + 30
    img = Image.new("RGB", (W, mer.height + alto_leyenda), "white")
    img.paste(mer, (0, 0))
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(F, 20)
    fb = ImageFont.truetype(FB, 22)
    y = mer.height + 16
    for i, (linea, _) in enumerate(LEYENDA):
        d.text((30, y), linea, font=fb if i == 0 else f, fill=(20, 20, 20))
        y += 34
    img.save(salida)
    return img.size


# --------------------------------------------------------------- mapa de relaciones
CAJAS = {  # entidad: (x, y, w, h)
    "CLIENTE": (60, 120, 200, 70),
    "PEDIDO": (400, 120, 200, 70),
    "PRODUCTO": (760, 120, 210, 70),
    "CATEGORIA": (1160, 120, 210, 70),
    "LOCAL": (60, 700, 200, 70),
    "SUMINISTRO": (400, 700, 200, 70),
    "ALMACEN": (760, 700, 210, 70),
}
ROMBOS = {  # relacion: (x, y, radio, numero)
    "REALIZA": (335, 155, 55, 1),
    "CONTIENE": (700, 155, 55, 2),
    "CLASIFICA": (1095, 155, 55, 3),
    "ALMACENA": (865, 430, 55, 4),
    "PROVEE": (500, 430, 55, 5),
    "ABASTECE": (690, 735, 50, 6),
    "INCLUYE": (690, 545, 52, 7),
    "RECIBE": (335, 735, 50, 8),
}


def mapa_relaciones(salida, esc=2):
    W, H = 1450, 900
    img = Image.new("RGB", (W * esc, H * esc), "white")
    d = ImageDraw.Draw(img)
    f_ent = ImageFont.truetype(FB, 21 * esc)
    f_rel = ImageFont.truetype(F, 14 * esc)
    f_num = ImageFont.truetype(FB, 15 * esc)
    f_card = ImageFont.truetype(F, 12 * esc)

    def E(v):
        return v * esc

    def centro(c):
        return c[0] + c[2] / 2, c[1] + c[3] / 2

    def borde(c, hacia):
        cx, cy = centro(c)
        vx, vy = hacia[0] - cx, hacia[1] - cy
        t = min((c[2] / 2) / abs(vx) if vx else 1e9, (c[3] / 2) / abs(vy) if vy else 1e9)
        return cx + vx * t, cy + vy * t

    def linea(a, b):
        ca, cb = centro(CAJAS[a]), centro(CAJAS[b])
        p = borde(CAJAS[a], cb)
        q = borde(CAJAS[b], ca)
        d.line([E(p[0]), E(p[1]), E(q[0]), E(q[1])], fill="black", width=2 * esc)

    def rombo_a_entidad(rel, ent):
        r = ROMBOS[rel]
        rc = (r[0] - r[2], r[1] - r[2], 2 * r[2], 2 * r[2])
        c = CAJAS[ent]
        p = borde(rc, centro(c))
        q = borde(c, centro(rc))
        d.line([E(p[0]), E(p[1]), E(q[0]), E(q[1])], fill="black", width=2 * esc)

    enlaces = [("REALIZA", "CLIENTE"), ("REALIZA", "PEDIDO"),
               ("CONTIENE", "PEDIDO"), ("CONTIENE", "PRODUCTO"),
               ("CLASIFICA", "PRODUCTO"), ("CLASIFICA", "CATEGORIA"),
               ("RECIBE", "LOCAL"), ("RECIBE", "SUMINISTRO"),
               ("ABASTECE", "SUMINISTRO"), ("ABASTECE", "ALMACEN"),
               ("PROVEE", "PEDIDO"), ("PROVEE", "SUMINISTRO"),
               ("INCLUYE", "SUMINISTRO"), ("INCLUYE", "PRODUCTO"),
               ("ALMACENA", "PRODUCTO"), ("ALMACENA", "ALMACEN")]
    for rel, ent in enlaces:
        rombo_a_entidad(rel, ent)

    for n, (x, y, w, h) in CAJAS.items():
        d.rectangle([E(x), E(y), E(x + w), E(y + h)], fill="white", outline="black", width=2 * esc)
        tw = d.textlength(n, font=f_ent)
        d.text((E(x + w / 2) - tw / 2, E(y + h / 2) - 14 * esc), n, font=f_ent, fill="black")

    for n, (x, y, r, num) in ROMBOS.items():
        pts = [(E(x), E(y - r)), (E(x + r), E(y)), (E(x), E(y + r)), (E(x - r), E(y))]
        d.polygon(pts, fill="white", outline="black")
        d.line(pts + [pts[0]], fill="black", width=2 * esc)
        tw = d.textlength(n, font=f_rel)
        d.text((E(x) - tw / 2, E(y) - 9 * esc), n, font=f_rel, fill="black")
        # numero en circulo amarillo sobre el rombo
        cy = y - r - 26
        d.ellipse([E(x - 15), E(cy - 15), E(x + 15), E(cy + 15)], fill="#D4E84A",
                  outline="black", width=2 * esc)
        tw = d.textlength(str(num), font=f_num)
        d.text((E(x) - tw / 2, E(cy) - 10 * esc), str(num), font=f_num, fill="black")

    img = img.crop((int(20 * esc), int(20 * esc), int(1430 * esc), int(870 * esc)))
    img.save(salida)
    return img.size


if __name__ == "__main__":
    print(mer_con_leyenda(PROJ + "/nivel_conceptual/MER_informe.png"))
    print(mapa_relaciones("/home/user/generadores/fig_mapa_relaciones.png"))
