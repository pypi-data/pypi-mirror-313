import math
import os
from datetime import timedelta, datetime
from typing import Tuple, List

import openpyxl
import pandas as pd
from dateutil.relativedelta import relativedelta
from dateutil.utils import today
from pandas import DatetimeIndex


class DateUtils:
    @staticmethod
    def yearly_daterange_split(df: pd.DataFrame, date_col: str='dates', time_delta_days=1) ->List[Tuple[datetime, datetime]]:
        """
        # Sample DataFrame with a column of dates
        df = pd.DataFrame({
            'dates': pd.to_datetime(
                ['2022-01-01', '2022-01-02', '2022-03-01', '2022-12-30', '2023-01-01', '2023-01-02'])
        })
        """

        # Ensure dates are sorted
        df = df.sort_values(by=date_col)

        # Identify consecutive dates and ranges
        df['diff'] = df['dates'].diff().dt.days
        df['new_range'] = (df['diff'] != 1).cumsum()

        # Function to split ranges exceeding one year
        def split_ranges_exceeding_one_year(group):
            min_date = group['dates'].min()
            max_date = group['dates'].max()
            ranges = []

            while (max_date - min_date).days > 365:
                next_year_date = min_date + pd.DateOffset(years=1)
                ranges.append((min_date, next_year_date - pd.DateOffset(days=1)))
                min_date = next_year_date
            ranges.append((min_date, max_date))

            return ranges

        # Apply function and create list of ranges
        range_list = []
        for _, g in df.groupby('new_range'):
            range_list.extend(split_ranges_exceeding_one_year(g))

        # Adjusted formatting for Google Earth Engine
        formatted_range_list = [
            # (start.date(), end.date()) if start != end else (start.date(), start.date()) for start, end in
            (start.date(), end.date()) for start, end in
            range_list if end.date() > (start.date() + timedelta(days=time_delta_days)) ]

        return formatted_range_list

    @staticmethod
    def get_date_range(no_of_days: int, date=None):
        if date is None:
            date = today()
            no_of_days = -no_of_days if no_of_days > 0 else no_of_days
        if no_of_days < 0:
            end_date = date
            start_date = end_date + timedelta(days=no_of_days)
        else:
            start_date = date
            end_date = start_date + timedelta(days=no_of_days)

        return start_date, end_date

    @staticmethod
    def Make_TimeStamps(start_date, end_date) -> DatetimeIndex:
        '''
        This function determines all time steps of which the FPAR must be downloaded
        The time stamps are 8 daily.

        Keywords arguments:
        start_date -- 'yyyy-mm-dd'
        end_date -- 'yyyy-mm-dd'
        '''

        # Define the DOY and year of the start day
        DOY = datetime.strptime(start_date, '%Y-%m-%d').timetuple().tm_yday
        Year = datetime.strptime(start_date, '%Y-%m-%d').timetuple().tm_year

        # Define the year of the end day
        YearEnd = datetime.strptime(end_date, '%Y-%m-%d').timetuple().tm_year

        # Change the DOY of the start day into a DOY of MODIS day (8-daily) and create new startdate
        DOYstart = int(math.floor(DOY / 8.0) * 8) + 1
        DOYstart = str('%s-%s' % (DOYstart, Year))
        Day = datetime.strptime(DOYstart, '%j-%Y')
        Month = '%02d' % Day.month
        Day = '%02d' % Day.day
        start_date = (str(Year) + '-' + str(Month) + '-' + str(Day))

        # Create the start and end data for the whole year
        year_start_date = pd.date_range(start_date, end_date, freq='AS')
        YearEndDate = pd.date_range(start_date, end_date, freq='A')

        # Define the amount of years that are involved
        amount_of_year = YearEnd - Year

        # If the startday is not in the same year as the enddate
        if amount_of_year > 0:
            for i in range(0, amount_of_year + 1):
                if i == 0:
                    startdate1 = start_date
                    enddate1 = YearEndDate[0]
                    dates = pd.date_range(startdate1, enddate1, freq='8D')
                if i == amount_of_year:
                    startdate1 = year_start_date[-1]
                    enddate1 = end_date
                    Dates1 = pd.date_range(startdate1, enddate1, freq='8D')
                    dates = dates.union(Dates1)
                if i != amount_of_year and i != 0:
                    startdate1 = year_start_date[i - amount_of_year - 1]
                    enddate1 = YearEndDate[i]
                    Dates1 = pd.date_range(startdate1, enddate1, freq='8D')
                    dates = dates.union(Dates1)

        # If the startday is in the same year as the enddate
        if amount_of_year == 0:
            dates = pd.date_range(start_date, end_date, freq='8D')

        return dates

    @staticmethod
    def Check_Dates(dates_8d_first):
        # # Check if dates are already processed
        # output_excel_indicator = os.path.join(home_folder, "Output_Data", "Indicators", "EXCEL_IPIs_V2.xlsx")
        # if os.path.exists(output_excel_indicator):
        #     wb = openpyxl.open(output_excel_indicator)
        #     ws = wb["IPI1"]
        #     dates_done = []
        #     date_column = ws['A']
        #
        #     # Print the contents
        #     for x in range(2, len(date_column)):
        #         dates_done.append(date_column[x].value)
        #
        #     dates_done_datetime = [datetime.strptime(k, "%Y%m%d").toordinal() for k in dates_done]
        #
        #     Startdate_or = -9999
        #     Enddate_or = -9999
        #
        #     for date_8d in dates_8d_first:
        #         date_check = date_8d.toordinal()
        #         if date_check not in dates_done_datetime and Startdate_or == -9999:
        #             Startdate_or = np.copy(date_check)
        #
        #         if date_check not in dates_done_datetime and date_check > Enddate_or:
        #             Enddate_or = np.copy(date_check)
        #
        #     if Startdate_or != -9999 and Enddate_or != -9999:
        #         startdate = datetime.strftime(datetime.fromordinal(Startdate_or), "%Y-%m-%d")
        #         enddate = datetime.strftime(datetime.fromordinal(Enddate_or), "%Y-%m-%d")
        #     else:
        #         startdate = ""
        #         enddate = ""
        #
        # else:
        start_date = datetime.strftime(dates_8d_first[0], "%Y-%m-%d")
        end_date = datetime.strftime(dates_8d_first[-1], "%Y-%m-%d")

        if datetime.strptime(end_date, "%Y-%m-%d") > datetime.now() - relativedelta(days=7):
            end_date = datetime.strftime(datetime.now() - relativedelta(days=7), "%Y-%m-%d")

        return start_date, end_date

    @staticmethod
    def Make_TimeStamps(start_date, end_date):
        '''
        This function determines all time steps of which the LST must be downloaded
        The time stamps are 8 daily.

        Keywords arguments:
        Startdate -- 'yyyy-mm-dd'
        Enddate -- 'yyyy-mm-dd'
        '''

        # Define the DOY and year of the start day
        DOY = datetime.strptime(start_date, '%Y-%m-%d').timetuple().tm_yday
        Year = datetime.strptime(start_date, '%Y-%m-%d').timetuple().tm_year

        # Define the year of the end day
        YearEnd = datetime.strptime(end_date, '%Y-%m-%d').timetuple().tm_year

        # Change the DOY of the start day into a DOY of MODIS day (16-daily) and create new startdate
        DOYstart = int(math.floor(DOY / 8.0) * 8) + 1
        DOYstart = str('%s-%s' % (DOYstart, Year))
        Day = datetime.strptime(DOYstart, '%j-%Y')
        Month = '%02d' % Day.month
        Day = '%02d' % Day.day
        start_date = (str(Year) + '-' + str(Month) + '-' + str(Day))

        # Create the start and end data for the whole year
        YearStartDate = pd.date_range(start_date, end_date, freq='AS')
        YearEndDate = pd.date_range(start_date, end_date, freq='A')

        # Define the amount of years that are involved
        AmountOfYear = YearEnd - Year

        # If the startday is not in the same year as the enddate
        if AmountOfYear > 0:
            for i in range(0, AmountOfYear + 1):
                if i == 0:
                    startdate1 = start_date
                    enddate1 = YearEndDate[0]
                    dates = pd.date_range(startdate1, enddate1, freq='8D')
                if i == AmountOfYear:
                    startdate1 = YearStartDate[-1]
                    enddate1 = end_date
                    dates1 = pd.date_range(startdate1, enddate1, freq='8D')
                    dates = dates.union(dates1)
                if i != AmountOfYear and i != 0:
                    startdate1 = YearStartDate[i - AmountOfYear - 1]
                    enddate1 = YearEndDate[i]
                    dates1 = pd.date_range(startdate1, enddate1, freq='8D')
                    dates = dates.union(dates1)

        # If the startday is in the same year as the enddate
        if AmountOfYear == 0:
            dates = pd.date_range(start_date, end_date, freq='8D')

        return dates
