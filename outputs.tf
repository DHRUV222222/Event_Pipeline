output "bucket_name" {
  value = aws_s3_bucket.event_bucket.bucket
}

output "lambda_function_name" {
  value = aws_lambda_function.s3_lambda.function_name
}
