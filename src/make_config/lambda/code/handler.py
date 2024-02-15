from aws_cdk import (
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    core
)

class LambdaCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Lambda function
        lambda_function = _lambda.Function(
            self, "MyLambdaFunction",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="index.lambda_handler",
            code=_lambda.Code.from_asset("make_config/lambda/code"),
            environment={
                'MODEL_ID': 'anthropic.claude-instant-v1'
            }
        )

        # Define Lambda function's rules
        rules = {
            'student_name': {
                'prompt': 'Please respond with student name, holder of this certificate, as stated in this document.',
                'rule': '',
                'item': 'Saeed Saberi'
            },
            'university_name': {
                'prompt': 'Please response with student name, holder of this certificate, as stated in this document.',
                'rule': 'for university_name if the city name exists right after the university name, include it in the name of the university',
                'item': 'simon fraser university'
            }
        }

        # Lambda function environment variables
        lambda_function.add_environment("RULES", json.dumps(rules))
        lambda_function.add_environment("BODY", json.dumps({
            "prompt": "",
            "max_tokens_to_sample": 1024,
            "top_k": 1,
            "temperature": 0.,
            "top_p": 0.999
        }))
        lambda_function.add_environment("ACCEPT", "application/json")
        lambda_function.add_environment("CONTENT_TYPE", "application/json")

        # Create API Gateway
        api = apigateway.RestApi(
            self, "MyApi",
            rest_api_name="MyApi",
            description="My API Gateway"
        )

        # Create Lambda integration for API Gateway
        integration = apigateway.LambdaIntegration(
            lambda_function,
            integration_responses=[
                apigateway.IntegrationResponse(
                    status_code="200",
                    response_parameters={
                        'method.response.header.Content-Type': "'application/json'"
                    }
                )
            ]
        )

        # Define API Gateway resource and method
        api_resource = api.root.add_resource("myresource")
        api_resource.add_method("POST", integration)

app = core.App()
LambdaCdkStack(app, "LambdaCdkStack")
app.synth()
