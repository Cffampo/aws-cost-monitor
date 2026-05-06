import boto3
from datetime import datetime, timedelta

# AWS clients
cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
sns = boto3.client('sns')
s3 = boto3.client('s3')

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:992382382027:cost-alerts"
BUCKET_NAME = "carl-aws-cost-dashboard"

SERVICES = ['AmazonEC2', 'AmazonS3', 'AWSLambda']

def lambda_handler(event, context):
    end = datetime.utcnow()
    start = end - timedelta(days=7)

    report_lines = []
    total_cost = 0

    html_rows = ""

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
            Period=604800,
            Statistics=['Maximum']
        )

        cost = response['Datapoints'][0]['Maximum'] if response['Datapoints'] else 0

        total_cost += cost

        report_lines.append(f"{service}: ${cost:.2f}")

        html_rows += f"""
        <tr>
            <td>{service}</td>
            <td>${cost:.2f}</td>
            <td>Normal</td>
        </tr>
        """

    report_lines.append(f"\nTotal: ${total_cost:.2f}")

    message = "Weekly AWS Cost Report (per service):\n" + "\n".join(report_lines)

    # SNS Email
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=message,
        Subject="Weekly AWS Cost Report"
    )

    # Generate HTML dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AWS Cost Dashboard</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #0f172a;
                color: white;
                padding: 40px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}

            th, td {{
                border: 1px solid #334155;
                padding: 12px;
                text-align: left;
            }}

            th {{
                background-color: #1e293b;
            }}

            tr:nth-child(even) {{
                background-color: #111827;
            }}

            .card {{
                background: #111827;
                padding: 20px;
                border-radius: 12px;
                margin-bottom: 20px;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            <h1>AWS Cost Monitoring Dashboard</h1>
            <h2>Total Weekly Cost: ${total_cost:.2f}</h2>
            <p>Last Updated: {datetime.utcnow()}</p>
        </div>

        <table>
            <tr>
                <th>Service</th>
                <th>Weekly Cost</th>
                <th>Status</th>
            </tr>

            {html_rows}

        </table>
    </body>
    </html>
    """

    # Upload dashboard to S3
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key='index.html',
        Body=html_content,
        ContentType='text/html'
    )

    return {
        'statusCode': 200,
        'body': message
    }
