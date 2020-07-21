def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    forecast.create_forecast_export_job(
        ForecastExportJobName='uk_sales_add_20091201_20101216',
        ForecastArn='arn:aws:forecast:us-east-1:805433377179:forecast/uk_sales_add_20091201_20101216',
        Destination={
            'S3Config': {
                'Path': 's3://demo2-forecast-805433377179/output',
                'RoleArn': 'arn:aws:iam::805433377179:role/service-role/AmazonForecast-ExecutionRole-1576658959279',
            }
        },
    )
    return event