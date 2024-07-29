import json

import pandas as pd
from datetime import datetime, timezone, timedelta

pd.set_option('display.max_columns', None)


# pd.set_option('display.max_rows', None)


def extract_organization_from_message(message):
    message = json.loads(message)
    # This is just a username, not the actual organization_id in the DB
    organization = message['organization']
    return message, organization


def process_message(message: dict, organization_rules: pd.DataFrame):
    """
    This method should be more sophisticated. Its job is to process a log (message) according to all the rules
    defined by the organization to determine whether a notification is warranted or not.

    The current implementation simply checks for simple user based rules. More complex rules require more complex processing

    :param message: An actual AWS log coming from client's AWS
    :type message: dict
    :param organization_rules: Client defined rules for their organization
    :type organization_rules: pd.DataFrame
    :return:
    :rtype:
    """
    try:
        organization_rules = organization_rules[organization_rules['rule_type'] == 'USER_BASED']['rule_content']
        organization_rules = [json.loads(organization_rule) for organization_rule in organization_rules]
        username = message['userIdentity']['userName']
        region = message['awsRegion']
        accountId = message['userIdentity']['accountId']
        sourceIPAddress = message['sourceIPAddress']
        event_time = message['eventTime']
        try:
            timestamp_utc = datetime.fromisoformat(event_time[:-1])
            timestamp_est = timestamp_utc.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-5)))
            est_time_str = timestamp_est.strftime('%Y-%m-%d %H:%M:%S %Z')
        except:
            est_time_str = event_time

        for organization_rule in organization_rules:
            if username == organization_rule['user']:
                text_body = f"""
                            Security Alert
            
                            Dear Team,
            
                            We have detected an unauthorized access attempt with the following details:
            
                            User: {username}
                            IP Address: {sourceIPAddress}
                            Action: {message["eventName"]}
                            Resource: {message["eventSource"]}
                            Region: {region}
                            Account ID: {accountId}
                            Time: {est_time_str}
            
                            Please take the necessary actions to investigate this incident.
            
                            Best regards,
                            Your Security Team
                            """
                return True, text_body
        return False, None
    except Exception as e:
        raise e
