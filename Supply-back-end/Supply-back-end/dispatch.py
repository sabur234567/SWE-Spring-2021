import sys
sys.path.append('../common-services-back-end')

from datetime import datetime
from threading import Thread
import requests
import vehicle
import time
import routingUtil


class Dispatch:
    def __init__(self, order):
        self._dispatch_id = "D_" + order.order_id
        self._time_of_reception = datetime.now()
        self._time_of_processing = None
        self._time_of_completion = None
        self._destination = order.geolocation
        self._origin = None
        self._route = None
        self._dispatched = False
        self._eta = None
        self._duration = None
        self._distance = None
        self._order = order
        self._av = None
        self._order_id = order.order_id
        self._av_plate_num = None

    def get_available_av(self):
        if self._av is not None:
            raise Exception('This dispatch has an av.')
        vehicle_request = requests.get("http://localhost:8081/supply-back-end/vehicle_api/v1/available_vehicle")
        response = vehicle_request.json()
        assert response['data'] != '', 'No vehicle available'
        # choose only one car to use
        self._av = vehicle.Vehicle(response["data"]["plate_num"], response["data"]["vin"])
        self._origin = self.av.location

    def create_route(self):
        if self._av is None:
            raise Exception('This dispatch does not have an an')
        elif self._route is not None:
            raise Exception('This dispatch has a route')

        self._route = routingUtil.get_route(self._origin, self._destination)
        self._av.set_route(self._route)
        self._duration = self._route["routes"][0]["duration"]  # in seconds
        self._distance = self._route["routes"][0]["distance"]  # in meters
        seconds = time.time()
        # adding a three minute grace period to the ETA
        self._eta = datetime.fromtimestamp(seconds + self._duration + 180).strftime("%Y-%m-%d %I:%M:%S")

    def start_processing(self):
        if self._time_of_processing is not None:
            raise Exception("This dispatch has been processed")
        self._time_of_processing = datetime.now()
        print('\n', self._dispatch_id, '\n')
        self._order.start_processing(self._dispatch_id)
        self.get_available_av()
        self.create_route()

        print("\n***\nNow starting vehicle simulation and returning order request.\n***\n")
        thread1 = Thread(target=self._av.run)
        thread1.start()
        self._dispatched = True

    def complete_dispatch(self):
        if self._time_of_processing is None:
            raise Exception('This dispatch has not been processed')
        if self._route is None:
            raise Exception('This dispatch never received a route')
        if self._time_of_completion is not None:
            raise Exception('This dispatch is completed')

        self._time_of_completion = datetime.now()
        self._order.complete_order()

        return self._order

    @property
    def time_of_processing(self):
        return self._time_of_processing
    
    @property
    def order(self):
        return self._order

    @property
    def order_id(self):
        return self._order.order_id

    @property
    def av(self):
        return self._av

    @property
    def origin(self):
        return self._origin

    @property
    def route(self):
        return self._route

    @property
    def dispatched(self):
        return self._dispatched

    @property
    def eta(self):
        return self._eta

    @property
    def duration(self):
        return self._duration

    @property
    def distance(self):
        return self._distance

    @property
    def dispatch_id(self):
        return self._dispatch_id

    @property
    def time_of_reception(self):
        return self._time_of_reception

    @property
    def time_of_completion(self):
        return self._time_of_completion

    @property
    def destination(self):
        return self._destination

    @property
    def order_id(self):
        return self._order_id

    @property
    def av_plate_num(self):
        return self._av_plate_num

    def __dict__(self):
        d = {'dispatch_id': self._dispatch_id, 'time_of_reception': self._time_of_reception,
             'time_of_completion': self._time_of_completion, 'time_of_processing': self._time_of_processing,
             'destination_longitude': self._destination[0], 'destination_latitude': self._destination[1],
             'origin_longitude': self._origin[0], 'origin_latitude': self._origin[1], 'dispatched': self._dispatched,
             'eta': self._eta, 'duration': self._duration, 'distance': self._distance, 'order_id': self._order_id,
             'av_plate_num': self._av_plate_num}
        return d

    def __str__(self):
        return str(self.__dict__())
