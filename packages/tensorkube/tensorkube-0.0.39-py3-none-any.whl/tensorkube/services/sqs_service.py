import boto3
from tensorkube.constants import REGION

def create_sqs_queue(queue_name: str, region: str = REGION) -> str:
    sqs = boto3.client('sqs', region_name=region)
    response = sqs.create_queue(
        QueueName=queue_name,
        Attributes={
            'DelaySeconds': '0',
            'MessageRetentionPeriod': '86400',  # Retain messages for 1 day
            'VisibilityTimeout': '43200' # Make messages invisible for 12 hrs
        }
    )
    queue_url = response['QueueUrl']
    return queue_url


def delete_sqs_queue(queue_name: str, region: str = REGION) -> None:
    sqs = boto3.client('sqs', region_name=region)
    queue_url = sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
    sqs.delete_queue(QueueUrl=queue_url)
    print(f"Queue {queue_name} deleted successfully.")

def queue_message(queue_url: str, message_body: str, region: str = REGION) -> None:
    sqs = boto3.client('sqs', region_name=region)
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    print(f"Message sent to queue")
