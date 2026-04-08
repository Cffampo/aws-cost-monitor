# AWS Cost Monitoring System

## Overview
Built a serverless AWS cost monitoring system that tracks cloud spending and sends automated reports.

## Features
- Weekly cost reports using AWS Lambda
- Per-service cost breakdown (EC2, S3, Lambda)
- Real-time billing alerts via CloudWatch + SNS

## Architecture
CloudWatch → Lambda → SNS → Email

## Technologies
- AWS Lambda
- CloudWatch
- SNS
- Python (Boto3)

## How It Works
- CloudWatch stores AWS billing metrics
- Lambda retrieves weekly cost data
- SNS sends email notifications with reports
