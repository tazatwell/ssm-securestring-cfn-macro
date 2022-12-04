import json
import cfnresponse
import boto3

# import requests


def lambda_handler(event, context):

    print(event)

    print(context)

    if 'ResourceProperties' not in event:
      cfnresponse.send(event, context, cfnresponse.FAILED, {'Reason': "No Resource Properties key in Request"}, event['PhysicalResourceId'])

    if 'Name' not in event['ResourceProperties']:
      cfnresponse.send(event, context, cfnresponse.FAILED, {'Reason': "No Name key in Request"}, event['PhysicalResourceId'])

    if 'Value' not in event['ResourceProperties']:
      cfnresponse.send(event, context, cfnresponse.FAILED, {'Reason': "No Value key in Request"}, event['PhysicalResourceId'])

    if 'Type' not in event['ResourceProperties'] and event['RequestType'] == "Create":
      cfnresponse.send(event, context, cfnresponse.FAILED, {'Reason': "Type key must be specified when creating an SSM Parameter"}, event['PhysicalResourceId']) 

    if event['RequestType'] == 'Create':
      # create SSM Param here
      ssm_client = boto3.client('ssm')
      ssm_client.put_parameter(
        Name=event['ResourceProperties']['Name'],
        Description=event['ResourceProperties']['Description'],
        Value=event['ResourceProperties']['Value'],
        Type=event['ResourceProperties']['Type'],
        KeyId=event['ResourceProperties']['KeyId'],
        Overwrite=event['ResourceProperties']['Overwrite'],
        AllowedPattern=event['ResourceProperties']['AllowedPattern'],
        Tags=event['ResourceProperties']['Tags'],
        Tier=event['ResourceProperties']['Tier'],
        Policies=event['ResourceProperties']['Policies'],
        DataType=event['ResourceProperties']['DataType']
      )
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
