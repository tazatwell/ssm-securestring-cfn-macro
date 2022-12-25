"""
    Unit Test SSM Client
"""

import unittest
import botocore.session
from botocore.stub import Stubber

import client as ssm

class TestSSMClient(unittest.TestCase):
    """Unit Test SSM Client"""

    region = "us-west-2"

    def test_put_parameter_normal(self):
        """Request returns a normal response"""

        ssm_client = botocore.session.get_session().create_client('ssm', region_name = self.region)

        ssm_put_parameter_params = {
            'Name': "some-name",
            'Value': "some-value",
            'Type': "SecureString"
        }

        ssm_get_parameter_response = {
            'Version': 1,
            'Tier': "some-tier"
        }

        with Stubber(ssm_client) as stubber:
            stubber.add_response('put_parameter', ssm_get_parameter_response, ssm_put_parameter_params)
            service_response = ssm.put_parameter(ssm_client, ssm_put_parameter_params)

        assert service_response == ssm_get_parameter_response


    def test_put_parameter_exception(self):
        """Request returns exception"""

        ssm_client = botocore.session.get_session().create_client('ssm', region_name = self.region)

        ssm_put_parameter_params = {
            'Name': "some-name",
            'Value': "some-value",
            'Type': "SecureString"
        }

        service_message_exception = "An error occurred (ParameterAlreadyExists) when calling the PutParameter operation: The parameter already exists. To overwrite this value, set the overwrite option in the request to true"

        with Stubber(ssm_client) as stubber:
            stubber.add_client_error(
                method = 'put_parameter',
                service_error_code = "ParameterAlreadyExists",
                service_message = service_message_exception,
                expected_params = ssm_put_parameter_params
            )

            self.assertRaises(ssm_client.exceptions.ParameterAlreadyExists, ssm.put_parameter, ssm_client, ssm_put_parameter_params)


    def test_delete_parameter_normal(self):
        """Request returns a normal response"""

        ssm_client = botocore.session.get_session().create_client('ssm', region_name = self.region)

        ssm_delete_parameter_params = {
            'Name': "some-name"
        }

        with Stubber(ssm_client) as stubber:
            stubber.add_response('delete_parameter', {}, ssm_delete_parameter_params)
            service_response = ssm.delete_parameter(ssm_client, ssm_delete_parameter_params)

        assert service_response == {}


    def test_delete_parameter_exception(self):
        """Request returns exception"""

        ssm_client = botocore.session.get_session().create_client('ssm', region_name = self.region)

        ssm_delete_parameter_params = {
            'Name': "some-name"
        }

        service_message_exception = "An error occurred (ParameterNotFound) when calling the DeleteParameter operation:"

        with Stubber(ssm_client) as stubber:
            stubber.add_client_error(
                method = 'delete_parameter',
                service_error_code = "ParameterNotFound",
                service_message = service_message_exception,
                expected_params = ssm_delete_parameter_params
            )

            self.assertRaises(ssm_client.exceptions.ParameterNotFound, ssm.delete_parameter, ssm_client, ssm_delete_parameter_params)
