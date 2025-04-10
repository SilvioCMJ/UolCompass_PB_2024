import os
import boto3
import json
from botocore.exceptions import BotoCoreError, ClientError

# Inicializa o recurso do DynamoDB usando boto3.
dynamodb = boto3.resource('dynamodb')


def list_item_db(event, context):
    """Listar todos os itens do DynamoDB."""

    # Acessa a tabela DynamoDB a partir da variável de ambiente DB_TABLE_NAME.
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])

    try:
        # Faz a primeira leitura (scan) da tabela para obter todos os itens.
        response = table.scan()
        data = response['Items']  # Armazena os itens obtidos.

        # Continua escaneando enquanto houver mais dados a serem buscados.
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])  # Adiciona os itens ao conjunto de dados já coletado.

    except (BotoCoreError, ClientError) as error:
        # Captura erros relacionados ao boto3 ou ao cliente da AWS e retorna uma resposta de erro.
        print(error)
        return {
            "statusCode": 500,
            "headers": {'Content-Type': 'application/json'},
            "body": json.dumps({
                "message": "Error fetching records from DynamoDB.",
                "error": str(error)
            })
        }

    # Retorna os dados em formato JSON com um status de sucesso.
    return {
        "statusCode": 200,
        "headers": {'Content-Type': 'application/json'},
        "body": json.dumps(data)
    }
