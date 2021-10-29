# Using code from https://www.cloudamqp.com/docs/python.html
# and https://www.rabbitmq.com/tutorials/tutorial-six-python.html
# publish.py
import pika, os, ssl, json, uuid
from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# # Access the CLODUAMQP_URL environment variable and parse it
# #  (Fallback to localhost)
# url = os.environ.get('CLOUDAMQP_URL')
# params = pika.URLParameters(url)
# context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
# params.ssl_options = pika.SSLOptions(context, server_hostname='CLOUDAMQP_HOST') 
# connection = pika.BlockingConnection(params)
# # Start a channel
# channel = connection.channel() 
# # Declare a queue
# channel.queue_declare(queue='resize') 
# # Create JSON message
# # Based on https://stackoverflow.com/questions/34534178/

# message = {
#   'name': 'this is a test',
#   'image_url': 'www.testing.com'
# }

# # Send message
# channel.basic_publish(exchange='',
#                         routing_key='resize',
#                         body=json.dumps(message))
# print(" [x] Sent 'A message from CS361'")
# connection.close()

class ResizeClient(object):

    def __init__(self):

        # Set up connection
        self.url = os.environ.get('CLOUDAMQP_URL')
        self.params = pika.URLParameters(self.url)
        self.context =ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.params.ssl_options = pika.SSLOptions(self.context, server_hostname='CLOUDAMQP_HOST') 
        self.connection = pika.BlockingConnection(self.params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='resize',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=n)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


resize_client = ResizeClient()

message = {
  'name': 'this is a test',
  'image_url': 'www.testing.com'
}

print(" [x] Sending message to consumer")
response = resize_client.call(json.dumps(message))
print("Printing response sent to publisher from consumer:")
print(json.loads(response))


