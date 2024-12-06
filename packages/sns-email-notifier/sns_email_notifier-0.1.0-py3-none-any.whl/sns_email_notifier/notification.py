import boto3

def send_email_notification_via_sns(subject, body, sns_topic_arn, aws_region='us-east-1'):
    """
    Sends an email notification via AWS SNS.

    Args:
        subject (str): Subject of the email.
        body (str): Body of the email.
        sns_topic_arn (str): ARN of the SNS topic.
        aws_region (str): AWS region where the SNS topic is located.
    """
    try:
        sns_client = boto3.client('sns', region_name=aws_region)
        message = f"Subject: {subject}\n\n{body}"
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message
        )
        print(f"Email notification sent! Message ID: {response['MessageId']}")
    except Exception as e:
        raise RuntimeError(f"Failed to send SNS notification: {str(e)}")
