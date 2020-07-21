def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.describe_predictor(
        PredictorArn='arn:aws:forecast:us-east-1:805433377179:predictor/uk_sales_add_20091201_20101209'
    )
    
    if response['Status'] == 'ACTIVE':
        event['is_active_predictor'] = True
    else:
        event['is_active_predictor'] = False

    return event