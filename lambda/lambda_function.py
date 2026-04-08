import boto3
from datetime import datetime, timedelta

# AWS clients
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:992382382027:cost-alerts"

# List of services you want to track
SERVICES = ['AmazonEC2', 'AmazonS3', 'AWSLambda']

def lambda_handler(event, context):
    end = datetime.utcnow()
    start = end - timedelta(days=7)
    
    report_lines = []
    total_cost = 0
    
    for service in SERVICES:
        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[
                {'Name': 'Currency', 'Value': 'USD'},
                {'Name': 'ServiceName', 'Value': service}
            ],
            StartTime=start,
            EndTime=end,
            Period=604800,  # 7 days in seconds
            Statistics=['Maximum']
        )
        
        cost = response['Datapoints'][0]['Maximum'] if response['Datapoints'] else 0
        total_cost += cost
        report_lines.append(f"{service}: ${cost:.2f}")
    
    report_lines.append(f"\nTotal: ${total_cost:.2f}")
    message = "Weekly AWS Cost Report (per service):\n" + "\n".join(report_lines)
    
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="Weekly AWS Cost Report"
    )

    return message