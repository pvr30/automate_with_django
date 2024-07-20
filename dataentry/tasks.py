import time
from awd_main.celery import app
from django.core.management import call_command
from django.conf import settings
from .utils import send_email_notification


@app.task
def celery_test_task():
    time.sleep(10)
    mail_subject = "Test Subject"
    message = "This is a test email"
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)
    return "Email sent successfully."


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as ex:
        raise ex

    mail_subject = "Import Data Completed."
    message = "Your data import has been successful."
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject, message, to_email)

    return "Data imported successfully."
