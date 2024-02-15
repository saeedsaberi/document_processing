import json, boto3
from io import BytesIO

def lambda_handler(event, context):
    textract_client = boto3.client('textract')
    s3 = boto3.client('s3')
    response = json.loads(event)
    
    file_path = response.get('file_path', {})
    bucket_name = response.get('bucket_name', {})
    
    
    print([(response.keys()), file_path, bucket_name, '\n', response ])
    # Download the file from S3
    try:
        response = s3.get_object(Bucket=bucket_name, Key=file_path)
        img_test = response['Body'].read()
        bytes_test = bytearray(img_test)
    except Exception as e:
        print(f"Error downloading file from S3: {e}")
        return {'statusCode': 500, 'body': 'Error downloading file from S3'}

    # Analyze the document using Textract
    try:
        textract_response = textract_client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['TABLES'])
        blocks = textract_response['Blocks']
        text = ""
        for block in blocks:
            if block['BlockType'] == 'WORD':
                text += block['Text'] + ' '
    except Exception as e:
        print(f"Error analyzing document with Textract: {e}")
        return {'statusCode': 500, 'body': 'Error analyzing document with Textract'}


    print("Extracted Text:", text)

    # Include the extracted text in the response
    response = json.loads(event)
    response['text'] = text[:-1]
    print('text',response['text'] )
    return json.dumps(response)
