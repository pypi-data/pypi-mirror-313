from huggingface_hub import hf_hub_download, from_pretrained_keras
import tensorflow as tf
import numpy as np
import keras.layers as kl
import os
from PIL import Image
import re

class GoogleLoader:
    def __init__(self, model_name="google/path-foundation"):

        try:
            # Load the model directly from Hugging Face Hub
            loaded_model = from_pretrained_keras("google/path-foundation")
            self.model = loaded_model.signatures["serving_default"]
        except ValueError as e:
            # Use TFSMLayer to load the SavedModel for inference
            model_string = ' '.join(e.args[0].split()[47:50]).replace('`','').replace('use ','')
            match = re.match(r'keras\.layers\.TFSMLayer\(([^,]+), call_endpoint=\'([^\']+)\'\)', model_string)
            model_path = match.group(1).strip()
            call_endpoint = match.group(2).strip()
            self.model = kl.TFSMLayer(model_path, call_endpoint=call_endpoint)
        self.processor = self.create_processor()
        self.device = 1 if tf.config.list_physical_devices('GPU') else 0

    @staticmethod
    def create_processor():
        """Returns a processor function for resizing and normalizing numpy arrays."""
        def processor(image_array):
            if isinstance(image_array, Image.Image):
                image_array = np.array(image_array)
            if not isinstance(image_array, np.ndarray):
                raise ValueError("Input must be a numpy array.")
            # Ensure the array has three channels (H, W, C)
            if image_array.ndim != 3 or image_array.shape[2] != 3:
                raise ValueError("Input numpy array must have shape (H, W, 3).")
            # Convert image to float32 and normalize to [0, 1]
            image_array = image_array.astype('float32') / 255.0

            # Resize to (224, 224)
            image_tensor = tf.image.resize(image_array, (224, 224))

            # Add batch dimension
            return tf.expand_dims(image_tensor, axis=0)
        return processor

    def get_processor_and_model(self):
        return self.processor, self.model


    # Function to get image embedding
    def get_image_embedding(self, image, processor, model, device):
        image_tensor = self.processor(image)

        embeddings = self.model(image_tensor)

        return np.squeeze(embeddings["output_0"])
