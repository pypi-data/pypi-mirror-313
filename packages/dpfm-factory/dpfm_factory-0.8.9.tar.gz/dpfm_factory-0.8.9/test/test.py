from dpfm_model_runners.model_factory import model_factory
from PIL import Image
import numpy as np

# Specify the model you want to load
model_name = 'google/path-foundation'
# Read in image
img_path = 'test/crc_images_1.3.6.1.4.1.5962.99.1.2240754973.60441079.1638623327517.8.0_4352_4608_10240_10496_3287.png'
your_image = np.asarray(Image.open(img_path))
# Load the model, processor, and the function to get image embeddings
model, processor, get_image_embedding = model_factory(model_name=model_name)

# Example usage with an image (replace 'your_image' with actual image data)
image_embedding = get_image_embedding(your_image, processor, model, 'gpu')

print("Image Embedding:", image_embedding.shape)
