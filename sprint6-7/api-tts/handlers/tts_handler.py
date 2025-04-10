import json
from aws.polly.polly_service import synthesize_speech
from aws.s3.s3_service import upload_to_s3
from aws.dynamodb.create_record_db import create_record
from utils.hash_util import create_hash_sha256
from aws.dynamodb.get_item_db import get_item_db

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
    except (json.JSONDecodeError, KeyError) as e:
        return {
            "statusCode": 400,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps({"message": "Invalid request. Body must be a valid JSON with 'phrase' key."})
        }

    if "phrase" not in body or len(body) != 1:
        return {
            "statusCode": 400,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps({"message": "Invalid key in the request body."})
        }

    text = body.get("phrase")
    
    # Verifica se já existe no DynamoDB
    hashcode = create_hash_sha256(text)
    existing_record = get_item_db(hashcode)
    if existing_record:
        return {
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps(existing_record)
        }

    # Caso não exista, gera o áudio
    audio_file = synthesize_speech(text)
    if not audio_file:
        return {
            "statusCode": 500,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps({"message": "Error synthesizing speech."})
        }

    # Faz o upload para o S3
    url_file = upload_to_s3(audio_file, text, hashcode)
    if not url_file:
        return {
            "statusCode": 500,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps({"message": "Error uploading the file to S3."})
        }

    # Salva o registro no DynamoDB
    create_record(text, url_file)

    # Retorna o resultado final
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(get_item_db(hashcode), ensure_ascii=False)
    }
