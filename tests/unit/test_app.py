"""
    Unit Test handler Function
"""

import unittest
import pytest

from app import validate_request
from app import construct_param_args
from app import set_boolean_flag
from app import CustomLambdaRuntimeException

class HandlerTest(unittest.TestCase):
    """Unit Test Handler Function"""

    def test_verify_request_no_resource_properties(self):
        """Request with no 'ResourceProperties' field"""
        sample_event = {}
        with pytest.raises(CustomLambdaRuntimeException) as e_info:
            validate_request(sample_event)

    def test_verify_request_no_name_field(self):
        """Request with no 'Name' key in 'ResourceProperties' field"""
        sample_event = {}
        sample_event['ResourceProperties'] = {}
        with pytest.raises(CustomLambdaRuntimeException) as e_info:
            validate_request(sample_event)

    def test_verify_request_proper(self):
        """Request with proper 'ResourceProperties' field"""
        sample_event = {}
        sample_event['ResourceProperties'] = {}
        sample_event['ResourceProperties']['Name'] = "some-name"
        expected_response = True
        actual_response = validate_request(sample_event)
        assert expected_response == actual_response

    def test_construct_param_args_delete(self):
        """Request with Delete request type"""
        sample_event = {}
        sample_event['RequestType'] = "Delete"
        sample_event['ResourceProperties'] = {}
        sample_event['ResourceProperties']['Name'] = "some-name"
        expected_response = {'Name': "some-name"}
        assert construct_param_args(sample_event) == expected_response

    def test_construct_param_args_create_with_all_args_overwrite_false(self):
        """Request with Create request type and all create args present"""
        sample_event = {}
        sample_event['RequestType'] = "Create"
        sample_event['ResourceProperties'] = {}
        sample_event['ResourceProperties']['Name'] = "some-name"
        sample_event['ResourceProperties']['Value'] = "some-value"
        sample_event['ResourceProperties']['Description'] = "some-description"
        sample_event['ResourceProperties']['Type'] = "some-type"
        sample_event['ResourceProperties']['KeyId'] = "some-key-id"
        sample_event['ResourceProperties']['Overwrite'] = "some-overwrite"
        sample_event['ResourceProperties']['AllowedPattern'] = "some-allowed-pattern"
        sample_event['ResourceProperties']['Tags'] = "some-tags"
        sample_event['ResourceProperties']['Tier'] = "some-tier"
        sample_event['ResourceProperties']['Policies'] = "some-policies"
        sample_event['ResourceProperties']['DataType'] = "some-data-type"
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
        assert construct_param_args(sample_event) == expected_response

    def test_construct_param_args_create_with_all_args_overwrite_true(self):
        """Request with Create request type and all create args present"""
        sample_event = {}
        sample_event['RequestType'] = "Create"
        sample_event['ResourceProperties'] = {}
        sample_event['ResourceProperties']['Name'] = "some-name"
        sample_event['ResourceProperties']['Value'] = "some-value"
        sample_event['ResourceProperties']['Description'] = "some-description"
        sample_event['ResourceProperties']['Type'] = "some-type"
        sample_event['ResourceProperties']['KeyId'] = "some-key-id"
        sample_event['ResourceProperties']['Overwrite'] = "true"
        sample_event['ResourceProperties']['AllowedPattern'] = "some-allowed-pattern"
        sample_event['ResourceProperties']['Tags'] = "some-tags"
        sample_event['ResourceProperties']['Tier'] = "some-tier"
        sample_event['ResourceProperties']['Policies'] = "some-policies"
        sample_event['ResourceProperties']['DataType'] = "some-data-type"
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
        assert construct_param_args(sample_event) == expected_response
    
    def test_set_boolean_flag_no_flag(self):
        """Set Boolean Flag call with no such field in request"""
        sample_event = {}
        sample_event['ResourceProperties'] = {}
        expected_response = False
        assert expected_response == set_boolean_flag(sample_event, "some-flag")

    def test_set_boolean_flag_false(self):
        """Set Boolean Flag call with field set to false"""
        sample_event = {}
        sample_event['ResourceProperties'] = {}
        sample_event['ResourceProperties']['some-flag'] = "False"
        expected_response = False
        assert expected_response == set_boolean_flag(sample_event, "some-flag")

    def test_set_boolean_flag_true(self):
        """Set Boolean Flag call with field set to true"""
        sample_event = {}
        sample_event['ResourceProperties'] = {}
        sample_event['ResourceProperties']['some-flag'] = "True"
        expected_response = True
        assert expected_response == set_boolean_flag(sample_event, "some-flag")


if __name__ == '__main__':
    unittest.main()
