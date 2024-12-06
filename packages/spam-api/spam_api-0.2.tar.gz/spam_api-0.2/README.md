##Nuevo! pueden instalar la API como una libreria directamente con "pip install spam-api" desde la terminal

# Spam Detection API

Esta es una API simple creada con **FastAPI** que permite detectar si un mensaje es **spam** o **no spam** usando un modelo de machine learning entrenado con **Naive Bayes**. La API permite cargar nuevos datos de entrenamiento, así como realizar predicciones sobre mensajes.

## Requisitos

- **Python 3.7+**
- Las siguientes dependencias:

```bash
fastapi
uvicorn
pydantic
joblib
scikit-learn
python-multipart
pandas
```

Instalacion
Clona este repositorio o descarga el código fuente.

Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate  # En Linux/MacOS
venv\Scripts\activate     # En Windows
```
**Instala las dependecias**

```bash
pip install -r requirements.txt
```

Ejecutar la API
Para correr la API, usa Uvicorn:

```bash
uvicorn anti_spam:app --reload
```

Esto iniciará la API en http://127.0.0.1:8000.


**Endpoints**

/detect_spam/ (POST)
Este endpoint recibe un mensaje de texto y devuelve si es spam o no.

Ejemplo de request:

```json
{
    "text": "Congratulations! You have won a free gift card."
}
```
Ejemplo de respuesta:

```json
{
  "is_spam": true
}
```

/train_model/ (POST)
Este endpoint permite agregar nuevos datos de entrenamiento (texto y etiqueta) al modelo.

Ejemplo de request: (hay que asegurarse de que cada dato de entrenamiento tenga el texto y la etiqueta correspondiendte. 1 = SPAM, 0 = NO SPAM)

```json
[{
    "text": "spam message!",
    "label": 1
  },
  {
    "text": "normal message.",
    "label": 0
}]
```

Ejemplo de respuesta:

```json
{
  "message": "Datos cargados correctamente, el modelo se ha entrenado."
}
```

Cargar un archivo CSV
Puedes cargar un archivo CSV con datos de entrenamiento usando el siguiente endpoint:
/upload_data/ (POST)


**Nota**
Este proyecto utiliza un modelo de Naive Bayes para clasificación de texto, que ha sido entrenado previamente con algunos datos de ejemplo. Puedes agregar más datos de entrenamiento y reentrenar el modelo en cualquier momento.

