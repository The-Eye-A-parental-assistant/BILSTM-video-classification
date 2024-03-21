from keras.preprocessing import image
from keras.applications.inception_v3 import InceptionV3, preprocess_input
from keras.models import Model, load_model
from keras.layers import Input
from keras.utils import img_to_array, load_img 
import numpy as np

class Extractor():
    def __init__(self, image_shape=(299, 299, 3), weights=None, cnn_model = 'inception'):
        """Either load pretrained from imagenet, or load our saved
        weights from our own training."""

        self.weights = weights  # so we can check elsewhere which model

        input_tensor = Input(image_shape)
        # Get model with pretrained weights.
        if cnn_model == 'inception':
            print("Using InceptionV3")
            base_model = InceptionV3(
                input_tensor=input_tensor,
                weights='imagenet',
                include_top=True
            )

        # We'll extract features at the final pool layer.
        self.model = Model(
            inputs=base_model.input,
            outputs=base_model.get_layer('avg_pool').output
        )

    def extract(self, image_path):
        img = load_img(image_path)

        return self.extract_image(img)

    def extract_image(self, img):
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Get the prediction.
        features = self.model.predict(x)

        if self.weights is None:
            # For imagenet/default network:
            features = features[0]
        else:
            # For loaded network:
            features = features[0]

        return features