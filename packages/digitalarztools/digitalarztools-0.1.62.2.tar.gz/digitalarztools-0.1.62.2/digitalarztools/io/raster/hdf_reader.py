import os.path
import traceback

import numpy as np
import pandas as pd
import pyproj
from pyhdf.SD import SD, SDC
from pyproj import CRS

from digitalarztools.io.raster.gdal_raster_io import GDALRasterIO


def metadata_reader(fmd: dict, ln_list: list, pre_var: str = None, pre_val: str = None):
    def get_info():
        d_list = []
        while len(d_list) != 2 and len(ln_list) > 0:
            data = ln_list.pop(0)
            d_list = data.split("=")
        if len(d_list) >= 2:
            var = d_list[0].strip().lower() or ""
            val = d_list[1].strip().lower() or ""
            if val.startswith('"'):
                val = val[1:]
            if val.endswith('"'):
                val = val[:-1]
        else:
            var = ""
            val = ""
        # print(var, val)
        return var, val

    var, val = get_info()
    # print("len", len(ln_list))
    if len(ln_list) == 0 or var == "END":
        return
    elif var == 'object'.lower():
        var1 = ""
        while var1 != "value" and len(ln_list) > 0:
            var1, val1 = get_info()
        fmd[val] = val1
        metadata_reader(fmd, ln_list, pre_var, pre_val)
    elif var == 'group':
        fmd[val] = {}
        if val.find('structure') != -1:
            var1, val1 = get_info()
            cur_dict = fmd[val]
            prv_dir = []
            prv_dir.append(fmd[val])
            while var1 != 'end_group' or val1 != val:
                if var1 in ['group', 'object']:
                    cur_dict[val1] = {}
                    prv_dir.append(cur_dict)
                    cur_dict = cur_dict[val1]
                elif var1 in ['end_group', 'end_object']:
                    cur_dict = prv_dir.pop()
                else:
                    cur_dict[var1] = val1
                var1, val1 = get_info()
                # print(var1, val1, val)

        metadata_reader(fmd[val], ln_list, var, val)
    else:
        metadata_reader(fmd, ln_list, pre_var, pre_val)


class HDFReader:
    hdf: SD
    metadata: dict

    def __init__(self, file_name: str):
        self.hdf = SD(file_name, SDC.READ)
        self.set_metadata()
        # self.metadata['custom']['crs'] = pyproj.CRS.from_epsg(4326)
        self.metadata['custom']['filename'] = os.path.basename(file_name)
        self.metadata['custom']['filepath'] = os.path.dirname(file_name)
        # print(self.metadata)

    def set_metadata(self):
        self.metadata = {}
        attr = self.hdf.attributes()
        metadata_types = ['StructMetadata', 'CoreMetadata', 'ArchiveMetadata']  # ,
        for t in metadata_types:
            ln_list = attr[f'{t}.0'].split('\n')
            ln_list.pop()
            self.metadata[t.lower()] = {}
            metadata_reader(self.metadata[t.lower()], ln_list, t.upper())
        self.metadata['custom'] = {}
        # print("meta data", self.metadata)

    def get_metadata(self):
        return self.metadata

    def find_metadata_key_data(self, md: dict, key: str):
        if key in md.keys():
            return md[key]
        for k in md.keys():
            if isinstance(md[k], dict):
                res = self.find_metadata_key_data(md[k], key)
                if res is not None:
                    return res

    def get_image_res(self):
        # bounding_rect = self.metadata['archivedmetadata']['boundingrectangle']
        # rows = int(bounding_rect['datarows'])
        # cols = int(bounding_rect['datacolumns'])
        row_keys = ['datarows', 'ydim']
        col_keys = ['datacolumns', 'xdim']
        rows, cols = None, None
        for key in row_keys:
            rows = self.find_metadata_key_data(self.metadata, key)
            if rows is not None:
                if isinstance(rows, str):
                    rows = int(rows)
                break
        for key in col_keys:
            cols = self.find_metadata_key_data(self.metadata, key)
            if cols is not None:
                if isinstance(cols, str):
                    cols = int(cols)

        return rows, cols

    # def get_envelop(self):
    #     if 'envelop' not in self.metadata['custom'].keys():
    #         extent = self.get_extent()
    #         self.metadata['custom']['envelop'] = box(extent[0], extent[1], extent[2], extent[3])
    #     return self.metadata['extent']['envelop']

    def get_extent(self) -> tuple:
        # bounding_rect = self.metadata['archivedmetadata']['boundingrectangle']
        bounding_rect = self.find_metadata_key_data(self.metadata, 'boundingrectangle')
        if bounding_rect:
            min_x = float(bounding_rect['westboundingcoordinate'])
            max_x = float(bounding_rect['eastboundingcoordinate'])
            min_y = float(bounding_rect['southboundingcoordinate'])
            max_y = float(bounding_rect['northboundingcoordinate'])
        else:
            h = self.find_metadata_key_data(self.metadata, 'horizontaltilenumber')
            v = self.find_metadata_key_data(self.metadata, 'verticaltilenumber')
            min_x, min_y, max_x, max_y = self.get_extent_from_h_v(h, v)
        self.metadata['custom']['crs'] = CRS.from_epsg(4326)
        return float(min_x), float(min_y), float(max_x), float(max_y)

    def get_crs(self) -> pyproj.CRS:
        return self.metadata['custom'].get('crs', None)

    def calculate_affine(self):
        rows, cols = self.get_image_res()
        extent = self.get_extent()
        A = np.array([
            [0, rows, 1, 0, 0, 0], [0, 0, 0, 0, rows, 1],
            [cols, rows, 1, 0, 0, 0], [0, 0, 0, cols, rows, 1],
            [cols, 0, 1, 0, 0, 0], [0, 0, 0, cols, 0, 1],
            [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1]
        ])
        A_t = A.transpose()
        b = np.array([
            [extent[0]], [extent[1]],
            [extent[2]], [extent[1]],
            [extent[2]], [extent[3]],
            [extent[0]], [extent[3]]
        ])
        # affine = inv(A_t*A) * A_t * b
        s0 = np.matmul(A_t, A)
        s1 = np.linalg.inv(s0)
        s2 = np.matmul(s1, A_t)
        affine = np.matmul(s2, b)
        # affine [a, b, c,d, e, f]
        return affine.reshape(-1)

    def get_geo_transform(self):
        if 'geo_transform' not in self.metadata['custom'].keys():
            self.metadata['custom']['geo_transform'] = self.calculate_affine()
        return self.metadata['custom']['geo_transform']

    def get_dataset_names(self) -> list:
        datasets = self.hdf.datasets()
        # return [k.replace(" ", "_") for k in datasets.keys()]
        return list(datasets.keys())

    def get_data(self, dataset_name) -> np.array:
        data = self.hdf.select(dataset_name).get()
        return data

    def get_tiff_path(self):
        if not 'tiff_path' in self.metadata['custom'].keys():
            tiff_path = os.path.join(self.metadata['custom']['filepath'], self.metadata['custom']['filename'][:-4])
            self.metadata['custom']['tiff_path'] = tiff_path
            if not os.path.exists(tiff_path):
                os.makedirs(tiff_path)
        return self.metadata['custom']['tiff_path']

    def to_gdal_dataset(self, ds_name):
        try:
            data = self.get_data(ds_name)
            bands, *_ = data.shape
            ds = GDALRasterIO.from_numpy(
                data, geo_transform=self.get_geo_transform(),
                proj_crs=self.get_crs())
            return ds
        except Exception as e:
            traceback.print_exc()

    def to_geotiff(self, ds_name):
        tiff_path = self.get_tiff_path()
        data = self.get_data(ds_name)
        fp = f'{tiff_path}/{ds_name}.tif'
        if os.path.isfile(fp) and os.path.exists(fp):
            os.remove(fp)
        GDALRasterIO.write_geotiff(fp, data,
                                   geo_transform=self.get_geo_transform(),
                                   proj_crs=self.get_crs())

    def to_geotiff_all(self):
        datasets = self.get_dataset_names()
        for d_name in datasets:
            self.to_geotiff(d_name)

    def get_extent_from_h_v(self, h, v):
        cur_dir = os.path.dirname(os.path.abspath(__file__))

        df = pd.read_fwf(os.path.join(cur_dir, 'config/modis_bound_10deg.txt'), sep='\t')
        #  lon_min    lon_max   lat_min   lat_max
        df = df[(df.ih == str(int(h))) & (df.iv == str(int(v)))]
        if not df.empty:
            return (df.get('lon_min').values[0], df.get('lat_min').values[0],
                    df.get('lon_max').values[0], df.get('lat_max').values[0])

        return None
