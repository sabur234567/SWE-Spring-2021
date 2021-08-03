import time
import sys
from unittest import TestCase
from vehicle import Vehicle
from dispatch import Dispatch

common_services = "/home/team11-project/common-services-back-end"
sys.path.append(common_services)
from order import Order

class TestDispatch(TestCase):
    def test_get_available_av(self):
        test_order = Order('tester', 'covid19', '1100 Congress Ave, Austin, TX 78704')
        test_dispatch = Dispatch(test_order)

        TestCase.assertTrue(self, test_dispatch.av is None)
        TestCase.assertTrue(self, test_dispatch.origin is None)

        test_dispatch.get_available_av()

        TestCase.assertFalse(self, test_dispatch.av is None)
        TestCase.assertTrue(self, type(test_dispatch.av) is Vehicle)
        TestCase.assertTrue(self, test_dispatch.origin is not None)
        with self.assertRaises(Exception):
            test_dispatch.get_available_av()

    def test_create_route(self):
        test_order = Order('tester', 'covid19', '1100 Congress Ave, Austin, TX 78704')
        test_dispatch = Dispatch(test_order)
        test_dispatch.start_processing()

        TestCase.assertTrue(self, test_dispatch.route is None)

        test_dispatch.create_route()

        with self.assertRaises(Exception):
            test_dispatch.create_route()
        TestCase.assertTrue(self, test_dispatch.route is not None)
        TestCase.assertTrue(self, type(test_dispatch.route) is dict)
        TestCase.assertTrue(self, test_dispatch.route is not {})
        TestCase.assertTrue(self, test_dispatch.distance is not None)
        TestCase.assertTrue(self, test_dispatch.duration is not None)
        TestCase.assertTrue(self, test_dispatch.eta is not None)
        eta = test_dispatch.eta
        msg = "ETA: " + str(eta)
        TestCase.assertTrue(self, test_dispatch.eta > time.ctime(time.time() + test_dispatch.duration), msg)
        TestCase.assertTrue(self, test_dispatch.duration > 0)
        TestCase.assertTrue(self, test_dispatch.distance > 0)

    def test_start_processing(self):
        test_order = Order('tester', 'covid19', '1100 Congress Ave, Austin, TX 78704')
        test_dispatch = Dispatch(test_order)
        test_dispatch.start_processing()

        TestCase.assertTrue(self, test_dispatch._time_of_processing is not None)
        TestCase.assertTrue(self, test_dispatch.order._is_confirmed is True)
        TestCase.assertTrue(self, test_dispatch.av is not None)
        TestCase.assertTrue(self, type(test_dispatch.av) is Vehicle)

    def test_complete_dispatch(self):
        test_order = Order('tester', 'covid19', '1100 Congress Ave, Austin, TX 78704')
        test_dispatch = Dispatch(test_order)

        with self.assertRaises(Exception):
            test_dispatch.complete_dispatch()

        test_dispatch.start_processing()

        with self.assertRaises(Exception):
            test_dispatch.complete_dispatch()

        test_dispatch.create_route()

        TestCase.assertTrue(self, test_dispatch.route is not None)

        complete_test_order = None
        msg = 'An order was returned'
        try:
            complete_test_order = test_dispatch.complete_dispatch()
        except:
            msg = 'No order was returned'
        TestCase.assertTrue(self, complete_test_order is not None, msg)
        TestCase.assertTrue(self, type(complete_test_order) is Order)
