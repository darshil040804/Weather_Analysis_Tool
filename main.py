###############################################################################################
# ALGORITHM
#
# Weather Data Analysis Tool
# 
# This code implemenets a total of 11 functions. The flow of the program is as follows:
# open_files(): This function is first used to prompt the user for cities about which they 
# wish to retrieve data. If the computer has a file for that city, this function returns a 
# list of valid cities and a list of file pointers for each valid city
# city_data(): This function then goes through a csv file by using a filepointer as an 
# arguement. it returns a list of lists of tuples containing the data for each city
# read_files(): This function takes in a list of file pointers and reads in all the data
# into a list of lists of tuples by calling the helper function, the city_data() function
# get_data_in_range(): This function filters out all the data which is between the specified
# start and end date inclusive. This was done using the datetime opertor.
# get_max(): This function finds out the maximum value in a given column index of the data
# get_min(): This function finds out the minimum value in a given column index of the data
# get_averages(): This function finds out the average of all values in a given column index of the data
# get_modes(): This function finds out the modes, that is, the most occurring values in a 
# given column index. It returns the city, the list of mode(s) and the frequency of the mode(s)
# high_low_averages(): This function finds the highest and the lowest average of values in a 
# particular category. It returns the lowest and highest averages and the respective city names
# display_statistics(): This function displays the max value, the minimum value, the average value
# and the mode(s) with the number of occurrences.
# Finally the main function offers the user to choose from a list of 6 options. Each opeiton offers 
# different services and gives different outputs as per the user's desire.
# If the user doesnt want to continue with the program anymore, this function also offers an
# option to quit.
#########################################################################################

import csv
from datetime import datetime
from operator import itemgetter

COLUMNS = ["date",  "average temp", "high temp", "low temp", "precipitation", \
           "snow", "snow depth"]

TOL = 0.02

BANNER = 'This program will take in csv files with weather data and compare \
the sets.\nThe data is available for high, low, and average temperatures,\
\nprecipitation, and snow and snow depth.'    


MENU = '''
        Menu Options:
        1. Highest value for a specific column for all cities
        2. Lowest value for a specific column for all cities
        3. Average value for a specific column for all cities
        4. Modes for a specific column for all cities
        5. Summary Statistics for a specific column for a specific city
        6. High and low averages for each category across all data
        7. Quit
        Menu Choice: '''
        
        
def open_files():
    '''
    This function prompts the user to enter a list of city names and tries to open a 
    corresponding CSV file for each city.If a file is found, it is added to the cities_fp list
    and the city name is added to the valid_cities list. Else an error message is printed.
    The function returns the list of valid city names and the list of file pointers.
    '''
    #intitializing the two empty lists that are to be returned    
    valid_cities = []
    cities_fp = []
    input_cities = input("Enter cities names: ").split(",")

    #for loop to iterate over all cities in the input_cities list
    for city in input_cities:        

        #try-except suite to open a file if present else display error message
        try:
            city.strip()
            city_csv = city+".csv"
            fp = open(city_csv,"r")
            cities_fp.append(fp)
            valid_cities.append(city)

        #print error message if file not found
        except:
            print("\nError: File {} is not found".format(city_csv))
    return valid_cities, cities_fp


def city_data(fp):
    ''' 
    This function is a helper function for read_files function. It skips the first two lines 
    of a csv file and returns a list of tuples containing the data from each row
    '''
    reader = csv.reader(fp)
    next(reader)    #skip first line
    next(reader)    #skip second line 
    
    inner_list = []

    #for loop to iterate over each row in the csv file
    for row in reader:
        data_list = []
        date = row[0]   
        data_list.append(date)

        #for loop to add the float of each of the elements from index 1 to 6 in the data_list
        for element in row[1:7]:
            if element == "":
                element = None
            else:
                element = float(element)
            data_list.append(element)
        data_tuple = tuple(data_list) #converting data_list to a tuple
        inner_list.append(data_tuple) #appending each data_tuple into an inner list  
    return inner_list
    

def read_files(cities_fp):
    ''' This function takes a list of file pointers. Then it calls the city_data function
    to get the list of data for each file pointer. Then it appends all the data into a final 
    list which is known as list_of_lists'''
    list_of_lists = []

    #for loop tp iterate over each file pointer in cities_fp list
    for fp in cities_fp:
        inner_list = city_data(fp)   #calling the helper function city_data to get the inner_list
        list_of_lists.append(inner_list)     #appending each inner list to the final list_of_lists
    return list_of_lists


def get_data_in_range(master_list, start_str, end_str):
    '''
    This function takes a master list of data (a list of lists of tuples),
    a start date string, and an end date string, and returns a new list of data
    containing only the tuples with dates between the start and end dates.This
    was accomplished by using the datetime operator
    '''
    start_date = datetime.strptime(start_str, "%m/%d/%Y").date()
    end_date = datetime.strptime(end_str, "%m/%d/%Y").date()
    final_list = []

    #for loop to iterate over each sublist in the masterlist
    for sub_list in master_list:
        inner_list = []

        #for loop to iterate over each tuple in the sublist
        for tup in sub_list: 
            date_str = tup[0]     
            date = datetime.strptime(date_str, "%m/%d/%Y").date()

            #condition to retrieve all tuples whose dates are within the start and the end date inclusive
            if start_date <= date <= end_date:
                inner_list.append(tup)

        final_list.append(inner_list)
    return final_list
    

def get_min(col, data, cities): 
    '''
    This function takes a column index, data (a list of lists of tuples),
    and a list of city names, and returns a list of tuples where each tuple
    contains the city name and the minimum value in the specified column 
    with index "col" for that city's data.
    '''
    final_list = []

    #for lop to iterate over each city in the cities list
    for i in range(len(cities)):
        values = []
        min_value = 0

        #for loop tp iterate over each tuple in the list corresponding to the city at index i
        for tup in data[i]:

            #condition to avoid appending None to the values list
            if tup[col] != None:
                values.append(tup[col])

        min_value = min(values)   #finding the minimum value from the list of values
        final_list.append((cities[i],min_value))
    return final_list

     
def get_max(col, data, cities): 
    '''
    This function takes a column index, data (a list of lists of tuples),
    and a list of city names, and returns a list of tuples, where each tuple
    contains the city name and the maximum value in the specified column 
    with index "col" for that city's data.
    '''
    final_list = []

    #for lop to iterate over each city in the cities list
    for i in range(len(cities)):
        values = []
        max_value = 0

        #for loop tp iterate over each tuple in the list corresponding to the city at index i
        for tup in data[i]:

            #condition to avoid appending None to the values list
            if tup[col] != None:
                values.append(tup[col])
                
        max_value = max(values)      #finding the maximum value from list of values
        final_list.append((cities[i],max_value))
    return final_list

def get_average(col, data, cities): 
    '''
    This function takes a column index, data (a list of lists of tuples),
    and a list of city names, and returns a list of tuples, where each tuple
    contains the city name and the average of all the values in the specified 
    column with index "col" for that city's data.
    '''
    final_list = []

    #for lop to iterate over each city in the cities list
    for i in range(len(cities)):
        values = []
        avg_value = 0

        #for loop tp iterate over each tuple in the list corresponding to the city at index i
        for tup in data[i]:

            #condition to avoid appending None to the values list
            if tup[col] != None:
                values.append(float(tup[col]))

        avg_value = sum(values)/len(values)     #finding the average of all floats in the list of values
        avg_value = round(avg_value,2)     #rounding avg_value to 2 digits
        final_list.append((cities[i],avg_value))
    return final_list

def get_modes(col, data, cities):
    '''
    This function takes three arguements, col which is the column index, data (list of lists of tuples)
    and cities (list). It then finds the modes and its frequency for the specific column with column
    index "col". Further it creates a tuple including the city name, the list of modes, and the maximum
    count or maximum frequency). For each city, this tuple is appended into the final list and this 
    final list is returned.  
    '''
    final_list = []

    #for loop to iterate over each city in the cities list 
    for k in range(len(cities)):
        col_values = []

        #loop to iterate over each tuple in the list of data for this city
        for tup in data[k]:
            if tup[col] is not None:   #condition to avoid appending None to the col_values list
                col_values.append(tup[col])  #appending each column value to the col_values list
        col_values.sort()    # sorting the col_values list in ascending order
        
        #initializing empty list for modes, 0 for max_count and i=0 for initial index
        modes = []
        max_count = 0
        i = 0

        #initializing the index i to the first non-zero value in the col_values list (if there is one)
        if col_values and col_values[0] == 0:
            i += 1
            while i < len(col_values) and col_values[i] == 0:
                i += 1
        
        #loop to iterate over values in col_values list
        while i < len(col_values):
            count = 1   #initialize a counter for calculating frequeny 
            j = i + 1   #initialize index j to the value after the current value

            #iterate over the subsequent values that are within the tolerance of the current value
            while j < len(col_values) and abs((col_values[j]-col_values[i])/col_values[i]) <= 0.02:
                count += 1    #increase count by 1 if within tolerence
                j += 1        #increase index j by 1 if conditions of while loop satisfied

            #if count is greater than the current max_count, update the count and set the modes to the current value    
            if count > max_count:
                modes = [col_values[i]]
                max_count = count
            
            #if count is equal to max_count then append the current value to the modes list
            elif count == max_count:
                modes.append(col_values[i])
            
            #moving the index to the next value that is not within the tolerance of the current value
            i = j
        each_tuple = (cities[k], modes, max_count)  #preparing one tuplw per city
        
        #if max_count is 1, return a tuple with an epmty modes list
        if max_count == 1:
            final_list.append((cities[k], [], 1))
        else:
            final_list.append(each_tuple)
    return final_list
  

def high_low_averages(data, cities, categories):
    '''
    This function takes a list of data, a list of cities, and a list of categories. 
    It then calculates the average value for each category across all cities using
    the get_average() function.Then it finds the highest and lowest average values for 
    each category and returns a list of tuples for each category. With each tuple 
    containing the city with the lowest average value and the city with the highest 
    average value for that category. If a category is not found in the COLUMNS constant,
    a None value is appended to the results list.
    '''
    results = []

    #loop to iterte over each category in the categories list
    for category in categories:

        #condition to append None if category is not found in COLUMNS
        if category not in COLUMNS:
            results.append(None)
            continue
        col_index = COLUMNS.index(category)     #finding the index of the category in COLUMNS
        averages = get_average(col_index, data, cities)   #calling get_averages function to get an averages list

        #finding the highest and the lowest averages using itemgetter operator
        #compared index 1 of tuple because index 1 contains averages
        highest = max(averages, key=itemgetter(1))
        lowest = min(averages, key=itemgetter(1))
        results.append([(lowest[0], lowest[1]), (highest[0], highest[1])])
    return results
    

def display_statistics(col,data, cities):
    '''
    This function takes a column index col, the list of lists of tuples (data) and
    a list of cities and displays the summary statistics for each city. It displays
    the minimum value, the maximum value, the average value and the most common 
    repeated values (Modes) along with the number of occurrences.
    '''
    #retrieve the min, max and average values by calling the respective functions
    min_val= get_min(col,data,cities)
    max_val = get_max(col,data,cities)
    avg_val = get_average(col,data,cities)

    #retrieve the modes_ist by calling the get_modes function
    modes_list = get_modes(col,data,cities)

    #loop to iterate over each city in the cities list
    for i in range(len(cities)):
        print("\t{}: ".format(cities[i]))
        print("\tMin: {:.2f} Max: {:.2f} Avg: {:.2f}".format((min_val)[i][1], max_val[i][1], avg_val[i][1]))

        #modes is a list of modes at the first index of every 
        modes = modes_list[i][1]

        if modes:      #if modes is not an empty list
            modes_str_list = []

            #loop to get a list of all modes seperated by commas
            for mode in modes:
                modes_str_list.append(str(mode))
            
            #joining each element of the modes_str_list to form a string
            modes_str = ",".join(modes_str_list)

            frequency = modes_list[i][2]  #finding the number of occurrences
            print("\tMost common repeated values ({:d} occurrences): {:s}\n".format(frequency, modes_str))

        else:          #if modes is an empty list
            print("\tNo modes.")

def main():
    '''
    This is the main function which is used to interact with the user. It is responsible for diplaying messages
    and taking inputs from the user. Based on the inputs, it outputs the desired information.
    '''
    print(BANNER)
    valid_cities, cities_fp = open_files()
    list_of_lists = read_files(cities_fp)
    option = input(MENU)
    while True:     #main loop

        if option == '1':

            #prompting user for start date, end date and desired category
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            data_in_range_list = get_data_in_range(list_of_lists, start_date, end_date)
            category = input("\nEnter desired category: ").lower().strip()

            #while loop to check if category is present in COLUMNS. If not, reprompt until category in COLUMNS
            while True:
                try:
                    category in COLUMNS
                    break
                except:
                    print("\n\t{} category is not found.".format(category))    #error message printed if category not in COLUMNS
                    category = input("\nEnter desired category: ").lower().strip()
            print("\n\t{}: ".format(category))
            col_index = COLUMNS.index(category)
            max_list = get_max(col_index,data_in_range_list,valid_cities)

            #for loop to iterate over each tuple in the max_list and printing each tuple in the specified format
            for tup in max_list:
                print("\tMax for {:s}: {:.2f}".format(tup[0],tup[1]))
            option = input(MENU)   
            continue

        elif option == '2':

            #prompting user for start date, end date and desired category
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            data_in_range_list = get_data_in_range(list_of_lists, start_date, end_date)
            category = input("\nEnter desired category: ").lower().strip()

            #while loop to check if category is present in COLUMNS. If not, reprompt until category in COLUMNS
            while True:
                try:
                    category in COLUMNS
                    break
                except:
                    print("\n\t{} category is not found.".format(category))
                    category = input("\nEnter desired category: ").lower().strip()
            print("\n\t{}: ".format(category))
            col_index = COLUMNS.index(category)
            min_list = get_min(col_index,data_in_range_list,valid_cities)

            #for loop to iterate over each tuple in the max_list and printing each tuple in the specified format
            for tup in min_list:
                print("\tMin for {:s}: {:.2f}".format(tup[0],tup[1]))
            option = input(MENU)   
            continue

        elif option == '3':
            
            #prompting user for start date, end date and desired category
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            data_in_range_list = get_data_in_range(list_of_lists, start_date, end_date)
            category = input("\nEnter desired category: ").lower().strip()

            #while loop to check if category is present in COLUMNS. If not, reprompt until category in COLUMNS
            while True:
                try:
                    category in COLUMNS
                    break
                except:
                    print("\n\t{} category is not found.".format(category))
                    category = input("\nEnter desired category: ").lower().strip()
            print("\n\t{}: ".format(category))
            col_index = COLUMNS.index(category)
            avg_list = get_average(col_index,data_in_range_list,valid_cities)

            #for loop to iterate over each tuple in the avg_list and printing each tuple in the specified format
            for tup in avg_list:
                print("\tAverage for {:s}: {:.2f}".format(tup[0],tup[1]))
            option = input(MENU)   
            continue

        elif option == '4':

            #prompting user for start date, end date and desired category
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            data_in_range_list = get_data_in_range(list_of_lists, start_date, end_date)
            category = input("\nEnter desired category: ").lower().strip()

            #while loop to check if category is present in COLUMNS. If not, reprompt until category in COLUMNS
            while True:
                try:
                    category in COLUMNS
                    break
                except:
                    print("\n\t{} category is not found.".format(category))
                    category = input("\nEnter desired category: ").lower().strip()
            print("\n\t{}: ".format(category))
            col_index = COLUMNS.index(category)
            modes_list = get_modes(col_index,data_in_range_list, valid_cities)

            #for loop to iterate over each tuple in the modes_list
            for i,tup in enumerate(modes_list):
                modes = get_modes(col_index,data_in_range_list, valid_cities)[i][1] 

                #condition to check it modes is an empty list or not 
                if modes:
                    modes_str_list = []

                    #for loop to form a list of al modes in the list of modes
                    for mode in modes:
                        modes_str_list.append(str(mode))
                    
                    #joining each element from the list of modes to form a string with modes seperated by commas
                    modes_str = ",".join(modes_str_list) 
                    frequency = modes_list[i][2]    #finding the number of occurrences of each mode value
                    print("\tMost common repeated values for {:s} ({:d} occurrences): {:s}\n".format(tup[0],frequency,modes_str))
                else:
                    print("\tNo modes.")
            option = input(MENU)

        elif option == '5':

            #prompting user for start date, end date and desired category
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            data_in_range_list = get_data_in_range(list_of_lists, start_date, end_date)
            category = input("\nEnter desired category: ").lower().strip()

            #while loop to check if the categories entered by user are valid, and display statistics if valid. 
            while True:
                if category in COLUMNS:
                    print("\n\t{}: ".format(category))
                    col_index = COLUMNS.index(category)
                    display_statistics(col_index, data_in_range_list,valid_cities)
                    break

                #if not valid, print error statement for each category not found
                else:
                    print("\n\t{} category is not found.".format(category))
                    category = input("\nEnter desired category: ").lower().strip()
            
            option = input(MENU)
            
        elif option == '6':

            #prompting user for start date, end date and desired categories seperated by commas
            start_date = input("\nEnter a starting date (in mm/dd/yyyy format): ")
            end_date = input("\nEnter an ending date (in mm/dd/yyyy format): ")
            data_in_range_list = get_data_in_range(list_of_lists, start_date, end_date)
            categories = input("\nEnter desired categories seperated by comma: ").lower().strip().split(',')

            #retrieve data in the high_low_list by calling high_low_averages function
            high_low_list = high_low_averages(data_in_range_list,valid_cities,categories)

            print("\nHigh and low averages for each category across all data.")

            #print the high and low averages for each category
            for i,category in enumerate(categories):
                    if category in COLUMNS:
                        print("\n\t{}: ".format(category))
                        print("\tLowest Average: {:s} = {:.2f} Highest Average: {:s} = {:.2f}".format(high_low_list[i][0][0], high_low_list[i][0][1],high_low_list[i][1][0],high_low_list[i][1][1]))
                    else:
                        print("\n\t{} category is not found.".format(category))
            option = input(MENU)  
                
        elif option == '7':

            #print a closing message and break the loop to quit the program
            print("\nThank you using this program!")
            break
        
#DO NOT CHANGE THE FOLLOWING TWO LINES OR ADD TO THEM
#ALL USER INTERACTIONS SHOULD BE IMPLEMENTED IN THE MAIN FUNCTION
if __name__ == "__main__":
    main()
                                           

