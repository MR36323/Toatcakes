resource "null_resource" "create_dependencies" {
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../requirements.txt -t ${path.module}/../dependencies/python"
  }

  triggers = {
    dependencies = filemd5("${path.module}/../requirements.txt")
  }
}

data "archive_file" "layer_code" {
    depends_on = [null_resource.create_dependencies]

  type        = "zip"
  output_path = "${path.module}/../packages/extract/layer.zip"
  source_dir  = "${path.module}/../dependencies"
}

resource "aws_lambda_layer_version" "dependencies" {
    depends_on = [aws_s3_object.extract_lambda_layers]
    
  layer_name = "requests_library_layer"
  s3_bucket  = aws_s3_bucket.lambda_code_bucket.bucket
  s3_key     = "extract/layer.zip"
}