from aws_cdk import (
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_iam as iam,
    aws_apigateway as apigateway,
    core
)

class TextractLambdaCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 bucket
        bucket = s3.Bucket(
            self, "MyS3Bucket",
            removal_policy=core.RemovalPolicy.DESTROY  # WARNING: This will delete the bucket and its content when the stack is deleted
        )

        # Create Lambda function
        lambda_function = _lambda.Function(
            self, "TextractLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("path/to/your/lambda/code"),
            environment={
                'TEXTRACT_BUCKET_NAME': bucket.bucket_name
            }
        )

        # Grant permissions to Lambda function to access S3 bucket
        bucket.grant_read(lambda_function)

        # Create API Gateway
        api = apigateway.RestApi(
            self, "MyApi",
            rest_api_name="MyApi",
            description="My API Gateway"
        )

        # Create Lambda integration for API Gateway
        integration = apigateway.LambdaIntegration(lambda_function)

        # Define API Gateway resource and method
        api_resource = api.root.add_resource("myresource")
        api_resource.add_method("POST", integration)

app = core.App()
TextractLambdaCdkStack(app, "Textrac
