"""
ssm_securestring_cfn_macro
    Lambda Application Code to create AWS SSM SecureString Parameters using a CloudFormation Macro
        uses boto3 library for aws api
        uses cfnresponse library to send status response object
"""

import json
import cfnresponse

import ssm.client as ssm
from log import logger

def lambda_handler(event, context):     # pragma: no cover
    """Lambda Handler entrypoint for lambda"""

    try:
        validate_request(event)
    except Exception as exc:
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            {
                'Status': "FAILED",
                'Reason': f"Error processing ssm request. Type: {type(exc)}. Error: {exc}",
                'PhysicalResourceId': "",
                'StackId': event['StackId'],
                'RequestId': event['RequestId'],
            }
        )

    ignore_param_not_found = set_boolean_flag(event, "IgnoreParamNotFound")

    debug = set_boolean_flag(event, "Debug")

    logger.add_log(
        debug,
        event
    )

    logger.add_log(
        debug,
        context
    )

    ssm_client = ssm.create_client()

    try:
        response = process_ssm_request(event, ssm_client, ignore_param_not_found, debug)
    except Exception as exc:
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            {
                'Status': "FAILED",
                'Reason': f"Error processing ssm request. Type: {type(exc)}. Error: {exc}",
                'PhysicalResourceId': event['ResourceProperties']['Name'],
                'StackId': event['StackId'],
                'RequestId': event['RequestId'],
            }
        )

    else:
        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            {
                'Status': "SUCCESS",
                'Reason': f"Successfully performed ssm operation. Reason: {response}",
                'PhysicalResourceId': event['ResourceProperties']['Name'],
                'StackId': event['StackId'],
                'RequestId': event['RequestId'],
            }
        )

def process_ssm_request(event, ssm_client, ignore_param_not_found, debug):
    """Perform ssm create_parameter or delete_parameter based by event"""
    if event['RequestType'] == "Create" or event['RequestType'] == "Update":
        try:
            param_args = construct_param_args(event, debug)
        except Exception as exc:
            logger.add_log(
                debug,
                f"Error processing parameters. Type: {type(exc)}. Error: {exc}"
            )
            raise exc

        try:
            response = ssm.put_parameter(ssm_client, param_args, debug)

        except Exception as exc:
            logger.add_log(
                debug,
                f"Error creating parameter. Type: {type(exc)}. Error: {exc}"
            )
            raise exc

        else:
            logger.add_log(
                debug,
                f"Successfully performed put-parameter operation. Response: {response}"
            )
            return response

    elif event['RequestType'] == 'Delete':
        param_args = construct_param_args(event, debug)

        try:
            response = ssm.delete_parameter(ssm_client, param_args, debug, ignore_param_not_found)

        except Exception as exc:
            logger.add_log(
                debug,
                f"Error deleting parameter. Type: {type(exc)}. Error: {exc}"
            )
            raise exc

        else:
            logger.add_log(
                debug,
                f"Successfully performed delete-parameter operation. Response: {response}"
            )
            return response

    else:
        raise CustomLambdaRuntimeException(f"InvalidRequestType: {event['RequestType']}")


def set_boolean_flag(event, flag_name):
    """Set flag"""
    flag = False
    if flag_name in event['ResourceProperties']:
        if event['ResourceProperties'][flag_name].lower() == "true":
            flag = True
    return flag

def construct_param_args(event, debug):
    """Construct arguments for ssm put-parameter operation"""
    param_args = {}
    param_args['Name'] = event['ResourceProperties']['Name']

    if event['RequestType'] == "Delete":
        return param_args

    if 'Value' in event['ResourceProperties']:
        param_args['Value'] = event['ResourceProperties']['Value']

    if 'Description' in event['ResourceProperties']:
        param_args['Description'] = event['ResourceProperties']['Description']

    if 'Type' in event['ResourceProperties']:
        param_args['Type'] = event['ResourceProperties']['Type']

    if 'KeyId' in event['ResourceProperties']:
        param_args['KeyId'] = event['ResourceProperties']['KeyId']

    if 'Overwrite' in event['ResourceProperties']:
        if event['ResourceProperties']['Overwrite'].lower() == 'true':
            param_args['Overwrite'] = True
        else:
            param_args['Overwrite'] = False

    if 'AllowedPattern' in event['ResourceProperties']:
        param_args['AllowedPattern'] = event['ResourceProperties']['AllowedPattern']

    if 'Tags' in event['ResourceProperties']:
        try:
            json_tags = json.loads(event['ResourceProperties']['Tags'])

        except json.decoder.JSONDecodeError as exc:
            logger.add_log(
                debug,
                f"Received error encoding {event['ResourceProperties']['Tags']} into json"
            )
            raise exc

        else:
            if not isinstance(json_tags, list):
                raise CustomLambdaRuntimeException(
                    f"Tags object {event['ResourceProperties']['Tags']} must be a list of maps"
                )

            for json_tags_iter in json_tags:
                if not isinstance(json_tags_iter, dict):
                    raise CustomLambdaRuntimeException(
                        f"Tags object {event['ResourceProperties']['Tags']} must be a list of maps"
                    )

            param_args['Tags'] = json_tags

    if 'Tier' in event['ResourceProperties']:
        param_args['Tier'] = event['ResourceProperties']['Tier']

    if 'Policies' in event['ResourceProperties']:
        param_args['Policies'] = event['ResourceProperties']['Policies']

    if 'DataType' in event['ResourceProperties']:
        param_args['DataType'] = event['ResourceProperties']['DataType']

    return param_args

def validate_request(event):
    """Perform high level validation on input"""

    if 'ResourceProperties' not in event:
        raise CustomLambdaRuntimeException("No Resource Properties key in request")

    if 'Name' not in event['ResourceProperties']:
        raise CustomLambdaRuntimeException("No Name key in request's ResourceProperties field")

    return True


class CustomLambdaRuntimeException(Exception):
    """
        Thrown for various reasons
        pass message param to set the custom message
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
