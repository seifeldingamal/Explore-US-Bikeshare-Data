import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input("Would you like to see data for Chicago, New York, or Washington?\n")).lower()
            if not city:
                raise ValueError('empty string')
            if city not in CITY_DATA:
                raise ValueError("Not one of the city names, Please try again ...")
        except ValueError:
            print("Not a String, Please try again ...")
        else:
            break
        # TO DO: get user input for month (all, january, february, ... , june)
    resps = ['month','day','none']
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    resp = ''
    while True:
        try:
            resp = str(input("Would you like to filter the data by month, day or not at all? (month, day or none)\n")).lower()
            if resp == 'none':
                month = None
                day = None
                break
            if not resp:
                raise ValueError('empty string')
            if resp not in resps:
                raise ValueError("Not one of the given responds, Please try again ...")
        except ValueError:
            print("Not a String, Please try again ...")
        else:
            break
    if resp == 'month':
        while True:
            try:
                month = str(input("Which month - January, February, March, April, May, or June?\n")).lower()
                day = None
                if not month:
                    raise ValueError('empty string')
                if month not in months:
                    raise ValueError("Not a month, Please try again ...")
            except ValueError:
                print("Not a String, Please try again ...")
            else:
                break
    if resp == 'day':
        while True:
            try:
                day = str(input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday?\n")).lower()
                month = None
                if not day:
                    raise ValueError('empty string')
                if day not in days:
                    raise ValueError("Not a day, Please try again ...")
            except ValueError:
                print("Not a String, Please try again ...")
            else:
                break
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != None:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != None:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Start Month:', popular_month)
    # display the most common day of week
    df['week'] = df['Start Time'].dt.week
    popular_week = df['week'].mode()[0]
    print('Most Frequent Start Week:', popular_week)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df.groupby(['Start Station']).size().sort_values(ascending=False)
    print('Most Frequent Start Station:', popular_start.index[0])
    # display most commonly used end station
    popular_end = df.groupby(['End Station']).size().sort_values(ascending=False)
    print('Most Frequent End Station:', popular_end.index[0])
    # display most frequent combination of start station and end station trip
    freq_comb = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print('Most Frequent Combination of Start and End Stations:', freq_comb.index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_tript = df['Trip Duration'].sum()
    print('Total Trip Duration:', total_tript)
    # display mean travel time
    avg_tript = df['Trip Duration'].mean()
    print('Average Trip Duration:', avg_tript)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('Counts of User Types:\n', user_type_counts)
    # Display counts of gender
    if city != 'washington':
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of Gender Types:\n', gender_counts)
        # Display earliest, most recent, and most common year of birth
        earliest_by = df['Birth Year'].min()
        print('\nEarliest Year of Birth:\n', int(earliest_by))
        most_recent_by = df['Birth Year'].max()
        print('\nMost Recent Year of Birth:\n', int(most_recent_by))
        Common_by = df['Birth Year'].mode()[0]
        print('\nMost Common Year of Birth:\n', int(Common_by))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    """Displays raw data on bikeshare"""
    resps = ['yes','no']
    past = 0
    current = 5
    cond = True
    while cond == True:
        while True:
            try:
                resp = str(input("do you want to see raw data?(yes or no)\n")).lower()
                if not resp:
                    raise ValueError('empty string')
                if resp not in resps:
                    raise ValueError("Not one of the city names, Please try again ...")
                if resp == 'no':
                    cond = False
                    break
            except ValueError:
                print("Not a String, Please try again ...")
            else:
                break
        out = df.iloc[past:current]
        print(out)
        past = current
        current += 5

def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
