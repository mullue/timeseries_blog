def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.describe_dataset_import_job(
        DatasetImportJobArn='arn:aws:forecast:us-east-1:805433377179:dataset-import-job/uk_sales/uk_sales_add_20091201_20101209'
    )
    
    if response['Status'] == 'ACTIVE':
        event['is_active_import'] = True
    else:
        event['is_active_import'] = False

    return event