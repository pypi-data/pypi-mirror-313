import boto3
import json
from datetime import datetime


def interact_with_bedrock(
    prompt : str,
    model_id : str = "anthropic.claude-3-5-sonnet-20240620-v1:0"
) -> str:

    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [
                    # {
                    #     "type": "image",
                    #     "source": {
                    #         "type": "base64",
                    #         "media_type": "image/jpeg",
                    #         "data": encoded_image
                    #     }
                    # },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    }

    try:

        response = bedrock.invoke_model(modelId=model_id, body=json.dumps(request_body))
        response_body = json.loads(response.get("body").read())

        return response_body
    
    except bedrock.exceptions.ClientError as err:
        print(f"Couldn't invoke LLM. Here's why: {err.response['Error']['Code']}: {err.response['Error']['Message']}")
        raise


def put_item_on_dynamodb(
    table_name : str,
    partition_key : int,
    data : dict
) -> None:

    #
    dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
    table = dynamodb.Table(table_name)

    #
    data['id'] = partition_key
    data['created_at'] = str(datetime.now())

    #
    table.put_item(
        Item=data
    )