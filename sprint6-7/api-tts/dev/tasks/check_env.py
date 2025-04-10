import os

def add_env_var(variables: dict):
    env_file = '.env'
    
    # Lê o conteúdo existente do .env
    if os.path.exists(env_file):
        with open(env_file, 'r') as file:
            lines = file.readlines()
    else:
        lines = []

    # Para cada variável na lista, verifica se já existe e, se não, adiciona
    for key, value in variables.items():
        if not any(line.startswith(f"{key}=") for line in lines):
            with open(env_file, 'a') as file:
                file.write(f'\n{key}="{value}"\n')

# Exemplo de uso:
# add_env_var({"BUCKET_NAME": "sprint-6-7-bucket", "AUDIO_S3_DIR": "aws_polly"})
