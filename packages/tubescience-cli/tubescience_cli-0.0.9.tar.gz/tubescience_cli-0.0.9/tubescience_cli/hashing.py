from dataclasses import  fields, is_dataclass
from typing import Any
import hashlib
from collections import OrderedDict


class MerkleNode:
    def __init__(self, value: Any = None):
        self.value = value
        self.hash = None
        self.children = OrderedDict()

    def add_child(self, key: str, node: 'MerkleNode'):
        self.children[key] = node

    def compute_hash(self) -> str:
        if not self.children:
            # Leaf node - hash the value directly
            return hashlib.sha1(str(self.value).encode('utf-8')).hexdigest()
        
        # Internal node - combine child hashes
        child_hashes = []
        for key, child in self.children.items():
            child_hash = child.compute_hash()
            child_hashes.append(f"{key}:{child_hash}")
        
        combined = "|".join(sorted(child_hashes))
        return hashlib.sha1(combined.encode('utf-8')).hexdigest()


def build_merkle_tree(obj: Any) -> MerkleNode:
    """Build a Merkle tree from a dataclass instance."""
    
    def _process_value(val: Any) -> MerkleNode:
        node = MerkleNode()
        
        if val is None:
            node.value = "None"
            return node
            
        elif isinstance(val, (int, float, str, bool)):
            node.value = str(val)
            return node
            
        elif isinstance(val, (list, tuple)):
            for i, item in enumerate(val):
                child = _process_value(item)
                node.add_child(f"[{i}]", child)
            return node
            
        elif isinstance(val, set):
            for i, item in enumerate(sorted(val, key=str)):
                child = _process_value(item)
                node.add_child(f"{{{i}}}", child)
            return node
            
        elif isinstance(val, dict):
            for key in sorted(val.keys()):
                child = _process_value(val[key])
                node.add_child(str(key), child)
            return node
            
        elif is_dataclass(val):
            for f in fields(val):
                field_value = getattr(val, f.name)
                child = _process_value(field_value)
                node.add_child(f.name, child)
            return node
            
        else:
            node.value = str(val)
            return node
    
    return _process_value(obj)


def deterministic_hash(obj: Any) -> str:
    """
    Generate a deterministic hash for any dataclass instance using a Merkle tree.
    Returns a hex string representation of the SHA-1 hash.
    """
    merkle_tree = build_merkle_tree(obj)
    return merkle_tree.compute_hash()
