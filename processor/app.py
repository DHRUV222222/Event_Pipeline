import boto3

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        summary_key = f"summary_{key}"
        s3.put_object(
            Bucket=bucket,
            Key=summary_key,
            Body=f"Summary generated for file: {key}"
        )
    return {"status": "success"}
