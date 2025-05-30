data "archive_file" "extract_lambda" {
  type        = "zip"
  output_path = "${path.module}/../packages/extract/function.zip"
  source_file = "${path.module}/../src/extract.py"
}

resource "aws_lambda_function" "extract_lambda" {
  depends_on = [data.archive_file.extract_lambda]

  function_name = "extract_lambda"
  source_code_hash = filebase64sha256("${path.module}/../packages/extract/function.zip")
  s3_bucket = aws_s3_bucket.lambda_code_bucket.bucket
  s3_key = "extract/function.zip"
  role = aws_iam_role.extract_lambda_role.arn
  handler = "extract.lambda_handler"
  runtime = "python3.9"
  layers = [aws_lambda_layer_version.dependencies.arn]
}

