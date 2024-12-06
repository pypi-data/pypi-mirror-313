# =============================================================================
#  USGS/EROS Inventory Service Example
#  Description: Download Landsat Collection 2 files
#  Usage: python download_sample.py -u username -p password -f filetype
#         optional argument f refers to filetype including 'bundle' or 'band'
#  Machine-to-Machine (M2M) Api Script
# =============================================================================

import os

import geopandas as gpd
import requests
import time
import re
import threading

from datetime import datetime

from shapely.geometry import shape

from digitalarztools.io.file_io import FileIO
from digitalarztools.pipelines.config.data_centers import DataCenters
from digitalarztools.utils.logger import da_logger


class EarthExplorerM2M:
    """
     USGS Machine to Machine (M2M) API...
     JSON-based REST API used to interact with USGS/EROS data inventories.
    """
    def __init__(self, des_dir, max_threads=3):
        self.path = des_dir  # Fill a valid download path
        self.maxthreads = max_threads  # Threads count for downloads
        self.sema = threading.Semaphore(value=self.maxthreads)
        self.label = datetime.now().strftime("%Y%m%d_%H%M%S")  # Customized label using date time
        self.threads = []

    @classmethod
    def login_m2m(cls):
        username, password = DataCenters().get_server_account("EARTHEXPLORER")
        # Login
        payload = {'username': username, 'password': password}
        apiKey = cls.sendRequest(cls.get_service_url("login"), payload)

        if not apiKey:
            da_logger.error("Failed to login ")
        else:
            da_logger.info("Temp API Key found")
            return apiKey

    @classmethod
    def logout_m2m(cls, apiKey):
        if not cls.sendRequest(cls.get_service_url("logout"), None, apiKey):
            da_logger.info("Logged Out\n")
        else:
            da_logger.error("Logout Failed\n")

    # @staticmethod
    # def sendRequest(url, data, apiKey=None, exitIfNoResponse=True):
    #     # Send http request
    #             json_data = json.dumps(data)
    #
    #     if not apiKey:
    #         response = requests.post(url, json_data)
    #     else:
    #         headers = {'X-Auth-Token': apiKey}
    #         response = requests.post(url, json_data, headers=headers)
    #
    #     try:
    #         httpStatusCode = response.status_code
    #         if response == None:
    #             da_logger.error("No output from service")
    #             # if exitIfNoResponse:
    #             #     sys.exit()
    #             # else:
    #             #     return False
    #         output = json.loads(response.text)
    #         if output['errorCode'] != None:
    #             da_logger.error(output['errorCode'], "- ", output['errorMessage'])
    #             if exitIfNoResponse:
    #                 sys.exit()
    #             else:
    #                 return False
    #         if httpStatusCode == 404:
    #             da_logger.error("404 Not Found")
    #             if exitIfNoResponse:
    #                 sys.exit()
    #             else:
    #                 return False
    #         elif httpStatusCode == 401:
    #             da_logger.error("401 Unauthorized")
    #             if exitIfNoResponse:
    #                 sys.exit()
    #             else:
    #                 return False
    #         elif httpStatusCode == 400:
    #             da_logger.error("Error Code", httpStatusCode)
    #             if exitIfNoResponse:
    #                 sys.exit()
    #             else:
    #                 return False
    #     except Exception as e:
    #         response.close()
    #         da_logger.error(str(e))
    #         if exitIfNoResponse:
    #             sys.exit()
    #         else:
    #             return False
    #     response.close()
    #
    #     return output['data']

    def downloadFile(self, url):
        self.sema.acquire()
        try:
            response = requests.get(url, stream=True)
            disposition = response.headers['content-disposition']
            filename = re.findall("filename=(.+)", disposition)[0].strip("\"")
            da_logger.info(f"Downloading {filename} ...\n")
            # if self.path[-1] != "/":
            #     filename = "/" + filename
            filepath = os.path.join(self.path, filename)
            open(filepath, 'wb').write(response.content)
            da_logger.critical(f"Downloaded {filename}\n")
            self.sema.release()
            # FileIO.extract_data(filepath)
        except Exception as e:
            da_logger.error(f"Failed to download from {url}. Will try to re-download.")
            self.sema.release()
            self.runDownload(self.threads, url)

    def runDownload(self, threads, url):
        thread = threading.Thread(target=self.downloadFile, args=(url,))
        threads.append(thread)
        thread.start()

    @staticmethod
    def get_service_url(end_point):
        """
        :param end_point: string should have value in "login", "logout", "download-options",
        :return:
        """
        serviceUrl = "https://m2m.cr.usgs.gov/api/api/json/stable/"
        return f"{serviceUrl}{end_point}"

    @classmethod
    def search_datasets(cls, dataset_name, start_date, end_date, extent) -> dict:
        """

        :param dataset_name: get dataset name from https://earthexplorer.usgs.gov/
            possible dataset name "asas", gls_all, andsat_tm_c1, landsat_tm_c2_l1, landsat_tm_c2_l2, landsat_etm_c1,
            landsat_etm_c2_l1, landsat_etm_c2_l2, landsat_8_c1, landsat_ot_c2_l1, landsat_ot_c2_l2
        :param start_date:  str  YYYY-MM-DD format
        :param end_date: str  YYYY-MM-DD format
        :param extent:  list or tuple having [min_x,min_y,max_x,max_y]
        :return: panda dataframe of result

        payload sample:
        {
            "datasetName": "Global Land Survey",
            "spatialFilter": {
                "filterType": "mbr",
                "lowerLeft": {
                        "latitude": 44.60847,
                        "longitude": -99.69639
                },
                "upperRight": {
                        "latitude": 44.60847,
                        "longitude": -99.69639
                }
            },
            "temporalFilter": {
                "start": "2012-01-01",
                "end": "2012-12-01"
            }
        }
        """
        api_key = cls.login_m2m()
        payload = {
            "datasetName": dataset_name,
            "spatialFilter": {
                "filterType": "mbr",
                "lowerLeft": {
                    "latitude": extent[1],
                    "longitude": extent[0]
                },
                "upperRight": {
                    "latitude": extent[3],
                    "longitude": extent[2]
                }
            },
            "temporalFilter": {
                "start": start_date,
                "end": end_date
            }
        }
        res = cls.sendRequest(cls.get_service_url("dataset-search"), payload, api_key)
        cls.logout_m2m(api_key)
        return res

    @classmethod
    def search_scenes(cls, dataset_name, start_date, end_date, extent, max_cloud_cover=10) -> gpd.GeoDataFrame:
        """

        :param dataset_name: get dataset name from https://earthexplorer.usgs.gov/
            possible dataset name "asas", gls_all, andsat_tm_c1, landsat_tm_c2_l1, landsat_tm_c2_l2, landsat_etm_c1,
            landsat_etm_c2_l1, landsat_etm_c2_l2, landsat_8_c1, landsat_ot_c2_l1, landsat_ot_c2_l2
        :param start_date:  str  YYYY-MM-DD format
        :param end_date: str  YYYY-MM-DD format
        :param extent:  list or tuple having [min_x,min_y,max_x,max_y]
        :param max_cloud_cover: in percentage default is 10
        :return: panda dataframe of result
        """
        api_key = cls.login_m2m()

        payload = {
            "datasetName": dataset_name,
            "sceneFilter": {
                "spatialFilter": {
                    "filterType": "mbr",
                    "lowerLeft": {
                        "latitude": extent[1],
                        "longitude": extent[0]
                    },
                    "upperRight": {
                        "latitude": extent[3],
                        "longitude": extent[2]
                    }
                },
                "cloudCoverFilter": {
                    "max": max_cloud_cover,
                    "min": 0,
                    "includeUnknown": False
                },
                "acquisitionFilter": {
                    "start": start_date,
                    "end": end_date
                }
            }
        }
        res = cls.sendRequest(cls.get_service_url("scene-search"), payload, api_key)
        cls.logout_m2m(api_key)

        gdf = gpd.GeoDataFrame(res['results'])
        gdf.geometry = gdf['spatialCoverage'].apply(lambda x: shape(x))
        return gdf

    def download_datasets(self, dataset_name, entity_ids: list, filetype='bundle'):
        """
        :param dataset_name:
        :param entity_ids: list of entity ids
        :param filetype:  str either 'bundle' or 'band'
        :return:
        """
        startTime = time.time()
        apiKey = self.login_m2m()
        """
               check download options
                {
                    "entityIds": "LT50290302005219EDC00,LE70820552011359EDC00"
                    "datasetName": "gls_all"
                }
        """
        list_id = "lbdc_scene_list"
        payload = {
            "entityIds": ",".join(map(str, entity_ids)),
            "datasetName": dataset_name,
            "listId": list_id
        }
        products = self.sendRequest(self.get_service_url("download-options"), payload, apiKey)
        da_logger.info("Got product download options\n")

        # Select products
        # downloads = []
        # for product in products:
        #     if product["bulkAvailable"]:
        #         downloads.append({"entityId": product["entityId"], "productId": product["id"]})
        downloads = []
        if products:
            if filetype == 'bundle':
                # select bundle files
                for product in products:
                    if product["bulkAvailable"]:
                        downloads.append({"entityId": product["entityId"], "productId": product["id"]})
            elif filetype == 'band':
                # select band files
                for product in products:
                    if product["secondaryDownloads"] is not None and len(product["secondaryDownloads"]) > 0:
                        for secondaryDownload in product["secondaryDownloads"]:
                            if secondaryDownload["bulkAvailable"]:
                                downloads.append(
                                    {"entityId": secondaryDownload["entityId"], "productId": secondaryDownload["id"]})
            else:
                # select all available files
                for product in products:
                    if product["bulkAvailable"]:
                        downloads.append({"entityId": product["entityId"], "productId": product["id"]})
                        if product["secondaryDownloads"] is not None and len(product["secondaryDownloads"]) > 0:
                            for secondaryDownload in product["secondaryDownloads"]:
                                if secondaryDownload["bulkAvailable"]:
                                    downloads.append(
                                        {"entityId": secondaryDownload["entityId"],
                                         "productId": secondaryDownload["id"]})

        # Remove the list
        payload = {
            "listId": list_id
        }
        self.sendRequest(self.get_service_url("scene-list-remove"), payload, apiKey)

        # Send download-request
        if len(downloads) > 0:
            payLoad = {
                "downloads": downloads,
                "label": self.label,
                'returnAvailable': True
            }

            da_logger.info(f"Sending download request ...\n")
            results = self.sendRequest(self.get_service_url("download-request"), payLoad, apiKey)
            da_logger.info(f"Done sending download request\n")

            for result in results['availableDownloads']:
                da_logger.debug(f"Get download url: {result['url']}\n")
                self.runDownload(self.threads, result['url'])

            preparingDownloadCount = len(results['preparingDownloads'])
            preparingDownloadIds = []
            if preparingDownloadCount > 0:
                for result in results['preparingDownloads']:
                    preparingDownloadIds.append(result['downloadId'])

                payload = {"label": self.label}
                # Retrieve download urls
                da_logger.info("Retrieving download urls...\n")
                results = self.sendRequest(self.get_service_url("download-retrieve"), payload, apiKey, False)
                if not results:
                    for result in results['available']:
                        if result['downloadId'] in preparingDownloadIds:
                            preparingDownloadIds.remove(result['downloadId'])
                            da_logger.debug(f"Get download url: {result['url']}\n")
                            self.runDownload(self.threads, result['url'])

                    for result in results['requested']:
                        if result['downloadId'] in preparingDownloadIds:
                            preparingDownloadIds.remove(result['downloadId'])
                            da_logger.debug(f"Get download url: {result['url']}\n")
                            self.runDownload(self.threads, result['url'])

                # Don't get all download urls, retrieve again after 30 seconds
                while len(preparingDownloadIds) > 0:
                    da_logger.critical(
                        f"{len(preparingDownloadIds)} downloads are not available yet. Waiting for 30s to retrieve again\n")
                    time.sleep(30)
                    results = self.sendRequest(self.get_service_url("download-retrieve"), payload, apiKey, False)
                    if not results:
                        for result in results['available']:
                            if result['downloadId'] in preparingDownloadIds:
                                preparingDownloadIds.remove(result['downloadId'])
                                da_logger.debug(f"Get download url: {result['url']}\n")
                                self.runDownload(self.threads, result['url'])

            da_logger.info("\nGot download urls for all downloads\n")

        self.logout_m2m(apiKey)
        if len(self.threads) > 0:
            da_logger.info("Downloading files... Please do not close the program\n")
            for thread in self.threads:
                thread.join()

            da_logger.critical("Complete Downloading")

            executionTime = round((time.time() - startTime), 2)
            da_logger.critical(f'Total time: {executionTime} seconds')
        else:
            da_logger.critical("No file available to download")
