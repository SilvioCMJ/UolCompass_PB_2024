# Avaliação Sprints 6 e 7 - Programa de Bolsas Compass UOL e AWS - turma junho/2024

Avaliação das sexta e sétima sprints do programa de bolsas Compass UOL para formação em machine learning para AWS.

## Execução (Código Fonte)

Crie uma API que irá capturar uma frase qualquer inserida pelo usuário e transformará essa frase em um audio em mp3 via polly. Após, crie um chatbot que se utilize da API criada.

**Especificações**:

A aplicação deverá ser desenvolvida com o framework 'serverless' e deverá seguir a estrutura que já foi desenvolvida neste repo.

Passo a passo para iniciar o projeto:

1. Crie a branch para o seu grupo e efetue o clone

2. Instale o framework serverless em seu computador. Mais informações [aqui](https://www.serverless.com/framework/docs/getting-started)

```json
npm install -g serverless
```

3. Gere suas credenciais (AWS Acess Key e AWS Secret) na console AWS pelo IAM. Mais informações [aqui](https://www.serverless.com/framework/docs/providers/aws/guide/credentials/)

4. Em seguida insira as credenciais e execute o comando conforme exemplo:

```json
serverless config credentials \
  --provider aws \
  --key AKIAIOSFODNN7EXAMPLE \
  --secret wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
  ```

Também é possivel configurar via [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) executando o comando:

```json
$ aws configure
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: us-east-1
Default output format [None]: ENTER
  ```

#### Observação

As credenciais devem ficar apenas localmente no seu ambiente. Nunca exponha as crendenciais no Readme ou qualquer outro ponto do código.

Após executar as instruções acima, o serverless estará pronto para ser utilizado e poderemos publicar a solução na AWS.

5. Para efetuar o deploy da solução na sua conta aws execute (acesse a pasta `api-tts`):

```
serverless deploy
```

Depois de efetuar o deploy, teremos um retorno semelhante a este:

```bash
Deploying api-tts to stage dev (us-east-1)

Service deployed to stack api-tts-dev (85s)

endpoints:
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/v1
functions:
  health: api-tts-dev-health (2.1 kB)
  v1Description: api-tts-dev-v1Description (2.1 kB)
  v2Description: api-tts-dev-v2Description (2.1 kB)
```

6. Abra o browser e confirme que a solução está funcionando colando os 3 endpoints que deixamos como exemplo:

### Rota 1 → Get /

1. Esta rota já está presente no projeto.
2. O retorno rota é:

```json
  {
    "message": "Go Serverless v3.0! Your function executed successfully!",
    "input": { 
        ...(event)
      }
  }
```

3. Status code para sucesso da requisição será `200`.

### Rota 2 → Get /v1

1. Esta rota já está presente no projeto.
2. O retorno rota é:

```json
  {
    "message": "TTS api version 1."
  }
 
```

3. Status code para sucesso da requisição será `200`.


***

Após conseguir rodar o projeto base o objetivo final será divida em duas partes:

## Atividade -> Parte 1

### Rota 3 -> Post /v1/tts

Deverá ser criada a rota `/v1/tts` que receberá um post no formato abaixo:

```json
  {
    "phrase": "converta esse texto para áudio e salve uma referencia no dynamoDB. Caso a referencia já exista me devolva a URL com audio já gerado"
  }
```

- Deverá ser criada uma lógica para que a frase recebida seja um id único (um _hash code_);
- Esse hash será o atributo chave em nosso DynamoDB - exemplo: "Teste 123" será sempre o id "123456";
- O texto da frase recebida deverá ser transformado em áudio via AWS Polly;
- O áudio deverá ser armazenado em um bucket S3 (que deverá ser público, apenas para a nossa avaliação);
- Deverá utilizar a lógica de _hash code_ para verificar se a frase já foi gerada anteriormente;
- Caso o hash (_unique_id_) já exista no DynamoDB entregue o retorno conforme abaixo;
- Caso não exista, faça a geração do áudio, grave no s3 e grave as referências no dynamoDB.

Resposta a ser entregue:

```json
  {
    "received_phrase": "converta esse texto para áudio",
    "url_to_audio": "https://meu-buckect/audio-xyz.mp3",
    "created_audio": "02-02-2023 17:00:00",
    "unique_id": "123456"
  }
```

Exemplos de referência:

- <https://github.com/hussainanjar/polly-lambda> (Python)
- <https://github.com/serverless/examples/tree/v3/aws-python-http-api-with-dynamodb> (Python)

***

## Atividade -> Parte 2

Com base na [Documentação Amazon Lex](https://compasso-my.sharepoint.com/:f:/g/personal/lucas_sousa_compasso_com_br/Eph8d9BDeRhGhBzyoAYRLZUBhfjA54P1-5YHERGaN5_Osg?e=1ibFDI), crie um chatbot utilizando o Amazon Lex V2 e o conecte a uma plataforma de mensageria.

**Especificações**:

- Função do chatbot é de livre escolha do desenvolvedor;
- Conexões: O chatbot deve ser disponibilizado em uma das seguintes plataformas:  
  - Slack - [Conexão Slack](https://docs.aws.amazon.com/pt_br/lex/latest/dg/slack-bot-association.html);  
  - Web - [Web](https://github.com/aws-samples/aws-lex-web-ui);
- Construção:
  - Intents:
    - O chatbot deve possuir ao menos 4 intents distintas;  
  - Slots:
    - Captação de informações presentes no texto;
    - Solicitação de informações quando o slot não for reconhecido;
    - Confirmação de informações;
    - O chatbot deve captar ao menos 3 slots no decorrer do fluxo;
- O chatbot deve utilizar-se de menu com botões (Response Cards);
- Tratamento de erros (fallback);
- Deve ter a opção de enviar a resposta em áudio, utilizando o texto de resposta do chatbot, com uso da API da Parte 1 deste trabalho;
- (Opcional) Uso de conditional branching para controle de fluxos ([Doc Conditional Branching](https://docs.aws.amazon.com/pt_br/lexv2/latest/dg/paths-branching.html));

Ao final, a arquitetura a ser implantada deverá estar assim:

![post-v3-tts](./assets/sprints6-7.jpg)

***

## O que será avaliado?

- Projeto em produção na AWS;
- Em python conforme projeto base disponibilizado;
- Infra-estrutura como codigo;
- Seguir as atividades na ordem proposta;
- Sobre as rotas:
  - Possuir a rota com o retorno esperado (somente campos solicitados conforme especificação);
- Entendimento do chatbot e o que ele soluciona;
- Criatividade em relação ao tema escolhido para o desenvolvimento do chatbot;
- Intents e slots criados e informações que eles se dispõem a obter;
- Organização:  
  - Estrutura de intenções;  
  - Estrutura da lógica de negócio;  
  - Divisão de responsabilidades da equipe;  
  - Funcionalidade do chatbot;
- Objetividade do README.md.

***

## Entrega

- **O trabalho deve ser feito em grupos de três ou quatro pessoas**;
  - Evitar repetições de grupos da sprint anterior;
- Criar uma branch no repositório com o formato grupo-número (Exemplo: grupo-1);
- Subir o trabalho na branch com um Readme.md:
  - Documentar detalhes sobre como a avaliação foi desenvolvida;
  - Dificuldades conhecidas;
  - Como utilizar o sistema;
  - **Export do bot Lex em formato .zip**;
- 🔨 código fonte desenvolvido (observar estruturas de pastas);
- O prazo de entrega é até às 14h do dia 30/09/2024 no repositório do github (https://github.com/Compass-pb-aws-2024-JUNHO/sprints-6-7-pb-aws-junho).
