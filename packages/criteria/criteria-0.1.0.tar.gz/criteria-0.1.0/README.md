# Image Similarity Criteria

A Python package that provides various perceptual similarity metrics for comparing images using state-of-the-art models including Face Recognition Systems (FRS), CLIP, and LPIPS.

## Features

- Face Recognition System (FRS) based identity loss with multiple model options:
  - IR-152
  - IR-SE-50
  - MobileFaceNet
  - FaceNet
  - CurricularFace
- CLIP-based similarity metrics
- LPIPS (Learned Perceptual Image Patch Similarity)
- Ensemble ID loss for combining multiple FRS models

## Installation

1. Clone the repository:
```bash
git clone https://github.com/minha12/criteria.git
cd criteria
```

2. Install the package:
```bash
pip install -e .
```

## Usage

### Face Recognition System (FRS)

```python
from criteria import id_loss
from PIL import Image

# Initialize ID loss with a specific model
id_loss_fn = id_loss.IDLoss(model_name='ir_se50')

# Load images
img1 = Image.open('image1.jpg')
img2 = Image.open('image2.jpg')

# Calculate identity loss
loss = id_loss_fn(img1, img2)
```

### CLIP Similarity

```python
from criteria import clip_loss

# Initialize CLIP loss
clip_loss_fn = clip_loss.CLIPLoss()

# Calculate CLIP similarity
similarity = clip_loss_fn(img1, img2)
```

### LPIPS

```python
from criteria import lpips_loss

# Initialize LPIPS
lpips_fn = lpips_loss.LPIPSLoss()

# Calculate perceptual similarity
distance = lpips_fn(img1, img2)
```

## Model Weights

Pre-trained model weights will be automatically downloaded when initializing the respective loss functions.

## License

MIT License

## Citation

If you use this package in your research, please cite:

```bibtex
@misc{criteria2023,
  author = {Le, Minh-Ha},
  title = {Criteria: Image Similarity Metrics},
  year = {2023},
  publisher = {GitHub},
  url = {https://github.com/username/criteria}
}
```
