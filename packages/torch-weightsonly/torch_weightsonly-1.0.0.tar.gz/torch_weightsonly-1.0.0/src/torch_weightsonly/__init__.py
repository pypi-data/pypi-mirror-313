from functools import partial

import torch as _torch  # Import the actual torch module

# Replace `torch.load` with a partial that enforces weights_only=True
_torch.load = partial(_torch.load, weights_only=True)

# Restore the original name for proper introspection
_torch.load.__name__ = _torch.load.__name__

# Re-export everything from torch
from torch import *  # noqa
