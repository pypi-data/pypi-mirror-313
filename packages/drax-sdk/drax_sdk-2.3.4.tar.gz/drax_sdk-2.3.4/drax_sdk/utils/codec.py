import json

import numpy as np
from drax_ecc import crypto

from drax_sdk.model.node import State

DRAX_PUBLIC_KEY = "bb099d6dce1a953c7c5d2380815ee02ea191b39206000000ceefb3c222b480459556ce440379cef89db0ccfc04000000"


def encode_state(private_key: bytes, state: State | dict) -> bytes:
    json_data = json.dumps(state.to_dict() if isinstance(state, State) else state)
    json_data_np = np.frombuffer(json_data.encode(), dtype=np.uint8)
    private_key_np = np.frombuffer(private_key, dtype=np.uint8)
    public_key: bytes = bytes.fromhex(DRAX_PUBLIC_KEY)
    public_key_np = np.frombuffer(public_key, dtype=np.uint8)
    encrypted_data_np = crypto.sign(
        private_key_np,
        public_key_np,
        json_data_np,
    )
    encrypted_data_bytes = encrypted_data_np.tobytes()

    return encrypted_data_bytes


def decode_configuration(private_key: bytes, configuration: bytes) -> dict:
    configuration_np = np.frombuffer(configuration, dtype=np.uint8)
    private_key_np = np.frombuffer(private_key, dtype=np.uint8)
    public_key: bytes = bytes.fromhex(DRAX_PUBLIC_KEY)
    public_key_np = np.frombuffer(public_key, dtype=np.uint8)
    decrypted_data_np = crypto.unsign(
        private_key_np,
        public_key_np,
        configuration_np,
    )
    decrypted_data = decrypted_data_np.tobytes()
    return json.loads(decrypted_data)


def encode_state_in_clear(state: State) -> bytes:
    json_data = json.dumps(state.to_dict())
    return json_data.encode()
