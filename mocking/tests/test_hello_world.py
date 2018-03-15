from __future__ import print_function  # Python 2/3 compatibility
import unittest
import mock
# from mock import patch
import hello_world


class TestLambda(unittest.TestCase):

    @mock.patch('hello_world.Person')
    def test_hello_world_ok(self, mock_Person):
        """Test hello world expected behaviour."""

        mock_Person.return_value = mock.Mock()
        print(mock_Person)

        response = hello_world.lambda_handler(None, None)
        assert response == 'Hello world'
