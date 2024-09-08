import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#Section to ask which city, month and day to display data
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        city = input("Which city would you like to explore? (chicago, new york city, washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Incorrect city. Please try again.")
    
    while True:
        month = input("Which month? (all, january, february, ... , june): ").lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print("Incorrect month. Please try again.")
    
    while True:
        day = input("Which day? (all, monday, tuesday, ... sunday): ").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print("Incorrect day. Please try again.")
    
    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df

def time_stats(df):
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    common_month = df['month'].mode()[0]
    print('Most Common Month:', common_month)

    common_day_of_week = df['day_of_week'].mode()[0]
    print('Most Common Day of Week:', common_day_of_week)

    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('Most Common Start Hour:', common_start_hour)

    # Section for total and mean travel time
    if 'Trip Duration' in df:
        total_travel_time = df['Trip Duration'].sum()
        mean_travel_time = df['Trip Duration'].mean()
        print('\nTotal Travel Time:', total_travel_time)
        print('Mean Travel Time:', mean_travel_time)
    else:
        print("\n'Trip Duration' data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    common_start_station = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station:', common_start_station)

    common_end_station = df['End Station'].mode()[0]
    print('Most Commonly Used End Station:', common_end_station)

    df['Start-End Combination'] = df['Start Station'] + " to " + df['End Station']
    common_start_end_combination = df['Start-End Combination'].mode()[0]
    print('Most Frequent Combination of Start Station and End Station Trip:', common_start_end_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if 'User Type' in df:
        user_types = df['User Type'].value_counts().to_dict()
        print('Counts of User Types:')
        for user_type, count in user_types.items():
            print(f"  {user_type}: {count}")
    else:
        print("'User Type' data not available for this city.")

    # Display counts of gender (only available for some cities)
    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts().to_dict()
        print('\nCounts of Gender:')
        for gender, count in gender_counts.items():
            print(f"  {gender}: {count}")
    else:
        print("\n'Gender' data not available for this city.")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nEarliest Year of Birth:', earliest_year)
        print('Most Recent Year of Birth:', most_recent_year)
        print('Most Common Year of Birth:', most_common_year)
    else:
        print("\n'Birth Year' data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """Displays 5 lines of raw data at a time upon user request."""
    start_loc = 0
    while True:
        while True:
            display = input('\nWould you like to see 5 more rows of raw data? Enter yes or no.\n').lower()
            if display in ['yes', 'no']:
                break
            else:
                print("Incorrect response. Please type 'yes' or 'no'.")
        
        if display == 'no':
            break

        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5

        if start_loc >= len(df):
            print("No more data to display.")
            break

def restart_program():
    """Asks the user if they want to restart the program."""
    while True:
        restart = input("\nWould you like to restart the program? (yes/no): ").lower()
        if restart in ['yes', 'no']:
            return restart == 'yes'
        print("Invalid input. Please type 'yes' or 'no'.")

if __name__ == "__main__":
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        user_stats(df)
        display_raw_data(df)

        # Ask if the user wants to restart after everything is done
        if not restart_program():
            print("Thank you for using the program. Goodbye!")
            break
