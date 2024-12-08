import tensorflow as tf
import keras.models
from keras.models import load_model
import numpy as np
from tensorflow.keras.utils import load_img,img_to_array
from keras.utils import custom_object_scope
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'TunedModel.keras')



def getModel():
    model = tf.keras.models.load_model(model_path,compile=True)
    base_learning_rate = 0.0001
    model.compile(optimizer=tf.keras.optimizers.RMSprop(learning_rate=base_learning_rate),
                loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=['accuracy'])
    return model


def examine(model, imgFile):
    class_names=['IllegibleMeter','Calculator','Meter','Non-Meter']
    # dimensions of our images
    img_width, img_height = 160, 160
    # predicting images
    img = load_img(imgFile, target_size=(img_width, img_height))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])
    pred= np.argmax( tf.nn.softmax(model.predict(images)))
    return class_names[pred]