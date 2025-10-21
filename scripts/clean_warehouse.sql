/* ==========================================================================
   SCRIPT COMPLETO Y CORREGIDO PARA: clean_warehouse.sql
   ==========================================================================
   
   Correcciones:
   1. Se eliminaron los 'go' para que sea un procedimiento válido.
   2. Se reemplazó 'sp_MSforeachtable' por el comando correcto:
      'TRUNCATE TABLE dbo.FactFlight', ya que solo queremos 
      limpiar la tabla de hechos, no las dimensiones.
*/

-- Asegúrate de estar en la base de datos 'hd'
USE hd;
GO

-- 1. Borramos el procedimiento viejo (si es que se creó con error)
DROP PROCEDURE IF EXISTS clean_warehouse;
GO

-- 2. Creamos el procedimiento nuevo y completo
CREATE PROCEDURE clean_warehouse AS
BEGIN
    SET NOCOUNT ON;

    -- ----------------------------------------------------
    -- ETAPA 1: Quitar las llaves foráneas de FactFlight
    -- ----------------------------------------------------
    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_ACTUALARR_DIMTIME')
    alter table FactFlight drop constraint FK_FACTFLIG_ACTUALARR_DIMTIME;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_ACTUALDEP_DIMTIME')
    alter table FactFlight drop constraint FK_FACTFLIG_ACTUALDEP_DIMTIME;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_AIRLINE_DIMAIRLI')
    alter table FactFlight drop constraint FK_FACTFLIG_AIRLINE_DIMAIRLI;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_ARRIVALDE_DIMDELAY')
    alter table FactFlight drop constraint FK_FACTFLIG_ARRIVALDE_DIMDELAY;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_ARRIVALTI_DIMTIME')
    alter table FactFlight drop constraint FK_FACTFLIG_ARRIVALTI_DIMTIME;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_DEPARTURE_DIMDELAY')
    alter table FactFlight drop constraint FK_FACTFLIG_DEPARTURE_DIMDELAY;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_DEPARTURE_DIMTIME')
    alter table FactFlight drop constraint FK_FACTFLIG_DEPARTURE_DIMTIME;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_DESTINATI_DIMAIRPO')
    alter table FactFlight drop constraint FK_FACTFLIG_DESTINATI_DIMAIRPO;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_DISTANCEG_DIMDISTA')
    alter table FactFlight drop constraint FK_FACTFLIG_DISTANCEG_DIMDISTA;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_FLIGHTDAT_DIMDATE')
    alter table FactFlight drop constraint FK_FACTFLIG_FLIGHTDAT_DIMDATE;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_ORIGINAIR_DIMAIRPO')
    alter table FactFlight drop constraint FK_FACTFLIG_ORIGINAIR_DIMAIRPO;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_WHEELSOFF_DIMTIME')
    alter table FactFlight drop constraint FK_FACTFLIG_WHEELSOFF_DIMTIME;

    if exists (select 1 from sys.sysreferences r join sys.sysobjects o on (o.id = r.constid and o.type = 'F') where r.fkeyid = object_id('FactFlight') and o.name = 'FK_FACTFLIG_WHEELSON_DIMTIME')
    alter table FactFlight drop constraint FK_FACTFLIG_WHEELSON_DIMTIME;

    
    -- ----------------------------------------------------
    -- ETAPA 2: Truncar SÓLO la tabla de hechos
    -- ----------------------------------------------------
    TRUNCATE TABLE dbo.FactFlight;


    -- ----------------------------------------------------
    -- ETAPA 3: Volver a agregar las llaves foráneas
    -- ----------------------------------------------------
    alter table FactFlight
    add constraint FK_FACTFLIG_ACTUALARR_DIMTIME foreign key (ActualArrivalTimeID)
        references DimTime (TimeID);

    alter table FactFlight
    add constraint FK_FACTFLIG_ACTUALDEP_DIMTIME foreign key (ActualDepartureTimeID)
        references DimTime (TimeID);

    alter table FactFlight
    add constraint FK_FACTFLIG_AIRLINE_DIMAIRLI foreign key (AirlineID)
        references DimAirline (AirlineID);

    alter table FactFlight
    add constraint FK_FACTFLIG_ARRIVALDE_DIMDELAY foreign key (ArrivalDelayGroupsID)
        references DimDelayGroups (DelayGroupsID);

    alter table FactFlight
    add constraint FK_FACTFLIG_ARRIVALTI_DIMTIME foreign key (ArrivalTimeID)
        references DimTime (TimeID);

    alter table FactFlight
    add constraint FK_FACTFLIG_DEPARTURE_DIMDELAY foreign key (DepartureDelayGroupsID)
        references DimDelayGroups (DelayGroupsID);

    alter table FactFlight
    add constraint FK_FACTFLIG_DEPARTURE_DIMTIME foreign key (WheelsOnID)
        references DimTime (TimeID);

    alter table FactFlight
    add constraint FK_FACTFLIG_DESTINATI_DIMAIRPO foreign key (OriginAirportID)
        references DimAirport (AirportID);

    alter table FactFlight
    add constraint FK_FACTFLIG_DISTANCEG_DIMDISTA foreign key (DistanceRangeID)
        references DimDistanceRange (DistanceRangeID);

    alter table FactFlight
    add constraint FK_FACTFLIG_FLIGHTDAT_DIMDATE foreign key (FlightDateID)
        references DimDate (DateID);

    alter table FactFlight
    add constraint FK_FACTFLIG_ORIGINAIR_DIMAIRPO foreign key (DestinationAirportID)
        references DimAirport (AirportID);

    alter table FactFlight
    add constraint FK_FACTFLIG_WHEELSOFF_DIMTIME foreign key (DepartureTimeID)
        references DimTime (TimeID);

    alter table FactFlight
    add constraint FK_FACTFLIG_WHEELSON_DIMTIME foreign key (WheelsOffID)
        references DimTime (TimeID);

END
GO