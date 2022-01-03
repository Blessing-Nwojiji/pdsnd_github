import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['all','january', 'february','march', 
         'april','may','june']

DAYS =['all','monday','tuesday','wednesday',
      'thursday','friday',' saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    selected_city = None
    city_prompt = 'Please select or type in any number from the list of available cities: '

    print(" List of available cities")  
    for index,city in enumerate(CITY_DATA):
        print(f' {index} --> {city}')
    
    #we use the while loop together with try and except to ensure the loop does not break and that the user puts in the correct information.
    while selected_city == None:
        city_index = input(city_prompt)
        try:
            city_key = list(CITY_DATA.keys())[int(city_index)]
            selected_city = CITY_DATA[city_key]
        except Exception:
            city_prompt = "There was a little mix up there, try any of the city index numbers e.g (1,2 or 3): "

    # get user input for month (all, january, february, ... , june)
    selected_month = None
    month_prompt = 'You rock!! now, select or type in any number from the list of months (you can select the index for all to see the details from all the months): '

    print("\n Months")   
    for index,month in enumerate(MONTHS):
        print(f' {index} --> {month}')
    
    #we use the while loop together with try and except to ensure the loop does not break and that the user puts in the correct information.
    while selected_month == None:
        month_index = input(month_prompt)
        try:
            selected_month = MONTHS[int(month_index)]
        except Exception:
            month_prompt = "Oops! you made the wrong entry, select or type in a correct number e.g (1,2 or 3): "

    # get user input for day of week (all, monday, tuesday, ... sunday)
    selected_day = None
    day_prompt = 'Seems you are an expert in this!! now, select or type in any number from the list of days(you can select the index for all): '

    print("\n DAYS")   
    for index,day in enumerate(DAYS):
        print(f' {index} --> {day}')
    
    #we use the while loop together with try and except to ensure the loop does not break and that the user puts in the correct information.
    while selected_day == None:
        day_index = input(day_prompt)
        try:
            selected_day = DAYS[int(day_index)]
        except Exception:
            day_prompt = "We know you got this, just try again, Please select or type in a correct number: "

    print('-'*40)
    return selected_city, selected_month, selected_day


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
    #Load data to df
    df = pd.read_csv(city)       

    #convert start and End time to datetime
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["End Time"] = pd.to_datetime(df["End Time"])

    #Extract month, day and hour colunms from Start time and End time.
    df["Start Month"] = df["Start Time"].dt.month
    df["Start Day"] = df["Start Time"].dt.day_name()
    df["Start Hour"] = df["Start Time"].dt.hour

    df["End Month"] = df["End Time"].dt.month
    df["End Day"] = df["End Time"].dt.day_name()
    df["End Hour"] = df["End Time"].dt.hour

    #To filter the data set
    if month != "all":      # filter data by month given
        # use the index of month to get the month list
        month_list = ["january", "february", "march", "april", "may", "june"]
        month = month_list.index(month) + 1
        # filter by month
        df = df[df["Start Month"] == month]

    #filter data by weekday given
    if day != "all":
        # filter by day of week
        df = df[df["Start Day"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    highest_start_month = df["Start Month"].mode()[0] - 1
    highest_end_month = df["End Month"].mode()[0] - 1

    month_list = ["january", "february", "marcch", "april", "may", "june"]

    print("\t The highest number of bike travel started in {} and most bike ride ended in {}\n".format(month_list[highest_start_month], month_list[highest_end_month]))

    # display the most common day of week
    common_day = df["Start Day"].mode()[0]

    print("\t The most common week day for bike riding is {}\n".format(common_day))


    # display the most common start hour
    common_start_hour = df["Start Hour"].mode()[0]
    common_end_hour = df["End Hour"].mode()[0]

    print("\t Most ride started at about the {}th hour while most ride ended about the {}th hour \n".format(common_start_hour,common_end_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_stn = df["Start Station"].mode()[0]
    print("\t The most popular start station is {} \n".format(most_common_start_stn))

    # display most commonly used end station
    most_common_end_stn = df["End Station"].mode()[0]
    print("\t The most popular end station is {} \t".format(most_common_end_stn))

    # display most frequent combination of start station and end station trip
    df["Start and End Station"] = df["Start Station"] + df["End Station"]    #this will add both start and end station to produce a new column which is a combination of the two locations

    #filtering the Start and End station for the most frequent combination on the "Start and End Station" 
    start_combined = df['Start Station'][df["Start and End Station"] == df["Start and End Station"].mode()[0]].unique()[0]
    end_combined = df['End Station'][df["Start and End Station"] == df["Start and End Station"].mode()[0]].unique()[0]

    print("\t The most frequent combination of start and end station trip is \"{}\" and \"{}\" respectively. \n".format(start_combined, end_combined))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # trip duration statistics 
    print(' Trip Duration statistics '.center(78, '-'))
    # display total travel time
    print('Total Travel Time '.ljust(40, '.'), df['Trip Duration'].sum())
    # display the mean travel time 
    print('Average Travel Time '.ljust(40, '.'), df['Trip Duration'].mean())
    # display the most travel time
    print('Most Travel Time '.ljust(40, '.'), df['Trip Duration'].mode()[0])
    # display the maximum travel time
    print('Max Travel Time '.ljust(40, '.'), df['Trip Duration'].max())
    # display the minimum travel time
    print('Min Travel Time '.ljust(40, '.'), df['Trip Duration'].min())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = dict(df.groupby(["User Type"])["User Type"].count())
    print(' User Statistics '.center(78, '-'))
    print("\n \t The bike Users type distribution is given below: \n \t\t User Type \t\t Total ")
    for user_type in user_types.keys():
        print("\t {} : \t {}".format(user_type, user_types[user_type]))

    # Display counts of gender
    try:   
        #Some of the data set does not have a gender column. So we have to use try and except to handle this error in case it occurs. 
        user_genders = dict(df.groupby(["Gender"])["Gender"].count())
        print(' Gender Statistics '.center(78, '-'))        
        print("\n \t The bike users gender distribution is given below: \n \t\t Gender \t Total ")
        for user_gender in user_genders.keys():
            print("\t {} : \t {}".format(user_gender, user_genders[user_gender]))
    except:
        print("\t Oops!! we could not find any gender classification in the selected data set \n")

    # Display earliest, most recent, and most common year of birth
    #Again to ensure the code does not break if we have a wrong date input we use try and except.
    try:
        earliest_birth_year = list(df["Birth Year"].dropna().sort_values(ascending=True).head(1))
        print("\n \t The birth year for the oldest set of bikers in the specified data is : {} \n".format(int(earliest_birth_year[0])))

        most_recent_birth_year = list(df["Birth Year"].dropna().sort_values(ascending=False).head(1))
        print("\t The birth year for the youngest set of bikers in the specified data is : {} \n".format(int(most_recent_birth_year[0])))

        most_common_year_of_birth = int(df["Birth Year"].mode()[0])
        print("\t The most common year of birth for the bikers in the specified data is : {} \n".format(most_common_year_of_birth))
    except:
        print("\t We are sorry to inform you that there is currently no year of birth data for the selected city \n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_data(df):
    """
        Ask the user if he/she needs to see the rows of the data used by 5 steps increment.
        Args:
            (dataframe) df - dataframe used for the analysis
        """

    # remove the combined column created
    df = df.drop(columns=["Start and End Station"], axis=1)

    answer = input("Do you wish to see the first 5 rows of the raw data set? (yes or no): ").lower().strip() #requsting user consent to display the dataset

    #index position holder for viewing the data set rows in step of 5's
    start_index = 0
    end_index = 5

    # while loop to keep requesting user consent to see more of the raw data
    while answer == "yes" and end_index <= df.size:
        print(df[start_index: end_index])
        start_index = end_index
        end_index += 5
        answer = input("Great job!1, do you wish to see the next first 5 rows of the raw data? (yes or no) : ").lower().strip()

def main():
    #this calls all the functions.
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
