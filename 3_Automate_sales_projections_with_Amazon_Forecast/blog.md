# Introduction

In the retail industry, forecasting sales and visitor numbers is an important topic that directly affects your business. Accurate sales forecasting can help you avoid overstocked merchandise, lost sales opportunities, and achieve more business. Accurately predicting the number of visitors will also allow you to properly plan employee shifts and use the information as an aid to forecast sales. On the other hand, although POS data is stored on the system, many people think that it may be difficult to utilize AI and machine learning. In this blog, I'll show you how Amazon Forecast, an AI service provided by AWS for time-series forecasting, can be used to make predictions without difficult programming or anything else. We'll also go one step further and explain how it can be easily implemented in a systematic way with daily batches, for example. By systematization, all you have to do is feed data into the storage called S3, the data pipeline is executed, and the prediction results can be output to S3.

# Problem definition

This blog uses sales data from a UK e-commerce company published on the internet to forecast sales for the following week. We will use Amazon Forecast to make sales forecasts, either manually in the GUI or automatically by building a pipeline. The results of the forecast are visualized using Amazon QuickSight, allowing management to get an immediate view of the sales forecast.


# Architecture design



## first : manual forecasting and visualization

The first step is to perform sales forecasting by operating the console. From the console, you import data in Amazon Forecast, train the forecasters, run the forecasts, and export the results of the forecasts. The exported forecast results are then visualized in Amazon QuickSight.

![01_arch_design_1](https://user-images.githubusercontent.com/27226946/89359516-0100f300-d701-11ea-8bf0-f4fbe3204119.png)


## second : auto forecasting with AWS Step Functions and AWS Lambda

Triggered by the data upload to S3, it automatically imports data, learns predictors, executes predictions, and exports the results of the prediction, all done by manual execution. The pipeline is configured using AWS Lambda and AWS Step Funcions. The output prediction results are visualized using Amazon QuickSight.

![01_arch_design_2](https://user-images.githubusercontent.com/27226946/89359520-02cab680-d701-11ea-979c-c1f35cb07292.png)


# Data - Download data - Data analysis (see missing data etc.)

Run 1_prepare_dataset.ipynb. Download data and calculate sales as the target variable. Prepare data from 2009/12/01 to 2010/12/02 as training data and upload them to S3. And as additional training data, from 2009/12/01 to 2010/12/09, we upload the data from 2009/12/01 to 2010/12/09 to S3.

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/1_prepare_dataset.ipynb



# Forecast - import dataset - AutoML - Evaluation

Once we have stored the training data in S3, we can go to the Amazon Forecast console and create the dataset.

## Step 1: Import dataset

Enter the name of the dataset group (retail_uk_sales_predictin), select Retail as the domain and click Next.

![02_import_1](https://user-images.githubusercontent.com/27226946/89359522-03fbe380-d701-11ea-8ffd-9d0ffbd0290d.png)

Enter a name for the dataset (uk_sales) and select day as the forecast unit, leave the Data schema intact and click Next.

![02_import_2](https://user-images.githubusercontent.com/27226946/89359523-04947a00-d701-11ea-86e0-15d5768a08db.png)

Enter Dataset Import name (uk_sales_2009120101_20101202) and create a new IAM Role. In the Data location field, enter the S3 path of the training data that you have stored in the previous preparation and click Create.

![02_import_3](https://user-images.githubusercontent.com/27226946/89359527-052d1080-d701-11ea-83c4-e1c751041a77.png)

Wait until the target time series data becomes active. Next, we train the predictor.

![02_import_4](https://user-images.githubusercontent.com/27226946/89359528-05c5a700-d701-11ea-9e49-3ed2cd399bc8.png)


## Step 2: Build predictor with AutoML

Click Start for Predictor training. Enter the Predictor name and enter 7, the time period you want to forecast, in the Forecast horizon. You may want to use the calendar information built into Amazon Forecast for a potentially more accurate forecast. Select United Kingdom as the Country for holidays - optional and click Create.

![03_predictor_1](https://user-images.githubusercontent.com/27226946/89359529-05c5a700-d701-11ea-9e7a-eff879bb6bae.png)

The training will begin. After a short period of time, the training is complete and you will see the word Acitive in Predictor training. Click View in Predictor training to see the training results.

![03_predictor_2](https://user-images.githubusercontent.com/27226946/89359532-065e3d80-d701-11ea-8ab5-c1a6cde65d99.png)



## Step 3: Evaluation

AutoML results show that Deep_AR_Plus is chosen as the algorithm, with an error of 14.23%.

![03_predictor_3](https://user-images.githubusercontent.com/27226946/89359534-065e3d80-d701-11ea-9497-275cfe7d9e9b.png)

Next, generate a prediction and click Create a Forecast.


## Step 4: Create a forecast

Enter a forecast name and choose the one you just learned for Predictor. Click Create a forecast.

![04_forecast_1](https://user-images.githubusercontent.com/27226946/89359535-06f6d400-d701-11ea-845d-89c759fa7a9f.png)

Once the forecast is generated, review the details.


## Step 5: Export forecast

Export the forecast results to S3, and to the right of Exports, click Create forecast export.

![05_export_1](https://user-images.githubusercontent.com/27226946/89359537-078f6a80-d701-11ea-9701-a703502ca9e5.png)

Enter an export name and specify Generated forecast. Specify where you want to export the forecast results to S3 and click Create forecast export.

![05_export_2](https://user-images.githubusercontent.com/27226946/89359538-078f6a80-d701-11ea-8f8c-915adb7f9fd7.png)
![05_export_3](https://user-images.githubusercontent.com/27226946/89359539-08280100-d701-11ea-9ce5-24e04fc96ade.png)


The predictions were exported to the specified S3 path.
![05_export_4](https://user-images.githubusercontent.com/27226946/89359540-08c09780-d701-11ea-8376-9fc21cd40164.png)


## Step 6: Visualization by QuickSight

Let's visualize the prediction results exported to S3 in Amazon QuickSight. First, click Add or remove QuickSight access to AWS services from Security & permissions to allow the file to be read from S3.

![06_quicksight_1](https://user-images.githubusercontent.com/27226946/89359541-08c09780-d701-11ea-92f6-3183fc2ca187.png)

Select the S3 bucket to which you exported the predictions and check the Write permission for Athena Workgroup box. You have now completed your preconfiguration.

![06_quicksight_2](https://user-images.githubusercontent.com/27226946/89359543-09592e00-d701-11ea-8b3d-25538c7a1cff.png)

Load the data and visualize it. Click New analysis on the top page.

![06_quicksight_3](https://user-images.githubusercontent.com/27226946/89359544-09592e00-d701-11ea-97a4-84644d21e73d.png)

Select S3.

![06_quicksight_4](https://user-images.githubusercontent.com/27226946/89359545-09f1c480-d701-11ea-83c5-812eec305287.png)

Enter an arbitrary value in Data source name to specify a manifest file for S3 loading. The manifest file is created when the notebook is executed and uploaded to S3.

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/manifest_for_quicksight/manifest_uk_sales_pred.json


![06_quicksight_5](https://user-images.githubusercontent.com/27226946/89359546-0a8a5b00-d701-11ea-8d8a-c3b8dd12b1dd.png)

When the data is loaded into SPICE, click Visualize.

![06_quicksight_6](https://user-images.githubusercontent.com/27226946/89359547-0a8a5b00-d701-11ea-819f-f4bf2010965d.png)

Select the line graph and select date for X axis and p10(sum), p50(sum) and p90(sum) for Value. You can now visualize.

![06_quicksight_7](https://user-images.githubusercontent.com/27226946/89359548-0b22f180-d701-11ea-8229-13590e2f63b0.png)
![06_quicksight_8](https://user-images.githubusercontent.com/27226946/89359549-0bbb8800-d701-11ea-9e5d-ff1859058533.png)

For the sake of simplicity, we loaded the S3 data directly, but you can also use Amazon Athena if you want to process it in advance with queries.


# Lambda trigger - lambda job to trigger retrain and report building when new data posted to s3

Next, we'll leverage AWS Lambda and AWS Step Functions to build a pipeline. AWS Step Functions are triggered by the data input to S3, which automatically imports data from Amazon Forecast, builds the forecasters, predicts, and exports the results.


![07_arch](https://user-images.githubusercontent.com/27226946/89359550-0bbb8800-d701-11ea-82f1-7e8ec30952f6.png)

Run the notebook in 2_building_pipeline.ipynb to build the pipeline and upload the data to S3.

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/2_building_pipeline.ipynb


## Step 1: create Lambda functions

Using boto3, we will create functions to import data from Amazon Forecast, create a predictor, forecast, and export the forecast results. We will also create a function to get the status of each job.

## Step 2: create Step Functions state machine

StepFunctions proceeds by issuing a job, checking the status of the job, waiting if it is not completed, and moving on to the next job when it is completed.

![08_stepfunctions](https://user-images.githubusercontent.com/27226946/89359551-0c541e80-d701-11ea-93f1-404066bf3fcd.png)


## Step 3: Cloud Trail and Cloud Watch Events

Configure Cloud Trail and CloudWatch to run Step Functions when the files are stored in S3. The Step Functions developer's guide is helpful.

https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html


## Step 4: put additional data and visualize

The Step Functions pipeline is executed as a data put and trigger to S3. It takes a bit of time for it to run to the end. Once the job is completed, the results are stored in S3. When we check the predictor with the additional data, Deep_AR-Plus is selected, with a margin of error of 8.14%.


![09_predictor](https://user-images.githubusercontent.com/27226946/89359552-0cecb500-d701-11ea-8e29-93bee36a2cae.png)


## Step 5: Visualize with QuickSight

The same steps as in the first half of this section can be used to visualize

![10_quicksight](https://user-images.githubusercontent.com/27226946/89359553-0cecb500-d701-11ea-83e5-e618ca164fa5.png)



# Conclusion
Time series forecasting has a lot of opportunities to be used in various aspects of business and can make your business bigger. As I have explained, you can easily verify it from the GUI, so why not give it a try first? When it comes to actually integrating it into your business processes, you can easily configure an automated pipeline using AWS Step Functions and AWS Lambda. Why not try it out with your existing data first?

We have covered 4 big scenarios to handle timeseres data. You can find other posts below:

* Introduction to time series forecasting with SageMaker and Python by Eric Greene
* Benchmarking popular time series forecasting algorithms on electricity demand forecast by Yin Song
* Anomaly Detection of timeseries by Seongmoon Kang


