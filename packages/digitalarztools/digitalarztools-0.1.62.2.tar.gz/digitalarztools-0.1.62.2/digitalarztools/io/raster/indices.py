from fractions import Fraction

from sklearn.preprocessing import MinMaxScaler


class IndicesCalc:
    # red: np.ndarray
    # green: np.ndarray
    # blue: np.ndarray
    # nir: np.ndarray
    #
    # def __init__(self, red, green, blue, nir):
    #     self.red = red
    #     self.green = green
    #     self.blue = blue
    #     self.nir = nir
    # @staticmethod
    # def WDRVIndices(nir, red):
    #     a = 0.15
    #     wdrvi = (a * nir - red) / (a * nir + red)
    #     return wdrvi

    # @staticmethod
    # def NPCRIndices(red, blue):
    #     npcri = (red - blue) / (red + blue)
    #     return npcri

    @staticmethod
    def NDWIndices(grean, nir):
        ndwi = (grean - nir) / (grean + nir + 1e-5)
        return ndwi

    @staticmethod
    def NDVIndices(nir, red):
        ndvi = (nir - red) / (nir + red + 1e-5)
        return ndvi

    @staticmethod
    def ShadowIndices(red, green, blue):
        expo = Fraction('1/3')
        si = (((1 - red) * (1 - green) * (1 - blue)) ** expo)
        return si

    @staticmethod
    def normalize(arr, range: tuple = (0, 255)):
        scaler = MinMaxScaler(feature_range=range)
        scaler = scaler.fit(arr)
        arr_norm = scaler.transform(arr)
        # Checking reconstruction
        # arr_norm = scaler.inverse_transform(arr_norm)

        return arr_norm

    # def bandstack(self):
    #     stack = np.dstack((self.red, self.green, self.blue))
    #     return stack

    # wdrvi = WDRVIcalc(nir, red)
    #
    # # npcri = NPCRIcalc(red,blue)
    #
    # ndi = NDVIcalc(nir, red)
    #
    # si = SIcalc(red, green, blue)
    #
    # print("wdrvi: ", wdrvi.min(), wdrvi.max(), "ndi: ", ndi.min(), ndi.max(), "si: ", si.min(), si.max())
    #
    # wdrvi = norm(wdrvi)
    # ndi = norm(ndi)
    # si = norm(si)

    # index_stack = np.dstack((wdrvi, ndi, si))

    # return index_stack
