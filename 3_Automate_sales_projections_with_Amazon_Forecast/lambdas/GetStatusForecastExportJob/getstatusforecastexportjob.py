def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.describe_forecast_export_job(
        ForecastExportJobArn=event['ForecastExportJobArn']
    )
    
    if response['Status'] == 'ACTIVE':
        event['is_active_export'] = True
    else:
        event['is_active_export'] = False

    return event