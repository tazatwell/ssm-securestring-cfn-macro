"""
ssm_securestring_cfn_macro
    Lambda Application Code to create AWS SSM SecureString Parameters using a CloudFormation Macro
        uses boto3 library for aws api
        uses cfnresponse library to send status response object
"""

import cfnresponse
import boto3

def lambda_handler(event, context):     # pragma: no cover
    """Lambda Handler entrypoint for lambda"""

    print(event)

    print(context)

    validate, validate_error = validate_request(event)
    if validate is False:
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            {'Reason': f"{validate_error}"}
        )

    if event['RequestType'] == "Create" or event['RequestType'] == "Update":
        ssm_client = boto3.client("ssm")

        param_args = construct_param_args(event)

        try:
            ssm_response = ssm_client.put_parameter(**param_args)

            cfnresponse.send(
                event,
                context,
                cfnresponse.SUCCESS,
                f"Successfully performed put-parameter operation. Response: {ssm_response}"
            )

        except Exception as exc:
            print(
                f"Error calling aws ssm put-parameter operation. Type: {type(exc)}. Error: {exc}"
            )

            cfnresponse.send(
                event,
                context,
                cfnresponse.FAILED,
                f"Error calling aws ssm put-parameter operation. Type: {type(exc)}. Error: {exc}"
            )

    elif event['RequestType'] == 'Delete':
        ssm_client = boto3.client('ssm')

        param_args = construct_param_args(event)

        try:
            ssm_response = ssm_client.delete_parameter(param_args)

            cfnresponse.send(
                event,
                context,
                cfnresponse.SUCCESS,
                f"Successfully performed delete-parameter operation. Response: {ssm_response}"
            )

        except Exception as exc:
            print(
                f"Error calling aws ssm delete-parameter operation. Type: {type(exc)}. Error: {exc}"
            )

            cfnresponse.send(
                event,
                context,
                cfnresponse.FAILED,
                f"Error calling aws ssm put-parameter operation. Type: {type(exc)}. Error: {exc}"
            )

    else:
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            f"Input event has invalid RequestType field: {event['RequestType']}"
        )

def construct_param_args(event):        # pragma: no cover
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
        param_args['Overwrite'] = event['ResourceProperties']['Overwrite']

    if 'AllowedPattern' in event['ResourceProperties']:
        param_args['AllowedPattern'] = event['ResourceProperties']['AllowedPattern']

    if 'Tags' in event['ResourceProperties']:
        param_args['Tags'] = event['ResourceProperties']['Tags']

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
        return (
            False,
            "No Resource Properties key in request"
        )

    return (
        True,
        None
    )
