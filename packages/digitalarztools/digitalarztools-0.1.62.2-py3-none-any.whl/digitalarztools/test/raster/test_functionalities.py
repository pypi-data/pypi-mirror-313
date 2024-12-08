import pyproj


tif_file = '../../../media/Adyala Land 2D Svy_dsm.tif'


def test_reproject():
    # prj_file = '../../../media/Adyala Land 2D Svy_dsm.prj'
    # img_des = '../../../media/Adyala_dsm_utm.tif'
    # crs = FileIO.read_prj_file(prj_file)
    # raster = RioRaster(tif_file)
    # raster.set_crs(crs)
    # crs = pyproj.CRS.from_epsg('32643')
    # raster.reproject_raster(crs)
    # print(raster.get_crs())
    # raster.save_to_file(img_des)
    pass

def test_edge_enhancement():
    # raster = RioRaster(tif_file)
    # for tile in raster.get_tiles(1000,1000):

    # data_arr = raster.get_data_array(1, convert_no_data_2_nan=True)
    # plt.imshow(data_arr)
    # plt.show()
    pass


if __name__ == '__main__':
    test_reproject()
    # test_edge_enhancement()
