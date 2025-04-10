import os
import boto3
from collections import OrderedDict

# Inicializa o recurso DynamoDB usando boto3.
dynamodb = boto3.resource('dynamodb')


def get_item_db(hashcode):
    """Buscar um item específico no DynamoDB com base no hashcode fornecido."""

    # Acessa a tabela DynamoDB a partir da variável de ambiente DB_TABLE_NAME.
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])

    # Busca o item no banco de dados usando o hashcode como chave.
    result = table.get_item(
        Key={
            os.environ['DB_PART_KEY']: hashcode
        }
    )

    # Verifica se o item foi encontrado no resultado da busca.
    if 'Item' in result:
        item = result['Item']

        # Organiza os campos do item em uma ordem específica usando OrderedDict.
        ordered_item = OrderedDict([
            ('received_phrase', item.get('received_phrase')),   # Frase recebida
            ('url_to_audio', item.get('url_to_audio')),         # URL do áudio gerado
            ('created_audio', item.get('created_audio')),       # Data e hora de criação do áudio
            (os.environ['DB_PART_KEY'], item.get(os.environ['DB_PART_KEY']))  # Chave principal
        ])
        
        # Retorna o item ordenado.
        return ordered_item
    
    # Retorna None se nenhum item for encontrado no DynamoDB.
    return
