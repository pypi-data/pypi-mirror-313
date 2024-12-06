from mdps_ds_lib.lib.aws.aws_cred import AwsCred


class AwsSns(AwsCred):
    def __init__(self):
        super().__init__()
        self.__sns_client = self.get_client('sns')
        self.__topic_arn = ''

    def set_topic_arn(self, topic_arn):
        self.__topic_arn = topic_arn
        return self

    def publish_message(self, msg_str: str):
        if self.__topic_arn == '':
            raise ValueError('missing topic arn to publish message')
        response = self.__sns_client.publish(
            TopicArn=self.__topic_arn,
            # TargetArn='string',  # not needed coz of we are using topic arn
            # PhoneNumber='string',  # not needed coz of we are using topic arn
            Message=msg_str,
            # Subject='optional string',
            # MessageStructure='string',
            # MessageAttributes={
            #     'string': {
            #         'DataType': 'string',
            #         'StringValue': 'string',
            #         'BinaryValue': b'bytes'
            #     }
            # },
            # MessageDeduplicationId='string',
            # MessageGroupId='string'
        )
        return response

    def create_sqs_subscription(self, sqs_arn):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/subscribe.html
        if self.__topic_arn == '':
            raise ValueError('missing topic arn to publish message')
        response = self.__sns_client.subscribe(
            TopicArn=self.__topic_arn,
            Protocol='sqs',
            Endpoint=sqs_arn,  # For the sqs protocol, the endpoint is the ARN of an Amazon SQS queue.
            # Attributes={
            #     'string': 'string'
            # },
            ReturnSubscriptionArn=True  # if the API request parameter ReturnSubscriptionArn is true, then the value is always the subscription ARN, even if the subscription requires confirmation.
        )
        return response['SubscriptionArn']
