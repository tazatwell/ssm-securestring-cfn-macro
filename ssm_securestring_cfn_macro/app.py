import json
import cfnresponse
import boto3

# import requests


def lambda_handler(event, context):

    print(event)

    print(context)

    if not event:
        cfnresponse.send(event, context, cfnresponse.FAILED, "Input event is empty", None)

    if 'RequestType' not in event:
        cfnresponse.send(event, context, cfnresponse.FAILED, "Input event has no RequestType field", None)

    if event['RequestType'] == 'Create':
        # create SSM Param here
        ssm_client = boto3.client('ssm')
        # ssm_client.put_parameter(...)
        cfnresponse.send(event, context, cfnresponse.SUCCESS, "Sample success", None)
    elif event['RequestType'] == 'Update':
        # create SSM Param here
        cfnresponse.send(event, context, cfnresponse.SUCCESS, "Sample success", None)
    elif event['RequestType'] == 'Delete':
        # delete SSM Param here
        cfnresponse.send(event, context, cfnresponse.SUCCESS, "Sample success", None)
    else:
        cfnresponse.send(event, context, cfnresponse.FAILED, "Input event has invalid RequestType field: " + event['RequestType'], None)


    return {
        "Status": "SUCCESS",
        "PhysicalResourceId": "some-resource-id",
        "StackId": "some-stack-id",
        "RequestId": "some-request-id",
        "LogicalResourceId": "some-logical-resource-id",
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
