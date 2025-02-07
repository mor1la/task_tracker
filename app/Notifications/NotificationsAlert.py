import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI

app = FastAPI()

# Конфигурация для SMTP-сервера Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_LOGIN = "yuraserb05@gmail.com"
SMTP_PASSWORD = "wyea hqob lhxl kwlm"  # Замените на сгенерированный пароль приложения


def send_email(to_email: str, subject: str, plain_message: str, html_message: str):
    try:
        # Создаем объект сообщения
        msg = MIMEMultipart("alternative")
        msg["From"] = SMTP_LOGIN
        msg["To"] = to_email
        msg["Subject"] = subject

        # Создаем текстовую и HTML-часть письма
        part1 = MIMEText(plain_message, "plain")
        part2 = MIMEText(html_message, "html")

        # Добавляем обе части к сообщению
        msg.attach(part1)
        msg.attach(part2)

        # Подключаемся к SMTP-серверу и отправляем письмо
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Защищаем соединение
        server.login(SMTP_LOGIN, SMTP_PASSWORD)
        server.sendmail(SMTP_LOGIN, to_email, msg.as_string())
        server.quit()

        return {"message": f"Email sent to {to_email}"}

    except Exception as e:
        return {"error": str(e)}


@app.post("/send-email/")
async def send_email_notification(to_email: str, subject: str, plain_message: str, html_message: str):
    response = send_email(to_email, subject, plain_message, html_message)
    return response
