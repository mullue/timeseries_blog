def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    forecast.create_predictor(
        PredictorName='uk_sales_add_20091201_20101209',
        ForecastHorizon=7,
        PerformAutoML=True,
        PerformHPO=False,
        EvaluationParameters={
            'NumberOfBacktestWindows': 1,
            'BackTestWindowOffset': 7
        },
        InputDataConfig={
            'DatasetGroupArn': 'arn:aws:forecast:us-east-1:805433377179:dataset-group/retail_uk_sales_prediction',
            'SupplementaryFeatures': [
                {
                    'Name': 'holiday',
                    'Value': 'UK'
                },
            ]
        },
        FeaturizationConfig={
            'ForecastFrequency': 'D',
            'Featurizations': [
                {
                    'AttributeName': 'demand',
                },
            ]
        },
    )
    return event
