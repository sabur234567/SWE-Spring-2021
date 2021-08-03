import logging
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

import database_util

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

        if path == '/supply-front-end/RegisterVehicle':
            vehicleRegistration_parameters = postBody
            database = database_util.DatabaseUtil()
            vehicleType = postBody['serviceType']
            for j in vehicleType:
                for i in range(postBody['amount'):
                    vehicle = Vehicle(i, i+j, j)
                    database = DatabaseUtil()
                    try:
                        database.insert_vehicle(vehicle)
                    except Exception as e:
                        print(e)
                    finally:
                        database.close_connection
            # try:
            #     database.insert_vehicle(vehicleRegistration_parameters)
            #     responseBody['status'] = 'Success'
            # except Exception as e:
            #     responseBody['status'] = 'Failed'
            #     print(e)
            # finally:
            #     database.close_connection()
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        response = json.dumps(responseBody, indent=4, sort_keys=True, default=str)
        logging.info('Response: ' + response)
        byteStringResponse = response.encode('utf-8')
        self.wfile.write(byteStringResponse)



            def do_POST(self):
                path = self.path
                postBody = self.extract_POST_Body()
                status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND'].value
                responseBody = {}

                if path == '/supply-front-end/RegisterFleet':
                    fleetRegistration_parameters = postBody
                    database = database_util.DatabaseUtil()
                    try:
                        database.insert_fleet(fleetRegistration_parameters)
                        responseBody['status'] = 'Success'
                    except Exception as e:
                        responseBody['status'] = 'Failed'
                        print(e)
                    finally:
                        database.close_connection()
                self.send_response(status)
                self.send_header("Content-type", "text/html")
                self.end_headers()

                response = json.dumps(responseBody, indent=4, sort_keys=True, default=str)
                logging.info('Response: ' + response)
                byteStringResponse = response.encode('utf-8')
                self.wfile.write(byteStringResponse)

    # def do_GET(self):
    #     # self.path here will return us the http request path entered by the client.
    #     path = self.path
    #     # Extract the GET parameters associated with this HTTP request and store them in a python dictionary
    #     postBody = self.extract_GET_parameters()
    #     print(postBody)
    #     status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND'].value
    #     responseBody = {}
    #     username = postBody['username']
    #     password = postBody['password']
    #     if path == '/common-services/logInForm':
    #         database = database_util.DatabaseUtil()
    #         try:
    #             user = database.read_user(username, password)
    #
    #             if user['userName']  == username and user['password']== password:
    #                 responseBody['status'] = 'Success'
    #         except Exception as e:
    #             responseBody['status'] = 'Failed'
    #             print(e)
    #         finally:
    #             database.close_connection()
    #
    #     self.send_response(status)
    #     self.send_header("Content-type", "text/html")
    #     self.end_headers()
    #
    #     response = json.dumps(responseBody, indent=4, sort_keys=True, default=str)
    #     logging.info('Response: ' + response)
    #     byteStringResponse = response.encode('utf-8')
    #     self.wfile.write(byteStringResponse)


# Turn the application server on at port 8082 on localhost and fork the process.
if __name__ == '__main__':
    hostName = "localhost"
    # Ports are part of a socket connection made between a server and a client. Ports 0-1023 are
    # reserved for common TCP/IP applications and shouldn't be used here. Communicate with your
    # DevOps member to find out which port you should be running your application off of.
    serverPort = 8082
    appServer = HTTPServer((hostName, serverPort), handler)
    logging.info('Server started http://%s:%s' % (hostName, serverPort))

    # Start the server and fork it. Use 'Ctrl + c' command to kill this process when running it in the foreground
    # on your terminal.
    try:
        appServer.serve_forever()
    except KeyboardInterrupt:
        pass

    appServer.server_close()
    logging.info('Server stopped')
    # comment added
