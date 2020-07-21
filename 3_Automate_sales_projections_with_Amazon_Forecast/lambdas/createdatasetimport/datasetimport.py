def lambda_handler(event, context):
    import boto3
    forecast = boto3.client('forecast')
    
    forecast.create_dataset_import_job(
        DatasetImportJobName='uk_sales_add_20091201_20101209',
        DatasetArn='arn:aws:forecast:us-east-1:805433377179:dataset/uk_sales',
        DataSource={
            'S3Config': {
                'Path': 's3://demo2-forecast-805433377179/input/tr_target_add_20091201_20101209.csv',
                'RoleArn': 'arn:aws:iam::805433377179:role/PersonalizePOCDemo-SageMakerIamRole-125YH74GVVADM',
            }
        },
        TimestampFormat='yyyy-MM-dd HH:mm:ss',
    )
    return event
    