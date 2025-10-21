create procedure loadData as
begin


bulk insert AIRLINES
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\airlines.dat'
WITH ( 
DATAFILETYPE = 'char',
FIELDTERMINATOR = ',',
ROWTERMINATOR = '0x0A',
FIRSTROW = 2,
KEEPNULLS
);

bulk insert AIRPORT
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\L_AIRLINE_ID.csv'
WITH ( 
DATAFILETYPE = 'char',
FIELDTERMINATOR = ',',
ROWTERMINATOR = '0x0A',
FIRSTROW = 2,
KEEPNULLS
);

bulk insert AIRPORTS
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\airports.dat'
WITH ( 
DATAFILETYPE = 'char',
FIELDTERMINATOR = ',',
ROWTERMINATOR = '0x0A',
FIRSTROW = 2,
KEEPNULLS
);

bulk insert CITYMARKETID
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\L_CITY_MARKET_ID.csv'
WITH ( 
DATAFILETYPE = 'char',
FIELDTERMINATOR = ',',
ROWTERMINATOR = '0x0A',
FIRSTROW = 2,
KEEPNULLS
);


bulk insert DISTANCEGROUP250
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\L_DISTANCE_GROUP_250.csv'
WITH ( 
DATAFILETYPE = 'char',
FIELDTERMINATOR = ',',
ROWTERMINATOR = '0x0A',
FIRSTROW = 2,
KEEPNULLS
);

bulk insert FACTFLIGHT
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\574784350_T_ONTIME_REPORTING.csv'
WITH ( 
    DATAFILETYPE = 'char',
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '0x0A',
    FIRSTROW = 2,
    KEEPNULLS
);

bulk insert ONTIMEDELAYGROUPS
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\L_ONTIME_DELAY_GROUPS.csv'
WITH ( 
DATAFILETYPE = 'char',
FIELDTERMINATOR = ',',
ROWTERMINATOR = '0x0A',
FIRSTROW = 2,
KEEPNULLS
);


bulk insert UNIQUECARRIERS
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\L_UNIQUE_CARRIERS.csv'
WITH ( 
DATAFILETYPE = 'char',
FIELDTERMINATOR = ',',
ROWTERMINATOR = '0x0A',
FIRSTROW = 2,
KEEPNULLS
);

bulk insert WORLDAREACODES
from 'C:\Users\josue\OneDrive\Documentos\J4P0N\Airport-Warehouse\Dane\L_WORLD_AREA_CODES.csv'
WITH ( 
DATAFILETYPE = 'char',
FIELDTERMINATOR = ',',
ROWTERMINATOR = '0x0A',
FIRSTROW = 2,
KEEPNULLS
);

end
