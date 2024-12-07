from typing import Optional, List
from dataclasses import dataclass


@dataclass
class Layer:
    layer_type: int  # The layer type (e.g., 0, 2)
    name: str  # Name of the layer
    left: int  # Left coordinate
    top: int  # Top coordinate
    width: int  # Width of the layer
    height: int  # Height of the layer
    type: int  # Type of the layer
    opacity: int  # Opacity value (0–255)
    visible: int  # Visibility flag (0 or 1)
    layer_id: int  # Unique ID of the layer
    group_layer_id: Optional[int]  # ID of the parent group layer (use -1 if no group)
    base: Optional[int]  # Additional base information (use -1 if no value)
    images: Optional[str]  # Image-related data (use an empty string if no value)


@dataclass
class ParseResult:
    dresses: List[str]
    faces: List[str]
    info_type: str
