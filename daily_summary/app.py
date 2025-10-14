import boto3
from datetime import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = "event-data-raw-dhruv-tf"
    
    response = s3.list_objects_v2(Bucket=bucket)
    summary_files = [obj['Key'] for obj in response.get('Contents', []) if obj['Key'].startswith('summary_')]

    daily_summary = ""
    for key in summary_files:
        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj['Body'].read().decode('utf-8')
        daily_summary += f"{content}\n"

    today = datetime.now().strftime("%Y-%m-%d")
    report_key = f"daily_summary_{today}.txt"

    s3.put_object(
        Bucket=bucket,
        Key=report_key,
        Body=daily_summary or "No summary files today."
    )

    return {"status": "success", "report_key": report_key}
