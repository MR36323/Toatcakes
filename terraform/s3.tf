resource "aws_s3_bucket" "ingestion_zone_bucket" {
  bucket_prefix = "ingestion-zone-bucket-"
  force_destroy = true
}

resource "aws_s3_bucket" "processed_zone_bucket" {
  bucket_prefix = "processed-zone-bucket-"
  force_destroy = true
}

resource "aws_s3_bucket" "lambda_code_bucket" {
  bucket_prefix = "lambda-code-bucket-"
}

resource "aws_s3_object" "extract_lambda_code" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key = "extract/function.zip"
  source = "${path.module}/../packages/extract/function.zip"
}

resource "aws_s3_object" "transform_lambda_code" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key = "transform/function.zip"
  source = "${path.module}/../packages/transform/function.zip"
}

resource "aws_s3_object" "load_lambda_code" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key = "load/function.zip"
  source = "${path.module}/../packages/load/function.zip"
}


resource "aws_s3_object" "extract_lambda_layers" {
  bucket = aws_s3_bucket.lambda_code_bucket.bucket
  key = "extract/layer.zip"
  source = data.archive_file.layer_code1.output_path
  source_hash = data.archive_file.layer_code1.output_base64sha256
}