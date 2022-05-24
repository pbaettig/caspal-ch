terraform {
  # This module is now only being tested with Terraform 1.1.x. However, to make upgrading easier, we are setting 1.0.0 as the minimum version.
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
}

provider "aws" {
  region = "eu-central-1"
}

provider "aws" {
  alias  = "us"
  region = "us-east-1"
}


# locals {
#   vpc_name = "caspal-prod"
# }

# data "aws_availability_zones" "all" {
#   #   state            = var.availability_zone_state
#   #   exclude_names    = var.availability_zone_exclude_names
#   #   exclude_zone_ids = var.availability_zone_exclude_ids
# }

# resource "aws_vpc" "main" {
#   cidr_block           = "10.123.0.0/16"
#   instance_tenancy     = "default"
#   enable_dns_support   = true
#   enable_dns_hostnames = true
#   tags                 = { Name = local.vpc_name }
# }

# resource "aws_subnet" "public" {
#   count = length(data.aws_availability_zones.all.names)

#   vpc_id = aws_vpc.main.id

#   # Depending on if user has requested specific availability_zone_ids, use those.
#   # Note that we use element instead of [] here for wrap around behavior
#   availability_zone = data.aws_availability_zones.all.names[count.index]

#   cidr_block              = "10.123.${40 + count.index}.0/24"
#   map_public_ip_on_launch = true
#   tags                    = { Name = "${local.vpc_name}-public-${count.index}" }
# }