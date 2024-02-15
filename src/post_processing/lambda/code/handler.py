from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    core
)

class RulesLambdaCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Lambda function
        lambda_function = _lambda.Function(
            self, "RulesLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("post_processing/lambda/code")
        )

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
RulesLambdaCdkStack(app, "RulesLambdaCdkStack")
app.synth()
