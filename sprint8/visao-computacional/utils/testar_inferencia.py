import requests

bucket = "fotos-grupo5" # Nome do seu bucket S3
key = "pessoa_triste.jpg" # Nome do arquivo que será salvo no S3

url = "https://v9ae6hopl6.execute-api.us-east-1.amazonaws.com/dev/v1/vision"
data = {
   "bucket": bucket,
   "imageName": key
}

response = requests.post(url, json=data)

print(response.json())