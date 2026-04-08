## Architecture

1. CloudWatch tracks AWS billing metrics
2. Lambda runs weekly and retrieves cost data
3. Lambda sends report via SNS
4. SNS delivers email notifications

CloudWatch Alarm → SNS → Email Alert
EventBridge → Lambda → SNS → Weekly Report