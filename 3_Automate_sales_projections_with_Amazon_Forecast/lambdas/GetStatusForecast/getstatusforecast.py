def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.describe_forecast(
        ForecastArn='arn:aws:forecast:us-east-1:805433377179:forecast/uk_sales_add_20091201_20101216'
    )
    
    if response['Status'] == 'ACTIVE':
        event['is_active_forecast'] = True
    else:
        event['is_active_forecast'] = False

    return event