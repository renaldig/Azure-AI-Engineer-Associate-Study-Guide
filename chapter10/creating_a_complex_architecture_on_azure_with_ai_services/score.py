import json
import numpy as np
from joblib import load
from azureml.core.model import Model

def init():
    global model
    # Retrieve the path to the model file using the model name
    model_path = Model.get_model_path('iris-classifier')
    model = load(model_path)

def run(raw_data):
    try:
        # Parse the input data
        data = np.array(json.loads(raw_data)['data'])
        # Make a prediction
        result = model.predict(data)
        # Return the result as JSON
        return json.dumps({'result': result.tolist()})
    except Exception as e:
        error = str(e)
        return json.dumps({'error': error})
