import pika


class RabbitMQProducer:
    def __init__(self, rabbitmq_params: dict):
        """
        An instance of RabbitMQProducer is used by services that need to write a message to a RabbitMQ
        instance. Producers are abstracted away from the details of consumption side.
        :param rabbitmq_params: A dictionary that must contain the following keys:
            - HOST
            - USERNAME
            - PASSWORD
            - EXCHANGE
            - EXCHANGE_TYPE
        and in case the EXCHANGE_TYPE is not fanout, then for more robustness in case the consumer may have
        not started execution yet, the producer is supposed to define a queue and routing_key as well.
        If the EXCHANGE_TYPE is fanout, then the producer does not need to define queue or routing_key
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

        self.load_params()
        self.establish_connection()
        self.establish_channel()

        # It doesn't hurt to declare a queue when dealing with direct exchanges
        if self.exchange_type == 'direct':
            self.establish_queue()

    def load_params(self):
        host_url = self.rabbitmq_params.get('HOST')
        username = self.rabbitmq_params.get('USERNAME')
        password = self.rabbitmq_params.get('PASSWORD')

        self.params = pika.URLParameters(host_url)
        self.params.credentials = pika.PlainCredentials(username, password)

        self.exchange = self.rabbitmq_params.get('EXCHANGE')
        self.exchange_type = self.rabbitmq_params.get('EXCHANGE_TYPE')

        self.routing_key = self.rabbitmq_params.get('ROUTING_KEY', '')
        self.queue_name = self.rabbitmq_params.get('QUEUE_NAME', '')

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

    # We don't need the queue, outside of this method's namespace, we only need to declare it once. Hence, local variable
    def establish_queue(self):
        try:
            queue = self.channel.queue_declare(queue=self.queue_name, exclusive=False)
            self.channel.queue_bind(exchange=self.exchange, queue=queue.method.queue, routing_key=self.routing_key)
            return
        except Exception as e:
            print(e)
            print('Cannot establish queue to rabbitmq. Trying again...')

        try:
            self.establish_channel()
            queue = self.channel.queue_declare(queue=self.queue_name, exclusive=False)
            self.channel.queue_bind(exchange=self.exchange, queue=queue.method.queue, routing_key=self.routing_key)
        except Exception as e:
            print('Cannot establish queue to rabbitmq')
            raise e

    def publish_message(self, message):
        try:
            self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=message)
            return 'OK', 200
        except Exception as e:
            print(e)
            print('Cannot publish message to rabbitmq. Trying again...')

        try:
            self.establish_channel()
            self.channel.basic_publish(exchange=self.exchange, routing_key=self.routing_key, body=message)
            return 'OK', 200
        except Exception as e:
            print(e)
            print('Cannot publish message to rabbitmq')
            return 'Error', 500

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
