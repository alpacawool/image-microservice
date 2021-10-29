# Based on https://apidocs.sirv.com/?python

import http.client, os, json, uuid
from dotenv import load_dotenv
from datetime import datetime as dt

# Load environmental variables
load_dotenv()

class ImageClient(object):

    def __init__(self):
        self.url = "api.sirv.com"
        self.image_location_url = os.environ.get("SIRV_IMG_SAVE_LOCATION")
        self.token = ''
        self.last_retrieved_token = dt.now()

    def __send_token_request(self, headers, payload, endpoint, type):
        connection = http.client.HTTPSConnection(self.url)
        connection.request(type, endpoint, payload, headers)
        response = connection.getresponse()
        data = json.loads(response.read())
        return data

    def send_request(self, payload, endpoint, type):
        self.__get_token()
        headers = {"Content-Type": "application/json", "authorization": f"Bearer {self.token}"}
        connection = http.client.HTTPSConnection(self.url)
        connection.request(type, endpoint, payload, headers)
        response = connection.getresponse()
        data = json.loads(response.read())
        return data

    def __get_token(self):
        current_time = dt.now()
        elapsed_seconds = (current_time - self.last_retrieved_token).total_seconds()

        # Retrieve a token if the current token is expired
        #print(f'Elapsed seconds: {elapsed_seconds}')
        if elapsed_seconds >= 1200 or self.token == '':
            #print("Token has expired.")
            self.last_retrieved_token = dt.now()
            payload = {"clientId": os.environ.get('SIRV_CLIENT_ID'), "clientSecret": os.environ.get('SIRV_SECRET')}
            headers = {"Content-Type" : "application/json"}
            endpoint = '/v2/token'
            response = self.__send_token_request(headers, json.dumps(payload), endpoint, "POST")
            self.token = response['token']
            #print(f"New token is {self.token}")
        else:
            #print("Token has not expired.")
            #print(f"Current token is {self.token}")
            pass

    # Upload image that is already hosted
    def upload_hosted_image(self, image_url):
        # Generate unique filename
        # https://stackoverflow.com/questions/10501247/
        filename = str(uuid.uuid4())
        payload = {"url": image_url, "filename": f"/Uploads/{filename}"}
        endpoint = '/v2/files/fetch'
        upload_report = self.send_request(json.dumps(payload), endpoint, "POST")
        return upload_report
    
    # Resize upload image
    def __resize_image(self, uploaded_url, height, width, scale_option='ignore'):
        return f'{uploaded_url}?h={height}&w={width}&scale.option={scale_option}'

    # Upload and resize image
    def upload_and_resize(self, image_url, height, width, scale_option='ignore'):
        upload_response = self.upload_hosted_image(image_url)
        is_upload_success = upload_response[0]['success']
        if is_upload_success:
            filename = upload_response[0]['filename']
            upload_image_url = f'{self.image_location_url}{filename}'
            resized_url = self.__resize_image(upload_image_url, height, width, scale_option)
            resize_success_message = {'image_url': resized_url, 'success': True}
            return resize_success_message
        else:
            resize_failure_message = {'image_url': '', 'success': False}
            return resize_failure_message

    

# Demonstration
image_client = ImageClient()
print(image_client.upload_and_resize('https://upload.wikimedia.org/wikipedia/commons/3/3a/Russian_blue.jpg', 400, 400))





