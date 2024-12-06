from digitalarztools.pipelines.gee.core.auth import GEEAuth
from digitalarztools.pipelines.gee.core.image import GEEImage
from digitalarztools.pipelines.gee.core.region import GEERegion


class Hydro:
    @staticmethod
    def merit_data_using_gee(gee_auth: GEEAuth, region: GEERegion, output_fp:  str, band_name='wat'):
        """
        https://developers.google.com/earth-engine/datasets/catalog/MERIT_Hydro_v1_0_1
        @:param gee_auth:
        @:param region
        @:param output_fp:
        @:param band_name: choices elv, dir, wth, wat, upa, upg, hnd, viswth for detail check above url
        """
        if gee_auth.is_initialized:
            gee_img = GEEImage.get_image_by_tag('MERIT/Hydro/v1_0_1')
            gee_img.get_band(band_name, in_place=True)
            gee_img.download_image(output_fp, img_region=region, scale=100, bit_depth=8)