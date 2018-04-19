DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
aws --profile caspal s3 sync $DIR s3://caspal-bootstrap/cv --exclude "upload.sh"