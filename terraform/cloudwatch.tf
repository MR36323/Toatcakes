##########################################
#            EXTRACT LAMBDA              #
##########################################

resource "aws_sns_topic" "notification_topic" {
  name = "extract_lambda_error"                               
}

resource "aws_sns_topic_subscription" "notification_subscription" {
  topic_arn = aws_sns_topic.notification_topic.arn
  protocol   = "email"
  endpoint   = var.cloudwatch_email
}

resource "aws_cloudwatch_log_metric_filter" "lambda_error_filter_simple" {
  name           = "extract_lambda-error-filter-simple"
  log_group_name = "/aws/lambda/extract_lambda"
  pattern        = "?ERROR"

  metric_transformation {
    name      = "extract_lambda-error-count"
    namespace = "Lambda/Errors"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_error_alarm" {
  alarm_name          = "extract_lambda-error-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "extract_lambda-error-count"
  namespace           = "Lambda/Errors"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  alarm_description   = "This alarm monitors errors in extract_lambda Lambda function"
  alarm_actions       = [aws_sns_topic.notification_topic.arn]
  ok_actions          = [aws_sns_topic.notification_topic.arn]
  treat_missing_data  = "notBreaching"
}

##########################################
#            TRANSFORM LAMBDA            #
##########################################

resource "aws_sns_topic" "transform_notification_topic" {
  name = "transform_lambda_error"                               
}

resource "aws_sns_topic_subscription" "transform_notification_subscription" {
  topic_arn = aws_sns_topic.transform_notification_topic.arn
  protocol   = "email"
  endpoint   = var.cloudwatch_email
}

resource "aws_cloudwatch_log_metric_filter" "transform_lambda_error_filter_simple" {
  name           = "transform_lambda-error-filter-simple"
  log_group_name = "/aws/lambda/transform_lambda"
  pattern        = "?ERROR"

  metric_transformation {
    name      = "transform_lambda-error-count"
    namespace = "Lambda/Errors"
    value     = "1"
    default_value = "0"
  }
}

resource "aws_cloudwatch_metric_alarm" "transform_lambda_error_alarm" {
  alarm_name          = "transform_lambda-error-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = "1"
  metric_name         = "transform_lambda-error-count"
  namespace           = "Lambda/Errors"
  period              = "60"
  statistic           = "Sum"
  threshold           = "1"
  alarm_description   = "This alarm monitors errors in transform_lambda Lambda function"
  alarm_actions       = [aws_sns_topic.transform_notification_topic.arn]
  ok_actions          = [aws_sns_topic.transform_notification_topic.arn]
  treat_missing_data  = "notBreaching"
}