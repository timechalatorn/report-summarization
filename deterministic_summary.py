import torch
import numpy as np
import random
import os

def set_deterministic(enable=True, seed=42):
    if not enable:
        return
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":16:8"
    torch.use_deterministic_algorithms(True, warn_only=True)
