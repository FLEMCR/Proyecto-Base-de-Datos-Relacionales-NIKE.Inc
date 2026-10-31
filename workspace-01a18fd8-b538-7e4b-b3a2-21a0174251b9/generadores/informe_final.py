# -*- coding: utf-8 -*-
"""Actualiza el informe (docx y pdf) con el MER y los modelos finales."""
import io

import docx
import pymupdf
from docx.shared import Emu
from PIL import Image

PROJ = "/home/user/proyecto_parcial"
DOCX = ["ENTREGA DE MODELO LOGICO_RELACIONAL GRUPO-5.docx", "PROYECTO_BD_MER_GRUPO_CINCO.docx"]
PDF = ["ENTREGA DE MODELO LOGICO_RELACIONAL GRUPO-5.pdf", "PROYECTO_BD_MER_GRUPO_CINCO.pdf"]

FIGURAS = [
    PROJ + "/nivel_conceptual/MER_informe.png",
    PROJ + "/nivel_logico/MODELO_LOGICO.png",
    PROJ + "/nivel_logico/MODELO_RELACIONAL.png",
    PROJ + "/nivel_fisico/MODELO_FISICO.png",
]

CAMBIO_TEXTO = [
    ("(cantidad, talla elegida, precio de venta y subtotal)",
     "(cantidad, talla elegida, color y precio aplicado)"),
]


def arreglar_docx(nombre):
    ruta = PROJ + "/" + nombre
    doc = docx.Document(ruta)
    # textos
    for p in doc.paragraphs:
        for viejo, nuevo in CAMBIO_TEXTO:
            if viejo in p.text:
                for r in p.runs:
                    if viejo in r.text:
                        r.text = r.text.replace(viejo, nuevo)
    # imagenes 2..5 (la 1 es el logo)
    for i, fig in enumerate(FIGURAS, start=1):
        if i >= len(doc.inline_shapes):
            break
        sh = doc.inline_shapes[i]
        im = Image.open(fig)
        ar = im.width / im.height
        ancho = sh.width
        sh.height = Emu(int(ancho / ar)) if ancho / ar < Emu(0).emu + 10 ** 12 else sh.height
        rid = sh._inline.graphic.graphicData.pic.blipFill.blip.embed
        part = doc.part.related_parts[rid]
        part._blob = open(fig, "rb").read()
    doc.save(ruta)
    return ruta


def arreglar_pdf(nombre):
    ruta = PROJ + "/" + nombre
    doc = pymupdf.open(ruta)
    # paginas 3..6 -> figuras 0..3
    for k, fig in enumerate(FIGURAS):
        pagina = doc[2 + k]
        imagenes = pagina.get_image_info()
        if not imagenes:
            continue
        grande = max(imagenes, key=lambda im: (im["bbox"][2] - im["bbox"][0]) *
                    (im["bbox"][3] - im["bbox"][1]))
        rect = pymupdf.Rect(grande["bbox"])
        # se borra la imagen anterior y se coloca la nueva sin deformarla
        pagina.add_redact_annot(rect, fill=(1, 1, 1))
        pagina.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE)
        im = Image.open(fig)
        ar = im.width / im.height
        caja = rect
        if caja.width / caja.height > ar:
            ancho = caja.height * ar
            caja = pymupdf.Rect(caja.x0 + (caja.width - ancho) / 2, caja.y0,
                                caja.x0 + (caja.width - ancho) / 2 + ancho, caja.y1)
        else:
            alto = caja.width / ar
            caja = pymupdf.Rect(caja.x0, caja.y0 + (caja.height - alto) / 2,
                                caja.x1, caja.y0 + (caja.height - alto) / 2 + alto)
        pagina.insert_image(caja, filename=fig, keep_proportion=True)
    doc.saveIncr() if False else doc.save(ruta + ".tmp", garbage=3, deflate=True)
    doc.close()
    import os
    os.replace(ruta + ".tmp", ruta)
    return ruta


if __name__ == "__main__":
    for n in DOCX:
        print(arreglar_docx(n))
    for n in PDF:
        print(arreglar_pdf(n))
