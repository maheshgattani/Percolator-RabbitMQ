import unittest
from tornado.testing import AsyncHTTPTestCase, LogTrapTestCase
from eds.pika_publisher import PikaPublisher
from eds.publisher_app import PublishHandler, PublishApplciation
import mock

class PublishHandlerTest(AsyncHTTPTestCase):
  
  _post_url = '/test'
  _http_success_code = 200
  _http_method_not_allowed = 405 

  def setUp(self):
    self._publisher = PikaPublisher("fake_params", "fake_exchange", "fake_exchange_type", "fake_queue", "fake_routing_key")
    AsyncHTTPTestCase.setUp(self)

  def get_app(self):
    return PublishApplciation(self._publisher)

  @mock.patch.object(PikaPublisher, 'publish_message')
  def test_post(self, mock_pika_publisher):
    self.http_client.fetch(self.get_url(self._post_url), self.stop, method = "POST", body = '{"test": "data"}')
    response = self.wait()
    self.assertEqual(self._http_success_code, response.code)
    self.assertTrue(mock_pika_publisher.called, "Failed to upload data to queue")

  def test_get(self):
    self.http_client.fetch(self.get_url(self._post_url), self.stop)
    response = self.wait()
    self.assertEqual(self._http_method_not_allowed, response.code)

if __name__ == '__main__':
  unittest.main()
