##########################################
#                LAYER 1                 #
##########################################


     


resource "null_resource" "create_dependencies1" {
  provisioner "local-exec" {
    command = <<EOT
      rm -rf ${path.module}/../dependencies*
      mkdir -p ${path.module}/../dependencies1/python
      pip install --no-cache-dir --no-deps pandas -t ${path.module}/../dependencies1/python
      pip install numpy -t ${path.module}/../dependencies1/python
      pip install pg8000 -t ${path.module}/../dependencies1/python
      pip install -r ${path.module}/../requirements_cloud.txt -t ${path.module}/../dependencies1/python
      cp -r ${path.module}/../utils ${path.module}/../dependencies1/python
    EOT
  }

  triggers = {
    # dependencies = filemd5("${path.module}/../requirements.txt")
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
  # filename = "${path.module}/../packages/extract/layer.zip"
  compatible_runtimes = ["python3.9"]
  # source_code_hash = filebase64sha256("${path.module}/../packages/extract/layer.zip")
  s3_bucket  = aws_s3_bucket.lambda_code_bucket.bucket
  s3_key     = aws_s3_object.extract_lambda_layers.key
}






##########################################



















