def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.describe_dataset_import_job(
        DatasetImportJobArn=event['DatasetImportJobArn']
    )
    
    if response['Status'] == 'ACTIVE':
        event['is_active_import'] = True
    else:
        event['is_active_import'] = False

    return event