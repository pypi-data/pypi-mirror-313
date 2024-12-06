class RioProbavViirs:
    def __init__(self):
        pass

    @staticmethod
    def get_time_info():
        # # Open the VIIRS_PROBAV_Input sheet
        # ws = workbook['VIIRS_PROBAV_Input']
        #
        # # Extract the name of the thermal and quality VIIRS image from the excel file
        # Name_VIIRS_Image_TB = '%s' % str(ws['B%d' % number].value)
        # Name_VIIRS_Image_QC = '%s' % str(ws['C%d' % number].value)
        #
        # # Extract the name to the PROBA-V image from the excel file
        # Name_PROBAV_Image = '%s' % str(ws['D%d' % number].value)  # Must be a tiff file
        #
        # # UTM Zone of the end results
        # UTM_Zone = float(ws['G%d' % number].value)

        # Get time from the VIIRS dataset name (IMPORTANT TO KEEP THE TEMPLATE OF THE VIIRS NAME CORRECT example: VIIRS_SVIO5_npp_20160601_1103128_e1108532_b23808_c20160601170854581426_noaa_ops.tif npp_viirs_i05_20150701_124752_wgs84_fit.tif)
        # Total_Day_VIIRS = Name_VIIRS_Image_TB.split('_')[3]
        # Total_Time_VIIRS = Name_VIIRS_Image_TB.split('_')[4]
        # "NPP_VIAES_L1.A2018001.0854.001.2018009150807.pssgrpgs_000501315598.BrightnessTemperature_I5-BrightnessTemperature_I5.tif"
        # Total_Day_VIIRS = datetime.datetime.strptime(Name_VIIRS_Image_TB.split('.')[1][1:], "%Y%j").strftime("%Y%m%d")
        # Total_Time_VIIRS = Name_VIIRS_Image_TB.split('.')[2]
        #
        # # Get the information out of the VIIRS name
        # year = int(Total_Day_VIIRS[:4])
        # month = int(Total_Day_VIIRS[4:6])
        # day = int(Total_Day_VIIRS[6:8])
        # Startdate = '%d-%02d-%02d' % (year, month, day)
        # DOY = datetime.datetime.strptime(Startdate, '%Y-%m-%d').timetuple().tm_yday
        # hour = int(Total_Time_VIIRS[0:2])
        # minutes = int(Total_Time_VIIRS[2:4])
        #
        # # Print data used from sheet General_Input
        # print('VIIRS PROBA-V Input:')
        # print('Path to Thermal VIIRS image = %s' % str(Name_VIIRS_Image_TB))
        # print('Path to Quality VIIRS image = %s' % str(Name_VIIRS_Image_QC))
        # print('Name of PROBA-V image = %s' % str(Name_PROBAV_Image))
        year, DOY, hour, minutes, UTM_Zone = -1, -1, -1, -1, -1
        return year, DOY, hour, minutes, UTM_Zone
