import json

def lambda_handler(event, context):
    response = json.loads(event)
    text = response['text'] 
    payload = json.loads(response['Payload'])

    rules=''
    prompts = ''
    items = []
    response['prompt']  = "Human: Please provide the information asked in a json format: \n"
    
    index = 1
    for  key in payload.keys():
        if payload[key]['rule'] != '':
            rules   = str(rules)   + str(index) +". " + payload[key]['rule']  +'\n' 
            index += 1

    index = 1
    for  key in payload.keys():
        if payload[key]['prompt'] != '':
           prompts = str(prompts) + str(index) +". " + payload[key]['prompt'] +'\n' 
           index += 1
    
    items = ''
    for  key in payload.keys():
        if payload[key]['item'] != '':
           items = str(items)  + key + ':' + payload[key]['item'] +'\n' 

        
    response['prompt']  = response['prompt']  + f"""
    <rule>
    {rules}
    </rule>
    <items>
    {prompts}
    </items>
    text:
    <text>
    {text}
    </text>
    
    example of the response in json format is:
    <json>
        {items}
    </json>
    Assistant:"""
    print(response['prompt'])
    return  json.dumps(response)
