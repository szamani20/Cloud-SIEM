import json

from config.postgresql.parameters import PostgreSQLParams
from config.rabbitmq.parameters import RabbitMQParams
from messaging.rabbitmq.consumer import RabbitMQConsumer
from messaging.rabbitmq.producer import RabbitMQProducer
from storage.postgres.db_operations import PostgresDBOperations
from utils.helpers import extract_organization_from_message, process_message
import threading


def main():
    # logs_rabbitmq_consumer consumes logs from a fanout exchange produced by logs_fanout_exchange
    logs_rabbitmq_consumer = RabbitMQConsumer(RabbitMQParams.LOGS_RABBITMQ)

    # rules_change_rabbitmq_consumer consumes events of rule change produced by rules_exchange
    rules_change_rabbitmq_consumer = RabbitMQConsumer(RabbitMQParams.RULES_CHANGE_RABBITMQ)

    # notifications_rabbitmq_producer produces notifications into a RabbitMQ that will be consumed by a dedicated notification processor
    notifications_rabbitmq_producer = RabbitMQProducer(RabbitMQParams.NOTIFICATIONS_RABBITMQ)

    # postgres_read_client is used to load rules and notifications subscriptions from the Postgres DB
    postgres_read_client = PostgresDBOperations(PostgreSQLParams.RULES_POSTGRES)

    def start_consumer(consumer, callback):
        consumer.consume(callback=callback)

    def handle_rabbitmq_publish(notification, organization_id):
        # Include the organization_id with the notification message to be produced to RabbitMQ
        message = json.dumps({'organization_id': organization_id, 'message': notification})

        # Publish the message to notifications_exchange on RabbitMQ
        notifications_rabbitmq_producer.publish_message(message)

    def rules_change_callback(ch, method, properties, body):
        # When a message comes in indicating that there was a change in the client defined rules for their
        # organization, we must update our local cache
        try:
            print('Before: ', postgres_read_client.rules.shape)
            postgres_read_client.load_rules()
            print('Before: ', postgres_read_client.rules.shape)
        except Exception as e:
            print('Failed to load_rules:\n', e)

    def callback(ch, method, properties, body):
        # When a new log comes in, extract the log content as well as the organization_name from it
        message, organization = extract_organization_from_message(body)

        # Using organization_name, we use postgres client to extract the organization_id
        organization_id = postgres_read_client.get_organization_id(organization_name=organization)

        # Once we have the organization_id, we need to fetch the rules from postgres
        organization_rules = postgres_read_client.get_organization_rules(organization_id=organization_id)

        # Once we got the log and the rules, we need to process the log according to rules to determine if it warrants a notification
        should_notify, notification = process_message(message, organization_rules)

        # In case a notification is warranted, we need to publish one using AWS SNS topics defined in our Postgres DB for that particular organization
        if should_notify:
            threading.Thread(target=handle_rabbitmq_publish, args=(notification, organization_id)).start()
        print('Finished processing Message!', organization)

    # Start consuming messages
    thread1 = threading.Thread(target=start_consumer, args=(logs_rabbitmq_consumer, callback))
    thread2 = threading.Thread(target=start_consumer, args=(rules_change_rabbitmq_consumer, rules_change_callback))

    thread1.start()
    thread2.start()

    # Optionally, join the threads if you need to wait for them to finish
    thread1.join()
    thread2.join()


if __name__ == "__main__":
    # if ENVIRONMENT == 'development':
    #     print("Running in development mode")
    # else:
    #     print("Running in production mode")

    main()
