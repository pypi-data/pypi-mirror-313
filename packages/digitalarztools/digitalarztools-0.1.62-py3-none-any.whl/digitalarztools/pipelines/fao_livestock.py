
"""
https://data.apps.fao.org/catalog/dataset/47457ad7-ed00-4346-81e2-85aacd0e6d91/resource/8a4c8a18-22c7-448f-b0af-ec63b9f58455
https://www.livestockdata.org/contributor/gridded-livestock-world-glw3
"""
import os.path

from owslib.wms import WebMapService

from digitalarztools.io.raster.rio_raster import RioRaster


class WebMapServices:
    pass


class GWL3:
    @staticmethod
    def download_grid( bbox_4326,  output_fp:str) -> RioRaster:
        """
        download 10 km grided  livestock data from GWL3  of FAO
        :param bbox_4326:
        :param output_fp:
        """
        if not os.path.exists(output_fp):
            wms_url = "https://io.apps.fao.org/gismgr/api/v1/GLW3/D_DA/2/wms?request=GetCapabilities&service=WMS&version=1.3.0"
            wms = WebMapService(wms_url,version='1.3.0')
            contents = list(wms.contents)
            ### content s D_DA and 10 KM grided data
            width = int((bbox_4326[2] - bbox_4326[0]) * 110 * 1000 / 10000)
            height = int((bbox_4326[3] - bbox_4326[1]) * 110 * 1000 / 10000)
            size = [width, height]
            print("downloading livestock data...")
            img = wms.getmap(layers=contents,srs='EPSG:4326',bbox=bbox_4326, size=size,format='image/geotiff')
            out = open(output_fp, 'wb')
            out.write(img.read())
            out.close()
            print("file downloaded at ", output_fp)
        return RioRaster(output_fp)
