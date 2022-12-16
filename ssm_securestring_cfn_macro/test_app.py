"""
    Unit Test handler Function
"""

import unittest

from .app import validate_request

class HandlerTest(unittest.TestCase):
    """Unit Test Handler Function"""

    def test_verify_request_no_resource_properties(self):
        """Request with no 'ResourceProperties' field"""

        sample_event = {}
        expected_response = False
        actual_response, actual_err = validate_request(sample_event)
        assert expected_response == actual_response
        assert actual_err == "No Resource Properties key in request"

    def test_verify_request_proper(self):
        """Request with no 'ResourceProperties' field"""

        sample_event = {}
        sample_event['ResourceProperties'] = {}
        expected_response = True
        actual_response, actual_err = validate_request(sample_event)
        assert expected_response == actual_response
        assert actual_err is None

if __name__ == '__main__':      # pragma: no cover
    unittest.main()
