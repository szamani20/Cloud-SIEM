import boto3


class NotificationDispatch:
    def __init__(self):
        self.sns_client = boto3.client('sns')

    def dispatch_notifications(self, notification: str, topic_arns: list):
        """
        This method receives a notification message and a list of SNS ARNs and will send the message to each topic ARN
        :param notification: The message to dispatch as notification
        :type notification: str
        :param topic_arns: A list of AWS SNS Topic ARNs that are representing clients' notification subscriptions
        :type topic_arns: list
        """
        for topic_arn in topic_arns:
            self.sns_client.publish(
                TopicArn=topic_arn,
                Subject="Security Alert: Unauthorized Access Attempt Detected",
                Message=notification
            )
