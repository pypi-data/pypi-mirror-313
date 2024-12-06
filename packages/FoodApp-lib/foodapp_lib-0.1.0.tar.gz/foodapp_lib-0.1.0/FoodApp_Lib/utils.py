# import boto3

# # Replace with your AWS region and SNS Topic ARN
# AWS_REGION = 'us-west-2'
# SNS_TOPIC_ARN = 'arn:aws:sns:us-west-2:481665109829:MySNSTopic'

# # Initialize boto3 clients
# sns_client = boto3.client('sns', region_name=AWS_REGION)
# sqs_client = boto3.client('sqs', region_name=AWS_REGION)

# def send_sns_notification(message):
#     """
#     Sends a notification to the SNS Topic.
#     """
#     try:
#         sns_client.publish(
#             TopicArn=SNS_TOPIC_ARN,
#             Message=message
#         )
#     except Exception as e:
#         print(f"Error sending SNS notification: {str(e)}")


# def fetch_sqs_notifications(queue_url):
#     """
#     Fetches messages from the SQS Queue.
#     """
#     try:
#         response = sqs_client.receive_message(
#             QueueUrl=queue_url,
#             MaxNumberOfMessages=10,
#             WaitTimeSeconds=20  # Long polling
#         )
#         messages = response.get('Messages', [])
#         notifications = []
#         if messages:
#             for message in messages:
#                 receipt_handle = message['ReceiptHandle']
#                 notifications.append(message['Body'])
#                 # Delete the message after processing
#                 sqs_client.delete_message(
#                     QueueUrl=queue_url,
#                     ReceiptHandle=receipt_handle
#                 )
#         return notifications
#     except Exception as e:
#         print(f"Error fetching SQS messages: {str(e)}")
#         return []
