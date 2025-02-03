#!/bin/sh -l

S3CMD_PATH=/opt/s3cmd/s3cmd
S3CMD_CONFIG=/github/home/.s3cfg

COMMAND=$1
ACCESS_KEY=$2
SECRET_KEY=$3
ENDPOINT_URL=$4
BUCKET_LOCATION=$5

echo "access_key=$ACCESS_KEY" >> "$S3CMD_CONFIG"
echo "secret_key=$SECRET_KEY" >> "$S3CMD_CONFIG"
echo "host_base=$ENDPOINT_URL" >> "$S3CMD_CONFIG"
echo "bucket_location=$BUCKET_LOCATION" >> "$S3CMD_CONFIG"

# Run the user-provided s3cmd command (e.g., 'put file.txt s3://my-bucket')
${S3CMD_PATH} $COMMAND