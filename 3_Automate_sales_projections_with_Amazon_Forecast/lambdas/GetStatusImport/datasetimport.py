def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    response = forecast.create_dataset_import_job(
        DatasetImportJobName=event['detail']['requestParameters']['key'].replace('input/','').replace('.csv',''),
        DatasetArn='arn:aws:forecast:' + event['region'] + ':' + event['account'] + ':dataset/uk_sales',
        DataSource={
            'S3Config': {
                'Path': 's3://' + event['detail']['requestParameters']['bucketName'] + '/' + event['detail']['requestParameters']['key'],
                'RoleArn': event['detail']['userIdentity']['sessionContext']['sessionIssuer']['arn'],
            }
        },
        TimestampFormat='yyyy-MM-dd HH:mm:ss',
    )
    
    event['DatasetImportJobArn'] = response['DatasetImportJobArn']
    return event
    