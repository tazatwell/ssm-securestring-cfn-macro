"""
ssm
    Wrapper for boto3.ssm module
"""

import boto3

def create_client():        # pragma: no cover
    """Create SSM Client"""
    return boto3.client("ssm")

def put_parameter(client, put_parameter_args):
    """SSM Put Parameter"""
    try:
        response = client.put_parameter(**put_parameter_args)

    except Exception as exc:
        print(
            f"Error calling aws ssm put-parameter operation. Type: {type(exc)}. Error: {exc}"
        )
        raise exc

    else:
        return response

def delete_parameter(client, delete_parameter_args):
    """SSM Delete Parameter"""
    try:
        response = client.delete_parameter(**delete_parameter_args)

    except Exception as exc:
        print(
            f"Error calling aws ssm delete-parameter operation. Type: {type(exc)}. Error: {exc}"
        )
        raise exc

    else:
        return response
