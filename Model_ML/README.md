# Model ML - Sistema de Classificação de Doenças em Plantas

Este diretório contém os scripts para treinamento, validação e inferência de um modelo de Machine Learning para classificação de doenças em plantas usando MobileNetV2.

## 📋 Requisitos

- Python 3.10
- TensorFlow 2.1.0
- Keras
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- GPU (opcional, mas recomendado para treinamento)

### Instalação de Dependências

```bash
pip install tensorflow numpy pandas matplotlib scikit-learn
```

## 📁 Estrutura de Arquivos

```
Model_ML/
├── ModelTraining.py      # Script de treinamento do modelo
├── ModelValidation.py    # Script de validação e métricas
├── ModelInferencia.py    # Script de inferência/predição
├── disease_info.json     # Informações sobre doenças (nomes científicos e descrições)
├── melhor_modelo.h5      # Modelo treinado (gerado após o treinamento)
```

## 🎯 Dataset Necessário

O projeto espera o dataset **"New Plant Diseases Dataset (Augmented)"** na seguinte estrutura:

```
New Plant Diseases Dataset(Augmented)/
├── train/           # Imagens de treinamento
├── valid/           # Imagens de validação
└── test/            # Imagens de teste
```

Cada subpasta deve conter diretórios com o nome das classes (ex: `Apple___Apple_scab`, `Tomato___healthy`, etc.)

### Classes Suportadas

O modelo classifica 38 classes de plantas e suas respectivas doenças/condições saudáveis:
- Apple (4 classes)
- Blueberry (1 classe)
- Cherry (2 classes)
- Corn/Maize (4 classes)
- Grape (4 classes)
- Orange (1 classe)
- Peach (2 classes)
- Pepper/Bell (2 classes)
- Potato (3 classes)
- Raspberry (1 classe)
- Soybean (1 classe)
- Squash (1 classe)
- Strawberry (2 classes)
- Tomato (10 classes)

## 🚀 Como Usar

### 1. Treinamento do Modelo

O script `ModelTraining.py` treina um modelo MobileNetV2 com transfer learning.

**Parâmetros principais:**
- `img_height`, `img_width`: 224x224 pixels
- `epochs_base`: 50 épocas
- `batch_size`: 16 (padrão)

**Callbacks configurados:**
- `EarlyStopping`: Para evitar overfitting (patience=10)
- `ModelCheckpoint`: Salva o melhor modelo baseado em val_accuracy
- `ReduceLROnPlateau`: Reduz learning rate quando necessário


**Como executar:**

```bash
python ModelTraining.py
```

**Antes de executar, ajuste os caminhos:**
```python
data_dir = "Endereço local/New Plant Diseases Dataset(Augmented)"
```

**Saída:**
- Arquivo `melhor_modelo.h5` com o modelo treinado
- Histórico de treinamento com métricas de loss e accuracy

---

### 2. Validação do Modelo

O script `ModelValidation.py` avalia o desempenho do modelo no conjunto de teste.

**Funcionalidades:**
- Carrega o modelo treinado (`melhor_modelo.h5`)
- Realiza predições no conjunto de teste
- Gera relatório de classificação (precision, recall, f1-score)
- Cria matriz de confusão

**Como executar:**

```bash
python ModelValidation.py
```

**Antes de executar, ajuste os caminhos:**
```python
model_dir = "C:/UNICAMP/Hackthon/soa_hackaton/Model_ML"
data_dir = "C:/UNICAMP/Hackthon/New Plant Diseases Dataset(Augmented)"
```

**Saída:**
- Classification Report com métricas por classe
- Matriz de confusão
- Métricas de acurácia geral do modelo

---

### 3. Inferência (Predição)

O script `ModelInferencia.py` realiza predições em imagens individuais.

**Funcionalidades:**
- Carrega o modelo treinado
- Processa uma imagem de entrada
- Retorna predição com confiança
- Busca informações científicas no `disease_info.json`
- Retorna JSON estruturado com resultado

**Como executar:**

```bash
python ModelInferencia.py
```

**Antes de executar, ajuste os caminhos:**
```python
model_dir = "C:/UNICAMP/Hackthon/soa_hackaton/Model_ML"
img_path = "caminho/para/sua/imagem.jpg"
```

**Formato de saída (JSON):**
```json
{
  "class": "Apple___Apple_scab",
  "plant": "Apple",
  "disease": "Apple_scab",
  "confidence": 0.9876,
  "scientific_name": "Venturia inaequalis",
  "description": "Doença fúngica que causa lesões escuras nas folhas e frutos..."
}
```

## 📊 Arquitetura do Modelo

O modelo utiliza **MobileNetV2** como base (pré-treinado no ImageNet):

```
Input (224x224x3)
    ↓
Rescaling (1./255)
    ↓
MobileNetV2 (frozen)
    ↓
GlobalAveragePooling2D
    ↓
Dense (128, relu)
    ↓
Dropout (0.5)
    ↓
Dense (38, softmax)
```

**Compilação:**
- Optimizer: Adam
- Loss: Categorical Crossentropy
- Metrics: Accuracy

---

## 🔧 Configurações Importantes

### Ajuste de Caminhos
**IMPORTANTE:** Ajuste os seguintes caminhos antes de executar:

```python
# ModelTraining.py e ModelValidation.py
data_dir = "C:/UNICAMP/Hackthon/New Plant Diseases Dataset(Augmented)"

# ModelInferencia.py e ModelValidation.py
model_dir = "C:/UNICAMP/Hackthon/soa_hackaton/Model_ML"

# ModelInferencia.py
img_path = "caminho/para/imagem/teste.jpg"
```

## 📝 Arquivo disease_info.json

Contém informações detalhadas sobre cada doença:

```json
{
  "Apple___Apple_scab": {
    "scientific_name": "Venturia inaequalis",
    "description": "Descrição da doença..."
  }
}
```

Este arquivo é essencial para o script de inferência retornar informações científicas.

---

## ⚠️ Troubleshooting

### Erro de GPU
Se não houver GPU disponível, o modelo rodará em CPU (mais lento para treinamento).

### Erro de Caminho
Verifique se todos os caminhos nos scripts estão corretos para sua máquina.

### Erro de Memória
Reduza o `batch_size` ou ajuste `memory_limit` na configuração da GPU.

---

## 📈 Resultados Esperados

Com o dataset completo e treinamento adequado, espera-se:
- **Accuracy de treino:** > 95%
- **Accuracy de validação:** > 90%
- **Tempo de treinamento:** ~2-4 horas com GPU, muito mais em CPU

---

## 📄 Licença

Este projeto foi desenvolvido para o Hackathon UNICAMP.
