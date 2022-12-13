"""
ssm_securestring_cfn_macro
    Lambda Application Code to create AWS SSM SecureString Parameters using a CloudFormation Macro
        uses boto3 library for aws api
        uses cfnresponse library to send status response object
        uses included put_parameter_args to unit test handling input to aws ssm api call

"""

import cfnresponse
import boto3

def lambda_handler(event, context):
    """Lambda Handler entrypoint for lambda"""

    print(event)

    print(context)

    validate, validateError = validate_request(event)
    if validate == False:
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            {'Reason': f"{validateError}"}
        )

    if event['RequestType'] == "Create" or event['RequestType'] == "Update":
        ssm_client = boto3.client("ssm")
        put_parameter_args = put_param_args(event['ResourceProperties'])

        ssm_client.put_parameter(put_parameter_args.construct_put_parameter_args())

        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            f"Created parameter. Arguments: {put_parameter_args.construct_put_parameter_args()}"
        )

    elif event['RequestType'] == 'Delete':
        # delete SSM Param here
        ssm_client = boto3.client('ssm')

        ssm_client.delete_parameter(Name=event['ResourceProperties']['Name'])

        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            f"Deleted parameter {event['ResourceProperties']['Name']}"
        )

    else:
        cfnresponse.send(
            event,
            context,
            cfnresponse.FAILED,
            f"Input event has invalid RequestType field: {event['RequestType']}"
        )

def validate_request(event):
    """Perform high level validation based on put_parameter args"""

    if 'ResourceProperties' not in event:
        return (False, "No Resource Properties key in request")

    if 'Name' not in event['ResourceProperties']:
        return (False, "No Name key in request's ResourceProperties field")

    if 'Value' not in event['ResourceProperties']:
        return (False, "No Value key in request's ResourceProperties field")

    if 'Type' not in event['ResourceProperties'] and event['RequestType'] == "Create":
        return (False, "No Type key in request's ResourceProperties field. Type must be specified when creating an SSM Parameter")

    return True, None

def construct_put_parameter_args(eventProps):
    """
        Construct args passed to ssm.put_parameter_args
        Handles dynamic event properties
    """

    put_parameter_args = {}
    put_parameter_args['Name'] = eventProps['Name']
    put_parameter_args['Value'] = eventProps['Value']

    if 'Description' in eventProps:
        put_parameter_args['Description'] = eventProps['Description']

    if 'Type' in eventProps:
        put_parameter_args['Type'] = eventProps['Type']

    if 'KeyId' in eventProps:
        put_parameter_args['KeyId'] = eventProps['KeyId']
    if 'Overwrite' in eventProps:
        put_parameter_args['Overwrite'] = eventProps['Overwrite']
    if 'AllowedPattern' in eventProps:
        put_parameter_args['AllowedPattern'] = eventProps['AllowedPattern']
    if 'Tags' in eventProps:
        put_parameter_args['Tags'] = eventProps['Tags']
    if 'Tier' in eventProps:
        put_parameter_args['Tier'] = eventProps['Tier']
    if 'Policies' in eventProps:
        put_parameter_args['Policies'] = eventProps['Policies']
    if 'DataType' in eventProps:
        put_parameter_args['DataType'] = eventProps['DataType']

    return put_parameter_args
