# Based on https://apidocs.sirv.com/?python

import http.client, os, json
from dotenv import load_dotenv
from datetime import datetime as dt

# Load environmental variables
load_dotenv()

class ImageClient(object):

    def __init__(self):
        self.url = "api.sirv.com"
        self.token = ''
        self.last_retrieved_token = dt.now()

    def send_token_request(self, headers, payload, endpoint, type):
        connection = http.client.HTTPSConnection(self.url)
        connection.request(type, endpoint, payload, headers)
        response = connection.getresponse()
        data = json.loads(response.read())
        return data

    def get_token(self):
        current_time = dt.now()
        elapsed_seconds = (current_time - self.last_retrieved_token).total_seconds()

        # Retrieve a token if the current token is expired
        print(f'Elapsed seconds: {elapsed_seconds}')
        if elapsed_seconds >= 1200 or self.token == '':
            #print("Token has expired.")
            self.last_retrieved_token = dt.now()
            payload = {"clientId": os.environ.get('SIRV_CLIENT_ID'), "clientSecret": os.environ.get('SIRV_SECRET')}
            headers = {"Content-Type" : "application/json"}
            endpoint = '/v2/token'
            response = self.send_token_request(headers, json.dumps(payload), endpoint, "POST")
            self.token = response['token']
            #print(f"New token is {self.token}")
        else:
            #print("Token has not expired.")
            #print(f"Current token is {self.token}")
            pass
    

# Demonstration
image_client = ImageClient()





