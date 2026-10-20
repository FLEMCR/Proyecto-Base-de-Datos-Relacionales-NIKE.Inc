CREATE DATABASE BD_NIKE_INC;
GO

USE BD_NIKE_INC;
GO

CREATE TABLE CLIENTE (
    id_cliente INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    correo_e VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NULL,
    direccion VARCHAR(200) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    usuario_creacion VARCHAR(50) NOT NULL DEFAULT SUSER_SNAME(),
    estado_registro CHAR(1) NOT NULL DEFAULT 'A',
    CONSTRAINT PK_CLIENTE PRIMARY KEY (id_cliente),
    CONSTRAINT UQ_CLIENTE_CORREO UNIQUE (correo_e),
    CONSTRAINT CHK_CLIENTE_ESTADO CHECK (estado_registro IN ('A', 'I'))
);
GO

CREATE TABLE CATEGORIA (
    id_categoria INT NOT NULL,
    nombre VARCHAR(80) NOT NULL,
    descripcion VARCHAR(200) NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    estado_registro CHAR(1) NOT NULL DEFAULT 'A',
    CONSTRAINT PK_CATEGORIA PRIMARY KEY (id_categoria),
    CONSTRAINT CHK_CATEGORIA_ESTADO CHECK (estado_registro IN ('A', 'I'))
);
GO

CREATE TABLE ALMACEN (
    id_almacen INT NOT NULL,
    nombre_almacen VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(150) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    estado_registro CHAR(1) NOT NULL DEFAULT 'A',
    CONSTRAINT PK_ALMACEN PRIMARY KEY (id_almacen),
    CONSTRAINT CHK_ALMACEN_ESTADO CHECK (estado_registro IN ('A', 'I'))
);
GO

CREATE TABLE LOCAL (
    id_local INT NOT NULL,
    nombre_local VARCHAR(100) NOT NULL,
    direccion_local VARCHAR(150) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    estado_registro CHAR(1) NOT NULL DEFAULT 'A',
    CONSTRAINT PK_LOCAL PRIMARY KEY (id_local),
    CONSTRAINT CHK_LOCAL_ESTADO CHECK (estado_registro IN ('A', 'I'))
);
GO

CREATE TABLE PRODUCTO (
    id_producto INT NOT NULL,
    CATEGORIA_id_categoria INT NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    especificaciones VARCHAR(255) NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    estado VARCHAR(20) NOT NULL DEFAULT 'DISPONIBLE',
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    fecha_modificacion DATETIME NULL,
    CONSTRAINT PK_PRODUCTO PRIMARY KEY (id_producto),
    CONSTRAINT FK_PROD_CATEGORIA FOREIGN KEY (CATEGORIA_id_categoria) REFERENCES CATEGORIA (id_categoria),
    CONSTRAINT CHK_PROD_PRECIO CHECK (precio_unitario > 0)
);
GO

CREATE TABLE PEDIDO (
    id_pedido INT NOT NULL,
    CLIENTE_id_cliente INT NOT NULL,
    fecha DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    metodo_pago VARCHAR(40) NOT NULL,
    igv DECIMAL(10,2) NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    estado_envio VARCHAR(30) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    usuario_modificacion VARCHAR(50) NULL,
    CONSTRAINT PK_PEDIDO PRIMARY KEY (id_pedido),
    CONSTRAINT FK_PEDIDO_CLIENTE FOREIGN KEY (CLIENTE_id_cliente) REFERENCES CLIENTE (id_cliente),
    CONSTRAINT CHK_PEDIDO_TOTAL CHECK (total >= 0)
);
GO

CREATE TABLE DETALLE_VENTA (
    id_detalle INT NOT NULL,
    PEDIDO_id_pedido INT NOT NULL,
    PRODUCTO_id_producto INT NOT NULL,
    talla_elegida VARCHAR(15) NOT NULL,
    cantidad INT NOT NULL,
    precio_venta DECIMAL(10,2) NOT NULL,
    total_linea DECIMAL(10,2) NOT NULL,
    fecha_creacion DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_DETALLE_VENTA PRIMARY KEY (id_detalle),
    CONSTRAINT FK_DET_PEDIDO FOREIGN KEY (PEDIDO_id_pedido) REFERENCES PEDIDO (id_pedido),
    CONSTRAINT FK_DET_PRODUCTO FOREIGN KEY (PRODUCTO_id_producto) REFERENCES PRODUCTO (id_producto),
    CONSTRAINT CHK_DET_CANTIDAD CHECK (cantidad > 0)
);
GO

CREATE TABLE STOCK_ALMACEN (
    ALMACEN_id_almacen INT NOT NULL,
    PRODUCTO_id_producto INT NOT NULL,
    talla VARCHAR(15) NOT NULL,
    color VARCHAR(40) NOT NULL,
    stock_actual INT NOT NULL,
    stock_minimo INT NOT NULL,
    fecha_actualizacion DATETIME NOT NULL DEFAULT GETDATE(),
    CONSTRAINT PK_STOCK_ALM PRIMARY KEY (ALMACEN_id_almacen, PRODUCTO_id_producto, talla, color),
    CONSTRAINT FK_STK_ALMACEN FOREIGN KEY (ALMACEN_id_almacen) REFERENCES ALMACEN (id_almacen),
    CONSTRAINT FK_STK_PRODUCTO FOREIGN KEY (PRODUCTO_id_producto) REFERENCES PRODUCTO (id_producto),
    CONSTRAINT CHK_STK_ACTUAL CHECK (stock_actual >= 0),
    CONSTRAINT CHK_STK_MINIMO CHECK (stock_minimo >= 0)
);
GO

CREATE TABLE SUMINISTRO_LOCAL (
    ALMACEN_id_almacen INT NOT NULL,
    LOCAL_id_local INT NOT NULL,
    fecha_suministro DATE NOT NULL,
    estado_despacho VARCHAR(30) NULL,
    usuario_creacion VARCHAR(50) NOT NULL DEFAULT SUSER_SNAME(),
    CONSTRAINT PK_SUMINISTRO PRIMARY KEY (ALMACEN_id_almacen, LOCAL_id_local, fecha_suministro),
    CONSTRAINT FK_SUM_ALMACEN FOREIGN KEY (ALMACEN_id_almacen) REFERENCES ALMACEN (id_almacen),
    CONSTRAINT FK_SUM_LOCAL FOREIGN KEY (LOCAL_id_local) REFERENCES LOCAL (id_local)
);
GO

CREATE NONCLUSTERED INDEX IDX_PEDIDO_CLIENTE ON PEDIDO (CLIENTE_id_cliente);
CREATE NONCLUSTERED INDEX IDX_PRODUCTO_CATEGORIA ON PRODUCTO (CATEGORIA_id_categoria);
CREATE NONCLUSTERED INDEX IDX_DETALLE_PEDIDO ON DETALLE_VENTA (PEDIDO_id_pedido);
CREATE NONCLUSTERED INDEX IDX_DETALLE_PRODUCTO ON DETALLE_VENTA (PRODUCTO_id_producto);
GO

INSERT INTO CLIENTE (id_cliente, nombre, correo_e, telefono, direccion) VALUES
(1, 'Carlos Mendoza', 'cmendoza@gmail.com', '987654321', 'Av. Javier Prado 1240, San Isidro'),
(2, 'Lucia Paredes', 'lparedes@hotmail.com', '912345678', 'Calle Las Begonias 450, Miraflores'),
(3, 'Diego Quispe', 'dquispe@outlook.com', '998877665', 'Av. Arequipa 2310, Lince');

INSERT INTO CATEGORIA (id_categoria, nombre, descripcion) VALUES
(10, 'Calzado Running', 'Zapatillas de entrenamiento y maraton'),
(20, 'Calzado Urbano', 'Zapatillas de uso diario y coleccion Sportswear'),
(30, 'Indumentaria Deportiva', 'Polos, casacas y pantalones Dri-FIT');

INSERT INTO ALMACEN (id_almacen, nombre_almacen, ubicacion) VALUES
(100, 'CD Lurigancho Norte', 'Av. Ramiro Priale Km 8, Lurigancho'),
(200, 'CD Villa El Salvador Sur', 'Panamericana Sur Km 19, Villa El Salvador');

INSERT INTO LOCAL (id_local, nombre_local, direccion_local) VALUES
(501, 'Nike Store Jockey Plaza', 'Av. Javier Prado Este 4200, Surco'),
(502, 'Nike Store Larcomar', 'Malecon de la Reserva 610, Miraflores'),
(503, 'Nike Store Plaza Norte', 'Av. Tomas Valle con Panamericana Norte, Independencia');

INSERT INTO PRODUCTO (id_producto, CATEGORIA_id_categoria, nombre, especificaciones, precio_unitario, estado) VALUES
(1001, 10, 'Nike Air Zoom Pegasus 40', 'Amortiguacion React con doble unidad Zoom Air', 549.90, 'DISPONIBLE'),
(1002, 20, 'Nike Air Force 1 07', 'Capellada de cuero con suela Air encapsulada', 499.90, 'DISPONIBLE'),
(1003, 30, 'Camiseta Nike Dri-FIT Academy', 'Tejido transpirable 100% poliester reciclado', 129.90, 'DISPONIBLE');

INSERT INTO STOCK_ALMACEN (ALMACEN_id_almacen, PRODUCTO_id_producto, talla, color, stock_actual, stock_minimo) VALUES
(100, 1001, '42', 'Negro/Blanco', 85, 15),
(100, 1002, '41', 'Blanco Total', 120, 20),
(200, 1003, 'M', 'Azul Marino', 200, 30);

INSERT INTO SUMINISTRO_LOCAL (ALMACEN_id_almacen, LOCAL_id_local, fecha_suministro, estado_despacho) VALUES
(100, 501, '2026-10-04', 'ENTREGADO'),
(100, 502, '2026-10-05', 'EN RUTA'),
(200, 503, '2026-10-06', 'PROGRAMADO');

INSERT INTO PEDIDO (id_pedido, CLIENTE_id_cliente, fecha, metodo_pago, igv, total, estado_envio) VALUES
(9001, 1, '2026-10-05', 'Tarjeta de Credito', 188.96, 1238.76, 'ENVIADO'),
(9002, 2, '2026-10-06', 'Yape / Plin', 89.98, 589.88, 'ENTREGADO');

INSERT INTO DETALLE_VENTA (id_detalle, PEDIDO_id_pedido, PRODUCTO_id_producto, talla_elegida, cantidad, precio_venta, total_linea) VALUES
(1, 9001, 1001, '42', 1, 549.90, 549.90),
(2, 9001, 1002, '41', 1, 499.90, 499.90),
(3, 9002, 1002, '41', 1, 499.90, 499.90);
GO
