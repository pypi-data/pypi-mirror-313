import os
import gdown
import hydra
from omegaconf import DictConfig

def download_fr_model_weights(model_name, cfg: DictConfig):
    weights_dir = os.path.expanduser(cfg.id_loss.model_weights_dir)
    os.makedirs(weights_dir, exist_ok=True)
    weights_path = os.path.join(weights_dir, f'{model_name}.pth')

    if not os.path.exists(weights_path):
        gdrive_urls = {
            "cur_face": "https://drive.google.com/uc?id=1eYohkbi8WXEusDFKRs4ZEp3HOiHLKW_D",
            "facenet": "https://drive.google.com/uc?id=1hZ27WlRuCrl7kJo9doOxypaXJcGCQld2",
            "ir152": "https://drive.google.com/uc?id=1_Lb3ElnWu7SL-Fh_yknXSAIA7S2l4iYn",
            "irse50": "https://drive.google.com/uc?id=1bjHgpn6o99CSrXT4-DH0lO283sRJMPHN",
            "mobile_face": "https://drive.google.com/uc?id=1FnkXR0Wv8YqCzJ9FYpprv2Xi4m_wmNhK",
        }
        url = gdrive_urls.get(model_name)
        if url is None:
            raise ValueError(f"No download URL for model '{model_name}'")

        print(f"Downloading weights for '{model_name}'...")
        gdown.download(url, weights_path, quiet=False)