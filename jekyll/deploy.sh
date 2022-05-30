#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

CF_DISTRIBUTION=`jq -r '(.resources[] | select(.type == "aws_cloudfront_distribution")).instances[].attributes.id' ../terraform/terraform.tfstate`
echo $CF_DISTRIBUTION

./jekyll.sh build
./update_cv_pdf.py

aws s3 sync $SCRIPT_DIR/../placeholder/ s3://caspal.ch-prod/placeholder/
aws s3 sync $SCRIPT_DIR/content/_site s3://caspal.ch-prod/caspal/

aws cloudfront create-invalidation \
    --distribution-id "$CF_DISTRIBUTION" \
    --paths "/*"