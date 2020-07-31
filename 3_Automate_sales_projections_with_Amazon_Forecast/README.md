# BLOG
https://quip-amazon.com/z5V6AKhoxrDo/20200722TimeSeriesblogyshiy

3. Automate sales projections with Amazon Forecast, QuicksiGHT and AWS Lamda

# WA
This module is based on Well-Architected Machine Learning Lends

https://d1.awsstatic.com/whitepapers/architecture/wellarchitected-Machine-Learning-Lens.pdf

Page 43

"
• Additional Training Data: AWS supports mechanisms for automatically
triggering retraining based on new data PUT to an Amazon S3 bucket. The
preferred method to initiate a controlled execution of model retraining is to set up
an ML pipeline that includes an event trigger based on changes to a source
Amazon S3 bucket. To detect the presence of new training data in an S3 bucket,
CloudTrail combined with CloudWatch Events allows you to trigger an AWS
Lambda function or AWS Step Functions workflow to initiate retraining tasks in
your training pipeline. The following figure illustrates the practice showing AWS
CodePipeline with ML Services:
"

# 1. Introduction

Demand forecasting using POS data has the potential to have a huge impact on your business. We will
We have a good business outlook, adequate supply to reduce lost opportunities, reduce unsold items and hold excess inventory. Make sure it is not. etc.
But you don't know anything about AI and you think it's hard to build a system, right?
AWS makes it easy.


# 2. Problem definition

In this blog, we're going to take retail data and run predictions with Amazon Forecast to Here is the flow to visualize the prediction results in Amazon QuickSight.


# 3. Architecture design

[Image: image.png](put diagram)
S3
Amazon Forecast
Athena
QuickSight



# 4. about this module

## Datasets

* UC Irvine Machine Learning Repository - https://archive.ics.uci.edu/ml/datasets/Online+Retail+II#

## AWS services

* Amazon Forecast
* Amazon QuickSight
* AWS Lambda
* AWS Step Functions

## Visualisations

* Screen Shots of forecast console during data import, training and evaluation
* Screen shots of creating QuickSight report
* Architecture diagram

## Outline

1. Introduction
2. Problem definition
3. Architecture design
4. Data    - Download data   - Data analysis (see missing data etc.)
5. Forecast   - import dataset    - AutoML and HPO   - Evaluation
6. QuickSight - Build report
7. Lambda trigger   - lambda job to trigger retrain and report building when new data posted to s3
8. Conclusion   - Other resources   - Intro next blog post in series


## Reference>
AWS Well-Architected Framework – Machine Learning Lens  
https://d1.awsstatic.com/whitepapers/architecture/wellarchitected-Machine-Learning-Lens.pdf

Automated and continuous deployment of Amazon SageMaker models with AWS Step Functions  
https://aws.amazon.com/blogs/machine-learning/automated-and-continuous-deployment-of-amazon-sagemaker-models-with-aws-step-functions/

Manage Amazon SageMaker with Step Functions  
https://docs.aws.amazon.com/step-functions/latest/dg/connect-sagemaker.html

Automating your Amazon Forecast workflow with Lambda, Step Functions, and CloudWatch Events rule  
https://aws.amazon.com/blogs/machine-learning/automating-your-amazon-forecast-workflow-with-lambda-step-functions-and-cloudwatch-events-rule/

Building AI-powered forecasting automation with Amazon Forecast by applying MLOps  
https://aws.amazon.com/blogs/machine-learning/building-ai-powered-forecasting-automation-with-amazon-forecast-by-applying-mlops/

Starting a State Machine Execution in Response to Amazon S3 Events  
https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html

Creating a Dataset Using Amazon S3 Files  
https://docs.aws.amazon.com/quicksight/latest/user/create-a-data-set-s3.html

Forecast Visualization Automation Blog  
https://github.com/aws-samples/amazon-forecast-samples/tree/master/ml_ops/visualization_blog

Analyzing contact center calls—Part 1: Use Amazon Transcribe and Amazon Comprehend to analyze customer sentiment  
https://aws.amazon.com/blogs/machine-learning/analyzing-contact-center-calls-part-1-use-amazon-transcribe-and-amazon-comprehend-to-analyze-customer-sentiment/



