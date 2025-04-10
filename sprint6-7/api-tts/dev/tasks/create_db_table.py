import boto3
import os
from botocore.exceptions import ClientError
import importlib

add_env_var_module = importlib.import_module("api-tts.dev.tasks.check_env")
add_env_var = add_env_var_module.add_env_var


def create_table(table_name, part_key):
    dynamodb = boto3.client('dynamodb')

    # Verifica se a tabela já existe
    existing_tables = dynamodb.list_tables()['TableNames']
    if table_name in existing_tables:
        print(f"Tabela {table_name} já existe.")
    else:
        try:
            # Cria a tabela DynamoDB
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': part_key, 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': part_key, 'AttributeType': 'S'}
                ],
                BillingMode='PAY_PER_REQUEST'
            )
            print(f"Tabela {table_name} criada.")
        except ClientError as e:
            print(f"Erro ao criar a tabela: {e}")
            return False

    # Adicionar as informações ao .env
    add_env_var({
        "DB_TABLE_NAME": table_name, 
        "DB_PART_KEY": part_key
        })

    return True

if __name__ == "__main__":
    table_name = "sprint-6-7-table"
    part_key = "unique_id"
    create_table(table_name, part_key)
