import re
from PIL import Image
from pathlib import Path
from typing import List, Tuple

from .models import Layer


def draw(layers: List[Layer], layer_type: str, base_path: Path) -> Image.Image:
    data: List[Tuple[Image.Image, Layer]] = []
    files = list(base_path.glob(f"*{layer_type}_*.png"))
    for layer in layers:
        available_files = [
            file
            for file in files
            if re.search(rf"^.+{layer_type}_{layer.layer_id}.png$", file.name)
        ]
        if not available_files:
            print(f"Layer {layer.name}:{layer.layer_id} not found, skipping")
            continue
        image_path = available_files[0]
        layer_image = Image.open(image_path)
        data.append((layer_image, layer))

    # Find biggest layer to create background
    max_width = max([layer.width + layer.left for _, layer in data])
    max_height = max([layer.height + layer.top for _, layer in data])

    canvas = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))

    for layer_image, layer in data:
        temp = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        # Adjust opacity
        alpha = layer_image.split()[3].point(lambda p: p * layer.opacity / 255)
        layer_image.putalpha(alpha)
        temp.paste(layer_image, (layer.left, layer.top))
        canvas = Image.alpha_composite(canvas, temp)

    # Cut the empty space
    canvas = canvas.crop(canvas.getbbox())

    return canvas
