from db import add_student
from generator import generate_token


def create_student(full_name, student_class, email):
    token = generate_token()
    print(full_name, student_class, email, token)
    add_student(full_name, student_class, email, token)