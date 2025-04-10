# **API-TTS - HELP DESK**

## **👥 Desenvolvedores**
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/167718668?v=4" width="115" alt="Jean Carlos Penha da Conceição">](https://github.com/JeanPTBR) <br>[Jean Carlos Penha da Conceição](https://github.com/JeanPTBR) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/114765722?v=4" width="115" alt="Silvio Cabral de Melo">](https://github.com/SilvioCMJ) <br>[Silvio Cabral de Melo](https://github.com/SilvioCMJ) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/167145673?v=4" width="115" alt="Roger Santos Vargas">](https://github.com/Rogerdev02) <br>[Roger Santos Vargas](https://github.com/Rogerdev02) | [<img loading="lazy" src="https://avatars.githubusercontent.com/u/95103547?v=4" width="115" alt="Monique da Silva Borges">](https://github.com/niqueborges) <br>[Monique da Silva Borges](https://github.com/niqueborges) |
|:---:|:---:|:---:|:---:|


---




## **📑 Índice**
- [📈 Status do Projeto](#-status-do-projeto)
- [✨ Funcionalidades](#-funcionalidades)
- [⚙️ Arquitetura e Fluxo de Trabalho](#-arquitetura-e-fluxo-de-trabalho)
- [🤖 Chatbot Help Desk - Detalhes](#-chatbot-help-desk---detalhes)
- [🗃️ Banco de Dados](#-banco-de-dados)
- [⚙️ Variáveis de Ambiente](#-variáveis-de-ambiente)
- [📦 Como Rodar a Aplicação](#-como-rodar-a-aplicação)
- [🚀 Deploy](#-deploy)
- [💻 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📂 Estrutura de Diretórios](#-estrutura-de-diretórios)
- [📐 Padrões Utilizados](#-padrões-utilizados)
- [📅 Metodologia de Desenvolvimento](#-metodologia-de-desenvolvimento)
- [😿 Principais Dificuldades](#-principais-dificuldades)
- [📝 Licença](#-licença)

---


## **📈 Status do Projeto**
🚀 **Status**: Finalizado

Este projeto tem como objetivo desenvolver uma **API de Text-to-Speech (TTS)** usando o **Amazon Polly** para converter textos em áudio, armazenar os arquivos no **S3**, e usar o **DynamoDB** para gerenciar os metadados. Além disso, há uma integração com o **Amazon Lex v2** e o **Slack**, onde um chatbot chamado **Help Desk** captura e processa as mensagens dos usuários, retornando respostas em áudio relacionadas a **problemas de hardware de Notebooks e Desktops**.

---

## **✨ Funcionalidades**
1. **Conversão de Texto para Áudio**:
   - A API recebe uma frase via POST, gera um hash único para a frase e verifica no DynamoDB se o áudio já foi criado. Caso contrário, o Polly gera o áudio, que é armazenado no S3.
   
2. **Integração com Chatbot Amazon Lex e Slack**:
   - O chatbot **Help Desk**, integrado ao Lex v2, permite que usuários no Slack enviem perguntas sobre hardware de **Notebooks** e **Desktops**. O bot processa as intenções (intents), captura parâmetros relevantes (slots) e fornece respostas por meio de **cards** com texto e áudio, retornados pela API TTS.

3. **Persistência de Dados**:
   - As frases e metadados são armazenados no **DynamoDB**, enquanto os arquivos de áudio são salvos no **S3**.
---



## **⚙️ Arquitetura e Fluxo de Trabalho**
A arquitetura do projeto envolve os seguintes componentes:

1. **API de TTS**:
Exemplo de requisição POST:
   ```json
   {
     "phrase": "Por favor, converta este texto para áudio"
   }
   ```

   Exemplo de resposta:
   ```json
   {
     "received_phrase": "Por favor, converta este texto para áudio",
     "url_to_audio": "https://meu-bucket-s3/audio-xyz.mp3",
     "created_audio": "2023-09-20 17:00:00",
     "unique_id": "hash-da-frase"
   }
   ```
---

## **🤖 Chatbot Help Desk - Detalhes**
O chatbot **Help Desk** foi projetado para interagir com usuários que enfrentam problemas relacionados ao hardware de Notebooks e Desktops. Ele fornece respostas detalhadas em texto e áudio, ajudando os usuários a identificar e resolver questões comuns.

- Para utilizar o nosso chatbot utilize esse link para entrar no Workspace do Slack e selecione o **DeskBotFinal** dentro de **Apps**:
   https://join.slack.com/t/compassuolsede/shared_invite/zt-2r678ikhe-zOvQVfLK0CzbX~BFRurEQg

Abaixo estão as principais características do chatbot:

### **Intents** (Intenções):
1. **Saudação**:
   - **Exemplo de interação**: "Oi, estou com problemas no dispositivo."
   - **Resposta**: "Olá! Eu sou o HelpDesk bot, seu assistente técnico de hardware. Descreva o problema que você está enfrentando, e vou te ajudar a solucioná-lo!"

2. **Problema de Tela preta**:
   - **Exemplo de interação**: "Meu computador está com problema de tela preta. Como posso resolver?"
   - **Resposta**: "Verifique a conexão do monitor: Certifique-se de que o cabo do monitor está bem conectado à placa de vídeo ou à saída de vídeo da placa-mãe."

3. **Problema de superaquecimento**:
   - **Exemplo de interação**: "Meu computador está esquentando muito. O que posso fazer?"
   - **Resposta**: "Limpeza interna: Abra o dispositivo e limpe a poeira dos ventiladores, dissipadores de calor e componentes com ar comprimido. Poeira acumulada pode obstruir o fluxo de ar."

4. **Dispositivo não liga**:
   - **Exemplo de interação**: "Meu computador não liga. O que pode estar errado?"
   - **Resposta**: "Verifique a alimentação: Certifique-se de que o cabo de energia está conectado corretamente e que a tomada está funcionando."

5. **Problema de desempenho lento**:
   - **Exemplo de interação**: "Meu computador está lento. Como solucionar?"
   - **Resposta**: "Verifique o armazenamento: Certifique-se de que o disco rígido (HD ou SSD) não está cheio. Unidades muito cheias podem reduzir o desempenho. Considere usar um SSD se estiver usando um HD."

6. **Dispositivo reiniciando**:
   - **Exemplo de interação**: "Meu computador está reiniciando. Como resolver?"
   - **Resposta**: "Memória RAM: Retire e reinsira os módulos de RAM. Teste um de cada vez em diferentes slots. Use ferramentas como MemTest86 para verificar erros de RAM."
  

### **Slots** (Parâmetros):
- **Dispositivos_Slot**: Identifica o dispositivo do usuário.
- **HardwareProblems**: Captura o tipo de problema do usuário.
- **SimNão**: Captura a resposta do usuário caso exista outros problemas.

### **Cards**:
- Para cada resposta fornecida, o chatbot retorna um **card** visual com:
   - **Tela preta**
   - **Superaquecimento** 
   - **Dispositivo não liga**
   - **Desempenho lento**
   - **Dispositivo reiniciando**
  
   **Exemplo de estrutura de card:**
   ```
   {
     {"text": "Tela preta", "value": "problema_tela_preta"},
     {"text": "Super Aquecimento", "value": "problema_superaquecimento"},
     {"text": f"{dispositivo} Não liga", "value": "problema_nao_liga"},
     {"text": "Desempenho Lento", "value": "problema_desempenho_lento"},
     {"text": f"{dispositivo} Reiniciando", "value": "problema_reiniciando"}
   }
   ```


---

## **🗃️ Banco de Dados**
O projeto usa dois principais serviços de armazenamento:

- **DynamoDB**: Armazena o hash das frases e as URLs dos arquivos no S3. Estrutura de exemplo:
  - `unique_id`: Hash gerado a partir da frase.
  - `phrase`: A frase original.
  - `audio_url`: URL do áudio no S3.
  - `timestamp`: Data de criação.

- **S3**: Armazena os arquivos de áudio gerados pelo Polly.

---

## **⚙️ Variáveis de Ambiente**
As variáveis de desenvolvimento são configuradas automaticamente ao executar a API.

---

## **📦 Como Rodar a Aplicação**

### **Pré-requisitos**:
- **Serverless Framework** instalado.
- Credenciais AWS configuradas corretamente.

### **Passos**:

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-6-7-pb-aws-junho.git
   ```
2. **Criar o ambiente de desenvolvimento**:

   Windows
   ```bash
   criação: python -m venv inference
   ativação: .\inference\Scripts\activate.bat
   ```
   Linux
   ```bash
   instalar python venv: sudo apt install python3-venv
   criação: python -m venv inference
   ativação: source inference/bin/activate     
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
   task config
   ```

6. **Execute o deploy da aplicação**:
   ```bash
   task deploy
   ```

7. **Verifique os endpoints gerados** e utilize a rota `/v1/tts` para transformar texto em áudio.

8. **Teste a API localmente**:
   ```bash
   task run
   ```

---

## **🚀 Deploy**
O deploy é realizado via **Serverless Framework**, que configura e gerencia os serviços AWS necessários. Isso irá criar a API no **API Gateway**, as funções no **Lambda** e configurar os buckets no **S3** e as tabelas no **DynamoDB**.

- **Lambda** para a lógica de conversão.
- **API Gateway** para exposição das rotas.
- **Polly** para geração de áudio.
- **DynamoDB** e **S3** para armazenamento de dados e arquivos.

Para testar a rota do endpoint utilizado no chatbot:
https://rmbshe6lg3.execute-api.us-east-1.amazonaws.com/v1/tts

---


## **💻 Tecnologias Utilizadas**
- **Amazon Polly**: Serviço de conversão de texto para fala.
- **Amazon Lambda**: Executa código em resposta a eventos sem necessidade de gerenciar servidores.
- **Amazon S3**: Armazenamento escalável e durável dos arquivos de áudio.
- **Amazon DynamoDB**: Banco de dados NoSQL utilizado para armazenar metadados.
- **Amazon Lex v2**: Processa linguagem natural para construir chatbots conversacionais.
- **Slack**: Interface de mensagens usada para interações do chatbot.
- **Python 3.9**: Linguagem utilizada no desenvolvimento da aplicação.
- **Serverless Framework**: Orquestra o deploy dos serviços serverless.
- **Git**: Sistema de controle de versão para rastrear alterações e facilitar a colaboração.

---


<div align="center">
      
![Amazon Polly](https://img.shields.io/badge/Amazon%20Polly-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Amazon S3](https://img.shields.io/badge/Amazon%20S3-569A31?style=flat-square&logo=amazonaws&logoColor=white)
![Amazon DynamoDB](https://img.shields.io/badge/Amazon%20DynamoDB-4053D6?style=flat-square&logo=amazonaws&logoColor=white)
![Amazon Lex](https://img.shields.io/badge/Amazon%20Lex-4B8BBE?style=flat-square&logo=amazonaws&logoColor=white)
![Slack](https://img.shields.io/badge/Slack-4A154B?style=flat-square&logo=slack&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Serverless Framework](https://img.shields.io/badge/Serverless%20Framework-23B17B?style=flat-square&logo=serverless&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![AWS Lambda](https://img.shields.io/badge/AWS%20Lambda-FF9900?style=flat-square&logo=amazonaws&logoColor=white)

</div>

---


```bash
SPRINT-6-7-DEV/
├── api-tts/                        # Diretório da API Text-to-Speech
│   ├── aws/                        # Serviços AWS utilizados pela API
│   │   ├── dynamodb/               # Interações com DynamoDB
│   │   ├── polly/                  # Interações com AWS Polly
│   │   └── s3/                     # Interações com S3
│   ├── dev/                        # Arquivos relacionados ao desenvolvimento
│   │   ├── collections/            # Coleções Postman para testes
│   │   └── tasks/                  # Scripts e utilidades para desenvolvimento
│   ├── handlers/                   # Manipuladores de requisições da API
│   ├── utils/                      # Utilidades e funções auxiliares
│   └── serverless.yml              # Arquivo de configuração Serverless
├── assets/                         # Recursos como imagens e arquivos estáticos
├── lex_chatbot/                    # Diretório relacionado ao chatbot Lex
│   ├── DeskBotFinal.zip            # Arquivo final do chatbot
│   └── lambda_function.py          # Função Lambda do chatbot
├── package.json                    # Configuração e dependências Node.js
├── pyproject.toml                  # Configuração do Poetry para dependências Python
├── requirements.txt                # Dependências Python para o projeto
├── README.md                       # Documentação principal do projeto
├── .env                            # Arquivo de variáveis de ambiente
└── .gitignore                      # Arquivo de configuração do Git
```
---

## **📐 Padrões Utilizados**
- **Commits Semânticos**: Para manter um histórico claro e organizado.
- **RESTFul API**: Para comunicação entre os serviços.
- **Arquitetura Serverless**: Toda a aplicação utiliza serviços gerenciados pela AWS.
- **Python PEP8**: Segue os padrões de formatação de código Python.

---

## **📅 Metodologia de Desenvolvimento**
O desenvolvimento seguiu a metodologia **Ágil**, com as seguintes práticas:

1. **Sprints**: Ciclos de desenvolvimento com metas definidas.
2. **Daily Meetings**: Reuniões diárias para acompanhamento de progresso.
3. **Code Review**: Revisões de código regulares para garantir qualidade e coesão.

---

## **😿 Principais Dificuldades**
1. **Integração com o Amazon Lex**: A configuração inicial do Lex e o mapeamento correto das intenções e slots apresentaram desafios, mas foram superados com pesquisa e testes contínuos.
2. **Erros de Permissão na AWS**: Configurações de IAM exigiram ajustes detalhados para garantir o acesso correto entre os serviços.
3. **Sincronização de Áudio e Texto**: Garantir que a resposta do chatbot no Slack estivesse sincronizada com o áudio gerado.
---

## **📝 Licença**

Este projeto está sob a Licença MIT. Veja o arquivo LICENSE para mais detalhes.


---


Este README foi estruturado conforme as melhores práticas recomendadas no Programa de Bolsas Compass UOL e AWS.


