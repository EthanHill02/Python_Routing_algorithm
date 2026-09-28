#Ethan Hill
#Student ID: 011021273
#C950 Task 2 Project


from hashTable import hashTable
from package import Package
import csv
import truck
import datetime




#function to look up package ID and display relevant information
def lookup_id(packageID, check_time = None):
    found_package = package_table.lookup(packageID)
    if check_time is None:
        check_time = datetime.datetime.now().time()
    if found_package:
        found_package.update_status(check_time)
        return found_package
    else:
        print("No package found")
        return None



#importing csv file of addresses for package delivery
with open("CSV/Address_File.csv") as csv_file:
    CSV_Address = csv.reader(csv_file)
    CSV_Address = list(CSV_Address)

#importing csv file of distances for package delivery
with open("CSV/Distance_file.csv") as csv_file1:
    CSV_Distance = csv.reader(csv_file1)
    CSV_Distance = list(CSV_Distance)

#importing csv file of package information for package delivery
with open("CSV/Package_file.csv") as csv_file2:
    CSV_Package = csv.reader(csv_file2)
    CSV_Package = list(CSV_Package)



#loading data from csv into hashmap
def load_data(file_name, package_hash_table):
    with open(file_name) as package_details:
        package_details = csv.reader(package_details)
        for package in package_details:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pStatus = "At Hub"
            ptruck_number = package[7]

            p = Package(pID, pAddress, pCity, pState, pZipcode, pWeight, pDeadline, pStatus, ptruck_number)

            package_hash_table.insert(pID, p)


# creating hash table
package_table = hashTable()

#load packages into hash table
load_data("CSV/Package_File.csv", package_table)

#determining the distance between two addresses
def distance_between_addresses(x_address, y_address):
    x_index = find_address(x_address)
    y_index = find_address(y_address)

    distance = CSV_Distance[x_index][y_index]
    if distance == '':
        distance = CSV_Distance[y_index][x_index]
    return float(distance)


#getting an address from CSV file
def find_address(address):
    for row in CSV_Address:
        if address == row[2]:
            return int(row[0])
    return None

#creating truck objects
truck1 = truck.Truck(16,18, None, [13,14,15,16,19,20,29,30,31,34,37,40,1,4,7,21], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=8),1)
truck2 = truck.Truck(16,18, None, [3,6,18,25,28,32,36,38,2,5,8,10,11,12,17,22], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=9, minutes= 5),2)
truck3 = truck.Truck(16,18, None, [9,23,24,26,27,33,35,39], 0.0,
                     "4001 South 700 East", datetime.timedelta(hours=10, minutes=20),3)

#implementing nearest neighbor algorithm
def delivery_algorithm(truck):
    #creating a hash map of all unvisited points
    truck_map = []
    for ID in truck.packages:
        package = package_table.lookup(ID)
        package.departureTime = truck.time
        package.truck_number = truck.truck_id
        #add packages into truck_map for unvisited points
        truck_map.append(package)
    #setting current location to the first package on the truck
    current_location = truck.address
    #setting total distance to 0 to be able to add final values together
    distance_traveled = 0
    #cycles through list until no packages are left
    while len(truck_map) > 0:
        #creating a rule to deliver package 15 first to meet deadline
        p15 = next((p for p in truck_map if p.ID == 15), None)

        if p15:
            closest_package = p15
            min_distance = distance_between_addresses(current_location, p15.address)
        else:
            min_distance = float('inf')
            closest_package = None

            for package in truck_map:
                distance = distance_between_addresses(current_location, package.address)
                if distance < min_distance:
                    min_distance = distance
                    closest_package = package
        #adding distance taken to deliver package to total mileage
        distance_traveled += min_distance
        #setting current location as the package that was last delivered
        current_location = closest_package.address
        #removing closest package from the array
        truck_map.remove(closest_package)
        #adding the mileage together for each individual truck
        truck.mileage += min_distance
        #updates time it took driver to deliver package
        truck.time +=datetime.timedelta(hours=min_distance/18.0)
        closest_package.deliveryTime = truck.time
    return_distance = distance_between_addresses(current_location, truck.address)
    distance_traveled += return_distance
    truck.mileage += return_distance
    truck.time += datetime.timedelta(hours=return_distance / 18.0)
    return distance_traveled


#putting each truck through the loading and delivery process
delivery_algorithm(truck1)
delivery_algorithm(truck2)
#code below does not allow truck 3 to depart before either truck one or two has returned
truck3.depart_time = max(datetime.timedelta(hours=10, minutes=20), min(truck1.time, truck2.time))
truck3.time = truck3.depart_time
delivery_algorithm(truck3)













#creating title for GUI
print("Welcome to WGUPS's system database. Please choose from the following options")
print("-------------------------------------------------------------------------------")
print("1. Package information/status")
print("2. Truck information/status")

user_input = input()
#tracking user input and displaying ways to get package information
if user_input == "1":
    print("Welcome to WGUPS's package hub!")
    time_input = input("Enter a time you would like to view the packages in HH:MM:SS")
    h, m, s = time_input.split(":")
    check_time = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
    print("Would you like to view the status/information of one package or all? Please type one or all")
    package_info1 = input()
    if package_info1 == "all":
        #checking status of all packages per user input
        print("All packages are listed below alongside any identifying information regarding them.")
        for package_ID in range(1,41):
            all_packages = lookup_id(package_ID, check_time)
            print(all_packages)
    else:
        #asking more to get the ID that the user wants to display
        print("Please type the ID of the package you wish to view")
        specific_package_id = int(input())
        one_package = lookup_id(specific_package_id, check_time)
        print(one_package)

#printing output of all truck mileages and their combined total
elif user_input == "2":
    print("The mileage of each truck is as follows:")
    print("Truck 1:", truck1.mileage)
    print("Truck 2:", truck2.mileage)
    print("Truck 3:", truck3.mileage)
    print("Total mileage")
    print("Total:", truck1.mileage + truck2.mileage + truck3.mileage)


