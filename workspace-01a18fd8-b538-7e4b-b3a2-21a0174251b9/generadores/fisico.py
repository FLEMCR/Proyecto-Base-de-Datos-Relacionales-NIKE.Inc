# -*- coding: utf-8 -*-
"""Modelo fisico: las 10 tablas con IDENTITY, DEFAULT, CHECK y auditoria.

Es la lamina que muestra lo que el docente no encontraba en el DDL: la clave
auto-numerada, los valores por omision, las validaciones y las cuatro columnas
de auditoria que lleva cada tabla.
"""
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/user/generadores")
import modelo_final as M

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

NEGRO, AZUL, GRIS, BORDE = "#111417", "#1F4E79", "#5A646B", "#7E878D"
CREMA, CREMA_B, VERDE, VERDE_B = "#FFF2CC", "#D8C48A", "#E2EFD9", "#A9C9A0"

W, H, ESC = 2290, 990, 2
CW = 320
Y1, Y2 = 120, 420
POS = {
    "CLIENTE": (24, Y1), "CATEGORIA": (504, Y1), "ALMACEN": (984, Y1),
    "LOCAL": (1464, Y1), "PRODUCTO": (1944, Y1),
    "PEDIDO": (24, Y2), "SUMINISTRO": (504, Y2), "DETALLE_VENTA": (984, Y2),
    "STOCK_ALMACEN": (1464, Y2), "DETALLE_SUMINISTRO": (1944, Y2),
}


def alto(tab):
    return 32 + 19 * (len(M.TABLES[tab]["cols"]) + len(M.AUDITORIA)) + 14


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
    f_ent = ImageFont.truetype(FB, 12 * ESC)
    f_atr = ImageFont.truetype(F, 9.5 * ESC)
    f_atrb = ImageFont.truetype(FB, 9.5 * ESC)
    f_mar = ImageFont.truetype(FB, 7.5 * ESC)
    f_tip = ImageFont.truetype(FM, 8.5 * ESC)
    f_tag = ImageFont.truetype(FB, 7 * ESC)
    f_sec = ImageFont.truetype(FB, 12 * ESC)
    f_ley = ImageFont.truetype(F, 10.5 * ESC)

    def E(v):
        return v * ESC

    d.text((E(24), E(26)), "MODELO FISICO - BD NIKE Inc. (Grupo 05)", font=f_tit, fill=NEGRO)
    d.text((E(24), E(60)),
           "SQL Server: IDENTITY en las claves simples, DEFAULT en los valores de arranque, CHECK en las "
           "validaciones y 4 campos de auditoria en todas las tablas.", font=f_sub, fill=GRIS)

    for tab in POS:
        x, y = POS[tab]
        w, h = CW, alto(tab)
        d.rectangle([E(x), E(y), E(x + w), E(y + h)], fill="white", outline=BORDE, width=2 * ESC)
        d.rectangle([E(x), E(y), E(x + w), E(y + 32)], fill=AZUL, outline=BORDE, width=2 * ESC)
        tw = d.textlength(tab, font=f_ent)
        d.text((E(x + w / 2) - tw / 2, E(y + 9)), tab, font=f_ent, fill="white")
        yy = y + 38
        defs = {c: v for c, v, _ in M.defaults_de(tab)}
        for col in M.TABLES[tab]["cols"]:
            nombre, tipo, largo, m, opc = col
            mk = marca(col)
            if mk != "*" and mk != "o":
                ancho = 46 if mk == "PK,FK" else (28 if mk == "FK" else 26)
                d.rectangle([E(x + 8), E(yy - 1), E(x + 8 + ancho), E(yy + 14)], fill=CREMA,
                            outline=CREMA_B)
                tw = d.textlength(mk, font=f_mar)
                d.text((E(x + 8 + ancho / 2) - tw / 2, E(yy + 1)), mk, font=f_mar, fill=NEGRO)
                x0, fuente = x + 8 + ancho + 8, f_atrb
            else:
                d.text((E(x + 13), E(yy + 1)), mk, font=f_mar, fill=GRIS)
                x0, fuente = x + 32, f_atr
            d.text((E(x0), E(yy)), nombre, font=fuente, fill=NEGRO)
            # etiquetas de la capa fisica
            etiquetas = []
            if M.es_identidad(tab, nombre):
                etiquetas.append("IDENTITY")
            if nombre in defs:
                etiquetas.append("DEFAULT")
            if etiquetas:
                xt = x0 + d.textlength(nombre, font=fuente) + 6
                for et in etiquetas:
                    tw = d.textlength(et, font=f_tag)
                    d.rectangle([E(xt), E(yy + 1), E(xt + tw + 8), E(yy + 12)], fill=VERDE,
                                outline=VERDE_B)
                    d.text((E(xt + 4), E(yy + 2)), et, font=f_tag, fill="#2A5B2A")
                    xt += tw + 12
            t = tipo_txt(col)
            tw = d.textlength(t, font=f_tip)
            d.text((E(x + w - 10) - tw, E(yy + 1)), t, font=f_tip, fill=GRIS)
            yy += 19
        # auditoria
        d.line([E(x + 6), E(yy), E(x + w - 6), E(yy)], fill=BORDE, width=1)
        yy += 3
        for nombre, tipo, largo, valor, motivo in M.AUDITORIA:
            d.text((E(x + 13), E(yy + 1)), "A", font=f_mar, fill=GRIS)
            d.text((E(x + 32), E(yy)), nombre, font=f_atr, fill=NEGRO)
            tw = d.textlength("DATETIME" if tipo != "VARCHAR" else "VARCHAR(%d)" % largo, font=f_tip)
            d.text((E(x + w - 10) - tw, E(yy + 1)),
                   "DATETIME" if tipo != "VARCHAR" else "VARCHAR(%d)" % largo,
                   font=f_tip, fill=GRIS)
            yy += 19

    # --------------------------------------------------------- panel inferior
    py = 706
    d.text((E(24), E(py)), "RESTRICCIONES CHECK (11)", font=f_sec, fill=NEGRO)
    d.text((E(24), E(py + 20)),
           "Se validan en la base, no en la aplicacion: si el dato no cumple, el INSERT falla.",
           font=f_ley, fill=GRIS)
    yy = py + 44
    for nombre, tabla, cond, motivo in M.CHECKS:
        d.text((E(30), E(yy)), "%-32s" % nombre, font=f_tip, fill=NEGRO)
        d.text((E(320), E(yy)), "%-18s" % tabla, font=f_tip, fill=AZUL)
        d.text((E(460), E(yy)), cond.split(" AND ")[0][:62], font=f_tip, fill=NEGRO)
        yy += 19

    d.text((E(1180), E(py)), "VALORES POR OMISION DE NEGOCIO (9)", font=f_sec, fill=NEGRO)
    d.text((E(1180), E(py + 20)),
           "Escriben el dato cuando el INSERT no lo envia.", font=f_ley, fill=GRIS)
    yy = py + 44
    for tabla, col, valor, motivo in M.DEFAULTS:
        d.text((E(1186), E(yy)), "%-18s" % tabla, font=f_tip, fill=AZUL)
        d.text((E(1320), E(yy)), "%-22s" % col, font=f_tip, fill=NEGRO)
        d.text((E(1520), E(yy)), "%-20s" % valor[:20], font=f_tip, fill=NEGRO)
        yy += 19

    d.text((E(1740), E(py)), "AUDITORIA (4 x 10 = 40 columnas)", font=f_sec, fill=NEGRO)
    yy = py + 44
    for nombre, tipo, largo, valor, motivo in M.AUDITORIA:
        d.text((E(1746), E(yy)), nombre, font=f_tip, fill=NEGRO)
        d.text((E(1930), E(yy)), valor, font=f_tip, fill=AZUL)
        yy += 19
    d.text((E(1746), E(yy + 14)),
           "usuario_creacion y fecha_creacion se llenan solas;", font=f_ley, fill=GRIS)
    d.text((E(1746), E(yy + 32)),
           "las de modificacion nacen en NULL y las llena el", font=f_ley, fill=GRIS)
    d.text((E(1746), E(yy + 50)),
           "proceso que actualiza la fila.", font=f_ley, fill=GRIS)

    img.save(salida)
    return img.size


if __name__ == "__main__":
    print(dibujar(M.PROJ + "/nivel_fisico/MODELO_FISICO.png"))
