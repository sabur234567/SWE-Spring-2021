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
        self._fleet_id = "ID" + self._service_type
        self._manufacturer = None
        self._service_type = None
        self._make = None
        self._model = None


#    def get_available_av(self):
#        if self._av is not None:
#        vehicle_request = requests.get("http://localhost:8081/supply-back-end/vehicle_api/v1/available_vehicle")
#        response = vehicle_request.json()
#        assert response['data'] != '', 'No vehicle available'
        # choose only one car to use
#        self._av = vehicle.Vehicle(response["data"]["plate_num"])
#        self._origin = self._av.location()

    # def create_route(self):
    #     if self._av is None:
    #         raise Exception('This dispatch does not have an an')
    #     elif self._route is not None:
    #         raise Exception('This dispatch has a route')
    #
    #     self._route = routingUtil.get_route(self._origin, self._destination)
    #     self._av.set_route(self._route)
    #     self._duration = self._route["routes"][0]["duration"]  # in seconds
    #     self._distance = self._route["routes"][0]["distance"]  # in meters
    #     seconds = time.time()
    #     # adding a three minute grace period to the ETA
    #     self._eta = time.ctime(seconds + self._duration + 180)
    #
    # def start_processing(self):
    #     if self._time_of_processing is not None:
    #         raise Exception("This dispatch has been processed")
    #     self._time_of_processing = datetime.now()
    #     self._order.start_processing()
    #     self.get_available_av()
    #
    #     print("\n***\nNow starting vehicle simulation and returning order request.\n***\n")
    #     thread1 = Thread(target=self._av.run)
    #     thread1.start()
    #     self._dispatched = True
    #
    # def complete_dispatch(self):
    #     if self._time_of_processing is None:
    #         raise Exception('This dispatch has not been processed')
    #     if self._route is None:
    #         raise Exception('This dispatch never received a route')
    #     if self._time_of_completion is not None:
    #         raise Exception('This dispatch is completed')
    #
    #     self._time_of_completion = datetime.now()
    #     self._order.complete_order()
    #
    #     return self._order

    @property
    def _fleet_id(self):
        return self._fleet_id

    @property
    def _manufacturer(self):
        return self._manufacturer

    @property
    def _service_type(self):
        return self._service_type

    @property
    def _make(self):
        return self._make

    @property
    def origin(self):
        return self._model


    def __dict__(self):
        d = {'fleet_id': self._fleet_id, 'manufacturer': self._manufacturer,
             'service_type': self._service_type, 'make': self._make,
             'model': self._model}
        return d

    def __str__(self):
        return str(self.__dict__())
