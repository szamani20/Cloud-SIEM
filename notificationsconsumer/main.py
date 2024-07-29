from config.postgresql.parameters import PostgreSQLParams
from config.rabbitmq.parameters import RabbitMQParams
from messaging.rabbitmq.consumer import RabbitMQConsumer
from notification.sns.notification_dispatch import NotificationDispatch
import threading

from storage.postgres.db_operations import PostgresDBOperations
from utils.helpers import extract_organization_from_message


def main():
    # notification_rabbitmq_consumer consumes notifications to be sent from notifications_exchange
    notification_rabbitmq_consumer = RabbitMQConsumer(RabbitMQParams.NOTIFICATIONS_RABBITMQ)

    # notification_subscription_rabbitmq_consumer consumes messages about change in notification_subscription changes from notifications_subscription_exchange
    notification_subscription_rabbitmq_consumer = RabbitMQConsumer(RabbitMQParams.NOTIFICATIONS_SUBSCRIPTION_RABBITMQ)

    # notification_dispatch_client is a simple SNS client used to send SNS notifications
    notification_dispatch_client = NotificationDispatch()

    # notification_postgres_client is used to store a log of sent out notifications for future references
    notification_postgres_client = PostgresDBOperations(PostgreSQLParams.NOTIFICATION_SUBSCRIPTION_POSTGRES)

    def start_consumer(consumer, callback):
        consumer.consume(callback=callback)

    def dispatch_notifications(notification, organization_topic_arns, notification_subscription_ids, organization_id):
        # First dispatch the notifications
        notification_dispatch_client.dispatch_notifications(notification=notification, topic_arns=organization_topic_arns)

        # Then write a copy to the DB
        notification_postgres_client.write_notifications(notification_content=notification,
                                                         notification_subscription_ids=notification_subscription_ids,
                                                         organization_id=organization_id)

    def callback(ch, method, properties, body):
        # When a new notification is supposed to be sent, this function is used to extract the organization_id to which the notification content should be sent
        notification, organization_id = extract_organization_from_message(body)

        # The organization_id is then used to fetch the notification subscriptions (SNS Topic ARNs) associated with the particular organization
        notification_subscription_ids, organization_topic_arns = notification_postgres_client.get_organization_notification_subscriptions(
            organization_id=organization_id)

        # Once we have the notification subscription info (SNS Topic ARNs) and the notification content, we dispatch notification to all subscribers
        threading.Thread(target=dispatch_notifications, args=(notification, organization_topic_arns,
                                                              notification_subscription_ids, organization_id)).start()

        print('Finished dispatching notifications!', organization_id)

    def ns_callback(ch, method, properties, body):
        try:
            print('Before: ', notification_postgres_client.notification_subscriptions.shape)
            notification_postgres_client.load_notification_subscriptions()
            print('Before: ', notification_postgres_client.notification_subscriptions.shape)
        except Exception as e:
            print('Failed to load_notification_subscriptions:\n', e)

    # Start consuming messages
    thread1 = threading.Thread(target=start_consumer, args=(notification_rabbitmq_consumer, callback))
    thread2 = threading.Thread(target=start_consumer, args=(notification_subscription_rabbitmq_consumer, ns_callback))

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
