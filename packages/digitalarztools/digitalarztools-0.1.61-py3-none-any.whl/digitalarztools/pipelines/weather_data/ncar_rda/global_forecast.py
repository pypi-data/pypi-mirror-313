import csv
import os
import traceback
from datetime import datetime, timedelta

from pprint import pprint

import pandas as pd
import requests

import digitalarztools.pipelines.weather_data.ncar_rda.rdams_client as rc
from digitalarztools.pipelines.weather_data.ncar_rda.rda_enum import RDAStatus, RDAFormat

current_dir = os.path.dirname(__file__)
docs_dir = os.path.join(current_dir, 'docs')


class GlobalForecast:
    """
        Research Data Archive (RDA) apps clients utils
        datasets details https://rda.ucar.edu/datasets/
        for token generation https://rda.ucar.edu/accounts/profile/
        documentation https://github.com/NCAR/rda-apps-clients/blob/main/docs/README.md

        ds084.1 - NCEP GFS 0.25 Degree Global Forecast Grids Historical Archive
        data access https://rda.ucar.edu/datasets/ds084.1/dataaccess/
        pip install rda-apps-clients

        sample control file
              {'dataset': 'ds084.1',
                 'date': '202404200600/to/202405060600',
                 'datetype': 'valid',
                 'elon': 79.29198455810547,
                 'level': 'HTGL:2',
                 'nlat': 37.089423898000064,
                 'oformat': 'grib',
                 'param': 'R H',
                 'product': '384-hour Forecast',
                 'slat': 23.694683075000057,
                 'wlon': 60.87859740400006}
    """

    def __init__(self, is_meta_data_req=False):
        self.ds = "ds084.1"
        self.metadata_df = self.get_metadata() if is_meta_data_req else pd.DataFrame()

    def get_summary(self):
        res = rc.get_summary(self.ds)
        pprint(res)

    def get_metadata(self) -> pd.DataFrame:
        res = rc.get_metadata(self.ds)
        df = pd.DataFrame(res['data']['data'])
        return df

    def save_metadata(self):
        fp = os.path.join(os.path.dirname(__file__), "ds084.1_meta_data.xlsx")
        # print(fp)
        if self.metadata_df.empty:
            self.metadata_df = self.get_metadata()
        self.metadata_df.to_excel(fp)

    def get_common_product(self, params_of_interest: list):
        # Define the parameters of interest
        # params_of_interest = ["T MAX", "T MIN", "TMP", "R H", "A PCP"]

        # Filter the DataFrame to only include rows with these parameters
        filtered_df = self.metadata_df[self.metadata_df['param'].isin(params_of_interest)]

        # Group by 'product' and collect unique parameters associated with each product
        grouped_products = filtered_df.groupby('product')['param'].unique()
        grouped_products_df = pd.DataFrame(grouped_products).reset_index()
        # Filter to find products associated with all specified parameters
        # common_products = grouped_products[grouped_products.apply(lambda x: set(params_of_interest).issubset(set(x)))]

        # Display the common products
        # print(common_products)
        # return common_products['product'].values.tolist()
        return grouped_products_df

    def get_distinct_product_params(self, product) -> dict:
        if self.metadata_df.empty:
            self.metadata_df = self.get_metadata()
        product_df = self.metadata_df[self.metadata_df['product'].str.contains(product, na=False)]
        product_df = product_df.drop_duplicates(subset='param')
        params = dict(zip(product_df['param'], product_df['param_description']))
        return params

    def get_distinct_param_name_list(self) -> dict:
        if self.metadata_df.empty:
            self.metadata_df = self.get_metadata()
        # params = self.metadata_df.param.unique().tolist()
        params_df = self.metadata_df.drop_duplicates(subset='param')
        params = dict(zip(params_df['param'], params_df['param_description']))
        # pprint(params)
        return params

    def get_distinct_param_product_list(self, param_name: list) -> list:
        param_df = self.get_params_metadata(param_name)
        products = param_df['product'].unique().tolist()
        # pprint(products)
        return products

    def get_params_metadata(self, param_names: list, save_file=False) -> pd.DataFrame:
        # param_df = self.metadata_df[self.metadata_df.param_description.str.contains("temperature", case=False)]
        if self.metadata_df.empty:
            self.metadata_df = self.get_metadata()
        param_df = self.metadata_df[self.metadata_df.param.isin(param_names)]
        if save_file:
            fp = os.path.join(os.path.dirname(__file__), f"ds084.1_{'_'.join(param_names)}.xlsx")
            param_df.to_excel(fp)
        # pprint(param_df.shape)
        # pprint(param_df)
        return param_df

    def get_param_product_metadata(self, param_names: list, product: str, is_full_string=True) -> pd.DataFrame:
        param_df = self.get_params_metadata(param_names)
        if is_full_string:
            product_df = param_df[param_df['product'] == product]
        else:
            product_df = param_df[param_df['product'].str.contains(product)]
        return product_df

    def get_latest_request_dates(self, product_df: pd.DataFrame=None, time_delta_hrs=384, delta_in_days=-2) -> str:
        if product_df is not None:
            start, end = self.get_product_available_dates(product_df)
            end_date = end + timedelta(days=delta_in_days) if delta_in_days <= 0 else end
            start_date = end_date + timedelta(hours=-time_delta_hrs)
        else:
            start_date = datetime.now() + timedelta(days=delta_in_days)
            end_date =  start_date  + timedelta(hours=+time_delta_hrs)
        # as product is 6-hour Minimum (initial+378 to initial+384)
        start_date_time_string = start_date.strftime("%Y%m%d%H%M")
        end_date_time_string = end_date.strftime("%Y%m%d%H%M")
        return f"{start_date_time_string}/to/{end_date_time_string}"

    def get_product_available_dates(self, product_df: pd.DataFrame):
        date_format = "%Y%m%d%H%M"
        start_date = datetime.strptime(str(product_df['start_date'].min()), date_format)
        end_date = datetime.strptime(str(product_df['end_date'].max()), date_format)
        return start_date, end_date

    def get_product_levels_info(self, product_df: pd.DataFrame, level_name='HTGL'):
        for levels in product_df.levels:
            level_df = pd.DataFrame(levels)
            gb = level_df.groupby('level')
            for level, group_df in gb:
                # info = f'{level}:' + '/'.join(ISBL_levels)
                if level == level_name:
                    info = f'{level}:' + '/'.join(group_df['level_value'].values.tolist())
                    return info

    def save_control_files_template(self):
        fp = os.path.join(docs_dir, "ds084.1_general_template.txt")
        rc.write_control_file_template(self.ds, fp)
        print("Saved control file template to {}".format(fp))

    def get_request_params(self, control_fil_name: str = None):
        control_file_name = os.path.join(docs_dir, f"{self.ds}_t_max_template.txt")
        _dict = rc.read_control_file(control_file_name)
        return _dict

    def submit_control_files(self, format: RDAFormat = RDAFormat.grib, bbox: list = [], request_params: dict = None,
                             params: list = []):
        if request_params is None:
            request_params = self.get_request_params()
            # param_product_df = self.get_param_product_metadata(request_params['param'], request_params["product"])
            # if not param_product_df.empty:
            #     request_params['level'] = self.get_product_levels_info(param_product_df)
            #     request_params['date'] = self.get_latest_request_dates(param_product_df)
        if format.value == "csv":
            request_params['oformat'] = 'csv'
        else:
            request_params['oformat'] = format.value if format.value else 'grib'
        if len(bbox) >= 4:
            request_params['slat'] = bbox[1]
            request_params['nlat'] = bbox[3]
            request_params['wlon'] = bbox[0]
            request_params['elon'] = bbox[2]

        if len(params) > 0:
            request_params['param'] = "/".join(params)
        # pprint(request_params)
        # res_fp = os.path.join(os.path.dirname(__file__), f"response_{_dict['date'].replace('/','_')}.json")
        res = rc.submit_json(request_params)
        # pprint(res)
        # with open(res_fp, 'w') as f:
        #     f.write(json.dumps(res))
        if 'request_id' in res['data']:
            req_id = res['data']['request_id']
            return req_id, request_params
        else:
            print(request_params)
            print(res)
            return None, request_params

    @staticmethod
    def check_ready(request_idx: str, wait_interval=120):
        """
        https://github.com/NCAR/rda-apps-clients/blob/main/src/python/request_workflow_example.ipynb
        """
        request_status = None
        """Checks if a request is ready."""
        # for i in range(10):  # 100 is arbitrary. This would wait 200 minutes for request to complete
        res = rc.get_status(request_idx)
        try:
            if 'data' in res and 'status' in  res['data']:
                request_status = res['data']['status']
                if request_status == 'Completed':
                    return True, request_status
                return False, request_status
        except Exception as e:
            traceback.print_exc()
            print(res)
        return False, None

    def extract_csv_file_as_json(self, request_idx: str) -> pd.DataFrame:
        ret = rc.get_filelist(request_idx)
        if len(ret['data']) == 0:
            return ret

        filelist = ret['data']['web_files']
        web_files = set(list(map(lambda x: x['web_path'], filelist)))
        final_df = pd.DataFrame()
        for _file in web_files:
            try:
                print(f'Downloading {_file}...')
                response = requests.get(_file)
                response.raise_for_status()  # Check that the request was successful

                # Read the content as text and split into lines
                lines = response.text.splitlines()

                # Use csv.DictReader to parse the CSV data
                reader = csv.DictReader(lines)

                # Convert each row of the CSV to a dictionary and store in a list
                data = [row for row in reader]
                # The [data] syntax converts it into a list of dictionaries
                df = pd.DataFrame(data)
                # Convert the date and time into a single datetime column
                df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
                df.drop(labels=['Date', 'Time'], axis=1, inplace=True)

                # Create a DataFrame
                final_df = pd.concat([final_df, df], axis=1)
                # results.append(data)

            except requests.RequestException as e:
                print(f"Error downloading {_file}: {e}")
                # results.append({'error': str(e), 'url': _file})
            except Exception as e:
                print(f"Unexpected error for {_file}: {e}")
                # results.append({'error': str(e), 'url': _file})

        return final_df

    def download_files(self, request_idx: str, output_dir: str):
        is_ready, status = self.check_ready(request_idx)
        file_name = None
        if is_ready:
            ret = rc.get_filelist(request_idx)
            if len(ret['data']) == 0:
                return ret

            filelist = ret['data']['web_files']

            # token = rc.get_authentication()
            # file_name = rc.download(request_idt_id)
            web_files = set(list(map(lambda x: x['web_path'], filelist)))
            rc.download_files(web_files, output_dir)
        return is_ready, status

    @staticmethod
    def purge_request(request_idx: str, wait_interval=120) -> RDAStatus:
        try:
            if not isinstance(request_idx, str):
                request_idx = str(request_idx)
            res = rc.purge_request(request_idx)
            # pprint(res)
            if res['http_response'] == 421:
                return RDAStatus.Deleted.value
            elif res['http_response'] == 200:
                return RDAStatus.Purged.value
        except Exception as e:
            traceback.print_exc()
        return RDAStatus.Error

    @staticmethod
    def get_all_request_index():
        # Fetch the list of request IDs
        all_status = rc.get_all_status()
        request_idx = [info['request_index'] for info in all_status['data'] if info['status'] == RDAStatus.Completed.value]
        return request_idx

