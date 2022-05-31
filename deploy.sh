#!/bin/bash
set -euo pipefail

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

CF_DISTRIBUTION=`(cd $SCRIPT_DIR/terraform; terraform output -json | jq -r '.cloudfront_distribution_id.value')`
echo $CF_DISTRIBUTION

./jekyll/update_cv_pdf.py
./jekyll/jekyll.sh build


aws s3 sync $SCRIPT_DIR/placeholder/ s3://caspal.ch-prod/placeholder/
aws s3 sync $SCRIPT_DIR/jekyll/content/_site s3://caspal.ch-prod/caspal/

aws cloudfront create-invalidation \
    --distribution-id "$CF_DISTRIBUTION" \
    --paths "/*"