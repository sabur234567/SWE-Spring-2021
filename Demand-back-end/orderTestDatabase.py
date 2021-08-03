from order import Order
import database_util
from mapping import routingUtil
from datetime import datetime

if __name__ == '__main__':
    database = database_util.DatabaseUtil()
    #database.insert_user("joe@gmail.com", "Joe", "Smith", "1/1/21", "joeUsername", "joePassword")

    order_obj = Order("order122", "covid", "3001 S Congress Ave, Austin, TX 78704")
    print(order_obj.__str__())
    order_dict = order_obj.__dict__

    database.insert_order(order_dict)
    ordertable = database.read_table("Orders")
    orderrow = database.read_order(order_obj.order_id)