#  API Emotions and Pets - Detecção de Pessoas e suas emoções e Animais de Estimação

## **Desenvolvedores**
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/64118446?v=4" width="115" alt="Gerson Lopes Ramos Junior">](https://github.com/gersonlramos) <br>[Gerson Lopes Ramos Junior](https://github.com/gersonlramos) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/114765722?v=4" width="115" alt="Silvio Cabral de Melo">](https://github.com/SilvioCMJ) <br>[Silvio Cabral de Melo](https://github.com/SilvioCMJ) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/173846137?v=4" width="115" alt="Jefferson Luis Carneiro">](https://github.com/j3ffcarneiro) <br>[Jefferson Luis Carneiro](https://github.com/j3ffcarneiro) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/75399115?v=4" width="115" alt="Victor Iuri Costa Sousa">](https://github.com/souiuri) <br>[Victor Iuri Costa Sousa](https://github.com/souiuri) |
|:---:|:---:|:---:|:---:|
  
## Índice

- [Status do Projeto](#status-do-projeto)
- [Funcionalidades](#funcionalidades)
- [Arquitetura e Fluxo de Trabalho](#arquitetura-e-fluxo-de-trabalho)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Como Rodar a Aplicação](#como-rodar-a-aplicação)
- [Deploy](#deploy)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Estrutura de Diretórios](#estrutura-de-diretórios)
- [Padrões Utilizados](#padrões-utilizados)
- [Metodologia de Desenvolvimento](#metodologia-de-desenvolvimento)
- [Principais Dificuldades](#principais-dificuldades)
- [Licença](#licença)

---

## Status do Projeto

**Status**: Finalizado! 🎯

Este projeto visa desenvolver uma **API de Visão Computacional**, utilizando serviços da **AWS** para analisar emoções em imagens e identificar cães pastores. As principais tecnologias envolvem o **Amazon Rekognition** para análise de imagens e o **Amazon Bedrock**.

---

## Funcionalidades

1. **Análise de Emoções em Imagens**:
   - A API recebe o nome de uma imagem e verifica, através do **Amazon Rekognition**, as emoções predominantes detectadas nas faces presentes.

2. **Detecção de Pets e Geração de Dicas**:
   - A API também permite a identificação de pets na imagem e utiliza o **Amazon Bedrock** para gerar dicas sobre cuidados com o animal detectado, incluindo identificação de cães pastores.

3. **Monitoramento via CloudWatch**:
   - A API utiliza o **Amazon CloudWatch** para monitorar o uso, erros e logs.

---

## Arquitetura e Fluxo de Trabalho

A arquitetura do projeto envolve os seguintes componentes:

1. **API Vision**:
   Exemplo de requisição POST para a rota `/v1/vision`:
   ```json
   {
     "bucket": "myphotos",
     "imageName": "test-happy.jpg"
   }
   ```

   Exemplo de resposta:
   ```json
   {
    "url_to_image": "https://fotos-grupo5.s3.amazonaws.com/14-happypeople.jpg",
    "created_image": "12-10-2024 10:04:05",
    "faces": [
        {
            "position": {
                "Height": 0.2513464689254761,
                "Left": 0.32775333523750305,
                "Top": 0.20308414101600647,
                "Width": 0.2893712520599365
            },
            "classified_emotion": "HAPPY",
            "classified_emotion_confidence": 99.67448425292969
        }
    ]
   }
   ```

2. **Detecção de Pets e Dicas (v2)**:
   Exemplo de requisição POST para a rota `/v2/vision`:
   ```json
   {
     "bucket": "myphotos",
     "imageName": "poodle.jpg"
   }
   ```

   Exemplo de resposta:
   ```json
   {
    "url_to_image": "https://fotos-grupo5.s3.amazonaws.com/05-poodle.jpg",
    "created_image": "12-10-2024 10:09:56",
    "pets": [
        {
            "labels": [
                {
                    "Confidence": 99.70863342285156,
                    "Name": "Animal"
                },
                {
                    "Confidence": 99.70863342285156,
                    "Name": "Canine"
                },
                {
                    "Confidence": 99.70863342285156,
                    "Name": "Dog"
                },
                {
                    "Confidence": 99.70863342285156,
                    "Name": "Mammal"
                },
                {
                    "Confidence": 99.70863342285156,
                    "Name": "Pet"
                },
                {
                    "Confidence": 99.70863342285156,
                    "Name": "Puppy"
                },
                {
                    "Confidence": 92.27133178710938,
                    "Name": "Poodle"
                }
            ],
            "Dicas": "Dicas sobre Poodle: Nível de Energia e Necessidades de Exercícios: O poodle é um cachorro bastante ativo e inteligente, portanto, necessita de exercícios regulares para manter sua saúde física e mental. Os poodles são conhecidos por sua alta energia e necessidade de exercícios..."
        }
    ]
   }
   ```

---

## Variáveis de Ambiente
As variáveis de ambiente necessárias para a execução incluem as credenciais da **AWS** (chave de acesso e chave secreta) e detalhes dos serviços configurados, como o **Amazon Rekognition** e **Bedrock**.

---

## Como Rodar a Aplicação

### Pré-requisitos:
- **Serverless Framework** instalado.
- **Credenciais AWS** configuradas corretamente.

### Passos:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/seu-projeto.git
   ```

2. **Criar o ambiente de desenvolvimento**:

   **Windows**:
   ```bash
   python -m venv vision-env
   .\vision-env\Scripts\activate.bat
   ```

   **Linux**:
   ```bash
   python -m venv env
   source env/bin/activate
   ```

3. **Instale o Serverless Framework**:
   ```bash
   npm install -g serverless
   ```

4. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar as variáveis de ambiente**:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   ```

6. **Execute o deploy da aplicação**:
   ```bash
   serverless deploy
   ```

7. **Verifique os endpoints gerados** e utilize as rotas `/v1/vision` e `/v2/vision` para realizar as análises.

8. **Teste a API localmente**:
   ```bash
   serverless invoke local --function v1Description
   ```

---

## Deploy
O deploy é realizado via **Serverless Framework**, que configura e gerencia os serviços AWS necessários. Isso irá criar a API no **API Gateway**, as funções no **Lambda** e configurar os buckets no **S3**.

---

## Tecnologias Utilizadas
- **Amazon Rekognition**: Serviço de análise de imagens.
- **Amazon Bedrock**: Geração de respostas baseadas na presença de pets.
- **Amazon S3**: Armazenamento de imagens.
- **Amazon CloudWatch**: Monitoramento e logs da API.
- **Python 3.9**: Linguagem utilizada no desenvolvimento da aplicação.
- **Serverless Framework**: Orquestra o deploy dos serviços serverless.
- **Git**: Sistema de controle de versão para rastrear alterações e facilitar a colaboração.

---
<div align="center">

![Amazon Rekognition](https://img.shields.io/badge/Amazon%20Rekognition-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon Bedrock](https://img.shields.io/badge/Amazon%20Bedrock-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=for-the-badge&logo=amazonaws&logoColor=white)
![Amazon CloudWatch](https://img.shields.io/badge/Amazon%20CloudWatch-FF4F8B?style=for-the-badge&logo=amazonaws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Serverless](https://img.shields.io/badge/Serverless-FD5750?style=for-the-badge&logo=serverless&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

</div>

---

## Estrutura de Diretórios
```bash
SPRINT-8-pb-aws-junho/
├── assets/                          # Recursos como imagens e arquivos estáticos
│   ├── images-bucket/              # Imagens utilizadas na bucket
│   └── arquitetura-base.jpg        # Imagem da infraestrutura do Projeto
├── visao-computacional             # Diretório da API de Visão Computacional
│   ├── .serverless/                # Coleções Postman para testes
│   ├── node modules/               # Dependências do node
│   ├── utils/
|   |   └── testar_inferencia.py    # Manipuladores de requisições da API
│   ├── handler_faces.py            # API de identificação de emoções de rostos presentes na imagem
│   ├── handler_pets.py             # API de identificação de Pets
│   ├── handler.py                  # Teste do retorno da API
│   ├── package-lock.json           # Arquivo de controle de dependências
│   ├── package.json                # Metadados e dependências do projeto
│   ├── requirements.txt            # Dependências Python para o projeto
│   └── serverless.yml              # Arquivo de configuração Serverless
├── .gitignore                      # Arquivo para ignorar arquivos/diretórios no controle de versão Git.
├── serverless.yml                  # Configuração do Serverless Framework para deploy de funções serverless
└── README.md                       # Documentação principal do projeto
```

---

## Padrões Utilizados
- **Commits Semânticos**: Para manter um histórico claro e organizado.
- **RESTFul API**: Para comunicação entre os serviços.
- **Arquitetura Serverless**: Toda a aplicação utiliza serviços gerenciados pela AWS.
- **Python PEP8**: Segue os padrões de formatação de código Python.

---

## Metodologia de Desenvolvimento
O desenvolvimento seguiu a metodologia **Ágil**, com as seguintes práticas:

1. **Sprints**: Ciclos de desenvolvimento com metas definidas.
2. **Daily Meetings**: Reuniões diárias para acompanhamento de progresso.
3. **Code Review**: Revisões de código regulares para garantir qualidade e coesão.

---

## Principais Dificuldades
- Configuração de permissões para os serviços AWS.
- Integração dos logs do **CloudWatch** de forma eficiente.
- Ajuste da precisão do **Rekognition** para detecção de pets e emoções.

---

## Licença
Este projeto está licenciado sob a licença MIT.