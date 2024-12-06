# dpfm_factory
dpfm_factory is a Python package that provides a factory function to easily load different machine learning models and 
their associated preprocessing pipelines from Hugging Face. This package is particularly useful in the digital 
and computational pathology domains, where it is crucial to work with various specialized models.

## Features
 * Easy Model Loading: Load machine learning models and their preprocessing pipelines with a simple factory function.
 * Hugging Face Integration: Seamlessly integrates with Hugging Face to authenticate and load models.
 * Custom Environment Variables: Supports loading environment variables from a .env file for sensitive data like tokens.

## Installation
To install the package directly from GitHub, use the following command:

```shell
pip install git+https://github.com/Steven-N-Hart/dpfm_factory
```

Ensure that you have all necessary dependencies listed in the requirements.txt file. Alternatively, clone the 
repository and install the package locally:

```bash
git clone https://github.com/Steven-N-Hart/dpfm_factory
cd dpfm_factory
pip install -r requirements.txt
pip install .
```
## Usage
### Setup
Before using the package, make sure to create a .env file in the root of your project directory with your Hugging Face 
token:

> HUGGINGFACE_TOKEN=your_huggingface_token_here

### Example Usage
Here’s an example of how to use the model_factory function to load a model and its associated processor:

```python
from dpfm_factory.model_runners import model_factory

# Specify the model you want to load
model_name = 'MahmoodLab/conch'

# Load the model, processor, and the function to get image embeddings
model, processor, get_image_embedding = model_factory(model_name)

# Example usage with an image (replace 'your_image' with actual image data)
image_embedding = get_image_embedding(your_image)

print("Image Embedding:", image_embedding)
```

## Supported Models
The model_factory function currently supports the following models:

 * [owkin/phikon](https://www.medrxiv.org/content/10.1101/2023.07.21.23292757v1)
 * [paige-ai/Virchow2](https://arxiv.org/abs/2408.00738)
 * [MahmoodLab/conch](https://www.nature.com/articles/s41591-024-02856-4)
 * [prov-gigapath/prov-gigapath](https://www.nature.com/articles/s41586-024-07441-w)
 * [LGAI-EXAONE/EXAONEPath](https://arxiv.org/abs/2408.00380)
 * [histai/hibou-L](https://arxiv.org/html/2406.05074v1)
 * [histai/hibou-b](https://arxiv.org/html/2406.05074v1)
 * [google/path-foundation](https://huggingface.co/google/path-foundation)

> Note: Some of these models require a HuggingFace Token that has been approved by the model owner. The Google model 
> also requires submitters to sign additional Terms of Service.
 

## Error Handling
If an unsupported model name is provided, the model_factory will raise a NotImplementedError. For example:

```python
try:
    model, processor, get_image_embedding = model_factory('unsupported/model_name')
except NotImplementedError as e:
    print(e)
```
## Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.
