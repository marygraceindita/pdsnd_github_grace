import pandas as pd
import datetime
import getpass
import os

def get_city_filename(city):
    city_files = {
        "chicago": "chicago.csv",
        "washington": "washington.csv",
        "new york": "new_york_city.csv"
    }
    return city_files.get(city)

def load_data(city, month='all', day='all'):
    """Load data based on the city provided."""
    filename = get_city_filename(city)
    if filename:
        df = pd.read_csv(filename)
    else:
        print("Invalid city choice.")
        return None

    if 'Start Time' in df.columns:
        # Convert 'Start Time' column to datetime and extract month and day
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['month'] = df['Start Time'].dt.month
        df['day'] = df['Start Time'].dt.day_name()
    elif 'started_at' in df.columns:
        df['started_at'] = pd.to_datetime(df['started_at'])
        df['month'] = df['started_at'].dt.month
        df['day'] = df['started_at'].dt.day_name()
    else:
        print("'Start Time' or 'started_at' columns are not present in the dataframe. Please check the CSV.")
        return None

    # Filter by month and day if specified
    if month != 'all':
        month_num = datetime.datetime.strptime(month, '%B').month
        df = df[df['month'] == month_num]

    if day != 'all':
        df = df[df['day'] == day.capitalize()]

    return df

def get_mode_of_column(df, column_name):
    return df[column_name].mode()[0]

def most_frequent_times_of_travel(df):
    """Returns the most common month, day, and hour of travel."""
    
    # Most common month
    most_common_month_num = df['month'].mode()[0]
    most_common_month = datetime.datetime(1900, most_common_month_num, 1).strftime('%B')
    
    # Most common day
    most_common_day = df['day'].mode()[0]
    
    # Extract hour if it isn't already present in the dataframe
    if 'hour' not in df.columns:
        df['hour'] = df['started_at'].dt.hour if 'started_at' in df.columns else df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]

    print(f"\nMost Common Month: {most_common_month}")
    print(f"Most Common Day: {most_common_day}")
    print(f"Most Common Hour: {most_common_hour}")

    


def most_popular_stations_and_trip(df):
    """Return the most popular stations and trip."""
    start_time = datetime.datetime.now()

    if 'start_station_name' in df.columns and 'end_station_name' in df.columns:
        most_common_start_station = df['start_station_name'].mode()[0]
        most_common_end_station = df['end_station_name'].mode()[0]

        df['Trip'] = df['start_station_name'] + " to " + df['end_station_name']
        most_common_trip = df['Trip'].mode()[0]

        print(f"\nMost Common Start Station: {most_common_start_station}")
        print(f"Most Common End Station: {most_common_end_station}")
        print(f"Most Common Trip: {most_common_trip}")

    end_time = datetime.datetime.now()
    print(f"\nTime taken for most popular stations and trip calculation: {end_time - start_time}")

def trip_duration(df):
    """Return the trip duration calculations."""
    start_time = datetime.datetime.now()

    if 'started_at' in df.columns and 'ended_at' in df.columns:
        df['Trip Duration'] = (pd.to_datetime(df['ended_at']) - pd.to_datetime(df['started_at'])).dt.total_seconds()
        total_travel_time = df['Trip Duration'].sum()
        mean_travel_time = df['Trip Duration'].mean()

        print(f"\nTotal Travel Time: {total_travel_time}")
        print(f"Mean Travel Time: {mean_travel_time}")

    end_time = datetime.datetime.now()
    print(f"\nTime taken for trip duration calculation: {end_time - start_time}")

def main():
    overall_start_time = datetime.datetime.now()

    print("Good Day! Which city for Bikeshare would you like to see the data set? Washington, Chicago, New York?")
    city = input().lower()

    print("\nChoose a month (January, February, ..., June) or 'all':")
    month = input().lower()

    print("\nChoose a day (Monday, Tuesday, ... Sunday) or 'all':")
    day = input().lower()

    df = load_data(city, month, day)

    if df is not None:
        print(f"\nData for {city.capitalize()} in {month.capitalize()} on {day.capitalize()} loaded successfully.")
        
        # Print the total rows for each column
        for column in df.columns:
            print(f"Total rows in column '{column}': {df[column].notnull().sum()}")
        
        choice = input("\nWould you like to see the summarization? (yes/no) ").lower()
        
        if choice == 'yes':
            most_frequent_times_of_travel(df)
            most_popular_stations_and_trip(df)
            trip_duration(df)

            # Ask the user if they want to see the raw data
            raw_data_choice = input("\nWould you like to see the raw data? (yes/no) ").lower()

            if raw_data_choice == 'yes':
                start_row = 0
                rows_to_display = 5
                while True:
                    print(df.iloc[start_row:start_row + rows_to_display])
                    start_row += rows_to_display

                    more_data_choice = input("\nWould you like to see 5 more rows of raw data? (yes/no) ").lower()
                    if more_data_choice != 'yes':
                        break

        # Display closing message
        current_time = datetime.datetime.now()
        print("\nTHANK YOU AND HAVE A GOOD DAY!")
        print(f"Date and Time today: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        # This captures the total runtime of the script.
        print(f"Total run time of the whole data: {current_time - overall_start_time}")

if __name__ == '__main__':
    main()

