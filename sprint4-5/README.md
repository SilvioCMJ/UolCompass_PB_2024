# Inference Service

## Descrição do Projeto
A aplicação consiste em uma API que disponibiliza um endpoint que recebe dados enviados por método POST e realiza inferência através de um modelo de ML treinado, retornando o resultado.

## Swagger
<img alt="InferenceDocs" title="#InferenceDocs" src="./assets/img/InferenceDocs.png">

Acesse http://174.129.226.5/docs#/inference/post_inference_post em seu navegador preferido para postar os dados diretamente do Swagger.

Ou faça uma requisição POST para o endpoint http://174.129.226.5/api/v1/inference utilizando `Postman` ou outro API consumer de sua escolha. Veja as collections disponíveis em `dev/collections/`.

## Tecnologias
<div align="center" style="display: inline_block;">
 <img align="center" alt="Python" height="65" width="65" src="https://devicon-website.vercel.app/api/python/original.svg"></img>
 <img align="center" alt="FastApi" height="53" width="60" src="https://devicon-website.vercel.app/api/fastapi/original.svg"></img>
 <img align="center" alt="Pydantic" height="53" width="53" src="https://docs.pydantic.dev/latest/logo-white.svg">
 <img align="center" alt="SQLA" height="130" width="100" src="https://devicon-website.vercel.app/api/sqlalchemy/plain.svg?color=%23C73A3A"></img>
 <img align="center" alt="Docker" height="63" width="70" src="https://devicon-website.vercel.app/api/docker/plain-wordmark.svg"></img>
 <img align="center" alt="Pandas" height="63" width="70" src="https://devicon-website.vercel.app/api/pandas/original.svg"></img>
 <img align="center" alt="Joblib" height="63" width="70" src="https://joblib.readthedocs.io/en/stable/_static/joblib_logo.svg"></img>
 <img align="center" alt="Sklearn" height="100" width="90" src="https://icon.icepanel.io/Technology/svg/scikit-learn.svg"></img>
 <img align="center" alt="Numpy" height="58" width="57" src="https://icon.icepanel.io/Technology/svg/NumPy.svg"></img>
 <img align="center" alt="Sagemaker" height="63" width="60" src="https://cloud-icons.onemodel.app/aws/Resource-Icons_01312023/Res_Machine-Learning/Res_48_Light/Res_Amazon-SageMaker_Model_48_Light.svg"></img>
 <img align="center" alt="S3" height="60" width="52" src="https://static-00.iconduck.com/assets.00/aws-s3-simple-storage-service-icon-423x512-sofvbo3x.png"></img>
 <img align="center" alt="EC2" height="63" width="55" src="https://www.svgrepo.com/show/448268/aws-ec2.svg"></img>
 <img align="center" alt="RDS" height="63" width="55" src="https://www.svgrepo.com/show/353458/aws-rds.svg"></img>

</div>

## Execução
Primeiro, clone o repositório usando:
``` shell
git clone https://github.com/Compass-pb-aws-2024-JUNHO/sprints-4-5-pb-aws-junho.git

```
Ou (se tiver ssh configurado)
``` shell
git clone git@github.com:Compass-pb-aws-2024-JUNHO/sprints-4-5-pb-aws-junho.git

```

Mude para a branch grupo-3 usando: `git switch grupo-3`

### Ambiente de desenvolvimento
Para instalar e gerenciar as depências adequadamente você precisará configurar um ambiente virtual utilizando venv:

    Windows:
        criação: python -m venv inference
        ativação: .\inference\Scripts\activate.bat

    Linux:
        instalar python venv: sudo apt install python3-venv
        criação: python -m venv inference
        ativação: source inference/bin/activate


Execute no terminal para instalar as dependências:
``` shell
pip install -r requirements.txt
```

Crie um arquivo `.env` e insira as credenciais de `local.env` substituindo o valor das variáveis com prefixo `AWS_` por suas próprias crendenciais.

O bucket S3 foi mantido público durante o desenvolvimento da aplicação. Caso deseje ter acesso ao modelo armazendo no Bucket envie uma solicitação para inferenceprojectmodelaccess@gmail.com no seguinte esquema:
- Assunto: Acesso ao Bucket S3
- Corpo: Nome completo - E-mail compass corporativo

Para o desenvolvimento local deve-se utilizar o ModelHandler de desenvolvimento definido em `dev/ml/main.py`, faça isso substituindo o import no arquivo `app/presentation/views/inference.py`, de `app` para `dev`, conforme a instrução abaixo:

    app - from app.ml.main import ModelHandler
    dev - from dev.ml.main import ModelHandler


### Sem Contêiner.
Para subir a API, execute:
``` shell
task run
```


### Em Contêiner (Docker)
Caso não tenha o [Docker](https://www.docker.com/) instalado, siga a documentação oficial na plataforma.

Para construir a imagem da aplicação, execute:
``` shell
docker build -t inference/inference-service:v1 .
```
Para executar o contêiner:
``` shell
docker run -d --name inference -p 3000:3000 inference/inference-service
```

E acesse http://localhost:3000/docs para utilizar o Swagger.

Ou utilize http://localhost:3000/api/v1/inference no `Postman` ou outro API consumer de sua escolha. Veja as collections disponíveis em `dev/collections/`.




## Estrutura de Diretórios
<img alt="DirectoryStructure" title="#DirectoryStructure" src="./assets/img/directory_structure.png">

## Executar testes

Para executar os testes, execute:

```bash
task test
```

Caso queira executar um teste específico, execute:

```bash
task test-matching "nome-do-teste"
```

## Desenvolvimento
Para organizar o desenvolvimento e manter o bom andamento do projeto, foi criado um quadro no Trello com as etapas necessárias a serem seguidas.

Quando surgia um problema que poderia comprometer o andamento das tarefas delegadas a cada membro da equipe, o procedimento era alocar mais membros da equipe e instruí-los a ajudar na solução do problema de forma mais eficiente.

### Dificuldades
- Interconexão entre serviços AWS, por motivos de permissões negadas.
- Encontrar os melhores parâmetros para cada modelo de IA testado.
- Mapeamento das portas na instância EC2.
- Treinamento externo do modelo utilizando o Sagemaker SDK.

## Desenvolvedores
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/97261564?v=4" width=115><br><sub>Gustavo Felipe da Costa Silva</sub>](https://github.com/gusttavofelipe) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/130758430?v=4" width=115><br><sub>Hugo Bessa Susini Ribeiro</sub>](https://github.com/hsusini) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/167718668?v=4" width=115><br><sub>Jean Carlos Penha da Conceição</sub>](https://github.com/JeanPTBR) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/114765722?v=4" width=115><br><sub>Silvio Cabral de Melo Junior</sub>](https://github.com/SilvioCMJ)
| :---: | :---: | :---: | :---: |
