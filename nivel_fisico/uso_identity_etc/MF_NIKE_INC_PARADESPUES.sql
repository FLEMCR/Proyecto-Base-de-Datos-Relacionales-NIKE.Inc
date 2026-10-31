-- =====================================================================
-- BD NIKE Inc. | Grupo 05
-- Script corregido a partir del DDL de Data Modeler (se respetan los
-- nombres y tipos originales del grupo) + lo que faltaba para el fisico:
--   IDENTITY (7) | DEFAULT (10) | CHECK (10) | auditoria (4 x 10)
-- Sin vistas y sin columnas calculadas (no hay total ni igv).
--
-- Errores corregidos respecto al script anterior:
--   1. "CREATE NIKE_INC_BD" no es SQL valido -> CREATE DATABASE
--   2. Faltaban IDENTITY, DEFAULT, CHECK y columnas de auditoria
-- =====================================================================

IF DB_ID('NIKE_INC_BD') IS NOT NULL
    DROP DATABASE NIKE_INC_BD;
GO

CREATE DATABASE NIKE_INC_BD;
GO

USE NIKE_INC_BD;
GO

-- ---------------------------------------------------------------------
-- 1. ALMACEN
-- ---------------------------------------------------------------------
CREATE TABLE ALMACEN
    (
     id_almacen              INT IDENTITY(1,1) NOT NULL ,
     nombre_almacen          VARCHAR (50) NOT NULL ,
     ubicacion               VARCHAR (120) NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT ALMACEN_PK PRIMARY KEY CLUSTERED (id_almacen)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON )
    )
GO

-- ---------------------------------------------------------------------
-- 2. CATEGORIA
-- ---------------------------------------------------------------------
CREATE TABLE CATEGORIA
    (
     id_categoria            INT IDENTITY(1,1) NOT NULL ,
     nombre                  VARCHAR (50) NOT NULL ,
     descripcion             VARCHAR (150) ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT CATEGORIA_PK PRIMARY KEY CLUSTERED (id_categoria)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON )
    )
GO

-- ---------------------------------------------------------------------
-- 3. CLIENTE
-- ---------------------------------------------------------------------
CREATE TABLE CLIENTE
    (
     id_cliente              INT IDENTITY(1,1) NOT NULL ,
     nombre                  VARCHAR (80) NOT NULL ,
     correo_electronico      VARCHAR (80) NOT NULL ,
     telefono                VARCHAR (15) NOT NULL ,
     telefono_secundario     VARCHAR (15) ,
     direccion               VARCHAR (120) NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT CLIENTE_PK PRIMARY KEY CLUSTERED (id_cliente)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON ) ,
     CONSTRAINT CK_CLIENTE_CORREO CHECK (correo_electronico LIKE '%_@_%._%') ,
     CONSTRAINT CK_CLIENTE_TELEFONO CHECK (telefono NOT LIKE '%[^0-9]%'
                                           AND LEN(telefono) BETWEEN 6 AND 15)
    )
GO

-- ---------------------------------------------------------------------
-- 4. DETALLE_SUMINISTRO  (clave compuesta: no lleva IDENTITY)
-- ---------------------------------------------------------------------
CREATE TABLE DETALLE_SUMINISTRO
    (
     talla                   VARCHAR (10) NOT NULL ,
     color                   VARCHAR (30) NOT NULL ,
     cantidad                INTEGER DEFAULT 1 NOT NULL ,
     PRODUCTO_id_producto    INTEGER NOT NULL ,
     SUMINISTRO_id_suministro INTEGER NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT DETALLE_SUMINISTRO_PK PRIMARY KEY CLUSTERED
        (color, PRODUCTO_id_producto, SUMINISTRO_id_suministro, talla)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON ) ,
     CONSTRAINT CK_DETALLE_SUMINISTRO_CANTIDAD CHECK (cantidad > 0)
    )
GO

-- ---------------------------------------------------------------------
-- 5. DETALLE_VENTA  (clave compuesta: no lleva IDENTITY)
-- ---------------------------------------------------------------------
CREATE TABLE DETALLE_VENTA
    (
     talla_elegida           VARCHAR (10) NOT NULL ,
     color_elegido           VARCHAR (30) NOT NULL ,
     cantidad                INTEGER DEFAULT 1 NOT NULL ,
     precio_unitario_aplicado NUMERIC (10,2) NOT NULL ,
     PEDIDO_id_pedido        INTEGER NOT NULL ,
     PRODUCTO_id_producto    INTEGER NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT DETALLE_VENTA_PK PRIMARY KEY CLUSTERED
        (talla_elegida, color_elegido, PEDIDO_id_pedido, PRODUCTO_id_producto)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON ) ,
     CONSTRAINT CK_DETALLE_VENTA_CANTIDAD CHECK (cantidad > 0) ,
     CONSTRAINT CK_DETALLE_VENTA_PRECIO CHECK (precio_unitario_aplicado > 0)
    )
GO

-- ---------------------------------------------------------------------
-- 6. LOCAL
-- ---------------------------------------------------------------------
CREATE TABLE LOCAL
    (
     id_local                INT IDENTITY(1,1) NOT NULL ,
     nombre_local            VARCHAR (50) NOT NULL ,
     direccion_local         VARCHAR (120) NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT LOCAL_PK PRIMARY KEY CLUSTERED (id_local)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON )
    )
GO

-- ---------------------------------------------------------------------
-- 7. PEDIDO   (sin estado_envio: se deduce del estado_despacho)
-- ---------------------------------------------------------------------
CREATE TABLE PEDIDO
    (
     id_pedido               INT IDENTITY(1,1) NOT NULL ,
     fecha                   DATE DEFAULT CAST(GETDATE() AS DATE) NOT NULL ,
     metodo_pago             VARCHAR (30) DEFAULT 'Tarjeta de Credito' NOT NULL ,
     SUMINISTRO_id_suministro INTEGER NOT NULL ,
     CLIENTE_id_cliente      INTEGER NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT PEDIDO_PK PRIMARY KEY CLUSTERED (id_pedido)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON )
    )
GO

-- ---------------------------------------------------------------------
-- 8. PRODUCTO
-- ---------------------------------------------------------------------
CREATE TABLE PRODUCTO
    (
     id_producto             INT IDENTITY(1,1) NOT NULL ,
     nombre                  VARCHAR (80) NOT NULL ,
     especificaciones        VARCHAR (150) ,
     precio_unitario_base    NUMERIC (10,2) NOT NULL ,
     estado                  VARCHAR (20) DEFAULT 'DISPONIBLE' NOT NULL ,
     CATEGORIA_id_categoria  INTEGER NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT PRODUCTO_PK PRIMARY KEY CLUSTERED (id_producto)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON ) ,
     CONSTRAINT CK_PRODUCTO_PRECIO CHECK (precio_unitario_base > 0) ,
     CONSTRAINT CK_PRODUCTO_ESTADO CHECK (estado IN ('DISPONIBLE', 'AGOTADO', 'DESCONTINUADO'))
    )
GO

-- ---------------------------------------------------------------------
-- 9. STOCK_ALMACEN  (clave compuesta: no lleva IDENTITY)
-- ---------------------------------------------------------------------
CREATE TABLE STOCK_ALMACEN
    (
     talla                   VARCHAR (10) NOT NULL ,
     color                   VARCHAR (30) NOT NULL ,
     stock_actual            INTEGER DEFAULT 0 NOT NULL ,
     stock_minimo            INTEGER DEFAULT 0 NOT NULL ,
     PRODUCTO_id_producto    INTEGER NOT NULL ,
     ALMACEN_id_almacen      INTEGER NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT STOCK_ALMACEN_PK PRIMARY KEY CLUSTERED
        (talla, color, PRODUCTO_id_producto, ALMACEN_id_almacen)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON ) ,
     CONSTRAINT CK_STOCK_ALMACEN_ACTUAL CHECK (stock_actual >= 0) ,
     CONSTRAINT CK_STOCK_ALMACEN_MINIMO CHECK (stock_minimo >= 0)
    )
GO

-- ---------------------------------------------------------------------
-- 10. SUMINISTRO
-- ---------------------------------------------------------------------
CREATE TABLE SUMINISTRO
    (
     id_suministro           INT IDENTITY(1,1) NOT NULL ,
     fecha_suministro        DATE DEFAULT CAST(GETDATE() AS DATE) NOT NULL ,
     estado_despacho         VARCHAR (20) DEFAULT 'PROGRAMADO' NOT NULL ,
     ALMACEN_id_almacen      INTEGER NOT NULL ,
     LOCAL_id_local          INTEGER NOT NULL ,
     usuario_creacion        VARCHAR (30) DEFAULT SYSTEM_USER NOT NULL ,
     fecha_creacion          DATETIME DEFAULT GETDATE() NOT NULL ,
     usuario_modificacion    VARCHAR (30) ,
     fecha_modificacion      DATETIME ,
     CONSTRAINT SUMINISTRO_PK PRIMARY KEY CLUSTERED (id_suministro)
     WITH (
     ALLOW_PAGE_LOCKS = ON ,
     ALLOW_ROW_LOCKS = ON ) ,
     CONSTRAINT CK_SUMINISTRO_ESTADO CHECK (estado_despacho IN ('PROGRAMADO', 'EN RUTA', 'ENTREGADO'))
    )
GO

-- =====================================================================
-- CLAVES FORANEAS (11)
-- =====================================================================
ALTER TABLE DETALLE_SUMINISTRO
    ADD CONSTRAINT DETALLE_SUMINISTRO_PRODUCTO_FK FOREIGN KEY (PRODUCTO_id_producto)
    REFERENCES PRODUCTO (id_producto) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE DETALLE_SUMINISTRO
    ADD CONSTRAINT DETALLE_SUMINISTRO_SUMINISTRO_FK FOREIGN KEY (SUMINISTRO_id_suministro)
    REFERENCES SUMINISTRO (id_suministro) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE DETALLE_VENTA
    ADD CONSTRAINT DETALLE_VENTA_PEDIDO_FK FOREIGN KEY (PEDIDO_id_pedido)
    REFERENCES PEDIDO (id_pedido) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE DETALLE_VENTA
    ADD CONSTRAINT DETALLE_VENTA_PRODUCTO_FK FOREIGN KEY (PRODUCTO_id_producto)
    REFERENCES PRODUCTO (id_producto) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE PEDIDO
    ADD CONSTRAINT PEDIDO_CLIENTE_FK FOREIGN KEY (CLIENTE_id_cliente)
    REFERENCES CLIENTE (id_cliente) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE PEDIDO
    ADD CONSTRAINT PEDIDO_SUMINISTRO_FK FOREIGN KEY (SUMINISTRO_id_suministro)
    REFERENCES SUMINISTRO (id_suministro) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE PRODUCTO
    ADD CONSTRAINT PRODUCTO_CATEGORIA_FK FOREIGN KEY (CATEGORIA_id_categoria)
    REFERENCES CATEGORIA (id_categoria) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE STOCK_ALMACEN
    ADD CONSTRAINT STOCK_ALMACEN_ALMACEN_FK FOREIGN KEY (ALMACEN_id_almacen)
    REFERENCES ALMACEN (id_almacen) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE STOCK_ALMACEN
    ADD CONSTRAINT STOCK_ALMACEN_PRODUCTO_FK FOREIGN KEY (PRODUCTO_id_producto)
    REFERENCES PRODUCTO (id_producto) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE SUMINISTRO
    ADD CONSTRAINT SUMINISTRO_ALMACEN_FK FOREIGN KEY (ALMACEN_id_almacen)
    REFERENCES ALMACEN (id_almacen) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

ALTER TABLE SUMINISTRO
    ADD CONSTRAINT SUMINISTRO_LOCAL_FK FOREIGN KEY (LOCAL_id_local)
    REFERENCES LOCAL (id_local) ON DELETE NO ACTION ON UPDATE NO ACTION
GO

-- =====================================================================
-- COMPROBACION (ejecuta esto al final)
-- =====================================================================
SELECT COUNT(*) AS tablas FROM sys.tables;                 -- 10
SELECT COUNT(*) AS foraneas FROM sys.foreign_keys;         -- 11
SELECT COUNT(*) AS vistas FROM sys.views;                  -- 0
SELECT COUNT(*) AS checks FROM sys.check_constraints;      -- 10
SELECT t.name AS tabla, c.name AS columna
FROM sys.columns c JOIN sys.tables t ON t.object_id = c.object_id
WHERE c.is_identity = 1 ORDER BY t.name;                   -- 7 filas
SELECT t.name AS tabla, c.name AS columna
FROM sys.columns c JOIN sys.tables t ON t.object_id = c.object_id
WHERE c.is_nullable = 1 AND c.name NOT LIKE '%modificacion'
ORDER BY t.name, c.column_id;                              -- 3 filas
GO
