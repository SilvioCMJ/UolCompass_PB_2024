import boto3
import json
from botocore.exceptions import ClientError
import importlib

add_env_var_module = importlib.import_module("api-tts.dev.tasks.check_env")
add_env_var = add_env_var_module.add_env_var

def create_bucket(bucket_name):
    s3 = boto3.client('s3')

    try:
        # Verifica se o bucket já existe
        s3.head_bucket(Bucket=bucket_name)
        print(f"Bucket {bucket_name} já existe.")
    except ClientError:
        try:
            # Cria o bucket
            s3.create_bucket(Bucket=bucket_name)
            print(f"Bucket {bucket_name} criado.")
            
            # Desabilita o bloqueio de ACLs públicas
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )
            
            # Define uma política de bucket para permitir acesso público
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    },
                    {
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:PutObject",
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    }
                ]
            }
            s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
            
        except ClientError as e:
            print(f"Erro ao criar o bucket: {e}")
            return False
        
    # Adicionar as informações ao .env
    add_env_var({
        "BUCKET_NAME": bucket_name, 
        "AUDIO_S3_DIR": "aws_polly"
    })

    return True

if __name__ == "__main__":
    bucket_name = "sprint-6-7-bucket"
    create_bucket(bucket_name)
