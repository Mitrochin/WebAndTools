import os
from dotenv import load_dotenv
import pika
import mongoengine as me
from faker import Faker
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

fake = Faker()


def create_contacts(n):
    contacts = []
    for _ in range(n):
        contact = Contact(
            fullname=fake.name(),
            email=fake.email(),
            additional_info=fake.text()
        )
        contact.save()
        contacts.append(contact)
    return contacts


def main():
    contacts = create_contacts(10)

    for contact in contacts:
        message = str(contact.id)
        channel.basic_publish(exchange='', routing_key='email_queue', body=message.encode())
        print(f" [x] Sent {message}")

    connection.close()


if __name__ == '__main__':
    main()


