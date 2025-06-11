##########################################
#            EXTRACT LAMBDA              #
##########################################

resource "aws_iam_role" "extract_lambda_role" {
  name = "role-extract-lambda"
  assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]
    }
    EOF
}

data "aws_iam_policy_document""s3_read_access"{
    statement {
    actions = ["s3:GetObject"]
    resources = [
      "${aws_s3_bucket.lambda_code_bucket.arn}/*",
      "${aws_s3_bucket.ingestion_zone_bucket.arn}/*"
    ]
  }
}
data "aws_iam_policy_document""s3_write_access"{
    statement {
    actions = ["s3:PutObject"]
    resources = [
      "${aws_s3_bucket.ingestion_zone_bucket.arn}/*",
    ]
  }
}

data "aws_iam_policy_document""s3_list_access"{
    statement {

    actions = ["s3:ListBucket"]

    resources = [
      aws_s3_bucket.ingestion_zone_bucket.arn,
    ]
  }
}

data "aws_iam_policy_document" "cw_permissions" {
  statement {
    actions = [ "logs:CreateLogGroup" ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }
  statement {
    actions = [ "logs:CreateLogStream", "logs:PutLogEvents" ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/*"
    ]
  }
}
data "aws_iam_policy_document""read_secret_manager"{
    statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = [
      "arn:aws:secretsmanager:eu-west-2:292779133515:secret:prod/totesys-a3g2W3",
    ]
  }
}

resource "aws_iam_policy" "s3_read_policy" {
  name = "s3-read-policy"
  policy = data.aws_iam_policy_document.s3_read_access.json
}
resource "aws_iam_policy""s3_write_policy"{
    name = "s3-write-policy"
    policy = data.aws_iam_policy_document.s3_write_access.json
}

resource "aws_iam_policy""s3_list_policy"{
    name = "s3-list-buckets-policy"
    policy = data.aws_iam_policy_document.s3_list_access.json
}

resource "aws_iam_policy" "cw_log_policy" {
  name = "cw-log-policy"
  policy = data.aws_iam_policy_document.cw_permissions.json
}

resource "aws_iam_policy" "secret_manager_read_policy" {
  name = "secret-manager-policy"
  policy = data.aws_iam_policy_document.read_secret_manager.json
}

resource "aws_iam_role_policy_attachment" "lambda_s3_read_attachment" {
    role = aws_iam_role.extract_lambda_role.name
    policy_arn = aws_iam_policy.s3_read_policy.arn
}
resource "aws_iam_role_policy_attachment" "lambda_s3_write_attachment" {
  role = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.s3_write_policy.arn
}
resource "aws_iam_role_policy_attachment" "lambda_cw_logs_attachment" {
  role = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.cw_log_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_s3_list_attachment" {
  role = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.s3_list_policy.arn
}

resource "aws_iam_role_policy_attachment" "lambda_access_secret_manager_read_attachment" {
    role = aws_iam_role.extract_lambda_role.name
    policy_arn = aws_iam_policy.secret_manager_read_policy.arn
}

##########################################
#            TRANSFORM LAMBDA            #
##########################################

resource "aws_iam_role" "transform_lambda_role" {
  name = "role-transform-lambda"
  assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]
    }
    EOF
}

data "aws_iam_policy_document""transform_s3_read_access"{
    statement {
    actions = ["s3:GetObject"]
    resources = [
      "${aws_s3_bucket.lambda_code_bucket.arn}/*",
      "${aws_s3_bucket.processed_zone_bucket.arn}/*",
      "${aws_s3_bucket.ingestion_zone_bucket.arn}/*"
    ]
  }
}
data "aws_iam_policy_document""transform_s3_write_access"{
    statement {
    actions = ["s3:PutObject"]
    resources = [
      "${aws_s3_bucket.processed_zone_bucket.arn}/*",
    ]
  }
}

data "aws_iam_policy_document""transform_s3_list_access"{
    statement {

    actions = ["s3:ListBucket","s3:ListObjectsV2"]

    resources = [
      aws_s3_bucket.processed_zone_bucket.arn,
      aws_s3_bucket.ingestion_zone_bucket.arn
    ]
  }
}

data "aws_iam_policy_document" "transform_cw_permissions" {
  statement {
    actions = [ "logs:CreateLogGroup" ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
    ]
  }
  statement {
    actions = [ "logs:CreateLogStream", "logs:PutLogEvents" ]
    resources = [
      "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/*"
    ]
  }
}


resource "aws_iam_policy" "transform_s3_read_policy" {
  name = "transform-s3-read-policy"
  policy = data.aws_iam_policy_document.transform_s3_read_access.json
}
resource "aws_iam_policy""transform_s3_write_policy"{
    name = "transform-s3-write-policy"
    policy = data.aws_iam_policy_document.transform_s3_write_access.json
}

resource "aws_iam_policy""transform_s3_list_policy"{
    name = "transform-s3-list-buckets-policy"
    policy = data.aws_iam_policy_document.transform_s3_list_access.json
}

resource "aws_iam_policy""transform_cw_log_policy" {
  name = "transform-cw-log-policy"
  policy = data.aws_iam_policy_document.transform_cw_permissions.json
}


resource "aws_iam_role_policy_attachment" "transform_lambda_s3_read_attachment" {
    role = aws_iam_role.transform_lambda_role.name
    policy_arn = aws_iam_policy.transform_s3_read_policy.arn
}
resource "aws_iam_role_policy_attachment" "transform_lambda_s3_write_attachment" {
  role = aws_iam_role.transform_lambda_role.name
  policy_arn = aws_iam_policy.transform_s3_write_policy.arn
}
resource "aws_iam_role_policy_attachment" "transform_lambda_cw_logs_attachment" {
  role = aws_iam_role.transform_lambda_role.name
  policy_arn = aws_iam_policy.transform_cw_log_policy.arn
}

resource "aws_iam_role_policy_attachment" "transform_lambda_s3_list_attachment" {
  role = aws_iam_role.transform_lambda_role.name
  policy_arn = aws_iam_policy.transform_s3_list_policy.arn
}



##########################################
#            LOAD LAMBDA                 #
##########################################

resource "aws_iam_role" "load_lambda_role" {
  name = "role-load-lambda"
  assume_role_policy = <<EOF
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sts:AssumeRole"
                ],
                "Principal": {
                    "Service": [
                        "lambda.amazonaws.com"
                    ]
                }
            }
        ]
    }
    EOF
}

data "aws_iam_policy_document""load_s3_read_access"{
    statement {
    actions = ["s3:GetObject"]
    resources = [
      "${aws_s3_bucket.lambda_code_bucket.arn}/*",
      "${aws_s3_bucket.processed_zone_bucket.arn}/*"
    ]
  }
}

data "aws_iam_policy_document""load_s3_list_access"{
    statement {

    actions = ["s3:ListBucket"]

    resources = [
      aws_s3_bucket.processed_zone_bucket.arn,
    ]
  }
}

data "aws_iam_policy_document""load_read_secret_manager"{
    statement {
    actions = ["secretsmanager:GetSecretValue"]
    resources = [
      "arn:aws:secretsmanager:eu-west-2:292779133515:secret:prod/warehouse-thBZA4",
    ]
  }
}

# data "aws_iam_policy_document" "transform_cw_permissions" {
#   statement {
#     actions = [ "logs:CreateLogGroup" ]
#     resources = [
#       "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:*"
#     ]
#   }
#   statement {
#     actions = [ "logs:CreateLogStream", "logs:PutLogEvents" ]
#     resources = [
#       "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/*"
#     ]
#   }
# }


resource "aws_iam_policy" "load_s3_read_policy" {
  name = "load-s3-read-policy"
  policy = data.aws_iam_policy_document.load_s3_read_access.json
}

resource "aws_iam_policy""load_s3_list_policy"{
    name = "load-s3-list-buckets-policy"
    policy = data.aws_iam_policy_document.load_s3_list_access.json
}

# resource "aws_iam_policy""transform_cw_log_policy" {
#   name = "transform-cw-log-policy"
#   policy = data.aws_iam_policy_document.transform_cw_permissions.json
# }


resource "aws_iam_policy" "load_secret_manager_read_policy" {
  name = "load-secret-manager-policy"
  policy = data.aws_iam_policy_document.load_read_secret_manager.json
}


resource "aws_iam_role_policy_attachment" "load_lambda_s3_read_attachment" {
    role = aws_iam_role.load_lambda_role.name
    policy_arn = aws_iam_policy.load_s3_read_policy.arn
}

# resource "aws_iam_role_policy_attachment" "transform_lambda_s3_write_attachment" {
#   role = aws_iam_role.transform_lambda_role.name
#   policy_arn = aws_iam_policy.transform_s3_write_policy.arn
#}
# resource "aws_iam_role_policy_attachment" "transform_lambda_cw_logs_attachment" {
#   role = aws_iam_role.transform_lambda_role.name
#   policy_arn = aws_iam_policy.transform_cw_log_policy.arn
# }

resource "aws_iam_role_policy_attachment" "load_lambda_s3_list_attachment" {
  role = aws_iam_role.load_lambda_role.name
  policy_arn = aws_iam_policy.load_s3_list_policy.arn
}

resource "aws_iam_role_policy_attachment" "load_lambda_access_secret_manager_read_attachment" {
    role = aws_iam_role.load_lambda_role.name
    policy_arn = aws_iam_policy.load_secret_manager_read_policy.arn
}