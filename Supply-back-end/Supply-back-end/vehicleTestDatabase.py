
from vehicle import Vehicle
import database_util
import datetime
from mapping import routingUtil

if __name__ == '__main__':
    vehicle_obj = Vehicle("xyz123")
    print(vehicle_obj.__str__())
    database = database_util.DatabaseUtil()
    database.insert_vehicle(vehicle_obj.__dict__)
    vehicletable = database.read_table("Vehicle")
    vehiclerow = database.read_vehicle(vehicle_obj.get_plate_num())