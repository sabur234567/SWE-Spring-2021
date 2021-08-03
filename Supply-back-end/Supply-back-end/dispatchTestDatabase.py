import database_util
import datetime
from mapping import routingUtil
from dispatch import Dispatch
from order import Order

if __name__ == '__main__':
    order_obj = Order("order122", "covid", "3001 S Congress Ave, Austin, TX 78704v")
    dispatch_obj = Dispatch(order_obj)
    print(dispatch_obj.__str__())
    database = database_util.DatabaseUtil()
    database.insert_dispatch(dispatch_obj.__dict__)
    dispatchtable = database.read_table("Dispatch")
    dispatchrow = database.read_dispatch(dispatch_obj.dispatch_id)