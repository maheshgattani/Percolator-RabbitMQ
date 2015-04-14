import tornado.ioloop
import tornado.web
import json
import pika_publisher
import argparse
import pika
import yaml

PRODUCER_CONFIG_TAG = "producer"
RABBITMQ_CONFIG_TAG = "rabbitmq"

class PublishHandler(tornado.web.RequestHandler):
  def initialize(self, publisher):
    self.publisher = publisher

  def post(self):
    data = json.loads(self.request.body)
    self.publisher.publish_message(data)
    self.write(data)

class PublishApplciation(tornado.web.Application):
  def __init__(self, publisher):
    handlers = [
      (r"/test", PublishHandler, dict(publisher=publisher)),
    ]
    tornado.web.Application.__init__(self, handlers)

def main():

  # Parse arguments, especially config file location.
  parser = argparse.ArgumentParser(description='Publishes a payload to rabbitmq')
  parser.add_argument('--config_file', type=str, required=True, help='Path to the config file. Example: /etc/test-config.yaml')
  args = parser.parse_args()

  config = yaml.load(open(args.config_file))
  producer_config = config[PRODUCER_CONFIG_TAG]
  rabbitmq_config = config[RABBITMQ_CONFIG_TAG]

  credentials = pika.PlainCredentials(rabbitmq_config["username"], rabbitmq_config["password"])
  parameters = pika.ConnectionParameters(rabbitmq_config["host"], rabbitmq_config["port"], rabbitmq_config["virtual_host"], credentials)
  publisher = pika_publisher.PikaPublisher(parameters, producer_config["exchange"], producer_config["exchange_type"], producer_config["queue"], producer_config["routing_key"])

  application = PublishApplciation(publisher)

  application.listen(8888)
  ioloop = tornado.ioloop.IOLoop.instance()
  ioloop.add_timeout(500, publisher.connect())
  ioloop.start()

if __name__ == "__main__":
  main()
