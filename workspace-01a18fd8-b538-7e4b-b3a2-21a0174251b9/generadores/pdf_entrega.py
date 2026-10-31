# -*- coding: utf-8 -*-
"""PDF de entrega: respuesta a las observaciones del docente + los cuatro modelos.

Paginas:
  1. Portada
  2. Respuesta a las observaciones (que pedia / que se hizo)
  3. Regla del suministro unico y equivalencia de estados
  4. Extracto del DDL (IDENTITY, DEFAULT, CHECK y auditoria)
  5..8 Conceptual, logico, relacional y fisico, cada uno en su propia pagina
"""
import json
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

import modelo_final as M

ANCHO, ALTO = landscape(A4)
AZUL = colors.HexColor("#1F4E79")
GRIS = colors.HexColor("#5A646B")
VERDE = colors.HexColor("#00B050")
CREMA = colors.HexColor("#FFF2CC")
CLARO = colors.HexColor("#F2F5F8")

P_TIT = ParagraphStyle("tit", fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=AZUL)
P_SUB = ParagraphStyle("sub", fontName="Helvetica", fontSize=13, leading=17, textColor=GRIS)
P_H = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=16, leading=20, textColor=AZUL)
P_H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=AZUL)
P_TXT = ParagraphStyle("t", fontName="Helvetica", fontSize=9.5, leading=13)
P_PIE = ParagraphStyle("pie", fontName="Helvetica", fontSize=8, leading=11, textColor=GRIS)
P_CEL = ParagraphStyle("cel", fontName="Helvetica", fontSize=8.5, leading=11)
P_CELB = ParagraphStyle("celb", fontName="Helvetica-Bold", fontSize=8.5, leading=11,
                        textColor=colors.white)


def dibujar_parrafo(c, texto, estilo, x, y, ancho):
    p = Paragraph(texto, estilo)
    w, h = p.wrap(ancho, ALTO)
    p.drawOn(c, x, y - h)
    return y - h


def dibujar_tabla(c, filas, x, y, anchos, cabecera=True, alto_fila=16):
    # cada celda va como parrafo para que el texto se ajuste al ancho de su columna
    envueltas = []
    for i, fila in enumerate(filas):
        estilo = P_CELB if (i == 0 and cabecera) else P_CEL
        envueltas.append([Paragraph(str(v), estilo) for v in fila])
    t = Table(envueltas, colWidths=anchos, rowHeights=None)
    estilo = [
        ("FONT", (0, 0), (-1, -1), "Helvetica", 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if cabecera:
        estilo += [("BACKGROUND", (0, 0), (-1, 0), AZUL)]
        for i in range(1, len(filas)):
            if i % 2 == 0:
                estilo.append(("BACKGROUND", (0, i), (-1, i), CLARO))
    t.setStyle(TableStyle(estilo))
    w, h = t.wrap(sum(anchos), ALTO)
    t.drawOn(c, x, y - h)
    return y - h


def pie(c, numero, total):
    c.setFont("Helvetica", 7.5)
    c.setFillColor(GRIS)
    c.drawString(2 * cm, 1.0 * cm, "BD NIKE Inc. | Grupo 05 | Diseno de Bases de Datos Relacionales - IDAT")
    c.drawRightString(ANCHO - 2 * cm, 1.0 * cm, "Pagina %d de %d" % (numero, total))
    c.setFillColor(colors.black)


def cabecera(c, titulo, subtitulo=None):
    c.setFillColor(AZUL)
    c.rect(0, ALTO - 2.0 * cm, ANCHO, 2.0 * cm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 15)
    c.drawString(2 * cm, ALTO - 1.25 * cm, titulo)
    if subtitulo:
        c.setFont("Helvetica", 9.5)
        c.drawRightString(ANCHO - 2 * cm, ALTO - 1.25 * cm, subtitulo)
    c.setFillColor(colors.black)


def pagina_imagen(c, ruta, titulo, subtitulo, numero, total, margen=1.4):
    cabecera(c, titulo, subtitulo)
    img = ImageReader(ruta)
    iw, ih = img.getSize()
    disp_w = ANCHO - 2 * margen * cm
    disp_h = ALTO - 4.6 * cm
    escala = min(disp_w / iw, disp_h / ih)
    w, h = iw * escala, ih * escala
    c.drawImage(ruta, (ANCHO - w) / 2, (ALTO - 2.2 * cm - h) / 2 + 0.3 * cm, width=w, height=h,
                preserveAspectRatio=True, mask=None)
    pie(c, numero, total)


def construir(destino):
    c = canvas.Canvas(destino, pagesize=landscape(A4))
    c.setTitle("Entrega final - BD NIKE Inc. (Grupo 05)")
    c.setAuthor("Grupo 05")
    TOTAL = 12

    # ---------------------------------------------------------------- portada
    c.setFillColor(AZUL)
    c.rect(0, ALTO - 7.2 * cm, ANCHO, 7.2 * cm, stroke=0, fill=1)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 30)
    c.drawString(2 * cm, ALTO - 3.4 * cm, "BD NIKE Inc.")
    c.setFont("Helvetica", 17)
    c.drawString(2 * cm, ALTO - 4.3 * cm, "Modelo de base de datos: ventas y almacenes")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(2 * cm, ALTO - 5.4 * cm, "ENTREGA FINAL - correcciones del docente aplicadas")
    c.setFont("Helvetica", 10.5)
    c.setFillColor(colors.HexColor("#D6E4F0"))
    c.drawString(2 * cm, ALTO - 6.3 * cm,
                 "MER  |  Modelo logico (Barker)  |  Modelo relacional  |  Modelo fisico (SQL Server)")
    c.setFillColor(colors.black)

    y = ALTO - 8.6 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y, "Integrantes")
    c.setFont("Helvetica", 10.5)
    for i, n in enumerate(["Daniel Asmat", "Salomon Fernandez", "Luis Coloma", "Pablo Rios"]):
        c.drawString(2 * cm, y - (0.55 + 0.45 * i) * cm, "- " + n)

    c.setFont("Helvetica-Bold", 11)
    c.drawString(8.5 * cm, y, "Curso")
    c.setFont("Helvetica", 10.5)
    c.drawString(8.5 * cm, y - 0.55 * cm, "Diseno de Bases de Datos Relacionales - IDAT")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(8.5 * cm, y - 1.3 * cm, "Docente")
    c.setFont("Helvetica", 10.5)
    c.drawString(8.5 * cm, y - 1.85 * cm, "Sergio Fernando Castillo Carrion")
    c.setFont("Helvetica-Bold", 11)
    c.drawString(8.5 * cm, y - 2.6 * cm, "Alcance")
    c.setFont("Helvetica", 10.5)
    c.drawString(8.5 * cm, y - 3.15 * cm, "Ventas y almacenes de Nike a nivel nacional - Peru")

    # resumen
    y2 = 8.6 * cm
    c.setFont("Helvetica-Bold", 11)
    c.drawString(2 * cm, y2, "Contenido")
    filas = [
        ["Pagina", "Contenido"],
        ["2", "Respuesta punto por punto a las observaciones de 0FN, 1FN, 2FN y 3FN"],
        ["3", "Regla de un pedido atendido por un solo suministro y equivalencia de estados"],
        ["4", "Extracto del DDL: IDENTITY, DEFAULT, CHECK y auditoria"],
        ["5 a 7", "Diccionario de datos: las 48 columnas de negocio, una por una"],
        ["8", "Modelo conceptual (M.E.R.)"],
        ["9", "Modelo logico en notacion Barker"],
        ["10", "Modelo relacional: 10 tablas y 11 claves foraneas"],
        ["11", "Modelo fisico: 10 tablas con identidad, omisiones, validaciones y auditoria"],
        ["12", "Cuadro de paso de un modelo al siguiente"],
    ]
    dibujar_tabla(c, filas, 2 * cm, y2 - 0.4 * cm, [2.2 * cm, 20 * cm])
    pie(c, 1, TOTAL)
    c.showPage()

    # ------------------------------------------------- 2. respuesta
    cabecera(c, "Respuesta a las observaciones", "0FN y 1FN | 2FN | 3FN")
    filas = [["Fase", "Observacion del docente", "Correccion aplicada"],
             ["0FN y 1FN",
              "Los productos y cantidades del suministro aparecen recien en 2FN.",
              "La tabla general ya trae 'productos_suministrados' y 'cantidades_suministradas' "
              "(20, 15, 25 y 40 unidades) y la 1FN los deja atomicos en cada fila, con su producto, "
              "talla y color. La 2FN sale de esa misma informacion."],
             ["2FN",
              "Esta incompleta: faltaban PRODUCTO (con su categoria), ALMACEN, LOCAL y STOCK_ALMACEN.",
              "La hoja 2FN tiene ahora ocho tablas: PEDIDO, DETALLE_VENTA, PRODUCTO (con los datos de "
              "su categoria), SUMINISTRO, DETALLE_SUMINISTRO, ALMACEN, LOCAL y STOCK_ALMACEN. Todo lo "
              "que estaba en la 1FN queda en alguna de ellas."],
             ["3FN",
              "estado_envio se deduce del estado del suministro: es un dato repetido.",
              "Se elimino la columna de PEDIDO en el Excel, en el modelo logico, en el relacional y en "
              "el DDL. El estado del pedido se lee del suministro que lo atiende, sin guardarlo dos veces."],
             ["3FN",
              "Dejen escrito que un pedido se atiende con un solo suministro, es decir, un almacen y un local.",
              "Queda escrito en el MER, en el logico, en el relacional y en el fisico. En la base se cumple con "
              "PEDIDO.SUMINISTRO_id_suministro: una sola columna y obligatoria."]]
    dibujar_tabla(c, filas, 1.8 * cm, ALTO - 3.2 * cm, [2.6 * cm, 10.2 * cm, 12.6 * cm])
    y = 6.2 * cm
    y = dibujar_parrafo(c, "<b>Que se entrega en este PDF</b>", P_H2, 1.8 * cm, y, 25 * cm)
    y = dibujar_parrafo(c,
                        "Los cuatro modelos, cada uno en su propia lamina y a tamano completo: el conceptual "
                        "(M.E.R.), el logico en notacion Barker, el relacional con las diez tablas y sus once "
                        "claves foraneas, y el fisico con identidad, valores por omision, validaciones y auditoria. "
                        "El Excel de normalizacion se entrega aparte, con las hojas 0FN, 1FN, 2FN y 3FN ya "
                        "corregidas.", P_TXT, 1.8 * cm, y - 0.2 * cm, 25 * cm)
    pie(c, 2, TOTAL)
    c.showPage()

    # ------------------------------------------------- 3. regla y estados
    cabecera(c, "Regla del suministro unico y equivalencia de estados",
             "Lo que queda escrito en el modelo")
    y = ALTO - 3.4 * cm
    y = dibujar_parrafo(c, "<b>Un pedido se atiende con un solo suministro</b>", P_H2, 1.8 * cm, y, 25 * cm)
    y = dibujar_parrafo(c,
                        "La relacion PROVEE es 1:N: un SUMINISTRO provee uno o muchos PEDIDOS. El otro extremo "
                        "de esa misma relacion es la regla que el docente pidio dejar escrita: <b>cada PEDIDO se "
                        "atiende con un solo SUMINISTRO</b>. En el modelo relacional eso se ve como la clave foranea "
                        "SUMINISTRO_id_suministro dentro de PEDIDO: una sola columna, obligatoria (NOT NULL), de "
                        "modo que cada fila de PEDIDO guarda un unico suministro. Como cada SUMINISTRO tiene un unico "
                        "ALMACEN de origen y un unico LOCAL de destino, el pedido queda ligado a un almacen y a un "
                        "local sin repetir esos datos en su propia tabla.", P_TXT, 1.8 * cm, y - 0.25 * cm, 25 * cm)
    y -= 1.9 * cm
    y = dibujar_parrafo(c, "<b>El estado del envio no se guarda: se deduce</b>", P_H2, 1.8 * cm, y, 25 * cm)
    filas = [["Estado del pedido (deducido)", "estado_despacho del SUMINISTRO", "Que significa"],
             ["PENDIENTE", "PROGRAMADO", "El despacho aun no sale del centro de distribucion."],
             ["ENVIADO", "EN RUTA", "La mercaderia ya salio y va camino al local."],
             ["ENTREGADO", "ENTREGADO", "El local recibio la mercaderia y el pedido quedo atendido."]]
    dibujar_tabla(c, filas, 1.8 * cm, y - 0.3 * cm, [7 * cm, 7 * cm, 11.4 * cm])
    y = 6.0 * cm
    y = dibujar_parrafo(c, "<b>Por que la columna se elimina y no se justifica</b>", P_H2, 1.8 * cm, y, 25 * cm)
    y = dibujar_parrafo(c,
                        "Guardar estado_envio en PEDIDO seria un dato derivado: su valor se puede obtener siempre "
                        "del estado del suministro, y mantenerlo obliga a actualizar dos tablas cada vez que el "
                        "camion avanza. Al eliminarlo se cumple la tercera forma normal y el pedido queda con sus "
                        "datos propios: fecha, metodo de pago, cliente y el suministro con el que se atiende.",
                        P_TXT, 1.8 * cm, y - 0.25 * cm, 25 * cm)
    pie(c, 3, TOTAL)
    c.showPage()

    # ------------------------------------------------- 4. DDL
    cabecera(c, "Extracto del modelo fisico (SQL Server)", "IDENTITY | DEFAULT | CHECK | auditoria")
    codigo = [
        "CREATE TABLE PEDIDO (",
        "    id_pedido                 INT IDENTITY(1,1) NOT NULL,",
        "    fecha                     DATE DEFAULT CAST(GETDATE() AS DATE) NOT NULL,",
        "    metodo_pago               VARCHAR(30) DEFAULT 'Tarjeta de Credito' NOT NULL,",
        "    CLIENTE_id_cliente        INTEGER NOT NULL,",
        "    SUMINISTRO_id_suministro  INTEGER NOT NULL,",
        "    usuario_creacion          VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,",
        "    fecha_creacion            DATETIME DEFAULT GETDATE() NOT NULL,",
        "    usuario_modificacion      VARCHAR(30),",
        "    fecha_modificacion        DATETIME,",
        "    CONSTRAINT PEDIDO_PK PRIMARY KEY (id_pedido)",
        ");",
        "",
        "CREATE TABLE DETALLE_VENTA (",
        "    PEDIDO_id_pedido           INTEGER NOT NULL,",
        "    PRODUCTO_id_producto       INTEGER NOT NULL,",
        "    talla_elegida              VARCHAR(10) NOT NULL,",
        "    color_elegido              VARCHAR(30) NOT NULL,",
        "    cantidad                   INTEGER DEFAULT 1 NOT NULL,",
        "    precio_unitario_aplicado   DECIMAL(10,2) NOT NULL,",
        "    ...  (auditoria igual que en todas las tablas)",
        "    CONSTRAINT DETALLE_VENTA_PK PRIMARY KEY",
        "        (PEDIDO_id_pedido, PRODUCTO_id_producto, talla_elegida, color_elegido),",
        "    CONSTRAINT CK_DETALLE_VENTA_CANTIDAD CHECK (cantidad > 0),",
        "    CONSTRAINT CK_DETALLE_VENTA_PRECIO CHECK (precio_unitario_aplicado > 0)",
        ");",
        "",
        "ALTER TABLE PEDIDO ADD CONSTRAINT PEDIDO_SUMINISTRO_FK",
        "    FOREIGN KEY (SUMINISTRO_id_suministro) REFERENCES SUMINISTRO (id_suministro);",
    ]
    c.setFont("Courier", 8)
    c.setFillColor(colors.HexColor("#1A1A1A"))
    yy = ALTO - 3.1 * cm
    for linea in codigo:
        c.drawString(1.8 * cm, yy, linea)
        yy -= 0.40 * cm
    c.setFillColor(colors.black)
    y = yy - 0.2 * cm
    c.setFont("Helvetica", 9)
    c.drawString(1.8 * cm, y,
                 "Total del script: 10 tablas, 11 claves foraneas, 7 IDENTITY, 9 valores por omision de "
                 "negocio, 10 CHECK y 40 columnas de auditoria. Sin vistas.")
    pie(c, 4, TOTAL)
    c.showPage()

    # ------------------------------------------------- 5, 6 y 7. diccionario
    datos = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                        "_diccionario.json"), encoding="utf-8"))
    negocio = [f for f in datos["filas"] if not f["auditoria"]]
    cortes = [16, 32]                      # tres paginas parejas de 16 columnas
    bloques = [negocio[:cortes[0]], negocio[cortes[0]:cortes[1]], negocio[cortes[1]:]]
    anchos = [3.9 * cm, 5.0 * cm, 2.8 * cm, 1.2 * cm, 1.6 * cm, 11.1 * cm]
    for k, bloque in enumerate(bloques, start=1):
        cabecera(c, "Diccionario de datos (%d de 3)" % k,
                 "48 columnas de negocio | tipo, obligatoriedad, clave y significado")
        filas = [["Tabla", "Columna", "Tipo", "NULL", "Clave", "Descripcion"]]
        for f in bloque:
            filas.append([f["tabla"], f["columna"], f["tipo"], f["nulo"],
                          f["clave"] or "-", f["descripcion"]])
        dibujar_tabla(c, filas, 1.8 * cm, ALTO - 2.9 * cm, anchos)
        dibujar_parrafo(c,
                        "Las 10 tablas llevan ademas las mismas 4 columnas de auditoria: "
                        "usuario_creacion, fecha_creacion, usuario_modificacion y fecha_modificacion. "
                        "El diccionario completo, con DEFAULT, CHECK y claves foraneas, esta en el archivo "
                        "DICCIONARIO_DE_DATOS.xlsx.",
                        P_PIE, 1.8 * cm, 2.2 * cm, 25.6 * cm)
        pie(c, 4 + k, TOTAL)
        c.showPage()

    # ------------------------------------------------- 7..11 imagenes
    base = M.PROJ
    pagina_imagen(c, os.path.join(base, "nivel_conceptual", "Diagrama MER (NIKE) - GRUPO 5.png"),
                  "1. Modelo conceptual (M.E.R.)",
                  "7 entidades | 8 relaciones | PK subrayadas | sin datos calculados", 5, TOTAL)
    c.showPage()
    pagina_imagen(c, os.path.join(base, "nivel_logico", "MODELO_LOGICO.png"),
                  "2. Modelo logico (Barker)",
                  "7 entidades | 8 relaciones con verbo y cardinalidad | M:N como relacion", 9, TOTAL)
    c.showPage()
    pagina_imagen(c, os.path.join(base, "nivel_logico", "MODELO_RELACIONAL.png"),
                  "3. Modelo relacional",
                  "10 tablas | 11 claves foraneas | sin columnas calculadas", 10, TOTAL)
    c.showPage()
    pagina_imagen(c, os.path.join(base, "nivel_fisico", "MODELO_FISICO.png"),
                  "4. Modelo fisico (SQL Server)",
                  "IDENTITY | DEFAULT | CHECK | auditoria", 11, TOTAL)
    c.showPage()

    # ------------------------------------------------- 9 cuadro final
    pagina_imagen(c, os.path.join(base, "CUADRO_DE_MODELOS.png"),
                  "De un modelo al siguiente",
                  "Que cambia en cada nivel y que no se debe agregar", 12, TOTAL)
    c.showPage()

    c.save()
    return destino


if __name__ == "__main__":
    print(construir(M.PROJ + "/ENTREGA_MODELOS_NIKE_GRUPO_5.pdf"))
