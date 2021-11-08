# Based on code from https://www.cloudamqp.com/docs/python.html
# consume.py
import pika, os, ssl, json
from dotenv import load_dotenv
# Add sirv API wrapper
from sirv import ImageClient

# Load environmental variables
load_dotenv()

# Access the CLOUDAMQP_URL environment variable 
# and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(url)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
params.ssl_options = pika.SSLOptions(context, server_hostname='CLOUDAMQP_HOST')
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='resize-jeff') # Declare a queue
# Set up image resizing client
resizer = ImageClient()

def on_request(ch, method, properties, body):
  
  response = {}

  # Check if JSON
  # https://stackoverflow.com/questions/5508509/
  is_json = True
  try:
    json.loads(body)
  except ValueError as e:
    is_json = False
  if is_json:
    print("-------Request Received--------")
    request = json.loads(body)
    print(request)
    # Check if required keys are there
    # REQUIRED: image_url, height, width
    if 'image_url' in request and 'height' in request \
      and 'width' in request:
      
      image_url = request['image_url']
      height = request['height']
      width = request['width']
      # Check for invalid height and width
      is_valid_dimensions = True
      if height < 0 or width < 0:
        response = {'success': False, 'error_message': 'Height or width must be greater than -1'}
        is_valid_dimensions = False
      # Check for optional key
      if 'scale_option' in request and is_valid_dimensions:
        scale_option = request['scale_option']
        # Check if valid scale_option
        if scale_option == 'fill' or scale_option == 'ignore' or scale_option == 'fit':
          # Valid scale_option
          # Resize image
          resize_response = resizer.upload_and_resize(image_url, height, width, scale_option)
          if resize_response['success'] == True:
            response = {'image_url': resize_response['image_url'], 'success': True}
          else:
            response = {'success': False, 'error_message': 'Problem resizing image'}
        else:
          # Invalid scale option
          response = {'success': False, 'error_message': 'Invalid scale_option. Must be fill, fit, or ignore'}
      elif is_valid_dimensions:
        # No scale option selected, just doing default (Resize to direct dimensions)
        resize_response = resizer.upload_and_resize(image_url, height, width)
        if resize_response['success'] == True:
          response = {'image_url': resize_response['image_url'], 'success': True}
        else:
          response = {'success': False, 'error_message': 'Problem resizing image'}
    else:
      response = {'success': False, 'error_message': 'Missing required arguments: image_url, height, and width.'}
  else:
    # Invalid JSON, did not receive JSON
    response = {'success': False, 'error_message': 'Error parsing JSON format.'}
  
  ch.basic_publish(exchange = '',
                  routing_key = properties.reply_to,
                  properties = pika.BasicProperties(correlation_id = \
                                  properties.correlation_id),
                  body=json.dumps(response))
  ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume('resize-jeff',
                      on_message_callback = on_request)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()