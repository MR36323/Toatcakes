resource "aws_sns_topic" "notification_topic" {
  name = "extract_lambda_error"                               # make "extract lambda" a variable
}

resource "aws_sns_topic_subscription" "notification_subscription" {
  topic_arn = aws_sns_topic.notification_topic.arn
  protocol   = "email"
  endpoint   = "mathieurees@gmail.com"                                             # NOT SECURE, DO NOT PUSH IT ON GITHUB
}

# CloudWatch Log Metric Filter for simple ERROR text matching
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

# CloudWatch Alarm for error detection
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


