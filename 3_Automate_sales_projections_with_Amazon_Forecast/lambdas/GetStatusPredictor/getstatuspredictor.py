def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.describe_predictor(
        PredictorArn=event['PredictorArn']
    )
    
    if response['Status'] == 'ACTIVE':
        event['is_active_predictor'] = True
    else:
        event['is_active_predictor'] = False

    return event