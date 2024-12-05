# Test S3 Bucket Module

This is a simple test module that creates an S3 bucket with versioning enabled.

## Prerequisites

- AWS credentials configured
- OpenTofu installed

## Usage

Using the infra-sdk CLI:

```bash
infra create .
```

## Resources Created

- AWS S3 Bucket with a random prefix "infra-sdk-test-"
- Versioning enabled on the bucket

## Outputs

- `bucket_name`: Name of the created S3 bucket
- `bucket_arn`: ARN of the created S3 bucket
