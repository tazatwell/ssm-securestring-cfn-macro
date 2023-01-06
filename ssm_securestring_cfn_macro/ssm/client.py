"""
ssm
    Wrapper for boto3.ssm module
"""

import boto3

from log import logger

def create_client():        # pragma: no cover
    """Create SSM Client"""
    return boto3.client("ssm")

def put_parameter(client, put_parameter_args, debug):
    """SSM Put Parameter"""
    try:
        response = client.put_parameter(**put_parameter_args)

    except Exception as exc:
        logger.add_log(
            debug,
            f"Error calling aws ssm put-parameter operation. Type: {type(exc)}. Error: {exc}"
        )
        raise exc

    else:
        return response

def delete_parameter(client, delete_parameter_args, debug, ignore_param_not_found):
    """SSM Delete Parameter"""
    try:
        response = client.delete_parameter(**delete_parameter_args)

    except Exception as exc:
        if isinstance(exc, client.exceptions.ParameterNotFound):
            if ignore_param_not_found is True:
                return {}

            logger.add_log(
                debug,
                ("Error calling aws ssm delete-parameter operation. Error: ParameterNotFound.\n"
                f"You can omit this error by setting the ParameterNotFound property"
                )
            )

        else:
            logger.add_log(
                debug,
                f"Error calling aws ssm delete-parameter operation. Type: {type(exc)}. Error: {exc}"
            )
        raise exc

    else:
        return response
