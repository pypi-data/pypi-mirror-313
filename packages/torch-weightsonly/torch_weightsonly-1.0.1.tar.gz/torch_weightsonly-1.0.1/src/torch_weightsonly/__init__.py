from functools import partial

import torch as _torch  # Import the actual torch module

old_name = _torch.load.__name__

# Replace `torch.load` with a partial that enforces weights_only=True
_torch.load = partial(_torch.load, weights_only=True)

# Restore the original name for proper introspection
_torch.load.__name__ = old_name

del old_name

# Re-export everything from torch
from torch import *  # noqa
