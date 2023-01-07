"""
    Unit Test handler Function
"""

import unittest
import pytest
import botocore.session
from botocore.stub import Stubber

import app

class HandlerTest(unittest.TestCase):
    """Unit Test Handler Function"""

    region = "us-west-2"

    def test_process_ssm_request_create_event_proper(self):
        """Request returns a normal response"""

        sample_event = {
            'RequestType': "Create",
            'ResourceProperties': {
                'Name': "some-name",
                'Value': "some-value",
                'Type': "SecureString"
            }
        }

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
            assert app.process_ssm_request(sample_event, ssm_client, False, False) == ssm_get_parameter_response

    def test_process_ssm_request_create_event_exception(self):
        """Request with Create RequestType raises an exception"""

        sample_event = {
            'RequestType': "Create",
            'ResourceProperties': {
                'Name': "some-name",
                'Value': "some-value",
                'Type': "SecureString"
            }
        }

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

        service_message_exception = "SomeException"

        with Stubber(ssm_client) as stubber:
            stubber.add_client_error(
                method = 'put_parameter',
                service_error_code = "ParameterAlreadyExists",
                service_message = service_message_exception,
                expected_params = ssm_put_parameter_params
            )

            self.assertRaises(ssm_client.exceptions.ParameterAlreadyExists, app.process_ssm_request, sample_event, ssm_client, False, False)

    def test_process_ssm_request_delete_event_proper(self):
        """Request with Delete RequestType returns a normal response"""

        sample_event = {
            'RequestType': "Delete",
            'ResourceProperties': {
                'Name': "some-name",
                'Value': "some-value",
                'Type': "SecureString"
            }
        }

        ssm_client = botocore.session.get_session().create_client('ssm', region_name = self.region)

        ssm_delete_parameter_params = {
            'Name': "some-name"
        }

        ssm_delete_parameter_response = {}

        with Stubber(ssm_client) as stubber:
            stubber.add_response('delete_parameter', ssm_delete_parameter_response, ssm_delete_parameter_params)
            assert app.process_ssm_request(sample_event, ssm_client, False, False) == ssm_delete_parameter_response

    def test_process_ssm_request_delete_event_raises_exception(self):
        """Request with Delete RequestType raises an exception"""

        sample_event = {
            'RequestType': "Delete",
            'ResourceProperties': {
                'Name': "some-name",
                'Value': "some-value",
                'Type': "SecureString"
            }
        }

        ssm_client = botocore.session.get_session().create_client('ssm', region_name = self.region)

        ssm_delete_parameter_params = {
            'Name': "some-name"
        }

        service_message_exception = "SomeException"

        with Stubber(ssm_client) as stubber:
            stubber.add_client_error(
                method = 'delete_parameter',
                service_error_code = "ParameterAlreadyExists",
                service_message = service_message_exception,
                expected_params = ssm_delete_parameter_params
            )

            self.assertRaises(ssm_client.exceptions.ParameterAlreadyExists, app.process_ssm_request, sample_event, ssm_client, False, False)

    def test_process_ssm_request_invalid_request_type(self):
        """Request with invalid Request Type"""

        sample_event = {
            'RequestType': "InvalidRequestType",
            'ResourceProperties': {
                'Name': "some-name",
                'Value': "some-value",
                'Type': "SecureString"
            }
        }

        ssm_client = botocore.session.get_session().create_client('ssm', region_name = self.region)

        with pytest.raises(app.CustomLambdaRuntimeException) as e_info:
            app.process_ssm_request(sample_event, ssm_client, False, False)

    def test_verify_request_no_resource_properties(self):
        """Request with no 'ResourceProperties' field"""
        sample_event = {}
        with pytest.raises(app.CustomLambdaRuntimeException) as e_info:
            app.validate_request(sample_event)

    def test_verify_request_no_name_field(self):
        """Request with no 'Name' key in 'ResourceProperties' field"""
        sample_event = {
            'ResourceProperties': {}
        }
        with pytest.raises(app.CustomLambdaRuntimeException) as e_info:
            app.validate_request(sample_event)

    def test_verify_request_proper(self):
        """Request with proper 'ResourceProperties' field"""

        sample_event = {
            'ResourceProperties': {
                'Name': "some-name"
            }
        }

        expected_response = True
        actual_response = app.validate_request(sample_event)
        assert expected_response == actual_response

    def test_construct_param_args_delete(self):
        """Request with Delete request type"""

        sample_event = {
            'RequestType': "Delete",
            'ResourceProperties': {
                'Name': "some-name"
            }
        }

        expected_response = {'Name': "some-name"}
        assert app.construct_param_args(sample_event) == expected_response

    def test_construct_param_args_create_with_all_args_overwrite_false(self):
        """Request with Create request type and all create args present"""

        sample_event = {
            'RequestType': "Create",
            'ResourceProperties': {
                'Name': "some-name",
                'Value': "some-value",
                'Description': "some-description",
                'Type': "some-type",
                'KeyId': "some-key-id",
                'Overwrite': "some-overwrite",
                'AllowedPattern': "some-allowed-pattern",
                'Tags': "some-tags",
                'Tier': "some-tier",
                'Policies': "some-policies",
                'DataType': "some-data-type"
            }
        }

        expected_response = {
            'Name': "some-name",
            'Value': "some-value",
            'Description': "some-description",
            'Type': "some-type",
            'KeyId': "some-key-id",
            'Overwrite': False,
            'AllowedPattern': "some-allowed-pattern",
            'Tags': "some-tags",
            'Tier': "some-tier",
            'Policies': "some-policies",
            'DataType': "some-data-type"
        }

        assert app.construct_param_args(sample_event) == expected_response

    def test_construct_param_args_create_with_all_args_overwrite_true(self):
        """Request with Create request type and all create args present"""

        sample_event = {
            'RequestType': "Create",
            'ResourceProperties': {
                'Name': "some-name",
                'Value': "some-value",
                'Description': "some-description",
                'Type': "some-type",
                'KeyId': "some-key-id",
                'Overwrite': "true",
                'AllowedPattern': "some-allowed-pattern",
                'Tags': "some-tags",
                'Tier': "some-tier",
                'Policies': "some-policies",
                'DataType': "some-data-type"
            }
        }

        expected_response = {
            'Name': "some-name",
            'Value': "some-value",
            'Description': "some-description",
            'Type': "some-type",
            'KeyId': "some-key-id",
            'Overwrite': True,
            'AllowedPattern': "some-allowed-pattern",
            'Tags': "some-tags",
            'Tier': "some-tier",
            'Policies': "some-policies",
            'DataType': "some-data-type"
        }

        assert app.construct_param_args(sample_event) == expected_response

    def test_set_boolean_flag_no_flag(self):
        """Set Boolean Flag call with no such field in request"""
        sample_event = {
            'ResourceProperties': {}
        }
        expected_response = False
        assert expected_response == app.set_boolean_flag(sample_event, "some-flag")

    def test_set_boolean_flag_false(self):
        """Set Boolean Flag call with field set to false"""
        sample_event = {
            'ResourceProperties': {
                "some-flag": "False"
            }
        }

        expected_response = False
        assert expected_response == app.set_boolean_flag(sample_event, "some-flag")

    def test_set_boolean_flag_true(self):
        """Set Boolean Flag call with field set to true"""
        sample_event = {
            'ResourceProperties': {
                "some-flag": "True"
            }
        }

        expected_response = True
        assert expected_response == app.set_boolean_flag(sample_event, "some-flag")


if __name__ == '__main__':
    unittest.main()
