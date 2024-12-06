import pandas as pd

from digitalarztools.adapters.data_manager import DataManager


class HeatwaveModeling:
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager

    def identify_heatwave_events(self, threshold: float):
        print("Heatwave Events against threshold", threshold)

        # Ensure the heatwave_events column exists
        self.data_manager.add_column("heatwave_events", "INTEGER", default_value=0)

        # Fetch the data as a DataFrame
        df = self.data_manager.get_data_as_df()

        # Assuming the DataFrame has a 'date' and 'temperature' column
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')  # Ensure data is sorted by date

        # Initialize variables for heatwave detection
        heatwave_events = [0] * len(df)  # Initialize the list with zeros
        event_no = 0
        consecutive_days = 0

        for i, row in df.iterrows():
            if row['max'] >= threshold:
                consecutive_days += 1
                if consecutive_days == 3:
                    event_no += 1  # Declare a new event number after 3 consecutive days
                    for j in range(i - 2, i + 1):  # Apply the event number to the last 3 days
                        heatwave_events[j] = event_no
                if consecutive_days > 3:
                    heatwave_events[i] = event_no  # Apply the event number to the current day
            else:
                consecutive_days = 0  # Reset the counter when the temperature drops below the threshold

        # Update the heatwave_events column with the event numbers
        df['heatwave_events'] = heatwave_events

        # Update the records in the database
        for _, row in df.iterrows():
            self.data_manager.update_column(row['key'], 'heatwave_events', row['heatwave_events'])

        print("Heatwave events identified and updated.")

    def calculate_heatwave_stats(self):
        query = f"SELECT * FROM {self.data_manager.table_name} WHERE heatwave_events >= 1"
        df = self.data_manager.get_data_as_df(query)

        # Ensure the date column is in datetime format
        df['date'] = pd.to_datetime(df['date'])

        # Group by heatwave event number
        grouped = df.groupby('heatwave_events')

        # Initialize lists to store the statistics
        frequencies = []
        durations = []
        intensities = []
        # date_ranges = []
        start_dates = []
        end_dates = []
        for event_no, group in grouped:
            # Frequency: The count of events (since each group is a unique event, it's implicitly counted)
            frequencies.append(event_no)

            # Duration: Count the number of days in the event
            duration = len(group)
            durations.append(duration)

            # Intensity: Calculate the maximum temperature during the event
            max_temp = group['max'].max()
            intensities.append(max_temp)

            # Date range: Get the start and end date of the event
            start_date = group['date'].min()
            end_date = group['date'].max()
            start_dates.append(start_date.strftime('%Y-%m-%d'))
            end_dates.append(end_date.strftime('%Y-%m-%d'))
            # date_ranges.append((start_date, end_date))

        # Compile the results into a DataFrame
        stats_df = pd.DataFrame({
            'event_no': frequencies,
            'duration_days': durations,
            'max_temperature': intensities,
            'start_date':start_dates,
            'end_date': end_dates,
        })

        print(stats_df)
        return stats_df


