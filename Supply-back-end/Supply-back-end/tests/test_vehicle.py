import sys
from unittest import TestCase
from vehicle import Vehicle

mapping = "/home/team11-project/common-services-back-end/"
sys.path.insert(0, mapping)
from routingUtil import *



class TestVehicle(TestCase):
    def test_class_methods(self):
        test_vehicle = Vehicle('xyz123', 1)
        status_report1 = test_vehicle.report_status()

        TestCase.assertTrue(self, status_report1['speed'] == 0)
        TestCase.assertTrue(self, status_report1['odometer'] == 0)
        TestCase.assertTrue(self, status_report1['trip_time'] == 0)

        downtown_atx = routingUtil.get_geolocation('Downtown Austin, TX')
        test_route = routingUtil.get_route(test_vehicle.location, downtown_atx)
        assert test_route is not None
        test_vehicle.set_route(test_route)
        test_vehicle.step_route(3)
        status_report2 = test_vehicle.report_status()

        msg = 'Speed: ' + str(status_report2['speed'])
        TestCase.assertTrue(self, status_report2['speed'] > 0, msg)
        msg = 'Odometer: ' + str(status_report2['odometer'])
        TestCase.assertTrue(self, status_report2['odometer'] > 0, msg)
        msg = 'Trip time: ' + str(status_report2['trip_time'])
        TestCase.assertTrue(self, status_report2['trip_time'] > 0, msg)
        TestCase.assertTrue(self, status_report2['en_route'] is True)

        test_vehicle.run()
        status_report3 = test_vehicle.report_status()
        TestCase.assertAlmostEqual(self, status_report3['location'][0], downtown_atx[0], 3)
        TestCase.assertAlmostEqual(self, status_report3['location'][1], downtown_atx[1], 3)
        TestCase.assertTrue(self, status_report3['speed'] == 0)
        TestCase.assertTrue(self, status_report3['en_route'] is False)

        test_vehicle_dict = test_vehicle.__dict__()

        for key in status_report3:
            print(key)
            TestCase.assertFalse(self, isinstance(type(test_vehicle_dict.get(key)), type(None)), key)
