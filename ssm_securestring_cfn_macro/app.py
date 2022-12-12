import json
import cfnresponse
import boto3
import put_parameter_args as param_args
# import requests


def lambda_handler(event, context):

    print(event)

    print(context)

    if 'ResourceProperties' not in event:
      cfnresponse.send(event, context, cfnresponse.FAILED, {'Reason': "No Resource Properties key in Request"})

    if 'Name' not in event['ResourceProperties']:
      cfnresponse.send(event, context, cfnresponse.FAILED, {'Reason': "No Name key in Request"})

    if 'Value' not in event['ResourceProperties']:
      cfnresponse.send(event, context, cfnresponse.FAILED, {'Reason': "No Value key in Request"})

    if 'Type' not in event['ResourceProperties'] and event['RequestType'] == "Create":
      cfnresponse.send(event, context, cfnresponse.FAILED, {'Reason': "Type key must be specified when creating an SSM Parameter"}) 

    if event['RequestType'] == 'Create':
      ssm_client = boto3.client('ssm')
      put_parameter_args = param_args(event['ResourceProperties'])

      ssm_client.put_parameter(put_parameter_args.construct_parameter_args())

      cfnresponse.send(event, context, cfnresponse.SUCCESS, "Created parameter. Arguments: {}".format(put_parameter_args.construct_parameter_args))

    elif event['RequestType'] == 'Update':
      ssm_client = boto3.client('ssm')
      put_parameter_args = param_args(event['ResourceProperties'])

      ssm_client.put_parameter(put_parameter_args.construct_parameter_args())

      cfnresponse.send(event, context, cfnresponse.SUCCESS, "Updated parameter. Arguments: {}".format(put_parameter_args.construct_parameter_args))

    elif event['RequestType'] == 'Delete':
      # delete SSM Param here
      ssm_client = boto3.client('ssm')

      ssm_client.delete_parameter(Name=event['ResourceProperties']['Name'])

      cfnresponse.send(event, context, cfnresponse.SUCCESS, "Deleted parameter {}".format(event['ResourceProperties']['Name']))

    else:
      cfnresponse.send(event, context, cfnresponse.FAILED, "Input event has invalid RequestType field: " + event['RequestType'])

