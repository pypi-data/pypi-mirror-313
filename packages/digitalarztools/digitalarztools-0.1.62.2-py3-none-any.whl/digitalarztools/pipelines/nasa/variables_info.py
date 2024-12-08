class GLDASVariablesInfo:
    """
     This class contains the information about the GLDAS variables
     """
    names = {'t2m': 'Air_Temperature',
             'u2m': 'Eastward_Wind',
             'v2m': 'Northward_Wind',
             'q2m': 'Specific_Humidity',
             'tpw': 'Total_Precipitable_Water_Vapor',
             'ps': 'Surface_Pressure',
             'slp': 'Sea_Level_Pressure',
             'swgnet': 'Surface_Net_Downward_Shortwave_Flux',
             'swgdn': 'Surface_Incoming_Shortwave_Flux',
             'prectotcorr': 'Total_Precipitation_Corrected',
             'ts': 'Surface_Skin_Temperature'
             }

    descriptions = {'t2m': '2m Air Temperature',
                    'u2m': '2m Eastward wind',
                    'v2m': '2m Northward wind',
                    'q2m': '2m Specific Humidity',
                    'tpw': 'Total Precipitable Water Vapor',
                    'ps': 'Surface Pressure',
                    'slp': 'Sea Level Pressure',
                    'swgnet': 'Surface Net Downward Shortwave Flux',
                    'swgdn': 'Surface Incoming Shortwave Flux',
                    'prectotcorr': 'Total Precipitation Corrected',
                    'ts': 'Surface Skin Temperature'
                    }

    factors = {'t2m': 1,
               'u2m': 1,
               'v2m': 1,
               'q2m': 1,
               'tpw': 1,
               'ps': 0.001,
               'slp': 0.001,
               'swgnet': 1,
               'swgdn': 1,
               'prectotcorr': 3600,
               'ts': 1}

    types = {'t2m': 'state',
             'u2m': 'state',
             'v2m': 'state',
             'q2m': 'state',
             'tpw': 'state',
             'ps': 'state',
             'slp': 'state',
             'swgnet': 'state',
             'swgdn': 'state',
             'prectotcorr': 'flux',
             'ts': 'state'
             }

    def __init__(self, step):
        if step == 'three_hourly':
            self.units = {'t2m': 'K',
                          'u2m': 'm-s-1',
                          'v2m': 'm-s-1',
                          'q2m': 'kg-kg-1',
                          'tpw': 'mm',
                          'ps': 'kpa',
                          'slp': 'kpa',
                          'swgnet': 'W-m-2',
                          'swgdn': 'W-m-2',
                          'prectotcorr': 'mm',
                          'ts': 'K'
                          }

        elif step == 'hourly_MERRA2':
            self.units = {'t2m': 'K',
                          'u2m': 'm-s-1',
                          'v2m': 'm-s-1',
                          'q2m': 'kg-kg-1',
                          'tpw': 'mm',
                          'ps': 'kpa',
                          'slp': 'kpa',
                          'swgnet': 'W-m-2',
                          'swgdn': 'W-m-2',
                          'prectotcorr': 'mm',
                          'ts': 'K'
                          }

        elif step == 'daily' or step == 'daily_MERRA2':
            self.units = {'t2m': 'K',
                          'u2m': 'm-s-1',
                          'v2m': 'm-s-1',
                          'q2m': 'kg-kg-1',
                          'tpw': 'mm',
                          'ps': 'kpa',
                          'slp': 'kpa',
                          'swgnet': 'W-m-2',
                          'swgdn': 'W-m-2',
                          'prectotcorr': 'mm',
                          'ts': 'K'
                          }

        elif step == 'yearly':
            self.units = {'t2m': 'K',
                          'u2m': 'm-s-1',
                          'v2m': 'm-s-1',
                          'q2m': 'kg-kg-1',
                          'tpw': 'mm',
                          'ps': 'kpa',
                          'slp': 'kpa',
                          'swgnet': 'W-m-2',
                          'swgdn': 'W-m-2',
                          'prectotcorr': 'mm',
                          'ts': 'K'
                          }

        else:
            raise KeyError("The input time step is not supported")


class GEOSVariablesInfo:
    """
    This class contains the information about the GEOS variables
    """
    names = {'t2m': 'Air_Temperature',
             'u2m': 'Eastward_Wind',
             'v2m': 'Northward_Wind',
             'qv2m': 'Specific_Humidity',
             'tqv': 'Total_Precipitable_Water_Vapor',
             'ps': 'Surface_Pressure',
             'slp': 'Sea_Level_Pressure',
             't10m': 'Air_Temperature_10m',
             'v10m': 'Northward_Wind_10m',
             'u10m': 'Eastward_Wind_10m',
             'v50m': 'Northward_Wind_50m',
             'u50m': 'Eastward_Wind_50m',
             'ts': 'Surface_Skin_Temperature',
             'emis': 'Surface_Emissivity',
             'swgnt': 'Surface_Net_Downward_Shortwave_Flux',
             'swgntclr': 'Surface_Net_Downward_Shortwave_Flux_Assuming_Clear_Sky',
             'swgntcln': 'Surface_Net_Downward_Shortwave_Flux_Assuming_No_Aerosol',
             'swgntclrcln': 'Surface_Net_Downward_Shortwave_Flux_Assuming_Clear_Sky_And_No_Aerosol',
             'swgdn': 'Surface_Incoming_Shortwave_Flux',
             'lwgnt': 'Surface_Net_Downward_Longwave_Flux',
             'lwgntclr': 'Surface_Net_Downward_Longwave_Flux_Assuming_Clear_Sky',
             'lwgntclrcln': 'Surface_Net_Downward_Longwave_Flux_Assuming_Clear_Sky_And_No_Aerosol'}

    descriptions = {'t2m': '2m Air Temperature',
                    'u2m': '2m Eastward wind',
                    'v2m': '2m Northward wind',
                    'qv2m': '2m Specific Humidity',
                    'tqv': 'Total Precipitable Water Vapor',
                    'ps': 'Surface Pressure',
                    'slp': 'Sea Level Pressure',
                    't10m': '10m Air Temperature',
                    'v10m': '10m Northward wind',
                    'u10m': '10m Eastward wind',
                    'v50m': '50m Northward wind',
                    'u50m': '50m Eastward wind',
                    'ts': 'Surface Skin Temperature',
                    'emis': 'Surface Emissivity',
                    'swgnt': 'Surface Net Downward Shortwave Flux',
                    'swgntclr': 'Surface Net Downward Shortwave Flux Assuming Clear Sky',
                    'swgntcln': 'Surface Net Downward Shortwave Flux Assuming No Aerosol',
                    'swgntclrcln': 'Surface Net Downward Shortwave Flux Assuming Clear Sky And No Aerosol',
                    'swgdn': 'Surface Incoming Shortwave Flux',
                    'lwgnt': 'Surface Net Downward Longwave Flux',
                    'lwgntclr': 'Surface Net Downward Longwave Flux Assuming Clear Sky',
                    'lwgntclrcln': 'Surface Net Downward Longwave Flux Assuming Clear Sky And No Aerosol'}

    factors = {'t2m': 1,
               'u2m': 1,
               'v2m': 1,
               'qv2m': 1,
               'tqv': 1,
               'ps': 0.001,
               'slp': 0.001,
               't10m': 1,
               'v10m': 1,
               'u10m': 1,
               'v50m': 1,
               'u50m': 1,
               'ts': 1,
               'emis': 1,
               'swgnt': 1,
               'swgntclr': 1,
               'swgntcln': 1,
               'swgntclrcln': 1,
               'swgdn': 1,
               'lwgnt': 1,
               'lwgntclr': 1,
               'lwgntclrcln': 1}

    types = {'t2m': 'state',
             'u2m': 'state',
             'v2m': 'state',
             'qv2m': 'state',
             'tqv': 'state',
             'ps': 'state',
             'slp': 'state',
             't10m': 'state',
             'v10m': 'state',
             'u10m': 'state',
             'v50m': 'state',
             'u50m': 'state',
             'ts': 'state',
             'emis': 'state',
             'swgnt': 'state',
             'swgntclr': 'state',
             'swgntcln': 'state',
             'swgntclrcln': 'state',
             'swgdn': 'state',
             'lwgnt': 'state',
             'lwgntclr': 'state',
             'lwgntclrcln': 'state'}

    def __init__(self, step):
        if step == 'three_hourly':
            self.units = {'t2m': 'K',
                          'u2m': 'm-s-1',
                          'v2m': 'm-s-1',
                          'qv2m': 'kg-kg-1',
                          'tqv': 'mm',
                          'ps': 'kpa',
                          'slp': 'kpa',
                          't10m': 'K',
                          'v10m': 'm-s-1',
                          'u10m': 'm-s-1',
                          'v50m': 'm-s-1',
                          'u50m': 'm-s-1'}

        elif step == 'hourly':
            self.units = {'ts': 'K',
                          'emis': '-',
                          'swgnt': 'W-m-2',
                          'swgntclr': 'W-m-2',
                          'swgntcln': 'W-m-2',
                          'swgntclrcln': 'W-m-2',
                          'swgdn': 'W-m-2',
                          'lwgnt': 'W-m-2',
                          'lwgntclr': 'W-m-2',
                          'lwgntclrcln': 'W-m-2',
                          't2m': 'K',
                          'u2m': 'm-s-1',
                          'v2m': 'm-s-1',
                          'qv2m': 'kg-kg-1',
                          'tqv': 'mm',
                          'ps': 'kpa',
                          'slp': 'kpa',
                          't10m': 'K',
                          'v10m': 'm-s-1',
                          'u10m': 'm-s-1',
                          'v50m': 'm-s-1',
                          'u50m': 'm-s-1'}


        elif step == 'daily':
            self.units = {'t2m': 'K',
                          'u2m': 'm-s-1',
                          'v2m': 'm-s-1',
                          'qv2m': 'kg-kg-1',
                          'tqv': 'mm',
                          'ps': 'kpa',
                          'slp': 'kpa',
                          't10m': 'K',
                          'v10m': 'm-s-1',
                          'u10m': 'm-s-1',
                          'v50m': 'm-s-1',
                          'u50m': 'm-s-1',
                          'ts': 'K',
                          'emis': '-',
                          'swgnt': 'W-m-2',
                          'swgntclr': 'W-m-2',
                          'swgntcln': 'W-m-2',
                          'swgntclrcln': 'W-m-2',
                          'swgdn': 'W-m-2',
                          'lwgnt': 'W-m-2',
                          'lwgntclr': 'W-m-2',
                          'lwgntclrcln': 'W-m-2'}

        else:
            raise KeyError("The input time step is not supported")
