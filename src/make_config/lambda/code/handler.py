import json, boto3

def lambda_handler(event, context):
    rules = {}
    response ={}

    rules['student_name'] = {
        'prompt': 'Please respond with student name, holder of this certificate, as stated in this document.',
        'rule'  : '',
        "item"  : "Saeed Saberi"
    }
    rules['university_name'] = {
        'prompt': 'Please response with student name, holder of this certificate, as stated in this document.',
        'rule'  : 'for university_name if the city name exists right after the university name, include it in the name of the university',
        "item"  : "simon fraser university"
        
    }


    response['body'] = json.dumps({
        "prompt": "",
        "max_tokens_to_sample":1024,
        "top_k":1,
        "temperature":0., 
        "top_p":0.999
    })

    response['modelId']="anthropic.claude-instant-v1"
    response['accept'] = 'application/json'
    response['contentType'] = 'application/json'
    response['bucket_name'] = 'documents-processing'
    response['file_path'] = 'India-fake-diploma-sample-University-of-Kerala.jpg'
    response['Payload'] = json.dumps(rules)
    return json.dumps(response)

import json, boto3

def lambda_handler(event, context):
    rules = {}
    response ={}

    rules['student_name'] = {
        'prompt': 'Please respond with student name, holder of this certificate, as stated in this document.',
        'rule'  : '',
        "item"  : "Saeed Saberi"
    }
    rules['university_name'] = {
        'prompt': 'Please response with student name, holder of this certificate, as stated in this document.',
        'rule'  : 'for university_name if the city name exists right after the university name, include it in the name of the university',
        "item"  : "simon fraser university"
        
    }


    response['body'] = json.dumps({
        "prompt": "",
        "max_tokens_to_sample":1024,
        "top_k":1,
        "temperature":0., 
        "top_p":0.999
    })

    response['modelId']="anthropic.claude-instant-v1"
    response['accept'] = 'application/json'
    response['contentType'] = 'application/json'
    response['bucket_name'] = 'documents-processing'
    response['file_path'] = 'India-fake-diploma-sample-University-of-Kerala.jpg'
    response['Payload'] = json.dumps(rules)
    return json.dumps(response)

