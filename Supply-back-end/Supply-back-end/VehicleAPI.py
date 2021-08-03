import sys
sys.path.append('../common-services-back-end')

from database_util import *
import logging
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs

# Class Logger we can use for debugging our Python service. You can add an additional parameter here for
# specifying a log file if you want to see a stream of log data in one file.
logging.basicConfig(level=logging.DEBUG)


# BaseHTTPRequestHandler is a class from the http.server python module. http.server is a simple
# module used for creating application servers. BaseHTTPRequestHandler will help us respond to requests that arrive
# at our server, matching a specified hostname and port. For additional documentation on this module,
# you can read: https://docs.python.org/3/library/http.server.html
class BaseAppService(BaseHTTPRequestHandler):
    # HTTP Response code dictionary constant we can reuse inside our responses back to the client. Typically this
    # would be in a configuration file where you store constants you repeatedly use throughout your services.
    HTTP_STATUS_RESPONSE_CODES = {
        'OK': HTTPStatus.OK,
        'FORBIDDEN': HTTPStatus.FORBIDDEN,
        'NOT_FOUND': HTTPStatus.NOT_FOUND,
    }

    # Here's how you extract GET parameters from a URL entered by a client.
    def extract_GET_parameters(self):
        path = self.path
        parsedPath = urlparse(path)
        paramsDict = parse_qs(parsedPath.query)
        logging.info('GET parameters received: ' + json.dumps(paramsDict, indent=4, sort_keys=True))
        return paramsDict

    # Here's how we extract the POST body of data attached to the request by the client.
    def extract_POST_Body(self):
        # The content-length HTTP header is where our POST data will be in the request. So we'll need to
        # read the data using an IO input buffer stream built into the http.server module.
        postBodyLength = int(self.headers['content-length'])
        postBodyString = self.rfile.read(postBodyLength)
        postBodyDict = json.loads(postBodyString)
        logging.info('POST Body received: ' + json.dumps(postBodyDict, indent=4, sort_keys=True))
        return postBodyDict

    # The do_GET(self) function is how we respond to GET requests from clients.
    def do_GET(self):
        # self.path here will return us the http request path entered by the client.
        path = self.path
        # Extract the GET parameters associated with this HTTP request and store them in a python dictionary
        paramsDict = self.extract_GET_parameters()
        status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND'].value
        responseBody = {}

        # This is a root URI or block of code that will be executed when client requests the address:
        # http://localhost:8082.
        if path == '/':
            status = self.HTTP_STATUS_RESPONSE_CODES['OK'].value
            responseBody['data'] = 'We-Go Vehicle API'

        elif '/supply-back-end/vehicle_api/v1/vehicles' in path:
            database = DatabaseUtil()
            try:
                vehicles = database.read_vehicles()
                responseBody['data'] = vehicles
                responseBody['status'] = 'Success'
                status = self.HTTP_STATUS_RESPONSE_CODES['OK'].value
            except Exception as e:
                print(e)
            finally:
                database.close_connection()

        elif '/supply-back-end/vehicle_api/v1/vehicle' in path:
            vin = paramsDict['vin']
            database = DatabaseUtil()
            try:
                vehicle = database.read_vehicle(vin)
                responseBody['data'] = vehicle
                responseBody['status'] = 'Success'
                status = self.HTTP_STATUS_RESPONSE_CODES['OK'].value
            except Exception as e:
                print(e)
            finally:
                database.close_connection()

        elif '/supply-back-end/vehicle_api/v1/available_vehicle' in path:
            database = DatabaseUtil()
            vehicle = database.get_available_vehicle()
            if vehicle == "":
                responseBody['data'] = 'None'
            else:
                responseBody['data'] = vehicle
                responseBody['status'] = 'Success'
                status = self.HTTP_STATUS_RESPONSE_CODES['OK'].value

        elif '/supply-back-end/vehicle_api/v1/vehicle_location' in path:
            vin = paramsDict['vin']
            database = DatabaseUtil()
            try:
                location = database.read_vehicle_location(vin)
                responseBody['data'] = location
                responseBody['status'] = 'Success'
                status = self.HTTP_STATUS_RESPONSE_CODES['OK'].value
            except Exception as e:
                print(e)
                responseBody['status'] = 'Success'
            finally:
                database.close_connection()

        # This will add a response header to the header buffer. Here, we are simply sending back
        # an HTTP response header with an HTTP status code to the client.
        self.send_response(status)
        # This will add a header to the header buffer included in our HTTP response. Here we are specifying
        # the data Content-type of our response from the server to the client.
        self.send_header("Content-type", "text/html")
        # The end_headers method will close the header buffer, indicating that we're not sending
        # any more headers back to the client after the line below.
        self.end_headers()
        # Convert the Key-value python dictionary into a string which we'll use to respond to this request
        response = json.dumps(responseBody)
        logging.info('Response: ' + response)
        # Fill the output stream with our encoded response string which will be returned to the client.
        # The wfile.write() method will only accept bytes data.
        byteStringResponse = response.encode('utf-8')
        self.wfile.write(byteStringResponse)

    # The do_POST(self) function is how we respond to POST requests from clients.
    def do_POST(self):
        path = self.path
        # Extract the POST body data from the HTTP request, and store it into a Python
        # dictionary we can utilize inside of any of our POST endpoints.
        postBody = self.extract_POST_Body()
        status = self.HTTP_STATUS_RESPONSE_CODES['NOT_FOUND'].value
        # 1. Access POST parameters using your postBody
        responseBody = {}
        if path == '/supply-back-end/vehicle_api/v1/vehicle':
            parameters = postBody
            database = DatabaseUtil()
            try:
                database.insert_vehicle(parameters)
                responseBody['status'] = 'Success'
                status = self.HTTP_STATUS_RESPONSE_CODES['OK'].value
            except Exception as e:
                responseBody['status'] = 'Failed'
                print(e)
            finally:
                database.close_connection()

        elif path == '/supply-back-end/vehicle_api/v1/vehicle_location':
            parameters = postBody
            print('Location post', parameters)
            vin = parameters['vin']

            database = DatabaseUtil()
            try:
                database.update_vehicle_location(vin, parameters['location'])
                responseBody['status'] = 'Success'
                responseBody['data'] = "location updated for " + str(vin)
                status = self.HTTP_STATUS_RESPONSE_CODES['OK'].value
            except Exception as e:
                responseBody['status'] = 'Failed'
                print(e)
            finally:
                database.close_connection()

        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # When using the json.dumps() method, you may encounter data types which aren't easily serializable into
        # a string. When working with these types of data you can include an additional parameters in the dumps()
        # method, 'default=str' to let the serializer know to convert to a string when it encounters a data type
        # it doesn't automatically know how to convert.
        response = json.dumps(responseBody, indent=4, sort_keys=True, default=str)
        logging.info('Response: ' + response)
        byteStringResponse = response.encode('utf-8')
        self.wfile.write(byteStringResponse)


# Turn the application server on at port 8082 on localhost and fork the process.
if __name__ == '__main__':
    hostName = "localhost"
    # Ports are part of a socket connection made between a server and a client. Ports 0-1023 are
    # reserved for common TCP/IP applications and shouldn't be used here. Communicate with your
    # DevOps member to find out which port you should be running your application off of.
    serverPort = 8081
    appServer = HTTPServer((hostName, serverPort), BaseAppService)
    logging.info('Server started http://%s:%s' % (hostName, serverPort))

    # Start the server and fork it. Use 'Ctrl + c' command to kill this process when running it in the foreground
    # on your terminal.
    try:
        appServer.serve_forever()
    except KeyboardInterrupt:
        pass

    appServer.server_close()
    logging.info('Server stopped')
