#!/bin/bash
set -e

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR

./jekyll.sh build

aws s3 sync $SCRIPT_DIR/../placeholder/ s3://caspal.ch-prod/placeholder/
aws s3 sync $SCRIPT_DIR/content/_site s3://caspal.ch-prod/caspal/

