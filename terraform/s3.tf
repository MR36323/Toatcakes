resource "aws_s3_bucket" "ingestion_zone_bucket" {
  bucket_prefix = "ingestion-zone-bucket-"
}

resource "aws_s3_bucket" "processed_zone_bucket" {
  bucket_prefix = "processed-zone-bucket-"
}

resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket_prefix = "lambda-code-bucket-"
}

resource "aws_s3_object" "extract_lambda_code" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key = "extract/function.zip"
  source = "${path.module}/../function.zip"
}