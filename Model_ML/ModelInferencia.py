# Este codigo ira seguir alguns passos para fazer a inferencia na imagem
# e retorna o JSON com as seguintes informações

import json
import numpy as np
from tensorflow import keras
from keras.models import load_model

# 1. Carregar o modelo treinado
model_dir = "C:/UNICAMP/Hackthon/soa_hackaton/Model_ML"
model = load_model(model_dir + "/melhor_modelo.h5")

# Lista de classes
class_names = ['Apple___Apple_scab',
'Apple___Black_rot',
'Apple___Cedar_apple_rust',
'Apple___healthy',
'Blueberry___healthy',
'Cherry_(including_sour)___healthy',
'Cherry_(including_sour)___Powdery_mildew',
'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
'Corn_(maize)___Common_rust_',
'Corn_(maize)___healthy',
'Corn_(maize)___Northern_Leaf_Blight',
'Grape___Black_rot',
'Grape___Esca_(Black_Measles)',
'Grape___healthy',
'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
'Orange___Haunglongbing_(Citrus_greening)',
'Peach___Bacterial_spot',
'Peach___healthy',
'Pepper,_bell___Bacterial_spot',
'Pepper,_bell___healthy',
'Potato___Early_blight',
'Potato___healthy',
'Potato___Late_blight',
'Raspberry___healthy',
'Soybean___healthy',
'Squash___Powdery_mildew',
'Strawberry___healthy',
'Strawberry___Leaf_scorch',
'Tomato___Bacterial_spot',
'Tomato___Early_blight',
'Tomato___healthy',
'Tomato___Late_blight',
'Tomato___Leaf_Mold',
'Tomato___Septoria_leaf_spot',
'Tomato___Spider_mites Two-spotted_spider_mite',
'Tomato___Target_Spot',
'Tomato___Tomato_mosaic_virus',
'Tomato___Tomato_Yellow_Leaf_Curl_Virus']

# Ordena para ficar igual o treino
class_names = sorted(class_names)

# 2. Carregar a imagem
img_path = "C:/UNICAMP/Hackthon/New Plant Diseases Dataset(Augmented)/test/Apple___Cedar_apple_rust/AppleCedarRust1.JPG"
img = keras.utils.load_img(img_path, target_size=(224, 224))
img_array = keras.utils.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# 3. Fazer a predição
predictions = model.predict(img_array)
predicted_class = np.argmax(predictions[0])
confidence = predictions[0][predicted_class]

# Mostra top 3 predições para debug
top3_indices = np.argsort(predictions[0])[-3:][::-1]
print("\nTop 3 predições:")
for idx in top3_indices:
    print(f"{class_names[idx]}: {predictions[0][idx]*100:.2f}%")

# Extrai nome da planta e doença
predicted_class_name = class_names[predicted_class]
predicted_plant = predicted_class_name.split("___")[0]
predicted_disease = predicted_class_name.split("___")[1]

# Leitura do Json com o nome cientifico da doença e uma breve descrição
with open("disease_info.json", "r") as f:
    diseases_info = json.load(f)
disease_info = diseases_info[predicted_class_name]

# Converte o nome da doença para o nome cientifico
scientific_disease = disease_info['scientific_name']
description_disease = disease_info['description']

# 4. Mostrar resultado final
print(f"\n=== RESULTADO ===")
print(f"Classe predita: {predicted_class_name}")
print(f"Planta predita: {predicted_plant}")
print(f"Doença predita: {predicted_disease}")
print(f"Nome científico: {scientific_disease}")
print(f"Descrição: {description_disease}")
print(f"Confiança: {confidence * 100:.2f}%")

#5. Json de resposta
response = {
    "class": predicted_class_name,
    "plant": predicted_plant,
    "disease": predicted_disease,
    "confidence": float(confidence),
    "scientific_name": scientific_disease,
    "description": description_disease
}

print(response)


