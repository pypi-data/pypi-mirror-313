# DigitalArz Tools
Tools for providing GIS capabilities in the DigitalArz Application. Tools are based on

1. RasterIO
2. GeoPandas
3. Shapely
4. Scikit-learn

Modules are

## Raster

1. rio_raster: to extract raster information and read and write operation using raster io
2. rio_process: to perform different process on a raster
3. rio_extraction : to extract data from different pipelines like GEE
4. indices

## Vector

1. gpd_vector: to extract vector and perform operation using geopandas

## Pipeline

To add the account in the digitalarztool module, you have to open the python console. 
Activate the venv environment and  open python in this environment. In console use following commands
```angular2html
from digitalarztools.pipelines.config.server_settings import ServerSetting
ServerSetting().set_up_account("NASA")
```
Following piplines are available

1. gee: pipeline with google earth engine for processing and extracting data
2. srtm: pipeline to extract SRTM data from
3. nasa: pipeline to extract NASA data. First need to setup account using
    ```
   SeverSetting.set_up_account("NASA")
   ```
   alos palsar: to extract alos palsar RTC data using earthsat api

4. grace & gldas: to extract grace and gldas data using ggtools(https://pypi.org/project/ggtools/). Grace data is
   available at https://podaac.jpl.nasa.gov/dataset/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06_V2
5. ClimateServ Date: https://pypi.org/project/climateserv/ 
6. CHIRP: download Rainfall data.