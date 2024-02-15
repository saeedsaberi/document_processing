import json, boto3

def lambda_handler(event, context):
    # TODO implement
    
    response                   = json.loads(event)
    bedrock                    = boto3.client(service_name="bedrock")
    response['body']['prompt'] = response['prompt']
    
    try:
        response['response'] = bedrock.invoke_model(
                                            body        = response['body'], 
                                            modelId     = response['modelId'], 
                                            accept      = response['accept'],
                                            contentType = response['contentType'] 
                                        )
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        return {'statusCode': 500, 'body': 'Error invoking LLM'}



    return json.dump(response)
