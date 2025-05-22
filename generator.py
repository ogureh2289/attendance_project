import uuid
from io import BytesIO
import PIL

import qrcode


def generate_token():
    return str(uuid.uuid4())


def create_qr_code(token):
    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(token)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    # Сохраним QR в байтах, чтобы потом вложить в письмо
    bio = BytesIO()
    img.save("qr.png")
    img.save(bio)
    bio.seek(0)
    return bio
