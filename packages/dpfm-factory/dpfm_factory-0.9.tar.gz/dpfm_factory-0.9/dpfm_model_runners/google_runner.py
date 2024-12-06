from huggingface_hub import hf_hub_download, from_pretrained_keras
import tensorflow as tf
import numpy as np
import keras.layers as kl
import os
from PIL import Image

class GoogleLoader:
    def __init__(self, model_name="google/path-foundation"):
        model_path = hf_hub_download(repo_id="google/path-foundation", filename='saved_model.pb', local_dir='hub/google')
        if model_path is None:  # In case No internet access, I will add to Docker container manually
            model_path='hub/google'
        # Load the model directly from Hugging Face Hub
        # Use TFSMLayer to load the SavedModel for inference
        self.model = kl.TFSMLayer(model_path, call_endpoint='serving_default')
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
