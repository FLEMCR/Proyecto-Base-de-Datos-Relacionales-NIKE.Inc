# -*- coding: utf-8 -*-
"""Modelo final del proyecto NIKE Inc. - Grupo 05.

Fuente unica de verdad para el MER, el Excel de normalizacion y el modelo logico.

Reglas del modelo (tomadas del MER entregado y de la revision del docente):
  * ALMACEN se relaciona SOLO con SUMINISTRO (ABASTECE) y con PRODUCTO (ALMACENA).
    No existe ninguna clave de almacen en DETALLE_VENTA.
  * Ningun dato calculado se guarda: no hay total, no hay igv, no hay vista.
  * Solo tres columnas admiten NULL: telefono_secundario, descripcion, especificaciones.
"""

PROYECTO = {
    "nombre": "BD NIKE Inc.",
    "curso": "Disenio de Bases de Datos Relacionales",
    "institucion": "IDAT",
    "docente": "Sergio Fernando Castillo Carrion",
    "grupo": "Grupo 05",
    "integrantes": "Daniel Asmat | Salomon Fernandez | Luis Coloma | Pablo Rios",
    "alcance": "Ventas y Almacenes - Peru",
}

PROJ = "/home/user/proyecto_parcial"

# ---------------------------------------------------------------------------
# columnas: (nombre, tipo, largo, marca, opcional)
#   marca: "*" obligatoria, "o" opcional, "PK", "FK", "PFK" (clave compuesta + FK)
#   tipo : VARCHAR | DECIMAL | INTEGER | DATE | CHAR
# ---------------------------------------------------------------------------
TABLES = {
    "CLIENTE": {
        "rol": "Maestra",
        "proposito": "Registra al comprador; un cliente puede hacer muchos pedidos.",
        "cols": [
            ("id_cliente", "INTEGER", None, "PK", False),
            ("nombre", "VARCHAR", 80, "*", False),
            ("correo_electronico", "VARCHAR", 80, "*", False),
            ("telefono", "VARCHAR", 15, "*", False),
            ("telefono_secundario", "VARCHAR", 15, "o", True),
            ("direccion", "VARCHAR", 120, "*", False),
        ],
        "filas": [
            [1, "Carlos Mendoza", "cmendoza@gmail.com", "987654321", "945112233",
             "Av. Javier Prado 1240, San Isidro - Lima"],
            [2, "Lucia Paredes", "lparedes@hotmail.com", "912345678", "NULL",
             "Av. Ejercito 710, Cayma - Arequipa"],
        ],
    },
    "CATEGORIA": {
        "rol": "Maestra",
        "proposito": "Clasifica los productos en una linea comercial.",
        "cols": [
            ("id_categoria", "INTEGER", None, "PK", False),
            ("nombre", "VARCHAR", 50, "*", False),
            ("descripcion", "VARCHAR", 150, "o", True),
        ],
        "filas": [
            [10, "Calzado Running", "Zapatillas de entrenamiento y maraton"],
            [20, "Calzado Urbano", "Zapatillas de uso diario Sportswear"],
            [30, "Indumentaria Deportiva", "Polos, casacas y pantalones Dri-FIT"],
        ],
    },
    "ALMACEN": {
        "rol": "Maestra",
        "proposito": "Centro de distribucion que guarda stock y abastece a los locales.",
        "cols": [
            ("id_almacen", "INTEGER", None, "PK", False),
            ("nombre_almacen", "VARCHAR", 50, "*", False),
            ("ubicacion", "VARCHAR", 120, "*", False),
        ],
        "filas": [
            [100, "CD Lima Norte", "Av. Ramiro Priale Km 8 - Lima"],
            [200, "CD Trujillo Norte", "Parque Industrial La Esperanza - Trujillo"],
        ],
    },
    "LOCAL": {
        "rol": "Maestra",
        "proposito": "Tienda fisica que recibe mercaderia de los centros de distribucion.",
        "cols": [
            ("id_local", "INTEGER", None, "PK", False),
            ("nombre_local", "VARCHAR", 50, "*", False),
            ("direccion_local", "VARCHAR", 120, "*", False),
        ],
        "filas": [
            [501, "Nike Store Jockey Plaza", "Av. Javier Prado Este 4200, Surco - Lima"],
            [502, "Nike Store Mall Arequipa", "Av. Porongoche 500, Paucarpata - Arequipa"],
            [503, "Nike Store Mallplaza Trujillo", "Av. America Oeste 750 - Trujillo"],
        ],
    },
    "PRODUCTO": {
        "rol": "Maestra",
        "proposito": "Catalogo de modelos; las tallas y colores viven en el stock y en el detalle.",
        "cols": [
            ("id_producto", "INTEGER", None, "PK", False),
            ("nombre", "VARCHAR", 80, "*", False),
            ("especificaciones", "VARCHAR", 150, "o", True),
            ("precio_unitario_base", "DECIMAL", (10, 2), "*", False),
            ("estado", "VARCHAR", 20, "*", False),
            ("CATEGORIA_id_categoria", "INTEGER", None, "FK", False),
        ],
        "filas": [
            [1001, "Nike Air Zoom Pegasus 40", "Amortiguacion React con doble Zoom Air", 549.90,
             "DISPONIBLE", 10],
            [1002, "Nike Air Force 1 07", "Capellada de cuero con suela Air", 499.90,
             "DISPONIBLE", 20],
            [1003, "Camiseta Nike Dri-FIT Academy", "Tejido transpirable 100% poliester", 129.90,
             "DISPONIBLE", 30],
        ],
    },
    "PEDIDO": {
        "rol": "Transaccional",
        "proposito": "Cabecera de la compra: quien compra, cuando, como paga y con que suministro se atiende.",
        "cols": [
            ("id_pedido", "INTEGER", None, "PK", False),
            ("fecha", "DATE", None, "*", False),
            ("metodo_pago", "VARCHAR", 30, "*", False),
            ("CLIENTE_id_cliente", "INTEGER", None, "FK", False),
            ("SUMINISTRO_id_suministro", "INTEGER", None, "FK", False),
        ],
        "filas": [
            [9001, "2026-10-05", "Tarjeta de Credito", 1, 1],
            [9002, "2026-10-06", "Yape", 2, 2],
            [9003, "2026-10-06", "Tarjeta de Debito", 1, 3],
        ],
    },
    "SUMINISTRO": {
        "rol": "Transaccional",
        "proposito": "Cabecera del abastecimiento: de que almacen sale y a que local llega.",
        "cols": [
            ("id_suministro", "INTEGER", None, "PK", False),
            ("fecha_suministro", "DATE", None, "*", False),
            ("estado_despacho", "VARCHAR", 20, "*", False),
            ("ALMACEN_id_almacen", "INTEGER", None, "FK", False),
            ("LOCAL_id_local", "INTEGER", None, "FK", False),
        ],
        "filas": [
            [1, "2026-10-04", "ENTREGADO", 100, 501],
            [2, "2026-10-05", "EN RUTA", 100, 502],
            [3, "2026-10-06", "PROGRAMADO", 200, 503],
        ],
    },
    "DETALLE_VENTA": {
        "rol": "Intermedia",
        "proposito": "Resuelve CONTIENE: que producto, en que talla y color, cuanto y a que precio.",
        "cols": [
            ("PEDIDO_id_pedido", "INTEGER", None, "PFK", False),
            ("PRODUCTO_id_producto", "INTEGER", None, "PFK", False),
            ("talla_elegida", "VARCHAR", 10, "PK", False),
            ("color_elegido", "VARCHAR", 30, "PK", False),
            ("cantidad", "INTEGER", None, "*", False),
            ("precio_unitario_aplicado", "DECIMAL", (10, 2), "*", False),
        ],
        "filas": [
            [9001, 1001, "42", "Negro", 1, 549.90],
            [9001, 1002, "41", "Blanco", 1, 499.90],
            [9002, 1002, "41", "Blanco", 1, 499.90],
            [9003, 1003, "M", "Azul Marino", 2, 129.90],
        ],
    },
    "STOCK_ALMACEN": {
        "rol": "Intermedia",
        "proposito": "Resuelve ALMACENA: existencias por almacen, producto, talla y color.",
        "cols": [
            ("ALMACEN_id_almacen", "INTEGER", None, "PFK", False),
            ("PRODUCTO_id_producto", "INTEGER", None, "PFK", False),
            ("talla", "VARCHAR", 10, "PK", False),
            ("color", "VARCHAR", 30, "PK", False),
            ("stock_actual", "INTEGER", None, "*", False),
            ("stock_minimo", "INTEGER", None, "*", False),
        ],
        "filas": [
            [100, 1001, "42", "Negro", 85, 15],
            [100, 1002, "41", "Blanco", 120, 20],
            [200, 1003, "M", "Azul Marino", 200, 30],
        ],
    },
    "DETALLE_SUMINISTRO": {
        "rol": "Intermedia",
        "proposito": "Resuelve INCLUYE: que productos y cantidades lleva cada suministro.",
        "cols": [
            ("SUMINISTRO_id_suministro", "INTEGER", None, "PFK", False),
            ("PRODUCTO_id_producto", "INTEGER", None, "PFK", False),
            ("talla", "VARCHAR", 10, "PK", False),
            ("color", "VARCHAR", 30, "PK", False),
            ("cantidad", "INTEGER", None, "*", False),
        ],
        "filas": [
            [1, 1001, "42", "Negro", 20],
            [1, 1002, "41", "Blanco", 15],
            [2, 1002, "41", "Blanco", 25],
            [3, 1003, "M", "Azul Marino", 40],
        ],
    },
}

# orden de presentacion: maestras, transaccionales e intermedias
ORDER = ["CLIENTE", "CATEGORIA", "ALMACEN", "LOCAL", "PRODUCTO", "PEDIDO", "SUMINISTRO",
         "DETALLE_VENTA", "STOCK_ALMACEN", "DETALLE_SUMINISTRO"]

# ---------------------------------------------------------------------------
# claves foraneas: (restriccion, hija, columna, padre, columna_pk, relacion del MER)
# ---------------------------------------------------------------------------
FKS = [
    ("PRODUCTO_CATEGORIA_FK", "PRODUCTO", "CATEGORIA_id_categoria", "CATEGORIA", "id_categoria",
     "CLASIFICA"),
    ("PEDIDO_CLIENTE_FK", "PEDIDO", "CLIENTE_id_cliente", "CLIENTE", "id_cliente", "REALIZA"),
    ("PEDIDO_SUMINISTRO_FK", "PEDIDO", "SUMINISTRO_id_suministro", "SUMINISTRO", "id_suministro",
     "PROVEE"),
    ("SUMINISTRO_ALMACEN_FK", "SUMINISTRO", "ALMACEN_id_almacen", "ALMACEN", "id_almacen",
     "ABASTECE"),
    ("SUMINISTRO_LOCAL_FK", "SUMINISTRO", "LOCAL_id_local", "LOCAL", "id_local", "RECIBE"),
    ("DETALLE_VENTA_PEDIDO_FK", "DETALLE_VENTA", "PEDIDO_id_pedido", "PEDIDO", "id_pedido",
     "CONTIENE"),
    ("DETALLE_VENTA_PRODUCTO_FK", "DETALLE_VENTA", "PRODUCTO_id_producto", "PRODUCTO",
     "id_producto", "CONTIENE"),
    ("STOCK_ALMACEN_ALMACEN_FK", "STOCK_ALMACEN", "ALMACEN_id_almacen", "ALMACEN", "id_almacen",
     "ALMACENA"),
    ("STOCK_ALMACEN_PRODUCTO_FK", "STOCK_ALMACEN", "PRODUCTO_id_producto", "PRODUCTO",
     "id_producto", "ALMACENA"),
    ("DETALLE_SUMINISTRO_SUMINISTRO_FK", "DETALLE_SUMINISTRO", "SUMINISTRO_id_suministro",
     "SUMINISTRO", "id_suministro", "INCLUYE"),
    ("DETALLE_SUMINISTRO_PRODUCTO_FK", "DETALLE_SUMINISTRO", "PRODUCTO_id_producto", "PRODUCTO",
     "id_producto", "INCLUYE"),
]

# relaciones del MER: (nombre, cardinalidad, entidad_a, entidad_b, lectura)
RELACIONES = [
    ("REALIZA", "(1,N)", "CLIENTE", "PEDIDO", "Un CLIENTE realiza muchos PEDIDOS."),
    ("CONTIENE", "(M,N)", "PEDIDO", "PRODUCTO",
     "Un PEDIDO contiene muchos PRODUCTOS, cada uno con talla, color, cantidad y precio."),
    ("CLASIFICA", "(1,N)", "CATEGORIA", "PRODUCTO", "Una CATEGORIA clasifica muchos PRODUCTOS."),
    ("ALMACENA", "(M,N)", "PRODUCTO", "ALMACEN",
     "Un ALMACEN almacena muchos PRODUCTOS por talla y color."),
    ("PROVEE", "(1,N)", "PEDIDO", "SUMINISTRO", "Un SUMINISTRO provee a muchos PEDIDOS."),
    ("ABASTECE", "(1,N)", "ALMACEN", "SUMINISTRO", "Un ALMACEN abastece muchos SUMINISTROS."),
    ("RECIBE", "(1,N)", "LOCAL", "SUMINISTRO", "Un LOCAL recibe muchos SUMINISTROS."),
    ("INCLUYE", "(M,N)", "SUMINISTRO", "PRODUCTO",
     "Un SUMINISTRO incluye muchos PRODUCTOS con su cantidad, talla y color."),
]

ESTADOS = [
    ("estado_despacho", "SUMINISTRO", "Como va el traslado del centro de distribucion al local.",
     "PROGRAMADO, EN RUTA, ENTREGADO", "Suministro 2 = EN RUTA"),
    ("estado", "PRODUCTO", "Si el modelo esta disponible para la venta.",
     "DISPONIBLE, AGOTADO, DESCONTINUADO", "PRODUCTO 1001 = DISPONIBLE"),
]

# ---------------------------------------------------------------------------
# El estado del envio NO se guarda: se deduce del estado del suministro con el que
# se atiende el pedido. Este es el mapeo que se explica en las guias.
# ---------------------------------------------------------------------------
MAPEO_ESTADOS = [
    ("PENDIENTE", "PROGRAMADO", "El despacho aun no sale del centro de distribucion."),
    ("ENVIADO", "EN RUTA", "La mercaderia ya salio y va camino al local."),
    ("ENTREGADO", "ENTREGADO", "El local recibio la mercaderia y el pedido quedo atendido."),
]

# un pedido se atiende con un solo suministro, es decir, con un almacen y un local
REGLA_SUMINISTRO = (
    "Un PEDIDO se atiende con un solo SUMINISTRO: la clave foranea SUMINISTRO_id_suministro vive "
    "en PEDIDO como una sola columna obligatoria, asi que cada pedido guarda un unico suministro. "
    "Como cada SUMINISTRO tiene un unico ALMACEN de origen y un unico LOCAL de destino, un pedido "
    "queda ligado a un almacen y a un local, sin repetir esos datos en la tabla del pedido. La "
    "relacion PROVEE se lee 1:N: un suministro puede atender muchos pedidos."
)

JUSTIF = [
    ("id_cliente, id_pedido, id_producto, id_categoria, id_almacen, id_local, id_suministro",
     "INTEGER", "Son numeros enteros que se generan en el sistema y nunca se suman como importe."),
    ("telefono / telefono_secundario", "VARCHAR(15)",
     "9 digitos en Peru; 15 es el tope internacional (E.164) para un cliente extranjero."),
    ("correo_electronico", "VARCHAR(80)", "un correo real mide entre 25 y 45 caracteres; 80 deja margen."),
    ("nombre (CLIENTE) / nombre (PRODUCTO)", "VARCHAR(80)",
     "entran nombres completos y nombres comerciales largos."),
    ("direccion / direccion_local / ubicacion", "VARCHAR(120)",
     "una direccion peruana con referencia y distrito llega a 90-120 caracteres."),
    ("nombre_almacen / nombre_local / nombre de categoria", "VARCHAR(50)",
     "son nombres cortos e institucionales."),
    ("metodo_pago", "VARCHAR(30)", "'Tarjeta de Credito', 'Yape' o 'Transferencia' no pasan de 20."),
    ("estado_despacho / estado", "VARCHAR(20)",
     "listas cortas y controladas; el estado del envio no se guarda porque se deduce del despacho."),
    ("talla / talla_elegida", "VARCHAR(10)", "guarda 38, 42 o M."),
    ("color / color_elegido", "VARCHAR(30)", "guarda Negro, Blanco o Azul Marino."),
    ("especificaciones / descripcion", "VARCHAR(150)", "una ficha tecnica corta, no un manual."),
    ("cantidad, stock_actual, stock_minimo", "INTEGER", "son unidades enteras, no llevan decimales."),
    ("precio_unitario_base / precio_unitario_aplicado", "DECIMAL(10,2)",
     "8 enteros y 2 decimales alcanzan para millones de soles y evitan el redondeo del FLOAT."),
    ("fecha / fecha_suministro", "DATE", "solo se guarda el dia de la operacion."),
]

CORRECCIONES = [
    ("PK", "STOCK_ALMACEN con PK de 4 campos",
     "Se mantiene: el docente confirmo que estaba bien.",
     "STOCK_ALMACEN"),
    ("PK", "SUMINISTRO_LOCAL no permitia dos despachos el mismo dia",
     "Se creo SUMINISTRO con id_suministro como PK y DETALLE_SUMINISTRO con producto, talla, "
     "color y cantidad.", "SUMINISTRO y DETALLE_SUMINISTRO"),
    ("1FN", "'Yape / Plin' eran dos metodos en una celda",
     "Un solo metodo por fila: el pedido 9002 queda con 'Yape'.", "PEDIDO.metodo_pago"),
    ("1FN", "Se cambiaron los colores del stock",
     "Se restauraron los datos de la tabla general: Negro, Blanco y Azul Marino.",
     "STOCK_ALMACEN.color"),
    ("1FN", "PK de un solo campo en DETALLE_VENTA",
     "PK compuesta: pedido + producto + talla + color.", "DETALLE_VENTA"),
    ("2FN", "CLIENTE separado antes de tiempo",
     "En 2FN los datos del cliente se quedan dentro de PEDIDO; la separacion se hace en 3FN.",
     "Hoja 2FN"),
    ("2FN", "Se perdia que suministro corresponde a cada pedido",
     "PEDIDO guarda SUMINISTRO_id_suministro, obligatoria.", "PEDIDO.SUMINISTRO_id_suministro"),
    ("3FN", "total e igv se pueden calcular",
     "No se guardan: el total de la linea sale de cantidad x precio y el IGV del 18 % de la suma.",
     "Ninguna tabla"),
    ("3FN", "DETALLE_VENTA guardaba talla pero no color",
     "Se agrego color_elegido, porque el stock se maneja por talla y color.",
     "DETALLE_VENTA.color_elegido"),
    ("3FN", "El estado del envio se repetia en PEDIDO",
     "Se elimino la columna: el estado del pedido se deduce del estado_despacho del suministro "
     "que lo atiende (PENDIENTE = PROGRAMADO, ENVIADO = EN RUTA, ENTREGADO = ENTREGADO).",
     "PEDIDO.estado_envio"),
    ("0FN y 1FN", "Los productos y cantidades del suministro aparecian recien en 2FN",
     "Se agregaron a la tabla general como productos y cantidades suministradas, y la 1FN los "
     "deja atomicos en cada fila.", "Hoja 0FN y 1FN"),
    ("2FN", "Faltaban PRODUCTO, ALMACEN, LOCAL y STOCK_ALMACEN",
     "La hoja 2FN ahora tiene las ocho tablas: todo lo que estaba en la 1FN queda en alguna tabla.",
     "Hoja 2FN"),
    ("MER", "ALMACEN se conectaba con la venta",
     "El almacen solo se relaciona con SUMINISTRO (ABASTECE) y con PRODUCTO (ALMACENA); "
     "DETALLE_VENTA ya no guarda el almacen de origen.", "MER y DETALLE_VENTA"),
]

# ---------------------------------------------------------------------------
# CAPA FISICA: identidad, valores por omision, validaciones y auditoria.
# El modelo conceptual y el logico no muestran estas marcas; el script DDL si,
# porque son propiedades de la implementacion (lo pidio el docente al calificar).
# ---------------------------------------------------------------------------
IDENTIDAD = {
    "CLIENTE": "id_cliente",
    "CATEGORIA": "id_categoria",
    "ALMACEN": "id_almacen",
    "LOCAL": "id_local",
    "PRODUCTO": "id_producto",
    "PEDIDO": "id_pedido",
    "SUMINISTRO": "id_suministro",
}

# (tabla, columna, valor por omision, motivo)
DEFAULTS = [
    ("PEDIDO", "fecha", "CURRENT_DATE", "Si no se envia la fecha, se registra el dia de la venta."),
    ("PEDIDO", "metodo_pago", "'Tarjeta de Credito'", "Es el medio de pago mas usado en la tienda online."),
    ("SUMINISTRO", "fecha_suministro", "CURRENT_DATE", "Si no se envia la fecha, se registra el dia del despacho."),
    ("SUMINISTRO", "estado_despacho", "'PROGRAMADO'", "Todo despacho nuevo nace programado."),
    ("PRODUCTO", "estado", "'DISPONIBLE'", "Todo modelo nuevo entra disponible para la venta."),
    ("DETALLE_VENTA", "cantidad", "1", "Una linea sin cantidad explicita equivale a una unidad."),
    ("DETALLE_SUMINISTRO", "cantidad", "1", "Una linea sin cantidad explicita equivale a una unidad."),
    ("STOCK_ALMACEN", "stock_actual", "0", "Un producto recien registrado en el almacen arranca en cero."),
    ("STOCK_ALMACEN", "stock_minimo", "0", "Sin minimo definido, el almacen arranca en cero."),
]

# (nombre, tabla, condicion, motivo)
CHECKS = [
    ("CK_DETALLE_VENTA_CANTIDAD", "DETALLE_VENTA", "cantidad > 0",
     "Una linea de venta no puede tener cero ni cantidades negativas."),
    ("CK_DETALLE_SUMINISTRO_CANTIDAD", "DETALLE_SUMINISTRO", "cantidad > 0",
     "Un despacho no puede enviar cero ni cantidades negativas."),
    ("CK_DETALLE_VENTA_PRECIO", "DETALLE_VENTA", "precio_unitario_aplicado > 0",
     "El precio aplicado siempre es un importe positivo."),
    ("CK_PRODUCTO_PRECIO", "PRODUCTO", "precio_unitario_base > 0",
     "El precio de lista siempre es un importe positivo."),
    ("CK_STOCK_ALMACEN_ACTUAL", "STOCK_ALMACEN", "stock_actual >= 0",
     "El stock no puede quedar en negativo."),
    ("CK_STOCK_ALMACEN_MINIMO", "STOCK_ALMACEN", "stock_minimo >= 0",
     "El stock minimo es una cantidad, nunca negativa."),
    ("CK_SUMINISTRO_ESTADO", "SUMINISTRO",
     "estado_despacho IN ('PROGRAMADO', 'EN RUTA', 'ENTREGADO')",
     "Solo se admiten los tres estados del despacho al local."),
    ("CK_PRODUCTO_ESTADO", "PRODUCTO",
     "estado IN ('DISPONIBLE', 'AGOTADO', 'DESCONTINUADO')",
     "Solo se admiten los tres estados comerciales del modelo."),
    ("CK_CLIENTE_CORREO", "CLIENTE", "correo_electronico LIKE '%_@_%._%'",
     "Un correo mal escrito no llega al cliente."),
    ("CK_CLIENTE_TELEFONO", "CLIENTE",
     "telefono NOT LIKE '%[^0-9]%' AND LEN(telefono) BETWEEN 6 AND 15",
     "El telefono se guarda solo con digitos, sin espacios ni guiones."),
]

# columnas de auditoria que lleva TODA tabla en la base de datos
AUDITORIA = [
    ("usuario_creacion", "VARCHAR", 30, "SYSTEM_USER",
     "Quien inserto la fila (el usuario de la base de datos)."),
    ("fecha_creacion", "DATETIME", None, "CURRENT_TIMESTAMP",
     "Cuando se inserto la fila."),
    ("usuario_modificacion", "VARCHAR", 30, "NULL",
     "Quien hizo el ultimo cambio; nace en NULL."),
    ("fecha_modificacion", "DATETIME", None, "NULL",
     "Cuando se hizo el ultimo cambio; nace en NULL."),
]


# ---------------------------------------------------------------------------
def tipo_texto(col):
    """Devuelve el tipo y la longitud en texto, listo para el Excel y el diccionario."""
    nombre, tipo, largo, marca, opc = col
    if tipo == "VARCHAR":
        return tipo, str(largo)
    if tipo == "DECIMAL":
        return tipo, "%d,%d" % (largo[0], largo[1])
    return tipo, "-"


def tipo_sql(col, motor="sqlserver"):
    nombre, tipo, largo, marca, opc = col
    if tipo == "VARCHAR":
        return ("VARCHAR2(%d)" % largo) if motor == "oracle" else ("VARCHAR(%d)" % largo)
    if tipo == "DECIMAL":
        return ("NUMBER(%d,%d)" % largo) if motor == "oracle" else ("DECIMAL(%d,%d)" % largo)
    if tipo == "INTEGER":
        return "INTEGER"
    return "DATE"


def pk_cols(tabla):
    return [c[0] for c in TABLES[tabla]["cols"] if c[3] in ("PK", "PFK")]


def fk_cols(tabla):
    return [c[0] for c in TABLES[tabla]["cols"] if c[3] in ("FK", "PFK")]


def opcionales():
    out = []
    for t in ORDER:
        for c in TABLES[t]["cols"]:
            if c[4]:
                out.append((t, c[0]))
    return out


def fk_de(tabla, col):
    for nombre, hija, columna, padre, pkc, rel in FKS:
        if hija == tabla and columna == col:
            return padre, pkc
    raise KeyError("%s.%s" % (tabla, col))


def obligatoria(col):
    return not col[4]


def defaults_de(tabla):
    return [(col, valor, motivo) for t, col, valor, motivo in DEFAULTS if t == tabla]


def checks_de(tabla):
    return [(nombre, cond, motivo) for nombre, t, cond, motivo in CHECKS if t == tabla]


def es_identidad(tabla, col):
    return IDENTIDAD.get(tabla) == col


if __name__ == "__main__":
    print("tablas: %d | FK: %d | relaciones: %d | opcionales: %d"
          % (len(ORDER), len(FKS), len(RELACIONES), len(opcionales())))
    for t in ORDER:
        print("  %-20s PK=%s  FK=%s" % (t, ", ".join(pk_cols(t)) or "-",
                                        ", ".join(fk_cols(t)) or "-"))
