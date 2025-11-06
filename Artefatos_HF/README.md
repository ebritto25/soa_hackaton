# AgroLens API 🌿

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/Leonardo-Cerce/agrolens)

Esta API permite o envio de imagens de folhas de plantas para a análise de pragas e infecções, utilizando um modelo de inferência (MobileNet) treinado.

Além do diagnóstico, a API se conecta ao serviço [Agrofit da Embrapa](https://www.agroapi.cnptia.embrapa.br/store/apis/info?name=AGROFIT&provider=agroapi&version=v1#/) para consultar recomendações de tratamento baseadas no nome científico da praga identificada.

## 📖 Documentação

Acesse a documentação interativa (Swagger) para testar os *endpoints* diretamente no navegador:

**[https://leonardo-cerce-agrolens.hf.space/docs](https://leonardo-cerce-agrolens.hf.space/docs)**

---

## 🌐 Endpoints

A API possui dois *endpoints* principais.

### 1. Diagnóstico por Imagem

Identifica a doença na imagem de uma folha e retorna informações detalhadas sobre ela.

* **Endpoint:** `POST /imageDiagnosis`
* **Corpo da Requisição:** `multipart/form-data`
    * `file`: A imagem da folha (`.jpg`, `.png`).
* **Resposta de Sucesso (200 OK):**
    ```json
    {
      "scientificName": "Alternaria solani",
      "crop": "Tomate",
      "commonName": "Pinta-preta (Requeima-precoce)",
      "description": "Doença fúngica que causa lesões em anéis concêntricos nas folhas. Afeta primeiro as folhas mais velhas e pode reduzir a produtividade.",
      "confidence": 0.5844219923019409
    }
    ```

### 2. Recomendação de Tratamento

Consulta a API da Embrapa para listar produtos formulados recomendados para tratar uma praga específica, usando seu nome científico.

* **Endpoint:** `GET /treatment`
* **Parâmetro de Query (Obrigatório):**
    * `diseaseName`: (string) O nome científico da praga (ex: "Alternaria solani").
* **Resposta de Sucesso (200 OK):**
    Retorna uma lista de produtos. O exemplo abaixo está **resumido** para clareza.
    ```json
    {
      "totalPaginas": 1,
      "totalRegistros": 1,
      "registros": [
        {
          "numero_registro": "19617",
          "marca_comercial": [ "Curado" ],
          "titular_registro": "Sumitomo Chemical Brasil Indústria Química S.A.",
          "classe_categoria_agronomica": [ "Fungicida" ],
          "ingrediente_ativo_detalhado": [
            {
              "ingrediente_ativo": "fluazinam",
              "grupo_quimico": "fenilpiridinilamina",
              "concentracao": "500"
              // ...
            }
          ],
          "indicacao_uso": [
            {
              "cultura": "Batata",
              "praga_nome_cientifico": "Alternaria solani",
              "praga_nome_comum": [ "Pinta-preta", "Pinta-preta-grande" ]
            },
            {
              "cultura": "Tomate",
              "praga_nome_cientifico": "Alternaria solani",
              "praga_nome_comum": [ "Mancha-de-Alternaria", "Pinta-preta-grande" ]
            }
            // ... e outras indicações
          ],
          "url_agrofit": "[https://agrofit.agricultura.gov.br/agrofit_cons/!ap_produto_form_detalhe_cons?p_nr_registro=19617](https://agrofit.agricultura.gov.br/agrofit_cons/!ap_produto_form_detalhe_cons?p_nr_registro=19617)..."
        }
        // ... e outros registros
      ]
    }
    ```

---

## 🛠️ Como Fazer o Deploy (Auto-Hospedagem com Docker)

Caso queira rodar esta API em seu próprio servidor, você pode fazê-lo usando Docker.

### Pré-requisitos

* [Git](https://git-scm.com/)
* [Git LFS](https://git-lfs.github.com/) (para baixar o arquivo do modelo `.h5`)
* [Docker](https://www.docker.com/)

### 1. Clonar o Repositório

```bash
# Clone o repositório do Space
git clone https://huggingface.co/spaces/Leonardo-Cerce/agrolens
cd agrolens

# Baixe os arquivos grandes (o modelo .h5)
git lfs pull
```

### 2. Configurar Variáveis de Ambiente

Este projeto precisa de uma chave de API para consultar o serviço da Embrapa.

Crie um arquivo chamado `.env` na raiz do projeto:

`.env`

```bash
# Obtenha seu token em: https://www.agroapi.cnptia.embrapa.br/store/apis/info?name=AGROFIT&provider=agroapi&version=v1#/
EMBRAPA_API_TOKEN="seu-token-bearer-da-embrapa-aqui"
```

### 3. Rodar a Aplicação com Docker
O `Dockerfile` já está incluído no projeto.

**1. Construa a imagem Docker:**

```bash
docker build -t agrolens-api .
```

**2. Execute o contâiner:**

```bash
# Este comando mapeia a porta 8000 do seu PC para a porta 7860
# do contâiner e injeta as variáveis de ambiente do arquivo .env

docker run -p 8000:7860 --env-file ./.env agrolens-api
```
A API estará disponível em `http://localhost:8000`.

## 📁 Estrutura do Repositório
* `app.py`: O código principal da API FastAPI. Contém a lógica dos endpoints, o carregamento do modelo e as chamadas à API da Embrapa.
* `melhor_modelo.h5`: O modelo MobileNet treinado, baixado via Git LFS.
* `disease_info.json`: Arquivo de dados (JSON) que mapeia os diagnósticos do modelo para informações detalhadas (nomes, descrições, etc.).
* `api_backend.yaml`: A especificação OpenAPI (contrato da API).
* `Dockerfile`: As instruções para construir o contâiner Docker que serve a API.
* `requirements.txt`: A lista de bibliotecas Python necessárias para rodar o projeto.
* `README.md`: Esta documentação.