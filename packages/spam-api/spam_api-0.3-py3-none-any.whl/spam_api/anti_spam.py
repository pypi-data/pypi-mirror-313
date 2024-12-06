from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib
import pandas as pd
import io
import uvicorn

class SpamRequest(BaseModel):
    text: str


app = FastAPI()

try:
    model_data = joblib.load('spam_detector_model.pkl')
    model = model_data[0] 
    vectorizer = model_data[1]
except FileNotFoundError:
    model = MultinomialNB()
    vectorizer = CountVectorizer()


class TrainRequest(BaseModel):
    text: str
    label: int


@app.post("/upload_data/")
async def upload_data(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Asegúrate de que el archivo tenga las columnas correctas
        if 'text' not in df or 'label' not in df:
            raise HTTPException(status_code=400, detail="El archivo debe contener las columnas 'text' y 'label'.")
        
        texts = df['text'].tolist()
        labels = df['label'].tolist()

        X_new = vectorizer.fit_transform(texts)

        model.partial_fit(X_new, labels, classes=[0, 1])

        joblib.dump((model, vectorizer), 'spam_detector_model.pkl')

        return {"message": "Datos cargados y modelo actualizado con éxito."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 

# Ruta para entrenar el modelo con nuevos datos
@app.post("/train_model/")
async def train_model(request: list[TrainRequest]):
    global model, vectorizer
    try:
        for item in request:
            texts = [item.text for item in request]
            labels = [item.label for item in request]
            
            X = vectorizer.fit_transform(texts)
            y = labels

            model.fit(X, y)
            joblib.dump((model, vectorizer), 'spam_detector_model.pkl')
            
            
        return {"message": "Textos agregados y modelo actualizado con éxito."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar los textos: {str(e)}")


@app.post("/detect_spam/")
def detect_spam(request: SpamRequest):
    try:
        text_vectorized = vectorizer.transform([request.text])
        prediction = model.predict(text_vectorized)
        return {"is_spam": bool(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run():
    """Función para ejecutar el servidor de FastAPI"""
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
if __name__ == "__main__":
    run()