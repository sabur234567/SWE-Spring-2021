import time

import requests
import json
import routingUtil


class Vehicle:
    def __init__(self, plate_num, vin, model='covid19', params=None):
        self._vin = vin
        self._plate_num = plate_num
        self._make = 'NVIDIA'
        self._model = model
        self._route = None
        if params is None:
            self._speed = 0
            self._odometer = 0
            self._trip_time = 0
            self._location = routingUtil.get_geolocation("3001 S Congress Ave, Austin, TX 78704")
            self._is_equipped = True
            self._is_damaged = False
            self._en_route = False
        else:
            assert type(params) is dict, 'TypeError params is not of type dict'
            assert len(params) == 9, 'params should only contain 9 entries'
            self._speed = params['speed']
            self._odometer = params['odometer']
            self._trip_time = params['trip_time']
            self._location = params['location']
            self._is_equipped = params['is_equipped']
            self._is_damaged = params['is_damaged']
            self._en_route = params['en_route']

    def report_status(self):
        status = {'speed': self._speed, 'odometer': self._odometer, 'trip_time': self._trip_time,
                  'location': self._location, 'route': self._route, 'is_equipped': self._is_equipped,
                  'is_damaged': self._is_damaged, 'en_route': self._en_route}
        return status

    def accelerate(self):
        self._speed += 5

    def brake(self):
        if self._speed < 5:
            self._speed = 0
        else:
            self._speed -= 5

    def post_location(self):
        data = {'vin': self._vin, 'location': self._location}
        location_request = requests.post("https://supply.team11.sweispring21.tk/supply-back-end/vehicle_api/v1"
                                         "/vehicle_location", json.dumps(data))
        response = location_request.json()
        return response['status']

    def set_route(self, route):
        self._route = route
        print("New route received.")

    def run(self):
        self._trip_time = 0
        destination = self._route["waypoints"][1]["name"]
        if destination == "":
            locations = (self._route["routes"][0]["legs"][0]["summary"]).split(", ")
            destination = locations[1]
        print("Starting route to " + destination)
        self.step_route()

    def end_route(self):
        # do equipment check and update at subclass level
        self._route = None
        self._en_route = False
        self._speed = 0
        return "AV has arrived at its destination."

    def equip_vehicle(self):
        # do further equipment at subclass level
        self._is_equipped = True

    def step_route(self, maneuvers=0):
        assert maneuvers >= 0, "maneuvers cannot be less than 0"
        self._en_route = True
        print("\nDriving!")
        steps = self._route["routes"][0]["legs"][0]["steps"]
        num_of_steps = len(steps)
        end_route = True
        if maneuvers > 0:
            assert num_of_steps >= maneuvers, "The route only has %ds steps." % num_of_steps
            if maneuvers != num_of_steps:
                num_of_steps = maneuvers
                end_route = False
        count = 0
        time.sleep(5)
        while count < num_of_steps:
            step = steps[count]
            maneuver = step["maneuver"]
            print(maneuver["instruction"])
            self._location = maneuver["location"][0], maneuver["location"][1]
            self.post_location()  # added send location for av simulator
            self._odometer += step["distance"]  # in meters
            self._trip_time += step["duration"]  # in seconds
            self._speed = self.avg_speed()
            time.sleep(3)
            count += 1
        print("Average speed: " + str(self.avg_speed()) + "km/h")
        if end_route:
            self.end_route()

    def avg_speed(self):
        if self._trip_time != 0:
            return round((self._odometer / 1000) / (self._trip_time / 3600), 2)

    def __dict__(self):
        vehicle = self.report_status()
        vehicle['vin'] = self._vin
        vehicle['plate_num'] = self._plate_num
        vehicle['make'] = self._make
        vehicle['model'] = self._model
        return vehicle

    def __str__(self):
        string = self._make + ' ' + self._model + '\n'
        string += 'VIN: ' + self._vin + '\nLicense Plate: ' + self._plate_num
        return string

    @property
    def speed(self):
        return self._speed

    @property
    def trip_time(self):
        return self._trip_time

    @property
    def en_route(self):
        return self._en_route

    @en_route.setter
    def en_route(self, boolean):
        self._en_route = boolean

    @property
    def odometer(self):
        return self._odometer

    @property
    def is_equipped(self):
        return self._is_equipped

    @is_equipped.setter
    def is_equipped(self, boolean):
        self._is_equipped = boolean

    @property
    def is_damaged(self):
        return self._is_damaged

    @is_damaged.setter
    def is_damaged(self, boolean):
        self._is_damaged = boolean

    @property
    def plate_num(self):
        return self._plate_num

    @property
    def location(self):
        return self._location

    @property
    def route(self):
        return self._route


def main():  # added main for proof of functionality
    test_car1 = Vehicle("xyz", 1)
    test_car2 = Vehicle("abc", 2)
    origin = routingUtil.get_geolocation("3001 S Congress Ave, Austin, TX 78704")
    destination1 = routingUtil.get_geolocation("4005 Banister Ln, Austin, TX 78704")
    destination2 = routingUtil.get_geolocation("2015 E Riverside Dr, Austin, TX 78741")
    route1 = routingUtil.get_route(origin, destination1)
    route2 = routingUtil.get_route(origin, destination2)
    test_car1.set_route(route1)
    test_car2.set_route(route2)
