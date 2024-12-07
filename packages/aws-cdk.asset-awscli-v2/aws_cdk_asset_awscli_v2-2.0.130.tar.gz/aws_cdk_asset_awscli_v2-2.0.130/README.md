# Asset with AWS CLI v2

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

---


> This library is currently under development. Do not use!

<!--END STABILITY BANNER-->

This module exports a single class called `AwsCliAsset` which is an `s3_assets.Asset` that bundles the AWS CLI v2.

Usage:

```python
# AwsCliLayer bundles the AWS CLI in a lambda layer
from aws_cdk.asset_awscli_v2 import AwsCliAsset
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_s3_assets as s3_assets
from aws_cdk import FileSystem

# fn: lambda.Function

awscli = AwsCliAsset(self, "AwsCliCode")
fn.add_layers(lambda_.LayerVersion(self, "AwsCliLayer",
    code=lambda_.Code.from_bucket(awscli.bucket, awscli.s3_object_key)
))
```

The CLI will be installed under `/opt/awscli/aws`.
