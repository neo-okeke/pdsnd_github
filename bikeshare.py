import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """

    Asks user to specify a city, month, and day to analyze.

    Returns:

    (str) city - name of the city to analyze

    (str) month - name of the month to filter by, or "all" to apply no month filter

    (str) day - name of the day of week to filter by, or "all" to apply no day filter

    """

    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington)

    while True:

        city = input("Would you like to see data for Chicago, New York or Washington?\n").lower()

        if city not in ['chicago', 'new york', 'washington']:

            print("The city you have chosen has not been recognised, please try again")

        else:

            break

    # TO DO: get user input for month (all, january, february, ... , june)

    while True:

        month = input(
            "Which month out of the following do you want to analyse? \n"
            "January, February, March, April, May, June or type 'All' to analyze all months. \n").lower()

        if month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:

            print("You have selected an incorrect month, please try again")

        else:

            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    while True:

        day = input(
            "Please specify the day of the week you would like to analyze. "
            "Or type 'All' to analyze all days of the week "
            "\nEnter day of week in the following format (Monday, Tuesday, Wednesday,"
            "Thursday, Friday, Saturday or Sunday)\n").lower()

        if day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:

            print("The day of the week you have chosen has not been recognised, please try again")

        else:

            break

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('-' * 40)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # Extract month from the Start Time column to create an month column
    df['month'] = df['Start Time'].dt.month

    # Extract day of week from the Start Time column to create an weekday column
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # display the most common month

    months = ['january', 'february', 'march', 'april', 'may', 'june']

    most_common_month = df['month'].mode()[0]
    # print('Most Common Month of travel:', most_common_month)
    print('Most Common Month of travel:', months[most_common_month - 1].title())

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print('Most Common Day of Travel:', most_common_day)

    # display the most common start hour
    most_popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', most_popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Concatenate End Station & Start Station to create a unique ID
    df['Combined Station Name'] = "\n" + df['Start Station'] + ' to ' + df['End Station']

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', most_common_start_station)

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', most_common_end_station)

    # display most frequent combination of start station and end station trip
    most_common_station_combination = df['Combined Station Name'].mode()[0]
    print('Most Popular Journey:', most_common_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time:', int(total_travel_time / 3600), 'hours')

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean(axis=0)
    print('Average travel time:', round((average_travel_time / 60), 2), 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    try:
        # Display counts of gender
        gender_count = df['Gender'].value_counts()
        print(gender_count)
    except KeyError:
        print('No gender data available')
    try:
        # Most common Year of Birth
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('Most Common Birth Year:', int(most_common_birth_year))
    except KeyError:
        print('No Common Birth Year data available')
    try:
        # Earliest Birth Year
        earliest_birth_year = df['Birth Year'].min()
        print('Earliest Birth Year:', int(earliest_birth_year))
    except KeyError:
        print('No Earliest Birth Year data available')

    try:
        # Latest Birth Year
        latest_birth_year = df['Birth Year'].max()
        print('Latest Birth Year:', int(latest_birth_year))
    except KeyError:
        print('No Latest Birth Year data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """Displays 5 lines of raw data upon user request."""
    x = 0
    while True:
        want_data = input("\nWould you like to view individual trip data? Enter \"Yes\" or \"No\"\n").lower()

        if want_data == 'yes':
            print(df.iloc[0:x+5])
            x += 5
        else:
            break


def main():
    """Runs the sequence of of functions for the overall program"""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter \"Yes\" or \"No\".\n')

        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
