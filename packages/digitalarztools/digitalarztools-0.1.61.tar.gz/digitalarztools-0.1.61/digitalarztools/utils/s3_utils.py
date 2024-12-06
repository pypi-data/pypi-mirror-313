import os.path
from typing import Union
from urllib.parse import urlparse

import rasterio
from boto3 import Session
from botocore.exceptions import ClientError
from botocore.response import StreamingBody
from rasterio.session import AWSSession

from digitalarztools.io.file_io import FileIO


# from app.config.utils import ConfigUtils

# config_utils = ConfigUtils()
# aws_access_key_id = config_utils.get_data('aws_access_key_id')
# aws_secret_access_key = config_utils.get_data('aws_secret_access_key')
# aws_region = config_utils.get_data('aws_region')
# # bucket_name = config_utils.get_data('bucket_name')
# cog_bucket_name = config_utils.get_data('bucket_name_cog')
# stac_bucket_name = config_utils.get_data("bucket_name_stac")


class S3Utils:
    session: Session

    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.session = Session(aws_access_key_id, aws_secret_access_key, region_name=region_name)

        # self.s3_resource =
        # self.s3_client =

    def get_s3_resource(self):
        return self.session.resource("s3")

    def get_session(self):
        return self.session

    def get_resource_file(self, object_uri) -> StreamingBody:
        bucket_name, object_name = S3Utils.get_bucket_name_and_path(object_uri)
        bucket = self.session.resource("s3").Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=object_name):
            return obj.get()['Body']

    def is_file_exists(self, object_uri):
        bucket_name, object_name = S3Utils.get_bucket_name_and_path(object_uri)
        bucket = self.session.resource("s3").Bucket(bucket_name)
        obj = list(bucket.objects.filter(Prefix=object_name))
        res = True if len(obj) >= 1 else False
        return res

    def get_files_list_dir(self, object_uri):
        bucket_name, object_name = S3Utils.get_bucket_name_and_path(object_uri)
        bucket = self.session.resource("s3").Bucket(bucket_name)
        objs = list(bucket.objects.filter(Prefix=object_name))
        return objs

    def upload_file(self, src_fp: str, des_path_uri:str):
        try:
            # file_path, object_name = CommonUtils.separate_file_path_name(des_path_name)
            bucket_name, object_path = S3Utils.get_bucket_name_and_path(des_path_uri)
            response = self.session.client("s3").upload_file(src_fp, bucket_name, object_path)
        except ClientError as e:
            print(e)
            return False
        return True

    def delete_file(self, uri):
        bucket_name, object_name = self.get_bucket_name_and_path(uri)
        response = self.session.client("s3").delete_object(Bucket=bucket_name, Key=object_name)
        return True

    def download_file_s3(self, uri, download_file_path):
        bucket_name, object_name = self.get_bucket_name_and_path(uri)
        download_file_path = os.path.join(download_file_path, object_name)
        FileIO.mkdirs(download_file_path)
        response = self.session.client("s3").download_file(Bucket=bucket_name, Key=object_name,
                                                           Filename=download_file_path)
        return download_file_path

    def read_file(self, object_uri):
        bucket_name, object_name = S3Utils.get_bucket_name_and_path(object_uri)
        bucket = self.session.resource("s3").Bucket(bucket_name)
        for obj in bucket.objects.filter(Prefix=object_name):
            return obj.get()['Body'].read().decode('utf-8')

    def write_file(self, content, des_uri):
        s3 = self.session.resource("s3")
        bucket_name, key = S3Utils.get_bucket_name_and_path(des_uri)
        result = s3.Object(bucket_name, key).put(Body=content, ContentEncoding="utf-8")
        res = result.get('ResponseMetadata')

        # if res.get('HTTPStatusCode') == 200:
        #     print('File Uploaded Successfully')
        # else:
        #     print('File Not Uploaded')

    # def get_obj_url(self, key):
    #     location = self.session.client("s3").get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    #     return "https://s3-%s.amazonaws.com/%s/%s" % (location, bucket_name, key)

    def get_rio_dataset(self, url: str):
        # url = 's3://sentinel-s2-l1c/tiles/10/S/DG/2015/12/7/0/B01.jp2'
        try:
            session = rasterio.Env(AWSSession(self.session))
            # if "s3://" not in img_path:
            #     url = self.get_s3_url(img_path)
            with session:
                raster = rasterio.open(url)
                if not raster.crs:
                    raster = self.convert_tiff_to_geo_tiff(raster, url)
                return raster
        except Exception as e:
            print(str(e.args))

    # def get_cog_rio_dataset(self, url: str) -> COGReader:
    #     session = rasterio.Env(AWSSession(self.session))
    #     with session:
    #         return COGReader(url)

    @staticmethod
    def get_s3_uri(s3_bucket_name: str, rel_file_path: str):

        """
        s3://AKIARQNTK7F6S6XI275M@s3.amazonaws.com/pak-dch/landscan_hd_pk_cog.tif
        s3://bucket_name/sub_folder/file+name
        s3://pucit-cms/pid_media/420973_740993_20.jpg
        """
        return "s3://{}/{}".format(s3_bucket_name, rel_file_path)

    @staticmethod
    def get_bucket_name_and_path(uri):
        parsed = urlparse(uri)
        if parsed.scheme == "s3":
            bucket = parsed.netloc
            key = parsed.path[1:]
            return bucket, key

    def get_file_size(self, uri):
        bucket_name, object_name = self.get_bucket_name_and_path(uri)
        response = self.session.client("s3").head_object(Bucket=bucket_name, Key=object_name)
        return response['ContentLength']

