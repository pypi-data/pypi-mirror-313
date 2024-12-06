import os
import urllib

import numpy as np
import pandas as pd
import pyproj

from digitalarztools.io.raster.gdal_raster_io import GDALRasterIO
from digitalarztools.pipelines.nasa.variables_info import GEOSVariablesInfo
from digitalarztools.utils.logger import da_logger
from digitalarztools.utils.waitbar_console import WaitBarConsole


class GEOS:
    @classmethod
    def geos_daily(cls, Dir, Vars, Startdate, Enddate, latlim, lonlim, Waitbar=1, data_type=["mean"]):
        """
        This function downloads GEOS daily data for a given variable, time
        interval, and spatial extent.

        Keyword arguments:
        Dir -- 'C:/file/to/path/'
        Vars -- ['t2m', 'v2m']
        Startdate -- 'yyyy-mm-dd'
        Enddate -- 'yyyy-mm-dd'
        latlim -- [ymin, ymax]
        lonlim -- [xmin, xmax]
        Waitbar -- 1 (Default) Will print a waitbar
        """
        for Var in Vars:

            if Waitbar == 1:
                WaitBarConsole.print_bar_text('\nDownloading daily GEOS %s data for the period %s till %s' % (Var, Startdate, Enddate))

            # Download data
            cls.DownloadData(Dir, Var, Startdate, Enddate, latlim, lonlim, "daily", '', Waitbar, data_type)

    @classmethod
    def geos_hourly(cls, Dir, Vars, Startdate, Enddate, latlim, lonlim,
                    Periods=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24],
                    Waitbar=1):
        """
        This function downloads GEOS inst data for a given variable, time
        interval, and spatial extent.

        Keyword arguments:
        Dir -- 'C:/file/to/path/'
        Vars -- ['']
        Startdate -- 'yyyy-mm-dd'
        Enddate -- 'yyyy-mm-dd'
        latlim -- [ymin, ymax]
        lonlim -- [xmin, xmax]
    	Periods -- [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24] Period that needs to be downloaded. 1 period is 1 hour starting from noon
        Waitbar -- 1 (Default) Will print a waitbar
        """

        for Var in Vars:

            for Period in Periods:

                if Waitbar == 1:
                    WaitBarConsole.print_bar_text('\nDownloading hourly GEOS %s data for the period %s till %s, Period = %s' % (
                        Var, Startdate, Enddate, Period))

                # Download data
                cls.DownloadData(Dir, Var, Startdate, Enddate, latlim, lonlim, "hourly", Period, Waitbar,
                                 data_type=["mean"])

    @classmethod
    def DownloadData(cls, Dir, Var, Startdate, Enddate, latlim, lonlim, TimeStep, Period, Waitbar, data_type=["mean"]):

        # Check the latitude and longitude and otherwise set lat or lon on greatest extent
        if latlim[0] < -90 or latlim[1] > 90:
            da_logger.warning('Latitude above 90N or below 90S is not possible. Value set to maximum')
            latlim[0] = np.max(latlim[0], -90)
            latlim[1] = np.min(latlim[1], 90)
        if lonlim[0] < -180 or lonlim[1] > 180:
            da_logger.warning('Longitude must be between 180E and 180W. Now value is set to maximum')
            lonlim[0] = np.max(lonlim[0], -180)
            lonlim[1] = np.min(lonlim[1], 180)

            # Get information of the parameter
        VarInfo = GEOSVariablesInfo(TimeStep)
        Parameter = VarInfo.names[Var]
        unit = VarInfo.units[Var]
        types = VarInfo.types[Var]

        # Create output folder
        output_folder = os.path.join(Dir, "GEOS", Parameter, TimeStep)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Define IDs
        IDx = [np.floor((lonlim[0] + 180) / 0.3125), np.ceil((lonlim[1] + 180) / 0.3125)]
        IDy = [np.floor((latlim[0] + 90) / 0.25), np.ceil((latlim[1] + 90) / 0.25)]

        # Create output geo transform
        Xstart = -180 + 0.3125 * IDx[0]
        Ystart = -90 + 0.25 * IDy[1]
        geo_out = tuple([Xstart, 0.3125, 0, Ystart, 0, -0.25])
        proj = "WGS84"
        wgs_crs = pyproj.CRS.from_epsg(4326)

        Dates = pd.date_range(Startdate, Enddate, freq="D")

        # Create Waitbar
        if Waitbar == 1:
            total_amount = len(Dates)
            amount = 0
            WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)

        for Date in Dates:

            # Define the IDz
            if TimeStep == "hourly":
                IDz_start = IDz_end = int(((Date - pd.Timestamp("2017-12-01")).days) * 24) + (Period - 1)
                Hour = int((Period - 1))
                output_name = os.path.join(output_folder, "%s_GEOS_%s_hourly_%d.%02d.%02d_H%02d.M00.tif" % (
                    Var, unit, Date.year, Date.month, Date.day, Hour))
                output_name_min = output_folder
                output_name_max = output_folder
                if Var in ['t2m', 'u2m', 'v2m', 'qv2m', 'tqv', 'ps', 'slp', 't10m', 'v10m', 'u10m', 'v50m', 'u50m',
                           'ts']:
                    url_start = r"https://opendap.nccs.nasa.gov/dods/GEOS-5/fp/0.25_deg/assim/tavg1_2d_slv_Nx."
                if Var in ['swgdn']:
                    url_start = r"https://opendap.nccs.nasa.gov/dods/GEOS-5/fp/0.25_deg/assim/tavg1_2d_rad_Nx."

            if TimeStep == "three_hourly":
                IDz_start = IDz_end = int(((Date - pd.Timestamp("2017-12-01")).days) * 8) + (Period - 1)
                Hour = int((Period - 1) * 3)
                output_name = os.path.join(output_folder, "%s_GEOS_%s_3-hourly_%d.%02d.%02d_H%02d.M00.tif" % (
                    Var, unit, Date.year, Date.month, Date.day, Hour))
                output_name_min = output_folder
                output_name_max = output_folder
                url_start = r"https://opendap.nccs.nasa.gov/dods/GEOS-5/fp/0.25_deg/assim/inst3_2d_asm_Nx."

            if TimeStep == "daily":
                if Var in ['t2m', 'u2m', 'v2m', 'qv2m', 'tqv', 'ps', 'slp', 't10m', 'v10m', 'u10m', 'v50m', 'u50m',
                           'ts']:
                    IDz_start = int(((Date - pd.Timestamp("2017-12-01")).days) * 8)
                    IDz_end = IDz_start + 7
                    url_start = r"https://opendap.nccs.nasa.gov/dods/GEOS-5/fp/0.25_deg/assim/inst3_2d_asm_Nx."
                    size_z = 8
                else:
                    IDz_start = int(((Date - pd.Timestamp("2017-12-01")).days) * 24)
                    IDz_end = IDz_start + 23
                    url_start = r"https://opendap.nccs.nasa.gov/dods/GEOS-5/fp/0.25_deg/assim/tavg1_2d_rad_Nx."
                    size_z = 24

                if "mean" in data_type:
                    output_name = os.path.join(output_folder, "%s_GEOS_%s_daily_%d.%02d.%02d.tif" % (
                        Var, unit, Date.year, Date.month, Date.day))
                else:
                    output_name = output_folder
                if "min" in data_type:
                    output_name_min = os.path.join(output_folder, "min", "%smin_GEOS_%s_daily_%d.%02d.%02d.tif" % (
                        Var, unit, Date.year, Date.month, Date.day))
                else:
                    output_name_min = output_folder
                if "max" in data_type:
                    output_name_max = os.path.join(output_folder, "max", "%smax_GEOS_%s_daily_%d.%02d.%02d.tif" % (
                        Var, unit, Date.year, Date.month, Date.day))
                else:
                    output_name_max = output_folder

            if not (os.path.exists(output_name) and os.path.exists(output_name_min) and os.path.exists(
                    output_name_max)):

                # define total url
                url_GEOS = url_start + 'ascii?%s[%s:1:%s][%s:1:%s][%s:1:%s]' % (
                    Var, IDz_start, IDz_end, int(IDy[0]), int(IDy[1]), int(IDx[0]), int(IDx[1]))

                # Reset the begin parameters for downloading
                downloaded = 0
                N = 0

                # if not downloaded try to download file
                while downloaded == 0:
                    try:

                        # download data (first save as text file)
                        pathtext = os.path.join(output_folder, 'temp%s.txt' % str(IDz_start))

                        # Download the data
                        da_logger.debug(url_GEOS)
                        urllib.request.urlretrieve(url_GEOS, filename=pathtext)

                        # Reshape data
                        datashape = [int(IDy[1] - IDy[0] + 1), int(IDx[1] - IDx[0] + 1)]
                        data_start = np.genfromtxt(pathtext, dtype=float, skip_header=1, skip_footer=6, delimiter=',')
                        data_list = np.asarray(data_start[:, 1:])
                        if TimeStep == "daily":
                            data_end = np.resize(data_list, (size_z, datashape[0], datashape[1]))
                        if TimeStep == "hourly" or TimeStep == "three_hourly":
                            data_end = np.resize(data_list, (datashape[0], datashape[1]))
                        os.remove(pathtext)

                        # Set no data value
                        data_end[data_end > 1000000] = np.nan

                        if TimeStep == "daily":

                            if "min" in data_type:
                                data_min = np.nanmin(data_end, 0)
                            if "max" in data_type:
                                data_max = np.nanmax(data_end, 0)
                            if "mean" in data_type:
                                if types == "state":
                                    data_end = np.nanmean(data_end, 0)
                                else:
                                    data_end = np.nansum(data_end, 0)

                                    # Add the VarFactor
                        if VarInfo.factors[Var] < 0:
                            if "mean" in data_type:
                                data_end[data_end != -9999] = data_end[data_end != -9999] + VarInfo.factors[Var]
                                data_end[data_end < -9999] = -9999
                                data_end = np.flipud(data_end)
                            if "min" in data_type:
                                data_min[data_min != -9999] = data_min[data_min != -9999] + VarInfo.factors[Var]
                                data_min[data_min < -9999] = -9999
                                data_min = np.flipud(data_min)
                            if "max" in data_type:
                                data_max[data_max != -9999] = data_max[data_max != -9999] + VarInfo.factors[Var]
                                data_max[data_max < -9999] = -9999
                                data_max = np.flipud(data_max)

                        else:
                            if "mean" in data_type:
                                data_end[data_end != -9999] = data_end[data_end != -9999] * VarInfo.factors[Var]
                                data_end[data_end < -9999] = -9999
                                data_end = np.flipud(data_end)
                            if "min" in data_type:
                                data_min[data_min != -9999] = data_min[data_min != -9999] * VarInfo.factors[Var]
                                data_min[data_min < -9999] = -9999
                                data_min = np.flipud(data_min)
                            if "max" in data_type:
                                data_max[data_max != -9999] = data_max[data_max != -9999] * VarInfo.factors[Var]
                                data_max[data_max < -9999] = -9999
                                data_max = np.flipud(data_max)

                        if "mean" in data_type:
                            GDALRasterIO.write_geotiff(output_name, data_end, wgs_crs, geo_out)
                            # DC.Save_as_tiff(output_name, data_end, geo_out, proj)
                        if "min" in data_type:
                            GDALRasterIO.write_geotiff(output_name, data_min, wgs_crs, geo_out)
                            # DC.Save_as_tiff(output_name_min, data_min, geo_out, proj)
                        if "max" in data_type:
                            GDALRasterIO.write_geotiff(output_name, data_max, wgs_crs, geo_out)
                            # DC.Save_as_tiff(output_name_max, data_max, geo_out, proj)

                        # Download was succesfull
                        downloaded = 1

                        # If download was not succesfull
                    except Exception as e:
                        da_logger.error(str(e))
                        # Try another time
                        N = N + 1

                        # Stop trying after 10 times
                        if N == 10:
                            da_logger.critical('Data from ' + Date.strftime('%Y-%m-%d') + ' is not available')
                            downloaded = 1

            if Waitbar == 1:
                amount += 1
                WaitBarConsole.print_wait_bar(amount, total_amount, prefix='Progress:', suffix='Complete', length=50)
