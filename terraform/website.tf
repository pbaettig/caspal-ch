locals {
  bucket_name  = "caspal.ch-prod"
  s3_origin_id = "${local.bucket_name}-origin"
}

resource "aws_s3_bucket" "bp" {
  bucket = local.bucket_name

  tags = {
    Name        = local.bucket_name
    Environment = "prod"
  }
}


data "aws_acm_certificate" "c" {
  provider    = aws.us
  domain      = "caspal.ch"
  types       = ["AMAZON_ISSUED"]
  most_recent = true
}


resource "aws_s3_bucket_policy" "bp" {
  bucket = aws_s3_bucket.bp.id
  policy = data.aws_iam_policy_document.cf.json
}

data "aws_iam_policy_document" "cf" {
  statement {
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.oai.iam_arn]
    }

    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      "${aws_s3_bucket.bp.arn}",
      "${aws_s3_bucket.bp.arn}/*",
    ]
  }
}



resource "aws_s3_bucket_acl" "bp_acl" {
  bucket = aws_s3_bucket.bp.id
  acl    = "private"
}


resource "aws_cloudfront_origin_access_identity" "oai" {
  comment = "oai-caspal.ch"
}

resource "aws_cloudfront_distribution" "s3_distribution" {
  origin {
    domain_name = aws_s3_bucket.bp.bucket_regional_domain_name
    origin_id   = local.s3_origin_id
    origin_path = "/caspal" # use "/placeholder" to display placeholder page


    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = ""
  default_root_object = "index.html"
  aliases             = ["caspal.ch", "www.caspal.ch"]

  custom_error_response {
    error_caching_min_ttl = 10
    error_code            = 404
    response_code         = 404
    response_page_path    = "/404.html"
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"] #["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = local.s3_origin_id
    viewer_protocol_policy = "allow-all"
    min_ttl                = 0
    default_ttl            = 300
    max_ttl                = 3600
    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
      headers = [
        # this will hurt cache-hit ratios, but is necessary
        # for the automatic language detection to work
        "Accept-Language",
      ]
    }

    lambda_function_association {
      # event_type = "viewer-request"
      event_type = "origin-request"
      lambda_arn = aws_lambda_function.f.qualified_arn
    }


  }


  price_class = "PriceClass_200"

  restrictions {
    geo_restriction {
      restriction_type = "none"
      locations        = []
    }
  }

  tags = {
    Environment = "production"
  }

  viewer_certificate {
    acm_certificate_arn = data.aws_acm_certificate.c.arn
    ssl_support_method  = "sni-only"
  }
}