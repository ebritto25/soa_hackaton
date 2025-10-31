import pandas as pd
import os
import tensorflow as tf
from tensorflow import keras
from keras import layers, models
from keras.applications import MobileNetV2
from keras.models import load_model

#Variaveis globais
img_height, img_width = 224, 224
epochs_base = 50

# === CALLBACKS ===
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
checkpoint = tf.keras.callbacks.ModelCheckpoint("melhor_modelo.h5", monitor='val_accuracy', save_best_only=True)

# Define os caminhos das pastas com as imagens
data_dir = "D:/UNICAMP/Hackthon/New Plant Diseases Dataset(Augmented)"
train_dir = data_dir + "/train"
validation_dir = data_dir + "/valid"
test_dir = data_dir + "/test"

# Leitura dos diretorios das imagens
class_names = sorted(os.listdir(train_dir))
class_number = len(class_names)
print(f"Numero total de classes: {class_number}")
print(f"Classes: {class_names[:5]}")


# Funções para criar os datasets de treino e validação
def CreateTrainDataset(train_directory, img_height = 224, img_width = 224, batch_size = 32, label_mode = "categorical"):
    return keras.preprocessing.image_dataset_from_directory(
        train_directory,
     #   subset="training",
        seed = 42,
        image_size=(img_height, img_width),
        batch_size=batch_size,
        label_mode=label_mode
    )

def CreateValidationDataset(validation_directory, img_height = 224, img_width = 224, batch_size = 32, label_mode = "categorical"):
    return keras.preprocessing.image_dataset_from_directory(
        validation_directory,
      #  subset="validation",
        seed = 42,
        image_size=(img_height, img_width),
        batch_size=batch_size,
        label_mode=label_mode
    )

# === CARREGA DATASETS === #

train_ds = CreateTrainDataset(train_dir)
val_ds = CreateValidationDataset(validation_dir)

#cache + prefetch
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)

# === CRIA O MODELO DE REDE NEURAL ===
# O modelo utilizado e com os pesos da imagenet e sem o topo do modelo
# que vai ser substituido

base_model = MobileNetV2(
    input_shape=(img_height, img_width, 3),
    include_top=False,
    weights="imagenet"
)
base_model.trainable = False

model = models.Sequential([
    layers.Rescaling(1./255),
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(38, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs_base,
    callbacks=[checkpoint, reduce_lr]
)

# Percorre cada nome das classes 
#for class_name in class_names:
#    train_path = os.path.join(train_dir,class_name)
#    valid_path = os.path.join(validation_dir,class_name)
