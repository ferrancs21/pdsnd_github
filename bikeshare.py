import time
import pandas as pd
import numpy as np
import statistics
import datetime

CITY_DATA = { 'Chicago': 'data/chicago.csv',
              'New York City': 'data/new_york_city.csv',
              'Washington': 'data/washington.csv'}


CITY_number = { '1' :'chicago',
                '2' :'new york city',
                '3' :'washington'}

months = { 'January': 1,
           'February': 2,
           'March': 3,
           'April': 4,
           'May': 5,
           'June': 6,
           'July': 7,
           'August': 8,
           'September': 9,
           'October': 10,
           'November': 11,
           'December': 12
            }

NumToMonth = { '1': 'January',
           '2': 'February',
           '3': 'March',
           '4': 'April',
           '5': 'May',
           '6': 'June',
           '7': 'July',
           '8': 'August',
           '9': 'September',
           '10': 'October',
           '11': 'November',
           '12': 'December'
            }

dayofweek = ('Monday', 'Tuesday', 'Wednesday',
 'Thursday', 'Friday', 'Saturday', 'Sunday')

dayz = { 'Monday': 0,
          'Tuesday': 1,
          'Wednesday': 2,
          'Thursday': 3,
          'Friday': 4,
          'Saturday': 5,
          'Sunday': 6
        }

def find_max_mode(list1):
    list_table = statistics._counts(list1)
    len_table = len(list_table)

    if len_table == 1:
        max_mode = statistics.mode(list1)
    else:
        new_list = []
        for i in range(len_table):
            new_list.append(list_table[i][0])
        max_mode = max(new_list) # use the max value here
    return max_mode

# asks for the city
def citycheck():
    while True:
        try:
            city = input('There is data available for the bikesharing systems \
of the following cities: \n-Chicago\n-New York city\n-Washington, D.C. \n\
Which city do you want to explore(chicago/new york city/washington)?\n')
# Checks if anwser exists in the dictionary, if it exits, asks if you are
# sure about your anwser and exits de loop. If it does not exists,
# it prints your input and ask you again.
            if city.title() in CITY_DATA:
                confirmation = input('\nAre you sure you want to see the data \
for {}?(y/n)\n'.format(city.title()))
                break
            else:
                print('Ups! Looks like your input ({}) did not match any city \
in our data base.\n'.format(city))
        except:
            print('\nUps! Looks like your input was not valid\n')
    return city,confirmation

# asks for the month
def monthcheck(city):
    while True:
        try:
            month = input('\nSelect a month for which you want to check the \
data for {}\'s bikesharing system.\nType all if you want the data for all \
months.)\n'.format(city))
# Checks if anwser exists in the dictionary or user wants all, if it exits,
# asks if you are sure about your anwser and exits de loop.
# If it does not exists asks you again.
            if month == 'all':
                confirmation = input('\nAre you sure you want to see the data \
for all months?(y/n)\n')
                break
            elif month.title() in months:
                confirmation = input('\nAre you sure you want to see the data \
for {}?(y/n)\n'.format(month.title()))
                break
            else:
                print('\nLooks like your awnser is not a valid anwser\n')
        except:
            print('\nUps! Looks like your input was not valid\n')
    return month,confirmation

# asks for the day
def daycheck(city):
    while True:
        try:
            day = input('\nSelect the day of the week for which you want \
the data. Type all if you want the data for all the days.\n')
# Checks if anwser exists in the dictionary or user wants all, if it exits,
# asks if you are sure about your anwser and exits de loop.
# If it does not exists asks you again
            if day == 'all':
                confirmation = input('\nAre you sure you want to see the data \
for all the days of the week?(y/n)\n')
                break
            elif day.title() in dayz:
                confirmation = input('\nAre you sure you want to see the data \
for {}?(y/n)\n'.format(day.title()))
                break
            else:
                print('\nLooks like your awnser is not a valid anwser\n')
        except:
            print('\nUps! Looks like your input was not valid\n')
    return day,confirmation

#obtains filters
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # asks for city and checks if city exists in data base. asks user if
    # he is sure of its selection.
    city,confirmation = citycheck()
# loops question untill user is sure that the anwser is correct.
    while confirmation != "y":
        city,confirmation = citycheck()
    # Asks user for the months that he desires to check.
    month,confirmation = monthcheck(city)
# loops question untill user is sure that the anwser is correct.
    while confirmation != "y":
        month,confirmation = monthcheck(city)
    # Asks user for day of the week that he desires to check.
    day,confirmation = daycheck(city)
# loops question untill user is sure that the anwser is correct.
    while confirmation != "y":
        day,confirmation = daycheck(city)
    print('-'*40)
    city = city.title()
    return city, month, day

#Creates datasets
def load_data(city, month, day):
    # Loads data for the specified city and filters by month and day if applicable.
    path = CITY_DATA[city]
    df = pd.read_csv(path)
    # Extracts month, day and time of the Start Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    #Selects month
    if month == "all":
        df = df
    else:
        df = df.loc[df['Start Time'].dt.month == months[month.title()]]

    #Selects day of the week
    if day == "all":
        df = df
    else:
        df = df.loc[df['Start Time'].dt.dayofweek == dayz[day.title()]]

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df['TripLength'] = df['End Time'] - df['Start Time']
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = NumToMonth[str(find_max_mode(df['month']))]
    print('\nThe most common month is {}\n'.format(popular_month))
    # display the most common day of week
    popular_dow = find_max_mode(df['day_of_week'])
    print('\nThe most common day of the week is {}\n'.format(popular_dow))

    # display the most common start hour
    popular_hour = find_max_mode(df['hour'])
    print('\nThe most common hour is {}\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_StartStn =  find_max_mode(df['Start Station'])
    print('\nThe most common start station is {}\n'.format(popular_StartStn))

    # display most commonly used end station

    popular_EndStn = find_max_mode(df['End Station'])
    print('\nThe most common end station is {}\n'.format(popular_EndStn))

    # display most frequent combination of start station and end station trip
    popularTrip = find_max_mode(list(zip(df['Start Station'],df['End Station'])))
    FirstStn = popularTrip[0]
    EndStn = popularTrip[1]
    print('\nThe most common trip is from {} to {}\n'.format(FirstStn, EndStn))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    TTT = df['TripLength'].sum()
    print('\nThe total travel time is {}\n'.format(TTT))

    # display mean travel time
    MTT = TTT/len(df['TripLength'])
    print('\nThe mean travel time is {}\n'.format(MTT))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    df_nna = df.dropna()
    # Display counts of user types
    # User types
    usertypes = df_nna['User Type'].unique()
    #extracts user counts
    usercount = df_nna['User Type'].value_counts()
    print('\nThere are a total of {} user types:\nUser type - count'.format(len(usertypes,)))
    # goes over the user types and prints the count for each one.
    for i in range(len(usertypes)):
        print('{} - {}'.format(usertypes[i], usercount.loc[usertypes[i]]))

    if city != 'Washington':
        # Display counts of gender
        # gender types
        gendertypes = df_nna['Gender'].unique()
        #extracts gender counts
        gendercount = df_nna['Gender'].value_counts()
        print('\nThere are a total of {} genders:\nGender - count'.format(len(gendertypes,)))
        # goes over the gender types and prints the count for each one.
        for i in range(len(gendertypes)):
            print('{} - {}'.format(gendertypes[i], gendercount.loc[gendertypes[i]]))

        # Display earliest, most recent, and most common year of birth
        oldest = int(df_nna['Birth Year'].min())
        young = int(df_nna['Birth Year'].max())
        common = int(find_max_mode(df_nna['Birth Year']))

        print('\nThe oldest user was born in {},\nThe youngest user was born in {}\
,\nThe most common year of birth is {},\n'.format(oldest, young, common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    i = 0
    totalrows = len(df.index)
    while True:
        if i + 5 <= totalrows-1:
            print('\nShowing raw data from row {} to row {} out of {} rows\n'.format(i+1,(i+5),totalrows))
            print(df.iloc[i:(i+5)])
            i += 6
            FiveMore = input('\nWould you like to see the next 5 rows? (y/n).\n')
            if FiveMore.lower() != 'y':
                break
        else:
            print('\nShowing raw data from row {} to row {} out of {} rows\n'.format(i,totalrows,totalrows))
            print(df.iloc[i:(totalrows-1)])
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_data = input('\nWould you like to view 5 rows of individual \
trip data? (y/n)\n')
        if view_data.lower() == 'y':
            raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
