import requests
import logging
import json
import time
from geopy.geocoders import Nominatim

class Simulator:

    #### Dictionary for holding key value pair

    lwm2m_objects = {

                'device'   : { '3' : { 'battery_level' : '9' } },

                'location' : { '6' : { 'latitude' : '0', 'longitude' : '1' } }

                 }

    auth_token = "eef88835-dcb6-4a4f-a3b7-feb597192b5c"

    headers_1 = {

            'Content-Type' : 'application/json',
            'Authorization':  auth_token
        }

    logging.basicConfig(level=logging.INFO)

    def __init__(self,imei):

        self.imei = imei
        self.username = "TMO"
        self.password = "TMOPassword1"

        self.psk = "123456"

        self.base_url = "https://petcloud.cfapps.io"
        self.api_url = self.base_url + "/simulators/"
        self.end_point = "urn:imei:" + imei

        self.url = self.api_url + self.end_point

        # step 1: create the simulator
        self.create_simulator(self.api_url)

        # step 2: run the simulator
        self.start_simulator(self.url,self.end_point)

    def create_simulator(self, url):

        """
        to create simulator
        :param url:
        :return:

        """

        end_point = self.end_point
        request_url = url.rstrip('/')

        payload = {

            "endpoint": end_point,
            "psk": self.psk
        }

        response = requests.post(request_url, headers=Simulator.headers_1, data=json.dumps(payload))
        # assert response.status_code == 200 or response.status_code == 201

        if response.status_code == 201:
            logging.info("create simulator : " + end_point + " has been created!")
        elif response.status_code == 200:
            logging.info("create simulator : " + end_point + " was already created")
        else:
            logging.error("create simulator : " + end_point + " creation wrong status code" + str(response.status_code))

    def start_simulator(self,url,end_point):

        """
        to start simulator
        :param url:
        :param end_point:
        :return:

        """

        request_url = url + '/start'

        response = requests.post(request_url, headers=Simulator.headers_1)

        # assert response.status_code == 200
        if response.status_code == 200:
            logging.info("start simulator " + end_point + " has run successfully!")
        else:
            logging.error("start simulator " + end_point + " is not running: error status code =" + str(response.status_code))

    def stop_simulator(self, url):

        """
       to stop simulator
       :param url:
       :return:

        """

        request_url = url + '/stop'

        response = requests.post(request_url, headers=Simulator.headers_1)
        # assert response.status_code == 200
        if response.status_code == 200:
            logging.info(end_point + ' has run successfully!')
        else:
            logging.error(end_point + ' is not running: error status code=' + str(response.status_code))

    def generate_batterylevel(self,lat,long,level):

        """
        sends battery level update
        :param lat:
        :param long:
        :param level:
        :return:

        """

        flag = 0

        object_id = list(Simulator.lwm2m_objects['device'].keys())[0];  ### Gets object id
        object_field_info = Simulator.lwm2m_objects['device']['3']['battery_level'];

        object_info = object_id + '/0/' + object_field_info;

        # Creating Request for updating battery status

        request_url = self.url + "/" + object_info;

        payload = {

            "type": "INTEGER",
            "value": level
        }

        response = requests.post(request_url, headers=Simulator.headers_1, data=json.dumps(payload))

        if response.status_code == 200:
            logging.debug("successfully sent battery level update")

        else:
            flag = 1
            logging.debug("unable to send battery level update")

        # Creating request for location update, required for battery update

        object_id = list(Simulator.lwm2m_objects['location'].keys())[0];

        object_field_info_lat = Simulator.lwm2m_objects['location']['6']['latitude'];
        object_field_info_long = Simulator.lwm2m_objects['location']['6']['longitude'];

        object_info_lat = object_id + '/0/' + object_field_info_lat;
        object_info_long = object_id + '/0/' + object_field_info_long;

        ### Latitude update ###

        request_url = self.url + "/" + object_info_lat;

        payload = {

            "type": "FLOAT",
            "value": lat
        }

        response = requests.post(request_url, headers=Simulator.headers_1, data=json.dumps(payload))

        if response.status_code == 200:
            logging.debug("successfully sent latitude update")

        else:
            flag = 1
            logging.debug("unable to send latitude update")

        ### Longitude update ###

        request_url = self.url + "/" + object_info_long;

        payload = {

            "type": "FLOAT",
            "value": long
        }

        response = requests.post(request_url, headers=Simulator.headers_1, data=json.dumps(payload))

        if response.status_code == 200:
            logging.debug("successfully sent longitude update")

        else:
            flag = 1
            logging.debug("unable to send longitude update")

        if flag == 0:
            logging.info("Successfully updated battery level")
        else:
            logging.info("Unable to update battery level")

    def generate_location(self,lat,long):

        flag = 0
        # Creating request for location update, required for battery update

        object_id = list(Simulator.lwm2m_objects['location'].keys())[0];

        object_field_info_lat = Simulator.lwm2m_objects['location']['6']['latitude'];
        object_field_info_long = Simulator.lwm2m_objects['location']['6']['longitude'];

        object_info_lat = object_id + '/0/' + object_field_info_lat;
        object_info_long = object_id + '/0/' + object_field_info_long;

        ### Latitude update ###

        request_url = self.url + "/" + object_info_lat;

        payload = {

            "type": "FLOAT",
            "value": lat
        }

        response = requests.post(request_url, headers=Simulator.headers_1, data=json.dumps(payload))

        if response.status_code == 200:
            logging.debug("successfully sent latitude update")

        else:
            flag = 1
            logging.debug("unable to send latitude update")

        ### Longitude update ###

        request_url = self.url + "/" + object_info_long;

        payload = {

            "type": "FLOAT",
            "value": long
        }

        response = requests.post(request_url, headers=Simulator.headers_1, data=json.dumps(payload))

        if response.status_code == 200:
            logging.debug("successfully sent longitude update")

        else:
            flag = 1
            logging.debug("unable to send longitude update")

        if flag == 0:
            logging.info("Successfully updated location")
        else:
            logging.info("Unable to update location")

    def get_gps_coordinates(self,address):

        geolocator = Nominatim(user_agent = "Pet Tracker simulator")
        location   = geolocator.geocode(address)

        gps_location = {}
        gps_location['latitude']  = location.latitude
        gps_location['longitude'] = location.longitude
        logging.info(gps_location)

        return gps_location
