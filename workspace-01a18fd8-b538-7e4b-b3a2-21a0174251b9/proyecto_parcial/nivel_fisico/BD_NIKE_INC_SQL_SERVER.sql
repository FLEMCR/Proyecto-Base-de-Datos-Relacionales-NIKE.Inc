-- =====================================================================
-- BD NIKE Inc. | Grupo 05 | Diseno de Bases de Datos Relacionales
-- MODELO FISICO - Microsoft SQL Server (SSMS)
-- 10 tablas | 11 claves foraneas | PK compuestas
-- IDENTITY | DEFAULT | CHECK | 4 campos de auditoria
-- Ninguna columna calculada: no hay total, no hay igv, no hay vistas.
-- =====================================================================
IF DB_ID('NIKE_INC_BD') IS NOT NULL
    DROP DATABASE NIKE_INC_BD;
GO
CREATE DATABASE NIKE_INC_BD;
GO
USE NIKE_INC_BD;
GO

-- ---------------------------------------------------------------------
-- 1. CLIENTE - Maestra
-- Registra al comprador; un cliente puede hacer muchos pedidos.
-- ---------------------------------------------------------------------
CREATE TABLE CLIENTE (
    id_cliente                   INT IDENTITY(1,1) NOT NULL,
    nombre                       VARCHAR(80) NOT NULL,
    correo_electronico           VARCHAR(80) NOT NULL,
    telefono                     VARCHAR(15) NOT NULL,
    telefono_secundario          VARCHAR(15),
    direccion                    VARCHAR(120) NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT CLIENTE_PK PRIMARY KEY (id_cliente),
    CONSTRAINT CK_CLIENTE_CORREO CHECK (correo_electronico LIKE '%_@_%._%'),
    CONSTRAINT CK_CLIENTE_TELEFONO CHECK (telefono NOT LIKE '%[^0-9]%' AND LEN(telefono) BETWEEN 6 AND 15)
);
GO

-- ---------------------------------------------------------------------
-- 2. CATEGORIA - Maestra
-- Clasifica los productos en una linea comercial.
-- ---------------------------------------------------------------------
CREATE TABLE CATEGORIA (
    id_categoria                 INT IDENTITY(1,1) NOT NULL,
    nombre                       VARCHAR(50) NOT NULL,
    descripcion                  VARCHAR(150),
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT CATEGORIA_PK PRIMARY KEY (id_categoria)
);
GO

-- ---------------------------------------------------------------------
-- 3. ALMACEN - Maestra
-- Centro de distribucion que guarda stock y abastece a los locales.
-- ---------------------------------------------------------------------
CREATE TABLE ALMACEN (
    id_almacen                   INT IDENTITY(1,1) NOT NULL,
    nombre_almacen               VARCHAR(50) NOT NULL,
    ubicacion                    VARCHAR(120) NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT ALMACEN_PK PRIMARY KEY (id_almacen)
);
GO

-- ---------------------------------------------------------------------
-- 4. LOCAL - Maestra
-- Tienda fisica que recibe mercaderia de los centros de distribucion.
-- ---------------------------------------------------------------------
CREATE TABLE LOCAL (
    id_local                     INT IDENTITY(1,1) NOT NULL,
    nombre_local                 VARCHAR(50) NOT NULL,
    direccion_local              VARCHAR(120) NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT LOCAL_PK PRIMARY KEY (id_local)
);
GO

-- ---------------------------------------------------------------------
-- 5. PRODUCTO - Maestra
-- Catalogo de modelos; las tallas y colores viven en el stock y en el detalle.
-- ---------------------------------------------------------------------
CREATE TABLE PRODUCTO (
    id_producto                  INT IDENTITY(1,1) NOT NULL,
    nombre                       VARCHAR(80) NOT NULL,
    especificaciones             VARCHAR(150),
    precio_unitario_base         DECIMAL(10,2) NOT NULL,
    estado                       VARCHAR(20) DEFAULT 'DISPONIBLE' NOT NULL,
    CATEGORIA_id_categoria       INTEGER NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT PRODUCTO_PK PRIMARY KEY (id_producto),
    CONSTRAINT CK_PRODUCTO_PRECIO CHECK (precio_unitario_base > 0),
    CONSTRAINT CK_PRODUCTO_ESTADO CHECK (estado IN ('DISPONIBLE', 'AGOTADO', 'DESCONTINUADO'))
);
GO

-- ---------------------------------------------------------------------
-- 6. PEDIDO - Transaccional
-- Cabecera de la compra: quien compra, cuando, como paga y con que suministro se atiende.
-- ---------------------------------------------------------------------
CREATE TABLE PEDIDO (
    id_pedido                    INT IDENTITY(1,1) NOT NULL,
    fecha                        DATE DEFAULT CAST(GETDATE() AS DATE) NOT NULL,
    metodo_pago                  VARCHAR(30) DEFAULT 'Tarjeta de Credito' NOT NULL,
    CLIENTE_id_cliente           INTEGER NOT NULL,
    SUMINISTRO_id_suministro     INTEGER NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT PEDIDO_PK PRIMARY KEY (id_pedido)
);
GO

-- ---------------------------------------------------------------------
-- 7. SUMINISTRO - Transaccional
-- Cabecera del abastecimiento: de que almacen sale y a que local llega.
-- ---------------------------------------------------------------------
CREATE TABLE SUMINISTRO (
    id_suministro                INT IDENTITY(1,1) NOT NULL,
    fecha_suministro             DATE DEFAULT CAST(GETDATE() AS DATE) NOT NULL,
    estado_despacho              VARCHAR(20) DEFAULT 'PROGRAMADO' NOT NULL,
    ALMACEN_id_almacen           INTEGER NOT NULL,
    LOCAL_id_local               INTEGER NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT SUMINISTRO_PK PRIMARY KEY (id_suministro),
    CONSTRAINT CK_SUMINISTRO_ESTADO CHECK (estado_despacho IN ('PROGRAMADO', 'EN RUTA', 'ENTREGADO'))
);
GO

-- ---------------------------------------------------------------------
-- 8. DETALLE_VENTA - Intermedia
-- Resuelve CONTIENE: que producto, en que talla y color, cuanto y a que precio.
-- ---------------------------------------------------------------------
CREATE TABLE DETALLE_VENTA (
    PEDIDO_id_pedido             INTEGER NOT NULL,
    PRODUCTO_id_producto         INTEGER NOT NULL,
    talla_elegida                VARCHAR(10) NOT NULL,
    color_elegido                VARCHAR(30) NOT NULL,
    cantidad                     INTEGER DEFAULT 1 NOT NULL,
    precio_unitario_aplicado     DECIMAL(10,2) NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT DETALLE_VENTA_PK PRIMARY KEY (PEDIDO_id_pedido, PRODUCTO_id_producto, talla_elegida, color_elegido),
    CONSTRAINT CK_DETALLE_VENTA_CANTIDAD CHECK (cantidad > 0),
    CONSTRAINT CK_DETALLE_VENTA_PRECIO CHECK (precio_unitario_aplicado > 0)
);
GO

-- ---------------------------------------------------------------------
-- 9. STOCK_ALMACEN - Intermedia
-- Resuelve ALMACENA: existencias por almacen, producto, talla y color.
-- ---------------------------------------------------------------------
CREATE TABLE STOCK_ALMACEN (
    ALMACEN_id_almacen           INTEGER NOT NULL,
    PRODUCTO_id_producto         INTEGER NOT NULL,
    talla                        VARCHAR(10) NOT NULL,
    color                        VARCHAR(30) NOT NULL,
    stock_actual                 INTEGER DEFAULT 0 NOT NULL,
    stock_minimo                 INTEGER DEFAULT 0 NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT STOCK_ALMACEN_PK PRIMARY KEY (ALMACEN_id_almacen, PRODUCTO_id_producto, talla, color),
    CONSTRAINT CK_STOCK_ALMACEN_ACTUAL CHECK (stock_actual >= 0),
    CONSTRAINT CK_STOCK_ALMACEN_MINIMO CHECK (stock_minimo >= 0)
);
GO

-- ---------------------------------------------------------------------
-- 10. DETALLE_SUMINISTRO - Intermedia
-- Resuelve INCLUYE: que productos y cantidades lleva cada suministro.
-- ---------------------------------------------------------------------
CREATE TABLE DETALLE_SUMINISTRO (
    SUMINISTRO_id_suministro     INTEGER NOT NULL,
    PRODUCTO_id_producto         INTEGER NOT NULL,
    talla                        VARCHAR(10) NOT NULL,
    color                        VARCHAR(30) NOT NULL,
    cantidad                     INTEGER DEFAULT 1 NOT NULL,
    usuario_creacion             VARCHAR(30) DEFAULT SYSTEM_USER NOT NULL,
    fecha_creacion               DATETIME DEFAULT GETDATE() NOT NULL,
    usuario_modificacion         VARCHAR(30),
    fecha_modificacion           DATETIME,
    CONSTRAINT DETALLE_SUMINISTRO_PK PRIMARY KEY (SUMINISTRO_id_suministro, PRODUCTO_id_producto, talla, color),
    CONSTRAINT CK_DETALLE_SUMINISTRO_CANTIDAD CHECK (cantidad > 0)
);
GO

-- =====================================================================
-- CLAVES FORANEAS (11)
-- =====================================================================
ALTER TABLE PRODUCTO
    ADD CONSTRAINT PRODUCTO_CATEGORIA_FK FOREIGN KEY (CATEGORIA_id_categoria)
    REFERENCES CATEGORIA (id_categoria) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion CLASIFICA del MER
GO
ALTER TABLE PEDIDO
    ADD CONSTRAINT PEDIDO_CLIENTE_FK FOREIGN KEY (CLIENTE_id_cliente)
    REFERENCES CLIENTE (id_cliente) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion REALIZA del MER
GO
ALTER TABLE PEDIDO
    ADD CONSTRAINT PEDIDO_SUMINISTRO_FK FOREIGN KEY (SUMINISTRO_id_suministro)
    REFERENCES SUMINISTRO (id_suministro) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion PROVEE del MER
GO
ALTER TABLE SUMINISTRO
    ADD CONSTRAINT SUMINISTRO_ALMACEN_FK FOREIGN KEY (ALMACEN_id_almacen)
    REFERENCES ALMACEN (id_almacen) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion ABASTECE del MER
GO
ALTER TABLE SUMINISTRO
    ADD CONSTRAINT SUMINISTRO_LOCAL_FK FOREIGN KEY (LOCAL_id_local)
    REFERENCES LOCAL (id_local) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion RECIBE del MER
GO
ALTER TABLE DETALLE_VENTA
    ADD CONSTRAINT DETALLE_VENTA_PEDIDO_FK FOREIGN KEY (PEDIDO_id_pedido)
    REFERENCES PEDIDO (id_pedido) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion CONTIENE del MER
GO
ALTER TABLE DETALLE_VENTA
    ADD CONSTRAINT DETALLE_VENTA_PRODUCTO_FK FOREIGN KEY (PRODUCTO_id_producto)
    REFERENCES PRODUCTO (id_producto) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion CONTIENE del MER
GO
ALTER TABLE STOCK_ALMACEN
    ADD CONSTRAINT STOCK_ALMACEN_ALMACEN_FK FOREIGN KEY (ALMACEN_id_almacen)
    REFERENCES ALMACEN (id_almacen) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion ALMACENA del MER
GO
ALTER TABLE STOCK_ALMACEN
    ADD CONSTRAINT STOCK_ALMACEN_PRODUCTO_FK FOREIGN KEY (PRODUCTO_id_producto)
    REFERENCES PRODUCTO (id_producto) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion ALMACENA del MER
GO
ALTER TABLE DETALLE_SUMINISTRO
    ADD CONSTRAINT DETALLE_SUMINISTRO_SUMINISTRO_FK FOREIGN KEY (SUMINISTRO_id_suministro)
    REFERENCES SUMINISTRO (id_suministro) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion INCLUYE del MER
GO
ALTER TABLE DETALLE_SUMINISTRO
    ADD CONSTRAINT DETALLE_SUMINISTRO_PRODUCTO_FK FOREIGN KEY (PRODUCTO_id_producto)
    REFERENCES PRODUCTO (id_producto) ON DELETE NO ACTION ON UPDATE NO ACTION;
    -- relacion INCLUYE del MER
GO

-- =====================================================================
-- COMPROBACION
-- =====================================================================
EXEC sp_help 'STOCK_ALMACEN';        -- se ven IDENTITY, DEFAULT, CHECK y auditoria
SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS ORDER BY TABLE_NAME, ORDINAL_POSITION;
GO

-- =====================================================================
-- DATOS DE PRUEBA: el INSERT no envia las claves ni las auditorias,
-- las genera IDENTITY y los DEFAULT.
-- =====================================================================
INSERT INTO CATEGORIA (nombre, descripcion)
VALUES ('Calzado Running', 'Zapatillas de entrenamiento y maraton');
INSERT INTO CLIENTE (nombre, correo_electronico, telefono, direccion)
VALUES ('Carlos Mendoza', 'cmendoza@gmail.com', '987654321',
        'Av. Javier Prado 1240, San Isidro - Lima');
INSERT INTO PEDIDO (CLIENTE_id_cliente, SUMINISTRO_id_suministro, fecha)
VALUES (1, 1, '2026-09-14');   -- metodo_pago y fecha salen de los DEFAULT
GO
-- fin del script
