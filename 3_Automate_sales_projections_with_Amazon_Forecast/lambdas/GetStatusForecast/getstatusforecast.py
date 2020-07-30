def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.describe_forecast(
        ForecastArn=event['ForecastArn']
    )
    
    if response['Status'] == 'ACTIVE':
        event['is_active_forecast'] = True
    else:
        event['is_active_forecast'] = False

    return event