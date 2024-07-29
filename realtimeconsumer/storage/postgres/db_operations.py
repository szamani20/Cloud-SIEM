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
        self.rules = None

        self.load_params()

        self.establish_connection()
        self.establish_cursor()

        self.load_organizations()
        self.load_rules()

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

    def _fetch_rules(self):
        self.cursor.execute("SELECT * FROM rules LIMIT 0;")
        rules_cols = [desc[0] for desc in self.cursor.description]

        self.cursor.execute("SELECT * FROM rules;")
        rows = self.cursor.fetchall()

        rows = pd.DataFrame(data=rows, columns=rules_cols)

        rows['rule_content'] = rows['rule_content'].apply(json.dumps)
        return rows

    def load_rules(self):
        try:
            self.rules = self._fetch_rules()
            return
        except Exception as e:
            print(e)
            print('Cannot load rules. Trying again...')

        try:
            self.establish_cursor()
            self.rules = self._fetch_rules()
        except Exception as e:
            print('Cannot load rules')
            raise e

    def get_organization_id(self, organization_name):
        organization_id = None
        try:
            organization_id = \
                self.organizations[self.organizations['organization_name'] == organization_name]['organization_id'].to_list()[0]
        except Exception as e:
            self.load_organizations()
            organization_id = \
                self.organizations[self.organizations['organization_name'] == organization_name]['organization_id'].to_list()[0]
        finally:
            if organization_id is None:
                print(f'Cannot retrieve organization_id for {organization_name}')
        return organization_id

    def get_organization_rules(self, organization_id):
        try:
            return self.rules[self.rules['organization_id'] == organization_id].reset_index(drop=True)
        except Exception as e:
            print(e)
            print('Cannot get organization_id from rules. Trying again...')

        try:
            self.load_organizations()
            self.load_rules()
            return self.rules[self.rules['organization_id'] == organization_id].reset_index(drop=True)
        except Exception as e:
            return pd.DataFrame()

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
