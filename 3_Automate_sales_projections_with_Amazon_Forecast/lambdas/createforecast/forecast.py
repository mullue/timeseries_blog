def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    forecast.create_forecast(
        ForecastName='uk_sales_add_20091201_20101216',
        PredictorArn='arn:aws:forecast:us-east-1:805433377179:predictor/uk_sales_add_20091201_20101209',
    )
    return event
    