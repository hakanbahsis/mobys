import pickle
from keras_preprocessing.image import load_img, img_to_array
import numpy as np
import tensorflow as tf


def predict(image):
    model_path=image
    interpreter = tf.lite.Interpreter(model_path="sinifmodel.tflite")
    interpreter.allocate_tensors()

    input_tensor=interpreter.tensor(interpreter.get_input_details()[0]["index"])
    output_tensor=interpreter.tensor(interpreter.get_input_details()[0]["index"])
    





    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    img = load_img(image, target_size = (224, 224,3))
    img = img_to_array(img)
    img = np.expand_dims(img, axis = 0)

    # Seçilen dosyayı modelle eşleştirin ve tahminlerinizi hesaplayın
    prediction = model.predict(img)
    return prediction
