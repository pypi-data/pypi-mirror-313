r'''
<img src="https://github.com/dbsystel/cdk-sops-secrets/blob/main/img/banner-dl-small.png?raw=true">
<p/>

![stability](https://img.shields.io/badge/Stability-stable-green) 
[![release](https://github.com/dbsystel/cdk-sops-secrets/actions/workflows/release.yml/badge.svg)](https://github.com/dbsystel/cdk-sops-secrets/actions/workflows/release.yml)<br>

[![cdk-construct-hub](https://img.shields.io/badge/CDK-ConstructHub-blue)](https://constructs.dev/packages/cdk-sops-secrets)<br>
[![npm](https://img.shields.io/npm/v/cdk-sops-secrets.svg)](https://www.npmjs.com/package/cdk-sops-secrets) 
[![npm downloads](https://img.shields.io/npm/dw/cdk-sops-secrets)](https://www.npmjs.com/package/cdk-sops-secrets)<br>
[![pypi](https://img.shields.io/pypi/v/cdk-sops-secrets.svg)](https://pypi.org/project/cdk-sops-secrets) 
[![pypi downloads](https://img.shields.io/pypi/dw/cdk-sops-secrets)](https://pypi.org/project/cdk-sops-secrets)<br>

[![codecov](https://codecov.io/gh/dbsystel/cdk-sops-secrets/branch/main/graph/badge.svg?token=OT7P7HQHXB)](https://codecov.io/gh/dbsystel/cdk-sops-secrets)  
[![security-vulnerabilities](https://img.shields.io/github/issues-search/dbsystel/cdk-sops-secrets?color=%23ff0000&label=security-vulnerabilities&query=is%3Aissue%20is%3Aopen%20label%3A%22Mend%3A%20dependency%20security%20vulnerability%22)](https://github.com/dbsystel/cdk-sops-secrets/issues?q=is%3Aissue+is%3Aopen+label%3A%22security+vulnerability%22) 

## Introduction

This construct library provides a replacement for CDK SecretsManager secrets, with extended functionality for Mozilla/sops.

<p/><center><img src="img/flow.drawio.svg"></center><p/>
Using this library it is possible to populate Secrets with values from a Mozilla/sops file without additional scripts and steps in the CI stage. Thereby transformations like JSON conversion of YAML files and transformation into a flat, JSONPath like structure will be performed, but can be disabled.

Secrets filled in this way can be used immediately within the CloudFormation stack and dynamic references. This construct should handle all dependencies, if you use the `secretValueFromJson()` or `secretValue()` call to access secret values.

This way, secrets can be securely stored in git repositories and easily synchronized into AWS SecretsManager secrets.

## Stability

You can consider this package as stable. Updates will follow [Semantic Versioning](https://semver.org/).<br>
Nevertheless, I would recommend pinning the exact version of this library in your `package.json`.

## Prerequisites

* [AWS](https://aws.amazon.com/): I think you already knew it, but this construct will only work with an AWS account.

* [KMS Key](https://aws.amazon.com/kms/?nc1=h_ls): It makes most sense to encrypt your secrets with AWS KMS if you want to sync and use the secret content afterwards in your AWS account.
* [mozilla/sops](https://github.com/mozilla/sops): This construct assumes that you store your secrets encrypted via sops in your git repository.
* [CDK](https://aws.amazon.com/cdk/?nc1=h_ls): As this is a CDK construct, it's only useful if you use the CloudDevelopmentToolkit.

## Getting started

1. Create a Mozilla/sops secrets file (encrypted with an already existing KMS key) and place it somewhere in your git repository
2. Create a secret with the SopsSecret construct inside your app

   ```python
   const secret = new SopsSecret(stack, 'SopsComplexSecretJSON', {
     sopsFilePath: 'secets/sopsfile-encrypted.json',
   });
   ```
3. Optional: Access the secret via dynamic references

   ```python
   secret.secretValueFromJson('json.path.dotted.notation.accessor[0]').toString(),
   ```

## Advanced configuration examples

Even if using the main functionality should be done in 3 lines of code, there are more options to configure the constructs of this library. If you want to get an Overview of all available configuration options take a look at the [documentation at the CDK ConstructHub](https://constructs.dev/packages/cdk-sops-secrets).

The most useful settings will be explained in the further chapters:

### Binary - Just the raw file

If you have the need to just upload a sops encrypted binary file, just name your sops encrypted file *.binary, or specify the option "binary" as format.

```python
const secret = new SopsSecret(this, 'SopsComplexSecretJSON', {
  ...
  sopsFilePath: 'secrets/sopsfile-encrypted.binary',
});
```

or

```python
const secret = new SopsSecret(this, 'SopsComplexSecretJSON', {
  ...
  sopsFilePath: 'secrets/sopsfile-encrypted.something',
  sopsFileFormat: 'binary',
});
```

### Getting a specific (older version)

While creating the secret or updating the entries of a secret, the native CDK function `cdk.FileSystem.fingerprint(...)` is used to generate the version information of the AWS SecretsManager secret.
Therefore, it is possible to reference the entries from a specific AWS SecretsManager version.

```python
const versionId = cdk.FileSystem.fingerprint(`./sops/SomeSecrets.json`)
const passphrase = ecs.Secret.fromSecretsManagerVersion(secretMgmt, { versionId: versionId }, 'MY_PRIVATE_PASSPHRASE')

const container = TaskDef.addContainer('Container', {
   secrets: {
     MY_PRIVATE_PASSPHRASE: passphrase,
   },
});
```

### Default conversions and how to disable them?

As default behavior, the SopsSecret (via the SopsSync) will convert all content to JSON and flatten its structure. This is useful, because the AWS SecretsManager has some limitations if it comes to YAML and/or complex objects and decimal values. Even if you can store YAML, complex objects and even binaries in AWS SecretsManager secrets, you can't access their values via the SecretsManager API — you can only return them as is. So accessing (nested) values or values from YAML files won't be possible via [dynamic references](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html) in CloudFormation (and CDK). That's why I decided that conversion to JSON, flatten the structure and stringify all values should be the default behavior. But you can turn off all of these conversion steps:

```python
const secret = new SopsSecret(this, 'SopsComplexSecretJSON', {
  convertToJSON: false, // disable converting the encrypted content to JSON
  stringify: false, // disable stringifying all values
  flatten: false, // disable flattening of the object structure
  sopsFilePath: 'secrets/sopsfile-encrypted.json',
});
```

### Resource provider is missing permissions

Sometimes it can be necessary to access the IAM role of the SopsSync provider. If this is the case, you should create the provider before creating the SopsSecret, and pass the provider to it like this:

```python
// Create the provider
const provider = new SopsSyncProvider(this, 'CustomSopsSyncProvider');
// Grant whatever you need to the provider
const myExtraKmsKey = Key.fromKeyArn(this, 'MyExtraKmsKey', 'YourKeyArn');
myExtraKmsKey.grantDecrypt(provider);
// create the secret and pass the the provider to it
const secret = new SopsSecret(this, 'SopsComplexSecretJSON', {
  sopsProvider: provider,
  secretName: 'myCoolSecret',
  sopsFilePath: 'secrets/sopsfile-encrypted.json',
});
```

### Use a VPC for the Lambda Function

Internally, SopsSync uses a lambda function. In some environments it may be necessary to place this lambda function into a VPC and configure subnets and/or security groups for it.
This can be done by creating a custom `SopsSyncProvider`, setting the required networking configuration and passing it to the secret like this:

```python
// Create the provider
const provider = new SopsSyncProvider(this, 'CustomSopsSyncProvider', {
  vpc: myVpc,
  vpcSubnets: subnetSelection,
  securityGroups: [mySecurityGroup],
});
// create the secret and pass the the provider to it
const secret = new SopsSecret(this, 'SopsSecret', {
  sopsProvider: provider,
  secretName: 'myCoolSecret',
  sopsFilePath: 'secrets/sopsfile-encrypted.json',
});
```

### UploadType: INLINE / ASSET

I decided, that the default behavior should be "INLINE" because of the following consideration:

* Fewer permissions: If we use inline content instead of a S3 asset, the SopsSyncProvider does not need permissions to access the asset bucket and its KMS key.
* Faster: If we don't have to upload and download things from and to S3, it should be a little faster.
* Interchangeable: As we use the same information to generate the version of the secret, no new version of the secret should be created, if you change from INLINE to ASSET or vice versa, even if the CloudFormation resource updates.
* I personally think sops files are not that big, that we should run into limits, but if so — we can change to asset `uploadType`.

You can change the uplaodType via the properties:

```python
const secret = new SopsSecret(this, 'SopsWithAssetUpload', {
  sopsFilePath: 'secrets/sopsfile-encrypted.json',
  uploadType: UploadType.ASSET, // instead of the default UploadType.INLINE
});
```

## FAQ

### It does not work, what can I do?

Even if this construct has some unit and integration tests performed, there can be bugs and issues. As everything is performed by a cloudformation custom resource provider, a good starting point is the log of the corresponding lambda function. It should be located in your AWS Account under Cloudwatch -> Log groups:

`/aws/lambda/<YOUR-STACK-NAME>-SingletonLambdaSopsSyncProvider<SOMETHINGsomething1234>`

### I get errors with dotenv formatted files

Only very basic dotenv syntax is working right now. Only single line values are accepted. The format must match:

```dotenv
key=value
```

comments must be a single line, not after value assignments.

### Error getting data key: 0 successful groups required, got 0

This error message (and failed sync) is related to the  mozilla/sops issues [#948](https://github.com/mozilla/sops/issues/948) and [#634](https://github.com/mozilla/sops/issues/634). You must not create your secret with the `--aws-profile` flag. This profile will be written to your sops filed and is required in every runtime environment. You have to define the profile to use via the environment variable `AWS_PROFILE` instead, to avoid this.

### Asset of sync lambda not found

The lambda asset code is generated relative to the path of the index.ts in this package. With tools like nx this can lead to wrong results, so that the asset could not be found.

You can override the asset path via the [cdk.json](https://docs.aws.amazon.com/cdk/v2/guide/get_context_var.html) or via the flag `-c`of the cdk cli.

The context used for this override is `sops_sync_provider_asset_path`.

So for example you can use

```bash
cdk deploy -c "sops_sync_provider_asset_path=some/path/asset.zip"
```

or in your cdk.json

```json
{
  "context": {
    "sops_sync_provider_asset_path": "some/path/asset.zip"
  }
}
```

### I want to upload the sops file myself and only want to reference it

That's possible since version 1.8.0. You can reference the file in S3 like:

```python
new SopsSecret(stack, 'SopsSecret', {
  sopsS3Bucket: 'testbucket',
  sopsS3Key: 'secret.json',
  sopsFileFormat: 'json',
  // ...
});
```

Passing those values as CloudFormation parameters should also be possible:

```python

const sopsS3BucketParam = new CfnParameter(this, "s3BucketName", {
  type: "String",
  description: "The name of the Amazon S3 bucket where your sopsFile was uploaded."});

const sopsS3KeyParam = new CfnParameter(this, "s3KeyName", {
  type: "String",
  description: "The name of the key of the sopsFile inside the Amazon S3 bucket."});

new SopsSecret(stack, 'SopsSecret', {
  sopsS3Bucket: sopsS3BucketParam.valueAsString,
  sopsS3Key: sopsS3KeyParam.valueAsString,
  sopsFileFormat: 'json',
  // ...
});
```

## Motivation

I have created this project to solve a recurring problem of syncing Mozilla/sops secrets into AWS SecretsManager in a convenient, secure way.

Other than that, or perhaps more importantly, my goal was to learn new things:

* Write a Golang lambda
* Writing unit tests incl. mocks in Golang
* Reproducible builds of Golang binaries (byte-by-byte identical)
* Build reproducible zips (byte-by-byte identical)
* Release a NPM package
* Setting up projects with projen
* CI/CD with GitHub actions
* CDK unit and integration tests

## Other Tools like this

The problem this Construct addresses is so good, already two other implementations exist:

* [isotoma/sops-secretsmanager-cdk](https://github.com/isotoma/sops-secretsmanager-cdk): Does nearly the same. Uses CustomResource, wraps the sops CLI, does not support flatten. Found it after I published my solution to NPM :-/
* [taimos/secretsmanager-versioning](https://github.com/taimos/secretsmanager-versioning): Different approach on the same problem. This is a CLI tool with very nice integration into CDK and also handles git versioning information.

## License

The Apache-2.0 license. Please have a look at the [LICENSE](LICENSE) and [LICENSE-3RD-PARTY](LICENSE-3RD-PARTY).
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="cdk-sops-secrets.CreationType")
class CreationType(enum.Enum):
    SINGLE = "SINGLE"
    '''Create or update a single secret/parameter.'''
    MULTI = "MULTI"
    '''Create or update a multiple secrets/parameters by flattening the SOPS file.'''


class MultiStringParameter(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.MultiStringParameter",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        key_prefix: typing.Optional[builtins.str] = None,
        key_separator: typing.Optional[builtins.str] = None,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional["ResourceType"] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional["UploadType"] = None,
        string_value: builtins.str,
        data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
        type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType] = None,
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param key_prefix: 
        :param key_separator: 
        :param encryption_key: 
        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param string_value: The value of the parameter. It may not reference another parameter and ``{{}}`` cannot be used in the value.
        :param data_type: The data type of the parameter, such as ``text`` or ``aws:ec2:image``. Default: ParameterDataType.TEXT
        :param type: (deprecated) The type of the string parameter. Default: ParameterType.STRING
        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates if the parameter name is a simple name (i.e. does not include "/" separators). This is required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520cbd9adefd0e4a3135f2f09bd2fa26acb8be581e0f77b06f12862c0125b5b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MultiStringParameterProps(
            key_prefix=key_prefix,
            key_separator=key_separator,
            encryption_key=encryption_key,
            convert_to_json=convert_to_json,
            creation_type=creation_type,
            flatten=flatten,
            flatten_separator=flatten_separator,
            parameter_key_prefix=parameter_key_prefix,
            resource_type=resource_type,
            sops_age_key=sops_age_key,
            sops_file_format=sops_file_format,
            sops_file_path=sops_file_path,
            sops_kms_key=sops_kms_key,
            sops_provider=sops_provider,
            sops_s3_bucket=sops_s3_bucket,
            sops_s3_key=sops_s3_key,
            stringify_values=stringify_values,
            upload_type=upload_type,
            string_value=string_value,
            data_type=data_type,
            type=type,
            allowed_pattern=allowed_pattern,
            description=description,
            parameter_name=parameter_name,
            simple_name=simple_name,
            tier=tier,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> _aws_cdk_ceddda9d.ResourceEnvironment:
        return typing.cast(_aws_cdk_ceddda9d.ResourceEnvironment, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="keyPrefix")
    def key_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyPrefix"))

    @builtins.property
    @jsii.member(jsii_name="keySeparator")
    def key_separator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keySeparator"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="sync")
    def sync(self) -> "SopsSync":
        return typing.cast("SopsSync", jsii.get(self, "sync"))


@jsii.enum(jsii_type="cdk-sops-secrets.ResourceType")
class ResourceType(enum.Enum):
    SECRET = "SECRET"
    PARAMETER = "PARAMETER"


@jsii.implements(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret)
class SopsSecret(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.SopsSecret",
):
    '''A drop in replacement for the normal Secret, that is populated with the encrypted content of the given sops file.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        generate_secret_string: typing.Optional[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringGenerator, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        replica_regions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
        secret_name: typing.Optional[builtins.str] = None,
        secret_object_value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_ceddda9d.SecretValue]] = None,
        secret_string_beta1: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringValueBeta1] = None,
        secret_string_value: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[ResourceType] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional["UploadType"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: Configuration for how to generate a secret value. Only one of ``secretString`` and ``generateSecretString`` can be provided. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param removal_policy: Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param replica_regions: A list of regions where to replicate this secret. Default: - Secret is not replicated
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        :param secret_object_value: Initial value for a JSON secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret object -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies a JSON object that you want to encrypt and store in this new version of the secret. To specify a simple string value instead, use ``SecretProps.secretStringValue`` Only one of ``secretStringBeta1``, ``secretStringValue``, 'secretObjectValue', and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.
        :param secret_string_beta1: (deprecated) Initial value for the secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret string -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies text data that you want to encrypt and store in this new version of the secret. May be a simple string value, or a string representation of a JSON structure. Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.
        :param secret_string_value: Initial value for the secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret string -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies text data that you want to encrypt and store in this new version of the secret. May be a simple string value. To provide a string representation of JSON structure, use ``SecretProps.secretObjectValue`` instead. Only one of ``secretStringBeta1``, ``secretStringValue``, 'secretObjectValue', and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.
        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641b47276285e7c457eb639fea01f8b2e2f54dd58d3bc6f9e184404914516a11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SopsSecretProps(
            description=description,
            encryption_key=encryption_key,
            generate_secret_string=generate_secret_string,
            removal_policy=removal_policy,
            replica_regions=replica_regions,
            secret_name=secret_name,
            secret_object_value=secret_object_value,
            secret_string_beta1=secret_string_beta1,
            secret_string_value=secret_string_value,
            convert_to_json=convert_to_json,
            creation_type=creation_type,
            flatten=flatten,
            flatten_separator=flatten_separator,
            parameter_key_prefix=parameter_key_prefix,
            resource_type=resource_type,
            sops_age_key=sops_age_key,
            sops_file_format=sops_file_format,
            sops_file_path=sops_file_path,
            sops_kms_key=sops_kms_key,
            sops_provider=sops_provider,
            sops_s3_bucket=sops_s3_bucket,
            sops_s3_key=sops_s3_key,
            stringify_values=stringify_values,
            upload_type=upload_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRotationSchedule")
    def add_rotation_schedule(
        self,
        id: builtins.str,
        *,
        automatically_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        hosted_rotation: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.HostedRotation] = None,
        rotate_immediately_on_update: typing.Optional[builtins.bool] = None,
        rotation_lambda: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.RotationSchedule:
        '''Adds a rotation schedule to the secret.

        :param id: -
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. The minimum value is 4 hours. The maximum value is 1000 days. A value of zero (``Duration.days(0)``) will not create RotationRules. Default: Duration.days(30)
        :param hosted_rotation: Hosted rotation. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        :param rotate_immediately_on_update: Specifies whether to rotate the secret immediately or wait until the next scheduled rotation window. Default: true
        :param rotation_lambda: A Lambda function that can rotate the secret. Default: - either ``rotationLambda`` or ``hostedRotation`` must be specified
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd08508625195135b318d9657d717ca369ecceb1cc51cd6b3fa8c66c489c3dad)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_secretsmanager_ceddda9d.RotationScheduleOptions(
            automatically_after=automatically_after,
            hosted_rotation=hosted_rotation,
            rotate_immediately_on_update=rotate_immediately_on_update,
            rotation_lambda=rotation_lambda,
        )

        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.RotationSchedule, jsii.invoke(self, "addRotationSchedule", [id, options]))

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    ) -> _aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult:
        '''Adds a statement to the IAM resource policy associated with this secret.

        If this secret was created in this stack, a resource policy will be
        automatically created upon the first call to ``addToResourcePolicy``. If
        the secret is imported, then this is a no-op.

        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54076b0a3bb41bb64b3bbd471f51ee813e6ce6437b4b2ee14f76246051614126)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement]))

    @jsii.member(jsii_name="applyRemovalPolicy")
    def apply_removal_policy(self, policy: _aws_cdk_ceddda9d.RemovalPolicy) -> None:
        '''Apply the given removal policy to this resource.

        The Removal Policy controls what happens to this resource when it stops
        being managed by CloudFormation, either because you've removed it from the
        CDK application or because you've made a change that requires the resource
        to be replaced.

        The resource can be deleted (``RemovalPolicy.DESTROY``), or left in your AWS
        account for data recovery and cleanup later (``RemovalPolicy.RETAIN``).

        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85d3b1469d7d365dc715e5fc30a5ca749e3a126bab5731a9cb3e3bd09de54905)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "applyRemovalPolicy", [policy]))

    @jsii.member(jsii_name="attach")
    def attach(
        self,
        target: _aws_cdk_aws_secretsmanager_ceddda9d.ISecretAttachmentTarget,
    ) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''Attach a target to this secret.

        :param target: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7169bcc05cc9fef09daa2e6732c5c382897a8dace487c441a5df1ea46b3123fc)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.invoke(self, "attach", [target]))

    @jsii.member(jsii_name="currentVersionId")
    def current_version_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "currentVersionId", []))

    @jsii.member(jsii_name="denyAccountRootDelete")
    def deny_account_root_delete(self) -> None:
        '''Denies the ``DeleteSecret`` action to all principals within the current account.'''
        return typing.cast(None, jsii.invoke(self, "denyAccountRootDelete", []))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grants reading the secret value to some role.

        :param grantee: -
        :param version_stages: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b84d1e6becdb6cf951b358b8a8bc63f668e555a12d11b0028528af866931a1c8)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument version_stages", value=version_stages, expected_type=type_hints["version_stages"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee, version_stages]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        _grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grants writing and updating the secret value to some role.

        :param _grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fd3a17eb68d15973a8af9441eb6cd97ed5338dead66b7679f005db68637eb5f)
            check_type(argname="argument _grantee", value=_grantee, expected_type=type_hints["_grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [_grantee]))

    @jsii.member(jsii_name="secretValueFromJson")
    def secret_value_from_json(
        self,
        json_field: builtins.str,
    ) -> _aws_cdk_ceddda9d.SecretValue:
        '''Interpret the secret as a JSON object and return a field's value from it as a ``SecretValue``.

        :param json_field: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65919d041d660423e596dfdaa79882405d878d5eda9d3e1171335aa874544f9)
            check_type(argname="argument json_field", value=json_field, expected_type=type_hints["json_field"])
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, jsii.invoke(self, "secretValueFromJson", [json_field]))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> _aws_cdk_ceddda9d.ResourceEnvironment:
        '''The environment this resource belongs to.

        For resources that are created and managed by the CDK
        (generally, those created by creating new class instances like Role, Bucket, etc.),
        this is always the same as the environment of the stack they belong to;
        however, for imported resources
        (those obtained from static methods like fromRoleArn, fromBucketName, etc.),
        that might be different than the stack they were imported into.
        '''
        return typing.cast(_aws_cdk_ceddda9d.ResourceEnvironment, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        '''The ARN of the secret in AWS Secrets Manager.

        Will return the full ARN if available, otherwise a partial arn.
        For secrets imported by the deprecated ``fromSecretName``, it will return the ``secretName``.
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        '''The name of the secret.

        For "owned" secrets, this will be the full resource name (secret name + suffix), unless the
        '@aws-cdk/aws-secretsmanager:parseOwnedSecretName' feature flag is set.
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @builtins.property
    @jsii.member(jsii_name="secretValue")
    def secret_value(self) -> _aws_cdk_ceddda9d.SecretValue:
        '''Retrieve the value of the stored secret as a ``SecretValue``.'''
        return typing.cast(_aws_cdk_ceddda9d.SecretValue, jsii.get(self, "secretValue"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        '''The stack in which this resource is defined.'''
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="sync")
    def sync(self) -> "SopsSync":
        return typing.cast("SopsSync", jsii.get(self, "sync"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The customer-managed encryption key that is used to encrypt this secret, if any.

        When not specified, the default
        KMS key for the account and region is being used.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="secretFullArn")
    def secret_full_arn(self) -> typing.Optional[builtins.str]:
        '''The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix.

        This is equal to ``secretArn`` in most cases, but is undefined when a full ARN is not available (e.g., secrets imported by name).
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "secretFullArn"))


@jsii.implements(_aws_cdk_aws_ssm_ceddda9d.IStringParameter)
class SopsStringParameter(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.SopsStringParameter",
):
    '''A drop in replacement for the normal String Parameter, that is populated with the encrypted content of the given sops file.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[ResourceType] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional["UploadType"] = None,
        string_value: builtins.str,
        data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
        type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType] = None,
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption_key: 
        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param string_value: The value of the parameter. It may not reference another parameter and ``{{}}`` cannot be used in the value.
        :param data_type: The data type of the parameter, such as ``text`` or ``aws:ec2:image``. Default: ParameterDataType.TEXT
        :param type: (deprecated) The type of the string parameter. Default: ParameterType.STRING
        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates if the parameter name is a simple name (i.e. does not include "/" separators). This is required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18c9bb48fa41cbb41be59793bbe0b888d5730c69b1bf3580c6c19d7d6be65d8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SopsStringParameterProps(
            encryption_key=encryption_key,
            convert_to_json=convert_to_json,
            creation_type=creation_type,
            flatten=flatten,
            flatten_separator=flatten_separator,
            parameter_key_prefix=parameter_key_prefix,
            resource_type=resource_type,
            sops_age_key=sops_age_key,
            sops_file_format=sops_file_format,
            sops_file_path=sops_file_path,
            sops_kms_key=sops_kms_key,
            sops_provider=sops_provider,
            sops_s3_bucket=sops_s3_bucket,
            sops_s3_key=sops_s3_key,
            stringify_values=stringify_values,
            upload_type=upload_type,
            string_value=string_value,
            data_type=data_type,
            type=type,
            allowed_pattern=allowed_pattern,
            description=description,
            parameter_name=parameter_name,
            simple_name=simple_name,
            tier=tier,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="applyRemovalPolicy")
    def apply_removal_policy(self, policy: _aws_cdk_ceddda9d.RemovalPolicy) -> None:
        '''Apply the given removal policy to this resource.

        The Removal Policy controls what happens to this resource when it stops
        being managed by CloudFormation, either because you've removed it from the
        CDK application or because you've made a change that requires the resource
        to be replaced.

        The resource can be deleted (``RemovalPolicy.DESTROY``), or left in your AWS
        account for data recovery and cleanup later (``RemovalPolicy.RETAIN``).

        :param policy: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3df10361f8a5b128d2433c218086d617e482ecd374cb8020cdc94262ee0764ad)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "applyRemovalPolicy", [policy]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grants read (DescribeParameter, GetParameters, GetParameter, GetParameterHistory) permissions on the SSM Parameter.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77542577a7e47c1c7b3090197d5a0c6f281fe2b6578631e3d20a4d286277d0ff)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''Grants write (PutParameter) permissions on the SSM Parameter.

        :param grantee: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96018dc2f4a57e7a385eced7113b3297dcd94c0473ff9eb0d54ebc35edd378de)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> _aws_cdk_ceddda9d.ResourceEnvironment:
        '''The environment this resource belongs to.

        For resources that are created and managed by the CDK
        (generally, those created by creating new class instances like Role, Bucket, etc.),
        this is always the same as the environment of the stack they belong to;
        however, for imported resources
        (those obtained from static methods like fromRoleArn, fromBucketName, etc.),
        that might be different than the stack they were imported into.
        '''
        return typing.cast(_aws_cdk_ceddda9d.ResourceEnvironment, jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> builtins.str:
        '''The ARN of the SSM Parameter resource.'''
        return typing.cast(builtins.str, jsii.get(self, "parameterArn"))

    @builtins.property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> builtins.str:
        '''The name of the SSM Parameter resource.'''
        return typing.cast(builtins.str, jsii.get(self, "parameterName"))

    @builtins.property
    @jsii.member(jsii_name="parameterType")
    def parameter_type(self) -> builtins.str:
        '''The type of the SSM Parameter resource.'''
        return typing.cast(builtins.str, jsii.get(self, "parameterType"))

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _aws_cdk_ceddda9d.Stack:
        '''The stack in which this resource is defined.'''
        return typing.cast(_aws_cdk_ceddda9d.Stack, jsii.get(self, "stack"))

    @builtins.property
    @jsii.member(jsii_name="stringValue")
    def string_value(self) -> builtins.str:
        '''The parameter value.

        Value must not nest another parameter. Do not use {{}} in the value.
        '''
        return typing.cast(builtins.str, jsii.get(self, "stringValue"))

    @builtins.property
    @jsii.member(jsii_name="sync")
    def sync(self) -> "SopsSync":
        return typing.cast("SopsSync", jsii.get(self, "sync"))


class SopsSync(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.SopsSync",
):
    '''The custom resource, that is syncing the content from a sops file to a secret.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        parameter_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[ResourceType] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional["UploadType"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param encryption_key: The encryption key used for encrypting the ssm parameter if ``parameterName`` is set.
        :param parameter_name: The parameter name. If set this creates an encrypted SSM Parameter instead of a secret.
        :param parameter_names: The parameter name. If set this creates an encrypted SSM Parameter instead of a secret.
        :param secret: The secret that will be populated with the encrypted sops file content.
        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b3134de7215a676a4feb3291975d227477d2dc9d5914405b8ab165ac30d7bad)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SopsSyncProps(
            encryption_key=encryption_key,
            parameter_name=parameter_name,
            parameter_names=parameter_names,
            secret=secret,
            convert_to_json=convert_to_json,
            creation_type=creation_type,
            flatten=flatten,
            flatten_separator=flatten_separator,
            parameter_key_prefix=parameter_key_prefix,
            resource_type=resource_type,
            sops_age_key=sops_age_key,
            sops_file_format=sops_file_format,
            sops_file_path=sops_file_path,
            sops_kms_key=sops_kms_key,
            sops_provider=sops_provider,
            sops_s3_bucket=sops_s3_bucket,
            sops_s3_key=sops_s3_key,
            stringify_values=stringify_values,
            upload_type=upload_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="converToJSON")
    def conver_to_json(self) -> builtins.bool:
        '''Was the format converted to json?'''
        return typing.cast(builtins.bool, jsii.get(self, "converToJSON"))

    @builtins.property
    @jsii.member(jsii_name="flatten")
    def flatten(self) -> builtins.bool:
        '''Was the structure flattened?'''
        return typing.cast(builtins.bool, jsii.get(self, "flatten"))

    @builtins.property
    @jsii.member(jsii_name="stringifiedValues")
    def stringified_values(self) -> builtins.bool:
        '''Were the values stringified?'''
        return typing.cast(builtins.bool, jsii.get(self, "stringifiedValues"))

    @builtins.property
    @jsii.member(jsii_name="versionId")
    def version_id(self) -> builtins.str:
        '''The current versionId of the secret populated via this resource.'''
        return typing.cast(builtins.str, jsii.get(self, "versionId"))


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsSyncOptions",
    jsii_struct_bases=[],
    name_mapping={
        "convert_to_json": "convertToJSON",
        "creation_type": "creationType",
        "flatten": "flatten",
        "flatten_separator": "flattenSeparator",
        "parameter_key_prefix": "parameterKeyPrefix",
        "resource_type": "resourceType",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "stringify_values": "stringifyValues",
        "upload_type": "uploadType",
    },
)
class SopsSyncOptions:
    def __init__(
        self,
        *,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[ResourceType] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional["UploadType"] = None,
    ) -> None:
        '''Configuration options for the SopsSync.

        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e7f5d5a68ee1675b645864f7bab39e30d7c7922956c69686578f4d6fb05723)
            check_type(argname="argument convert_to_json", value=convert_to_json, expected_type=type_hints["convert_to_json"])
            check_type(argname="argument creation_type", value=creation_type, expected_type=type_hints["creation_type"])
            check_type(argname="argument flatten", value=flatten, expected_type=type_hints["flatten"])
            check_type(argname="argument flatten_separator", value=flatten_separator, expected_type=type_hints["flatten_separator"])
            check_type(argname="argument parameter_key_prefix", value=parameter_key_prefix, expected_type=type_hints["parameter_key_prefix"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument stringify_values", value=stringify_values, expected_type=type_hints["stringify_values"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if convert_to_json is not None:
            self._values["convert_to_json"] = convert_to_json
        if creation_type is not None:
            self._values["creation_type"] = creation_type
        if flatten is not None:
            self._values["flatten"] = flatten
        if flatten_separator is not None:
            self._values["flatten_separator"] = flatten_separator
        if parameter_key_prefix is not None:
            self._values["parameter_key_prefix"] = parameter_key_prefix
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if stringify_values is not None:
            self._values["stringify_values"] = stringify_values
        if upload_type is not None:
            self._values["upload_type"] = upload_type

    @builtins.property
    def convert_to_json(self) -> typing.Optional[builtins.bool]:
        '''Should the encrypted sops value should be converted to JSON?

        Only JSON can be handled by cloud formations dynamic references.

        :default: true
        '''
        result = self._values.get("convert_to_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def creation_type(self) -> typing.Optional[CreationType]:
        result = self._values.get("creation_type")
        return typing.cast(typing.Optional[CreationType], result)

    @builtins.property
    def flatten(self) -> typing.Optional[builtins.bool]:
        '''Should the structure be flattened?

        The result will be a flat structure and all
        object keys will be replaced with the full jsonpath as key.
        This is usefull for dynamic references, as those don't support nested objects.

        :default: true
        '''
        result = self._values.get("flatten")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flatten_separator(self) -> typing.Optional[builtins.str]:
        '''If the structure should be flattened use the provided separator between keys.

        :default: '.'
        '''
        result = self._values.get("flatten_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Add this prefix to parameter names.'''
        result = self._values.get("parameter_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[ResourceType]:
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[ResourceType], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional["SopsSyncProvider"]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional["SopsSyncProvider"], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stringify_values(self) -> typing.Optional[builtins.bool]:
        '''Shall all values be flattened?

        This is usefull for dynamic references, as there
        are lookup errors for certain float types
        '''
        result = self._values.get("stringify_values")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def upload_type(self) -> typing.Optional["UploadType"]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional["UploadType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsSyncOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsSyncProps",
    jsii_struct_bases=[SopsSyncOptions],
    name_mapping={
        "convert_to_json": "convertToJSON",
        "creation_type": "creationType",
        "flatten": "flatten",
        "flatten_separator": "flattenSeparator",
        "parameter_key_prefix": "parameterKeyPrefix",
        "resource_type": "resourceType",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "stringify_values": "stringifyValues",
        "upload_type": "uploadType",
        "encryption_key": "encryptionKey",
        "parameter_name": "parameterName",
        "parameter_names": "parameterNames",
        "secret": "secret",
    },
)
class SopsSyncProps(SopsSyncOptions):
    def __init__(
        self,
        *,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[ResourceType] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional["SopsSyncProvider"] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional["UploadType"] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        parameter_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    ) -> None:
        '''The configuration options extended by the target Secret.

        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param encryption_key: The encryption key used for encrypting the ssm parameter if ``parameterName`` is set.
        :param parameter_name: The parameter name. If set this creates an encrypted SSM Parameter instead of a secret.
        :param parameter_names: The parameter name. If set this creates an encrypted SSM Parameter instead of a secret.
        :param secret: The secret that will be populated with the encrypted sops file content.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3baaf21b8ae44e7f4d83d5677857cc4141222b3d41237073b75dca6d425c2c34)
            check_type(argname="argument convert_to_json", value=convert_to_json, expected_type=type_hints["convert_to_json"])
            check_type(argname="argument creation_type", value=creation_type, expected_type=type_hints["creation_type"])
            check_type(argname="argument flatten", value=flatten, expected_type=type_hints["flatten"])
            check_type(argname="argument flatten_separator", value=flatten_separator, expected_type=type_hints["flatten_separator"])
            check_type(argname="argument parameter_key_prefix", value=parameter_key_prefix, expected_type=type_hints["parameter_key_prefix"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument stringify_values", value=stringify_values, expected_type=type_hints["stringify_values"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument parameter_names", value=parameter_names, expected_type=type_hints["parameter_names"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if convert_to_json is not None:
            self._values["convert_to_json"] = convert_to_json
        if creation_type is not None:
            self._values["creation_type"] = creation_type
        if flatten is not None:
            self._values["flatten"] = flatten
        if flatten_separator is not None:
            self._values["flatten_separator"] = flatten_separator
        if parameter_key_prefix is not None:
            self._values["parameter_key_prefix"] = parameter_key_prefix
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if stringify_values is not None:
            self._values["stringify_values"] = stringify_values
        if upload_type is not None:
            self._values["upload_type"] = upload_type
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if parameter_name is not None:
            self._values["parameter_name"] = parameter_name
        if parameter_names is not None:
            self._values["parameter_names"] = parameter_names
        if secret is not None:
            self._values["secret"] = secret

    @builtins.property
    def convert_to_json(self) -> typing.Optional[builtins.bool]:
        '''Should the encrypted sops value should be converted to JSON?

        Only JSON can be handled by cloud formations dynamic references.

        :default: true
        '''
        result = self._values.get("convert_to_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def creation_type(self) -> typing.Optional[CreationType]:
        result = self._values.get("creation_type")
        return typing.cast(typing.Optional[CreationType], result)

    @builtins.property
    def flatten(self) -> typing.Optional[builtins.bool]:
        '''Should the structure be flattened?

        The result will be a flat structure and all
        object keys will be replaced with the full jsonpath as key.
        This is usefull for dynamic references, as those don't support nested objects.

        :default: true
        '''
        result = self._values.get("flatten")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flatten_separator(self) -> typing.Optional[builtins.str]:
        '''If the structure should be flattened use the provided separator between keys.

        :default: '.'
        '''
        result = self._values.get("flatten_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Add this prefix to parameter names.'''
        result = self._values.get("parameter_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[ResourceType]:
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[ResourceType], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional["SopsSyncProvider"]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional["SopsSyncProvider"], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stringify_values(self) -> typing.Optional[builtins.bool]:
        '''Shall all values be flattened?

        This is usefull for dynamic references, as there
        are lookup errors for certain float types
        '''
        result = self._values.get("stringify_values")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def upload_type(self) -> typing.Optional["UploadType"]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional["UploadType"], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The encryption key used for encrypting the ssm parameter if ``parameterName`` is set.'''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def parameter_name(self) -> typing.Optional[builtins.str]:
        '''The parameter name.

        If set this creates an encrypted SSM Parameter instead of a secret.
        '''
        result = self._values.get("parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The parameter name.

        If set this creates an encrypted SSM Parameter instead of a secret.
        '''
        result = self._values.get("parameter_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def secret(self) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret]:
        '''The secret that will be populated with the encrypted sops file content.'''
        result = self._values.get("secret")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsSyncProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iam_ceddda9d.IGrantable)
class SopsSyncProvider(
    _aws_cdk_aws_lambda_ceddda9d.SingletonFunction,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-sops-secrets.SopsSyncProvider",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: typing.Optional[builtins.str] = None,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param security_groups: Only if ``vpc`` is supplied: The list of security groups to associate with the Lambda's network interfaces. Default: - A dedicated security group will be created for the lambda function.
        :param vpc: VPC network to place Lambda network interfaces. Default: - Lambda function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Default: - Subnets will be chosen automatically.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2ccd4bddb65030756f5b6473575c1a4cc9c9ef0202c6dbe31603b006c05734)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SopsSyncProviderProps(
            security_groups=security_groups, vpc=vpc, vpc_subnets=vpc_subnets
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addAgeKey")
    def add_age_key(self, key: _aws_cdk_ceddda9d.SecretValue) -> None:
        '''
        :param key: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2a1da09ecfa1b4ae9738b2c30c913950581a07762445e7b2bb6fc32606a17d)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast(None, jsii.invoke(self, "addAgeKey", [key]))


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsSyncProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_groups": "securityGroups",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class SopsSyncProviderProps:
    def __init__(
        self,
        *,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Configuration options for a custom SopsSyncProvider.

        :param security_groups: Only if ``vpc`` is supplied: The list of security groups to associate with the Lambda's network interfaces. Default: - A dedicated security group will be created for the lambda function.
        :param vpc: VPC network to place Lambda network interfaces. Default: - Lambda function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Default: - Subnets will be chosen automatically.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1cafbc66169426f4b5af87376d7258f7064772025b196978a5b2312e359079)
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''Only if ``vpc`` is supplied: The list of security groups to associate with the Lambda's network interfaces.

        :default: - A dedicated security group will be created for the lambda function.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''VPC network to place Lambda network interfaces.

        :default: - Lambda function is not placed within a VPC.
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where to place the network interfaces within the VPC.

        :default: - Subnets will be chosen automatically.
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsSyncProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-sops-secrets.UploadType")
class UploadType(enum.Enum):
    INLINE = "INLINE"
    '''Pass the secret data inline (base64 encoded and compressed).'''
    ASSET = "ASSET"
    '''Uplaod the secert data as asset.'''


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsSecretProps",
    jsii_struct_bases=[
        _aws_cdk_aws_secretsmanager_ceddda9d.SecretProps, SopsSyncOptions
    ],
    name_mapping={
        "description": "description",
        "encryption_key": "encryptionKey",
        "generate_secret_string": "generateSecretString",
        "removal_policy": "removalPolicy",
        "replica_regions": "replicaRegions",
        "secret_name": "secretName",
        "secret_object_value": "secretObjectValue",
        "secret_string_beta1": "secretStringBeta1",
        "secret_string_value": "secretStringValue",
        "convert_to_json": "convertToJSON",
        "creation_type": "creationType",
        "flatten": "flatten",
        "flatten_separator": "flattenSeparator",
        "parameter_key_prefix": "parameterKeyPrefix",
        "resource_type": "resourceType",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "stringify_values": "stringifyValues",
        "upload_type": "uploadType",
    },
)
class SopsSecretProps(
    _aws_cdk_aws_secretsmanager_ceddda9d.SecretProps,
    SopsSyncOptions,
):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        generate_secret_string: typing.Optional[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringGenerator, typing.Dict[builtins.str, typing.Any]]] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        replica_regions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
        secret_name: typing.Optional[builtins.str] = None,
        secret_object_value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_ceddda9d.SecretValue]] = None,
        secret_string_beta1: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringValueBeta1] = None,
        secret_string_value: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[ResourceType] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional[SopsSyncProvider] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional[UploadType] = None,
    ) -> None:
        '''The configuration options of the SopsSecret.

        :param description: An optional, human-friendly description of the secret. Default: - No description.
        :param encryption_key: The customer-managed encryption key to use for encrypting the secret value. Default: - A default KMS key for the account and region is used.
        :param generate_secret_string: Configuration for how to generate a secret value. Only one of ``secretString`` and ``generateSecretString`` can be provided. Default: - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each category), per the default values of ``SecretStringGenerator``.
        :param removal_policy: Policy to apply when the secret is removed from this stack. Default: - Not set.
        :param replica_regions: A list of regions where to replicate this secret. Default: - Secret is not replicated
        :param secret_name: A name for the secret. Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to 30 days blackout period. During that period, it is not possible to create another secret that shares the same name. Default: - A name is generated by CloudFormation.
        :param secret_object_value: Initial value for a JSON secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret object -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies a JSON object that you want to encrypt and store in this new version of the secret. To specify a simple string value instead, use ``SecretProps.secretStringValue`` Only one of ``secretStringBeta1``, ``secretStringValue``, 'secretObjectValue', and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.
        :param secret_string_beta1: (deprecated) Initial value for the secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret string -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies text data that you want to encrypt and store in this new version of the secret. May be a simple string value, or a string representation of a JSON structure. Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.
        :param secret_string_value: Initial value for the secret. **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value. The secret string -- if provided -- will be included in the output of the cdk as part of synthesis, and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access to the CloudFormation template (via the AWS Console, SDKs, or CLI). Specifies text data that you want to encrypt and store in this new version of the secret. May be a simple string value. To provide a string representation of JSON structure, use ``SecretProps.secretObjectValue`` instead. Only one of ``secretStringBeta1``, ``secretStringValue``, 'secretObjectValue', and ``generateSecretString`` can be provided. Default: - SecretsManager generates a new secret value.
        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        '''
        if isinstance(generate_secret_string, dict):
            generate_secret_string = _aws_cdk_aws_secretsmanager_ceddda9d.SecretStringGenerator(**generate_secret_string)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5ff836a3767bbc726a1167e9f5e789f0fad2dcaf72b41a245494f0a121a8a3)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument generate_secret_string", value=generate_secret_string, expected_type=type_hints["generate_secret_string"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument replica_regions", value=replica_regions, expected_type=type_hints["replica_regions"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument secret_object_value", value=secret_object_value, expected_type=type_hints["secret_object_value"])
            check_type(argname="argument secret_string_beta1", value=secret_string_beta1, expected_type=type_hints["secret_string_beta1"])
            check_type(argname="argument secret_string_value", value=secret_string_value, expected_type=type_hints["secret_string_value"])
            check_type(argname="argument convert_to_json", value=convert_to_json, expected_type=type_hints["convert_to_json"])
            check_type(argname="argument creation_type", value=creation_type, expected_type=type_hints["creation_type"])
            check_type(argname="argument flatten", value=flatten, expected_type=type_hints["flatten"])
            check_type(argname="argument flatten_separator", value=flatten_separator, expected_type=type_hints["flatten_separator"])
            check_type(argname="argument parameter_key_prefix", value=parameter_key_prefix, expected_type=type_hints["parameter_key_prefix"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument stringify_values", value=stringify_values, expected_type=type_hints["stringify_values"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if generate_secret_string is not None:
            self._values["generate_secret_string"] = generate_secret_string
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if replica_regions is not None:
            self._values["replica_regions"] = replica_regions
        if secret_name is not None:
            self._values["secret_name"] = secret_name
        if secret_object_value is not None:
            self._values["secret_object_value"] = secret_object_value
        if secret_string_beta1 is not None:
            self._values["secret_string_beta1"] = secret_string_beta1
        if secret_string_value is not None:
            self._values["secret_string_value"] = secret_string_value
        if convert_to_json is not None:
            self._values["convert_to_json"] = convert_to_json
        if creation_type is not None:
            self._values["creation_type"] = creation_type
        if flatten is not None:
            self._values["flatten"] = flatten
        if flatten_separator is not None:
            self._values["flatten_separator"] = flatten_separator
        if parameter_key_prefix is not None:
            self._values["parameter_key_prefix"] = parameter_key_prefix
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if stringify_values is not None:
            self._values["stringify_values"] = stringify_values
        if upload_type is not None:
            self._values["upload_type"] = upload_type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional, human-friendly description of the secret.

        :default: - No description.
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''The customer-managed encryption key to use for encrypting the secret value.

        :default: - A default KMS key for the account and region is used.
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def generate_secret_string(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringGenerator]:
        '''Configuration for how to generate a secret value.

        Only one of ``secretString`` and ``generateSecretString`` can be provided.

        :default:

        - 32 characters with upper-case letters, lower-case letters, punctuation and numbers (at least one from each
        category), per the default values of ``SecretStringGenerator``.
        '''
        result = self._values.get("generate_secret_string")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringGenerator], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''Policy to apply when the secret is removed from this stack.

        :default: - Not set.
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def replica_regions(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion]]:
        '''A list of regions where to replicate this secret.

        :default: - Secret is not replicated
        '''
        result = self._values.get("replica_regions")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion]], result)

    @builtins.property
    def secret_name(self) -> typing.Optional[builtins.str]:
        '''A name for the secret.

        Note that deleting secrets from SecretsManager does not happen immediately, but after a 7 to
        30 days blackout period. During that period, it is not possible to create another secret that shares the same name.

        :default: - A name is generated by CloudFormation.
        '''
        result = self._values.get("secret_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_object_value(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _aws_cdk_ceddda9d.SecretValue]]:
        '''Initial value for a JSON secret.

        **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value.
        The secret object -- if provided -- will be included in the output of the cdk as part of synthesis,
        and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to
        another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access
        to the CloudFormation template (via the AWS Console, SDKs, or CLI).

        Specifies a JSON object that you want to encrypt and store in this new version of the secret.
        To specify a simple string value instead, use ``SecretProps.secretStringValue``

        Only one of ``secretStringBeta1``, ``secretStringValue``, 'secretObjectValue', and ``generateSecretString`` can be provided.

        :default: - SecretsManager generates a new secret value.

        Example::

            declare const user: iam.User;
            declare const accessKey: iam.AccessKey;
            declare const stack: Stack;
            new secretsmanager.Secret(stack, 'JSONSecret', {
              secretObjectValue: {
                username: SecretValue.unsafePlainText(user.userName), // intrinsic reference, not exposed as plaintext
                database: SecretValue.unsafePlainText('foo'), // rendered as plain text, but not a secret
                password: accessKey.secretAccessKey, // SecretValue
              },
            });
        '''
        result = self._values.get("secret_object_value")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _aws_cdk_ceddda9d.SecretValue]], result)

    @builtins.property
    def secret_string_beta1(
        self,
    ) -> typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringValueBeta1]:
        '''(deprecated) Initial value for the secret.

        **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value.
        The secret string -- if provided -- will be included in the output of the cdk as part of synthesis,
        and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to
        another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access
        to the CloudFormation template (via the AWS Console, SDKs, or CLI).

        Specifies text data that you want to encrypt and store in this new version of the secret.
        May be a simple string value, or a string representation of a JSON structure.

        Only one of ``secretStringBeta1``, ``secretStringValue``, and ``generateSecretString`` can be provided.

        :default: - SecretsManager generates a new secret value.

        :deprecated: Use ``secretStringValue`` instead.

        :stability: deprecated
        '''
        result = self._values.get("secret_string_beta1")
        return typing.cast(typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringValueBeta1], result)

    @builtins.property
    def secret_string_value(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''Initial value for the secret.

        **NOTE:** *It is **highly** encouraged to leave this field undefined and allow SecretsManager to create the secret value.
        The secret string -- if provided -- will be included in the output of the cdk as part of synthesis,
        and will appear in the CloudFormation template in the console. This can be secure(-ish) if that value is merely reference to
        another resource (or one of its attributes), but if the value is a plaintext string, it will be visible to anyone with access
        to the CloudFormation template (via the AWS Console, SDKs, or CLI).

        Specifies text data that you want to encrypt and store in this new version of the secret.
        May be a simple string value. To provide a string representation of JSON structure, use ``SecretProps.secretObjectValue`` instead.

        Only one of ``secretStringBeta1``, ``secretStringValue``, 'secretObjectValue', and ``generateSecretString`` can be provided.

        :default: - SecretsManager generates a new secret value.
        '''
        result = self._values.get("secret_string_value")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def convert_to_json(self) -> typing.Optional[builtins.bool]:
        '''Should the encrypted sops value should be converted to JSON?

        Only JSON can be handled by cloud formations dynamic references.

        :default: true
        '''
        result = self._values.get("convert_to_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def creation_type(self) -> typing.Optional[CreationType]:
        result = self._values.get("creation_type")
        return typing.cast(typing.Optional[CreationType], result)

    @builtins.property
    def flatten(self) -> typing.Optional[builtins.bool]:
        '''Should the structure be flattened?

        The result will be a flat structure and all
        object keys will be replaced with the full jsonpath as key.
        This is usefull for dynamic references, as those don't support nested objects.

        :default: true
        '''
        result = self._values.get("flatten")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flatten_separator(self) -> typing.Optional[builtins.str]:
        '''If the structure should be flattened use the provided separator between keys.

        :default: '.'
        '''
        result = self._values.get("flatten_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Add this prefix to parameter names.'''
        result = self._values.get("parameter_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[ResourceType]:
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[ResourceType], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional[SopsSyncProvider]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional[SopsSyncProvider], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stringify_values(self) -> typing.Optional[builtins.bool]:
        '''Shall all values be flattened?

        This is usefull for dynamic references, as there
        are lookup errors for certain float types
        '''
        result = self._values.get("stringify_values")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def upload_type(self) -> typing.Optional[UploadType]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional[UploadType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-sops-secrets.SopsStringParameterProps",
    jsii_struct_bases=[
        SopsSyncOptions, _aws_cdk_aws_ssm_ceddda9d.StringParameterProps
    ],
    name_mapping={
        "convert_to_json": "convertToJSON",
        "creation_type": "creationType",
        "flatten": "flatten",
        "flatten_separator": "flattenSeparator",
        "parameter_key_prefix": "parameterKeyPrefix",
        "resource_type": "resourceType",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "stringify_values": "stringifyValues",
        "upload_type": "uploadType",
        "allowed_pattern": "allowedPattern",
        "description": "description",
        "parameter_name": "parameterName",
        "simple_name": "simpleName",
        "tier": "tier",
        "string_value": "stringValue",
        "data_type": "dataType",
        "type": "type",
        "encryption_key": "encryptionKey",
    },
)
class SopsStringParameterProps(
    SopsSyncOptions,
    _aws_cdk_aws_ssm_ceddda9d.StringParameterProps,
):
    def __init__(
        self,
        *,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[ResourceType] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional[SopsSyncProvider] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional[UploadType] = None,
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
        string_value: builtins.str,
        data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
        type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType] = None,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    ) -> None:
        '''The configuration options of the StringParameter.

        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates if the parameter name is a simple name (i.e. does not include "/" separators). This is required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        :param string_value: The value of the parameter. It may not reference another parameter and ``{{}}`` cannot be used in the value.
        :param data_type: The data type of the parameter, such as ``text`` or ``aws:ec2:image``. Default: ParameterDataType.TEXT
        :param type: (deprecated) The type of the string parameter. Default: ParameterType.STRING
        :param encryption_key: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d4c6b41b250704c51710cadcac0559f659733c6085f47a56587b680e5275a68)
            check_type(argname="argument convert_to_json", value=convert_to_json, expected_type=type_hints["convert_to_json"])
            check_type(argname="argument creation_type", value=creation_type, expected_type=type_hints["creation_type"])
            check_type(argname="argument flatten", value=flatten, expected_type=type_hints["flatten"])
            check_type(argname="argument flatten_separator", value=flatten_separator, expected_type=type_hints["flatten_separator"])
            check_type(argname="argument parameter_key_prefix", value=parameter_key_prefix, expected_type=type_hints["parameter_key_prefix"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument stringify_values", value=stringify_values, expected_type=type_hints["stringify_values"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
            check_type(argname="argument allowed_pattern", value=allowed_pattern, expected_type=type_hints["allowed_pattern"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument simple_name", value=simple_name, expected_type=type_hints["simple_name"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "string_value": string_value,
            "encryption_key": encryption_key,
        }
        if convert_to_json is not None:
            self._values["convert_to_json"] = convert_to_json
        if creation_type is not None:
            self._values["creation_type"] = creation_type
        if flatten is not None:
            self._values["flatten"] = flatten
        if flatten_separator is not None:
            self._values["flatten_separator"] = flatten_separator
        if parameter_key_prefix is not None:
            self._values["parameter_key_prefix"] = parameter_key_prefix
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if stringify_values is not None:
            self._values["stringify_values"] = stringify_values
        if upload_type is not None:
            self._values["upload_type"] = upload_type
        if allowed_pattern is not None:
            self._values["allowed_pattern"] = allowed_pattern
        if description is not None:
            self._values["description"] = description
        if parameter_name is not None:
            self._values["parameter_name"] = parameter_name
        if simple_name is not None:
            self._values["simple_name"] = simple_name
        if tier is not None:
            self._values["tier"] = tier
        if data_type is not None:
            self._values["data_type"] = data_type
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def convert_to_json(self) -> typing.Optional[builtins.bool]:
        '''Should the encrypted sops value should be converted to JSON?

        Only JSON can be handled by cloud formations dynamic references.

        :default: true
        '''
        result = self._values.get("convert_to_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def creation_type(self) -> typing.Optional[CreationType]:
        result = self._values.get("creation_type")
        return typing.cast(typing.Optional[CreationType], result)

    @builtins.property
    def flatten(self) -> typing.Optional[builtins.bool]:
        '''Should the structure be flattened?

        The result will be a flat structure and all
        object keys will be replaced with the full jsonpath as key.
        This is usefull for dynamic references, as those don't support nested objects.

        :default: true
        '''
        result = self._values.get("flatten")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flatten_separator(self) -> typing.Optional[builtins.str]:
        '''If the structure should be flattened use the provided separator between keys.

        :default: '.'
        '''
        result = self._values.get("flatten_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Add this prefix to parameter names.'''
        result = self._values.get("parameter_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[ResourceType]:
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[ResourceType], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional[SopsSyncProvider]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional[SopsSyncProvider], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stringify_values(self) -> typing.Optional[builtins.bool]:
        '''Shall all values be flattened?

        This is usefull for dynamic references, as there
        are lookup errors for certain float types
        '''
        result = self._values.get("stringify_values")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def upload_type(self) -> typing.Optional[UploadType]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional[UploadType], result)

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        '''A regular expression used to validate the parameter value.

        For example, for String types with values restricted to
        numbers, you can specify the following: ``^\\d+$``

        :default: no validation is performed
        '''
        result = self._values.get("allowed_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Information about the parameter that you want to add to the system.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter.

        :default: - a name will be generated by CloudFormation
        '''
        result = self._values.get("parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def simple_name(self) -> typing.Optional[builtins.bool]:
        '''Indicates if the parameter name is a simple name (i.e. does not include "/" separators).

        This is required only if ``parameterName`` is a token, which means we
        are unable to detect if the name is simple or "path-like" for the purpose
        of rendering SSM parameter ARNs.

        If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or
        undefined) since the name generated by AWS CloudFormation is always a
        simple name.

        :default: - auto-detect based on ``parameterName``
        '''
        result = self._values.get("simple_name")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tier(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier]:
        '''The tier of the string parameter.

        :default: - undefined
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier], result)

    @builtins.property
    def string_value(self) -> builtins.str:
        '''The value of the parameter.

        It may not reference another parameter and ``{{}}`` cannot be used in the value.
        '''
        result = self._values.get("string_value")
        assert result is not None, "Required property 'string_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_type(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType]:
        '''The data type of the parameter, such as ``text`` or ``aws:ec2:image``.

        :default: ParameterDataType.TEXT
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType], result)

    @builtins.property
    def type(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType]:
        '''(deprecated) The type of the string parameter.

        :default: ParameterType.STRING

        :deprecated: - type will always be 'String'

        :stability: deprecated
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType], result)

    @builtins.property
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        result = self._values.get("encryption_key")
        assert result is not None, "Required property 'encryption_key' is missing"
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SopsStringParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-sops-secrets.MultiStringParameterProps",
    jsii_struct_bases=[SopsStringParameterProps],
    name_mapping={
        "convert_to_json": "convertToJSON",
        "creation_type": "creationType",
        "flatten": "flatten",
        "flatten_separator": "flattenSeparator",
        "parameter_key_prefix": "parameterKeyPrefix",
        "resource_type": "resourceType",
        "sops_age_key": "sopsAgeKey",
        "sops_file_format": "sopsFileFormat",
        "sops_file_path": "sopsFilePath",
        "sops_kms_key": "sopsKmsKey",
        "sops_provider": "sopsProvider",
        "sops_s3_bucket": "sopsS3Bucket",
        "sops_s3_key": "sopsS3Key",
        "stringify_values": "stringifyValues",
        "upload_type": "uploadType",
        "allowed_pattern": "allowedPattern",
        "description": "description",
        "parameter_name": "parameterName",
        "simple_name": "simpleName",
        "tier": "tier",
        "string_value": "stringValue",
        "data_type": "dataType",
        "type": "type",
        "encryption_key": "encryptionKey",
        "key_prefix": "keyPrefix",
        "key_separator": "keySeparator",
    },
)
class MultiStringParameterProps(SopsStringParameterProps):
    def __init__(
        self,
        *,
        convert_to_json: typing.Optional[builtins.bool] = None,
        creation_type: typing.Optional[CreationType] = None,
        flatten: typing.Optional[builtins.bool] = None,
        flatten_separator: typing.Optional[builtins.str] = None,
        parameter_key_prefix: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[ResourceType] = None,
        sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
        sops_file_format: typing.Optional[builtins.str] = None,
        sops_file_path: typing.Optional[builtins.str] = None,
        sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
        sops_provider: typing.Optional[SopsSyncProvider] = None,
        sops_s3_bucket: typing.Optional[builtins.str] = None,
        sops_s3_key: typing.Optional[builtins.str] = None,
        stringify_values: typing.Optional[builtins.bool] = None,
        upload_type: typing.Optional[UploadType] = None,
        allowed_pattern: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        parameter_name: typing.Optional[builtins.str] = None,
        simple_name: typing.Optional[builtins.bool] = None,
        tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
        string_value: builtins.str,
        data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
        type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType] = None,
        encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
        key_prefix: typing.Optional[builtins.str] = None,
        key_separator: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param convert_to_json: Should the encrypted sops value should be converted to JSON? Only JSON can be handled by cloud formations dynamic references. Default: true
        :param creation_type: 
        :param flatten: Should the structure be flattened? The result will be a flat structure and all object keys will be replaced with the full jsonpath as key. This is usefull for dynamic references, as those don't support nested objects. Default: true
        :param flatten_separator: If the structure should be flattened use the provided separator between keys. Default: '.'
        :param parameter_key_prefix: Add this prefix to parameter names.
        :param resource_type: 
        :param sops_age_key: The age key that should be used for encryption.
        :param sops_file_format: The format of the sops file. Default: - The fileformat will be derived from the file ending
        :param sops_file_path: The filepath to the sops file.
        :param sops_kms_key: The kmsKey used to encrypt the sops file. Encrypt permissions will be granted to the custom resource provider. Default: - The key will be derived from the sops file
        :param sops_provider: The custom resource provider to use. If you don't specify any, a new provider will be created - or if already exists within this stack - reused. Default: - A new singleton provider will be created
        :param sops_s3_bucket: If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param sops_s3_key: If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.
        :param stringify_values: Shall all values be flattened? This is usefull for dynamic references, as there are lookup errors for certain float types
        :param upload_type: How should the secret be passed to the CustomResource? Default: INLINE
        :param allowed_pattern: A regular expression used to validate the parameter value. For example, for String types with values restricted to numbers, you can specify the following: ``^\\d+$`` Default: no validation is performed
        :param description: Information about the parameter that you want to add to the system. Default: none
        :param parameter_name: The name of the parameter. Default: - a name will be generated by CloudFormation
        :param simple_name: Indicates if the parameter name is a simple name (i.e. does not include "/" separators). This is required only if ``parameterName`` is a token, which means we are unable to detect if the name is simple or "path-like" for the purpose of rendering SSM parameter ARNs. If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or undefined) since the name generated by AWS CloudFormation is always a simple name. Default: - auto-detect based on ``parameterName``
        :param tier: The tier of the string parameter. Default: - undefined
        :param string_value: The value of the parameter. It may not reference another parameter and ``{{}}`` cannot be used in the value.
        :param data_type: The data type of the parameter, such as ``text`` or ``aws:ec2:image``. Default: ParameterDataType.TEXT
        :param type: (deprecated) The type of the string parameter. Default: ParameterType.STRING
        :param encryption_key: 
        :param key_prefix: 
        :param key_separator: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7b531b153efe4b2be69da7047a42a42b5f4c97525cc7994a39eb4156186e11)
            check_type(argname="argument convert_to_json", value=convert_to_json, expected_type=type_hints["convert_to_json"])
            check_type(argname="argument creation_type", value=creation_type, expected_type=type_hints["creation_type"])
            check_type(argname="argument flatten", value=flatten, expected_type=type_hints["flatten"])
            check_type(argname="argument flatten_separator", value=flatten_separator, expected_type=type_hints["flatten_separator"])
            check_type(argname="argument parameter_key_prefix", value=parameter_key_prefix, expected_type=type_hints["parameter_key_prefix"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument sops_age_key", value=sops_age_key, expected_type=type_hints["sops_age_key"])
            check_type(argname="argument sops_file_format", value=sops_file_format, expected_type=type_hints["sops_file_format"])
            check_type(argname="argument sops_file_path", value=sops_file_path, expected_type=type_hints["sops_file_path"])
            check_type(argname="argument sops_kms_key", value=sops_kms_key, expected_type=type_hints["sops_kms_key"])
            check_type(argname="argument sops_provider", value=sops_provider, expected_type=type_hints["sops_provider"])
            check_type(argname="argument sops_s3_bucket", value=sops_s3_bucket, expected_type=type_hints["sops_s3_bucket"])
            check_type(argname="argument sops_s3_key", value=sops_s3_key, expected_type=type_hints["sops_s3_key"])
            check_type(argname="argument stringify_values", value=stringify_values, expected_type=type_hints["stringify_values"])
            check_type(argname="argument upload_type", value=upload_type, expected_type=type_hints["upload_type"])
            check_type(argname="argument allowed_pattern", value=allowed_pattern, expected_type=type_hints["allowed_pattern"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument simple_name", value=simple_name, expected_type=type_hints["simple_name"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument string_value", value=string_value, expected_type=type_hints["string_value"])
            check_type(argname="argument data_type", value=data_type, expected_type=type_hints["data_type"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument key_prefix", value=key_prefix, expected_type=type_hints["key_prefix"])
            check_type(argname="argument key_separator", value=key_separator, expected_type=type_hints["key_separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "string_value": string_value,
            "encryption_key": encryption_key,
        }
        if convert_to_json is not None:
            self._values["convert_to_json"] = convert_to_json
        if creation_type is not None:
            self._values["creation_type"] = creation_type
        if flatten is not None:
            self._values["flatten"] = flatten
        if flatten_separator is not None:
            self._values["flatten_separator"] = flatten_separator
        if parameter_key_prefix is not None:
            self._values["parameter_key_prefix"] = parameter_key_prefix
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if sops_age_key is not None:
            self._values["sops_age_key"] = sops_age_key
        if sops_file_format is not None:
            self._values["sops_file_format"] = sops_file_format
        if sops_file_path is not None:
            self._values["sops_file_path"] = sops_file_path
        if sops_kms_key is not None:
            self._values["sops_kms_key"] = sops_kms_key
        if sops_provider is not None:
            self._values["sops_provider"] = sops_provider
        if sops_s3_bucket is not None:
            self._values["sops_s3_bucket"] = sops_s3_bucket
        if sops_s3_key is not None:
            self._values["sops_s3_key"] = sops_s3_key
        if stringify_values is not None:
            self._values["stringify_values"] = stringify_values
        if upload_type is not None:
            self._values["upload_type"] = upload_type
        if allowed_pattern is not None:
            self._values["allowed_pattern"] = allowed_pattern
        if description is not None:
            self._values["description"] = description
        if parameter_name is not None:
            self._values["parameter_name"] = parameter_name
        if simple_name is not None:
            self._values["simple_name"] = simple_name
        if tier is not None:
            self._values["tier"] = tier
        if data_type is not None:
            self._values["data_type"] = data_type
        if type is not None:
            self._values["type"] = type
        if key_prefix is not None:
            self._values["key_prefix"] = key_prefix
        if key_separator is not None:
            self._values["key_separator"] = key_separator

    @builtins.property
    def convert_to_json(self) -> typing.Optional[builtins.bool]:
        '''Should the encrypted sops value should be converted to JSON?

        Only JSON can be handled by cloud formations dynamic references.

        :default: true
        '''
        result = self._values.get("convert_to_json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def creation_type(self) -> typing.Optional[CreationType]:
        result = self._values.get("creation_type")
        return typing.cast(typing.Optional[CreationType], result)

    @builtins.property
    def flatten(self) -> typing.Optional[builtins.bool]:
        '''Should the structure be flattened?

        The result will be a flat structure and all
        object keys will be replaced with the full jsonpath as key.
        This is usefull for dynamic references, as those don't support nested objects.

        :default: true
        '''
        result = self._values.get("flatten")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def flatten_separator(self) -> typing.Optional[builtins.str]:
        '''If the structure should be flattened use the provided separator between keys.

        :default: '.'
        '''
        result = self._values.get("flatten_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_key_prefix(self) -> typing.Optional[builtins.str]:
        '''Add this prefix to parameter names.'''
        result = self._values.get("parameter_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[ResourceType]:
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[ResourceType], result)

    @builtins.property
    def sops_age_key(self) -> typing.Optional[_aws_cdk_ceddda9d.SecretValue]:
        '''The age key that should be used for encryption.'''
        result = self._values.get("sops_age_key")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.SecretValue], result)

    @builtins.property
    def sops_file_format(self) -> typing.Optional[builtins.str]:
        '''The format of the sops file.

        :default: - The fileformat will be derived from the file ending
        '''
        result = self._values.get("sops_file_format")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_file_path(self) -> typing.Optional[builtins.str]:
        '''The filepath to the sops file.'''
        result = self._values.get("sops_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_kms_key(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]]:
        '''The kmsKey used to encrypt the sops file.

        Encrypt permissions
        will be granted to the custom resource provider.

        :default: - The key will be derived from the sops file
        '''
        result = self._values.get("sops_kms_key")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_kms_ceddda9d.IKey]], result)

    @builtins.property
    def sops_provider(self) -> typing.Optional[SopsSyncProvider]:
        '''The custom resource provider to use.

        If you don't specify any, a new
        provider will be created - or if already exists within this stack - reused.

        :default: - A new singleton provider will be created
        '''
        result = self._values.get("sops_provider")
        return typing.cast(typing.Optional[SopsSyncProvider], result)

    @builtins.property
    def sops_s3_bucket(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_bucket")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sops_s3_key(self) -> typing.Optional[builtins.str]:
        '''If you want to pass the sops file via s3, you can specify the key inside the bucket you can use cfn parameter here Both, sopsS3Bucket and sopsS3Key have to be specified.'''
        result = self._values.get("sops_s3_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stringify_values(self) -> typing.Optional[builtins.bool]:
        '''Shall all values be flattened?

        This is usefull for dynamic references, as there
        are lookup errors for certain float types
        '''
        result = self._values.get("stringify_values")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def upload_type(self) -> typing.Optional[UploadType]:
        '''How should the secret be passed to the CustomResource?

        :default: INLINE
        '''
        result = self._values.get("upload_type")
        return typing.cast(typing.Optional[UploadType], result)

    @builtins.property
    def allowed_pattern(self) -> typing.Optional[builtins.str]:
        '''A regular expression used to validate the parameter value.

        For example, for String types with values restricted to
        numbers, you can specify the following: ``^\\d+$``

        :default: no validation is performed
        '''
        result = self._values.get("allowed_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Information about the parameter that you want to add to the system.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter_name(self) -> typing.Optional[builtins.str]:
        '''The name of the parameter.

        :default: - a name will be generated by CloudFormation
        '''
        result = self._values.get("parameter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def simple_name(self) -> typing.Optional[builtins.bool]:
        '''Indicates if the parameter name is a simple name (i.e. does not include "/" separators).

        This is required only if ``parameterName`` is a token, which means we
        are unable to detect if the name is simple or "path-like" for the purpose
        of rendering SSM parameter ARNs.

        If ``parameterName`` is not specified, ``simpleName`` must be ``true`` (or
        undefined) since the name generated by AWS CloudFormation is always a
        simple name.

        :default: - auto-detect based on ``parameterName``
        '''
        result = self._values.get("simple_name")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tier(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier]:
        '''The tier of the string parameter.

        :default: - undefined
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier], result)

    @builtins.property
    def string_value(self) -> builtins.str:
        '''The value of the parameter.

        It may not reference another parameter and ``{{}}`` cannot be used in the value.
        '''
        result = self._values.get("string_value")
        assert result is not None, "Required property 'string_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data_type(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType]:
        '''The data type of the parameter, such as ``text`` or ``aws:ec2:image``.

        :default: ParameterDataType.TEXT
        '''
        result = self._values.get("data_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType], result)

    @builtins.property
    def type(self) -> typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType]:
        '''(deprecated) The type of the string parameter.

        :default: ParameterType.STRING

        :deprecated: - type will always be 'String'

        :stability: deprecated
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType], result)

    @builtins.property
    def encryption_key(self) -> _aws_cdk_aws_kms_ceddda9d.IKey:
        result = self._values.get("encryption_key")
        assert result is not None, "Required property 'encryption_key' is missing"
        return typing.cast(_aws_cdk_aws_kms_ceddda9d.IKey, result)

    @builtins.property
    def key_prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def key_separator(self) -> typing.Optional[builtins.str]:
        result = self._values.get("key_separator")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultiStringParameterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CreationType",
    "MultiStringParameter",
    "MultiStringParameterProps",
    "ResourceType",
    "SopsSecret",
    "SopsSecretProps",
    "SopsStringParameter",
    "SopsStringParameterProps",
    "SopsSync",
    "SopsSyncOptions",
    "SopsSyncProps",
    "SopsSyncProvider",
    "SopsSyncProviderProps",
    "UploadType",
]

publication.publish()

def _typecheckingstub__520cbd9adefd0e4a3135f2f09bd2fa26acb8be581e0f77b06f12862c0125b5b4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    key_prefix: typing.Optional[builtins.str] = None,
    key_separator: typing.Optional[builtins.str] = None,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
    string_value: builtins.str,
    data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
    type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType] = None,
    allowed_pattern: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    parameter_name: typing.Optional[builtins.str] = None,
    simple_name: typing.Optional[builtins.bool] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641b47276285e7c457eb639fea01f8b2e2f54dd58d3bc6f9e184404914516a11(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    generate_secret_string: typing.Optional[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringGenerator, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    replica_regions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_name: typing.Optional[builtins.str] = None,
    secret_object_value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_ceddda9d.SecretValue]] = None,
    secret_string_beta1: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringValueBeta1] = None,
    secret_string_value: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd08508625195135b318d9657d717ca369ecceb1cc51cd6b3fa8c66c489c3dad(
    id: builtins.str,
    *,
    automatically_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    hosted_rotation: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.HostedRotation] = None,
    rotate_immediately_on_update: typing.Optional[builtins.bool] = None,
    rotation_lambda: typing.Optional[_aws_cdk_aws_lambda_ceddda9d.IFunction] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54076b0a3bb41bb64b3bbd471f51ee813e6ce6437b4b2ee14f76246051614126(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d3b1469d7d365dc715e5fc30a5ca749e3a126bab5731a9cb3e3bd09de54905(
    policy: _aws_cdk_ceddda9d.RemovalPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7169bcc05cc9fef09daa2e6732c5c382897a8dace487c441a5df1ea46b3123fc(
    target: _aws_cdk_aws_secretsmanager_ceddda9d.ISecretAttachmentTarget,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84d1e6becdb6cf951b358b8a8bc63f668e555a12d11b0028528af866931a1c8(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    version_stages: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd3a17eb68d15973a8af9441eb6cd97ed5338dead66b7679f005db68637eb5f(
    _grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65919d041d660423e596dfdaa79882405d878d5eda9d3e1171335aa874544f9(
    json_field: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18c9bb48fa41cbb41be59793bbe0b888d5730c69b1bf3580c6c19d7d6be65d8d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
    string_value: builtins.str,
    data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
    type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType] = None,
    allowed_pattern: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    parameter_name: typing.Optional[builtins.str] = None,
    simple_name: typing.Optional[builtins.bool] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3df10361f8a5b128d2433c218086d617e482ecd374cb8020cdc94262ee0764ad(
    policy: _aws_cdk_ceddda9d.RemovalPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77542577a7e47c1c7b3090197d5a0c6f281fe2b6578631e3d20a4d286277d0ff(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96018dc2f4a57e7a385eced7113b3297dcd94c0473ff9eb0d54ebc35edd378de(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b3134de7215a676a4feb3291975d227477d2dc9d5914405b8ab165ac30d7bad(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e7f5d5a68ee1675b645864f7bab39e30d7c7922956c69686578f4d6fb05723(
    *,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3baaf21b8ae44e7f4d83d5677857cc4141222b3d41237073b75dca6d425c2c34(
    *,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    parameter_name: typing.Optional[builtins.str] = None,
    parameter_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    secret: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.ISecret] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2ccd4bddb65030756f5b6473575c1a4cc9c9ef0202c6dbe31603b006c05734(
    scope: _constructs_77d1e7e8.Construct,
    id: typing.Optional[builtins.str] = None,
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f2a1da09ecfa1b4ae9738b2c30c913950581a07762445e7b2bb6fc32606a17d(
    key: _aws_cdk_ceddda9d.SecretValue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1cafbc66169426f4b5af87376d7258f7064772025b196978a5b2312e359079(
    *,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5ff836a3767bbc726a1167e9f5e789f0fad2dcaf72b41a245494f0a121a8a3(
    *,
    description: typing.Optional[builtins.str] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    generate_secret_string: typing.Optional[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringGenerator, typing.Dict[builtins.str, typing.Any]]] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    replica_regions: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_secretsmanager_ceddda9d.ReplicaRegion, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret_name: typing.Optional[builtins.str] = None,
    secret_object_value: typing.Optional[typing.Mapping[builtins.str, _aws_cdk_ceddda9d.SecretValue]] = None,
    secret_string_beta1: typing.Optional[_aws_cdk_aws_secretsmanager_ceddda9d.SecretStringValueBeta1] = None,
    secret_string_value: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4c6b41b250704c51710cadcac0559f659733c6085f47a56587b680e5275a68(
    *,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
    allowed_pattern: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    parameter_name: typing.Optional[builtins.str] = None,
    simple_name: typing.Optional[builtins.bool] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    string_value: builtins.str,
    data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
    type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType] = None,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7b531b153efe4b2be69da7047a42a42b5f4c97525cc7994a39eb4156186e11(
    *,
    convert_to_json: typing.Optional[builtins.bool] = None,
    creation_type: typing.Optional[CreationType] = None,
    flatten: typing.Optional[builtins.bool] = None,
    flatten_separator: typing.Optional[builtins.str] = None,
    parameter_key_prefix: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[ResourceType] = None,
    sops_age_key: typing.Optional[_aws_cdk_ceddda9d.SecretValue] = None,
    sops_file_format: typing.Optional[builtins.str] = None,
    sops_file_path: typing.Optional[builtins.str] = None,
    sops_kms_key: typing.Optional[typing.Sequence[_aws_cdk_aws_kms_ceddda9d.IKey]] = None,
    sops_provider: typing.Optional[SopsSyncProvider] = None,
    sops_s3_bucket: typing.Optional[builtins.str] = None,
    sops_s3_key: typing.Optional[builtins.str] = None,
    stringify_values: typing.Optional[builtins.bool] = None,
    upload_type: typing.Optional[UploadType] = None,
    allowed_pattern: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    parameter_name: typing.Optional[builtins.str] = None,
    simple_name: typing.Optional[builtins.bool] = None,
    tier: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterTier] = None,
    string_value: builtins.str,
    data_type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterDataType] = None,
    type: typing.Optional[_aws_cdk_aws_ssm_ceddda9d.ParameterType] = None,
    encryption_key: _aws_cdk_aws_kms_ceddda9d.IKey,
    key_prefix: typing.Optional[builtins.str] = None,
    key_separator: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
