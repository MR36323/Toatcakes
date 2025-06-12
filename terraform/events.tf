resource "aws_cloudwatch_event_rule" "scheduler" {
  name = "trigger-step_func-10-mins"
  schedule_expression = "rate(10 minutes)"
  role_arn = aws_iam_role.Eventbridge_role.arn
}

resource "aws_cloudwatch_event_target" "step_func" {
  rule = aws_cloudwatch_event_rule.scheduler.name
  arn = aws_sfn_state_machine.step_function.arn
  role_arn = aws_iam_role.Eventbridge_role.arn
}