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
  provider = aws.us
  lifecycle {
    ignore_changes = [filename]
  }
  filename         = data.external.buildf.result.path
  function_name    = "caspal-ch-uri-rewrite"
  role             = aws_iam_role.r.arn
  handler          = "main.lambda_handler"
  source_code_hash = filebase64sha256(data.external.buildf.result.path)
  publish          = true
  runtime          = "python3.8"
}