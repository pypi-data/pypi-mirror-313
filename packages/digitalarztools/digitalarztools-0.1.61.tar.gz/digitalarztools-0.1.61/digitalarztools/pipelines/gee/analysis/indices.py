class GEEIndices:
    @staticmethod
    def add_ndvi(image):
        ndvi = image.normalizedDifference(['B8', 'B4']).rename('NDVI');
        return image.addBands(ndvi)

    @staticmethod
    def get_ndvi(image, ndvi_name='ndvi'):
        return image.normalizedDifference(['B8', 'B4']).rename(ndvi_name);

    @staticmethod
    def add_evi(image):
        evi = image.expression("2.5 * ((nir-red)/(nir + 6*red -7.5*blue + 1))",
                               {
                                   "nir": image.select("B8"),
                                   "red": image.select("B4"),
                                   "blue": image.select("B2")
                               }).rename('EVI')
        return image.addBands(evi)

    @staticmethod
    def add_ndwi(image, band_1='B3', band_2='B8'):
        ndwi = image.normalizedDifference([band_1, band_2]).rename('NDWI');
        return image.addBands(ndwi)

    @staticmethod
    def add_ndbi(image):
        ndbi = image.normalizedDifference(['B11', 'B8']).rename('NDBI')
        return image.addBands(ndbi)
