"""Pillow filteri nad jednom rasterskom slikom."""
from io import BytesIO
from pathlib import Path
from typing import Literal

from PIL import Image, ImageChops, ImageFilter, ImageMath, ImageOps

FilterName = Literal["grayscale", "invert", "pixelate", "blur", "derivative"]

PIXEL_SIZE = 12
BLUR_RADIUS = 4
SAVE_OPTIONS = {
    "JPEG": {"quality": 95},
    "TIFF": {"compression": "tiff_deflate"},
    "WEBP": {"lossless": True},
}

class MultiFrameImage(ValueError):
    pass

def working_image(image: Image.Image) -> Image.Image:
    if image.mode.startswith("I;16"):
        transparent=image.info.get("transparency")
        gray = image.point(lambda value: value * (255 / 65535)).convert("L") # '/' is true division
        if transparent is not None:
            alpha = ImageMath.lamba_eval(
                lambda args: (args["pixels"] != transparent) * 255,
                pixels=image.convert("I"),
            ).convert("L")
            gray = gray.convert("RGB")
            gray.putalpha(alpha)
        image = gray
    elif image.has_transparency_data:
        image = image.convert("RGBA")
    elif image.mode not in ("L", "RGB"):
        image = image.convert("RGB")
    image.info.clear()
    return image

def derivative(image: Image.Image) -> Image.Image:
    gray = ImageOps.grayscale(image)
    dx = ImageChops.difference(gray, ImageChops.offset(gray, -1, 0))
    dy = ImageChops.difference(gray, ImageChops.offset(gray, 0, -1))
    width, height = gray.size
    dx.paste(0, (width - 1, 0, width, height))
    dy.paste(0, (0, height - 1, width, height))
    return ImageChops.lighter(dx, dy)

def apply_filter(image: Image.Image, name: FilterName) -> Image.Image:
    if name == "pixelate":
        width, height = image.size
        small_size = ((width + PIXEL_SIZE - 1) // PIXEL_SIZE,
                      (height + PIXEL_SIZE - 1) // PIXEL_SIZE)
        small = image.resize(small_size, Image.Resampling.BOX)
        return small.resize(image.size, Image.Resampling.NEAREST)
    if name == "blur":
        blur = ImageFilter.GaussianBlur(BLUR_RADIUS)
        if image.mode == "RGBA":
            return image.convert("RGBa").filter(blur).convert("RGBA")
        return image.filter(blur)
    
    colors = image.convert("RGB") if image.mode == "RGBA" else image
    if name == "grayscale":
        result = ImageOps.grayscale(colors)
    elif name == "invert":
        result = ImageOps.invert(colors)
    elif name == "derivative":
        result = derivative(colors)
    else: 
        raise ValueError(f"Nepoznat filtar: {name}")
    
    if image.mode == "RGBA":
        result = result.convert("RGB")
        result.putalpha(image.getchannel("A"))
    return result

def render_filters(path: Path, filters: list[FilterName], *, preview: bool) -> bytes:
    with Image.open(path) as source:
        if getattr(source, "n_frames", 1) > 1:
            raise MultiFrameImage("Filtri podrzavaju slike s jednim kadrom ili stranicom.")
        output_format = "PNG" if preview and source.format == "TIFF" else source.format
        image = working_image(ImageOps.exif_transpose(source))
        
    for name in filters:
        image = apply_filter(image, name)
        
    with BytesIO() as output:
        image.save(output, format=output_format, **SAVE_OPTIONS.get(output_format, {}))
        return output.getvalue()
