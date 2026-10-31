CREATE DATABASE NIKE_INC_BD
GO

USE NIKE_INC_BD

-- Generado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   en:        2026-10-30 21:27:43 PET
--   sitio:      SQL Server 2012
--   tipo:      SQL Server 2012



CREATE TABLE ALMACEN 
    (
     id_almacen INTEGER NOT NULL , 
     nombre_almacen VARCHAR (50) NOT NULL , 
     ubicacion VARCHAR (100) NOT NULL 
    )
GO

ALTER TABLE ALMACEN ADD CONSTRAINT ALMACEN_PK PRIMARY KEY CLUSTERED (id_almacen)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE CATEGORIA 
    (
     id_categoria INTEGER NOT NULL , 
     nombre VARCHAR (50) NOT NULL , 
     descripcion VARCHAR (150) 
    )
GO

ALTER TABLE CATEGORIA ADD CONSTRAINT CATEGORIA_PK PRIMARY KEY CLUSTERED (id_categoria)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE CLIENTE 
    (
     id_cliente INTEGER NOT NULL , 
     nombre VARCHAR (80) NOT NULL , 
     correo_electronico VARCHAR (80) NOT NULL , 
     telefono VARCHAR (15) NOT NULL , 
     telefono_secundario VARCHAR (15) , 
     direccion VARCHAR (150) NOT NULL 
    )
GO

ALTER TABLE CLIENTE ADD CONSTRAINT CLIENTE_PK PRIMARY KEY CLUSTERED (id_cliente)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE DETALLE_SUMINISTRO 
    (
     talla VARCHAR (10) NOT NULL , 
     color VARCHAR (30) NOT NULL , 
     cantidad INTEGER NOT NULL , 
     PRODUCTO_id_producto INTEGER NOT NULL , 
     SUMINISTRO_id_suministro INTEGER NOT NULL 
    )
GO

ALTER TABLE DETALLE_SUMINISTRO ADD CONSTRAINT DETALLE_SUMINISTRO_PK PRIMARY KEY CLUSTERED (color, PRODUCTO_id_producto, SUMINISTRO_id_suministro, talla)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE DETALLE_VENTA 
    (
     talla_elegida VARCHAR (10) NOT NULL , 
     color_elegido VARCHAR (30) NOT NULL , 
     cantidad INTEGER NOT NULL , 
     precio_unitario_aplicado NUMERIC (10,2) NOT NULL , 
     PEDIDO_id_pedido INTEGER NOT NULL , 
     PRODUCTO_id_producto INTEGER NOT NULL 
    )
GO

ALTER TABLE DETALLE_VENTA ADD CONSTRAINT DETALLE_VENTA_PK PRIMARY KEY CLUSTERED (talla_elegida, color_elegido, PEDIDO_id_pedido, PRODUCTO_id_producto)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE LOCAL 
    (
     id_local INTEGER NOT NULL , 
     nombre_local VARCHAR (50) NOT NULL , 
     direccion_local VARCHAR (150) NOT NULL 
    )
GO

ALTER TABLE LOCAL ADD CONSTRAINT LOCAL_PK PRIMARY KEY CLUSTERED (id_local)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE PEDIDO 
    (
     id_pedido INTEGER NOT NULL , 
     fecha DATE NOT NULL , 
     metodo_pago VARCHAR (30) NOT NULL , 
     SUMINISTRO_id_suministro INTEGER NOT NULL , 
     CLIENTE_id_cliente INTEGER NOT NULL 
    )
GO

ALTER TABLE PEDIDO ADD CONSTRAINT PEDIDO_PK PRIMARY KEY CLUSTERED (id_pedido)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE PRODUCTO 
    (
     id_producto INTEGER NOT NULL , 
     nombre VARCHAR (80) NOT NULL , 
     especificaciones VARCHAR (150) , 
     precio_unitario_base NUMERIC (10,2) NOT NULL , 
     estado VARCHAR (20) NOT NULL , 
     CATEGORIA_id_categoria INTEGER NOT NULL 
    )
GO

ALTER TABLE PRODUCTO ADD CONSTRAINT PRODUCTO_PK PRIMARY KEY CLUSTERED (id_producto)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE STOCK_ALMACEN 
    (
     talla VARCHAR (10) NOT NULL , 
     color VARCHAR (30) NOT NULL , 
     stock_actual INTEGER NOT NULL , 
     stock_minimo INTEGER NOT NULL , 
     PRODUCTO_id_producto INTEGER NOT NULL , 
     ALMACEN_id_almacen INTEGER NOT NULL 
    )
GO

ALTER TABLE STOCK_ALMACEN ADD CONSTRAINT STOCK_ALMACEN_PK PRIMARY KEY CLUSTERED (talla, color, PRODUCTO_id_producto, ALMACEN_id_almacen)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE SUMINISTRO 
    (
     id_suministro INTEGER NOT NULL , 
     fecha_suministro DATE NOT NULL , 
     estado_despacho VARCHAR (20) NOT NULL , 
     ALMACEN_id_almacen INTEGER NOT NULL , 
     LOCAL_id_local INTEGER NOT NULL 
    )
GO

ALTER TABLE SUMINISTRO ADD CONSTRAINT SUMINISTRO_PK PRIMARY KEY CLUSTERED (id_suministro)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

ALTER TABLE DETALLE_SUMINISTRO 
    ADD CONSTRAINT DETALLE_SUMINISTRO_PRODUCTO_FK FOREIGN KEY 
    ( 
     PRODUCTO_id_producto
    ) 
    REFERENCES PRODUCTO 
    ( 
     id_producto 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE DETALLE_SUMINISTRO 
    ADD CONSTRAINT DETALLE_SUMINISTRO_SUMINISTRO_FK FOREIGN KEY 
    ( 
     SUMINISTRO_id_suministro
    ) 
    REFERENCES SUMINISTRO 
    ( 
     id_suministro 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE DETALLE_VENTA 
    ADD CONSTRAINT DETALLE_VENTA_PEDIDO_FK FOREIGN KEY 
    ( 
     PEDIDO_id_pedido
    ) 
    REFERENCES PEDIDO 
    ( 
     id_pedido 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE DETALLE_VENTA 
    ADD CONSTRAINT DETALLE_VENTA_PRODUCTO_FK FOREIGN KEY 
    ( 
     PRODUCTO_id_producto
    ) 
    REFERENCES PRODUCTO 
    ( 
     id_producto 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE PEDIDO 
    ADD CONSTRAINT PEDIDO_CLIENTE_FK FOREIGN KEY 
    ( 
     CLIENTE_id_cliente
    ) 
    REFERENCES CLIENTE 
    ( 
     id_cliente 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE PEDIDO 
    ADD CONSTRAINT PEDIDO_SUMINISTRO_FK FOREIGN KEY 
    ( 
     SUMINISTRO_id_suministro
    ) 
    REFERENCES SUMINISTRO 
    ( 
     id_suministro 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE PRODUCTO 
    ADD CONSTRAINT PRODUCTO_CATEGORIA_FK FOREIGN KEY 
    ( 
     CATEGORIA_id_categoria
    ) 
    REFERENCES CATEGORIA 
    ( 
     id_categoria 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE STOCK_ALMACEN 
    ADD CONSTRAINT STOCK_ALMACEN_ALMACEN_FK FOREIGN KEY 
    ( 
     ALMACEN_id_almacen
    ) 
    REFERENCES ALMACEN 
    ( 
     id_almacen 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE STOCK_ALMACEN 
    ADD CONSTRAINT STOCK_ALMACEN_PRODUCTO_FK FOREIGN KEY 
    ( 
     PRODUCTO_id_producto
    ) 
    REFERENCES PRODUCTO 
    ( 
     id_producto 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE SUMINISTRO 
    ADD CONSTRAINT SUMINISTRO_ALMACEN_FK FOREIGN KEY 
    ( 
     ALMACEN_id_almacen
    ) 
    REFERENCES ALMACEN 
    ( 
     id_almacen 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO

ALTER TABLE SUMINISTRO 
    ADD CONSTRAINT SUMINISTRO_LOCAL_FK FOREIGN KEY 
    ( 
     LOCAL_id_local
    ) 
    REFERENCES LOCAL 
    ( 
     id_local 
    ) 
    ON DELETE NO ACTION 
    ON UPDATE NO ACTION 
GO



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            10
-- CREATE INDEX                             0
-- ALTER TABLE                             21
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE DATABASE                          0
-- CREATE DEFAULT                           0
-- CREATE INDEX ON VIEW                     0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE ROLE                              0
-- CREATE RULE                              0
-- CREATE SCHEMA                            0
-- CREATE SEQUENCE                          0
-- CREATE PARTITION FUNCTION                0
-- CREATE PARTITION SCHEME                  0
-- 
-- DROP DATABASE                            0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
