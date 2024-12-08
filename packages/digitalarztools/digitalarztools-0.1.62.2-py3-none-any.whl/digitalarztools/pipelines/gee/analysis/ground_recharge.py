import ee
import pandas as pd
from matplotlib import pyplot as plt

from digitalarztools.pipelines.gee.core.image_collection import GEEImageCollection
from digitalarztools.pipelines.gee.tags.soil import Soil


class GroundWaterRecharge():
    """
    Implementation of the TM procedure
    https://developers.google.com/earth-engine/tutorials/community/groundwater-recharge-estimation#groundwater_recharge_map_of_france
    Some additional definitions are needed to formalize the Thornthwaite-Mather procedure. The following definitions are given in accordance with Allen et al. (1998) (the document can be downloaded here):
    http://www.climasouth.eu/sites/default/files/FAO%2056.pdf
    T
    AW = 1000 x (Tfc -Twp) x Zr
    where:

    TWA: the total available soil water in the root zone [mm],
    Tfc: the water content at the field capacity [m3 m-3],
    Twp: the water content at wilting point [m3 m-3],
    Zr: the rooting depth [m],
    """
    in_field_capacity: ee.ImageCollection
    in_wilting_point: ee.ImageCollection
    in_meteo: ee.ImageCollection  # meterological surface consist of precipitation and ET
    out_recharge_collection: GEEImageCollection

    def __init__(self, field_capacity, wilting_point, meteo,
                 zr_val=0.5, p_val=0.5):
        """
        According to this global dataset, the effective rooting depth
        around our region of interest (France) can reasonably assumed to zr=0.5
    .   Additionally, the parameter p is also assumed constant and equal to and p=0.5
        which is in line with common values described in Table 22 of Allen et al. (1998).
        :param field_capacity
        :param wilting_point
        :param meteo meterological surface consist of precipitation and evpo-transpiration
        :param zr_val
        :param p_val
        :return:
        """
        self.in_field_capacity = field_capacity
        self.in_wilting_point = wilting_point
        self.in_meteo = meteo
        self.zr = ee.Image(zr_val)
        self.p = ee.Image(p_val)

    def olm_prop_mean(self, olm_image, band_output_name):
        """
        This function calculates an averaged value of
        soil properties between reference depths.
        :param: open land map image
        :band_output_name:
        """
        mean_image = olm_image.expression(
            "(b0 + b10 + b30 + b60 + b100 + b200) / 6",
            {
                "b0": olm_image.select("b0"),
                "b10": olm_image.select("b10"),
                "b30": olm_image.select("b30"),
                "b60": olm_image.select("b60"),
                "b100": olm_image.select("b100"),
                "b200": olm_image.select("b200"),
            },
        ).rename(band_output_name)

        return mean_image

    def calculate_theoretical_available_water(self):
        # Apply the function to field capacity and wilting point.
        fcm = self.olm_prop_mean(self.in_field_capacity, "fc_mean")
        wpm = self.olm_prop_mean(self.in_wilting_point, "wp_mean")

        # Calculate the theoretical available water.
        taw = (
            (fcm.select("fc_mean").subtract(wpm.select("wp_mean"))).multiply(1000).multiply(self.zr)
        )
        return taw

    def calculate_stored_water_at_field_capacity(self, taw):
        # Calculate the stored water at the field capacity.
        stfc = taw.multiply(self.p)
        return stfc

    def initialize_surfaces(self, time0, stfc):
        """
        :param time0: start time of each surface
        :param stfc: stored water at field capacity
        :return:
        """
        # Initialize all bands describing the hydric state of the soil.
        # Do not forget to cast the type of the data with a .float().
        # Initial recharge.
        initial_rech = ee.Image(0).set("system:time_start", time0).select([0], ["rech"]).float()

        # Initialization of APWL.
        initial_apwl = ee.Image(0).set("system:time_start", time0).select([0], ["apwl"]).float()

        # Initialization of ST.
        initial_st = stfc.set("system:time_start", time0).select([0], ["st"]).float()

        # Initialization of precipitation.
        initial_pr = ee.Image(0).set("system:time_start", time0).select([0], ["pr"]).float()

        # Initialization of potential evapotranspiration.
        initial_pet = ee.Image(0).set("system:time_start", time0).select([0], ["pet"]).float()

        initial_image = initial_rech.addBands(
            ee.Image([initial_apwl, initial_st, initial_pr, initial_pet])
        )
        return initial_image

    def recharge_calculator_iterator(self, image_list, stfc, fcm, wpm):
        """
        Contains operations made at each iteration.
        :param image_list:
        :param stfc: stored water at field capacity
        :param fcm: field capacity mean
        :param wpm: wilting point mean
        """

        def recharge_calculator(image, image_list):
            """
            Contains operations made at each iteration.
            """
            # Determine the date of the current ee.Image of the collection.
            localdate = image.date().millis()

            # Import previous image stored in the list.
            prev_im = ee.Image(ee.List(image_list).get(-1))

            # Import previous APWL and ST.
            prev_apwl = prev_im.select("apwl")
            prev_st = prev_im.select("st")

            # Import current precipitation and evapotranspiration.
            pr_im = image.select("pr")
            pet_im = image.select("pet")

            # Initialize the new bands associated with recharge, apwl and st.
            # DO NOT FORGET TO CAST THE TYPE WITH .float().
            new_rech = (
                ee.Image(0)
                .set("system:time_start", localdate)
                .select([0], ["rech"])
                .float()
            )

            new_apwl = (
                ee.Image(0)
                .set("system:time_start", localdate)
                .select([0], ["apwl"])
                .float()
            )

            new_st = (
                prev_st.set("system:time_start", localdate).select([0], ["st"]).float()
            )

            # Calculate bands depending on the situation using binary layers with
            # logical operations.

            # CASE 1.
            # Define zone1: the area where PET > P.
            zone1 = pet_im.gt(pr_im)

            # Calculation of APWL in zone 1.
            zone1_apwl = prev_apwl.add(pet_im.subtract(pr_im)).rename("apwl")
            # Implementation of zone 1 values for APWL.
            new_apwl = new_apwl.where(zone1, zone1_apwl)

            # Calculate ST in zone 1.
            zone1_st = prev_st.multiply(
                ee.Image.exp(zone1_apwl.divide(stfc).multiply(-1))
            ).rename("st")
            # Implement ST in zone 1.
            new_st = new_st.where(zone1, zone1_st)

            # CASE 2.
            # Define zone2: the area where PET <= P.
            zone2 = pet_im.lte(pr_im)

            # Calculate ST in zone 2.
            zone2_st = prev_st.add(pr_im).subtract(pet_im).rename("st")
            # Implement ST in zone 2.
            new_st = new_st.where(zone2, zone2_st)

            # CASE 2.1.
            # Define zone21: the area where PET <= P and ST >= STfc.
            zone21 = zone2.And(zone2_st.gte(stfc))

            # Calculate recharge in zone 21.
            zone21_re = zone2_st.subtract(stfc).rename("rech")
            # Implement recharge in zone 21.
            new_rech = new_rech.where(zone21, zone21_re)
            # Implement ST in zone 21.
            new_st = new_st.where(zone21, stfc)

            # CASE 2.2.
            # Define zone 22: the area where PET <= P and ST < STfc.
            zone22 = zone2.And(zone2_st.lt(stfc))

            # Calculate APWL in zone 22.
            zone22_apwl = (
                stfc.multiply(-1).multiply(ee.Image.log(zone2_st.divide(stfc))).rename("apwl")
            )
            # Implement APWL in zone 22.
            new_apwl = new_apwl.where(zone22, zone22_apwl)

            # Create a mask around area where recharge can effectively be calculated.
            # Where we have have PET, P, FCm, WPm (except urban areas, etc.).
            mask = pet_im.gte(0).And(pr_im.gte(0)).And(fcm.gte(0)).And(wpm.gte(0))

            # Apply the mask.
            new_rech = new_rech.updateMask(mask)

            # Add all Bands to our ee.Image.
            new_image = new_rech.addBands(ee.Image([new_apwl, new_st, pr_im, pet_im]))

            # Add the new ee.Image to the ee.List.
            return ee.List(image_list).add(new_image)
        # Iterate the user-supplied function to the meteo collection.

        rech_list = self.in_meteo.iterate(recharge_calculator, image_list)
        return rech_list


    def get_res_df_at_poi(self, poi: ee.Geometry.Point, buffer):
        if self.out_recharge_collection is not None:
            arr = self.out_recharge_collection.img_collection.getRegion(poi, buffer).getInfo()
            rdf = self.out_recharge_collection.info_ee_array_to_df(arr,
                                                                   ["pr", "pet", "apwl", "st", "rech"]).sort_index()
            rdf.head(12)
            return rdf
        else:
            print("recharge collection is not available")
            return pd.DataFrame()

    @staticmethod
    def plot_final_result(rdf: pd.DataFrame):

        # Data visualization in the form of barplots.
        fig, ax = plt.subplots(figsize=(15, 6))

        # Barplot associated with precipitation.
        rdf["pr"].plot(kind="bar", ax=ax, label="precipitation", alpha=0.5)

        # Barplot associated with potential evapotranspiration.
        rdf["pet"].plot(
            kind="bar", ax=ax, label="potential evapotranspiration", color="orange", alpha=0.2
        )

        # Barplot associated with groundwater recharge
        rdf["rech"].plot(kind="bar", ax=ax, label="recharge", color="green", alpha=1)

        # Add a legend.
        ax.legend()

        # Define x/y-labels properties.
        ax.set_ylabel("Intensity [mm]")
        ax.set_xlabel(None)

        # Define the date format and shape of x-labels.
        x_labels = rdf.index.strftime("%m-%Y")
        ax.set_xticklabels(x_labels, rotation=90, fontsize=10)

        plt.show()

    def execute_tm_calculation(self):
        """
        :return:
        """
        """
            step1: calculate available water
        """
        taw = self.calculate_theoretical_available_water()
        stfc = self.calculate_stored_water_at_field_capacity(taw)
        """
        step 2 initialization
        """
        # Define the initial time (time0) according to the start of the collection.
        time0 = self.in_meteo.first().get("system:time_start")
        initial_image = self.initialize_surfaces(time0,stfc)
        # Apply the function to field capacity and wilting point.
        fcm = self.olm_prop_mean(self.in_field_capacity, "fc_mean")
        wpm = self.olm_prop_mean(self.in_wilting_point, "wp_mean")

        """
        step 3: calculate recharges based on cases
        """
        # Iterate the user-supplied function to the meteo collection.
        image_list = ee.List([initial_image])
        # rech_list = self.in_meteo.iterate(self.recharge_calculator, image_list)

        rech_list = self.recharge_calculator_iterator(image_list, stfc, fcm,wpm)
        # Remove the initial image from our list.
        rech_list = ee.List(rech_list).remove(initial_image)

        # Transform the list into an ee.ImageCollection.
        self.out_recharge_collection = GEEImageCollection(ee.ImageCollection(rech_list))
        print("recharge successfully calculate")

    def get_final_recharge_collection(self) -> GEEImageCollection:
        return self.out_recharge_collection