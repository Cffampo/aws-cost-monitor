# AWS Cost Monitoring System

## Overview
Built a serverless AWS cost monitoring system that tracks cloud spending, sends real-time billing alerts, and generates automated weekly cost reports.

---

## Features
- Weekly cost reports using AWS Lambda
- Per-service cost breakdown (EC2, S3, Lambda)
- Real-time billing alerts via CloudWatch + SNS
- Fully automated using EventBridge scheduling

---

## Architecture
CloudWatch → Lambda → SNS → Email  
CloudWatch Alarm → SNS → Email  
EventBridge → Lambda (weekly trigger)

---

## Technologies
- AWS Lambda
- Amazon CloudWatch
- Amazon SNS
- Amazon EventBridge
- Python (Boto3)

---

## How It Works

### AWS Lambda
AWS Lambda is a serverless compute service that runs code without managing servers. In this project, Lambda executes a Python function on a weekly schedule to retrieve AWS billing data, process it into a readable format, and send a report via SNS.

---

### Amazon CloudWatch
CloudWatch collects and monitors AWS metrics. This project uses CloudWatch billing metrics to track total and per-service costs, which are used for both reporting and alerting.

---

### Amazon SNS (Simple Notification Service)
SNS is a messaging service used to send notifications. It delivers both real-time alerts (from CloudWatch alarms) and weekly reports (from Lambda) to email subscribers.

---

### CloudWatch Alarms
CloudWatch Alarms monitor billing thresholds and trigger alerts when costs exceed a defined limit. These alerts are sent through SNS.

---

### Amazon EventBridge
EventBridge schedules the Lambda function to run automatically every 7 days, ensuring consistent cost monitoring without manual intervention.

---

## Architecture Diagram

            +----------------------+
            |   CloudWatch Metrics |
            | (Billing Data)       |
            +----------+-----------+
                       |
                       v
            +----------------------+
            |   CloudWatch Alarm   |
            | (Cost Threshold)     |
            +----------+-----------+
                       |
                       v
                 +-----------+
                 |    SNS    |
                 | (Alerts)  |
                 +-----+-----+
                       |
                       v
                    Email

            +----------------------+
            |   EventBridge        |
            | (Weekly Schedule)    |
            +----------+-----------+
                       |
                       v
                 +-----------+
                 |  Lambda   |
                 | (Reports) |
                 +-----+-----+
                       |
                       v
                 +-----------+
                 |    SNS    |
                 +-----+-----+
                       |
                       v
                    Email
