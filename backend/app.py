from flask import Flask, request, jsonify, send_from_directory
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import io
import os
import base64
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

# Get the absolute path of the directory where app.py is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute path to the model file
model_path = os.path.join(base_dir, 'model/digit_recognizer_model.h5')

# Load the model
model = load_model(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        img_data = base64.b64decode(data['image'].split(',')[1])
        image = Image.open(io.BytesIO(img_data)).convert('L')  # Convert to grayscale
        image.save("received_image.png")  # Save the received image for inspection
        image = image.resize((28, 28))  # Resize to 28x28
        image = img_to_array(image)
        image = image.reshape((1, 28 * 28))  # Flatten the image to (1, 784)
        image = image.astype('float32') / 255.0  # Normalize the image

        logging.debug(f'Image shape: {image.shape}')
        logging.debug(f'Image data: {image}')

        prediction = model.predict(image)
        logging.debug(f'Raw prediction: {prediction}')
        
        predicted_digit = np.argmax(prediction, axis=1)[0]
        confidence = np.max(prediction, axis=1)[0]

        logging.debug(f'Predicted digit: {predicted_digit}, Confidence: {confidence}')

        return jsonify({
            'digit': int(predicted_digit),
            'confidence': float(confidence)
        })
    except Exception as e:
        logging.error(f'Error during prediction: {e}')
        return jsonify({'error': str(e)})

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    app.run(debug=True)
