import pandas as pd
import psycopg2


class PostgresDBOperations:
    def __init__(self, postgres_params: dict):
        """
        An instance of PostgresDBOperations is used by services that need to interact with a Postgres
        instance.
        :param postgres_params: A dictionary that must contain the following keys:
            - HOST
            - USER
            - PASSWORD
            - DATABASE
            - PORT
        :type postgres_params: dict
        """
        self.postgres_params = postgres_params

        self.host = None
        self.user = None
        self.password = None
        self.database = None
        self.port = None

        self.connection = None
        self.cursor = None

        self.notification_subscriptions = None

        self.load_params()

        self.establish_connection()
        self.establish_cursor()

        self.load_notification_subscriptions()

    def load_params(self):
        self.host = self.postgres_params.get('HOST')
        self.user = self.postgres_params.get('USER')
        self.password = self.postgres_params.get('PASSWORD')
        self.database = self.postgres_params.get('DATABASE')
        self.port = self.postgres_params.get('PORT')

    def establish_connection(self):
        self.close_everything()

        try:
            self.connection = psycopg2.connect(host=self.host, user=self.user,
                                               password=self.password, database=self.database,
                                               port=self.port)
            return
        except Exception as e:
            print(e)
            print('Cannot establish connection to postgresql. Trying again...')

        try:
            self.load_params()
            self.connection = psycopg2.connect(host=self.host, user=self.user,
                                               password=self.password, database=self.database,
                                               port=self.port)
        except Exception as e:
            print('Cannot establish connection to postgresql')
            raise e

    def establish_cursor(self):
        try:
            self.cursor = self.connection.cursor()
            return
        except Exception as e:
            print(e)
            print('Cannot establish cursor. Trying again...')

        try:
            self.establish_connection()
            self.cursor = self.connection.cursor()
        except Exception as e:
            print('Cannot establish cursor')
            raise e

    def _fetch_notification_subscriptions(self):
        self.cursor.execute("SELECT * FROM notification_subscriptions LIMIT 0;")
        notification_subscriptions_cols = [desc[0] for desc in self.cursor.description]

        self.cursor.execute("SELECT * FROM notification_subscriptions;")
        rows = self.cursor.fetchall()

        rows = pd.DataFrame(data=rows, columns=notification_subscriptions_cols)
        return rows

    def load_notification_subscriptions(self):
        try:
            self.notification_subscriptions = self._fetch_notification_subscriptions()
            return
        except Exception as e:
            print(e)
            print('Cannot load notification_subscriptions. Trying again...')

        try:
            self.establish_cursor()
            self.notification_subscriptions = self._fetch_notification_subscriptions()
            return
        except Exception as e:
            print('Cannot load notification_subscriptions')
            raise e

    def get_organization_notification_subscriptions(self, organization_id):
        print('TRYING TO GET NOTIF SUB FOR ORG:',organization_id)
        try:
            ns = self.notification_subscriptions[self.notification_subscriptions['organization_id'] == organization_id]
            if ns.empty:
                raise Exception('Empty notification_subscriptions')
            return ns['notification_subscription_id'].to_list(), ns['topic_arn'].to_list()
        except Exception as e:
            print(e)
            print('Cannot get notification_subscriptions for organization. Trying again...')

        try:
            self.load_notification_subscriptions()
            ns = self.notification_subscriptions[self.notification_subscriptions['organization_id'] == organization_id]
            return ns['notification_subscription_id'].to_list(), ns['topic_arn'].to_list()
        except Exception as e:
            print(e)
            print('Cannot get notification_subscriptions for organization. It could be empty.')
            return [], []

    def write_notifications(self, notification_content: str, notification_subscription_ids: list, organization_id: int):
        if notification_content is None or not isinstance(notification_content, str) or len(notification_content) == 0:
            return
        if notification_subscription_ids is None or not isinstance(notification_subscription_ids, list) or len(notification_subscription_ids) == 0:
            return
        if organization_id is None:
            return

        cols = ['organization_id', 'notification_subscription_id', 'notification_content', 'create_time']
        cols = '({})'.format(', '.join(cols))
        escaped_content = notification_content.replace("'", "''")

        values = [
            f"({organization_id}, {subscription_id}, '{escaped_content}', current_timestamp)"
            for subscription_id in notification_subscription_ids
        ]

        query = f"""
                INSERT INTO notifications {cols}
                VALUES {', '.join(values)};
                """.strip()
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return
        except Exception as e:
            try:
                self.connection.rollback()
            except:
                pass
            print(e)
            print('Cannot execute query for writing notifications. Trying again...')

        try:
            self.establish_cursor()
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            try:
                self.connection.rollback()
            except:
                pass
            print('Cannot execute query for writing notifications')
            raise e

    def close_cursor(self):
        try:
            self.cursor.close()
        except:
            pass

    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass

    def close_everything(self):
        self.close_cursor()
        self.close_connection()
