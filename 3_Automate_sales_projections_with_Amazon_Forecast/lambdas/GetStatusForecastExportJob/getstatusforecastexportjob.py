def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.describe_forecast_export_job(
        ForecastExportJobArn='arn:aws:forecast:us-east-1:805433377179:forecast-export-job/uk_sales_add_20091201_20101216/uk_sales_add_20091201_20101216'
    )
    
    if response['Status'] == 'ACTIVE':
        event['is_active_export'] = True
    else:
        event['is_active_export'] = False

    return event