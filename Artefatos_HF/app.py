# Imports necessários
import json
import numpy as np
import uvicorn
import io
import os
import httpx
import yaml
from datetime import datetime, timezone
from tensorflow import keras
from keras.models import load_model
from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Request
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel

# Schemas do YAML
class Diagnosis(BaseModel):
    scientificName: str
    crop: str
    commonName: str
    description: str
    confidence: float

class CommonError(BaseModel):
    code: int
    datetime: str
    message: str
    details: str

# Carregar YAML
openapi_schema = None
try:
    with open("api_backend.yaml", "r", encoding="utf-8") as f:
        openapi_schema = yaml.safe_load(f)
except Exception as e:
    print(f"ERRO CRÍTICO: Não foi possível carregar api_backend.yaml. {e}")

# Inicializa a API
app = FastAPI(
    title="AgroLens API",
    description="Diagnóstico de pragas por imagem e recomendação de tratamento",
    version="0.0.1",
    openapi_schema=openapi_schema
)

# Configuração inicial (classes e modelo)
model_path = "melhor_modelo.h5"
try:
    model = load_model(model_path)
except Exception as e:
    print(f"ERRO: Não foi possível carregar o modelo {model_path}: {e}")
    model = None

class_names = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 
               'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___healthy', 
               'Cherry_(including_sour)___Powdery_mildew', 
               'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
               'Corn_(maize)___healthy', 'Corn_(maize)___Northern_Leaf_Blight', 'Grape___Black_rot', 
               'Grape___Esca_(Black_Measles)', 'Grape___healthy', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
               'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 
               'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 
               'Potato___healthy', 'Potato___Late_blight', 'Raspberry___healthy', 'Soybean___healthy', 
               'Squash___Powdery_mildew', 'Strawberry___healthy', 'Strawberry___Leaf_scorch', 
               'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___healthy', 
               'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 
               'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
               'Tomato___Tomato_mosaic_virus', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus']

class_names = sorted(class_names)

with open("disease_info.json", "r", encoding="utf-8") as f:
    diseases_info = json.load(f)

TOKEN_API_EMBRAPA = os.getenv("TOKEN_API_EMBRAPA")

# Funções auxiliares
def preprocess_image(image_bytes: bytes) -> np.ndarray:
    try:
        img = Image.open(io.BytesIO(image_bytes))
    except UnidentifiedImageError:
        raise ValueError("Imagem inválida ou corrupta.")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = keras.utils.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def error_response(code: int, message: str, details: str):
    return CommonError(
        code=code,
        datetime=datetime.now(timezone.utc).isoformat(),
        message=message,
        details=details
    )

# Endpoints
@app.get("/")
def read_root(request: Request):
    return {"message": "AgroLens API está no ar."}

@app.post("/imageDiagnosis", response_model=Diagnosis, responses={401: {"model": CommonError}, 403: {"model": CommonError}, 404: {"model": CommonError}, 500: {"model": CommonError}})
async def image_diagnosis(file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail=error_response(500, "Erro interno", "Erro interno no servidor.").dict())

    try:
        image_bytes = await file.read()
        img_array = preprocess_image(image_bytes)
        predictions = model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        predicted_class_name = class_names[predicted_class]
        confidence_class = float(predictions[0][predicted_class])
    except Exception as e:
        raise HTTPException(status_code=500, detail=error_response(500, "Erro interno", "Erro interno no servidor.").dict())

    disease_info = diseases_info.get(predicted_class_name, {})
    if not disease_info:
        raise HTTPException(status_code=404, detail=error_response(404, "Praga não encontrada na nossa base de dados", "Não foi possível encontrar a Praga no nosso banco de dados.").dict()
        )
        
    return Diagnosis(
        scientificName=disease_info.get("scientific_name", "N/A"),
        commonName=disease_info.get("commonName", "N/A"),
        crop=disease_info.get("crop", "N/A"),
        description=disease_info.get("description", "N/A"),
        confidence=confidence_class
    )

@app.get("/treatment", responses={401: {"model": CommonError}, 403: {"model": CommonError}, 404: {"model": CommonError}, 500: {"model": CommonError}})
async def get_treatment(diseaseName: str = Query(...)):
    if not TOKEN_API_EMBRAPA:
        raise HTTPException(status_code=500, detail=error_response(500, "Erro interno", "Erro interno no servidor.").dict())

    EMBRAPA_API_URL = "https://api.cnptia.embrapa.br/agrofit/v1/search/produtos-formulados"
    headers = {"accept": "application/json", "Authorization": f"Bearer {TOKEN_API_EMBRAPA}"}
    params = {"q": diseaseName, "praga_nome_cientifico": diseaseName}

    async with httpx.AsyncClient(verify=False) as client:
        try:
            response = await client.get(EMBRAPA_API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data or not isinstance(data, list) or len(data) == 0:
                raise HTTPException(
                    status_code=404, 
                    detail=error_response(404, "Praga não encontrada na nossa base de dados", "Não foi possível encontrar a Praga no nosso banco de dados.").dict()
                )

            return data

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPException(status_code=401, detail=error_response(401, "Não autorizado", "Não autorizado.").dict())
            elif e.response.status_code == 403:
                raise HTTPException(status_code=403, detail=error_response(403, "Proibido", "Proibido para esse recurso.").dict())
            elif e.response.status_code == 404:
                raise HTTPException(status_code=404, detail=error_response(404, "Praga não encontrada na nossa base de dados", "Não foi possível encontrar a Praga no nosso banco de dados.").dict())
            else:
                raise HTTPException(status_code=500, detail=error_response(500, "Erro interno", "Erro interno no servidor.").dict())

        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=error_response(500, "Erro interno", "Erro interno no servidor.").dict())