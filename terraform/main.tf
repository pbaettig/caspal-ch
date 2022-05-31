terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 2.69.0, < 4.0"
    }
    null = {
      source = "hashicorp/null"
    }
  }
  backend "s3" {
    bucket = "caspal-terraform-state"
    key    = "caspal-ch-website/"
    region = "us-east-1"
    dynamodb_table = "caspal-terraform-locks"
  }
}

provider "aws" {
  region = "eu-central-1"
}

provider "aws" {
  alias  = "us"
  region = "us-east-1"
}
