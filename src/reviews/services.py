from botocore.exceptions import ClientError
import json
import logging
import boto3

logger = logging.getLogger(__name__)


def get_book_info(isbn):
    """
    Gets information about a book from the Open Library API.

    Returns the payload of the Lambda function, including the statusCode
    """
    lambda_client = boto3.client("lambda")
    iam_resource = boto3.resource("iam")
    wrapper = LambdaWrapper(lambda_client, iam_resource)
    response = wrapper.invoke_function("scalestack-lambda", {"isbn": isbn})
    if "FunctionError" in response:
        logger.error("Couldn't get book info for ISBN %s.", isbn)
        return None
    return json.loads(response["Payload"].read().decode("utf-8"))


class LambdaWrapper:
    def __init__(self, lambda_client, iam_resource):
        self.lambda_client = lambda_client
        self.iam_resource = iam_resource

    def invoke_function(self, function_name, function_params, get_log=False):
        """
        Invokes a Lambda function.

        :param function_name: The name of the function to invoke.
        :param function_params: The parameters of the function as a dict. This dict
                                is serialized to JSON before it is sent to Lambda.
        :param get_log: When true, the last 4 KB of the execution log are included in
                        the response.
        :return: The response from the function invocation.
        """
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                Payload=json.dumps(function_params),
                LogType="Tail" if get_log else "None",
            )
            logger.info("Invoked function %s.", function_name)
        except ClientError:
            logger.exception("Couldn't invoke function %s.", function_name)
            raise
        return response
