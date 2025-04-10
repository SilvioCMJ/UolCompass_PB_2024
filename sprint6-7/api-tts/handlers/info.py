import json  

# Função 'health' que é executada para verificar o status da aplicação
def health(event, context):
    # Monta o corpo da resposta com uma mensagem de sucesso e os dados recebidos no evento
    body = {
        "message": "Go Serverless v4.0! Your function executed successfully!",  # Mensagem de sucesso
        "input": event,  # Dados recebidos como input no evento
    }

    # Cria a resposta HTTP com o status 200 (sucesso), o corpo em formato JSON, e o cabeçalho 'Content-Type' como 'application/json'
    response = {
        "statusCode": 200,  # Código de status HTTP para sucesso
        "body": json.dumps(body),  # Converte o corpo da resposta para uma string JSON
        "headers": {
            "Content-Type": "application/json"  # Define o tipo de conteúdo da resposta como JSON
        }
    }

    return response  # Retorna a resposta para ser enviada de volta ao solicitante

# Função 'v1_description' que retorna a descrição da API TTS
def v1_description(event, context):
    # Monta o corpo da resposta com a versão da API
    body = {
        "message": "TTS api version 1."  # Mensagem com a descrição da versão da API
    }

    # Cria a resposta HTTP com o status 200 (sucesso), o corpo em formato JSON, e o cabeçalho 'Content-Type' como 'application/json'
    response = {
        "statusCode": 200,  # Código de status HTTP para sucesso
        "body": json.dumps(body),  # Converte o corpo da resposta para uma string JSON
        "headers": {
            "Content-Type": "application/json"  # Define o tipo de conteúdo da resposta como JSON
        }
    }

    return response  # Retorna a resposta para ser enviada de volta ao solicitante
