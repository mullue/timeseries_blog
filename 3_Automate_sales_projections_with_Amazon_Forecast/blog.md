20200722_TimeSeries_blog_yshiy

GitHub : 3_Automate_sales_projections_with_Amazon_Forecast/

https://github.com/glyfnet/timeseries_blog/tree/master/3_Automate_sales_projections_with_Amazon_Forecast


Introduction

Demand forecasting using POS data has the potential to have a huge impact on your business. We will We have a good business outlook, adequate supply to reduce lost opportunities, reduce unsold items and hold excess inventory. Make sure it is not. etc. But you don't know anything about AI and you think it's hard to build a system, right? AWS makes it easy.

Problem definition

In this blog, we're going to take retail data and run predictions with Amazon Forecast to Here is the flow to visualize the prediction results in Amazon QuickSight.


Architecture design



first : manual forecasting and visualization


![01_arch_design_1](https://user-images.githubusercontent.com/27226946/89359516-0100f300-d701-11ea-8bf0-f4fbe3204119.png)
![01_arch_design_2](https://user-images.githubusercontent.com/27226946/89359520-02cab680-d701-11ea-979c-c1f35cb07292.png)
![02_import_1](https://user-images.githubusercontent.com/27226946/89359522-03fbe380-d701-11ea-8ffd-9d0ffbd0290d.png)
![02_import_2](https://user-images.githubusercontent.com/27226946/89359523-04947a00-d701-11ea-86e0-15d5768a08db.png)
![02_import_3](https://user-images.githubusercontent.com/27226946/89359527-052d1080-d701-11ea-83c4-e1c751041a77.png)
![02_import_4](https://user-images.githubusercontent.com/27226946/89359528-05c5a700-d701-11ea-9e49-3ed2cd399bc8.png)
![03_predictor_1](https://user-images.githubusercontent.com/27226946/89359529-05c5a700-d701-11ea-9e7a-eff879bb6bae.png)
![03_predictor_2](https://user-images.githubusercontent.com/27226946/89359532-065e3d80-d701-11ea-8ab5-c1a6cde65d99.png)
![03_predictor_3](https://user-images.githubusercontent.com/27226946/89359534-065e3d80-d701-11ea-9497-275cfe7d9e9b.png)
![04_forecast_1](https://user-images.githubusercontent.com/27226946/89359535-06f6d400-d701-11ea-845d-89c759fa7a9f.png)
![05_export_1](https://user-images.githubusercontent.com/27226946/89359537-078f6a80-d701-11ea-9701-a703502ca9e5.png)
![05_export_2](https://user-images.githubusercontent.com/27226946/89359538-078f6a80-d701-11ea-8f8c-915adb7f9fd7.png)
![05_export_3](https://user-images.githubusercontent.com/27226946/89359539-08280100-d701-11ea-9ce5-24e04fc96ade.png)
![05_export_4](https://user-images.githubusercontent.com/27226946/89359540-08c09780-d701-11ea-8376-9fc21cd40164.png)
![06_quicksight_1](https://user-images.githubusercontent.com/27226946/89359541-08c09780-d701-11ea-92f6-3183fc2ca187.png)
![06_quicksight_2](https://user-images.githubusercontent.com/27226946/89359543-09592e00-d701-11ea-8b3d-25538c7a1cff.png)
![06_quicksight_3](https://user-images.githubusercontent.com/27226946/89359544-09592e00-d701-11ea-97a4-84644d21e73d.png)
![06_quicksight_4](https://user-images.githubusercontent.com/27226946/89359545-09f1c480-d701-11ea-83c5-812eec305287.png)
![06_quicksight_5](https://user-images.githubusercontent.com/27226946/89359546-0a8a5b00-d701-11ea-8d8a-c3b8dd12b1dd.png)
![06_quicksight_6](https://user-images.githubusercontent.com/27226946/89359547-0a8a5b00-d701-11ea-819f-f4bf2010965d.png)
![06_quicksight_7](https://user-images.githubusercontent.com/27226946/89359548-0b22f180-d701-11ea-8229-13590e2f63b0.png)
![06_quicksight_8](https://user-images.githubusercontent.com/27226946/89359549-0bbb8800-d701-11ea-9e5d-ff1859058533.png)
![07_arch](https://user-images.githubusercontent.com/27226946/89359550-0bbb8800-d701-11ea-82f1-7e8ec30952f6.png)
![08_stepfunctions](https://user-images.githubusercontent.com/27226946/89359551-0c541e80-d701-11ea-93f1-404066bf3fcd.png)



その後、パイプラインを作成し、S3へのアップロードをトリガにForecastを実施し、S3に結果を格納する。


second : auto forecasting with AWS Step Functions and AWS Lambda

[Image: image.png]


Data - Download data - Data analysis (see missing data etc.)

Download data from the site and calculate sales as a target variable.
Extract the records for UK only. In this case, I use only country, timestamp and sales data.
I use the data from 2009/12/01-2010/12/02 as the training data, and for the additional training data in the second half, I will use the data from 2009/12/01-2010/12/09.

https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/1_prepare_dataset.ipynb



Forecast - import dataset - AutoML - Evaluation

Step 1: Import dataset

[Image: image.png]
[Image: image.png]

[Image: image.png]
[Image: image.png]

Step 2: Build predictor with AutoML

[Image: image.png]




[Image: image.png]



Step 3: Evaluation

DeepAR+ with error 14% is best solution.
[Image: image.png]

Step 4: Create a forecast

[Image: image.png]

Step 5: Export forecast

[Image: image.png][Image: image.png]
[Image: image.png]

forecast located in S3 output object.
[Image: image.png]


QuickSight - Build report

configure access to S3 bucket
[Image: image.png]
[Image: image.png]
Loading forecast output of CSV.
[Image: image.png]

choose S3
[Image: image.png]
designate manifest file
https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/manifest_for_quicksight/manifest_uk_sales_pred.json
[Image: image.png]


[Image: image.png]
set attribute for visualization.
[Image: image.png]
[Image: image.png]
S3のデータを事前にクエリで加工したい場合、Amazon Athenaを利用してください。



Lambda trigger - lambda job to trigger retrain and report building when new data posted to s3


[Image: image.png]

follow this notebook
https://github.com/glyfnet/timeseries_blog/blob/master/3_Automate_sales_projections_with_Amazon_Forecast/2_building_pipeline.ipynb


Step 1: create Lambda functions

boto3を使って、Amazon Forecastのデータインポート、predictor作成、forecast、forecast結果のexportを行う関数を作成します。また、各ジョブのステータスを取得する関数を作成します。

Step 2: create Step Functions state machine

[Image: image.png]


Step 3: Cloud Trail and Cloud Watch Events

When a file is put to S3, Step Functions are started.


Step 4: put additional data and visualize

S3にデータを置くとパイプラインが実行され、S3に予測結果が出力される。
QuickSightにログインし、手動で可視化を実行する
最後に追加の学習ファイルがS3にアップされます。そしてそれをトリガに、Step Functionsのワークフローが開始されます。


最後まで実行されるのに少し時間がかかりますので、待ちましょう。
ジョブが完了したら、結果がS3に格納されています。

追加データによるpredictorの誤差を確認すると、8%でした。

When you put the data in 3, the pipeline will run and output the prediction results to S3.
Login to QuickSight and run the visualization manually
At the end, an additional training file is uploaded to S3, and it triggers the Step Functions workflow. It will then trigger the Step Functions workflow.


It will take a little while for it to run to the end, so wait.
Once the job is completed, the result is stored in S3.

When we checked the predictor error due to the additional data, it was 8%.

Translated with www.DeepL.com/Translator (free version)

![09_predictor](https://user-images.githubusercontent.com/27226946/89359552-0cecb500-d701-11ea-8e29-93bee36a2cae.png)

Step 5: Visualize with QuickSight

前半と同じ手順で、可視化することができます。
The same steps as in the first half of this section can be used to visualize.

![10_quicksight](https://user-images.githubusercontent.com/27226946/89359553-0cecb500-d701-11ea-83e5-e618ca164fa5.png)


Conclusion

実際にビジネスで機械学習を利用するときは、運用を考慮したシステム設計が重要になります。
今回のように、StepFunctionsとAIサービスを組み合わせることで、S3にデータを置くだけでモデルを学習し、予測結果をS3に出力するというパイプラインを簡単に構築することができます。

We can now look at the predictive results. Data analysis is the goal until you make a decision. Use the results of these predictions to figure out the next move for your business. You can make predictions by item or by customer as needed. This is how AWS allows you to enjoy the benefits of AI/ML at a very low cost. It's easy to use your company's dormant data and add value to your business.

In the next article, we will look at a variety of time series algorithms for power prediction.


