# -*- coding: utf-8 -*-
"""Arma la GUIA COMPLETA concatenando las guias 01..07 de /home/user/guias.

Regla: el encabezado (titulo, integrantes, indice) se escribe aqui una sola vez;
de cada guia se quita su H1 para no repetir titulos, y en la guia 1 tambien se
quita el bloque de integrantes porque ya esta en el encabezado.
"""
import glob
import os

DIR = "/home/user/guias"
SALIDA = os.path.join(DIR, "GUIA_PROYECTO_NIKE_GRUPO_5.md")

CABECERA = """# GUIA COMPLETA DEL PROYECTO - BD NIKE Inc. (Grupo 05)


**Grupo 5:** Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios  
**Curso:** Disenio de Bases de Datos Relacionales - IDAT  
**Docente:** Sergio Fernando Castillo Carrion

---

Esta guia reune las **siete** guias del proyecto en un solo documento. Cada una tambien esta
como archivo suelto en esta misma carpeta (`01_...md` a `07_...md`).

| Guia | Tema |
| :--- | :--- |
| 1 | Entender el proyecto y leer el diagrama M.E.R. (Draw.io) |
| 2 | Normalizacion 0FN, 1FN, 2FN y 3FN en Excel |
| 3 | Modelo logico y relacional en Oracle Data Modeler (Barker) |
| 4 | Modelo fisico en SQL Server (SSMS) con IDENTITY, DEFAULT, CHECK y auditoria |
| 5 | Longitudes justas y columnas opcionales |
| 6 | Correcciones del docente aplicadas en las tres revisiones |
| 7 | Diccionario de datos y cierre de la entrega |

---

"""


def cuerpo(ruta, primera):
    lineas = open(ruta, encoding="utf-8").read().splitlines()
    # fuera el H1
    if lineas and lineas[0].startswith("# "):
        lineas = lineas[1:]
    texto = "\n".join(lineas).strip("\n")
    if primera:
        # fuera el bloque de integrantes (ya esta en la cabecera)
        if texto.lstrip().startswith("**Grupo 5:**"):
            texto = texto.split("\n---\n", 1)[1].lstrip("\n")
    return texto.rstrip("\n")


def main():
    rutas = sorted(glob.glob(os.path.join(DIR, "0[1-7]_*.md")))
    partes = [CABECERA]
    for i, r in enumerate(rutas):
        partes.append(cuerpo(r, i == 0))
        partes.append("\n---\n")
    open(SALIDA, "w", encoding="utf-8").write("\n".join(partes))
    print("guias:", len(rutas), "->", SALIDA, os.path.getsize(SALIDA), "bytes")


if __name__ == "__main__":
    main()
