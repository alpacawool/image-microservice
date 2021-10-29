# Based on code from https://www.cloudamqp.com/docs/python.html
# consume.py
import pika, os, ssl
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
def callback(ch, method, properties, body):
  print(" [x] Received " + str(body))

channel.basic_consume('resize',
                      callback,
                      auto_ack=True)

print(' [*] Waiting for messages:')
channel.start_consuming()
connection.close()