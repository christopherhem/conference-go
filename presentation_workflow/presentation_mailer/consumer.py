import json
import pika
from pika.exceptions import AMQPConnectionError
import django
import os
import sys
import time
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()

while True:
    try:

        def process_approval_message(ch, method, properties, body):
            content = json.loads(body)
            print("I APPROVED YOU!")
            send_mail(
                subject="Wahoo! Presentation Approved!",
                message=f"Congratulations {content['presenter_name']}! Your {content['title']} presentation has been approved!",
                from_email="staff@conference-go.com",
                recipient_list=[f"{content['presenter_email']}"],
                fail_silently=False,
            )

        def process_rejected_message(ch, method, properties, body):
            content = json.loads(body)
            print("I REJECTED YOU!")
            send_mail(
                subject="Sorry, we have rejected your presentation...",
                message=f"Unfortunately {content['presenter_name']}, Your {content['title']} presentation has been rejected...",
                from_email="staff@conference-go.com",
                recipient_list=[f"{content['presenter_email']}"],
            )

        parameters = pika.ConnectionParameters(host="rabbitmq")
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue="presentation_approvals")
        channel.basic_consume(
            queue="presentation_approvals",
            on_message_callback=process_approval_message,
            auto_ack=True,
        )

        channel.queue_declare(queue="presentation_rejections")
        channel.basic_consume(
            queue="presentation_rejections",
            on_message_callback=process_rejected_message,
            auto_ack=True,
        )
        channel.start_consuming()
    except AMQPConnectionError:
        print("Could not connect to RabbitMQ")
        time.sleep(2.0)
