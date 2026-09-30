"""Converting between numpy arrays and the gRPC messages (schema TODO: not written yet).

Used on both sides of the connection: the simulation packs observations and unpacks
actions; the controller server does the reverse.
"""

import numpy as np


def pack(arrays: dict[str, np.ndarray]) -> dict:
    """Turn named numpy arrays into `Array` messages (dtype, shape, raw bytes)."""
    raise NotImplementedError


def unpack(messages: dict) -> dict[str, np.ndarray]:
    """Turn `Array` messages back into named numpy arrays."""
    raise NotImplementedError
