#!/bin/sh -l

set -e

S3CMD_CONFIG=/github/home/.s3cfg

COMMAND=$1
ACCESS_KEY=$2
SECRET_KEY=$3
HOST_BASE=$4
BUCKET_LOCATION=$5

sed -i s\|{{BUCKET_LOCATION}}\|${BUCKET_LOCATION}\|g ${S3CMD_CONFIG}
sed -i s\|{{HOST_BASE}}\|${HOST_BASE}\|g ${S3CMD_CONFIG}
sed -i s\|{{ACCESS_KEY}}\|${ACCESS_KEY}\|g ${S3CMD_CONFIG}
sed -i s\|{{SECRET_KEY}}\|${SECRET_KEY}\|g ${S3CMD_CONFIG}

# Run the user-provided s3cmd command (e.g., 'put file.txt s3://my-bucket')
s3cmd ${COMMAND}

rm /github/home/.s3cfg