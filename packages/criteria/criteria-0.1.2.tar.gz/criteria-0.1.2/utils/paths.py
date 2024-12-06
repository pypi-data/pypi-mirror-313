import os
from pathlib import Path

from omegaconf import OmegaConf

def get_package_root():
    return Path(__file__).parent.parent

def get_weights_dir():
    # Default to package-level weights directory
    package_weights = get_package_root() / "weights"
    
    # Allow override via environment variable
    env_weights = os.getenv("CRITERIA_WEIGHTS_DIR")
    if env_weights:
        return Path(env_weights)
        
    # User home directory for weights
    user_weights = Path.home() / ".criteria" / "weights"
    
    # Priority:
    # 1. Environment variable if set
    # 2. User home directory if exists
    # 3. Package directory as fallback
    if user_weights.exists():
        return user_weights
    
    return str(package_weights)

def register_resolvers():
    OmegaConf.register_new_resolver("get_weights_dir", get_weights_dir)