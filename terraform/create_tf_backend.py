import boto3
REGION = 'us-east-1'
sess = boto3.Session(region_name=REGION)

s3 = sess.resource('s3')
dynamodb = sess.resource('dynamodb')

s3_client = sess.client('s3')
dynamodb_client = sess.client('dynamodb')


def bucket_exists(name: str) -> bool:
    try:
        s3_client.head_bucket(Bucket=name)
    except s3_client.exceptions.ClientError:
        return False
    else:
        return True

def table_exists(name: str) -> bool:
    try:
        dynamodb_client.describe_table(TableName=name)
    except dynamodb_client.exceptions.ResourceNotFoundException:
        return False
    else:
        return True


def create_s3_bucket(name: str) -> None:
    if bucket_exists(name):
        return
    
    bucket = s3.Bucket(name)
    
    bucket.create(
        ACL='private'
    )
    bucket.wait_until_exists()
    bucket.Versioning().enable()


def create_ddb_table(name: str) -> None:
    if table_exists(name):
        return

    table = dynamodb.create_table(
        TableName=name,
        KeySchema=[
            {
                'AttributeName': 'LockID',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'LockID',
                'AttributeType': 'S'
            },
        ],
        BillingMode='PAY_PER_REQUEST',
    )
    table.wait_until_exists()

    
  

if __name__ == '__main__':
    bucket_name = 'caspal-terraform-state'
    table_name = 'caspal-terraform-locks'

    create_s3_bucket(bucket_name)
    create_ddb_table(table_name)

    print(f'''
terraform {{
  backend "s3" {{
    bucket = "{bucket_name}"
    key    = ""
    region = "{REGION}"
    dynamodb_table = "{table_name}"
  }}
}}
    ''')


