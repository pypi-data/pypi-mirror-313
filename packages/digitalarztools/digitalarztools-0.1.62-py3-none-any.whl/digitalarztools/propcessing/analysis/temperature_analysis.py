import time
import numpy as np
import numpy.polynomial.polynomial as poly
from tqdm import tqdm

from digitalarztools.raster.rio_raster import RioRaster
from digitalarztools.utils.logger import da_logger


class TemperatureAnalysis:
    @staticmethod
    def Thermal_Sharpening(surface_temp_up: np.ndarray, NDVI_up: np.ndarray, NDVI: np.ndarray, Box, down_raster: RioRaster, up_raster: RioRaster, watermask=None):
        # Creating arrays to store the coefficients
        """
        upscale to fastent the process like from 30 to 90meter then downscaling
        :param surface_temp_up:  surface temperature using Landsat  or sentinel thermal bands RioLandsat.calculate_surface_temperature
        :param NDVI_up: ndvi upscaled
        :param NDVI: ndvi downscaled
        :param Box:
        :param down_raster: downscaling raster
        :param up_raster:  upscaling raster
        :param watermask:
        :return:
        """
        s_start_time = time.time()
        coef_a = np.zeros((len(surface_temp_up), len(surface_temp_up[1])))
        coef_b = np.zeros((len(surface_temp_up), len(surface_temp_up[1])))
        coef_c = np.zeros((len(surface_temp_up), len(surface_temp_up[1])))

        # Fit a second polynominal fit to the NDVI and Thermal data and save the coefficients for each pixel
        # NOW USING FOR LOOPS PROBABLY NOT THE FASTEST METHOD
        # for i in range(0, len(surface_temp_up)):
        #     for j in range(0, len(surface_temp_up[1])):
        m, n = surface_temp_up.shape
        x = np.arange(m * n)
        # with tqdm(total=len(x), desc="Calculating Thermal Sharpening", ncols=100) as pbar:

        for index in tqdm(x, desc="Calculating Thermal Sharpening", ncols=100):

            i = int(index / n)
            j = int(index % n)
            if not np.isnan(np.sum(surface_temp_up[i, j])) and not np.isnan(np.sum(NDVI_up[i, j])):
                x_data = NDVI_up[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))][
                    np.logical_and(np.logical_not(np.isnan(NDVI_up[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))])),
                                   np.logical_not(np.isnan(surface_temp_up[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))])))]
                y_data = surface_temp_up[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))][
                    np.logical_and(np.logical_not(np.isnan(NDVI_up[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))])),
                                   np.logical_not(np.isnan(surface_temp_up[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))])))]
                if watermask is not None:
                    wm_data = watermask[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))][
                        np.logical_and(np.logical_not(np.isnan(NDVI_up[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))])),
                                       np.logical_not(np.isnan(surface_temp_up[int(np.maximum(0, i - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up), i + (Box - 1) / 2 + 1)), int(np.maximum(0, j - (Box - 1) / 2)):int(np.minimum(len(surface_temp_up[1]), j + (Box - 1) / 2 + 1))])))]
                    x_data = x_data[wm_data == 0]
                    y_data = y_data[wm_data == 0]
                # x_data[~np.isnan(x_data)]
                # y_data[~np.isnan(y_data)]
                if len(x_data) > 6:
                    coefs = poly.polyfit(x_data, y_data, 2)
                    coef_a[i, j] = coefs[2]
                    coef_b[i, j] = coefs[1]
                    coef_c[i, j] = coefs[0]
                else:
                    coef_a[i, j] = np.nan
                    coef_b[i, j] = np.nan
                    coef_c[i, j] = np.nan
            else:
                coef_a[i, j] = np.nan
                coef_b[i, j] = np.nan
                coef_c[i, j] = np.nan
            # return CoefA, CoefB, CoefC

        # poly_fit_coef_fn = lambda i: [poly_fit_coef(i, j) for j in np.arange(len(surface_temp_up[i]))]
        # vec_poly_coef = np.vectorize(poly_fit_coef_fn)
        # i = np.arange(len(surface_temp_up))
        # vec_poly_coef(i)
        # x = np.arange(m * n)
        # with tqdm(total=len(x), desc="Calculating Thermal Sharpening", ncols=100) as pbar:
        # vec_poly_coef = np.vectorize(poly_fit_coefficient)
        # vec_poly_coef(x)
        s_end_time = time.time()
        da_logger.info(f"Time took in calculating Thermal Sharpening {(s_end_time - s_start_time) / 60} min")

        coef_a_raster = up_raster.rio_raster_from_array(coef_a)
        coef_b_raster = up_raster.rio_raster_from_array(coef_b)
        coef_c_raster = up_raster.rio_raster_from_array(coef_c)

        coef_a_raster.make_coincident_with(down_raster)
        coef_b_raster.make_coincident_with(down_raster)
        coef_c_raster.make_coincident_with(down_raster)

        coef_a = coef_a_raster.get_data_array(1)
        coef_b = coef_b_raster.get_data_array(1)
        coef_c = coef_c_raster.get_data_array(1)

        # Calculate the surface temperature based on the fitted coefficents and NDVI
        temp_surface_sharpened = coef_a * NDVI ** 2 + coef_b * NDVI + coef_c
        temp_surface_sharpened[temp_surface_sharpened < 250] = np.nan
        temp_surface_sharpened[temp_surface_sharpened > 400] = np.nan

        return temp_surface_sharpened

    @staticmethod
    def calculate_air_density(air_pressure, surface_temperature):
        """
        Calculate air density from air pressure and surfae temperature sharppend
        :param air_pressure:
        :param surface_temperature: Thermal sharpened Surface temperature using TemperatureAnalysis.Thermal_Sharpening
        :return:
        """
        air_dens = 1000 * air_pressure / (1.01 * surface_temperature * 287)
        return air_dens

    @staticmethod
    def correct_surface_temp_slope(surface_temperature, air_dens, dr, transmissivity_corrected, cos_zn, sun_elevation, QC_Map):
        """
         Correct Temperature based on air column above the ground
          Function to correct the surface temperature based on the DEM map
        :param surface_temperature: Thermal sharpened Surface temperature using TemperatureAnalysis.Thermal_Sharpening
        :param air_dens:  cls.calculate_air_density
        :param dr:  inverse relative distance Earth-Sun using RioLandsat.calculate_earth_sun_inverse_relative_distance
        :param transmissivity_corrected: Transmissivity instantaneous corrected
        :param cos_zn:  cos zenith sun angle
        :param sun_elevation: Sun eleavation from Landsat metadata
        :param QC_Map: Quality Control Map
            QC_Map = VegitationAnalysis.calculate_ndvi_qc_map(ndvi)
            Tot_Masks = cloud_mask + snow_mask + shadow_mask + QC_Map
            QC_Map[Tot_Masks > 0] = 1
        :return:
        """
        # constants:

        Gsc = 1367  # Solar constant (W / m2)
        deg2rad = np.pi / 180
        cos_zenith_flat = np.cos((90 - sun_elevation) * deg2rad)

        ts_corr = (surface_temperature + (Gsc * dr * transmissivity_corrected * cos_zn -
                                          Gsc * dr * transmissivity_corrected * cos_zenith_flat) / (air_dens * 1004 * 0.050))  # 0.05 dikte van de lucht laag boven grond
        # (Temp_corr - (Gsc * dr * Transm_corr * cos_zn -
        #          Gsc * dr * Transm_corr * cos_zenith_flat) / (air_dens * 1004 * 0.050))
        ts_corr[QC_Map == 1] = np.nan
        ts_corr[ts_corr == 0] = np.nan
        ts_corr[ts_corr < 250] = np.nan
        ts_corr[ts_corr > 350] = np.nan

        return ts_corr

    @staticmethod
    def correct_surface_temp_lapse_rate(ts_corr, dem_data, ndvi, slope, water_mask, QC_Map, QC_temp=None):
        """
        Correct Temperature to one DEM height
        :param ts_corr: Correct_Surface_Temp_slope
        :param dem_data: Elevation model
        :param ndvi: VegitationAnalysis.calculate_ndvi
        :param slope: DemAnalysis.calculate_slope
        :param water_mask: WaterAnalysis.calculate_water_mask
        :param QC_Map: Quality Control Map
            QC_Map = VegitationAnalysis.calculate_ndvi_qc_map(ndvi)
            Tot_Masks = cloud_mask + snow_mask + shadow_mask + QC_Map
            QC_Map[Tot_Masks > 0] = 1
        :param QC_temp:
        :return:
        """

        if np.all(QC_temp) == None:
            QC_temp = np.ones(ts_corr.shape)

        # Indicators to define the pixels selected for the lapse rate
        NDVI_flatten = ndvi.flatten()
        water_mask_flatten = water_mask.flatten()
        DEM_flatten = dem_data.flatten()
        slope_flatten = slope.flatten()
        ts_corr_flatten = ts_corr.flatten()
        QC_temp_flatten = QC_temp.flatten()

        ts_corr_flatten = ts_corr_flatten[np.logical_and.reduce((slope_flatten <= 1., DEM_flatten >= 0, NDVI_flatten <= 0.2, water_mask_flatten == 0., QC_temp_flatten == 1))]
        DEM_array_flatten = DEM_flatten[np.logical_and.reduce((slope_flatten <= 1., DEM_flatten >= 0, NDVI_flatten <= 0.2, water_mask_flatten == 0., QC_temp_flatten == 1))]

        DEM_array_flatten = DEM_array_flatten[~np.isnan(ts_corr_flatten)]
        ts_corr_flatten = ts_corr_flatten[~np.isnan(ts_corr_flatten)]

        if len(ts_corr_flatten) > 100:

            # Find the range of DEM
            DEMmin = np.nanmin(DEM_array_flatten)
            DEMmax = np.nanmax(DEM_array_flatten)
            DEMspace = round((DEMmax - DEMmin) / 100)

            # Define steps for temperature
            DEM_spaces = np.linspace(int(DEMmin), int(DEMmax), int(DEMspace))

            if len(DEM_spaces) > 1:

                Temps = np.zeros(len(DEM_spaces) - 1)
                Tot_array = np.vstack([DEM_array_flatten, ts_corr_flatten])

                # Calculate Temperature for the different buckets and remove outliers
                for i in range(1, len(DEM_spaces)):
                    # Define the bucket range for this step
                    min_bucket = DEM_spaces[i - 1]
                    max_bucket = DEM_spaces[i]

                    # Select all the temperatures for this bucket
                    Select_temp = Tot_array[:, np.logical_and(Tot_array[0, :] < max_bucket, Tot_array[0, :] >= min_bucket)]
                    Temp_values = Select_temp[1, :]

                    # Remove outliers from bucket
                    Temp_std = np.nanstd(Select_temp[1, :])
                    Temp_avg = np.nanmean(Select_temp[1, :])
                    Temp_good = Temp_values[np.logical_and(Temp_values <= (Temp_avg + Temp_std), Temp_values >= (Temp_avg - Temp_std))]

                    # Define temperature for that bucket
                    Temps[i - 1] = np.nanmean(Temp_good)

                x_values = (DEM_spaces[1:] + DEM_spaces[:-1]) / 2
                y_values = Temps
                x_values = x_values[~np.isnan(y_values)]
                y_values = y_values[~np.isnan(y_values)]
            else:
                y_values = []

            # Calculate lapse rate
            if len(y_values) > 0:
                Temp_lapse = y_values - y_values[0]
                x_values = np.append(DEMmin, x_values)
                Temp_lapse = np.append(Temp_lapse[0], Temp_lapse)
                x_values = np.append(x_values, DEMmax)
                Temp_lapse = np.append(Temp_lapse, Temp_lapse[-1])

                z = np.polyfit(x_values, Temp_lapse, 10)
                f = np.poly1d(z)
                Temp_array_lapse_rate = f(dem_data)
                Temp_array_lapse_rate = np.where(QC_temp == 1, Temp_array_lapse_rate, (dem_data - DEMmin) * -0.0065)
                ts_dem = ts_corr - Temp_array_lapse_rate

            else:
                ts_dem = ts_corr + 0.0065 * (dem_data - DEMmin)

        else:
            DEMmin = np.nanmin(np.nanpercentile(dem_data, 0.05))
            ts_dem = ts_corr + 0.0065 * (dem_data - DEMmin)

        # Remove bad pixels
        ts_dem[QC_Map == 1] = np.nan
        ts_dem[ts_dem == 0] = np.nan
        ts_dem[ts_dem < 273] = np.nan
        ts_dem[ts_dem > 350] = np.nan

        return ts_dem

    @staticmethod
    def stress_temperature(t_air_24, t_opt=25.0, t_min=0.0, t_max=50.0):
        r"""
        Computes the stress for plants when it is too cold or hot

         math ::
            f=\frac{T_{max}-T_{opt}}{T_{opt}-T_{min}}

        math ::
            s_{T}=\frac{\left(T_{a}-T_{min}\right)\left(T_{max}-T_{a}\right)^{f}}
                {\left(T_{opt}-T_{min}\right)\left(T_{max}-T_{opt}\right)^{f}}

        Parameters
        ----------
        t_air_24 : np.ndarray or float
            daily air temperature
            :math:`T_{a}`
            [C]
        t_opt : np.ndarray or float
            optimum air temperature for plant growth
            :math:`T_{opt}`
            [C]
        t_min : np.ndarray or float
            minimum air temperature for plant growth
            :math:`T_{min}`
            [C]
        t_max : np.ndarray or float
            maximum air temperature for plant growth
            :math:`T_{max}`
            [C]

        Returns
        -------
        stress_temp : np.ndarray or float
            stress factor for air temperature
            :math:`S_{T}`
            [-]

        Examples
        --------

        TemperatureAnalysis.stress_temperature(15)
        0.83999999999999997
        TemperatureAnalysis.stress_temperature(15, t_opt =20)
        0.9451080185178129
        TemperatureAnalysis.stress_temperature(15, t_opt =20, t_min=10)
        0.79398148148148151
        TemperatureAnalysis.stress_temperature(15, t_opt =20, t_min=10, t_max=30)
        0.75

        """
        # f = float((t_max - t_opt))/float((t_opt - t_min))
        f = (t_max - t_opt) / (t_opt - t_min)
        x = (t_air_24 - t_min) * (t_max - t_air_24) ** f
        y = (t_opt - t_min) * (t_max - t_opt) ** f

        stress = x / y
        stress = np.clip(stress, 0, 1)

        return stress
