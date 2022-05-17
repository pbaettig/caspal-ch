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

  # {
  #     "Version": "2008-10-17",
  #     "Id": "PolicyForCloudFrontPrivateContent",
  #     "Statement": [
  #         {
  #             "Sid": "1",
  #             "Effect": "Allow",
  #             "Principal": {
  #                 "AWS": "arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity E3EF4ONC4GKSVM"
  #             },
  #             "Action": "s3:GetObject",
  #             "Resource": "arn:aws:s3:::caspal.ch-prod/*"
  #         }
  #     ]
  # }
  statement {
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.oai.iam_arn]
    }

    actions = [
      "s3:GetObject"
    ]

    resources = [
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


    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = ""
  default_root_object = "index.html"
  aliases             = ["caspal.ch", "www.caspal.ch"]
  #   logging_config {
  #     include_cookies = false
  #     bucket          = "mylogs.s3.amazonaws.com"
  #     prefix          = "myprefix"
  #   }

  #   aliases = ["mysite.example.com", "yoursite.example.com"]

  default_cache_behavior {
    allowed_methods        = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
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
    }

    lambda_function_association {
      event_type = "viewer-request"
      lambda_arn = aws_lambda_function.f.qualified_arn
    }


  }

  # Cache behavior with precedence 0
  #   ordered_cache_behavior {
  #     path_pattern     = "/content/immutable/*"
  #     allowed_methods  = ["GET", "HEAD", "OPTIONS"]
  #     cached_methods   = ["GET", "HEAD", "OPTIONS"]
  #     target_origin_id = local.s3_origin_id

  #     forwarded_values {
  #       query_string = false
  #       headers      = ["Origin"]

  #       cookies {
  #         forward = "none"
  #       }
  #     }

  #     min_ttl                = 0
  #     default_ttl            = 86400
  #     max_ttl                = 31536000
  #     compress               = true
  #     viewer_protocol_policy = "redirect-to-https"
  #   }

  # Cache behavior with precedence 1
  #   ordered_cache_behavior {
  #     path_pattern     = "/content/*"
  #     allowed_methods  = ["GET", "HEAD", "OPTIONS"]
  #     cached_methods   = ["GET", "HEAD"]
  #     target_origin_id = local.s3_origin_id

  #     forwarded_values {
  #       query_string = false

  #       cookies {
  #         forward = "none"
  #       }
  #     }

  #     min_ttl                = 0
  #     default_ttl            = 3600
  #     max_ttl                = 86400
  #     compress               = true
  #     viewer_protocol_policy = "redirect-to-https"
  #   }

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
    # cloudfront_default_certificate = true
    acm_certificate_arn = data.aws_acm_certificate.c.arn
    ssl_support_method  = "sni-only"
  }


}