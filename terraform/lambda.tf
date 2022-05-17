data "aws_iam_policy_document" "rp" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com", "edgelambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "r" {
  name               = "${local.s3_origin_id}_cloudfront_edge"
  assume_role_policy = data.aws_iam_policy_document.rp.json
}

resource "aws_iam_role_policy_attachment" "basic" {
  role       = aws_iam_role.r.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}



data "external" "buildf" {
  program = [
    "/bin/bash",
    "build.sh"
    # "zip",
    # "main.py.zip",
    # "main.py"
  ]
  working_dir = "${path.module}/lambda"
  query       = {}
}



resource "aws_lambda_function" "f" {
  provider      = aws.us
  filename      = "${path.module}/lambda/main.py.zip"
  function_name = "caspal-ch-uri-rewrite"
  role          = aws_iam_role.r.arn
  handler       = "main.lambda_handler"
#   publish       = true
  # The filebase64sha256() function is available in Terraform 0.11.12 and later
  # For Terraform 0.11.11 and earlier, use the base64sha256() function and the file() function:
  # source_code_hash = "${base64sha256(file("lambda_function_payload.zip"))}"
  source_code_hash = base64encode(data.external.buildf.result.sha256)

  runtime = "python3.8"
}