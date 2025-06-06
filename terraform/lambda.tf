data "archive_file" "extract_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/extract/function.zip"
  source_content = file("${path.module}/../src/extract.py")
  source_content_filename = "extract.py"
  output_file_mode = "0666"
}

resource "aws_lambda_function" "extract_lambda" {
  depends_on = [aws_s3_object.extract_lambda_code]


  function_name = "extract_lambda"
  source_code_hash = data.archive_file.extract_lambda.output_base64sha256
  s3_bucket = aws_s3_bucket.lambda_code_bucket.bucket
  s3_key = aws_s3_object.extract_lambda_code.key
  role = aws_iam_role.extract_lambda_role.arn
  handler = "extract.lambda_handler"
  runtime = "python3.9"
  layers = [aws_lambda_layer_version.dependencies.arn]
  timeout = 900
  memory_size = 256
  environment {
    variables = {
      BUCKET = aws_s3_bucket.ingestion_zone_bucket.bucket
    }
  }
}

