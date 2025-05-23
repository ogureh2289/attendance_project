from db import add_student
from generator import generate_token, create_qr_code
from smtp_service import send_qr


def create_student(full_name, student_class, email):
    token = generate_token()
    add_student(full_name, student_class, email, token)
    qr_code=create_qr_code(token)
    send_qr(email,full_name,qr_code)