import boto3
import json
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
import os
from handler_faces import handler_faces  # Importando handler_faces

# carregando as credenciais
load_dotenv()

# variáveis para acesso
S3_BUCKET = "fotos-grupo5"  # Alterem para o nome do seu bucket S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")  # Sua Access Key ID da AWS
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")  # Sua Secret Key da AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")  # Região AWS, ou retorna a padrão

# Inicializar sessão boto3 com credenciais
session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)

rekognition = boto3.client("rekognition")
bedrock = boto3.client("bedrock-runtime")


def detect_labels(bucket, image_name):
    """Função para detectar rótulos no S3 usando Rekognition."""
    print(
        f"Detectando rótulos para a imagem '{image_name}' no bucket '{bucket}' usando Rekognition..."
    )
    response = rekognition.detect_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": image_name}},
        MaxLabels=20,
        MinConfidence=85,
    )
    print(f"Resposta do Rekognition detect_labels: {json.dumps(response)}")
    return response


def generate_pet_tips(labels):
    # Palavras-chave que não queremos no resultado final
    exclude_keywords = {
        "Animal",
        "Canine",
        "Mammal",
        "Pet",
        "Dog",
        "Puppy",
        "Cat",
        "Kitten",
    }

    # Filtra os rótulos da categoria "Animals and Pets"
    pet_labels = [
        {"Confidence": label["Confidence"], "Name": label["Name"]}
        for label in labels
        for category in label.get("Categories", [])
        if category["Name"] == "Animals and Pets"
    ]

    print(f"Rótulos detectados: {pet_labels}")

    # Filtra as raças que não estão em exclude_keywords
    other_pet_labels = [
        label["Name"] for label in pet_labels if label["Name"] not in exclude_keywords
    ]

    print(f"Rótulos filtrados: {other_pet_labels}")

    # Verifica se há raças para gerar as dicas
    if other_pet_labels:
        raca_nome = other_pet_labels[
            0
        ]  # Pegue a primeira raça identificada que não está nos keywords excluídos
        print(f"Raça identificada: {raca_nome}")

        prompt = f"""Eu gostaria de Dicas sobre {raca_nome}:
                    Nível de Energia e Necessidades de Exercícios:
                    Temperamento e Comportamento:
                    Cuidados e Necessidades:
                    Problemas de Saúde Comuns:
inclua obrigatoriamente no início de cada frase os títulos acima (Nível de Energia e Necessidades de Exercícios:
                    Temperamento e Comportamento:
                    Cuidados e Necessidades:
                    Problemas de Saúde Comuns:) e escreva as dicas em frente do título, só mude de linha no próximo titulo."""

        # Prepara a requisição no formato nativo do Bedrock
        native_request = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 500,  # Ajuste conforme necessário
                "temperature": 0.6,
                "topP": 0.9,
            },
        }

        print(f"Enviando prompt ao Bedrock: {prompt}")

        try:
            # Chama o Bedrock para gerar dicas
            response = bedrock.invoke_model(
                modelId="amazon.titan-text-express-v1",  # Substitua pelo ID do modelo que você está usando
                body=json.dumps(native_request),
            )

            # Decodifica a resposta
            model_response = json.loads(response["body"].read())
            print(f"Resposta do modelo Bedrock: {model_response}")
            bedrock_response = model_response["results"][0]["outputText"]

            print(f"Resposta do Bedrock formatada: {bedrock_response}")

            # Processa a resposta do Bedrock para remover números e hífens, e formatar adequadamente
            dicas_formatadas = ""
            current_section = ""
            sections = {
                "Nível de Energia e Necessidades de Exercícios": "",
                "Temperamento e Comportamento": "",
                "Cuidados e Necessidades": "",
                "Problemas de Saúde Comuns": "",
            }

            for line in bedrock_response.split("\n"):
                line = line.strip()
                if line.startswith(
                    ("1.", "2.", "3.", "4.")
                ):  # Remove os números das seções
                    line = line[line.find(" ") + 1 :].strip()
                if line.startswith("-"):
                    line = line[1:].strip()  # Remove o hífen do início da linha

                if line.startswith("Nível de Energia"):
                    current_section = "Nível de Energia e Necessidades de Exercícios"
                elif line.startswith("Temperamento"):
                    current_section = "Temperamento e Comportamento"
                elif line.startswith("Cuidados"):
                    current_section = "Cuidados e Necessidades"
                elif line.startswith("Problemas de Saúde"):
                    current_section = "Problemas de Saúde Comuns"
                else:
                    if current_section:
                        sections[current_section] += line + " "

            # Garante que cada seção tenha uma resposta válida
            for key in sections:
                if not sections[key].strip():
                    sections[key] = "Informação não disponível. "

            dicas_formatadas = ""
            for key, value in sections.items():
                dicas_formatadas += f"{key}: {value.strip()} "

            dicas_formatadas = dicas_formatadas.strip()
            print(f"Dicas formatadas: {dicas_formatadas}")

            return {
                "labels": pet_labels,
                "Dicas": f"Dicas sobre {raca_nome}: " + dicas_formatadas,
            }

        except (boto3.exceptions.Boto3Error, Exception) as e:
            print(f"ERROR: Can't invoke the Bedrock model. Reason: {e}")
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    elif other_pet_labels == []:
        return {
            "labels": pet_labels,
            "Dicas": f"Infelizmente nenhuma raça foi identificada!",
        }

    print("Nenhuma raça identificada.")
    return pet_labels


def handler_pets(event, context):
    print("Iniciando handler_pets...")
    body = json.loads(event["body"])
    bucket = body.get("bucket")
    image_name = body.get("imageName")
    print("Event recebido:", json.dumps(event))

    if not image_name:
        raise ValueError("O parâmetro 'imageName' está faltando ou está vazio.")

    # Chamando a função handler_faces para detectar rostos
    response_faces = handler_faces(
        {"body": json.dumps({"bucket": bucket, "imageName": image_name})}, context
    )
    faces = json.loads(response_faces["body"]).get("faces", [])
    print(f"Faces detectadas: {faces}")

    if not bucket or not image_name:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Faltando bucket ou imageName"}),
        }

    try:
        # Detectando pets usando Rekognition (labels)
        print(f"Chamando detect_labels para imagem '{image_name}'...")
        rekognition_label_response = detect_labels(bucket, image_name)
        print(f"Rekognition response: {rekognition_label_response}")
        labels = rekognition_label_response["Labels"]
        print(f"Labels detectados: {labels}")

        # Verificando se há pets e gerando dicas
        pet_analysis = generate_pet_tips(labels)
        if pet_analysis:
            fuso = timezone("America/Sao_Paulo")
            result = {
                "url_to_image": f"https://{bucket}.s3.amazonaws.com/{image_name}",
                "created_image": datetime.now(fuso).strftime("%d-%m-%Y %H:%M:%S"),
            }
            # Adiciona a chave "faces" somente se houverem rostos detectados válidos
            if len(faces) > 0 and any(
                face["classified_emotion"] is not None for face in faces
            ):
                result["faces"] = faces
            result["pets"] = [
                {"labels": pet_analysis["labels"], "Dicas": pet_analysis["Dicas"]}
            ]
            # Imprime a resposta no log do CloudWatch
            print(f"Resposta final: {json.dumps(result)}")

            return {"statusCode": 200, "body": json.dumps(result)}

        # Se não houver pets detectados
        print("Nenhum pet detectado.")
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Nenhum pet detectado"}),
        }

    except Exception as e:
        print(f"Erro ao processar a imagem: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Falha ao processar a imagem"}),
        }
