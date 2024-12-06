import os
import traceback

import numpy as np
import pandas as pd
import pyproj
import requests
from datetime import datetime

from affine import Affine
from bs4 import BeautifulSoup
from dateutil.relativedelta import relativedelta

from digitalarztools.pipelines.config.data_centers import DataCenters
from digitalarztools.pipelines.nasa.variables_info import GLDASVariablesInfo

from netCDF4 import Dataset

from digitalarztools.io.raster.rio_raster import RioRaster
from digitalarztools.utils.logger import da_logger
from digitalarztools.utils.waitbar_console import WaitBarConsole


class MERRA:
    @staticmethod
    def get_last_available_date():
        url = "https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXFLX.5.12.4"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        Years = []
        for link in soup.findAll('a'):
            link_str = str(link.get('href'))
            if link_str[0] == "1" or link_str[0] == "2":
                Years.append(int(link_str[:-1]))

        Year = np.max(Years)
        url = "https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXFLX.5.12.4/%d" % Year
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        Months = []
        for link in soup.findAll('a'):
            link_str = str(link.get('href'))
            if link_str[0] == "0" or link_str[0] == "1":
                Months.append(int(link_str[:-1]))

        Month = np.max(Months)

        merra_end_date = datetime(Year, Month, 1) + relativedelta(months=+1)
        return merra_end_date

    @classmethod
    def merra2_daily(cls, des_dir, variables, start_date, end_date, lat_lim, lon_lim, wait_bar=1, data_type=["mean"]):
        """
            This function downloads MERRA daily data for a given variable, time
            interval, and spatial extent.

            Keyword arguments:
            des_dir -- 'C:/file/to/path/'
            Vars -- ['t2m', 'v2m']
            start_date -- 'yyyy-mm-dd'
            end_date -- 'yyyy-mm-dd'
            lat_lim -- [ymin, ymax]
            lon_lim -- [xmin, xmax]
            wait_bar -- 1 (Default) Will print a waitbar
        """
        for variable in variables:
            if wait_bar == 1:
                WaitBarConsole.print_bar_text(
                    '\nDownloading daily MERRA %s data for the period %s till %s' % (variable, start_date, end_date))

            # Download data
            cls.download_data(des_dir, variable, start_date, end_date, lat_lim, lon_lim, "daily_MERRA2", '', wait_bar,
                              data_type)

    @classmethod
    def merra2_hourly(cls, des_dir, variables, start_date, end_date, lat_lim, lon_lim, periods=list(range(1, 25)),
                      wait_bar=1):
        """
        This function downloads MERRA inst data for a given variable, time
        interval, and spatial extent.

        Keyword arguments:
        des_dir -- 'C:/file/to/path/'
        variables -- ['t2m', 'v2m']
        start_date -- 'yyyy-mm-dd'
        end_date -- 'yyyy-mm-dd'
        lat_lim -- [ymin, ymax]
        lon_lim -- [xmin, xmax]
        periods -- [1,2,3,4,5,6,7,8,23,24] Period that needs to be downloaded. 1 period is 1 hour starting from noon
        wait_bar -- 1 (Default) Will print a waitbar
        """

        for variable in variables:

            for Period in periods:

                if wait_bar == 1:
                    WaitBarConsole.print_bar_text(
                        '\nDownloading hourly MERRA %s data for the period %s till %s, Period = %s' % (
                            variable, start_date, end_date, Period))

                # Download data
                cls.download_data(des_dir, variable, start_date, end_date, lat_lim, lon_lim, "hourly_MERRA2", Period,
                                  wait_bar,
                                  data_type=["mean"])

    @classmethod
    def download_data(cls, des_dir, variable, start_date, end_date, lat_lim, lon_lim, time_step, period, wait_bar,
                      data_type=["mean"]):

        output_name, output_name_min, output_name_max = "", "", ""
        # Check the latitude and longitude and otherwise set lat or lon on greatest extent
        if lat_lim[0] < -90 or lat_lim[1] > 90:
            da_logger.warning('Latitude above 90N or below 90S is not possible. Value set to maximum')
            lat_lim[0] = np.max(lat_lim[0], -90)
            lat_lim[1] = np.min(lat_lim[1], 90)
        if lon_lim[0] < -180 or lon_lim[1] > 180:
            da_logger.warning('Longitude must be between 180E and 180W. Now value is set to maximum')
            lon_lim[0] = np.max(lon_lim[0], -180)
            lon_lim[1] = np.min(lon_lim[1], 180)

            # Get information of the parameter
        var_info = GLDASVariablesInfo(time_step)
        parameter = var_info.names[variable]
        unit = var_info.units[variable]
        types = var_info.types[variable]

        if time_step == "yearly":
            parameter = "Temperature_Amplitude"

        # Create output folder
        output_folder = os.path.join(des_dir, "MERRA", parameter, time_step)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if time_step.split("_")[-1] == "MERRA2":
            corr_x = 0.625 * 0.5
            corr_y = 0.5 * 0.5
        else:
            corr_x = 0
            corr_y = 0

        # Define IDs
        IDx = [np.floor((lon_lim[0] + corr_x + 180) / 0.625), np.ceil((lon_lim[1] + corr_x + 180) / 0.625)]
        IDy = [np.floor((lat_lim[0] + corr_y + 90) / 0.5), np.ceil((lat_lim[1] + corr_y + 90) / 0.5)]

        # Create output geo transform
        Xstart = -180 + 0.625 * IDx[0] - corr_x
        Ystart = -90 + 0.5 * IDy[1] - corr_y

        if time_step == "yearly":
            Dates = pd.date_range(start_date, end_date, freq="AS")
        else:
            Dates = pd.date_range(start_date, end_date, freq="D")

        # Create Waitbar
        if wait_bar == 1:
            total_amount = len(Dates)
            amount = 0
            WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

        for Date in Dates:

            # Define the IDz
            if time_step == "hourly_MERRA2":
                Hour = int((period - 1) * 1)
                output_name = os.path.join(output_folder, "%s_MERRA_%s_hourly_%d.%02d.%02d_H%02d.M00.tif" % (
                    variable, unit, Date.year, Date.month, Date.day, Hour))
                output_folder_temp = os.path.join(des_dir, "MERRA", "Temp")
                if not os.path.exists(output_folder_temp):
                    os.makedirs(output_folder_temp)
                year = Date.year
                month = Date.month
                day = Date.day
                output_name_min = output_folder
                output_name_max = output_folder

            if time_step == "daily_MERRA2":
                if "mean" in data_type:
                    output_name = os.path.join(output_folder, "%s_MERRA_%s_daily_%d.%02d.%02d.tif" % (
                        variable, unit, Date.year, Date.month, Date.day))
                else:
                    output_name = output_folder
                if "min" in data_type:
                    output_name_min = os.path.join(output_folder, "min", "%smin_MERRA_%s_daily_%d.%02d.%02d.tif" % (
                        variable, unit, Date.year, Date.month, Date.day))
                else:
                    output_name_min = output_folder
                if "max" in data_type:
                    output_name_max = os.path.join(output_folder, "max", "%smax_MERRA_%s_daily_%d.%02d.%02d.tif" % (
                        variable, unit, Date.year, Date.month, Date.day))
                else:
                    output_name_max = output_folder

                output_folder_temp = os.path.join(des_dir, "MERRA", "Temp")
                if not os.path.exists(output_folder_temp):
                    os.makedirs(output_folder_temp)
                year = Date.year
                month = Date.month
                day = Date.day

            if time_step == "three_hourly":
                IDz_start = IDz_end = int(((Date - pd.Timestamp("2002-07-01")).days) * 8) + (period - 1)
                Hour = int((period - 1) * 3)
                output_name = os.path.join(output_folder, "%s_MERRA_%s_3-hourly_%d.%02d.%02d_H%02d.M00.tif" % (
                    variable, unit, Date.year, Date.month, Date.day, Hour))
                output_name_min = output_folder
                output_name_max = output_folder

            if time_step == "daily":
                IDz_start = int(((Date - pd.Timestamp("2002-07-01")).days) * 8)
                IDz_end = IDz_start + 7
                if "mean" in data_type:
                    output_name = os.path.join(output_folder, "%s_MERRA_%s_daily_%d.%02d.%02d.tif" % (
                        variable, unit, Date.year, Date.month, Date.day))
                else:
                    output_name = output_folder
                if "min" in data_type:
                    output_name_min = os.path.join(output_folder, "min", "%smin_MERRA_%s_daily_%d.%02d.%02d.tif" % (
                        variable, unit, Date.year, Date.month, Date.day))
                else:
                    output_name_min = output_folder
                if "max" in data_type:
                    output_name_max = os.path.join(output_folder, "max", "%smax_MERRA_%s_daily_%d.%02d.%02d.tif" % (
                        variable, unit, Date.year, Date.month, Date.day))
                else:
                    output_name_max = output_folder

            if time_step == "yearly":
                IDz_start = (Date.year - pd.Timestamp("2002-07-01").year) * 12 + Date.month - pd.Timestamp(
                    "2002-07-01").month
                IDz_end = IDz_start + 11
                output_name = os.path.join(output_folder, "Tamp_MERRA_%s_yearly_%d.%02d.%02d.tif" % (
                    unit, Date.year, Date.month, Date.day))
                output_name_min = output_folder
                output_name_max = output_folder

            if not (os.path.exists(output_name) and os.path.exists(output_name_min) and os.path.exists(
                    output_name_max)):
                if time_step == "hourly_MERRA2" or time_step == "daily_MERRA2":
                    if Date < datetime(1992, 1, 1):
                        number = 1
                    elif (Date >= datetime(1992, 1, 1) and Date < datetime(2001, 1, 1)):
                        number = 2
                    elif (Date >= datetime(2001, 1, 1) and Date < datetime(2011, 1, 1)):
                        number = 3
                    else:
                        number = 4

                    if Date.month == 9 and Date.year == 2020:
                        number2 = 1
                    elif Date.month > 5 and Date.month < 10 and Date.year == 2021:
                        number2 = 1
                    else:
                        number2 = 0

                    if variable == "swgnet" or variable == "swgdn" or variable == "ts":
                        url_MERRA = r"https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXRAD.5.12.4/%d/%02d/MERRA2_%s0%s.tavg1_2d_rad_Nx.%d%02d%02d.nc4" % (
                            year, month, number, number2, year, month, day)
                    elif variable == "prectotcorr":
                        url_MERRA = r"https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2T1NXFLX.5.12.4/%d/%02d/MERRA2_%s0%s.tavg1_2d_flx_Nx.%d%02d%02d.nc4" % (
                            year, month, number, number2, year, month, day)
                    else:
                        url_MERRA = r"https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2I1NXASM.5.12.4/%d/%02d/MERRA2_%s0%s.inst1_2d_asm_Nx.%d%02d%02d.nc4" % (
                            year, month, number, number2, year, month, day)
                # https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2I1NXASM.5.12.4/2021/01/MERRA2_400.inst1_2d_asm_Nx.20210101.nc4
                # https://goldsmr4.gesdisc.eosdis.nasa.gov/data/MERRA2/M2I1NXASM.5.12.4/2021/09/MERRA2_401.inst1_2d_asm_Nx.20210902.nc4

                if (time_step == "three_hourly" or time_step == "daily"):

                    # define total url
                    if (variable == "ps" or variable == "slp"):
                        url_start = r"https://opendap.nccs.nasa.gov/dods/GEOS-5/MERRAero/hourly/inst3hr_3d_asm_Nv."
                    else:
                        url_start = r"https://opendap.nccs.nasa.gov/dods/GEOS-5/MERRAero/hourly/tavg3hr_2d_asm_Nx."

                    url_MERRA = url_start + 'ascii?%s[%s:1:%s][%s:1:%s][%s:1:%s]' % (
                        variable.replace("swgdn", "swgdwn"), IDz_start, IDz_end, int(IDy[0]), int(IDy[1]), int(IDx[0]),
                        int(IDx[1]))
                    da_logger.debug(url_MERRA)
                if time_step == "yearly":
                    url_start = r"https://opendap.nccs.nasa.gov/dods/GEOS-5/MERRAero/monthly/tavg3hr_2d_asm_Nx."
                    url_MERRA = url_start + 'ascii?%s[%s:1:%s][%s:1:%s][%s:1:%s]' % (
                        variable, IDz_start, IDz_end, int(IDy[0]), int(IDy[1]), int(IDx[0]), int(IDx[1]))

                    # Change date for now, there is no OpenDAP system for those years.
                    if Date >= datetime.datetime(2015, 1, 1):
                        Date = datetime.datetime(2014, 1, 1)

                # Reset the begin parameters for downloading
                downloaded = 0
                N = 0

                username, password = DataCenters().get_server_account("NASA")

                # if not downloaded try to download file
                while downloaded == 0:
                    try:
                        N += 1

                        if (time_step == "hourly_MERRA2" or time_step == "daily_MERRA2"):

                            # Define the output name that is downloaded
                            file_name = os.path.join(output_folder_temp, url_MERRA.split("/")[-1])
                            if not os.path.exists(file_name):

                                # make contact with server
                                x = requests.get(url_MERRA, allow_redirects=False, timeout=120)
                                try:
                                    try:
                                        y = requests.get(x.headers['location'], auth=(username, password), timeout=120)
                                    except:
                                        from requests.packages.urllib3.exceptions import InsecureRequestWarning
                                        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                                        y = requests.get(x.headers['location'], auth=(username, password), verify=False,
                                                         timeout=120)

                                    # Write the download in the output directory
                                    z = open(file_name, 'wb')
                                    z.write(y.content)
                                    z.close()
                                    statinfo = os.stat(file_name)
                                    # Say that download was succesfull
                                    if int(statinfo.st_size) > 1000:
                                        downloaded = 1
                                except:

                                    # Write the download in the output directory
                                    z = open(file_name, 'wb')
                                    z.write(x.content)
                                    z.close()
                                    statinfo = os.stat(file_name)
                                    # Say that download was succesfull
                                    if int(statinfo.st_size) > 1000:
                                        downloaded = 1

                            else:
                                downloaded = 1

                            data_end, data_min, data_max = cls.Get_NC_data_end(file_name, variable, time_step, period,
                                                                               IDy,
                                                                               IDx,
                                                                               var_info)
                            # os.remove(file_name)

                        else:

                            # download data (first save as text file)
                            pathtext = os.path.join(output_folder, 'temp%s.txt' % str(IDz_start))

                            # Download the data
                            # urllib.request.urlretrieve(url_MERRA, filename=pathtext)

                            if not os.path.exists(pathtext):

                                # make contact with server
                                x = requests.get(url_MERRA, allow_redirects=False, timeout=120)

                                # Write the download in the output directory
                                z = open(pathtext, 'wb')
                                z.write(x.content)
                                z.close()
                                statinfo = os.stat(pathtext)
                                # Say that download was succesfull
                                if int(statinfo.st_size) > 100:
                                    downloaded = 1

                            else:
                                downloaded = 1

                                # Reshape data
                            datashape = [int(IDy[1] - IDy[0] + 1), int(IDx[1] - IDx[0] + 1)]
                            data_start = np.genfromtxt(pathtext, dtype=float, skip_header=1, skip_footer=6,
                                                       delimiter=',')
                            data_list = np.asarray(data_start[:, 1:])
                            if time_step == "yearly":
                                data_end = np.resize(data_list, (12, datashape[0], datashape[1]))
                            if time_step == "daily":
                                data_end = np.resize(data_list, (8, datashape[0], datashape[1]))
                            if time_step == "three_hourly":
                                data_end = np.resize(data_list, (datashape[0], datashape[1]))
                            os.remove(pathtext)

                            # Set no data value
                            data_end[data_end > 1000000] = -9999

                            if time_step == "daily":

                                if "min" in data_type:
                                    data_min = np.nanmin(data_end, 0)

                                if "max" in data_type:
                                    data_max = np.nanmax(data_end, 0)

                                if "mean" in data_type:

                                    if types == "state":
                                        data_end = np.nanmean(data_end, 0)
                                    else:
                                        data_end = np.nansum(data_end, 0)

                            if time_step == "yearly":
                                data_min = np.nanmin(data_end, 0)
                                data_max = np.nanmax(data_end, 0)
                                data_end = data_max - data_min

                            # Download was succesfull
                            downloaded = 1

                        # Add the VarFactor
                        if var_info.factors[variable] < 0:
                            if "mean" in data_type:
                                data_end[data_end != -9999] = data_end[data_end != -9999] + var_info.factors[variable]
                                data_end[data_end < -9999] = -9999
                                data_end = np.flipud(data_end)
                            if "min" in data_type:
                                data_min[data_min != -9999] = data_min[data_min != -9999] + var_info.factors[variable]
                                data_min[data_min < -9999] = -9999
                                data_min = np.flipud(data_min)
                            if "max" in data_type:
                                data_max[data_max != -9999] = data_max[data_max != -9999] + var_info.factors[variable]
                                data_max[data_max < -9999] = -9999
                                data_max = np.flipud(data_max)

                        else:
                            if "mean" in data_type:
                                data_end[data_end != -9999] = data_end[data_end != -9999] * var_info.factors[variable]
                                data_end[data_end < -9999] = -9999
                                data_end = np.flipud(data_end)
                            if "min" in data_type:
                                data_min[data_min != -9999] = data_min[data_min != -9999] * var_info.factors[variable]
                                data_min[data_min < -9999] = -9999
                                data_min = np.flipud(data_min)
                            if "max" in data_type:
                                data_max[data_max != -9999] = data_max[data_max != -9999] * var_info.factors[variable]
                                data_max[data_max < -9999] = -9999
                                data_max = np.flipud(data_max)

                                # Save as tiff file
                        # geo_out = tuple([Xstart, 0.625, 0, Ystart, 0, -0.5])
                        # proj = "WGS84"

                        transform = Affine(0.625, 0, Xstart, 0, -0.5, Ystart)
                        wgs_crs = pyproj.CRS.from_epsg(4326)
                        if "mean" in data_type:
                            # DC.Save_as_tiff(output_name, data_end, geo_out, proj)
                            RioRaster.write_to_file(output_name, data_end, wgs_crs, transform, -9999)
                        if "min" in data_type:
                            # DC.Save_as_tiff(output_name_min, data_min, geo_out, proj)
                            RioRaster.write_to_file(output_name_min, data_min, wgs_crs, transform, -9999)
                        if "max" in data_type:
                            # DC.Save_as_tiff(output_name_max, data_max, geo_out, proj)
                            RioRaster.write_to_file(output_name_max, data_max, wgs_crs, transform, -9999)

                        # Stop trying after 3 times
                        if N == 4 and downloaded == 0:
                            da_logger.critical('Data from ' + Date.strftime('%Y-%m-%d') + ' is not available')
                            downloaded = 1

                            # If download was not succesfull
                    except:
                        da_logger.error(traceback.print_stack())
                        # Try another time
                        N = N + 1

                        # Stop trying after 3 times
                        if N == 4:
                            da_logger.critical('Data from ' + Date.strftime('%Y-%m-%d') + ' is not available')
                            downloaded = 1

            if wait_bar == 1:
                amount += 1
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

        return ()

    @staticmethod
    def Get_NC_data_end(file_name, Var, TimeStep, Period, IDy, IDx, VarInfo):
        dict_para = {'t2m': 'T2M',
                     'u2m': 'U2M',
                     'v2m': 'V2M',
                     'q2m': 'QV2M',
                     'tpw': 'TQV',
                     'ps': 'PS',
                     'slp': 'SLP',
                     'swgnet': 'SWGDN',
                     'swgdn': 'SWGDN',
                     'prectotcorr': 'PRECTOTCORR',
                     'ts': 'TS'}

        types = VarInfo.types[Var]
        if TimeStep == "hourly_MERRA2":
            data_end = Dataset(file_name)["%s" % dict_para[Var]][int(Period - 1), int(IDy[0]):int(IDy[1]),
                       int(IDx[0]):int(IDx[1])]
            data_min = []
            data_max = []

        else:
            data = Dataset(file_name)["%s" % dict_para[Var]][:, int(IDy[0]):int(IDy[1]), int(IDx[0]):int(IDx[1])]
            if types == "state":
                data_end = np.nanmean(data, 0)
            else:
                data_end = np.nansum(data, 0)

            data[data == -9999] = np.nan
            data_min = np.nanmin(data, 0)
            data_max = np.nanmax(data, 0)

        return data_end, data_min, data_max

