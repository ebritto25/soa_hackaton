import pandas as pd
import os
import tensorflow as tf
from tensorflow import keras
from keras import layers, models
from keras.applications import MobileNetV2

# === VARIAVEIS GLOBAIS === #
img_height, img_width = 224, 224
epochs_base = 50

# === VERIFICA GPU ===
# Configura para usar GPU se disponível
def VerificaGpu():
    print("TensorFlow version:", tf.__version__)
    print("GPUs disponíveis:", tf.config.list_physical_devices('GPU'))
    print("Construído com CUDA:", tf.test.is_built_with_cuda())
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        try:
            # Permite crescimento de memória dinâmico
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            # Limita uso de memória GPU a 80%
            tf.config.set_logical_device_configuration(
                gpus[0],
                [tf.config.LogicalDeviceConfiguration(memory_limit=6144)]  # 6GB
            )
            print(f"✓ GPU detectada e configurada: {len(gpus)} GPU(s)")
        except RuntimeError as e:
            print(e)
    else:
        print("⚠ Nenhuma GPU detectada. Usando CPU.")

VerificaGpu()

# Funções para criar os datasets de treino e validação
def CreateTrainDataset(train_directory, img_height = 224, img_width = 224, batch_size = 16, label_mode = "categorical"):
    return keras.preprocessing.image_dataset_from_directory(
        train_directory,
     #   subset="training",
        seed = 42,
        image_size=(img_height, img_width),
        batch_size=batch_size,
        label_mode=label_mode
    )

def CreateValidationDataset(validation_directory, img_height = 224, img_width = 224, batch_size = 16, label_mode = "categorical"):
    return keras.preprocessing.image_dataset_from_directory(
        validation_directory,
      #  subset="validation",
        seed = 42,
        image_size=(img_height, img_width),
        batch_size=batch_size,
        label_mode=label_mode
    )        


# === CALLBACKS ===
early_stop = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
checkpoint = tf.keras.callbacks.ModelCheckpoint("melhor_modelo.h5", monitor='val_accuracy', save_best_only=True)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)

# Define os caminhos das pastas com as imagens
data_dir = "C:/UNICAMP/Hackthon/New Plant Diseases Dataset(Augmented)"
train_dir = data_dir + "/train"
validation_dir = data_dir + "/valid"


# Leitura dos diretorios das imagens
class_names = sorted(os.listdir(train_dir))
class_number = len(class_names)
print(f"Numero total de classes: {class_number}")
print(f"Classes: {class_names[:5]}")


# === CARREGA DATASETS === #

train_ds = CreateTrainDataset(train_dir)
val_ds = CreateValidationDataset(validation_dir)

#cache + prefetch
#Retirei o cache por ter muitas imagens
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)


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

# Verifica em qual dispositivo o modelo será treinado
print("\n=== INICIANDO TREINAMENTO ===")
print("Dispositivo de execução:", tf.test.gpu_device_name() if tf.test.gpu_device_name() else "CPU")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs_base,
    callbacks=[checkpoint, reduce_lr]
)

