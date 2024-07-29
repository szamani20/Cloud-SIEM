import json

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

        self.organizations = None

        self.cols = '(organization_id, log_content, create_time)'

        self.load_params()

        self.establish_connection()
        self.establish_cursor()

        self.load_organizations()

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

    def write_logs(self, logs, organization_name):
        organization_id = None
        try:
            organization_id = self.organizations[self.organizations['organization_name']==organization_name]['organization_id'].to_list()[0]
        except Exception as e:
            self.load_organizations()
            organization_id = self.organizations[self.organizations['organization_name'] == organization_name]['organization_id'].to_list()[0]
        finally:
            if organization_id is None:
                print(f'Cannot retrieve organization_id for {organization_name}')
                return

        logs = json.dumps(logs)
        values = (organization_id, logs)

        query = '''
                INSERT INTO logs {} VALUES (%s, %s, current_timestamp);
                '''.format(self.cols).strip()
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return
        except Exception as e:
            print(e)
            print('Cannot execute query for writing logs. Trying again...')

        try:
            self.establish_cursor()
            self.cursor.execute(query, values)
            self.connection.commit()
        except Exception as e:
            print('Cannot execute query for writing logs')
            raise e

    def load_organizations(self):
        query = '''
                SELECT organization_id, organization_name, organization_account_id
                FROM organizations;
                '''

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.organizations = pd.DataFrame(data=rows, columns=['organization_id',
                                                              'organization_name',
                                                              'organization_account_id'])

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
