import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import os
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# === VARIAVEIS GLOBAIS === #
img_height, img_width = 224, 224

# === CARREGA O MODELO TREINADO === #
model_dir = "C:/UNICAMP/Hackthon/soa_hackaton/Model_ML"
model = load_model(model_dir + "/melhor_modelo.h5")

# === PREPARA O CONJUNTO DE TESTE === #
data_dir = "C:/UNICAMP/Hackthon/New Plant Diseases Dataset(Augmented)"
test_dir = data_dir + "/test"

test_ds = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    image_size=(img_height, img_width),
    batch_size=1,
    label_mode="categorical",
    shuffle=False
)

class_names = sorted(os.listdir(test_dir))

true_labels = []
pred_labels = []
pred_probs_all = []

# === PREDIÇÂO DO CONJUNTO DE TESTE === #
# Percorre o dataset de testes e realiza a predição de cada imagem
# utilizando a predição com a maior probabilidade
for i, (img_batch, label_batch) in enumerate(test_ds):
    true_class = tf.argmax(label_batch[0]).numpy()
    pred_prob = model.predict(img_batch, verbose=0)[0]
    pred_class = np.argmax(pred_prob)

    true_labels.append(true_class)
    pred_labels.append(pred_class)
    pred_probs_all.append(pred_prob)


# === RELATÓRIO E MATRIZ DE CONFUSÃO ===
print("\n=== Avaliação no conjunto de teste ===")
print(classification_report(true_labels, pred_labels, target_names=class_names))

cm = confusion_matrix(true_labels, pred_labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=class_names)
disp.plot(cmap=plt.cm.Blues)
plt.title("Matriz de Confusão - Teste")
plt.show()

# O resultado na base de teste utilizada teve o seguinte resultados:
# Acc: 95%
# F1: 93%
# Recall: 94%