import unittest
import pika
import json
from mock import Mock, patch, DEFAULT
from eds.pika_publisher import PikaPublisher

class PikaPublisherTest(unittest.TestCase):

  def setUp(self):
    self._message = 'dummy_message'
    self._publisher = PikaPublisher('fake_params', 'fake_exchange', 'fake_exchange_type', 'fake_queue', 'fake_routing_key')
    self._publisher._channel = pika.channel.Channel

  @patch.object(pika.channel.Channel, 'basic_publish', spec = pika.channel.Channel.basic_publish)  
  def test_publish_message(self, mock_basic_publish):
    self._publisher.publish_message(self._message)
    self.assertTrue(mock_basic_publish.called, 'basic_publish not called when publishing to queue via pika')

    args, kwargs = mock_basic_publish.call_args
    self.assertEqual('example-publisher', args[3].app_id)
    self.assertEqual('application/json', args[3].content_type)
    self.assertEqual(2, args[3].delivery_mode, 'queue message is not persistent')
    self.assertEqual(self._message, args[3].headers)
    self.assertEqual('fake_exchange', args[0])
    self.assertEqual('fake_routing_key', args[1])
    self.assertEqual(json.dumps(self._message, ensure_ascii=False), args[2])

  @patch.object(pika.channel.Channel, 'queue_declare', spec = pika.channel.Channel.queue_declare)
  def test_setup_queue(self, mock_queue_declare):
    self._publisher.setup_queue("fake_queue")
    self.assertTrue(mock_queue_declare.called, 'queue_declare not called when setuping up a queue')

    args, kwargs = mock_queue_declare.call_args
    self.assertEqual("fake_queue", args[1])
    self.assertEqual(True, kwargs["durable"], 'queue is not persistent')

  @patch.object(pika.channel.Channel, 'exchange_declare', spec = pika.channel.Channel.exchange_declare)
  def test_setup_exchange(self, mock_exchange_declare):
    self._publisher.setup_exchange("fake_exchange")
    self.assertTrue(mock_exchange_declare, 'exchange_declare not called when setting up an exchange')

    args, kwargs = mock_exchange_declare.call_args
    self.assertEqual(kwargs["durable"], True, 'exchange is not persistent')
    self.assertEqual(args[1], "fake_exchange")
    self.assertEqual(args[2], "fake_exchange_type")
