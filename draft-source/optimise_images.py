"""Create responsive web derivatives; keep uploaded originals untouched.
Optional asset-preparation command: python draft-source/optimise_images.py
Requires Pillow. Normal builds use the committed derivatives and need no Pillow.
"""
from pathlib import Path
from PIL import Image, ImageOps
root=Path(__file__).resolve().parent.parent
for name in ['founder-hero','founder-professional']:
    with Image.open(root/'assets'/f'{name}.jpg') as image:
        image=ImageOps.exif_transpose(image).convert('RGB')
        for width in [480,960,1440]:
            height=round(image.height*width/image.width)
            image.resize((width,height),Image.Resampling.LANCZOS).save(root/'assets'/f'{name}-{width}.webp','WEBP',quality=88,method=6)
            print(name,width,(root/'assets'/f'{name}-{width}.webp').stat().st_size)
