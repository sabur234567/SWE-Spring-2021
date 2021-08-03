import mysql.connector
import null


def connect_to_database():
    # Try/except block to validate connection
    try:
        db = mysql.connector.connect(user='developer', password='Team11_supplyDeveloper', host='localhost',
                                     database='team11_supply', auth_plugin='mysql_native_password')
    except Exception as e:
        raise Exception(e)

    return db


class DatabaseUtil:
    def __init__(self):
        self.connection = connect_to_database()
        if self.connection.is_connected():
            database_info = self.connection.get_server_info()
            print("NOW CONNECTED TO MYSQL SERVER v", database_info)
            self.cursor = self.connection.cursor()
            print("You are connected to the database")
        else:
            raise Exception('You are not connected to the database')

    def insert_vehicle(self, vehicle):
        sql = "INSERT INTO Vehicle (vin, plate_num, make, model, speed, odometer, trip_time, " \
              "longitude, latitude, is_equipped, is_damaged, en_route) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s ,%s, %s) "
        location = vehicle["location"]
        val = (vehicle["vin"], vehicle["plate_num"], vehicle["make"], vehicle["model"], vehicle["speed"],
               vehicle["odometer"], vehicle["trip_time"], location[0], location[1], vehicle["is_equipped"],
               vehicle["is_damaged"], vehicle["en_route"])
        print(sql, val)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print(self.cursor.rowcount, "was inserted")

    def insert_fleet(self, fleet):
        sql = "INSERT INTO Fleet (fleetID, manufacturer, service_type, model) VALUES (%s, %s, %s, %s) "

        val = (fleet["fleetID"], fleet["manufacturer"], fleet["service_type"], fleet["model"])
        print(sql)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print(self.cursor.rowcount, "was inserted")

    def update_vehicle_location(self, vin, location):
        sql = "UPDATE Vehicle set longitude = %s, latitude = %s where vin = %s"
        longitude = location[0]
        latitude = location[1]
        self.cursor.execute(sql, (longitude, latitude, vin))
        self.connection.commit()
        print(self.cursor.rowcount, "was inserted")

    def insert_dispatch(self, dispatch):
        sql = "INSERT INTO Dispatch (dispatch_id, time_of_reception, time_of_processing, time_of_completion, " \
              "destination_longitude, destination_latitude, origin_longitude, origin_latitude, " \
              "dispatched, eta, duration, distance, order_id, av_plate_num) VALUES (%s, %s, %s," \
              "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        val = (dispatch["dispatch_id"], dispatch["time_of_reception"], dispatch["time_of_processing"],
               dispatch['time_of_completion'], dispatch["destination_longitude"], dispatch["destination_latitude"],
               dispatch["origin_longitude"], dispatch["origin_latitude"], dispatch["dispatched"], dispatch["eta"],
               dispatch["duration"], dispatch["distance"], dispatch["order_id"], dispatch["av_plate_num"])
        print(sql)
        self.cursor.execute(sql, val)
        self.connection.commit()
        print(self.cursor.rowcount, "was inserted")

    def read_dispatch(self, order_id):
        select_statement = "SELECT * FROM Dispatch WHERE order_id=%s"
        dispatch = {}
        dispatch_tuple = ()
        try:
            self.cursor.execute(select_statement, order_id)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            dispatch_tuple = result

        assert dispatch_tuple != (), 'dispatch not found'
        dispatch['dispatch_id'] = dispatch_tuple[0]
        dispatch['time_of_reception'] = dispatch_tuple[1]
        dispatch['time_of_processing'] = dispatch_tuple[2]
        dispatch['time_of_completion'] = dispatch_tuple[3]
        dispatch['destination_longitude'] = dispatch_tuple[4]
        dispatch['destination_latitude'] = dispatch_tuple[5]
        dispatch['origin_longitude'] = dispatch_tuple[6]
        dispatch['origin_latitude'] = dispatch_tuple[7]
        dispatch['dispatched'] = dispatch_tuple[8]
        dispatch['eta'] = dispatch_tuple[9]
        dispatch['duration'] = dispatch_tuple[10]
        dispatch['distance'] = dispatch_tuple[9]
        dispatch['orderID'] = dispatch_tuple[11]
        dispatch['av_plate_num'] = dispatch_tuple[12]

        return dispatch

    def read_dispatches(self):
        select_statement = "SELECT * FROM Dispatch"
        try:
            self.cursor.execute(select_statement)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            return result

    def read_vehicle(self, vin):
        select_statement = "SELECT * FROM Vehicle WHERE vin= "+vin
        vehicle = {}
        vehicle_tuple = ()
        try:
            self.cursor.execute(select_statement)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            vehicle_tuple = result

        assert vehicle_tuple != (), 'vehicle not found'
        vehicle['vin'] = vehicle_tuple[0]
        vehicle['plate_num'] = vehicle_tuple[1]
        vehicle['make'] = vehicle_tuple[2]
        vehicle['model'] = vehicle_tuple[3]
        vehicle['speed'] = vehicle_tuple[4]
        vehicle['odometer'] = vehicle_tuple[5]
        vehicle['trip_time'] = vehicle_tuple[6]
        vehicle['location'] = (vehicle_tuple[7], vehicle_tuple[8])
        vehicle['is_equipped'] = vehicle_tuple[9]
        vehicle['is_damaged'] = vehicle_tuple[10]
        vehicle['en_route'] = vehicle_tuple[11]

        return vehicle

    def read_vehicles(self):
        select_statement = "SELECT * FROM Vehicle"
        vehicles_list = []
        returning_vehicles = []
        try:
            self.cursor.execute(select_statement)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchall()
            vehicles_list = result

        assert vehicles_list != (), 'vehicles not found'
        for i in vehicles_list:
            vehicles = {'vin': i[0], 'plate_num': i[1], 'make': i[2], 'model': i[3], 'speed': i[4], 'odometer': i[5],
                        'trip_time': i[6], 'location': (i[7], i[8]), 'is_equipped': i[9], 'is_damaged': i[10],
                        'en_route': i[11]}
            returning_vehicles.append(vehicles)

        return returning_vehicles

    def read_fleets(self):
        select_statement = "SELECT * FROM Fleet"
        try:
            self.cursor.execute(select_statement)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            return result

    def read_fleet(self, fleet_id):
        select_statement = "SELECT * FROM Fleet WHERE fleetID=%s"
        fleet = {}
        fleet_tuple = ()
        try:
            self.cursor.execute(select_statement, fleet_id)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            fleet_tuple = result

        assert fleet_tuple != (), 'fleet not found'
        fleet['fleetID'] = fleet_tuple[0]
        fleet['manufacturer'] = fleet_tuple[1]
        fleet['service_type'] = fleet_tuple[2]
        fleet['model'] = fleet_tuple[3]

        return fleet

    def close_connection(self):
        self.connection.close()
        print("MySQL connection is closed")

    def read_vehicle_location(self, vin):
        select_statement = "SELECT longitude, latitude FROM Vehicle WHERE vin=%s"
        try:
            self.cursor.execute(select_statement, vin)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            return result

    def get_available_vehicle(self):
        select_statement = "SELECT * FROM Vehicle WHERE en_route=False"
        vehicle_tuple = ()
        try:
            self.cursor.execute(select_statement)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            vehicle_tuple = result

        assert vehicle_tuple != (), 'vehicle not found'
        vehicle = {'vin': vehicle_tuple[0], 'plate_num': vehicle_tuple[1], 'make': vehicle_tuple[2],
                   'model': vehicle_tuple[3], 'speed': vehicle_tuple[4], 'odometer': int(vehicle_tuple[5]),
                   'trip_time': vehicle_tuple[6], 'location': (int(vehicle_tuple[7]), int(vehicle_tuple[8])),
                   'is_equipped': vehicle_tuple[9], 'is_damaged': vehicle_tuple[10], 'en_route': vehicle_tuple[11]}

        return vehicle
