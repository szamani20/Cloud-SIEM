import time

import pika


class RabbitMQConsumer:
    def __init__(self, rabbitmq_params: dict):
        """
        An instance of RabbitMQConsumer is used by services that need to consume messages from a RabbitMQ
        instance. Consumers are abstracted away from the details of production side.
        :param rabbitmq_params: A dictionary that must contain the following keys:
            - HOST
            - USERNAME
            - PASSWORD
            - EXCHANGE
            - EXCHANGE_TYPE
            - QUEUE_NAME
        and in case the EXCHANGE_TYPE is fanout, then the consumer is not supposed to define a ROUTING_KEY
        :type rabbitmq_params: dict
        """
        self.rabbitmq_params = rabbitmq_params

        self.params = None
        self.exchange = None
        self.routing_key = None
        self.exchange_type = None
        self.queue_name = None
        self.connection = None
        self.channel = None
        self.queue = None

        self.load_params()
        self.establish_connection()
        self.establish_channel()
        self.establish_queue()

    def load_params(self):
        host_url = self.rabbitmq_params.get('HOST')
        username = self.rabbitmq_params.get('USERNAME')
        password = self.rabbitmq_params.get('PASSWORD')

        self.params = pika.URLParameters(host_url)
        self.params.credentials = pika.PlainCredentials(username, password)

        self.exchange = self.rabbitmq_params.get('EXCHANGE')
        self.exchange_type = self.rabbitmq_params.get('EXCHANGE_TYPE')
        self.queue_name = self.rabbitmq_params.get('QUEUE_NAME')

        # If exchange_type='fanout', then a routing_key is not needed.
        self.routing_key = self.rabbitmq_params.get('ROUTING_KEY', '')

    def establish_connection(self):
        self.close_everything()

        try:
            self.connection = pika.BlockingConnection(self.params)
            return
        except Exception as e:
            print(e)
            print('Cannot establish connection to rabbitmq. Trying again...')

        try:
            self.load_params()
            self.connection = pika.BlockingConnection(self.params)
        except Exception as e:
            print('Cannot establish connection to rabbitmq')
            raise e

    def establish_channel(self):
        try:
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
            return
        except Exception as e:
            print(e)
            print('Cannot establish channel to rabbitmq. Trying again...')

        try:
            self.establish_connection()
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
        except Exception as e:
            print('Cannot establish channel to rabbitmq')
            raise e

    def establish_queue(self):
        try:
            self.queue = self.channel.queue_declare(queue=self.queue_name, exclusive=False)
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue.method.queue, routing_key=self.routing_key)
            return
        except Exception as e:
            print(e)
            print('Cannot establish queue to rabbitmq. Trying again...')

        try:
            self.establish_channel()
            self.queue = self.channel.queue_declare(queue=self.queue_name, exclusive=False)
            self.channel.queue_bind(exchange=self.exchange, queue=self.queue.method.queue, routing_key=self.routing_key)
        except Exception as e:
            print('Cannot establish queue to rabbitmq')
            raise e

    def consume(self, callback):
        while True:
            try:
                self.channel.basic_consume(queue=self.queue.method.queue, on_message_callback=callback, auto_ack=True)
                self.channel.start_consuming()
            except Exception as e:
                print(e)
                print('Cannot consume from rabbitmq. Trying again...')
                time.sleep(3)
                self.establish_queue()

    def close_channel(self):
        try:
            self.channel.close()
        except:
            pass

    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass

    def close_everything(self):
        self.close_channel()
        self.close_connection()
