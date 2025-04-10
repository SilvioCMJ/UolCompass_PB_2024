import json
import os
import boto3
from aws.dynamodb.get_item_db import get_item_db

# Inicializa os recursos do DynamoDB e S3 usando boto3.
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')


def find_file_with_id(file_id):
    """Procurar um arquivo no S3 com base no ID fornecido."""

    # Lista os objetos em uma pasta específica no bucket do S3.
    response = s3_client.list_objects_v2(
        Bucket=os.environ['BUCKET_NAME'],
        Prefix=os.environ['AUDIO_S3_DIR']
    )

    # Itera sobre os arquivos e verifica se o ID fornecido está no nome do arquivo.
    for obj in response['Contents']:
        file_name = obj['Key']

        if file_id in file_name:
            return file_name

    # Retorna None se nenhum arquivo for encontrado com o ID especificado.
    return


def delete_record(event, context):
    """Deletar um registro no DynamoDB e o arquivo correspondente no S3."""

    # Acessa a tabela DynamoDB a partir da variável de ambiente DB_TABLE_NAME.
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    
    # Obtém o ID do usuário a partir dos parâmetros da URL (event).
    user_id = event['pathParameters']['id']

    # Busca o registro no banco de dados usando o ID fornecido.
    result = get_item_db(user_id)

    if result:

        # Deleta o registro correspondente no DynamoDB.
        table.delete_item(
            Key={
                os.environ['DB_PART_KEY']: user_id
            }
        )

        # Procura o arquivo de áudio no S3 que corresponde ao ID fornecido.
        file_name = find_file_with_id(user_id)

        # Deleta o arquivo de áudio do bucket S3 se ele for encontrado.
        if file_name:
            s3_client.delete_object(
                Bucket=os.environ['BUCKET_NAME'],
                Key=file_name
            )

        # Cria uma resposta indicando sucesso na deleção.
        response = {
            "statusCode": 200,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps({"message": f"File with ID {user_id} deleted."})
        }

        return response
    
    else:
        # Retorna uma resposta de erro caso o ID não seja encontrado no banco de dados.
        return {
            "statusCode": 400,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps({"message": "ID Not found."})
        }
