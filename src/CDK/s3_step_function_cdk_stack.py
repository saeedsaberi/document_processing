import sys
print('aha',sys.path)

from aws_cdk import (
    aws_stepfunctions as sfn,
    aws_stepfunctions_tasks as tasks,
    aws_lambda as _lambda,
    # core,
    aws_s3 as s3,
    Stack, App
)

class S3BucketCdkStack(Stack):
    def __init__(self, app: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket
        document_processing_bucket = s3.Bucket(
            self, "DocumentProcessingBucket",
            bucket_name="document_processing",
            removal_policy=core.RemovalPolicy.DESTROY  # WARNING: This will delete the bucket and its content when the stack is deleted
        )


class StepFunctionCdkStack(Stack):

    def __init__(self, , app: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Lambda functions
        lambda_make_config = _lambda.Function(
            self, "MakeConfigLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("make_config/lambda/code")
        )

        lambda_retrieve_text = _lambda.Function(
            self, "RetrieveTextLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("retrieve_text/lambda/code")
        )

        lambda_make_prompt = _lambda.Function(
            self, "MakePromptLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("make_prompt/lambda/code")
        )

        lambda_call_llm = _lambda.Function(
            self, "CallLlmLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("call_llm/lambda/code")
        )

        lambda_post_processing = _lambda.Function(
            self, "PostProcessingLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("post_processing/lambda/code")
        )

        # Define Step Functions state machine
        definition = (
            tasks.LambdaInvoke(
                self, "MakeConfig",
                lambda_function=lambda_make_config,
                input_path="$.myStateInput",
                result_path="$.Payload",
                retry_on_error=["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException", "Lambda.TooManyRequestsException"]
            )
            .next(
                tasks.LambdaInvoke(
                    self, "RetrieveText",
                    lambda_function=lambda_retrieve_text,
                    input_path="$.Payload",
                    result_path="$.Payload",
                    retry_on_error=["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException", "Lambda.TooManyRequestsException"]
                )
            )
            .next(
                tasks.LambdaInvoke(
                    self, "MakePrompt",
                    lambda_function=lambda_make_prompt,
                    input_path="$.Payload",
                    result_path="$.Payload",
                    retry_on_error=["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException", "Lambda.TooManyRequestsException"]
                )
            )
            .next(
                tasks.LambdaInvoke(
                    self, "CallLlm",
                    lambda_function=lambda_call_llm,
                    input_path="$.Payload",
                    result_path="$.Payload",
                    retry_on_error=["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException", "Lambda.TooManyRequestsException"]
                )
            )
            .next(
                tasks.LambdaInvoke(
                    self, "PostProcessing",
                    lambda_function=lambda_post_processing,
                    input_path="$.Payload",
                    result_path="$.Payload",
                    retry_on_error=["Lambda.ServiceException", "Lambda.AWSLambdaException", "Lambda.SdkClientException", "Lambda.TooManyRequestsException"]
                )
            )
        )

        state_machine = sfn.StateMachine(
            self, "MyStateMachine",
            definition=definition,
            timeout=core.Duration.seconds(10)
        )

app = App()
S3BucketCdkStack(app, "S3BucketCdkStack")
StepFunctionCdkStack(app, "StepFunctionCdkStack")
app.synth()
