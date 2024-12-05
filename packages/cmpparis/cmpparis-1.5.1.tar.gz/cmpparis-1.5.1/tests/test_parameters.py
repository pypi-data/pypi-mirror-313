import boto3
import os
import unittest

from moto import mock_aws
from cmpparis.parameters_utils import get_parameter

class TestParameters(unittest.TestCase):
    @mock_aws
    def setUp(self):
        self.mock_aws = mock_aws()
        self.mock_aws.start()

        os.environ['AWS_ACCESS_KEY_ID'] = 'testing' 
        os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
        os.environ['AWS_DEFAULT_REGION'] = 'eu-west-3'

        self.ssm = boto3.client('ssm', 'eu-west-3')

    def tearDown(self):
        self.mock_aws.stop()

    def test_get_parameter(self):
        with mock_aws():
            self.ssm.put_parameter(
                Name='/test/parameter',
                Value='test_value',
                Type='String'
            )

            parameter = get_parameter('test', 'parameter')

            self.assertEqual(parameter, 'test_value')

    def test_get_parameter_not_found(self):
        with mock_aws():
            with self.assertRaises(Exception):
                raise get_parameter('test', 'parameter')

