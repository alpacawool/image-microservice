# Using code from https://www.cloudamqp.com/docs/python.html
# publish.py
import pika, os, ssl
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# Access the CLODUAMQP_URL environment variable and parse it
#  (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL')
params = pika.URLParameters(url)
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
params.ssl_options = pika.SSLOptions(context, server_hostname='CLOUDAMQP_HOST') 
connection = pika.BlockingConnection(params)
channel = connection.channel() # start a channel

for i in range(2000):
    channel.queue_declare(queue='resize') # Declare a queue
    channel.basic_publish(exchange='',
                        routing_key='resize',
                        body='A message from CS361')
    print(" [x] Sent 'A message from CS361'")


connection.close()