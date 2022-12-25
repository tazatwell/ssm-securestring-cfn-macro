"""
    Unit Test handler Function
"""

import unittest

from app import validate_request
from app import construct_param_args

class HandlerTest(unittest.TestCase):
    """Unit Test Handler Function"""

    def test_verify_request_no_resource_properties(self):
        """Request with no 'ResourceProperties' field"""
        sample_event = {}
        expected_response = False
        actual_response, actual_err = validate_request(sample_event)
        assert expected_response == actual_response
        assert actual_err == "No Resource Properties key in request"

    def test_verify_request_no_name_field(self):
        """Request with no 'Name' key in 'ResourceProperties' field"""
        sample_event = {}
        sample_event['ResourceProperties'] = {}
        expected_response = False
        actual_response, actual_err = validate_request(sample_event)
        assert expected_response == actual_response
        assert actual_err == "No Name key in request's ResourceProperties"

    def test_verify_request_proper(self):
        """Request with proper 'ResourceProperties' field"""
        sample_event = {}
        sample_event['ResourceProperties'] = {}
        sample_event['ResourceProperties']['Name'] = "some-name"
        expected_response = True
        actual_response, actual_err = validate_request(sample_event)
        assert expected_response == actual_response
        assert actual_err is None

    def test_construct_param_args_delete(self):
        """Request with Delete request type"""
        sample_event = {}
        sample_event['RequestType'] = "Delete"
        sample_event['ResourceProperties'] = {}
        sample_event['ResourceProperties']['Name'] = "some-name"
        expected_response = {'Name': "some-name"}
        assert construct_param_args(sample_event) == expected_response

    def test_construct_param_args_create_with_all_args(self):
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
            'Overwrite': "some-overwrite",
            'AllowedPattern': "some-allowed-pattern",
            'Tags': "some-tags",
            'Tier': "some-tier",
            'Policies': "some-policies",
            'DataType': "some-data-type"
        }
        assert construct_param_args(sample_event) == expected_response

if __name__ == '__main__':
    unittest.main()
