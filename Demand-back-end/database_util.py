import mysql.connector
import null


def connect_to_database():
    # Try/except block to validate connection
    try:
        db = mysql.connector.connect(user='developer', password='Team11_developer', host='localhost',
                                     database='team11_demand')
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

    def insert_user(self, user):
        assert user != {}, 'user cannot be empty'
        sql = """INSERT INTO TaasUser (email, FName, LName, DOB, username, password) VALUES (%s,%s,%s,%s,
                %s,%s) """
        print(sql)
        val = (user['email'], user['FName'], user['LName'], user['DOB'], user['username'], user['password'])

        self.cursor.execute(sql, val)
        self.connection.commit()
        print(self.cursor.rowcount, "was inserted")

    def insert_order(self, order):
        sql = "INSERT INTO Orders (order_id, price, date_fulfilled, date_processed, date_created, service_type," \
              " address, is_confirmed, is_complete, is_paid, dispatch_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, " \
              "%s, %s, %s)"
        val = (order["order_id"], order["price"], order["date_fulfilled"], order["date_processed"],
               order["date_created"], order["service_type"], order['address'], order["is_confirmed"],
               order["is_complete"], order["is_paid"], order["dispatch_id"])

        self.cursor.execute(sql, val)
        self.connection.commit()
        print(self.cursor.rowcount, "was inserted")

    def read_user(self, user_name, password):
        select_statement = "SELECT * FROM TaasUser WHERE userName=%s AND password=%s"
        user = {}
        user_tuple = ()
        try:
            self.cursor.execute(select_statement, (user_name, password))
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            user_tuple = result

        assert user_tuple != (), 'user not found'
        user['email'] = user_tuple[0]
        user['FName'] = user_tuple[1]
        user['LName'] = user_tuple[2]
        user['DOB'] = user_tuple[3]
        user['userName'] = user_tuple[4]
        user['password'] = user_tuple[5]

        return user

    def read_users(self):
        select_statement = "SELECT * FROM TaasUser"
        try:
            self.cursor.execute(select_statement)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            return result

    def read_order(self, user_id):
        select_statement = "SELECT * FROM Orders WHERE user_id=%s"
        try:
            self.cursor.execute(select_statement, user_id)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            return result

    def read_orders(self):
        select_statement = "SELECT * FROM Orders"
        try:
            self.cursor.execute(select_statement)
        except Exception as e:
            print(e)
        finally:
            result = self.cursor.fetchone()
            return result

    def close_connection(self):
        self.connection.close()
        print("MySQL connection is closed")