# -*- coding: utf-8 -*-
"""Figura de la lamina 7: fase 3FN con el esquema final corregido."""
from PIL import Image, ImageDraw, ImageFont

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def C(c):
    return "#" + c


def tabla(d, x, y, ancho, cabecera, filas, esc, tam=14):
    f_cab = ImageFont.truetype(FB, tam * esc)
    f_cel = ImageFont.truetype(F, tam * esc)
    n = len(cabecera)
    cw = ancho / n
    alto = 30 * esc
    d.rectangle([x, y, x + ancho, y + alto], fill="black")
    for i, c in enumerate(cabecera):
        d.text((x + i * cw + 6 * esc, y + 7 * esc), c, font=f_cab, fill=C("FFFFFF"))
    yy = y + alto
    for k, fila in enumerate(filas):
        fondo = C("F4F6F7") if k % 2 else C("FFFFFF")
        d.rectangle([x, yy, x + ancho, yy + alto], fill=fondo, outline=C("D5DBDF"))
        for i, v in enumerate(fila):
            d.text((x + i * cw + 6 * esc, yy + 7 * esc), str(v), font=f_cel, fill=C("1B2A38"))
        yy += alto
    return yy


def construir(salida, W=1760, H=700, esc=2):
    img = Image.new("RGB", (W * esc, H * esc), "white")
    d = ImageDraw.Draw(img)
    f_tit = ImageFont.truetype(FB, 30 * esc)
    f_sub = ImageFont.truetype(F, 15 * esc)
    f_h = ImageFont.truetype(FB, 16 * esc)
    f_b = ImageFont.truetype(F, 14 * esc)
    f_not = ImageFont.truetype(F, 13 * esc)

    def E(v):
        return v * esc

    d.rectangle([0, 0, E(W), E(58)], fill=C("0B0B0B"))
    d.text((E(30), E(14)), "FASE 3FN  ->  esquema final de 10 tablas", font=f_tit, fill=C("FFFFFF"))
    d.rectangle([0, E(58), E(W), E(63)], fill=C("9ACD32"))
    d.text((E(30), E(74)),
           "Se separa CLIENTE (ya es 3FN), se corrige SUMINISTRO y no se guarda ningun dato calculado",
           font=f_sub, fill=C("333F48"))

    y = 118
    d.text((E(30), E(y)), "CLIENTE EN 3FN - recien aqui sale de PEDIDO", font=f_h, fill=C("101010"))
    y += 30
    y = tabla(d, E(30), E(y), E(700),
              ["id_cliente", "nombre", "correo_electronico", "telefono", "telefono_secundario"],
              [[1, "Carlos Mendoza", "cmendoza@gmail.com", "987654321", "945112233"],
               [2, "Lucia Paredes", "lparedes@hotmail.com", "912345678", "NULL"]], esc, tam=10.5)
    d.text((E(30), E(y / esc + 8)),
           "El correo y el telefono ya no se repiten en cada compra del mismo cliente.",
           font=f_not, fill=C("5E676E"))

    y2 = y / esc + 44
    d.text((E(30), E(y2)), "SUMINISTRO - nueva entidad con PK id_suministro", font=f_h, fill=C("101010"))
    d.text((E(800), E(y2)), "DETALLE_SUMINISTRO - tabla nueva", font=f_h, fill=C("101010"))
    y2 += 30
    fin1 = tabla(d, E(30), E(y2), E(740),
                 ["id_suministro", "fecha_suministro", "estado_despacho", "ALMACEN_id_almacen",
                  "LOCAL_id_local"],
                 [[1, "2026-10-04", "ENTREGADO", 100, 501],
                  [2, "2026-10-05", "EN RUTA", 100, 502],
                  [3, "2026-10-06", "PROGRAMADO", 200, 503]], esc, tam=10.5)
    fin2 = tabla(d, E(800), E(y2), E(930),
                 ["SUMINISTRO_id_suministro", "PRODUCTO_id_producto", "talla", "color", "cantidad"],
                 [[1, 1001, "42", "Negro", 20],
                  [1, 1002, "41", "Blanco", 15],
                  [2, 1002, "41", "Blanco", 25],
                  [3, 1003, "M", "Azul Marino", 40]], esc, tam=10.5)
    d.text((E(30), E(max(fin1, fin2) / esc + 10)),
           "La PK de DETALLE_SUMINISTRO es suministro + producto + talla + color; la cantidad es un atributo.",
           font=f_not, fill=C("5E676E"))

    y3 = max(fin1, fin2) / esc + 70
    d.text((E(30), E(y3)), "Que se corrigio en la 3FN", font=f_h, fill=C("101010"))
    y3 += 34
    puntos = [
        "CLIENTE sale de PEDIDO: ya no se repite el nombre, el correo ni el telefono en cada compra.",
        "DETALLE_VENTA guarda talla y color: la venta queda amarrada a una fila de STOCK_ALMACEN.",
        "No existe columna total ni columna igv: las dos se calculan en la vista VW_PEDIDO_TOTALES.",
        "STOCK_ALMACEN mantiene su PK de 4 campos: talla, color, almacen y producto.",
        "SUMINISTRO usa id_suministro como clave, no la fecha: pueden salir dos despachos el mismo dia.",
    ]
    for t in puntos:
        d.ellipse([E(32), E(y3 + 5), E(42), E(y3 + 15)], fill=C("8BC34A"))
        d.text((E(52), E(y3)), t, font=f_b, fill=C("1B2A38"))
        y3 += 28

    img.save(salida)
    return img.size


if __name__ == "__main__":
    print(construir("/home/user/generadores/fig_fase3fn.png"))
