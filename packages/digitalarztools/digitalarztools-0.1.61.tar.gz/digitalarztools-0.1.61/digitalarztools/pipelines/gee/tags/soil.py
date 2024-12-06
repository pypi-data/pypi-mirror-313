import ee
import numpy as np
from matplotlib import pyplot as plt

from digitalarztools.pipelines.gee.core.image import GEEImage


class Soil:
    sand: ee.Image
    clay: ee.Image
    orgc: ee.Image
    def __init__(self):
        # Image associated with the sand content.
        self.sand = self.get_openlandmap_soil_prop("sand")

        # Image associated with the clay content.
        self.clay = self.get_openlandmap_soil_prop("clay")

        # Image associated with the organic carbon content.
        self.orgc = self.get_openlandmap_soil_prop("orgc")

    @staticmethod
    def get_openlandmap_soil_prop(param) -> ee.Image:
        """
        https://developers.google.com/earth-engine/datasets/catalog/OpenLandMap_SOL_SOL_CLAY-WFRACTION_USDA-3A1A1A_M_v02#description
        This function returns soil properties image
        param (str): must be one of:
            "sand"     - Sand fraction
            "clay"     - Clay fraction
            "orgc"     - Organic Carbon fraction
        """
        if param == "sand":  # Sand fraction [%w]
            snippet = "OpenLandMap/SOL/SOL_SAND-WFRACTION_USDA-3A1A1A_M/v02"
            # Define the scale factor in accordance with the dataset description.
            scale_factor = 1 * 0.01

        elif param == "clay":  # Clay fraction [%w]
            snippet = "OpenLandMap/SOL/SOL_CLAY-WFRACTION_USDA-3A1A1A_M/v02"
            # Define the scale factor in accordance with the dataset description.
            scale_factor = 1 * 0.01

        elif param == "orgc":  # Organic Carbon fraction [g/kg]
            snippet = "OpenLandMap/SOL/SOL_ORGANIC-CARBON_USDA-6A1C_M/v02"
            # Define the scale factor in accordance with the dataset description.
            scale_factor = 5 * 0.001  # to get kg/kg
        else:
            return print("error")

        # Apply the scale factor to the ee.Image.
        dataset = ee.Image(snippet).multiply(scale_factor)

        return dataset

    def get_olm_depth(self):
        return [0, 10, 30, 60, 100, 200]

    def get_olm_bands(self):
        # Soil depths [in cm] where we have data.
        olm_depths = self.get_olm_depth()

        # Names of bands associated with reference depths.
        olm_bands = ["b" + str(sd) for sd in olm_depths]
        return olm_bands

    def local_profile(self, dataset: ee.Image, poi, buffer):
        olm_bands = self.get_olm_bands()
        # dataset =  img.image
        # Get properties at the location of interest and transfer to client-side.
        prop = dataset.sample(poi, buffer).select(olm_bands).getInfo()

        # Selection of the features/properties of interest.
        profile = prop["features"][0]["properties"]

        # Re-shaping of the dict.
        profile = {key: round(val, 3) for key, val in profile.items()}

        return profile

    def plot_profile(self, profiles: list):
        """
        :param profile: list of object having
        [{
            "profile": profile_sand,
            "label": "Sand",
            "color": "#ecebbd",
        },{
            "profile": profile_clay,
            "label": "Sand",
            "color": "#6f6c5d",
        }, {
            "profile": profile_orgc,
            "label": "Organic Carbon",
            "color": "black",
        }]
        :return:
        """
        olm_bands = self.get_olm_bands()
        # Data visualization in the form of a bar plot.
        fig, ax = plt.subplots(figsize=(15, 6))
        ax.axes.get_yaxis().set_visible(False)

        # Definition of label locations.
        x = np.arange(len(olm_bands))

        # Definition of the bar width.
        width = 0.25
        rects = []
        # Bar plot representing the sand content profile.
        for profile in profiles:
            rects.append(ax.bar(
                x - width,
                [round(100 * profile['profile'][b], 2) for b in olm_bands],
                width,
                label=profile['label'],
                color=profile['color'],
            ))

        # Definition of a function to attach a label to each bar.
        def autolabel_soil_prop(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate(
                    "{}".format(height) + "%",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset.
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                )

        # Application of the function to each barplot.
        for index in range(len(rects)):
            autolabel_soil_prop(rects[index])

        # Title of the plot.
        ax.set_title("Properties of the soil at different depths (mass content)", fontsize=14)

        # Properties of x/y labels and ticks.
        ax.set_xticks(x)
        x_labels = [str(d) + " cm" for d in self.get_olm_depth()]
        ax.set_xticklabels(x_labels, rotation=45, fontsize=10)

        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["top"].set_visible(False)

        # Shrink current axis's height by 10% on the bottom.
        box = ax.get_position()
        ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])

        # Add a legend below current axis.
        ax.legend(
            loc="upper center", bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=True, ncol=3
        )

        plt.show()

    def get_organic_matter(self):
        # Conversion of organic carbon content into organic matter content.
        return self.orgc.multiply(1.724)


    # def get_hydraulic_properties_wp_fc(self, poi, scale):

    def get_field_capacity(self, orgm):
        """
        Expression to calculate hydraulic properties field capacity (fc)
        OC = organic content
        S = sand
        C = clay
        theeta 33T: T33ti= -0.251 * S + 0.195 * C + 0.011 * OM +0.006 * (S * OM) - 0.027 * (C * OM)+ 0.452 * (S * C) + 0.299
        Field capaicty: fci = T33ti + (1.283 * T33ti * T33ti - 0.374 * T33ti - 0.015)
        :param orgm: organic matter self.get_organic_matter()
        :return:
        """
        # Initialization of two constant images for wilting point and field capacity.
        field_capacity = ee.Image(0)

        # Calculation for each standard depth using a loop.
        olm_bands = self.get_olm_bands()
        for key in olm_bands:
            # Getting sand, clay and organic matter at the appropriate depth.
            si = self.sand.select(key)
            ci = self.clay.select(key)
            oi = orgm.select(key)
            # Same process for the calculation of the field capacity.
            # The parameter theta_33t is needed for the given depth.
            theta_33ti = (
                ee.Image(0).expression(
                    "-0.251 * S + 0.195 * C + 0.011 * OM +0.006 * (S * OM) - 0.027 * (C * OM)+\
                0.452 * (S * C) + 0.299", {"S": si, "C": ci, "OM": oi},
                ).rename("T33ti")
            )

            # Final expression for the field capacity of the soil.
            fci = theta_33ti.expression(
                "T33ti + (1.283 * T33ti * T33ti - 0.374 * T33ti - 0.015)",
                {"T33ti": theta_33ti.select("T33ti")},
            )

            # Add a new band of the global field capacity ee.Image.
            field_capacity = field_capacity.addBands(fci.rename(key).float())

        return field_capacity
    def get_wilting_point(self,orgm):
        """
        Expression to calculate hydraulic properties wilting point (wp)
        OC = organic content
        S = sand
        C = clay
        organic matter: OM = 1.724 * OC
        theeta 1500T: T1500ti=  "-0.024 * S + 0.487 * C + 0.006 * OM + 0.005 * (S * OM)- 0.013 * (C * OM) + 0.068 * (S * C) + 0.031"
        Welting point: wpi = T1500ti + ( 0.14 * T1500ti - 0.002)
        """
        # Initialization of two constant images for wilting point and field capacity.
        wilting_point = ee.Image(0)

        # Calculation for each standard depth using a loop.
        olm_bands = self.get_olm_bands()
        for key in olm_bands:
            # Getting sand, clay and organic matter at the appropriate depth.
            si = self.sand.select(key)
            ci = self.clay.select(key)
            oi = orgm.select(key)

            # Calculation of the wilting point.
            # The theta_1500t parameter is needed for the given depth.
            theta_1500ti = (
                ee.Image(0).expression(
                    "-0.024 * S + 0.487 * C + 0.006 * OM + 0.005 * (S * OM)\
                - 0.013 * (C * OM) + 0.068 * (S * C) + 0.031", {"S": si, "C": ci, "OM": oi},
                ).rename("T1500ti")
            )

            # Final expression for the wilting point.
            wpi = theta_1500ti.expression(
                "T1500ti + ( 0.14 * T1500ti - 0.002)", {"T1500ti": theta_1500ti}
            ).rename("wpi")

            # Add as a new band of the global wilting point ee.Image.
            # Do not forget to cast the type with float().
            wilting_point = wilting_point.addBands(wpi.rename(key).float())

        return wilting_point

