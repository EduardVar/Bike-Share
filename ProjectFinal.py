'''
This program is the final version of the bike share project

Author: Eduard Varshavsky
Date: November 25, 2018
'''

#Imports a library that allows the user to request data from a url online
import urllib.request

'''
This function will read in data from the Toronto Bicycle data website
The parameter is supposed to be an imported module that allows program to
request information from websites
The function returns the decoded html data
'''
def readInData():
    
    #Requests data from a website and then stores it within a list by decoding
    #it into usable string
    response = urllib.request.urlopen("http://research.cs.queensu.ca" +
        "/home/cords2/bikes.txt")
    html = response.read()
    data = html.decode('utf-8').split("\n")

    #Creates a new list to hold data to be split
    splittederData = []

    #Goes through each line of data provided by the website
    for i in range(len(data)):
        #Adds a list of cleaned data as an element of the overall data
        splittederData.append(data[i].strip("\r ").split("\t"))
    
    #Deletes the first and last pieces of irrelevant data
    del splittederData[0]
    del splittederData[-1]

    #Returnss an organized verion of the data decoded
    return organizeData(splittederData)

'''
This function uses the provided data and organizes it into a list with its
elements being a dictionary of all the info of a single  bicycle station
The parameter is the decoded data from the Toronto Bicycle data website
Returns a list of dictionaries containing all the usable data
'''
def organizeData(data):
    #Creates a list for the bicycle stations
    stationList = []

    #Goes through each set of station data within the data list 
    for station in data:
        #Adds a dictionary as an element with the dictionairy containing all
        #the information for a single station
        stationList.append({"stationId":station[0], "name":station[1], 
            "lat":float(station[2]), "lon":float(station[3]), 
            "capacity":int(station[4]), "numBikesAvailable":int(station[5]),
            "numDocksAvailable":int(station[6])})

    #Returns the list of stations
    return stationList

'''
This function checks if there are bikes available at the selected station
The parameter is the chosen bike station to check
Returns if it's true or false that a bike is available
'''
def checkBikeAvailable(bikeStation):
    #Returns boolean if the station exists and has a bicycle available
    return bikeStation != None and bikeStation["numBikesAvailable"] > 0

'''
This function checks if there is a dock available at the selected station
The parameter is the chosen bike station to check
Returns if it's true or false that a dock is available
'''
def checkDockAvailable(bikeStation):
    #Returns boolean if the station exists and has a dock available
    return bikeStation != None and bikeStation["numDocksAvailable"] > 0

'''
This function allows the user to rent a bike from a station; if any bikes
are available (use checkBikeAvailable). Should also display how many bikes
are available in total
The parameter is the chosen bike station to rent from
Returns a modified list of stations with a bike removed from the selected 
station if successful in renting it and a message to describe the action
'''
def rentBike(bikeStation):
    #Checks if a bicycle is available at the requested station
    if checkBikeAvailable(bikeStation):
        #Removes a bike while freeing up a dock. Notifies user
        bikeStation["numBikesAvailable"] -= 1
        bikeStation["numDocksAvailable"] += 1
        print("Bike rented from", bikeStation["name"] + "!\n")
    elif bikeStation == None:
        print("Invalid input.")
    else:
        #Notifies the user there were no bicycles available
        print("There are no bikes available here!")

'''
This function allows the user to return a bike to a station; if there is
space available to do so on the dock (use checkDockAvailable)
The parameter is the chosen bike station the user wants to return to
Returns a modified list of stations with a bike added to the selected 
station if there was space on the dock and a message to describe the action
'''
def returnBike(bikeStation):
    #Checks if a dock is available at the requested station
    if checkDockAvailable(bikeStation):
        #Adds a bike while removing a dock. Notifies user
        bikeStation["numBikesAvailable"] += 1
        bikeStation["numDocksAvailable"] -= 1
        print("Bike returned to", bikeStation["name"] + "!\n")
    elif bikeStation == None:
        print("Invalid input.")
    else:
        #Notifies the user there were no docks available
        print("There are no free docks available here!")

'''
This function calls all the info of a provided bicycle station and shows
it to the user
The parameter bikeStation is the selected bicycle station
Returns the data specific to the info of the desired bicycle station
'''
def stationInfo(bikeStation):
    #Stores the required character spacing per key of dictionary
    cellWidthDic = {"stationId":4, "name":36, "lat":12, "lon":12, 
            "capacity":4, "numBikesAvailable":4, "numDocksAvailable":4}

    #Uses every key in the station to print out station information with
    #adjusted 
    for key in bikeStation.keys():
        print((str(bikeStation[key])).ljust(cellWidthDic[key]), end = "\t")

'''
This function prints the headers for station information when listing station
data.
Requires no parameters and prints within the function
'''
def stationHeaders():
    print("ID\t\tName\t\t\t\t\t\t\t\t\tLatitude\t\tLongitude\t\tCapac." +
        "\tBikes\tDocks")

'''
This function displays a list all of bike stations with bicycles, sorted
by the amount of available bicycles at each station (use sortByAvailible)
The parameter is the list of all bicycle stations
Returns a list of bicycle stations that have at least one bike available,
sorted from highest to lowest by available
'''
def allStationsWithBikes(bikeStationList):
    #Initializes a list to store all stations with available bikes
    availableStations = []

    #Iterates through each station in the data
    for station in bikeStationList:
        #Checks if a bicycle is available at that specific station
        if checkBikeAvailable(station):
            #Adds it to the list  of stations with available bicycles
            availableStations.append(station)

    #Returns a sorted list of stations with available bicycles
    return insertionSort(availableStations)

'''
This function sorts a by bicycles available, largest to smallest. Defines a
swap function within the sort to make swapping elments easier
The parameter is the list of available bikes to be sorted
Returns a list ofsorted available bicycles
'''
def insertionSort(availableList):
    '''
    This function swaps two elements in the provided list
    The parameter array is the list; i and j are the positions in the list to be
    switched
    '''
    def swap(array, i, j):
        #Swaps the values at the positions provided
        array[i], array[j] = array[j], array[i]

    #Initializes position value i
    i = 1

    #Goes through entire available list
    while i < len(availableList):
        #Initializes position value j
        j = i

        #Checks if previous element is less than current element
        while j > 0 and (availableList[j - 1]["numBikesAvailable"] < 
            availableList[j]["numBikesAvailable"]):

            #Swaps the two elements in the list and continues searching from
            #the position before
            swap(availableList, j, j - 1)
            j -= 1

        #Checks next element
        i +=1

    #Returns the sorted list
    return availableList


'''
This function prints out a formatted list of provided stations
The parameter is a list of stations to print out
'''
def printStations(stationList):
    #Prints the headers for the information
    print()
    stationHeaders()

    #Goes through every station in the list of stations
    for station in stationList:
        #Prints out the station information 
        stationInfo(station)
        print()

'''
This function acquires the latitude and longitude of a bike station and
puts them into a value pair to be used for directions later on
The parameter is the selected bicycle station
Returns a tuple (latitude, longitude) of the bicycle station
'''
def aquireCoordinates(bikeStation):
    #Returns a tuple (latitude, longitude) of the bicycle station
    return (bikeStation["lat"], bikeStation["lon"])

'''
This function uses the northOrSouth and eastOrWest functions to output the
direction the user should go with the inputted start station, station1 and
the end station, station2
The parameter station1 is the start location and station2 is the end 
location the user wishes to go to
Returns a set of instructions in which direction to go using station1 as
the start location and station2 as the desired end location
'''
def giveDirections(station1, station2):
    #Gets the coordinates of the first and second station?
    coords1 = aquireCoordinates(station1)
    coords2 = aquireCoordinates(station2)

    #Returns the directions to the user
    return (northOrSouth(coords1[0], coords2[0]) + 
        eastOrWest(coords1[1], coords2[1]))


'''
This function uses latitude1 and latitude2 as the start and end latitude
respectively to determine if the user should go north or south or stay
The parameter latitude1 is the start latitude and latitude2 is the desired
end latitude to reach
Returns either 'North', 'South', or '' depending on which direction the 
user should go to reach latitude2
'''
def northOrSouth(lat1, lat2):
    #Checks if the latitude is more than or less than the starting location
    if lat2 > lat1 :
        #Returns NORTH if the desired location is above the initial location
        return "NORTH"
    elif lat2 <  lat1:
        #Returns SOUTH if the desired location is below the initial location
        return "SOUTH"
    else:
        #Doesn't return anything if the final location is the same latitude
        return ""

'''
This function uses longitude1 and longitude2 as the start and end latitude
respectively to determine if the user should go east or west or stay
The parameter longitude1 is the start latitude and longitude2 is the desired
end latitude to reach
Returns either 'East', 'West', or '' depending on which direction the 
user should go to reach longitude2
'''
def eastOrWest(lon1, lon2):
    #Returns EAST if the desired location is to the right of the initial
    if lon2 > lon1:
        return "EAST"
    elif lon2 < lon1:
        #Returns WEST if the desired location is to the left of the initial
        return "WEST"
    else:
        #Doesn't return anything if the final location is the same longitude
        return ""

'''
This function finds and displays all the stations that have their docks
full
The parameter is the list of bicycle stations
Returns the list of bicycle stations that are full
'''
def fullStations(bikeStationList):
    #Initializes a list for stations that are full of bicycles
    fullStations = []

    #Checks every station in the list of stations
    for station in bikeStationList:
        #Adds to the list if the amount of available bicycles are the same as 
        #capacity
        if station["numBikesAvailable"] == station["capacity"]:
            fullStations.append(station)

    #Returns the list of full stations
    return fullStations

'''
This function finds the specific station requested by the user using the ID
provided by them. Keeps asking until the user gives a valid ID or quits.
The parameter is the list of bicycle stations
Returns either the station if the selection was successful or returns None
if no station was selected
'''
def findStation(bikeStationList):
    #Keeps repeating until a station is found
    while True:
        #Asks the user for the ID of the station they want to find
        ID = input("\nPlease enter the ID for the bicycle station: ")

        #
        for station in bikeStationList:
            if ID == station["stationId"]:
                return station

        print("\nStation does not exist!")

        if input("Enter Y to search again ").lower() != "y":
            return None
            

'''
This function acts as the main interface of the program where the user may
choose an option to complete an action. Displays and organizes information
on the screen.
The parameter is the list of bicycle stations
Doesn't return anything
'''
def userInterface(bikeStationList):
    #Prints the interface and instructions to the screen
    print("WELCOME TO BIKE SHARE\n" + "-" * 51 + "\n")
    print("1. Rent Bike\n2. Return Bike\n3. Check if bikes are available" +
        "\n4. To see stations with bicycles available" +
        "\n5. To see all full stations\n6. To get information of a " +
        "specific bicycle station\n7. To get directions\n" + "=" * 51)

    #Initializes an integer to hold which choice the user decides on
    choice = -1

    try:
        #Attempts to take in the user's choice as an integer
        choice = int(input("Choose which option to do: "))
    except:
        pass

    #Checks which number the user chose
    if choice == 1:
        #Executes function for renting a bike
        rentBike(findStation(bikeStationList))
    elif choice == 2:
        #Executes function for returning a bike
        returnBike(findStation(bikeStationList))
    elif choice == 3:
        #Asks the user to find the station first
        station = findStation(bikeStationList)

        #Makes sure the bicycle station exists and that a bike is there
        if checkBikeAvailable(station):
            #Lets user know how many bicycles are available
            print("Bikes available! There are", 
                station["numBikesAvailable"], "available!")
        elif station == None:
            #Lets the user know their input was invalid
            print("Invalid Input")
        else:
            #Tells the user that there are no bikes here
            print("No bicycles are available.")
    elif choice == 4:
        #Executes the function to print all stations with bicycles
        printStations(allStationsWithBikes(bikeStationList))
    elif choice == 5:
        #Executes the function to print all stations full of bicycles
        printStations(fullStations(bikeStationList))
    elif choice == 6:
        #Asks the user to find the station first
        station = findStation(bikeStationList)

        #Checks if the station exists or not
        if station == None:
            #Lets the user know the input was invalid
            print("Invalid input.")
        else:
            #Prints the station information
            printStations([station])
    elif choice == 7:
        #Asks the user for the start and end station locations
        print("\nPlease enter your starting location:", end = "")
        location1 = findStation(bikeStationList)
        print("\nPlease enter your desired destination:", end = "")
        location2 = findStation(bikeStationList)

        #Checks if both stations exist
        if location1 != None and location2 != None:
            #Prints the directions to the location
            print("\nDirections: " + giveDirections(location1, location2))
        else:
            #Lets the user know they inputted the wrong information
            print("\nOne or more inputs were invalid.")
    else:
        #Lets the user know they inputted an invalid choice
        print("Invalid input.")

        

'''
This function runs the main code for the program
Doesn't require any parameters or returns anything
'''
def main():
    #Creates a boolean to track if the program is running and reads in the list
    #of bicycle stations from the website
    running = True
    bikeStationList = readInData()

    #Repeats the main code until the running boolean is disabled
    while running:
        #Runs the user interface function using the list of bicycle stations
        userInterface(bikeStationList)

        #Asks the user if they want to keep using the program
        if input("\n\nEnter Y to restart BIKE SHARE: ").lower() != "y":
            #Disables the running boolean
            running = False

        #Indents a huge amount of times to make it seem like the console has
        #been cleared (but also lets you check the history)
        print("\n" * 50)

'''
Only runs the main program if the file is being run in the main namespace
'''
if __name__ == '__main__':
    #Executes the main code
    main()
else:
    #Lets user know functions and attributes from this file have been imported
    print("IMPORTED: ProjectFinal.py")
