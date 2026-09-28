import datetime

#defining package class
class Package:
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, status, truck_number):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.status = status
        self.deliveryTime = None
        self.departureTime = None
        self.truck_number = truck_number

    def __str__(self):
        #creating rules to have the correct output displayed on the package info GUI
        if self.status != "Delivered":
            delivery_str = "Not Delivered"
        else:
            delivery_str = f"{self.deliveryTime}"
            #having the correct output for packages that are delayed
        if self.status in ["At Hub", "Delayed - Flight Arriving at 9:05 AM"]:
            depart_str = "Waiting"
        else:
            depart_str = f"{self.departureTime}"
        return (f"{self.ID}, Truck ID: {self.truck_number} {self.address}, {self.city}, {self.state}, {self.zipcode}, {self.weight},"
                f"{self.deadline}, {self.status}, {depart_str}, {delivery_str}")

    #checking to see which status a package is currently in and to update accordingly
    def update_status(self, convert_timedelta):
        #creating an instance to allow convert_timedelta and datetime to be able to be measured against
        if isinstance(convert_timedelta, datetime.time):
            convert_timedelta = datetime.timedelta(hours=convert_timedelta.hour, minutes=convert_timedelta.minute,
                                                  seconds=convert_timedelta.second)
        #setting the delayed packages from CSV
        delayed_packages = [6, 25, 28, 32]
        flight_arrival_time = datetime.timedelta(hours=9, minutes=5)
        if self.ID == 9:
            #having the error not be fixed until the appropriate time for package 9
            if convert_timedelta >= datetime.timedelta(hours=10, minutes=20):
                self.address = "410 S State St"
                self.zipcode = "84111"
            else:
                self.address = "300 State St"
                self.zipcode = "84103"
        #having correct output for packages that are delayed or otherwise
        if self.ID in delayed_packages and convert_timedelta < flight_arrival_time:
            self.status = "Delayed - Flight Arriving at 9:05 AM"

        elif self.departureTime is None or  convert_timedelta < self.departureTime:
            self.status = "At Hub"

        elif self.deliveryTime is not None and convert_timedelta >= self.deliveryTime:
            self.status = "Delivered"

        else:
            self.status = "En Route"