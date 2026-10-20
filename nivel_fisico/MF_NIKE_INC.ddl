-- Generado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   en:        2026-10-15 09:51:59 PET
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
     nombre VARCHAR (100) NOT NULL , 
     correo_e VARCHAR (100) NOT NULL , 
     telefono VARCHAR (9) NOT NULL , 
     direccion VARCHAR (200) NOT NULL 
    )
GO

ALTER TABLE CLIENTE ADD CONSTRAINT CLIENTE_PK PRIMARY KEY CLUSTERED (id_cliente)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE DETALLE_VENTA 
    (
     id_detalle INTEGER NOT NULL , 
     talla_elegida VARCHAR (15) NOT NULL , 
     cantidad INTEGER NOT NULL , 
     precio_unitario_aplicado DECIMAL (10,2) NOT NULL , 
     total DECIMAL (10,2) NOT NULL , 
     PEDIDO_id_pedido INTEGER NOT NULL , 
     PRODUCTO_id_producto INTEGER NOT NULL 
    )
GO

ALTER TABLE DETALLE_VENTA ADD CONSTRAINT DETALLE_VENTA_PK PRIMARY KEY CLUSTERED (id_detalle)
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
     fecha DATETIME NOT NULL , 
     metodo_pago VARCHAR (40) NOT NULL , 
     igv DECIMAL (10,2) NOT NULL , 
     estado_envio VARCHAR (30) NOT NULL , 
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
     nombre VARCHAR (120) NOT NULL , 
     especificaciones VARCHAR (255) , 
     precio_unitario_base DECIMAL (10,2) NOT NULL , 
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
     talla VARCHAR (15) NOT NULL , 
     color VARCHAR (40) NOT NULL , 
     stock_actual INTEGER NOT NULL , 
     stock_minimo INTEGER NOT NULL , 
     ALMACEN_id_almacen INTEGER NOT NULL , 
     PRODUCTO_id_producto INTEGER NOT NULL 
    )
GO

ALTER TABLE STOCK_ALMACEN ADD CONSTRAINT STOCK_ALMACEN_PK PRIMARY KEY CLUSTERED (talla, color, ALMACEN_id_almacen, PRODUCTO_id_producto)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
GO

CREATE TABLE SUMINISTRO_LOCAL 
    (
     fecha_suministro DATE NOT NULL , 
     estado_despacho VARCHAR (30) , 
     LOCAL_id_local INTEGER NOT NULL , 
     ALMACEN_id_almacen INTEGER NOT NULL 
    )
GO

ALTER TABLE SUMINISTRO_LOCAL ADD CONSTRAINT SUMINISTRO_LOCAL_PK PRIMARY KEY CLUSTERED (fecha_suministro, ALMACEN_id_almacen, LOCAL_id_local)
     WITH (
     ALLOW_PAGE_LOCKS = ON , 
     ALLOW_ROW_LOCKS = ON )
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

ALTER TABLE SUMINISTRO_LOCAL 
    ADD CONSTRAINT SUMINISTRO_LOCAL_ALMACEN_FK FOREIGN KEY 
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

ALTER TABLE SUMINISTRO_LOCAL 
    ADD CONSTRAINT SUMINISTRO_LOCAL_LOCAL_FK FOREIGN KEY 
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
-- CREATE TABLE                             9
-- CREATE INDEX                             0
-- ALTER TABLE                             17
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
