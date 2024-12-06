import glob
import os
import threading
from typing import Union

from digitalarztools.io.datasets.rio_landsat import RioLandsat
from digitalarztools.io.file_io import FileIO
from digitalarztools.pipelines.earth_explorer.m2m import EarthExplorerM2M
from digitalarztools.io.vector.gpd_vector import GPDVector


class LandSatEE:
    """
    usage:
    ls_ee = LandSatEE('landsat_ot_c2_l2')
    ls_ee.search_ls(extent, start_date_str, end_date_str)
    ls_ee.download_ls(input_folder_LS_RAW)

    # IDs of GeoTIFF data product for each dataset
    DATA_PRODUCTS = {
        "landsat_tm_c1": "5e83d08fd9932768",
        "landsat_etm_c1": "5e83a507d6aaa3db",
        "landsat_8_c1": "5e83d0b84df8d8c2",
        "landsat_tm_c2_l1": "5e83d0a0f94d7d8d",
        "landsat_etm_c2_l1": "5e83d0d0d2aaa488",
        "landsat_ot_c2_l1": "5e81f14ff4f9941c",
        "landsat_tm_c2_l2": "5e83d11933473426",
        "landsat_etm_c2_l2": "5e83d12aada2e3c5",
        "landsat_ot_c2_l2": "5e83d14f30ea90a9",
        "sentinel_2a": "5e83a42c6eba8084",
    }
    """
    search_res_gdv: GPDVector
    dataset_name: str
    des_path: str

    def __init__(self, dataset_name, des_path):
        """
        use following code to store password
         >>> from digitalarztools.pipelines.config.data_centers import DataCenters
         >>> DataCenters().set_up_account("EARTHEXPLORER")

        search for dataset from landsat_tm_c1, landsat_tm_c2_l1, landsat_tm_c2_l2, landsat_etm_c1,
        landsat_etm_c2_l1, landsat_etm_c2_l2, landsat_8_c1, landsat_ot_c2_l1, landsat_ot_c2_l2, sentinel_2a

        :param dataset_name:  Case-insensitive dataset alias default value is landsat_ot_c2_l1
        :param des_path: path for storing downloaded data
        """
        self.dataset_name = dataset_name
        self.des_path = des_path

    def search_ls(self, region: Union[list, GPDVector], start_date, end_date, search_res_xlsx,
                  max_cloud_cover=10) -> int:
        """
            :param extent: tuple of  form (xmin, ymin, xmax, ymax)
            :param start_date: str, YYYY-MM-DD like '1995-01-01',
            :param end_date: str YYYY-MM-DD like '1995-10-01',
            :param max_cloud_cover: percentage default value is 10
            :return: number of rows
        """
        # username, password = DataCenters().get_server_account("EARTHEXPLORER")
        # api = API(username=username, password=password)
        # scenes = api.search(
        #     dataset=self.dataset_name,
        #     bbox=extent,
        #     start_date=start_date,
        #     end_date=end_date,
        #     max_cloud_cover=max_cloud_cover
        # )
        # api.logout()
        # df = pd.DataFrame(scenes)
        # df = df.sort_values(['acquisition_date', 'cloud_cover'])
        # search_res = os.path.join(self.des_path, f'search_result_{end_date.replace("-", "")}.xlsx')
        if not os.path.exists(search_res_xlsx):
            extent = region.total_bounds if isinstance(region, GPDVector) else region
            gdf = EarthExplorerM2M.search_scenes(self.dataset_name, start_date, end_date, extent)
            self.search_res_gdv = GPDVector(gdf)
            self.search_res_gdv.to_datetime(col_name='publishDate', format='%Y-%m-%d')
            self.search_res_gdv.remove_duplicates(['displayId'])
            # remove duplicate row-path data
            # self.search_res_gdv.remove_duplicate_geometry(sort_by=['publishDate', 'cloudCover'], ascending=[False, True])
            self.search_res_gdv.to_datetime(col_name='publishDate', format='%Y-%m-%d')
            self.search_res_gdv["row_path"] = self.search_res_gdv["displayId"].apply(
                lambda name: RioLandsat.get_row_path(name))
            self.search_res_gdv["sensor"] = self.search_res_gdv["displayId"].apply(
                lambda name: RioLandsat.get_sensor_no(name))
            self.search_res_gdv[['sensor', 'row_path', 'publishDate']].sort_values(
                ['row_path', 'publishDate', 'sensor'],
                ascending=[True, False, False])
            self.search_res_gdv.remove_duplicates(['row_path'])
            if isinstance(region, GPDVector):
                # polygon = region.unary_union
                self.search_res_gdv.spatial_operation(region)
                # print(region.head())
            no_of_items = self.search_res_gdv.shape[0]
            print(f"Found {no_of_items} items")
            if no_of_items > 0:
                self.search_res_gdv.to_excel(des=search_res_xlsx)
        else:
            self.search_res_gdv = GPDVector.from_excel(search_res_xlsx)

        return self.search_res_gdv.shape[0]

    def extract_data(self):
        os.chdir(self.des_path)
        # datasets = [n for n in glob.glob("*.tar")]
        for n in glob.glob("*.tar"):
            fp = os.path.join(self.des_path, n)
            # FileIO.extract_data(fp)
            RioLandsat(fp)

    def download_ls(self, create_thread=True):
        m2m = EarthExplorerM2M(self.des_path)
        os.chdir(self.des_path)
        downloaded_entity_ids = [n.split(".")[0] for n in glob.glob("*.tar")]
        res_df = self.search_res_gdv[['entityId']][~self.search_res_gdv.displayId.isin(downloaded_entity_ids)]
        req_entity_ids = res_df['entityId'].values.tolist()

        if len(req_entity_ids) > 0:
            if create_thread:
                x = threading.Thread(target=m2m.download_datasets, args=(self.dataset_name, req_entity_ids))
                x.start()
            else:
                m2m.download_datasets(self.dataset_name, req_entity_ids)

    def set_search_res(self, gdv: GPDVector):
        self.search_res_gdv = gdv
