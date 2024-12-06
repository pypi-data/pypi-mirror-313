import requests
import json
from digitalarztools.io.file_io import FileIO
from digitalarztools.utils.logger import da_logger


class UrlIO:
    @staticmethod
    def download_url(url,file_path: str, allow_redirects=True):
        downloaded_obj = requests.get(url, allow_redirects=allow_redirects)
        if downloaded_obj.status_code == 200:
            FileIO.write_file(file_path, downloaded_obj.content)
            return True
        else:
            error = json.loads(downloaded_obj.text)
            da_logger.error(error['error']["code"], error['error']["message"])
            return False
