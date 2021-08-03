import logging
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
import mysql.connector
import mysql

logging.basicConfig(level=logging.DEBUG)


class handler(BaseHTTPRequestHandler):
    HTTP_STATUS_RESPONSE_CODES = {
        'OK': HTTPStatus.OK,
        'FORBIDDEN': HTTPStatus.FORBIDDEN,
        'NOT_FOUND': HTTPStatus.NOT_FOUND,
    }

    def extract_GET_parameters(self):
        path = self.path
        parsedPath = urlparse(path)
        paramsDict = parse_qs(parsedPath.query)
        logging.info('GET parameters received: ' + json.dumps(paramsDict, indent=4, sort_keys=True))
        return paramsDict

    def extract_POST_Body(self):
        postBodyLength = int(self.headers['content-length'])
        postBodyString = self.rfile.read(postBodyLength)
        postBodyDict = json.loads(postBodyString)
        logging.info('POST Body received: ' + json.dumps(postBodyDict, indent=4, sort_keys=True))
        return postBodyDict

    def do_POST(self):
        path = self.path
        postBody = self.extract_POST_Body()
        status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND'].value
        responseBody = {}

        if path == '/demand/orderFormCOVID':
            parameters = postBody
            connection = mysql.connector.connect(user='developer', password='Team11_developer', host='localhost',
                                                 database='team11_demand')
            if connection.is_connected():
                database_info = connection.get_server_info()
                print("NOW CONNECTED TO MYSQL SERVER v", database_info)
                myCursor = connection.cursor()
                myCursor.execute("select database(); ")
                record = myCursor.fetchone()
                print("You're connected to database", record)

               #for order; assign the values according to what the user enters in the form
                #use Laurent's order class
                # 3. write data into the database
                sql = """INSERT INTO TaasUser (, firstName, lastName, DOB, userName, password) VALUES (%s,%s,%s,%s,
                %s,%s) """
                print(sql)
                # val = (parameters["email"], parameters["firstName"], parameters["lastName"], parameters["DOB"]
                #        , parameters["userName"], parameters["password"])
                val = tuple(list(postBody.values()))

                myCursor.execute(sql, val)
                connection.commit()
                print(myCursor.rowcount, "was inserted")

                userData = val

                responseBody['data'] = userData
