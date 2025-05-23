import smtplib
from email.message import EmailMessage
SMTP_PASSWORD = 'khftzlbeedmtibbq'
SMTP_EMAIL = 'an1sinser@yandex.ru'
SMTP_SERVER = 'smtp.yandex.ru'
SMTP_PORT = 587

def send_qr(emal:str, fio: str, qr_bytes):
    message=EmailMessage()
    message['Subject']='Qr для программы посещямости'
    message['From']=SMTP_EMAIL
    message["To"]=emal
    message.set_content(f'Здравствуйте!\n {fio}, '
                        f'во вложении вы найдете персональный QR-код для '
                        f'подтверждения посещаемости на уроке.\n ')

    message.add_attachment(qr_bytes.read(), maintype="image", subtype='png', filename=f'{fio}_qr.png')

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            server.send_message(message)
    except Exception as e:
        print(e)