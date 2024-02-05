# document_processing

This repository process scan of documents and use LLM to reerieve desired information from the document. 
The AWS CDK project deploys an S3 bucket and a Step Function with Lambda functions.

## Project Structure

- `cdk/`: Contains AWS CDK stacks.
  - `s3_bucket_cdk_stack.py`: Defines the CDK stack for the S3 bucket.
  - `step_function_cdk_stack.py`: Defines the CDK stack for the Step Function.

- `lambdas/`: Contains Lambda functions.
  - `make_config/`: Lambda function for the "MakeConfig" step.
    - `lambda_handler.py`: Contains the Lambda function code.
    - `requirements.txt`: Lists the Python dependencies for this Lambda function.
  - `retrieve_text/`: Lambda function for the "RetrieveText" step.
    - `lambda_handler.py`: Contains the Lambda function code.
    - `requirements.txt`: Lists the Python dependencies for this Lambda function.
  - `make_prompt/`: Lambda function for the "MakePrompt" step.
    - `lambda_handler.py`: Contains the Lambda function code.
    - `requirements.txt`: Lists the Python dependencies for this Lambda function.
  - `call_llm/`: Lambda function for the "CallLlm" step.
    - `lambda_handler.py`: Contains the Lambda function code.
    - `requirements.txt`: Lists the Python dependencies for this Lambda function.
  - `post_processing/`: Lambda function for the "PostProcessing" step.
    - `lambda_handler.py`: Contains the Lambda function code.
    - `requirements.txt`: Lists the Python dependencies for this Lambda function.

- `cdk.json`: Configuration file for CDK.
- `requirements.txt`: Lists any global dependencies for your CDK project.

## Getting Started

1. **Install CDK**: Run `npm install -g aws-cdk` to install the AWS CDK globally.
2. **Bootstrap CDK**: Run `cdk bootstrap` to set up necessary resources in your AWS account.
3. **Deploy Stacks**: Run `cdk deploy` to deploy your CDK stacks.

## Local Development

- Each Lambda function directory contains its code and dependencies. To update the Lambda functions, modify the code and run `cdk deploy`.

## Cleanup

To remove all deployed resources:

```bash
cdk destroy
