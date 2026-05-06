# AWS Cost Monitoring System

## Overview
Built a serverless AWS cost monitoring system that tracks cloud spending, sends real-time billing alerts, generates automated weekly reports, and updates a live dashboard hosted on Amazon S3.

<img width="3191" height="1643" alt="dashboard" src="https://github.com/user-attachments/assets/5df8af1b-b69c-47ce-b705-698ad932e756" />


---

## Features
- Automated weekly AWS cost reports using AWS Lambda
- Per-service cost breakdown (EC2, S3, Lambda)
- Real-time billing alerts with CloudWatch Alarms + SNS
- Fully automated scheduling using Amazon EventBridge
- Live cloud cost dashboard hosted on Amazon S3
- Dynamic HTML dashboard generation through Lambda

---

## Architecture

CloudWatch Metrics → Lambda → SNS → Email  
CloudWatch Metrics → Lambda → S3 Dashboard  
CloudWatch Alarm → SNS → Email  
EventBridge → Lambda (weekly trigger)

---

## Technologies
- AWS Lambda
- Amazon CloudWatch
- CloudWatch Alarms
- Amazon SNS
- Amazon EventBridge
- Amazon S3
- Python (Boto3)

---

## How It Works

### AWS Lambda
AWS Lambda is used as the core automation engine for the project. A Python-based Lambda function retrieves AWS billing metrics from CloudWatch, generates weekly per-service cost reports, sends notifications through SNS, and dynamically updates the S3-hosted dashboard.

---

### Amazon CloudWatch
Amazon CloudWatch collects AWS billing metrics, including total estimated charges and service-level costs. These metrics are used by Lambda for reporting and by CloudWatch Alarms for real-time cost threshold monitoring.

---

### CloudWatch Alarms
CloudWatch Alarms monitor billing thresholds and trigger alerts when AWS spending exceeds a defined limit. Alerts are automatically sent through Amazon SNS.

---

### Amazon SNS (Simple Notification Service)
Amazon SNS acts as the notification layer for the system. It delivers both real-time billing alerts and automated weekly cost reports directly to subscribed email recipients.

---

### Amazon EventBridge
Amazon EventBridge schedules the Lambda function to execute automatically every 7 days, enabling fully automated reporting without manual intervention.

---

### Amazon S3
Amazon S3 hosts the live static dashboard website. Lambda dynamically generates and uploads an updated HTML dashboard to S3 after each reporting cycle.

---

## Architecture Diagram

```text
                 +----------------------+
                 |   CloudWatch Metrics |
                 |   (Billing Data)     |
                 +----------+-----------+
                            |
                            v
                      +-----------+
                      |  Lambda   |
                      | (Reports) |
                      +-----+-----+
                            |
              +-------------+-------------+
              |                           |
              v                           v
        +-----------+              +-------------+
        |    SNS    |              |     S3      |
        | (Emails)  |              | Dashboard   |
        +-----+-----+              +------+------+ 
              |                           |
              v                           v
           Email                   Live Website


                 +----------------------+
                 |   CloudWatch Alarm   |
                 | (Cost Threshold)     |
                 +----------+-----------+
                            |
                            v
                       +----------+
                       |   SNS    |
                       +-----+----+
                             |
                             v
                           Email


                 +----------------------+
                 |     EventBridge      |
                 |  Weekly Scheduler    |
                 +----------+-----------+
                            |
                            v
                         Lambda
