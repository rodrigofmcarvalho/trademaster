# Introdução

O projeto TradeMaster é uma solução de engenharia de dados concebida para otimizar a gestão de transações de uma loja de entretenimento que comercializa e aluga itens como livros, filmes e DVDs de séries. O sistema busca centralizar o controle de vendas e aluguéis, coletando dados relevantes dos clientes e funcionários, e gerenciando eficientemente os estoques das várias franquias da loja.

# Arquitetura da Solução

![Arquitetura da Solução](images/architecture.jpg)

- Os seguintes componentes foram implementados:
  -	API Gateway: Interface para receber transações e interagir com sistemas externos.
  -	Producer: Módulo responsável por publicar mensagens no sistema de mensageria.
  - Consumer: Componente que consome mensagens e executa o processamento de dados.
  - Data Store: Armazenamento persistente para manter o estado das transações processadas.

# Configuração do Ambiente (Ferramentas Utilizadas)

- Abaixo estão as ferramentas e tecnologias que foram escolhidas para este projeto, juntamente com suas versões específicas:
  - **Python 3.10.6:** Linguagem de programação usada para escrever os códigos.
  - **Minikube 1.31.2:** Ferramenta que permite a execução de um cluster Kubernetes localmente, simplificando testes e desenvolvimento.
  - **Strimzi 0.38.0**: Ferramenta usada para orquestrar e gerenciar clusters Apache Kafka no Kubernetes.
  - **Docker 24.0.7:** Plataforma de containerização usada para criar, implantar e executar aplicativos em containeres, garantindo que o ambiente seja isolado e consistente.
  - **Kubernetes 1.27.4:** Sistema de orquestração de contêineres para automatizar a implantação, dimensionamento e operações de aplicativos em contêineres.
  - **Helm 3.13.1:** Gerenciador de pacotes para Kubernetes, facilitando a instalação e gerenciamento de aplicativos.
  - **MinIO 8.0.10:** Solução de armazenamento de objetos de alto desempenho, compatível com a API do Amazon S3.
  - **PostgreSQL 15.3:** Sistemas de gerenciamento de banco de dados relacional usado para armazenar dados.
  - **Poetry 1.5.1:** Ferramenta de gerenciamento para Python, usada para gerenciar ambiente virtual, bibliotecas e pacotes necessários no projeto.
  - **DBeaver 3.2.3:** Ferramenta de administração de banco de dados com suporte ao PostgreSQL.
  - **VSCode 1.84.0:** Editor de código-fonte usado para o desenvolvimento do código de ETL e outras tarefas de codificação.
  - **Ubuntu 22.04.3 LTS 64-bit:** Sistema operacional em que o ambiente de desenvolvimento está configurado.
  - **VMware Workstation 17 Player: 17.5.0** Software de virtualização usado para criar e executar máquinas virtuais.
 
# Como Executar a Pipeline
1. **Iniciar o Minikube**:
   - Execute o Minikube para iniciar um cluster Kubernetes local com o comando:
     ```sh
     minikube start
     minikube tunnel
     ```
     
3. **Instalar o Strimzi Kafka Operator**:
   - Siga a documentação oficial do Strimzi para instalar a *release* no cluster Minikube para gerenciar e orquestrar os clusters Kafka.
     ```sh
     kubectl create namespace kafka
     helm repo update
     helm install my-strimzi strimzi/strimzi-kafka-operator -n kafka
     ```
4. ** Executar o cluster Kafka**:
   - Execute os manifestos para instanciar os containeres do cluster Kafka:
     ```sh
     kubectl apply -f namespace.yaml
     kubectl apply -f kafka.yaml
     kubectl apply -f kafkatopic.yaml
     ```

4. **Instalar o MinIO**:
   - Siga a documentação oficial do MinIO para instalar a *release* no cluster Minikube.
   - ```sh
     kubectl create namespace minio
     helm install minio minio/minio -n minio
     ```
   - Após a instalação, obtenha as chaves `ACCESS_KEY` e `SECRET_KEY` conforme orientado pela documentação.
     ```sh
     ACCESS_KEY=$(kubectl get secret minio -o jsonpath="{.data.accesskey}" | base64 --decode)
     SECRET_KEY=$(kubectl get secret minio -o jsonpath="{.data.secretkey}" | base64 --decode)
     ```
    - Configure um alias no cliente mc e encaminhar a porta para acessar o serviço MinIO localmente:
     ```sh
     mc alias set minio-local http://localhost:9000 "$ACCESS_KEY" "$SECRET_KEY" --api s3v4
     export POD_NAME=$(kubectl get pods --namespace minio -l "release=minio" -o jsonpath="{.items[0].metadata.name}")
     kubectl port-forward $POD_NAME 9000 --namespace minio
     ```
  
5. **Atualizar as Credenciais no Manifesto `deployments.yaml` da API**:
   - Revise o manifesto `deployments.yaml` da API e atualize as informações de acesso ao Kafka e ao MinIO com as novas credenciais e endereços. Atualize também o `PYTHONPATH` para que as importações dos módulos desenvolvidos funcionem corretamente.

6. **Construir a Imagem da API**:
   - Realize o build da imagem Docker da sua API apontando o daemon do Docker para o Minikube.
     ```sh
     eval $(minikube docker-env)
     docker build -t api -f api/dockerfile .
     ```

7. **Implantar o container da API**:
   - Execute os manifestos para instanciar o containeres da API.
     ```sh
     kubectl apply -f namespace.yaml
     kubectl apply -f manifest.yaml
     kubectl apply -f service.yaml
     ```

8. **Testar a API com um Evento Simulado**:
   - Simule um evento de teste para verificar se a API está processando as solicitações corretamente.
   - Utilize uma ferramenta de teste de API como `curl` ou Postman para enviar uma solicitação de teste à API.
   - Pode ser utilizada a biblioteca `Faker` para gerar dados fictícios.
   = Pode ser utilizado o `Kafka-UI` para visualização dos eventos nos tópicos.

## Respondendo as tarefas:

### Tarefa 1:
Mapear a estrutura de dados da loja, respeitando todas as necessidades listadas:
- O banco de dados origem será relacional;
- Imagine o cenário que uma aplicação irá possuir essa estrutura em um
banco Postgres e desejamos processar e manusear os dados para o GCP;
- Fica a critério do participante definir os detalhes dos campos, imagine que a
estrutura é para uma loja real;
- Crie uma documentação do resultado (clara suficiente para um usuário de
produtos entender a modelagem e detalhada o suficiente para um engenheiro de
software entender como a implementar).


### Tarefa 2:
Definição do evento:
- O dono da loja não possui conhecimento no ramo, mas ele deseja ter os dados
da venda/aluguel e seus dados relevantes para uma análise futura, seja do
negócio quanto dos clientes e seu time de funcionários. Sendo assim:
- Mapeie os dados a serem enviados no evento e o documente de forma simples,
para entendimento do time de produtos e técnico.

### Tarefa 3:
Publicação:
- Opcional o uso do Google Pub/Sub ou Kafka
- Google Pub/Sub - Configure o projeto para uso do Google Pub/Sub,
iremos testar o processo via Pub/Sub emulator
(https://cloud.google.com/pubsub/docs/emulator)
- Kafka - Pontos extras se a implementação utilizar Kafka, configure o
mesmo para testes no Docker
- O publisher deve ser implementado utilizando Python; Deseja-se uma API
exposta para call do publisher, também implementada utilizando Python

### Tarefa 4:
Desejamos garantir que iremos popular apenas dados válidos em nosso Data
Sink, sendo assim:
- Com base no evento mapeado, implemente também em Python as
devidas validações de dados e estrutura
- Implemente o transform dos dados após validação
- Caso o dado não seja apto para seguir na pipeline, desejamos ter o
controle de quais informações foram recusadas e o motivo
- Pontos extras: Implementar testes unitários para as validações e transformações
de dados.

### Tarefa 5:
Consumers/Subscribers
- Por fim, o dado deve ser enviado para a camada final, podendo ser:
    - BigQuery
    - Google Cloud Storage
- Implemente as SDKs e o código do DataSink escolhido, podendo:
- Criar um projeto GCP para o desafio ou
- Criar um json e salvar local (apenas para termos a informação) e deixe o
código que implementa a sdk pronto para revisão
- Implemente o transform dos dados de acordo com a opção escolhida e justifique
a escolha com base no contexto da solução.

