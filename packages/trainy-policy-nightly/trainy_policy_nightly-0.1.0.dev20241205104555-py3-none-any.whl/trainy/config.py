import os
from typing import Any, Dict

import sky

CONFIG_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "configs")


def load_config(config_name: str) -> Dict[str, Any]:
    config_path = os.path.join(CONFIG_DIR, "gke.yaml")
    config = sky.utils.common_utils.read_yaml(config_path)
    return config
