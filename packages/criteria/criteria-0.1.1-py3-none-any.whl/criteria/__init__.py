import os
import hydra
from omegaconf import DictConfig, OmegaConf
import torch

from models import ir152, facenet, model_irse
from models.model_irse import IR_101
from utils.download import download_fr_model_weights
from utils.paths import register_resolvers 

register_resolvers()

def load_model(model_name, cfg=None):
    if cfg is None:
        cfg = OmegaConf.load("configs/config.yaml")
    if model_name == 'ir152':
        model = ir152.IR_152((112, 112))
    elif model_name == 'facenet':
        model = facenet.InceptionResnetV1()
    elif model_name == 'irse':
        model = model_irse.IR_SE_50((112, 112))
    elif model_name == "cur_face":
        model = IR_101(input_size=112)
    else:
        raise ValueError(f"Model '{model_name}' is not supported.")

    # check if weights_path is exist, if not download it
    weights_path = f'{cfg.id_loss.model_weights_dir}/{model_name}.pth'
    if not os.path.exists(weights_path):
        download_fr_model_weights(model_name, cfg)
    
    model.load_state_dict(torch.load(weights_path, map_location='cpu', weights_only=True))
    model.eval()
    return model