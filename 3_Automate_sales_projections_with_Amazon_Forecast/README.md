3. Automate sales projections with Amazon Forecast, QuicksiGHT and AWS Lamda



1. Introduction

Demand forecasting using POS data has the potential to have a huge impact on your business. We will
We have a good business outlook, adequate supply to reduce lost opportunities, reduce unsold items and hold excess inventory. Make sure it is not. etc.
But you don't know anything about AI and you think it's hard to build a system, right?
AWS makes it easy.


1. Problem definition

In this blog, we're going to take retail data and run predictions with Amazon Forecast to Here is the flow to visualize the prediction results in Amazon QuickSight.


1. Architecture design

[Image: image.png](put diagram)
S3
Amazon Forecast
Athena
QuickSight



1. Data    - Download data   - Data analysis (see missing data etc.)

download retail data from web and data analytics and arrange with Excel.upload to S3.

(add Screen shot. Put the code on GitHub)



1. Forecast   - import dataset    - AutoML and HPO   - Evaluation

AutoML training and prediction with GUI console. 

(add Screen shot. Put the code on GitHub)
[Image: image.png][Image: image.png]


1. View prediction results in QuickSight

Enter the QuickSight screen and set up your new analytics. Choose Amazon Athena as your data source and set up the SQL for loading.

(add Screen shot.)



1. Lambda trigger   - lambda job to trigger retrain and report building when new data posted to s3

use StepFunctions to automate forecast.
[Image: image.png]


1. Conclusion   - Other resources   - Intro next blog post in series

We can now look at the predictive results. Data analysis is the goal until you make a decision. Use the results of these predictions to figure out the next move for your business. You can make predictions by item or by customer as needed.
This is how AWS allows you to enjoy the benefits of AI/ML at a very low cost. It's easy to use your company's dormant data and add value to your business.

In the next article, we will look at a variety of time series algorithms for power prediction.



<memo>

Datasets

* UC Irvine Machine Learning Repository - https://archive.ics.uci.edu/ml/datasets/Online+Retail+II#

AWS services

* Amazon Forecast
* Amazon QuickSight
* AWS Lambda

Visualisations

* Screen Shots of forecast console during data import, training and evaluation
* Screen shots of creating QuickSight report
* Architecture diagram

Outline

1. Introduction
2. Problem definition
3. Architecture design
4. Data    - Download data   - Data analysis (see missing data etc.)
5. Forecast   - import dataset    - AutoML and HPO   - Evaluation
6. QuickSight - Build report
7. Lambda trigger   - lambda job to trigger retrain and report building when new data posted to s3
8. Conclusion   - Other resources   - Intro next blog post in series




<reference>
https://aws.amazon.com/blogs/machine-learning/analyzing-contact-center-calls-part-1-use-amazon-transcribe-and-amazon-comprehend-to-analyze-customer-sentiment/

https://github.com/aws-samples/amazon-forecast-samples/tree/master/ml_ops/visualization_blog
