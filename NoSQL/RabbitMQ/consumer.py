import os
from dotenv import load_dotenv
import pika
import mongoengine as me
from contact_model import Contact

load_dotenv()

MONGO_USER = os.getenv('MONGO_USER')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
MONGO_HOST = os.getenv('MONGO_HOST')

me.connect('contacts_db', host=f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/contacts_db?retryWrites=true&w=majority')

# Подключение к RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.queue_declare(queue='email_queue')


def send_email(contact):
    # Имитация отправки email
    print(f"Sending email to {contact.email}")
    return True


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects(id=contact_id).first()
    if contact:
        if send_email(contact):
            contact.message_sent = True
            contact.save()
            print(f" [x] Email sent to {contact.fullname}")


# Follow the white rabbit
channel.basic_consume(queue='email_queue', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
