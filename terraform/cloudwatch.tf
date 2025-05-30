# resource "aws_cloudwatch_log_group" "log_group" {
#   name              = var.log_group_name
#   retention_in_days = var.retention_days
# }

# resource "aws_cloudwatch_log_stream" "log_stream" {
#   name           = "mahira-log-stream"
#   log_group_name = aws_cloudwatch_log_group.log_group.name
# }


resource "aws_sns_topic" "notification_topic" {
  name = "extract_lambda_error"

}

resource "aws_sns_topic_subscription" "notification_subscription" {
  topic_arn = aws_sns_topic.notification_topic.arn
  protocol   = "email"
  endpoint   = "" #NOT SECURE, DO NOT PUSH IT ON GITHUB
}
resource "aws_cloudwatch_metric_alarm" "cpu_utilization_alarm" {
  alarm_name          = "High CPU Utilization"
  alarm_description   = "Alerts when CPU utilization exceeds 90%"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  statistic           = "Average"
  period              = 60
  evaluation_periods  = 1
  threshold           = 90
  comparison_operator = "GreaterThanThreshold"
  alarm_actions      = [aws_sns_topic.notification_topic.arn] # Use the SNS topic
  # ... other attributes as needed
}
resource "aws_cloudwatch_log_metric_filter" "yada" {
  name           = "MyAppAccessCount"
  pattern        = ""
  log_group_name = "/aws/lambda/extract_lambda"
  metric_transformation {
    name      = "EventCount"
    namespace = "YourNamespace"
    value     = "1"
  }
}