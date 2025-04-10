import boto3
import json
from pytz import timezone
from datetime import datetime
from dotenv import load_dotenv
import os

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
s3 = boto3.client("s3")

def detect_emotions(bucket, image_name):
    """função que escreve a syntax para arquivos alocados no S3"""
    response = rekognition.detect_faces(
        Image={"S3Object": {"Bucket": bucket, "Name": image_name}}, Attributes=["ALL"]
    )
    return response

def handler_faces(event, context):
    print("Event received:", json.dumps(event))

    # transformando de string JSON para dicionário Python
    body = json.loads(event["body"])

    bucket = body.get("bucket")  # Pega o bucket enviado no JSON
    image_name = body.get("imageName")  # Pega o nome da imagem enviado no JSON

    if not image_name:
        raise ValueError("The 'imageName' parameter is missing or empty.")

    response = detect_emotions(bucket, image_name)
    print("Rekognition response:", json.dumps(response))

    faces = []
    for face in response["FaceDetails"]:
        position = face["BoundingBox"]
        emotion = max(face["Emotions"], key=lambda e: e["Confidence"])
        faces.append(
            {
                "position": {
                    "Height": position["Height"],
                    "Left": position["Left"],
                    "Top": position["Top"],
                    "Width": position["Width"],
                },
                "classified_emotion": emotion["Type"],
                "classified_emotion_confidence": emotion["Confidence"],
            }
        )
    fuso = timezone("America/Sao_Paulo")
    result = {
        "url_to_image": f"https://{bucket}.s3.amazonaws.com/{image_name}",
        "created_image": datetime.now(fuso).strftime("%d-%m-%Y %H:%M:%S"),
        "faces": faces
        or [
            {
                "position": {"Height": None, "Left": None, "Top": None, "Width": None},
                "classified_emotion": None,
                "classified_emotion_confidence": None,
            }
        ],
    }

    # Registra o resultado (body) no CloudWatch
    print(f"Resultado (body): {json.dumps(result)}")

    return {"statusCode": 200, "body": json.dumps(result)}