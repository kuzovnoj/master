from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def compress_image(image_field, max_width=1920, max_height=1920, quality=85):
    if not image_field or not image_field.name:
        return

    img = Image.open(image_field)
    img = img.convert('RGB')

    original_width, original_height = img.size
    if original_width > max_width or original_height > max_height:
        ratio = min(max_width / original_width, max_height / original_height)
        new_size = (int(original_width * ratio), int(original_height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    ext = image_field.name.lower()
    save_format = 'PNG' if ext.endswith('.png') else 'JPEG'

    buffer = BytesIO()
    img.save(buffer, format=save_format, quality=quality, optimize=True)

    image_field.save(image_field.name, ContentFile(buffer.getvalue()), save=False)
