import os

import pandas as pd
from pydantic import BaseModel
from typing import List, Optional
import logging

DRAX_PUBLIC_KEY = "bb099d6dce1a953c7c5d2380815ee02ea191b39206000000ceefb3c222b480459556ce440379cef89db0ccfc04000000"


class NodeKey(BaseModel):
    node_id: str
    private_key: bytes


class KeyStore:
    drax_public_key: bytes = bytes.fromhex(DRAX_PUBLIC_KEY)
    keys: List[NodeKey] = []

    @classmethod
    def add(cls, node_id: str, private_key: bytes):
        """
        Add a key to the keystore
        :param node_id:
        :param private_key:
        :return:
        """
        key = NodeKey(node_id=node_id, private_key=private_key)
        cls.keys.append(key)

    @classmethod
    def add_hex(cls, node_id: str, private_key_hex: str):
        """
        Add a key to the keystore from a hex string
        :param node_id:
        :param private_key_hex:
        :return:
        """
        try:
            private_key = bytes.fromhex(private_key_hex)
            cls.add(node_id, private_key)
        except Exception as e:
            logging.warning(f"Hex key error for node {node_id}", e)

    @classmethod
    def get_private_key(cls, node_id: str) -> Optional[bytes]:
        """
        Get the private key for a node
        :param node_id:
        :return:
        """
        for key in cls.keys:
            if key.node_id == node_id:
                return key.private_key

        raise ValueError(f"Node {node_id} not found in keystore")

    @classmethod
    def save(cls):
        """
        save keys in a parquet file
        """

        df = pd.DataFrame(
            [(key.node_id, key.private_key.hex()) for key in cls.keys],
            columns=["node_id", "private_key"],
        )

        keystore_path = cls._get_keystore_path()

        df.to_parquet(keystore_path)

    @classmethod
    def load(cls):
        """
        load keys from a parquet file
        """

        keystore_path = cls._get_keystore_path()

        if not os.path.exists(keystore_path):
            return

        df = pd.read_parquet(keystore_path)

        for index, row in df.iterrows():
            cls.add_hex(row["node_id"], row["private_key"])

    @classmethod
    def _get_keystore_path(cls):
        project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        keystore_path = os.path.join(project_root_path, "keystore.parquet")
        print(keystore_path)

        return keystore_path
