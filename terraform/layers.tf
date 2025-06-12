##########################################
#                LAYER 1                 #
##########################################

resource "null_resource" "create_dependencies1" {
  provisioner "local-exec" {
    command = <<EOT
      docker run --rm --platform linux/amd64 -v "${path.module}/..:/var/task" -w /var/task --entrypoint /bin/bash public.ecr.aws/lambda/python:3.9 -c "
      rm -rf dependencies1 &&
      mkdir -p dependencies1/python &&
      pip install --only-binary=:all: numpy -t dependencies1/python &&
      pip install --only-binary=:all: pandas==2.2.2 --no-deps -t dependencies1/python &&
      pip install --only-binary=:all: -r requirements_cloud.txt -t dependencies1/python &&
      cp -r utils dependencies1/python
      "
EOT
  }
  triggers = {
    dependencies = timestamp()
  }
}

data "archive_file" "layer_code1" {
  depends_on = [null_resource.create_dependencies1]

  type        = "zip"
  output_path = "${path.module}/../packages/extract/layer1.zip"
  source_dir  = "${path.module}/../dependencies1"
}

resource "aws_lambda_layer_version" "dependencies1" {
  depends_on = [aws_s3_object.extract_lambda_layers]
    
  layer_name = "requests_library_layer1"
  compatible_runtimes = ["python3.9"]
  s3_bucket  = aws_s3_bucket.lambda_code_bucket.bucket
  s3_key     = aws_s3_object.extract_lambda_layers.key
}
