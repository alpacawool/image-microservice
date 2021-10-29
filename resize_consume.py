# Based on code from https://www.cloudamqp.com/docs/python.html
# consume.py
import pika, os, ssl, json
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# Access the CLODUAMQP_URL environment variable 
# and parse it (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(url)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
params.ssl_options = pika.SSLOptions(context, server_hostname='CLOUDAMQP_HOST') 
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel
channel.queue_declare(queue='resize') # Declare a queue
def on_request(ch, method, properties, body):
  print(json.loads(body))

  response = {
  'name': 'this is a test response',
  'image_url': 'www.testing.com/response'
  }
  
  ch.basic_publish(exchange = '',
                  routing_key = properties.reply_to,
                  properties = pika.BasicProperties(correlation_id = \
                                  properties.correlation_id),
                  body=json.dumps(response))
  ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume('resize',
                      on_message_callback = on_request)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()