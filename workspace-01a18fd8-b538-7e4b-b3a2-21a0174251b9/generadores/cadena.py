# -*- coding: utf-8 -*-
"""Lamina unica que muestra que cambia en cada nivel: conceptual, logico,
relacional y fisico. Sirve de apoyo para la exposicion."""
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "/home/user/generadores")
import modelo_final as M

F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
NEGRO, AZUL, GRIS = "#111417", "#1F4E79", "#4C565C"
FILA_A, FILA_B = "#FFFFFF", "#F2F5F8"
CREMA = "#FFF2CC"
VERDE = "#E2EFD9"

W, H, ESC = 1660, 790, 2

COLS = [("Elemento", 330), ("1. CONCEPTUAL (MER)", 380), ("2. LOGICO", 320),
        ("3. RELACIONAL", 310), ("4. FISICO", 280)]

FILAS = [
    ("Entidades / tablas", "7 entidades + 3 rombos M:N", "7 entidades",
     "10 tablas", "10 tablas"),
    ("Relaciones M:N", "rombos con sus atributos y clave compuesta subrayada",
     "se dibujan como relacion, con verbo, M/N y sus atributos",
     "ya son tablas: DETALLE_VENTA, STOCK_ALMACEN, DETALLE_SUMINISTRO",
     "las mismas 3 tablas"),
    ("Claves", "PK subrayada", "PK marcada y FK heredada del lado 1",
     "PK + 11 FK; 3 PK compuestas", "PK con IDENTITY en las simples"),
    ("Atributos calculados", "no se dibujan: Total e IGV no son atributos",
     "no se dibujan", "no existen en ninguna tabla",
     "no hay columnas ni vistas"),
    ("Tipos de dato", "no se anotan", "VARCHAR, INTEGER, DECIMAL(10,2), DATE",
     "los mismos del logico", "los del motor: INT, VARCHAR(n), DECIMAL(10,2)"),
    ("Valores por omision", "-", "-", "-", "9 DEFAULT (estados, fechas, stock)"),
    ("Validaciones", "-", "-", "-", "10 CHECK (cantidades, precios, estados)"),
    ("Auditoria", "-", "-", "-", "4 columnas en las 10 tablas"),
    ("Datos que admiten NULL", "3 (telefono_secundario, descripcion, especificaciones)",
     "3, marcados con 'o'", "3, sin NOT NULL", "3, sin NOT NULL"),
    ("Herramienta", "Draw.io", "Oracle Data Modeler", "Oracle Data Modeler",
     "SSMS / SQL Server"),
]


def dibujar(salida):
    img = Image.new("RGB", (W * ESC, H * ESC), "white")
    d = ImageDraw.Draw(img)
    f_tit = ImageFont.truetype(FB, 25 * ESC)
    f_sub = ImageFont.truetype(F, 12 * ESC)
    f_enc = ImageFont.truetype(FB, 12 * ESC)
    f_cel = ImageFont.truetype(F, 10.5 * ESC)
    f_celb = ImageFont.truetype(FB, 10.5 * ESC)
    f_pie = ImageFont.truetype(F, 10.5 * ESC)

    def E(v):
        return v * ESC

    d.text((E(28), E(24)), "DE UN MODELO AL SIGUIENTE - BD NIKE Inc. (Grupo 05)",
           font=f_tit, fill=NEGRO)
    d.text((E(28), E(58)),
           "Lo que se agrega y lo que no se debe agregar en cada nivel. Cada modelo va en su propia lamina.",
           font=f_sub, fill=GRIS)

    x0, y0 = 28, 100
    # encabezados
    x = x0
    d.rectangle([E(x0), E(y0), E(x0 + sum(c[1] for c in COLS)), E(y0 + 34)], fill=AZUL)
    for titulo, ancho in COLS:
        d.text((E(x + 10), E(y0 + 10)), titulo, font=f_enc, fill="white")
        x += ancho
    y = y0 + 34
    for i, fila in enumerate(FILAS):
        alto = 58 if i in (1, 4, 8) else 40
        fondo = FILA_A if i % 2 == 0 else FILA_B
        d.rectangle([E(x0), E(y), E(x0 + sum(c[1] for c in COLS)), E(y + alto)],
                    fill=fondo, outline="#C9D2D9")
        x = x0
        for k, (valor, ancho) in enumerate(zip(fila, [c[1] for c in COLS])):
            fuente = f_celb if k == 0 else f_cel
            # partir el texto en dos lineas si hace falta
            palabras, linea, lineas = valor.split(), "", []
            for p in palabras:
                prueba = (linea + " " + p).strip()
                if d.textlength(prueba, font=fuente) > (ancho - 18) * ESC and linea:
                    lineas.append(linea)
                    linea = p
                else:
                    linea = prueba
            lineas.append(linea)
            yy = y + 8
            for ln in lineas[:3]:
                d.text((E(x + 10), E(yy)), ln, font=fuente, fill=NEGRO if k == 0 else "#22303A")
                yy += 15
            x += ancho
        y += alto

    # notas
    ny = y + 22
    d.text((E(28), E(ny)), "POR QUE ASI", font=f_enc, fill=NEGRO)
    notas = [
        "En el conceptual no se dibujan claves foraneas ni tipos: solo entidades, relaciones y atributos.",
        "En el logico las M:N se dibujan como relacion con sus atributos; al generar el relacional aparece una tabla por cada una.",
        "En el relacional ya no existen rombos: la relacion se lee desde la FK, con 1 del lado uno y N del lado muchos.",
        "En el fisico se agrega lo que depende del motor (IDENTITY, DEFAULT, CHECK) y la auditoria de cada tabla.",
        "Total e IGV no existen en ningun nivel: se calculan en la consulta (cantidad x precio, y el 18 % sobre la suma).",
    ]
    yy = ny + 24
    for n in notas:
        d.text((E(28), E(yy)), "\u2022 " + n, font=f_pie, fill=GRIS)
        yy += 19

    img.save(salida)
    return img.size


if __name__ == "__main__":
    print(dibujar(M.PROJ + "/CUADRO_DE_MODELOS.png"))
