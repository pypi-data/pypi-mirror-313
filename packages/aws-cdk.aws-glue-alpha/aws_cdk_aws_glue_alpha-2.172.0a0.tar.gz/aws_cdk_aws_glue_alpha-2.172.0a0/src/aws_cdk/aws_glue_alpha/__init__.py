r'''
# AWS Glue Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Job

A `Job` encapsulates a script that connects to data sources, processes them, and then writes output to a data target.

There are 3 types of jobs supported by AWS Glue: Spark ETL, Spark Streaming, and Python Shell jobs.

The `glue.JobExecutable` allows you to specify the type of job, the language to use and the code assets required by the job.

`glue.Code` allows you to refer to the different code assets required by the job, either from an existing S3 location or from a local file path.

`glue.ExecutionClass` allows you to specify `FLEX` or `STANDARD`. `FLEX` is appropriate for non-urgent jobs such as pre-production jobs, testing, and one-time data loads.

### Spark Jobs

These jobs run in an Apache Spark environment managed by AWS Glue.

#### ETL Jobs

An ETL job processes data in batches using Apache Spark.

```python
# bucket: s3.Bucket

glue.Job(self, "ScalaSparkEtlJob",
    executable=glue.JobExecutable.scala_etl(
        glue_version=glue.GlueVersion.V4_0,
        script=glue.Code.from_bucket(bucket, "src/com/example/HelloWorld.scala"),
        class_name="com.example.HelloWorld",
        extra_jars=[glue.Code.from_bucket(bucket, "jars/HelloWorld.jar")]
    ),
    worker_type=glue.WorkerType.G_8X,
    description="an example Scala ETL job"
)
```

#### Streaming Jobs

A Streaming job is similar to an ETL job, except that it performs ETL on data streams. It uses the Apache Spark Structured Streaming framework. Some Spark job features are not available to streaming ETL jobs.

```python
glue.Job(self, "PythonSparkStreamingJob",
    executable=glue.JobExecutable.python_streaming(
        glue_version=glue.GlueVersion.V4_0,
        python_version=glue.PythonVersion.THREE,
        script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
    ),
    description="an example Python Streaming job"
)
```

### Python Shell Jobs

A Python shell job runs Python scripts as a shell and supports a Python version that depends on the AWS Glue version you are using.
This can be used to schedule and run tasks that don't require an Apache Spark environment. Currently, three flavors are supported:

* PythonVersion.TWO (2.7; EOL)
* PythonVersion.THREE (3.6)
* PythonVersion.THREE_NINE (3.9)

```python
# bucket: s3.Bucket

glue.Job(self, "PythonShellJob",
    executable=glue.JobExecutable.python_shell(
        glue_version=glue.GlueVersion.V1_0,
        python_version=glue.PythonVersion.THREE,
        script=glue.Code.from_bucket(bucket, "script.py")
    ),
    description="an example Python Shell job"
)
```

### Ray Jobs

These jobs run in a Ray environment managed by AWS Glue.

```python
glue.Job(self, "RayJob",
    executable=glue.JobExecutable.python_ray(
        glue_version=glue.GlueVersion.V4_0,
        python_version=glue.PythonVersion.THREE_NINE,
        runtime=glue.Runtime.RAY_TWO_FOUR,
        script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
    ),
    worker_type=glue.WorkerType.Z_2X,
    worker_count=2,
    description="an example Ray job"
)
```

### Enable Spark UI

Enable Spark UI setting the `sparkUI` property.

```python
glue.Job(self, "EnableSparkUI",
    job_name="EtlJobWithSparkUIPrefix",
    spark_uI=glue.SparkUIProps(
        enabled=True
    ),
    executable=glue.JobExecutable.python_etl(
        glue_version=glue.GlueVersion.V3_0,
        python_version=glue.PythonVersion.THREE,
        script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
    )
)
```

The `sparkUI` property also allows the specification of an s3 bucket and a bucket prefix.

See [documentation](https://docs.aws.amazon.com/glue/latest/dg/add-job.html) for more information on adding jobs in Glue.

### Enable Job Run Queuing

AWS Glue job queuing monitors your account level quotas and limits. If quotas or limits are insufficient to start a Glue job run, AWS Glue will automatically queue the job and wait for limits to free up. Once limits become available, AWS Glue will retry the job run. Glue jobs will queue for limits like max concurrent job runs per account, max concurrent Data Processing Units (DPU), and resource unavailable due to IP address exhaustion in Amazon Virtual Private Cloud (Amazon VPC).

Enable job run queuing by setting the `jobRunQueuingEnabled` property to `true`.

```python
glue.Job(self, "EnableRunQueuing",
    job_name="EtlJobWithRunQueuing",
    executable=glue.JobExecutable.python_etl(
        glue_version=glue.GlueVersion.V4_0,
        python_version=glue.PythonVersion.THREE,
        script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
    ),
    job_run_queuing_enabled=True
)
```

## Connection

A `Connection` allows Glue jobs, crawlers and development endpoints to access certain types of data stores. For example, to create a network connection to connect to a data source within a VPC:

```python
# security_group: ec2.SecurityGroup
# subnet: ec2.Subnet

glue.Connection(self, "MyConnection",
    type=glue.ConnectionType.NETWORK,
    # The security groups granting AWS Glue inbound access to the data source within the VPC
    security_groups=[security_group],
    # The VPC subnet which contains the data source
    subnet=subnet
)
```

For RDS `Connection` by JDBC, it is recommended to manage credentials using AWS Secrets Manager. To use Secret, specify `SECRET_ID` in `properties` like the following code. Note that in this case, the subnet must have a route to the AWS Secrets Manager VPC endpoint or to the AWS Secrets Manager endpoint through a NAT gateway.

```python
# security_group: ec2.SecurityGroup
# subnet: ec2.Subnet
# db: rds.DatabaseCluster

glue.Connection(self, "RdsConnection",
    type=glue.ConnectionType.JDBC,
    security_groups=[security_group],
    subnet=subnet,
    properties={
        "JDBC_CONNECTION_URL": f"jdbc:mysql://{db.clusterEndpoint.socketAddress}/databasename",
        "JDBC_ENFORCE_SSL": "false",
        "SECRET_ID": db.secret.secret_name
    }
)
```

If you need to use a connection type that doesn't exist as a static member on `ConnectionType`, you can instantiate a `ConnectionType` object, e.g: `new glue.ConnectionType('NEW_TYPE')`.

See [Adding a Connection to Your Data Store](https://docs.aws.amazon.com/glue/latest/dg/populate-add-connection.html) and [Connection Structure](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-connections.html#aws-glue-api-catalog-connections-Connection) documentation for more information on the supported data stores and their configurations.

## SecurityConfiguration

A `SecurityConfiguration` is a set of security properties that can be used by AWS Glue to encrypt data at rest.

```python
glue.SecurityConfiguration(self, "MySecurityConfiguration",
    cloud_watch_encryption=glue.CloudWatchEncryption(
        mode=glue.CloudWatchEncryptionMode.KMS
    ),
    job_bookmarks_encryption=glue.JobBookmarksEncryption(
        mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
    ),
    s3_encryption=glue.S3Encryption(
        mode=glue.S3EncryptionMode.KMS
    )
)
```

By default, a shared KMS key is created for use with the encryption configurations that require one. You can also supply your own key for each encryption config, for example, for CloudWatch encryption:

```python
# key: kms.Key

glue.SecurityConfiguration(self, "MySecurityConfiguration",
    cloud_watch_encryption=glue.CloudWatchEncryption(
        mode=glue.CloudWatchEncryptionMode.KMS,
        kms_key=key
    )
)
```

See [documentation](https://docs.aws.amazon.com/glue/latest/dg/encryption-security-configuration.html) for more info for Glue encrypting data written by Crawlers, Jobs, and Development Endpoints.

## Database

A `Database` is a logical grouping of `Tables` in the Glue Catalog.

```python
glue.Database(self, "MyDatabase",
    database_name="my_database",
    description="my_database_description"
)
```

## Table

A Glue table describes a table of data in S3: its structure (column names and types), location of data (S3 objects with a common prefix in a S3 bucket), and format for the files (Json, Avro, Parquet, etc.):

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    ), glue.Column(
        name="col2",
        type=glue.Schema.array(glue.Schema.STRING),
        comment="col2 is an array of strings"
    )],
    data_format=glue.DataFormat.JSON
)
```

By default, a S3 bucket will be created to store the table's data but you can manually pass the `bucket` and `s3Prefix`:

```python
# my_bucket: s3.Bucket
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    bucket=my_bucket,
    s3_prefix="my-table/",
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)
```

Glue tables can be configured to contain user-defined properties, to describe the physical storage of table data, through the `storageParameters` property:

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    storage_parameters=[
        glue.StorageParameter.skip_header_line_count(1),
        glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
        glue.StorageParameter.custom("separatorChar", ",")
    ],
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)
```

Glue tables can also be configured to contain user-defined table properties through the [`parameters`](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters) property:

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    parameters={
        "key1": "val1",
        "key2": "val2"
    },
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)
```

### Partition Keys

To improve query performance, a table can specify `partitionKeys` on which data is stored and queried separately. For example, you might partition a table by `year` and `month` to optimize queries based on a time window:

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    partition_keys=[glue.Column(
        name="year",
        type=glue.Schema.SMALL_INT
    ), glue.Column(
        name="month",
        type=glue.Schema.SMALL_INT
    )],
    data_format=glue.DataFormat.JSON
)
```

### Partition Indexes

Another way to improve query performance is to specify partition indexes. If no partition indexes are
present on the table, AWS Glue loads all partitions of the table and filters the loaded partitions using
the query expression. The query takes more time to run as the number of partitions increase. With an
index, the query will try to fetch a subset of the partitions instead of loading all partitions of the
table.

The keys of a partition index must be a subset of the partition keys of the table. You can have a
maximum of 3 partition indexes per table. To specify a partition index, you can use the `partitionIndexes`
property:

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    partition_keys=[glue.Column(
        name="year",
        type=glue.Schema.SMALL_INT
    ), glue.Column(
        name="month",
        type=glue.Schema.SMALL_INT
    )],
    partition_indexes=[glue.PartitionIndex(
        index_name="my-index",  # optional
        key_names=["year"]
    )],  # supply up to 3 indexes
    data_format=glue.DataFormat.JSON
)
```

Alternatively, you can call the `addPartitionIndex()` function on a table:

```python
# my_table: glue.Table

my_table.add_partition_index(
    index_name="my-index",
    key_names=["year"]
)
```

### Partition Filtering

If you have a table with a large number of partitions that grows over time, consider using AWS Glue partition indexing and filtering.

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    partition_keys=[glue.Column(
        name="year",
        type=glue.Schema.SMALL_INT
    ), glue.Column(
        name="month",
        type=glue.Schema.SMALL_INT
    )],
    data_format=glue.DataFormat.JSON,
    enable_partition_filtering=True
)
```

### Glue Connections

Glue connections allow external data connections to third party databases and data warehouses. However, these connections can also be assigned to Glue Tables, allowing you to query external data sources using the Glue Data Catalog.

Whereas `S3Table` will point to (and if needed, create) a bucket to store the tables' data, `ExternalTable` will point to an existing table in a data source. For example, to create a table in Glue that points to a table in Redshift:

```python
# my_connection: glue.Connection
# my_database: glue.Database

glue.ExternalTable(self, "MyTable",
    connection=my_connection,
    external_data_location="default_db_public_example",  # A table in Redshift
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)
```

## [Encryption](https://docs.aws.amazon.com/athena/latest/ug/encryption.html)

You can enable encryption on a Table's data:

* [S3Managed](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html) - (default) Server side encryption (`SSE-S3`) with an Amazon S3-managed key.

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    encryption=glue.TableEncryption.S3_MANAGED,
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)
```

* [Kms](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html) - Server-side encryption (`SSE-KMS`) with an AWS KMS Key managed by the account owner.

```python
# my_database: glue.Database

# KMS key is created automatically
glue.S3Table(self, "MyTable",
    encryption=glue.TableEncryption.KMS,
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)

# with an explicit KMS key
glue.S3Table(self, "MyTable",
    encryption=glue.TableEncryption.KMS,
    encryption_key=kms.Key(self, "MyKey"),
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)
```

* [KmsManaged](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html) - Server-side encryption (`SSE-KMS`), like `Kms`, except with an AWS KMS Key managed by the AWS Key Management Service.

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    encryption=glue.TableEncryption.KMS_MANAGED,
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)
```

* [ClientSideKms](https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html#client-side-encryption-kms-managed-master-key-intro) - Client-side encryption (`CSE-KMS`) with an AWS KMS Key managed by the account owner.

```python
# my_database: glue.Database

# KMS key is created automatically
glue.S3Table(self, "MyTable",
    encryption=glue.TableEncryption.CLIENT_SIDE_KMS,
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)

# with an explicit KMS key
glue.S3Table(self, "MyTable",
    encryption=glue.TableEncryption.CLIENT_SIDE_KMS,
    encryption_key=kms.Key(self, "MyKey"),
    # ...
    database=my_database,
    columns=[glue.Column(
        name="col1",
        type=glue.Schema.STRING
    )],
    data_format=glue.DataFormat.JSON
)
```

*Note: you cannot provide a `Bucket` when creating the `S3Table` if you wish to use server-side encryption (`KMS`, `KMS_MANAGED` or `S3_MANAGED`)*.

## Types

A table's schema is a collection of columns, each of which have a `name` and a `type`. Types are recursive structures, consisting of primitive and complex types:

```python
# my_database: glue.Database

glue.S3Table(self, "MyTable",
    columns=[glue.Column(
        name="primitive_column",
        type=glue.Schema.STRING
    ), glue.Column(
        name="array_column",
        type=glue.Schema.array(glue.Schema.INTEGER),
        comment="array<integer>"
    ), glue.Column(
        name="map_column",
        type=glue.Schema.map(glue.Schema.STRING, glue.Schema.TIMESTAMP),
        comment="map<string,string>"
    ), glue.Column(
        name="struct_column",
        type=glue.Schema.struct([
            name="nested_column",
            type=glue.Schema.DATE,
            comment="nested comment"
        ]),
        comment="struct<nested_column:date COMMENT 'nested comment'>"
    )],
    # ...
    database=my_database,
    data_format=glue.DataFormat.JSON
)
```

### Primitives

#### Numeric

| Name      	| Type     	| Comments                                                                                                          |
|-----------	|----------	|------------------------------------------------------------------------------------------------------------------	|
| FLOAT     	| Constant 	| A 32-bit single-precision floating point number                                                                   |
| INTEGER   	| Constant 	| A 32-bit signed value in two's complement format, with a minimum value of -2^31 and a maximum value of 2^31-1 	|
| DOUBLE    	| Constant 	| A 64-bit double-precision floating point number                                                                   |
| BIG_INT   	| Constant 	| A 64-bit signed INTEGER in two’s complement format, with a minimum value of -2^63 and a maximum value of 2^63 -1  |
| SMALL_INT 	| Constant 	| A 16-bit signed INTEGER in two’s complement format, with a minimum value of -2^15 and a maximum value of 2^15-1   |
| TINY_INT  	| Constant 	| A 8-bit signed INTEGER in two’s complement format, with a minimum value of -2^7 and a maximum value of 2^7-1      |

#### Date and time

| Name      	| Type     	| Comments                                                                                                                                                                	|
|-----------	|----------	|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| DATE      	| Constant 	| A date in UNIX format, such as YYYY-MM-DD.                                                                                                                              	|
| TIMESTAMP 	| Constant 	| Date and time instant in the UNiX format, such as yyyy-mm-dd hh:mm:ss[.f...]. For example, TIMESTAMP '2008-09-15 03:04:05.324'. This format uses the session time zone. 	|

#### String

| Name                                       	| Type     	| Comments                                                                                                                                                                                          	|
|--------------------------------------------	|----------	|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------	|
| STRING                                     	| Constant 	| A string literal enclosed in single or double quotes                                                                                                                                              	|
| decimal(precision: number, scale?: number) 	| Function 	| `precision` is the total number of digits. `scale` (optional) is the number of digits in fractional part with a default of 0. For example, use these type definitions: decimal(11,5), decimal(15) 	|
| char(length: number)                       	| Function 	| Fixed length character data, with a specified length between 1 and 255, such as char(10)                                                                                                          	|
| varchar(length: number)                    	| Function 	| Variable length character data, with a specified length between 1 and 65535, such as varchar(10)                                                                                                  	|

#### Miscellaneous

| Name    	| Type     	| Comments                      	|
|---------	|----------	|-------------------------------	|
| BOOLEAN 	| Constant 	| Values are `true` and `false` 	|
| BINARY  	| Constant 	| Value is in binary            	|

### Complex

| Name                                	| Type     	| Comments                                                          	|
|-------------------------------------	|----------	|-------------------------------------------------------------------	|
| array(itemType: Type)               	| Function 	| An array of some other type                                       	|
| map(keyType: Type, valueType: Type) 	| Function 	| A map of some primitive key type to any value type                	|
| struct(collumns: Column[])          	| Function 	| Nested structure containing individually named and typed collumns 	|

## Data Quality Ruleset

A `DataQualityRuleset` specifies a data quality ruleset with DQDL rules applied to a specified AWS Glue table. For example, to create a data quality ruleset for a given table:

```python
glue.DataQualityRuleset(self, "MyDataQualityRuleset",
    client_token="client_token",
    description="description",
    ruleset_name="ruleset_name",
    ruleset_dqdl="ruleset_dqdl",
    tags={
        "key1": "value1",
        "key2": "value2"
    },
    target_table=glue.DataQualityTargetTable("database_name", "table_name")
)
```

For more information, see [AWS Glue Data Quality](https://docs.aws.amazon.com/glue/latest/dg/glue-data-quality.html).
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
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_glue as _aws_cdk_aws_glue_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_s3_assets as _aws_cdk_aws_s3_assets_ceddda9d
import constructs as _constructs_77d1e7e8


class ClassificationString(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.ClassificationString",
):
    '''(experimental) Classification string given to tables with this data format.

    :see: https://docs.aws.amazon.com/glue/latest/dg/add-classifier.html#classifier-built-in
    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_glue_alpha as glue_alpha
        
        classification_string = glue_alpha.ClassificationString.AVRO
    '''

    def __init__(self, value: builtins.str) -> None:
        '''
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bfce587a58c2deea97e71eeab8754a97692804f6d43271eda89c6257eaebdfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [value])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-avro
        :stability: experimental
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CSV")
    def CSV(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-csv
        :stability: experimental
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "CSV"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="JSON")
    def JSON(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-json
        :stability: experimental
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "JSON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-orc
        :stability: experimental
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-parquet
        :stability: experimental
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "PARQUET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="XML")
    def XML(cls) -> "ClassificationString":
        '''
        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-format.html#aws-glue-programming-etl-format-xml
        :stability: experimental
        '''
        return typing.cast("ClassificationString", jsii.sget(cls, "XML"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.CloudWatchEncryption",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "kms_key": "kmsKey"},
)
class CloudWatchEncryption:
    def __init__(
        self,
        *,
        mode: "CloudWatchEncryptionMode",
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''(experimental) CloudWatch Logs encryption configuration.

        :param mode: (experimental) Encryption mode.
        :param kms_key: (experimental) The KMS key to be used to encrypt the data. Default: A key will be created if one is not provided.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.SecurityConfiguration(self, "MySecurityConfiguration",
                cloud_watch_encryption=glue.CloudWatchEncryption(
                    mode=glue.CloudWatchEncryptionMode.KMS
                ),
                job_bookmarks_encryption=glue.JobBookmarksEncryption(
                    mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
                ),
                s3_encryption=glue.S3Encryption(
                    mode=glue.S3EncryptionMode.KMS
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ceec14d1d7029d8fb7df76e4abb14bc79250421d85a9584f0271d9e7c4f4ef3f)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def mode(self) -> "CloudWatchEncryptionMode":
        '''(experimental) Encryption mode.

        :stability: experimental
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast("CloudWatchEncryptionMode", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to be used to encrypt the data.

        :default: A key will be created if one is not provided.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.CloudWatchEncryptionMode")
class CloudWatchEncryptionMode(enum.Enum):
    '''(experimental) Encryption mode for CloudWatch Logs.

    :see: https://docs.aws.amazon.com/glue/latest/webapi/API_CloudWatchEncryption.html#Glue-Type-CloudWatchEncryption-CloudWatchEncryptionMode
    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.SecurityConfiguration(self, "MySecurityConfiguration",
            cloud_watch_encryption=glue.CloudWatchEncryption(
                mode=glue.CloudWatchEncryptionMode.KMS
            ),
            job_bookmarks_encryption=glue.JobBookmarksEncryption(
                mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
            ),
            s3_encryption=glue.S3Encryption(
                mode=glue.S3EncryptionMode.KMS
            )
        )
    '''

    KMS = "KMS"
    '''(experimental) Server-side encryption (SSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
    :stability: experimental
    '''


class Code(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-glue-alpha.Code"):
    '''(experimental) Represents a Glue Job's Code assets (an asset can be a scripts, a jar, a python file or any other file).

    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.Job(self, "EnableRunQueuing",
            job_name="EtlJobWithRunQueuing",
            executable=glue.JobExecutable.python_etl(
                glue_version=glue.GlueVersion.V4_0,
                python_version=glue.PythonVersion.THREE,
                script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
            ),
            job_run_queuing_enabled=True
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        path: builtins.str,
        *,
        deploy_time: typing.Optional[builtins.bool] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
        source_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    ) -> "AssetCode":
        '''(experimental) Job code from a local disk path.

        :param path: code file (not a directory).
        :param deploy_time: Whether or not the asset needs to exist beyond deployment time; i.e. are copied over to a different location and not needed afterwards. Setting this property to true has an impact on the lifecycle of the asset, because we will assume that it is safe to delete after the CloudFormation deployment succeeds. For example, Lambda Function assets are copied over to Lambda during deployment. Therefore, it is not necessary to store the asset in S3, so we consider those deployTime assets. Default: false
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_kms_key: The ARN of the KMS key used to encrypt the handler code. Default: - the default server-side encryption with Amazon S3 managed keys(SSE-S3) key will be used.
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7e88ca82e81ea6700503f28d9e5352c4a86e264d00afb35e761e591a7e0e24)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = _aws_cdk_aws_s3_assets_ceddda9d.AssetOptions(
            deploy_time=deploy_time,
            readers=readers,
            source_kms_key=source_kms_key,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

        return typing.cast("AssetCode", jsii.sinvoke(cls, "fromAsset", [path, options]))

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(
        cls,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> "S3Code":
        '''(experimental) Job code as an S3 object.

        :param bucket: The S3 bucket.
        :param key: The object key.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d23f6002340150960cebd70816482874d96a0de7d52265f1fcd0ab459eea2a61)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("S3Code", jsii.sinvoke(cls, "fromBucket", [bucket, key]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> "CodeConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param scope: -
        :param grantable: -

        :stability: experimental
        '''
        ...


class _CodeProxy(Code):
    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> "CodeConfig":
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param scope: -
        :param grantable: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b88388256be44082f9ce622ac393616c31af36dc246d0cb6ea3eb8e78b31dc1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument grantable", value=grantable, expected_type=type_hints["grantable"])
        return typing.cast("CodeConfig", jsii.invoke(self, "bind", [scope, grantable]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Code).__jsii_proxy_class__ = lambda : _CodeProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.CodeConfig",
    jsii_struct_bases=[],
    name_mapping={"s3_location": "s3Location"},
)
class CodeConfig:
    def __init__(
        self,
        *,
        s3_location: typing.Union[_aws_cdk_aws_s3_ceddda9d.Location, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) Result of binding ``Code`` into a ``Job``.

        :param s3_location: (experimental) The location of the code in S3.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            
            code_config = glue_alpha.CodeConfig(
                s3_location=Location(
                    bucket_name="bucketName",
                    object_key="objectKey",
            
                    # the properties below are optional
                    object_version="objectVersion"
                )
            )
        '''
        if isinstance(s3_location, dict):
            s3_location = _aws_cdk_aws_s3_ceddda9d.Location(**s3_location)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7667596ec33fb86df61ee9e5603a0bed57aa6e48e3795e84685966147e79b05e)
            check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "s3_location": s3_location,
        }

    @builtins.property
    def s3_location(self) -> _aws_cdk_aws_s3_ceddda9d.Location:
        '''(experimental) The location of the code in S3.

        :stability: experimental
        '''
        result = self._values.get("s3_location")
        assert result is not None, "Required property 's3_location' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.Location, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.Column",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "comment": "comment"},
)
class Column:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: typing.Union["Type", typing.Dict[builtins.str, typing.Any]],
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) A column of a table.

        :param name: (experimental) Name of the column.
        :param type: (experimental) Type of the column.
        :param comment: (experimental) Coment describing the column. Default: none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            
            column = glue_alpha.Column(
                name="name",
                type=glue_alpha.Type(
                    input_string="inputString",
                    is_primitive=False
                ),
            
                # the properties below are optional
                comment="comment"
            )
        '''
        if isinstance(type, dict):
            type = Type(**type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__043c8b76c78332fa2f7a0e1444ad14734d788355c87767ffb0dd0aac9a19fbdf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
        }
        if comment is not None:
            self._values["comment"] = comment

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) Name of the column.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> "Type":
        '''(experimental) Type of the column.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("Type", result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) Coment describing the column.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Column(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.ColumnCountMismatchHandlingAction")
class ColumnCountMismatchHandlingAction(enum.Enum):
    '''(experimental) Identifies if the file contains less or more values for a row than the number of columns specified in the external table definition.

    This property is only available for an uncompressed text file format.

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"* > *"column_count_mismatch_handling"*
    :stability: experimental
    '''

    DISABLED = "DISABLED"
    '''(experimental) Column count mismatch handling is turned off.

    :stability: experimental
    '''
    FAIL = "FAIL"
    '''(experimental) Fail the query if the column count mismatch is detected.

    :stability: experimental
    '''
    SET_TO_NULL = "SET_TO_NULL"
    '''(experimental) Fill missing values with NULL and ignore the additional values in each row.

    :stability: experimental
    '''
    DROP_ROW = "DROP_ROW"
    '''(experimental) Drop all rows that contain column count mismatch error from the scan.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.CompressionType")
class CompressionType(enum.Enum):
    '''(experimental) The compression type.

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"* > *"compression_type"*
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_database: glue.Database
        
        glue.S3Table(self, "MyTable",
            storage_parameters=[
                glue.StorageParameter.skip_header_line_count(1),
                glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
                glue.StorageParameter.custom("separatorChar", ",")
            ],
            # ...
            database=my_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            data_format=glue.DataFormat.JSON
        )
    '''

    NONE = "NONE"
    '''(experimental) No compression.

    :stability: experimental
    '''
    BZIP2 = "BZIP2"
    '''(experimental) Burrows-Wheeler compression.

    :stability: experimental
    '''
    GZIP = "GZIP"
    '''(experimental) Deflate compression.

    :stability: experimental
    '''
    SNAPPY = "SNAPPY"
    '''(experimental) Compression algorithm focused on high compression and decompression speeds, rather than the maximum possible compression.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.ConnectionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "connection_name": "connectionName",
        "description": "description",
        "match_criteria": "matchCriteria",
        "properties": "properties",
        "security_groups": "securityGroups",
        "subnet": "subnet",
    },
)
class ConnectionOptions:
    def __init__(
        self,
        *,
        connection_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        match_criteria: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
    ) -> None:
        '''(experimental) Base Connection Options.

        :param connection_name: (experimental) The name of the connection. Default: cloudformation generated name
        :param description: (experimental) The description of the connection. Default: no description
        :param match_criteria: (experimental) A list of criteria that can be used in selecting this connection. This is useful for filtering the results of https://awscli.amazonaws.com/v2/documentation/api/latest/reference/glue/get-connections.html Default: no match criteria
        :param properties: (experimental) Key-Value pairs that define parameters for the connection. Default: empty properties
        :param security_groups: (experimental) The list of security groups needed to successfully make this connection e.g. to successfully connect to VPC. Default: no security group
        :param subnet: (experimental) The VPC subnet to connect to resources within a VPC. See more at https://docs.aws.amazon.com/glue/latest/dg/start-connecting.html. Default: no subnet

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            
            connection_options = glue_alpha.ConnectionOptions(
                connection_name="connectionName",
                description="description",
                match_criteria=["matchCriteria"],
                properties={
                    "properties_key": "properties"
                },
                security_groups=[security_group],
                subnet=subnet
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1670baf78db937cd3601a16badd87755f3fc525b8fd6a352d45c2bc3994b494)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument match_criteria", value=match_criteria, expected_type=type_hints["match_criteria"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if description is not None:
            self._values["description"] = description
        if match_criteria is not None:
            self._values["match_criteria"] = match_criteria
        if properties is not None:
            self._values["properties"] = properties
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the connection.

        :default: cloudformation generated name

        :stability: experimental
        '''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the connection.

        :default: no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_criteria(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of criteria that can be used in selecting this connection.

        This is useful for filtering the results of https://awscli.amazonaws.com/v2/documentation/api/latest/reference/glue/get-connections.html

        :default: no match criteria

        :stability: experimental
        '''
        result = self._values.get("match_criteria")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Key-Value pairs that define parameters for the connection.

        :default: empty properties

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect.html
        :stability: experimental
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The list of security groups needed to successfully make this connection e.g. to successfully connect to VPC.

        :default: no security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) The VPC subnet to connect to resources within a VPC.

        See more at https://docs.aws.amazon.com/glue/latest/dg/start-connecting.html.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.ConnectionProps",
    jsii_struct_bases=[ConnectionOptions],
    name_mapping={
        "connection_name": "connectionName",
        "description": "description",
        "match_criteria": "matchCriteria",
        "properties": "properties",
        "security_groups": "securityGroups",
        "subnet": "subnet",
        "type": "type",
    },
)
class ConnectionProps(ConnectionOptions):
    def __init__(
        self,
        *,
        connection_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        match_criteria: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
        type: "ConnectionType",
    ) -> None:
        '''(experimental) Construction properties for ``Connection``.

        :param connection_name: (experimental) The name of the connection. Default: cloudformation generated name
        :param description: (experimental) The description of the connection. Default: no description
        :param match_criteria: (experimental) A list of criteria that can be used in selecting this connection. This is useful for filtering the results of https://awscli.amazonaws.com/v2/documentation/api/latest/reference/glue/get-connections.html Default: no match criteria
        :param properties: (experimental) Key-Value pairs that define parameters for the connection. Default: empty properties
        :param security_groups: (experimental) The list of security groups needed to successfully make this connection e.g. to successfully connect to VPC. Default: no security group
        :param subnet: (experimental) The VPC subnet to connect to resources within a VPC. See more at https://docs.aws.amazon.com/glue/latest/dg/start-connecting.html. Default: no subnet
        :param type: (experimental) The type of the connection.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            
            glue.Connection(self, "MyConnection",
                type=glue.ConnectionType.NETWORK,
                # The security groups granting AWS Glue inbound access to the data source within the VPC
                security_groups=[security_group],
                # The VPC subnet which contains the data source
                subnet=subnet
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3fa037db6ada98c73a1d8889753f75c2f3c7513c8a41daf149dc5769cdb83e8)
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument match_criteria", value=match_criteria, expected_type=type_hints["match_criteria"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet", value=subnet, expected_type=type_hints["subnet"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if connection_name is not None:
            self._values["connection_name"] = connection_name
        if description is not None:
            self._values["description"] = description
        if match_criteria is not None:
            self._values["match_criteria"] = match_criteria
        if properties is not None:
            self._values["properties"] = properties
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet is not None:
            self._values["subnet"] = subnet

    @builtins.property
    def connection_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the connection.

        :default: cloudformation generated name

        :stability: experimental
        '''
        result = self._values.get("connection_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the connection.

        :default: no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def match_criteria(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of criteria that can be used in selecting this connection.

        This is useful for filtering the results of https://awscli.amazonaws.com/v2/documentation/api/latest/reference/glue/get-connections.html

        :default: no match criteria

        :stability: experimental
        '''
        result = self._values.get("match_criteria")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def properties(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Key-Value pairs that define parameters for the connection.

        :default: empty properties

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-connect.html
        :stability: experimental
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The list of security groups needed to successfully make this connection e.g. to successfully connect to VPC.

        :default: no security group

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet]:
        '''(experimental) The VPC subnet to connect to resources within a VPC.

        See more at https://docs.aws.amazon.com/glue/latest/dg/start-connecting.html.

        :default: no subnet

        :stability: experimental
        '''
        result = self._values.get("subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet], result)

    @builtins.property
    def type(self) -> "ConnectionType":
        '''(experimental) The type of the connection.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ConnectionType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ConnectionType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.ConnectionType",
):
    '''(experimental) The type of the glue connection.

    If you need to use a connection type that doesn't exist as a static member, you
    can instantiate a ``ConnectionType`` object, e.g: ``new ConnectionType('NEW_TYPE')``.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-connection-connectioninput.html#cfn-glue-connection-connectioninput-connectiontype
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # security_group: ec2.SecurityGroup
        # subnet: ec2.Subnet
        
        glue.Connection(self, "MyConnection",
            type=glue.ConnectionType.NETWORK,
            # The security groups granting AWS Glue inbound access to the data source within the VPC
            security_groups=[security_group],
            # The VPC subnet which contains the data source
            subnet=subnet
        )
    '''

    def __init__(self, name: builtins.str) -> None:
        '''
        :param name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1f57c94567ffb3d89cdd8c9cd2b37bd37decd390b53c9bfdadd569dc797aa3f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        jsii.create(self.__class__, self, [name])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) The connection type name as expected by Connection resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CUSTOM")
    def CUSTOM(cls) -> "ConnectionType":
        '''(experimental) Uses configuration settings contained in a custom connector to read from and write to data stores that are not natively supported by AWS Glue.

        :stability: experimental
        '''
        return typing.cast("ConnectionType", jsii.sget(cls, "CUSTOM"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="JDBC")
    def JDBC(cls) -> "ConnectionType":
        '''(experimental) Designates a connection to a database through Java Database Connectivity (JDBC).

        :stability: experimental
        '''
        return typing.cast("ConnectionType", jsii.sget(cls, "JDBC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="KAFKA")
    def KAFKA(cls) -> "ConnectionType":
        '''(experimental) Designates a connection to an Apache Kafka streaming platform.

        :stability: experimental
        '''
        return typing.cast("ConnectionType", jsii.sget(cls, "KAFKA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MARKETPLACE")
    def MARKETPLACE(cls) -> "ConnectionType":
        '''(experimental) Uses configuration settings contained in a connector purchased from AWS Marketplace to read from and write to data stores that are not natively supported by AWS Glue.

        :stability: experimental
        '''
        return typing.cast("ConnectionType", jsii.sget(cls, "MARKETPLACE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MONGODB")
    def MONGODB(cls) -> "ConnectionType":
        '''(experimental) Designates a connection to a MongoDB document database.

        :stability: experimental
        '''
        return typing.cast("ConnectionType", jsii.sget(cls, "MONGODB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NETWORK")
    def NETWORK(cls) -> "ConnectionType":
        '''(experimental) Designates a network connection to a data source within an Amazon Virtual Private Cloud environment (Amazon VPC).

        :stability: experimental
        '''
        return typing.cast("ConnectionType", jsii.sget(cls, "NETWORK"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this ConnectionType, as expected by Connection resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.ContinuousLoggingProps",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "conversion_pattern": "conversionPattern",
        "log_group": "logGroup",
        "log_stream_prefix": "logStreamPrefix",
        "quiet": "quiet",
    },
)
class ContinuousLoggingProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        conversion_pattern: typing.Optional[builtins.str] = None,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        log_stream_prefix: typing.Optional[builtins.str] = None,
        quiet: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Properties for enabling Continuous Logging for Glue Jobs.

        :param enabled: (experimental) Enable continouous logging.
        :param conversion_pattern: (experimental) Apply the provided conversion pattern. This is a Log4j Conversion Pattern to customize driver and executor logs. Default: ``%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n``
        :param log_group: (experimental) Specify a custom CloudWatch log group name. Default: - a log group is created with name ``/aws-glue/jobs/logs-v2/``.
        :param log_stream_prefix: (experimental) Specify a custom CloudWatch log stream prefix. Default: - the job run ID.
        :param quiet: (experimental) Filter out non-useful Apache Spark driver/executor and Apache Hadoop YARN heartbeat log messages. Default: true

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            from aws_cdk import aws_logs as logs
            
            # log_group: logs.LogGroup
            
            continuous_logging_props = glue_alpha.ContinuousLoggingProps(
                enabled=False,
            
                # the properties below are optional
                conversion_pattern="conversionPattern",
                log_group=log_group,
                log_stream_prefix="logStreamPrefix",
                quiet=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6be4bb41017f52f2aa453e36400fa3a47b2e6bf3a87cf64d46e0345d6f22428b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument conversion_pattern", value=conversion_pattern, expected_type=type_hints["conversion_pattern"])
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument log_stream_prefix", value=log_stream_prefix, expected_type=type_hints["log_stream_prefix"])
            check_type(argname="argument quiet", value=quiet, expected_type=type_hints["quiet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if conversion_pattern is not None:
            self._values["conversion_pattern"] = conversion_pattern
        if log_group is not None:
            self._values["log_group"] = log_group
        if log_stream_prefix is not None:
            self._values["log_stream_prefix"] = log_stream_prefix
        if quiet is not None:
            self._values["quiet"] = quiet

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''(experimental) Enable continouous logging.

        :stability: experimental
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def conversion_pattern(self) -> typing.Optional[builtins.str]:
        '''(experimental) Apply the provided conversion pattern.

        This is a Log4j Conversion Pattern to customize driver and executor logs.

        :default: ``%d{yy/MM/dd HH:mm:ss} %p %c{1}: %m%n``

        :stability: experimental
        '''
        result = self._values.get("conversion_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        '''(experimental) Specify a custom CloudWatch log group name.

        :default: - a log group is created with name ``/aws-glue/jobs/logs-v2/``.

        :stability: experimental
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def log_stream_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify a custom CloudWatch log stream prefix.

        :default: - the job run ID.

        :stability: experimental
        '''
        result = self._values.get("log_stream_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def quiet(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Filter out non-useful Apache Spark driver/executor and Apache Hadoop YARN heartbeat log messages.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("quiet")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContinuousLoggingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataFormat(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.DataFormat",
):
    '''(experimental) Defines the input/output formats and ser/de for a single DataFormat.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_database: glue.Database
        
        glue.S3Table(self, "MyTable",
            database=my_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            partition_keys=[glue.Column(
                name="year",
                type=glue.Schema.SMALL_INT
            ), glue.Column(
                name="month",
                type=glue.Schema.SMALL_INT
            )],
            data_format=glue.DataFormat.JSON
        )
    '''

    def __init__(
        self,
        *,
        input_format: "InputFormat",
        output_format: "OutputFormat",
        serialization_library: "SerializationLibrary",
        classification_string: typing.Optional[ClassificationString] = None,
    ) -> None:
        '''
        :param input_format: (experimental) ``InputFormat`` for this data format.
        :param output_format: (experimental) ``OutputFormat`` for this data format.
        :param serialization_library: (experimental) Serialization library for this data format.
        :param classification_string: (experimental) Classification string given to tables with this data format. Default: - No classification is specified.

        :stability: experimental
        '''
        props = DataFormatProps(
            input_format=input_format,
            output_format=output_format,
            serialization_library=serialization_library,
            classification_string=classification_string,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="APACHE_LOGS")
    def APACHE_LOGS(cls) -> "DataFormat":
        '''(experimental) DataFormat for Apache Web Server Logs.

        Also works for CloudFront logs

        :see: https://docs.aws.amazon.com/athena/latest/ug/apache.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "APACHE_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> "DataFormat":
        '''(experimental) DataFormat for Apache Avro.

        :see: https://docs.aws.amazon.com/athena/latest/ug/avro.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDTRAIL_LOGS")
    def CLOUDTRAIL_LOGS(cls) -> "DataFormat":
        '''(experimental) DataFormat for CloudTrail logs stored on S3.

        :see: https://docs.aws.amazon.com/athena/latest/ug/cloudtrail.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "CLOUDTRAIL_LOGS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CSV")
    def CSV(cls) -> "DataFormat":
        '''(experimental) DataFormat for CSV Files.

        :see: https://docs.aws.amazon.com/athena/latest/ug/csv.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "CSV"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="JSON")
    def JSON(cls) -> "DataFormat":
        '''(experimental) Stored as plain text files in JSON format.

        Uses OpenX Json SerDe for serialization and deseralization.

        :see: https://docs.aws.amazon.com/athena/latest/ug/json.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "JSON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOGSTASH")
    def LOGSTASH(cls) -> "DataFormat":
        '''(experimental) DataFormat for Logstash Logs, using the GROK SerDe.

        :see: https://docs.aws.amazon.com/athena/latest/ug/grok.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "LOGSTASH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> "DataFormat":
        '''(experimental) DataFormat for Apache ORC (Optimized Row Columnar).

        :see: https://docs.aws.amazon.com/athena/latest/ug/orc.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "DataFormat":
        '''(experimental) DataFormat for Apache Parquet.

        :see: https://docs.aws.amazon.com/athena/latest/ug/parquet.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "PARQUET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TSV")
    def TSV(cls) -> "DataFormat":
        '''(experimental) DataFormat for TSV (Tab-Separated Values).

        :see: https://docs.aws.amazon.com/athena/latest/ug/lazy-simple-serde.html
        :stability: experimental
        '''
        return typing.cast("DataFormat", jsii.sget(cls, "TSV"))

    @builtins.property
    @jsii.member(jsii_name="inputFormat")
    def input_format(self) -> "InputFormat":
        '''(experimental) ``InputFormat`` for this data format.

        :stability: experimental
        '''
        return typing.cast("InputFormat", jsii.get(self, "inputFormat"))

    @builtins.property
    @jsii.member(jsii_name="outputFormat")
    def output_format(self) -> "OutputFormat":
        '''(experimental) ``OutputFormat`` for this data format.

        :stability: experimental
        '''
        return typing.cast("OutputFormat", jsii.get(self, "outputFormat"))

    @builtins.property
    @jsii.member(jsii_name="serializationLibrary")
    def serialization_library(self) -> "SerializationLibrary":
        '''(experimental) Serialization library for this data format.

        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.get(self, "serializationLibrary"))

    @builtins.property
    @jsii.member(jsii_name="classificationString")
    def classification_string(self) -> typing.Optional[ClassificationString]:
        '''(experimental) Classification string given to tables with this data format.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ClassificationString], jsii.get(self, "classificationString"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.DataFormatProps",
    jsii_struct_bases=[],
    name_mapping={
        "input_format": "inputFormat",
        "output_format": "outputFormat",
        "serialization_library": "serializationLibrary",
        "classification_string": "classificationString",
    },
)
class DataFormatProps:
    def __init__(
        self,
        *,
        input_format: "InputFormat",
        output_format: "OutputFormat",
        serialization_library: "SerializationLibrary",
        classification_string: typing.Optional[ClassificationString] = None,
    ) -> None:
        '''(experimental) Properties of a DataFormat instance.

        :param input_format: (experimental) ``InputFormat`` for this data format.
        :param output_format: (experimental) ``OutputFormat`` for this data format.
        :param serialization_library: (experimental) Serialization library for this data format.
        :param classification_string: (experimental) Classification string given to tables with this data format. Default: - No classification is specified.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            
            # classification_string: glue_alpha.ClassificationString
            # input_format: glue_alpha.InputFormat
            # output_format: glue_alpha.OutputFormat
            # serialization_library: glue_alpha.SerializationLibrary
            
            data_format_props = glue_alpha.DataFormatProps(
                input_format=input_format,
                output_format=output_format,
                serialization_library=serialization_library,
            
                # the properties below are optional
                classification_string=classification_string
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5302ed9f621270e44cf453ed62f78ee39e66f12961a87e084ec3d874438a19f)
            check_type(argname="argument input_format", value=input_format, expected_type=type_hints["input_format"])
            check_type(argname="argument output_format", value=output_format, expected_type=type_hints["output_format"])
            check_type(argname="argument serialization_library", value=serialization_library, expected_type=type_hints["serialization_library"])
            check_type(argname="argument classification_string", value=classification_string, expected_type=type_hints["classification_string"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_format": input_format,
            "output_format": output_format,
            "serialization_library": serialization_library,
        }
        if classification_string is not None:
            self._values["classification_string"] = classification_string

    @builtins.property
    def input_format(self) -> "InputFormat":
        '''(experimental) ``InputFormat`` for this data format.

        :stability: experimental
        '''
        result = self._values.get("input_format")
        assert result is not None, "Required property 'input_format' is missing"
        return typing.cast("InputFormat", result)

    @builtins.property
    def output_format(self) -> "OutputFormat":
        '''(experimental) ``OutputFormat`` for this data format.

        :stability: experimental
        '''
        result = self._values.get("output_format")
        assert result is not None, "Required property 'output_format' is missing"
        return typing.cast("OutputFormat", result)

    @builtins.property
    def serialization_library(self) -> "SerializationLibrary":
        '''(experimental) Serialization library for this data format.

        :stability: experimental
        '''
        result = self._values.get("serialization_library")
        assert result is not None, "Required property 'serialization_library' is missing"
        return typing.cast("SerializationLibrary", result)

    @builtins.property
    def classification_string(self) -> typing.Optional[ClassificationString]:
        '''(experimental) Classification string given to tables with this data format.

        :default: - No classification is specified.

        :stability: experimental
        '''
        result = self._values.get("classification_string")
        return typing.cast(typing.Optional[ClassificationString], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataFormatProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.DataQualityRulesetProps",
    jsii_struct_bases=[],
    name_mapping={
        "ruleset_dqdl": "rulesetDqdl",
        "target_table": "targetTable",
        "client_token": "clientToken",
        "description": "description",
        "ruleset_name": "rulesetName",
        "tags": "tags",
    },
)
class DataQualityRulesetProps:
    def __init__(
        self,
        *,
        ruleset_dqdl: builtins.str,
        target_table: "DataQualityTargetTable",
        client_token: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        ruleset_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Construction properties for ``DataQualityRuleset``.

        :param ruleset_dqdl: (experimental) The dqdl of the ruleset.
        :param target_table: (experimental) The target table of the ruleset.
        :param client_token: (experimental) The client token of the ruleset.
        :param description: (experimental) The description of the ruleset.
        :param ruleset_name: (experimental) The name of the ruleset. Default: cloudformation generated name
        :param tags: (experimental) Key-Value pairs that define tags for the ruleset. Default: empty tags

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.DataQualityRuleset(self, "MyDataQualityRuleset",
                client_token="client_token",
                description="description",
                ruleset_name="ruleset_name",
                ruleset_dqdl="ruleset_dqdl",
                tags={
                    "key1": "value1",
                    "key2": "value2"
                },
                target_table=glue.DataQualityTargetTable("database_name", "table_name")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abda2570732c667a87dd412c9aa6c70d5db49ac0b525ecc9c3c801e1271e451a)
            check_type(argname="argument ruleset_dqdl", value=ruleset_dqdl, expected_type=type_hints["ruleset_dqdl"])
            check_type(argname="argument target_table", value=target_table, expected_type=type_hints["target_table"])
            check_type(argname="argument client_token", value=client_token, expected_type=type_hints["client_token"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ruleset_name", value=ruleset_name, expected_type=type_hints["ruleset_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ruleset_dqdl": ruleset_dqdl,
            "target_table": target_table,
        }
        if client_token is not None:
            self._values["client_token"] = client_token
        if description is not None:
            self._values["description"] = description
        if ruleset_name is not None:
            self._values["ruleset_name"] = ruleset_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ruleset_dqdl(self) -> builtins.str:
        '''(experimental) The dqdl of the ruleset.

        :stability: experimental
        :attribute: true
        '''
        result = self._values.get("ruleset_dqdl")
        assert result is not None, "Required property 'ruleset_dqdl' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target_table(self) -> "DataQualityTargetTable":
        '''(experimental) The target table of the ruleset.

        :stability: experimental
        :attribute: true
        '''
        result = self._values.get("target_table")
        assert result is not None, "Required property 'target_table' is missing"
        return typing.cast("DataQualityTargetTable", result)

    @builtins.property
    def client_token(self) -> typing.Optional[builtins.str]:
        '''(experimental) The client token of the ruleset.

        :stability: experimental
        :attribute: true
        '''
        result = self._values.get("client_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the ruleset.

        :stability: experimental
        :attribute: true
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ruleset_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the ruleset.

        :default: cloudformation generated name

        :stability: experimental
        '''
        result = self._values.get("ruleset_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Key-Value pairs that define tags for the ruleset.

        :default: empty tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataQualityRulesetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataQualityTargetTable(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.DataQualityTargetTable",
):
    '''(experimental) Properties of a DataQualityTargetTable.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.DataQualityRuleset(self, "MyDataQualityRuleset",
            client_token="client_token",
            description="description",
            ruleset_name="ruleset_name",
            ruleset_dqdl="ruleset_dqdl",
            tags={
                "key1": "value1",
                "key2": "value2"
            },
            target_table=glue.DataQualityTargetTable("database_name", "table_name")
        )
    '''

    def __init__(self, database_name: builtins.str, table_name: builtins.str) -> None:
        '''
        :param database_name: -
        :param table_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18073ec885df4d5126a63d11958df64b1c8b43f719ce0fd6c6c594b457b6d4af)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        jsii.create(self.__class__, self, [database_name, table_name])

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''(experimental) The database name of the target table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) The table name of the target table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.DatabaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "database_name": "databaseName",
        "description": "description",
        "location_uri": "locationUri",
    },
)
class DatabaseProps:
    def __init__(
        self,
        *,
        database_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        location_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param database_name: (experimental) The name of the database. Default: - generated by CDK.
        :param description: (experimental) A description of the database. Default: - no database description
        :param location_uri: (experimental) The location of the database (for example, an HDFS path). Default: undefined. This field is optional in AWS::Glue::Database DatabaseInput

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.Database(self, "MyDatabase",
                database_name="my_database",
                description="my_database_description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d07df31a9d41958f45422a1d7914c5016d66ed0e46a7e97ab37e2dd3d42ecf38)
            check_type(argname="argument database_name", value=database_name, expected_type=type_hints["database_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument location_uri", value=location_uri, expected_type=type_hints["location_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if database_name is not None:
            self._values["database_name"] = database_name
        if description is not None:
            self._values["description"] = description
        if location_uri is not None:
            self._values["location_uri"] = location_uri

    @builtins.property
    def database_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the database.

        :default: - generated by CDK.

        :stability: experimental
        '''
        result = self._values.get("database_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the database.

        :default: - no database description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def location_uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) The location of the database (for example, an HDFS path).

        :default: undefined. This field is optional in AWS::Glue::Database DatabaseInput

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-database-databaseinput.html
        :stability: experimental
        '''
        result = self._values.get("location_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.ExecutionClass")
class ExecutionClass(enum.Enum):
    '''(experimental) The ExecutionClass whether the job is run with a standard or flexible execution class.

    :see: https://docs.aws.amazon.com/glue/latest/dg/add-job.html
    :stability: experimental
    '''

    FLEX = "FLEX"
    '''(experimental) The flexible execution class is appropriate for time-insensitive jobs whose start and completion times may vary.

    :stability: experimental
    '''
    STANDARD = "STANDARD"
    '''(experimental) The standard execution class is ideal for time-sensitive workloads that require fast job startup and dedicated resources.

    :stability: experimental
    '''


class GlueVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.GlueVersion",
):
    '''(experimental) AWS Glue version determines the versions of Apache Spark and Python that are available to the job.

    :see:

    https://docs.aws.amazon.com/glue/latest/dg/add-job.html.

    If you need to use a GlueVersion that doesn't exist as a static member, you
    can instantiate a ``GlueVersion`` object, e.g: ``GlueVersion.of('1.5')``.
    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.Job(self, "EnableRunQueuing",
            job_name="EtlJobWithRunQueuing",
            executable=glue.JobExecutable.python_etl(
                glue_version=glue.GlueVersion.V4_0,
                python_version=glue.PythonVersion.THREE,
                script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
            ),
            job_run_queuing_enabled=True
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, version: builtins.str) -> "GlueVersion":
        '''(experimental) Custom Glue version.

        :param version: custom version.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf24e914c5a2058c5a8ba633944792fe46a62d0d67ae96056f15edaf764112b)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        return typing.cast("GlueVersion", jsii.sinvoke(cls, "of", [version]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V0_9")
    def V0_9(cls) -> "GlueVersion":
        '''(experimental) Glue version using Spark 2.2.1 and Python 2.7.

        :stability: experimental
        '''
        return typing.cast("GlueVersion", jsii.sget(cls, "V0_9"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_0")
    def V1_0(cls) -> "GlueVersion":
        '''(experimental) Glue version using Spark 2.4.3, Python 2.7 and Python 3.6.

        :stability: experimental
        '''
        return typing.cast("GlueVersion", jsii.sget(cls, "V1_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_0")
    def V2_0(cls) -> "GlueVersion":
        '''(experimental) Glue version using Spark 2.4.3 and Python 3.7.

        :stability: experimental
        '''
        return typing.cast("GlueVersion", jsii.sget(cls, "V2_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V3_0")
    def V3_0(cls) -> "GlueVersion":
        '''(experimental) Glue version using Spark 3.1.1 and Python 3.7.

        :stability: experimental
        '''
        return typing.cast("GlueVersion", jsii.sget(cls, "V3_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V4_0")
    def V4_0(cls) -> "GlueVersion":
        '''(experimental) Glue version using Spark 3.3.0 and Python 3.10.

        :stability: experimental
        '''
        return typing.cast("GlueVersion", jsii.sget(cls, "V4_0"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this GlueVersion, as expected by Job resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.interface(jsii_type="@aws-cdk/aws-glue-alpha.IConnection")
class IConnection(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Interface representing a created or an imported ``Connection``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the connection.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''(experimental) The name of the connection.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IConnectionProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Interface representing a created or an imported ``Connection``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-glue-alpha.IConnection"

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''(experimental) The name of the connection.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IConnection).__jsii_proxy_class__ = lambda : _IConnectionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-glue-alpha.IDataQualityRuleset")
class IDataQualityRuleset(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="rulesetArn")
    def ruleset_arn(self) -> builtins.str:
        '''(experimental) The ARN of the ruleset.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="rulesetName")
    def ruleset_name(self) -> builtins.str:
        '''(experimental) The name of the ruleset.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IDataQualityRulesetProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-glue-alpha.IDataQualityRuleset"

    @builtins.property
    @jsii.member(jsii_name="rulesetArn")
    def ruleset_arn(self) -> builtins.str:
        '''(experimental) The ARN of the ruleset.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "rulesetArn"))

    @builtins.property
    @jsii.member(jsii_name="rulesetName")
    def ruleset_name(self) -> builtins.str:
        '''(experimental) The name of the ruleset.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "rulesetName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDataQualityRuleset).__jsii_proxy_class__ = lambda : _IDataQualityRulesetProxy


@jsii.interface(jsii_type="@aws-cdk/aws-glue-alpha.IDatabase")
class IDatabase(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> builtins.str:
        '''(experimental) The ARN of the catalog.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        '''(experimental) The catalog id of the database (usually, the AWS account id).

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> builtins.str:
        '''(experimental) The ARN of the database.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''(experimental) The name of the database.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IDatabaseProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-glue-alpha.IDatabase"

    @builtins.property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> builtins.str:
        '''(experimental) The ARN of the catalog.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "catalogArn"))

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        '''(experimental) The catalog id of the database (usually, the AWS account id).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "catalogId"))

    @builtins.property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> builtins.str:
        '''(experimental) The ARN of the database.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseArn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''(experimental) The name of the database.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDatabase).__jsii_proxy_class__ = lambda : _IDatabaseProxy


@jsii.interface(jsii_type="@aws-cdk/aws-glue-alpha.IJob")
class IJob(
    _aws_cdk_ceddda9d.IResource,
    _aws_cdk_aws_iam_ceddda9d.IGrantable,
    typing_extensions.Protocol,
):
    '''(experimental) Interface representing a created or an imported ``Job``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="jobArn")
    def job_arn(self) -> builtins.str:
        '''(experimental) The ARN of the job.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''(experimental) The name of the job.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        type: "MetricType",
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch metric.

        :param metric_name: name of the metric typically prefixed with ``glue.driver.``, ``glue.<executorId>.`` or ``glue.ALL.``.
        :param type: the metric type.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :see: https://docs.aws.amazon.com/glue/latest/dg/monitoring-awsglue-with-cloudwatch-metrics.html
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricFailure")
    def metric_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch Metric indicating job failure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricSuccess")
    def metric_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch Metric indicating job success.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metricTimeout")
    def metric_timeout(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch Metric indicating job timeout.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when something happens with this job.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onFailure")
    def on_failure(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when this job moves to the FAILED state.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        job_state: "JobState",
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when this job moves to the input jobState.

        :param id: -
        :param job_state: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onSuccess")
    def on_success(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when this job moves to the SUCCEEDED state.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="onTimeout")
    def on_timeout(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when this job moves to the TIMEOUT state.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        ...


class _IJobProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_iam_ceddda9d.IGrantable), # type: ignore[misc]
):
    '''(experimental) Interface representing a created or an imported ``Job``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-glue-alpha.IJob"

    @builtins.property
    @jsii.member(jsii_name="jobArn")
    def job_arn(self) -> builtins.str:
        '''(experimental) The ARN of the job.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobArn"))

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''(experimental) The name of the job.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        type: "MetricType",
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch metric.

        :param metric_name: name of the metric typically prefixed with ``glue.driver.``, ``glue.<executorId>.`` or ``glue.ALL.``.
        :param type: the metric type.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :see: https://docs.aws.amazon.com/glue/latest/dg/monitoring-awsglue-with-cloudwatch-metrics.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f8eb7ba0850dad06f49887b6323e6019fa48cdf967d96e579591ff36e61765)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, type, props]))

    @jsii.member(jsii_name="metricFailure")
    def metric_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch Metric indicating job failure.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricFailure", [props]))

    @jsii.member(jsii_name="metricSuccess")
    def metric_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch Metric indicating job success.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSuccess", [props]))

    @jsii.member(jsii_name="metricTimeout")
    def metric_timeout(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch Metric indicating job timeout.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTimeout", [props]))

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when something happens with this job.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e9bb641a392e36442ae2624591822707bc3af7603043bcb85c82e6dde0aedff)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onEvent", [id, options]))

    @jsii.member(jsii_name="onFailure")
    def on_failure(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when this job moves to the FAILED state.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__192bf1eecc268b3f759e65151917fb49666d5a0144c2df120f2dd72e3fd5e4f4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onFailure", [id, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        job_state: "JobState",
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when this job moves to the input jobState.

        :param id: -
        :param job_state: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab9c989bad00c9e92013f90e2646073cc90125f09e75268ec3f2999a69b9b8d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_state", value=job_state, expected_type=type_hints["job_state"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onStateChange", [id, job_state, options]))

    @jsii.member(jsii_name="onSuccess")
    def on_success(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when this job moves to the SUCCEEDED state.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b62843a9fea91eb93e6bf7bcd95a76fc790b72a6a7ae7024cf486b3fd9d20f7)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onSuccess", [id, options]))

    @jsii.member(jsii_name="onTimeout")
    def on_timeout(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Defines a CloudWatch event rule triggered when this job moves to the TIMEOUT state.

        :param id: -
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1fcdc972ccb29fe1572e8970cb83faccd76d7cee7f09ed3f5c9571bca7a886d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onTimeout", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJob).__jsii_proxy_class__ = lambda : _IJobProxy


@jsii.interface(jsii_type="@aws-cdk/aws-glue-alpha.ISecurityConfiguration")
class ISecurityConfiguration(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Interface representing a created or an imported ``SecurityConfiguration``.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="securityConfigurationName")
    def security_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the security configuration.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ISecurityConfigurationProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Interface representing a created or an imported ``SecurityConfiguration``.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-glue-alpha.ISecurityConfiguration"

    @builtins.property
    @jsii.member(jsii_name="securityConfigurationName")
    def security_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the security configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "securityConfigurationName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecurityConfiguration).__jsii_proxy_class__ = lambda : _ISecurityConfigurationProxy


@jsii.interface(jsii_type="@aws-cdk/aws-glue-alpha.ITable")
class ITable(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        ...


class _ITableProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-glue-alpha.ITable"

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''
        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ITable).__jsii_proxy_class__ = lambda : _ITableProxy


class InputFormat(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.InputFormat",
):
    '''(experimental) Absolute class name of the Hadoop ``InputFormat`` to use when reading table files.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_glue_alpha as glue_alpha
        
        input_format = glue_alpha.InputFormat.AVRO
    '''

    def __init__(self, class_name: builtins.str) -> None:
        '''
        :param class_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__697ee4e4007ce058f39e7fc610b2c0c4457bbd6008e9287406b18505ed299434)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
        jsii.create(self.__class__, self, [class_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> "InputFormat":
        '''(experimental) InputFormat for Avro files.

        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/avro/AvroContainerInputFormat.html
        :stability: experimental
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDTRAIL")
    def CLOUDTRAIL(cls) -> "InputFormat":
        '''(experimental) InputFormat for Cloudtrail Logs.

        :see: https://docs.aws.amazon.com/athena/latest/ug/cloudtrail.html
        :stability: experimental
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "CLOUDTRAIL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> "InputFormat":
        '''(experimental) InputFormat for Orc files.

        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/orc/OrcInputFormat.html
        :stability: experimental
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "InputFormat":
        '''(experimental) InputFormat for Parquet files.

        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/parquet/MapredParquetInputFormat.html
        :stability: experimental
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "PARQUET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TEXT")
    def TEXT(cls) -> "InputFormat":
        '''(experimental) An InputFormat for plain text files.

        Files are broken into lines. Either linefeed or
        carriage-return are used to signal end of line. Keys are the position in the file, and
        values are the line of text.
        JSON & CSV files are examples of this InputFormat

        :see: https://hadoop.apache.org/docs/stable/api/org/apache/hadoop/mapred/TextInputFormat.html
        :stability: experimental
        '''
        return typing.cast("InputFormat", jsii.sget(cls, "TEXT"))

    @builtins.property
    @jsii.member(jsii_name="className")
    def class_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "className"))


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.InvalidCharHandlingAction")
class InvalidCharHandlingAction(enum.Enum):
    '''(experimental) Specifies the action to perform when query results contain invalid UTF-8 character values.

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"* > *"invalid_char_handling"*
    :stability: experimental
    '''

    DISABLED = "DISABLED"
    '''(experimental) Doesn't perform invalid character handling.

    :stability: experimental
    '''
    FAIL = "FAIL"
    '''(experimental) Cancels queries that return data containing invalid UTF-8 values.

    :stability: experimental
    '''
    SET_TO_NULL = "SET_TO_NULL"
    '''(experimental) Replaces invalid UTF-8 values with null.

    :stability: experimental
    '''
    DROP_ROW = "DROP_ROW"
    '''(experimental) Replaces each value in the row with null.

    :stability: experimental
    '''
    REPLACE = "REPLACE"
    '''(experimental) Replaces the invalid character with the replacement character you specify using ``REPLACEMENT_CHAR``.

    :stability: experimental
    '''


@jsii.implements(IJob)
class Job(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.Job",
):
    '''(experimental) A Glue Job.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.Job(self, "EnableRunQueuing",
            job_name="EtlJobWithRunQueuing",
            executable=glue.JobExecutable.python_etl(
                glue_version=glue.GlueVersion.V4_0,
                python_version=glue.PythonVersion.THREE,
                script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
            ),
            job_run_queuing_enabled=True
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        executable: "JobExecutable",
        connections: typing.Optional[typing.Sequence[IConnection]] = None,
        continuous_logging: typing.Optional[typing.Union[ContinuousLoggingProps, typing.Dict[builtins.str, typing.Any]]] = None,
        default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_profiling_metrics: typing.Optional[builtins.bool] = None,
        execution_class: typing.Optional[ExecutionClass] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_run_queuing_enabled: typing.Optional[builtins.bool] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        notify_delay_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_configuration: typing.Optional[ISecurityConfiguration] = None,
        spark_ui: typing.Optional[typing.Union["SparkUIProps", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        worker_count: typing.Optional[jsii.Number] = None,
        worker_type: typing.Optional["WorkerType"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param executable: (experimental) The job's executable properties.
        :param connections: (experimental) The ``Connection``s used for this job. Connections are used to connect to other AWS Service or resources within a VPC. Default: [] - no connections are added to the job
        :param continuous_logging: (experimental) Enables continuous logging with the specified props. Default: - continuous logging is disabled.
        :param default_arguments: (experimental) The default arguments for this job, specified as name-value pairs. Default: - no arguments
        :param description: (experimental) The description of the job. Default: - no value
        :param enable_profiling_metrics: (experimental) Enables the collection of metrics for job profiling. Equivalent to a job parameter ``--enable-metrics``. Default: - no profiling metrics emitted.
        :param execution_class: (experimental) The ExecutionClass whether the job is run with a standard or flexible execution class. Default: - STANDARD
        :param job_name: (experimental) The name of the job. Default: - a name is automatically generated
        :param job_run_queuing_enabled: (experimental) Specifies whether job run queuing is enabled for the job runs for this job. A value of true means job run queuing is enabled for the job runs. If false or not populated, the job runs will not be considered for queueing. If this field does not match the value set in the job run, then the value from the job run field will be used. Default: - no job run queuing
        :param max_capacity: (experimental) The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs. Cannot be used for Glue version 2.0 and later - workerType and workerCount should be used instead. Default: - 10 when job type is Apache Spark ETL or streaming, 0.0625 when job type is Python shell
        :param max_concurrent_runs: (experimental) The maximum number of concurrent runs allowed for the job. An error is returned when this threshold is reached. The maximum value you can specify is controlled by a service limit. Default: 1
        :param max_retries: (experimental) The maximum number of times to retry this job after a job run fails. Default: 0
        :param notify_delay_after: (experimental) The number of minutes to wait after a job run starts, before sending a job run delay notification. Default: - no delay notifications
        :param role: (experimental) The IAM role assumed by Glue to run this job. If providing a custom role, it needs to trust the Glue service principal (glue.amazonaws.com) and be granted sufficient permissions. Default: - a role is automatically generated
        :param security_configuration: (experimental) The ``SecurityConfiguration`` to use for this job. Default: - no security configuration.
        :param spark_ui: (experimental) Enables the Spark UI debugging and monitoring with the specified props. Default: - Spark UI debugging and monitoring is disabled.
        :param tags: (experimental) The tags to add to the resources on which the job runs. Default: {} - no tags
        :param timeout: (experimental) The maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. Default: cdk.Duration.hours(48)
        :param worker_count: (experimental) The number of workers of a defined ``WorkerType`` that are allocated when a job runs. Default: - differs based on specific Glue version/worker type
        :param worker_type: (experimental) The type of predefined worker that is allocated when a job runs. Default: - differs based on specific Glue version

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6176c370f308e8911be636fb1acf643512dbe9ca58823d8267644ab7efc406c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JobProps(
            executable=executable,
            connections=connections,
            continuous_logging=continuous_logging,
            default_arguments=default_arguments,
            description=description,
            enable_profiling_metrics=enable_profiling_metrics,
            execution_class=execution_class,
            job_name=job_name,
            job_run_queuing_enabled=job_run_queuing_enabled,
            max_capacity=max_capacity,
            max_concurrent_runs=max_concurrent_runs,
            max_retries=max_retries,
            notify_delay_after=notify_delay_after,
            role=role,
            security_configuration=security_configuration,
            spark_ui=spark_ui,
            tags=tags,
            timeout=timeout,
            worker_count=worker_count,
            worker_type=worker_type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobAttributes")
    @builtins.classmethod
    def from_job_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        job_name: builtins.str,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> IJob:
        '''(experimental) Creates a Glue Job.

        :param scope: The scope creating construct (usually ``this``).
        :param id: The construct's id.
        :param job_name: (experimental) The name of the job.
        :param role: (experimental) The IAM role assumed by Glue to run this job. Default: - undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd8db6c08c7bba32e81d8cda162918f634f3065c707bdd1ddfb404e329994882)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = JobAttributes(job_name=job_name, role=role)

        return typing.cast(IJob, jsii.sinvoke(cls, "fromJobAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        type: "MetricType",
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Create a CloudWatch metric.

        :param metric_name: name of the metric typically prefixed with ``glue.driver.``, ``glue.<executorId>.`` or ``glue.ALL.``.
        :param type: the metric type.
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :see: https://docs.aws.amazon.com/glue/latest/dg/monitoring-awsglue-with-cloudwatch-metrics.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c143c24940c0f180cf99d417380821b95c0287b9b01c42df4f74c6e7959a56b8)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, type, props]))

    @jsii.member(jsii_name="metricFailure")
    def metric_failure(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return a CloudWatch Metric indicating job failure.

        This metric is based on the Rule returned by no-args onFailure() call.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricFailure", [props]))

    @jsii.member(jsii_name="metricSuccess")
    def metric_success(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return a CloudWatch Metric indicating job success.

        This metric is based on the Rule returned by no-args onSuccess() call.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSuccess", [props]))

    @jsii.member(jsii_name="metricTimeout")
    def metric_timeout(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(experimental) Return a CloudWatch Metric indicating job timeout.

        This metric is based on the Rule returned by no-args onTimeout() call.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTimeout", [props]))

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Create a CloudWatch Event Rule for this Glue Job when it's in a given state.

        :param id: construct id.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d8262e07cdf8942bd30cd21bf9d73a8b85e3b2683e99b4f40ed03fbf49b57ac)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onEvent", [id, options]))

    @jsii.member(jsii_name="onFailure")
    def on_failure(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Return a CloudWatch Event Rule matching FAILED state.

        :param id: construct id.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8a1d8b4180629a6e1364fed24a3f246786b2d528b0ef21dda37098ac2af2c9a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onFailure", [id, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        id: builtins.str,
        job_state: "JobState",
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Create a CloudWatch Event Rule for the transition into the input jobState.

        :param id: construct id.
        :param job_state: the job state.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0546c2bad534dee21310d2705463267023bd2bd40cd093c29b95dccda7c69228)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_state", value=job_state, expected_type=type_hints["job_state"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onStateChange", [id, job_state, options]))

    @jsii.member(jsii_name="onSuccess")
    def on_success(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Create a CloudWatch Event Rule matching JobState.SUCCEEDED.

        :param id: construct id.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8390e01882a245ed021fa1f65648219d84b9932b1c593026055b61fe2c56a85)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onSuccess", [id, options]))

    @jsii.member(jsii_name="onTimeout")
    def on_timeout(
        self,
        id: builtins.str,
        *,
        target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
        cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
        description: typing.Optional[builtins.str] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''(experimental) Return a CloudWatch Event Rule matching TIMEOUT state.

        :param id: construct id.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.
        :param cross_stack_scope: The scope to use if the source of the rule and its target are in different Stacks (but in the same account & region). This helps dealing with cycles that often arise in these situations. Default: - none (the main scope will be used, even for cross-stack Events)
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b061eb382ce02e7e8798f77ad4abe593f170f59b9df192c9e6c5fb3de7901a33)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _aws_cdk_aws_events_ceddda9d.OnEventOptions(
            target=target,
            cross_stack_scope=cross_stack_scope,
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
        )

        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "onTimeout", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _aws_cdk_aws_iam_ceddda9d.IPrincipal:
        '''(experimental) The principal this Glue Job is running as.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="jobArn")
    def job_arn(self) -> builtins.str:
        '''(experimental) The ARN of the job.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobArn"))

    @builtins.property
    @jsii.member(jsii_name="jobName")
    def job_name(self) -> builtins.str:
        '''(experimental) The name of the job.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobName"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The IAM role Glue assumes to run this job.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="sparkUILoggingLocation")
    def spark_ui_logging_location(self) -> typing.Optional["SparkUILoggingLocation"]:
        '''(experimental) The Spark UI logs location if Spark UI monitoring and debugging is enabled.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional["SparkUILoggingLocation"], jsii.get(self, "sparkUILoggingLocation"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.JobAttributes",
    jsii_struct_bases=[],
    name_mapping={"job_name": "jobName", "role": "role"},
)
class JobAttributes:
    def __init__(
        self,
        *,
        job_name: builtins.str,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(experimental) Attributes for importing ``Job``.

        :param job_name: (experimental) The name of the job.
        :param role: (experimental) The IAM role assumed by Glue to run this job. Default: - undefined

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            job_attributes = glue_alpha.JobAttributes(
                job_name="jobName",
            
                # the properties below are optional
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f1f5ae0406d4aaf443249ea9377b38a10b1814ed1f9c1fb9f0cbc5f489fd89e)
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "job_name": job_name,
        }
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def job_name(self) -> builtins.str:
        '''(experimental) The name of the job.

        :stability: experimental
        '''
        result = self._values.get("job_name")
        assert result is not None, "Required property 'job_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role assumed by Glue to run this job.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.JobBookmarksEncryption",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "kms_key": "kmsKey"},
)
class JobBookmarksEncryption:
    def __init__(
        self,
        *,
        mode: "JobBookmarksEncryptionMode",
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''(experimental) Job bookmarks encryption configuration.

        :param mode: (experimental) Encryption mode.
        :param kms_key: (experimental) The KMS key to be used to encrypt the data. Default: A key will be created if one is not provided.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.SecurityConfiguration(self, "MySecurityConfiguration",
                cloud_watch_encryption=glue.CloudWatchEncryption(
                    mode=glue.CloudWatchEncryptionMode.KMS
                ),
                job_bookmarks_encryption=glue.JobBookmarksEncryption(
                    mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
                ),
                s3_encryption=glue.S3Encryption(
                    mode=glue.S3EncryptionMode.KMS
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a555ea81acfe554401802d7d44d70d3e1a6f96890ffbc28283fadb7ea81f9e)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def mode(self) -> "JobBookmarksEncryptionMode":
        '''(experimental) Encryption mode.

        :stability: experimental
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast("JobBookmarksEncryptionMode", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to be used to encrypt the data.

        :default: A key will be created if one is not provided.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobBookmarksEncryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.JobBookmarksEncryptionMode")
class JobBookmarksEncryptionMode(enum.Enum):
    '''(experimental) Encryption mode for Job Bookmarks.

    :see: https://docs.aws.amazon.com/glue/latest/webapi/API_JobBookmarksEncryption.html#Glue-Type-JobBookmarksEncryption-JobBookmarksEncryptionMode
    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.SecurityConfiguration(self, "MySecurityConfiguration",
            cloud_watch_encryption=glue.CloudWatchEncryption(
                mode=glue.CloudWatchEncryptionMode.KMS
            ),
            job_bookmarks_encryption=glue.JobBookmarksEncryption(
                mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
            ),
            s3_encryption=glue.S3Encryption(
                mode=glue.S3EncryptionMode.KMS
            )
        )
    '''

    CLIENT_SIDE_KMS = "CLIENT_SIDE_KMS"
    '''(experimental) Client-side encryption (CSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html
    :stability: experimental
    '''


class JobExecutable(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.JobExecutable",
):
    '''(experimental) The executable properties related to the Glue job's GlueVersion, JobType and code.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.Job(self, "EnableRunQueuing",
            job_name="EtlJobWithRunQueuing",
            executable=glue.JobExecutable.python_etl(
                glue_version=glue.GlueVersion.V4_0,
                python_version=glue.PythonVersion.THREE,
                script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
            ),
            job_run_queuing_enabled=True
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        *,
        glue_version: GlueVersion,
        language: "JobLanguage",
        script: Code,
        type: "JobType",
        class_name: typing.Optional[builtins.str] = None,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        python_version: typing.Optional["PythonVersion"] = None,
        runtime: typing.Optional["Runtime"] = None,
        s3_python_modules: typing.Optional[typing.Sequence[Code]] = None,
    ) -> "JobExecutable":
        '''(experimental) Create a custom JobExecutable.

        :param glue_version: (experimental) Glue version.
        :param language: (experimental) The language of the job (Scala or Python). Equivalent to a job parameter ``--job-language``.
        :param script: (experimental) The script that is executed by a job.
        :param type: (experimental) Specify the type of the job whether it's an Apache Spark ETL or streaming one or if it's a Python shell job.
        :param class_name: (experimental) The Scala class that serves as the entry point for the job. This applies only if your the job langauage is Scala. Equivalent to a job parameter ``--class``. Default: - no scala className specified
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Equivalent to a job parameter ``--extra-files``. Default: - no extra files specified.
        :param extra_jars: (experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Equivalent to a job parameter ``--extra-jars``. Default: - no extra jars specified.
        :param extra_jars_first: (experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath. Equivalent to a job parameter ``--user-jars-first``. Default: - extra jars are not prioritized.
        :param extra_python_files: (experimental) Additional Python files that AWS Glue adds to the Python path before executing your script. Equivalent to a job parameter ``--extra-py-files``. Default: - no extra python files specified.
        :param python_version: (experimental) The Python version to use. Default: - no python version specified
        :param runtime: (experimental) The Runtime to use. Default: - no runtime specified
        :param s3_python_modules: (experimental) Additional Python modules that AWS Glue adds to the Python path before executing your script. Equivalent to a job parameter ``--s3-py-modules``. Default: - no extra python files specified.

        :stability: experimental
        '''
        config = JobExecutableConfig(
            glue_version=glue_version,
            language=language,
            script=script,
            type=type,
            class_name=class_name,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
            extra_python_files=extra_python_files,
            python_version=python_version,
            runtime=runtime,
            s3_python_modules=s3_python_modules,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "of", [config]))

    @jsii.member(jsii_name="pythonEtl")
    @builtins.classmethod
    def python_etl(
        cls,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        runtime: typing.Optional["Runtime"] = None,
    ) -> "JobExecutable":
        '''(experimental) Create Python executable props for Apache Spark ETL job.

        :param glue_version: (experimental) Glue version.
        :param python_version: (experimental) The Python version to use.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param extra_jars: (experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-jars``. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: (experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath. Equivalent to a job parameter ``--user-jars-first``. Default: false - priority is not given to user-provided jars
        :param extra_python_files: (experimental) Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-py-files``. Default: - no extra python files and argument is not set
        :param runtime: (experimental) Runtime. It is required for Ray jobs.

        :stability: experimental
        '''
        props = PythonSparkJobExecutableProps(
            glue_version=glue_version,
            python_version=python_version,
            script=script,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
            extra_python_files=extra_python_files,
            runtime=runtime,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "pythonEtl", [props]))

    @jsii.member(jsii_name="pythonRay")
    @builtins.classmethod
    def python_ray(
        cls,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        runtime: typing.Optional["Runtime"] = None,
        s3_python_modules: typing.Optional[typing.Sequence[Code]] = None,
    ) -> "JobExecutable":
        '''(experimental) Create Python executable props for Ray jobs.

        :param glue_version: (experimental) Glue version.
        :param python_version: (experimental) The Python version to use.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param runtime: (experimental) Runtime. It is required for Ray jobs.
        :param s3_python_modules: (experimental) Additional Python modules that AWS Glue adds to the Python path before executing your script. Equivalent to a job parameter ``--s3-py-modules``. Default: - no extra python files and argument is not set

        :stability: experimental
        '''
        props = PythonRayExecutableProps(
            glue_version=glue_version,
            python_version=python_version,
            script=script,
            extra_files=extra_files,
            runtime=runtime,
            s3_python_modules=s3_python_modules,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "pythonRay", [props]))

    @jsii.member(jsii_name="pythonShell")
    @builtins.classmethod
    def python_shell(
        cls,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        runtime: typing.Optional["Runtime"] = None,
    ) -> "JobExecutable":
        '''(experimental) Create Python executable props for python shell jobs.

        :param glue_version: (experimental) Glue version.
        :param python_version: (experimental) The Python version to use.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param extra_python_files: (experimental) Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-py-files``. Default: - no extra python files and argument is not set
        :param runtime: (experimental) Runtime. It is required for Ray jobs.

        :stability: experimental
        '''
        props = PythonShellExecutableProps(
            glue_version=glue_version,
            python_version=python_version,
            script=script,
            extra_files=extra_files,
            extra_python_files=extra_python_files,
            runtime=runtime,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "pythonShell", [props]))

    @jsii.member(jsii_name="pythonStreaming")
    @builtins.classmethod
    def python_streaming(
        cls,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        runtime: typing.Optional["Runtime"] = None,
    ) -> "JobExecutable":
        '''(experimental) Create Python executable props for Apache Spark Streaming job.

        :param glue_version: (experimental) Glue version.
        :param python_version: (experimental) The Python version to use.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param extra_jars: (experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-jars``. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: (experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath. Equivalent to a job parameter ``--user-jars-first``. Default: false - priority is not given to user-provided jars
        :param extra_python_files: (experimental) Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-py-files``. Default: - no extra python files and argument is not set
        :param runtime: (experimental) Runtime. It is required for Ray jobs.

        :stability: experimental
        '''
        props = PythonSparkJobExecutableProps(
            glue_version=glue_version,
            python_version=python_version,
            script=script,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
            extra_python_files=extra_python_files,
            runtime=runtime,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "pythonStreaming", [props]))

    @jsii.member(jsii_name="scalaEtl")
    @builtins.classmethod
    def scala_etl(
        cls,
        *,
        class_name: builtins.str,
        glue_version: GlueVersion,
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        runtime: typing.Optional["Runtime"] = None,
    ) -> "JobExecutable":
        '''(experimental) Create Scala executable props for Apache Spark ETL job.

        :param class_name: (experimental) The fully qualified Scala class name that serves as the entry point for the job. Equivalent to a job parameter ``--class``.
        :param glue_version: (experimental) Glue version.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param extra_jars: (experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-jars``. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: (experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath. Equivalent to a job parameter ``--user-jars-first``. Default: false - priority is not given to user-provided jars
        :param runtime: (experimental) Runtime. It is required for Ray jobs.

        :stability: experimental
        '''
        props = ScalaJobExecutableProps(
            class_name=class_name,
            glue_version=glue_version,
            script=script,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
            runtime=runtime,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "scalaEtl", [props]))

    @jsii.member(jsii_name="scalaStreaming")
    @builtins.classmethod
    def scala_streaming(
        cls,
        *,
        class_name: builtins.str,
        glue_version: GlueVersion,
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        runtime: typing.Optional["Runtime"] = None,
    ) -> "JobExecutable":
        '''(experimental) Create Scala executable props for Apache Spark Streaming job.

        :param class_name: (experimental) The fully qualified Scala class name that serves as the entry point for the job. Equivalent to a job parameter ``--class``.
        :param glue_version: (experimental) Glue version.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param extra_jars: (experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-jars``. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: (experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath. Equivalent to a job parameter ``--user-jars-first``. Default: false - priority is not given to user-provided jars
        :param runtime: (experimental) Runtime. It is required for Ray jobs.

        :stability: experimental
        '''
        props = ScalaJobExecutableProps(
            class_name=class_name,
            glue_version=glue_version,
            script=script,
            extra_files=extra_files,
            extra_jars=extra_jars,
            extra_jars_first=extra_jars_first,
            runtime=runtime,
        )

        return typing.cast("JobExecutable", jsii.sinvoke(cls, "scalaStreaming", [props]))

    @jsii.member(jsii_name="bind")
    def bind(self) -> "JobExecutableConfig":
        '''(experimental) Called during Job initialization to get JobExecutableConfig.

        :stability: experimental
        '''
        return typing.cast("JobExecutableConfig", jsii.invoke(self, "bind", []))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.JobExecutableConfig",
    jsii_struct_bases=[],
    name_mapping={
        "glue_version": "glueVersion",
        "language": "language",
        "script": "script",
        "type": "type",
        "class_name": "className",
        "extra_files": "extraFiles",
        "extra_jars": "extraJars",
        "extra_jars_first": "extraJarsFirst",
        "extra_python_files": "extraPythonFiles",
        "python_version": "pythonVersion",
        "runtime": "runtime",
        "s3_python_modules": "s3PythonModules",
    },
)
class JobExecutableConfig:
    def __init__(
        self,
        *,
        glue_version: GlueVersion,
        language: "JobLanguage",
        script: Code,
        type: "JobType",
        class_name: typing.Optional[builtins.str] = None,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        python_version: typing.Optional["PythonVersion"] = None,
        runtime: typing.Optional["Runtime"] = None,
        s3_python_modules: typing.Optional[typing.Sequence[Code]] = None,
    ) -> None:
        '''(experimental) Result of binding a ``JobExecutable`` into a ``Job``.

        :param glue_version: (experimental) Glue version.
        :param language: (experimental) The language of the job (Scala or Python). Equivalent to a job parameter ``--job-language``.
        :param script: (experimental) The script that is executed by a job.
        :param type: (experimental) Specify the type of the job whether it's an Apache Spark ETL or streaming one or if it's a Python shell job.
        :param class_name: (experimental) The Scala class that serves as the entry point for the job. This applies only if your the job langauage is Scala. Equivalent to a job parameter ``--class``. Default: - no scala className specified
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Equivalent to a job parameter ``--extra-files``. Default: - no extra files specified.
        :param extra_jars: (experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Equivalent to a job parameter ``--extra-jars``. Default: - no extra jars specified.
        :param extra_jars_first: (experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath. Equivalent to a job parameter ``--user-jars-first``. Default: - extra jars are not prioritized.
        :param extra_python_files: (experimental) Additional Python files that AWS Glue adds to the Python path before executing your script. Equivalent to a job parameter ``--extra-py-files``. Default: - no extra python files specified.
        :param python_version: (experimental) The Python version to use. Default: - no python version specified
        :param runtime: (experimental) The Runtime to use. Default: - no runtime specified
        :param s3_python_modules: (experimental) Additional Python modules that AWS Glue adds to the Python path before executing your script. Equivalent to a job parameter ``--s3-py-modules``. Default: - no extra python files specified.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            
            # code: glue_alpha.Code
            # glue_version: glue_alpha.GlueVersion
            # job_type: glue_alpha.JobType
            # runtime: glue_alpha.Runtime
            
            job_executable_config = glue_alpha.JobExecutableConfig(
                glue_version=glue_version,
                language=glue_alpha.JobLanguage.SCALA,
                script=code,
                type=job_type,
            
                # the properties below are optional
                class_name="className",
                extra_files=[code],
                extra_jars=[code],
                extra_jars_first=False,
                extra_python_files=[code],
                python_version=glue_alpha.PythonVersion.TWO,
                runtime=runtime,
                s3_python_modules=[code]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__629e6b8d2f364b0c0cfaa00ca6e06725f3d280ad7a2366cf5df8f63e472fea40)
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument extra_jars", value=extra_jars, expected_type=type_hints["extra_jars"])
            check_type(argname="argument extra_jars_first", value=extra_jars_first, expected_type=type_hints["extra_jars_first"])
            check_type(argname="argument extra_python_files", value=extra_python_files, expected_type=type_hints["extra_python_files"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument s3_python_modules", value=s3_python_modules, expected_type=type_hints["s3_python_modules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "glue_version": glue_version,
            "language": language,
            "script": script,
            "type": type,
        }
        if class_name is not None:
            self._values["class_name"] = class_name
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if extra_jars is not None:
            self._values["extra_jars"] = extra_jars
        if extra_jars_first is not None:
            self._values["extra_jars_first"] = extra_jars_first
        if extra_python_files is not None:
            self._values["extra_python_files"] = extra_python_files
        if python_version is not None:
            self._values["python_version"] = python_version
        if runtime is not None:
            self._values["runtime"] = runtime
        if s3_python_modules is not None:
            self._values["s3_python_modules"] = s3_python_modules

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''(experimental) Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        :stability: experimental
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def language(self) -> "JobLanguage":
        '''(experimental) The language of the job (Scala or Python).

        Equivalent to a job parameter ``--job-language``.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("language")
        assert result is not None, "Required property 'language' is missing"
        return typing.cast("JobLanguage", result)

    @builtins.property
    def script(self) -> Code:
        '''(experimental) The script that is executed by a job.

        :stability: experimental
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def type(self) -> "JobType":
        '''(experimental) Specify the type of the job whether it's an Apache Spark ETL or streaming one or if it's a Python shell job.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("JobType", result)

    @builtins.property
    def class_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Scala class that serves as the entry point for the job.

        This applies only if your the job langauage is Scala.
        Equivalent to a job parameter ``--class``.

        :default: - no scala className specified

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("class_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        Equivalent to a job parameter ``--extra-files``.

        :default: - no extra files specified.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Equivalent to a job parameter ``--extra-jars``.

        :default: - no extra jars specified.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_jars")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars_first(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath.

        Equivalent to a job parameter ``--user-jars-first``.

        :default: - extra jars are not prioritized.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_jars_first")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_python_files(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional Python files that AWS Glue adds to the Python path before executing your script.

        Equivalent to a job parameter ``--extra-py-files``.

        :default: - no extra python files specified.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_python_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def python_version(self) -> typing.Optional["PythonVersion"]:
        '''(experimental) The Python version to use.

        :default: - no python version specified

        :stability: experimental
        '''
        result = self._values.get("python_version")
        return typing.cast(typing.Optional["PythonVersion"], result)

    @builtins.property
    def runtime(self) -> typing.Optional["Runtime"]:
        '''(experimental) The Runtime to use.

        :default: - no runtime specified

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional["Runtime"], result)

    @builtins.property
    def s3_python_modules(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional Python modules that AWS Glue adds to the Python path before executing your script.

        Equivalent to a job parameter ``--s3-py-modules``.

        :default: - no extra python files specified.

        :see: https://docs.aws.amazon.com/glue/latest/dg/author-job-ray-job-parameters.html
        :stability: experimental
        '''
        result = self._values.get("s3_python_modules")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobExecutableConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.JobLanguage")
class JobLanguage(enum.Enum):
    '''(experimental) Runtime language of the Glue job.

    :stability: experimental
    '''

    SCALA = "SCALA"
    '''(experimental) Scala.

    :stability: experimental
    '''
    PYTHON = "PYTHON"
    '''(experimental) Python.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.JobProps",
    jsii_struct_bases=[],
    name_mapping={
        "executable": "executable",
        "connections": "connections",
        "continuous_logging": "continuousLogging",
        "default_arguments": "defaultArguments",
        "description": "description",
        "enable_profiling_metrics": "enableProfilingMetrics",
        "execution_class": "executionClass",
        "job_name": "jobName",
        "job_run_queuing_enabled": "jobRunQueuingEnabled",
        "max_capacity": "maxCapacity",
        "max_concurrent_runs": "maxConcurrentRuns",
        "max_retries": "maxRetries",
        "notify_delay_after": "notifyDelayAfter",
        "role": "role",
        "security_configuration": "securityConfiguration",
        "spark_ui": "sparkUI",
        "tags": "tags",
        "timeout": "timeout",
        "worker_count": "workerCount",
        "worker_type": "workerType",
    },
)
class JobProps:
    def __init__(
        self,
        *,
        executable: JobExecutable,
        connections: typing.Optional[typing.Sequence[IConnection]] = None,
        continuous_logging: typing.Optional[typing.Union[ContinuousLoggingProps, typing.Dict[builtins.str, typing.Any]]] = None,
        default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_profiling_metrics: typing.Optional[builtins.bool] = None,
        execution_class: typing.Optional[ExecutionClass] = None,
        job_name: typing.Optional[builtins.str] = None,
        job_run_queuing_enabled: typing.Optional[builtins.bool] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_concurrent_runs: typing.Optional[jsii.Number] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        notify_delay_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_configuration: typing.Optional[ISecurityConfiguration] = None,
        spark_ui: typing.Optional[typing.Union["SparkUIProps", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        worker_count: typing.Optional[jsii.Number] = None,
        worker_type: typing.Optional["WorkerType"] = None,
    ) -> None:
        '''(experimental) Construction properties for ``Job``.

        :param executable: (experimental) The job's executable properties.
        :param connections: (experimental) The ``Connection``s used for this job. Connections are used to connect to other AWS Service or resources within a VPC. Default: [] - no connections are added to the job
        :param continuous_logging: (experimental) Enables continuous logging with the specified props. Default: - continuous logging is disabled.
        :param default_arguments: (experimental) The default arguments for this job, specified as name-value pairs. Default: - no arguments
        :param description: (experimental) The description of the job. Default: - no value
        :param enable_profiling_metrics: (experimental) Enables the collection of metrics for job profiling. Equivalent to a job parameter ``--enable-metrics``. Default: - no profiling metrics emitted.
        :param execution_class: (experimental) The ExecutionClass whether the job is run with a standard or flexible execution class. Default: - STANDARD
        :param job_name: (experimental) The name of the job. Default: - a name is automatically generated
        :param job_run_queuing_enabled: (experimental) Specifies whether job run queuing is enabled for the job runs for this job. A value of true means job run queuing is enabled for the job runs. If false or not populated, the job runs will not be considered for queueing. If this field does not match the value set in the job run, then the value from the job run field will be used. Default: - no job run queuing
        :param max_capacity: (experimental) The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs. Cannot be used for Glue version 2.0 and later - workerType and workerCount should be used instead. Default: - 10 when job type is Apache Spark ETL or streaming, 0.0625 when job type is Python shell
        :param max_concurrent_runs: (experimental) The maximum number of concurrent runs allowed for the job. An error is returned when this threshold is reached. The maximum value you can specify is controlled by a service limit. Default: 1
        :param max_retries: (experimental) The maximum number of times to retry this job after a job run fails. Default: 0
        :param notify_delay_after: (experimental) The number of minutes to wait after a job run starts, before sending a job run delay notification. Default: - no delay notifications
        :param role: (experimental) The IAM role assumed by Glue to run this job. If providing a custom role, it needs to trust the Glue service principal (glue.amazonaws.com) and be granted sufficient permissions. Default: - a role is automatically generated
        :param security_configuration: (experimental) The ``SecurityConfiguration`` to use for this job. Default: - no security configuration.
        :param spark_ui: (experimental) Enables the Spark UI debugging and monitoring with the specified props. Default: - Spark UI debugging and monitoring is disabled.
        :param tags: (experimental) The tags to add to the resources on which the job runs. Default: {} - no tags
        :param timeout: (experimental) The maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status. Default: cdk.Duration.hours(48)
        :param worker_count: (experimental) The number of workers of a defined ``WorkerType`` that are allocated when a job runs. Default: - differs based on specific Glue version/worker type
        :param worker_type: (experimental) The type of predefined worker that is allocated when a job runs. Default: - differs based on specific Glue version

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.Job(self, "EnableRunQueuing",
                job_name="EtlJobWithRunQueuing",
                executable=glue.JobExecutable.python_etl(
                    glue_version=glue.GlueVersion.V4_0,
                    python_version=glue.PythonVersion.THREE,
                    script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
                ),
                job_run_queuing_enabled=True
            )
        '''
        if isinstance(continuous_logging, dict):
            continuous_logging = ContinuousLoggingProps(**continuous_logging)
        if isinstance(spark_ui, dict):
            spark_ui = SparkUIProps(**spark_ui)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f47dc7b3a9514a79f7f82e52c4441b82161dce2eb5b67f22211660776beaa70)
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument connections", value=connections, expected_type=type_hints["connections"])
            check_type(argname="argument continuous_logging", value=continuous_logging, expected_type=type_hints["continuous_logging"])
            check_type(argname="argument default_arguments", value=default_arguments, expected_type=type_hints["default_arguments"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_profiling_metrics", value=enable_profiling_metrics, expected_type=type_hints["enable_profiling_metrics"])
            check_type(argname="argument execution_class", value=execution_class, expected_type=type_hints["execution_class"])
            check_type(argname="argument job_name", value=job_name, expected_type=type_hints["job_name"])
            check_type(argname="argument job_run_queuing_enabled", value=job_run_queuing_enabled, expected_type=type_hints["job_run_queuing_enabled"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument max_concurrent_runs", value=max_concurrent_runs, expected_type=type_hints["max_concurrent_runs"])
            check_type(argname="argument max_retries", value=max_retries, expected_type=type_hints["max_retries"])
            check_type(argname="argument notify_delay_after", value=notify_delay_after, expected_type=type_hints["notify_delay_after"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_configuration", value=security_configuration, expected_type=type_hints["security_configuration"])
            check_type(argname="argument spark_ui", value=spark_ui, expected_type=type_hints["spark_ui"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "executable": executable,
        }
        if connections is not None:
            self._values["connections"] = connections
        if continuous_logging is not None:
            self._values["continuous_logging"] = continuous_logging
        if default_arguments is not None:
            self._values["default_arguments"] = default_arguments
        if description is not None:
            self._values["description"] = description
        if enable_profiling_metrics is not None:
            self._values["enable_profiling_metrics"] = enable_profiling_metrics
        if execution_class is not None:
            self._values["execution_class"] = execution_class
        if job_name is not None:
            self._values["job_name"] = job_name
        if job_run_queuing_enabled is not None:
            self._values["job_run_queuing_enabled"] = job_run_queuing_enabled
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_concurrent_runs is not None:
            self._values["max_concurrent_runs"] = max_concurrent_runs
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if notify_delay_after is not None:
            self._values["notify_delay_after"] = notify_delay_after
        if role is not None:
            self._values["role"] = role
        if security_configuration is not None:
            self._values["security_configuration"] = security_configuration
        if spark_ui is not None:
            self._values["spark_ui"] = spark_ui
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout
        if worker_count is not None:
            self._values["worker_count"] = worker_count
        if worker_type is not None:
            self._values["worker_type"] = worker_type

    @builtins.property
    def executable(self) -> JobExecutable:
        '''(experimental) The job's executable properties.

        :stability: experimental
        '''
        result = self._values.get("executable")
        assert result is not None, "Required property 'executable' is missing"
        return typing.cast(JobExecutable, result)

    @builtins.property
    def connections(self) -> typing.Optional[typing.List[IConnection]]:
        '''(experimental) The ``Connection``s used for this job.

        Connections are used to connect to other AWS Service or resources within a VPC.

        :default: [] - no connections are added to the job

        :stability: experimental
        '''
        result = self._values.get("connections")
        return typing.cast(typing.Optional[typing.List[IConnection]], result)

    @builtins.property
    def continuous_logging(self) -> typing.Optional[ContinuousLoggingProps]:
        '''(experimental) Enables continuous logging with the specified props.

        :default: - continuous logging is disabled.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("continuous_logging")
        return typing.cast(typing.Optional[ContinuousLoggingProps], result)

    @builtins.property
    def default_arguments(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The default arguments for this job, specified as name-value pairs.

        :default: - no arguments

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("default_arguments")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description of the job.

        :default: - no value

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_profiling_metrics(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables the collection of metrics for job profiling.

        Equivalent to a job parameter ``--enable-metrics``.

        :default: - no profiling metrics emitted.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("enable_profiling_metrics")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def execution_class(self) -> typing.Optional[ExecutionClass]:
        '''(experimental) The ExecutionClass whether the job is run with a standard or flexible execution class.

        :default: - STANDARD

        :see: https://docs.aws.amazon.com/glue/latest/dg/add-job.html
        :stability: experimental
        '''
        result = self._values.get("execution_class")
        return typing.cast(typing.Optional[ExecutionClass], result)

    @builtins.property
    def job_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the job.

        :default: - a name is automatically generated

        :stability: experimental
        '''
        result = self._values.get("job_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_run_queuing_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether job run queuing is enabled for the job runs for this job.

        A value of true means job run queuing is enabled for the job runs.
        If false or not populated, the job runs will not be considered for queueing.
        If this field does not match the value set in the job run, then the value from the job run field will be used.

        :default: - no job run queuing

        :stability: experimental
        '''
        result = self._values.get("job_run_queuing_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of AWS Glue data processing units (DPUs) that can be allocated when this job runs.

        Cannot be used for Glue version 2.0 and later - workerType and workerCount should be used instead.

        :default: - 10 when job type is Apache Spark ETL or streaming, 0.0625 when job type is Python shell

        :stability: experimental
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_concurrent_runs(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of concurrent runs allowed for the job.

        An error is returned when this threshold is reached. The maximum value you can specify is controlled by a service limit.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("max_concurrent_runs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry this job after a job run fails.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("max_retries")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def notify_delay_after(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The number of minutes to wait after a job run starts, before sending a job run delay notification.

        :default: - no delay notifications

        :stability: experimental
        '''
        result = self._values.get("notify_delay_after")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role assumed by Glue to run this job.

        If providing a custom role, it needs to trust the Glue service principal (glue.amazonaws.com) and be granted sufficient permissions.

        :default: - a role is automatically generated

        :see: https://docs.aws.amazon.com/glue/latest/dg/getting-started-access.html
        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_configuration(self) -> typing.Optional[ISecurityConfiguration]:
        '''(experimental) The ``SecurityConfiguration`` to use for this job.

        :default: - no security configuration.

        :stability: experimental
        '''
        result = self._values.get("security_configuration")
        return typing.cast(typing.Optional[ISecurityConfiguration], result)

    @builtins.property
    def spark_ui(self) -> typing.Optional["SparkUIProps"]:
        '''(experimental) Enables the Spark UI debugging and monitoring with the specified props.

        :default: - Spark UI debugging and monitoring is disabled.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("spark_ui")
        return typing.cast(typing.Optional["SparkUIProps"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The tags to add to the resources on which the job runs.

        :default: {} - no tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The maximum time that a job run can consume resources before it is terminated and enters TIMEOUT status.

        :default: cdk.Duration.hours(48)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def worker_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of workers of a defined ``WorkerType`` that are allocated when a job runs.

        :default: - differs based on specific Glue version/worker type

        :stability: experimental
        '''
        result = self._values.get("worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def worker_type(self) -> typing.Optional["WorkerType"]:
        '''(experimental) The type of predefined worker that is allocated when a job runs.

        :default: - differs based on specific Glue version

        :stability: experimental
        '''
        result = self._values.get("worker_type")
        return typing.cast(typing.Optional["WorkerType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.JobState")
class JobState(enum.Enum):
    '''(experimental) Job states emitted by Glue to CloudWatch Events.

    :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/EventTypes.html#glue-event-types
    :stability: experimental
    '''

    SUCCEEDED = "SUCCEEDED"
    '''(experimental) State indicating job run succeeded.

    :stability: experimental
    '''
    FAILED = "FAILED"
    '''(experimental) State indicating job run failed.

    :stability: experimental
    '''
    TIMEOUT = "TIMEOUT"
    '''(experimental) State indicating job run timed out.

    :stability: experimental
    '''
    STARTING = "STARTING"
    '''(experimental) State indicating job is starting.

    :stability: experimental
    '''
    RUNNING = "RUNNING"
    '''(experimental) State indicating job is running.

    :stability: experimental
    '''
    STOPPING = "STOPPING"
    '''(experimental) State indicating job is stopping.

    :stability: experimental
    '''
    STOPPED = "STOPPED"
    '''(experimental) State indicating job stopped.

    :stability: experimental
    '''


class JobType(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue-alpha.JobType"):
    '''(experimental) The job type.

    If you need to use a JobType that doesn't exist as a static member, you
    can instantiate a ``JobType`` object, e.g: ``JobType.of('other name')``.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_glue_alpha as glue_alpha
        
        job_type = glue_alpha.JobType.ETL
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, name: builtins.str) -> "JobType":
        '''(experimental) Custom type name.

        :param name: type name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0683afe40f10e5c8c02ac80ffb25aca1e5830884e6b5e539accb9e36df90257d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast("JobType", jsii.sinvoke(cls, "of", [name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ETL")
    def ETL(cls) -> "JobType":
        '''(experimental) Command for running a Glue Spark job.

        :stability: experimental
        '''
        return typing.cast("JobType", jsii.sget(cls, "ETL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_SHELL")
    def PYTHON_SHELL(cls) -> "JobType":
        '''(experimental) Command for running a Glue python shell job.

        :stability: experimental
        '''
        return typing.cast("JobType", jsii.sget(cls, "PYTHON_SHELL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RAY")
    def RAY(cls) -> "JobType":
        '''(experimental) Command for running a Glue Ray job.

        :stability: experimental
        '''
        return typing.cast("JobType", jsii.sget(cls, "RAY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STREAMING")
    def STREAMING(cls) -> "JobType":
        '''(experimental) Command for running a Glue Spark streaming job.

        :stability: experimental
        '''
        return typing.cast("JobType", jsii.sget(cls, "STREAMING"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this JobType, as expected by Job resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.MetricType")
class MetricType(enum.Enum):
    '''(experimental) The Glue CloudWatch metric type.

    :see: https://docs.aws.amazon.com/glue/latest/dg/monitoring-awsglue-with-cloudwatch-metrics.html
    :stability: experimental
    '''

    GAUGE = "GAUGE"
    '''(experimental) A value at a point in time.

    :stability: experimental
    '''
    COUNT = "COUNT"
    '''(experimental) An aggregate number.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.NumericOverflowHandlingAction")
class NumericOverflowHandlingAction(enum.Enum):
    '''(experimental) Specifies the action to perform when ORC data contains an integer (for example, BIGINT or int64) that is larger than the column definition (for example, SMALLINT or int16).

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"* > *"numeric_overflow_handling"*
    :stability: experimental
    '''

    DISABLED = "DISABLED"
    '''(experimental) Invalid character handling is turned off.

    :stability: experimental
    '''
    FAIL = "FAIL"
    '''(experimental) Cancel the query when the data includes invalid characters.

    :stability: experimental
    '''
    SET_TO_NULL = "SET_TO_NULL"
    '''(experimental) Set invalid characters to null.

    :stability: experimental
    '''
    DROP_ROW = "DROP_ROW"
    '''(experimental) Set each value in the row to null.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.OrcColumnMappingType")
class OrcColumnMappingType(enum.Enum):
    '''(experimental) Specifies how to map columns when the table uses ORC data format.

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"* > *"orc.schema.resolution"*
    :stability: experimental
    '''

    NAME = "NAME"
    '''(experimental) Map columns by name.

    :stability: experimental
    '''
    POSITION = "POSITION"
    '''(experimental) Map columns by position.

    :stability: experimental
    '''


class OutputFormat(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.OutputFormat",
):
    '''(experimental) Absolute class name of the Hadoop ``OutputFormat`` to use when writing table files.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_glue_alpha as glue_alpha
        
        output_format = glue_alpha.OutputFormat("className")
    '''

    def __init__(self, class_name: builtins.str) -> None:
        '''
        :param class_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8952681a040fc7931f48438a2e01cd3c2bed40202b6f32cd606344a5ea10e810)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
        jsii.create(self.__class__, self, [class_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> InputFormat:
        '''(experimental) OutputFormat for Avro files.

        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/avro/AvroContainerOutputFormat.html
        :stability: experimental
        '''
        return typing.cast(InputFormat, jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIVE_IGNORE_KEY_TEXT")
    def HIVE_IGNORE_KEY_TEXT(cls) -> "OutputFormat":
        '''(experimental) Writes text data with a null key (value only).

        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/HiveIgnoreKeyTextOutputFormat.html
        :stability: experimental
        '''
        return typing.cast("OutputFormat", jsii.sget(cls, "HIVE_IGNORE_KEY_TEXT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> InputFormat:
        '''(experimental) OutputFormat for Orc files.

        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/orc/OrcOutputFormat.html
        :stability: experimental
        '''
        return typing.cast(InputFormat, jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "OutputFormat":
        '''(experimental) OutputFormat for Parquet files.

        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/parquet/MapredParquetOutputFormat.html
        :stability: experimental
        '''
        return typing.cast("OutputFormat", jsii.sget(cls, "PARQUET"))

    @builtins.property
    @jsii.member(jsii_name="className")
    def class_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "className"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.PartitionIndex",
    jsii_struct_bases=[],
    name_mapping={"key_names": "keyNames", "index_name": "indexName"},
)
class PartitionIndex:
    def __init__(
        self,
        *,
        key_names: typing.Sequence[builtins.str],
        index_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties of a Partition Index.

        :param key_names: (experimental) The partition key names that comprise the partition index. The names must correspond to a name in the table's partition keys.
        :param index_name: (experimental) The name of the partition index. Default: - a name will be generated for you.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_table: glue.Table
            
            my_table.add_partition_index(
                index_name="my-index",
                key_names=["year"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854153aaeace5af7af75594677e850d114f911156b5cd93d50a01feeff4a76a8)
            check_type(argname="argument key_names", value=key_names, expected_type=type_hints["key_names"])
            check_type(argname="argument index_name", value=index_name, expected_type=type_hints["index_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key_names": key_names,
        }
        if index_name is not None:
            self._values["index_name"] = index_name

    @builtins.property
    def key_names(self) -> typing.List[builtins.str]:
        '''(experimental) The partition key names that comprise the partition index.

        The names must correspond to a name in the
        table's partition keys.

        :stability: experimental
        '''
        result = self._values.get("key_names")
        assert result is not None, "Required property 'key_names' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def index_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the partition index.

        :default: - a name will be generated for you.

        :stability: experimental
        '''
        result = self._values.get("index_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PartitionIndex(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.PythonRayExecutableProps",
    jsii_struct_bases=[],
    name_mapping={
        "glue_version": "glueVersion",
        "python_version": "pythonVersion",
        "script": "script",
        "extra_files": "extraFiles",
        "runtime": "runtime",
        "s3_python_modules": "s3PythonModules",
    },
)
class PythonRayExecutableProps:
    def __init__(
        self,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        runtime: typing.Optional["Runtime"] = None,
        s3_python_modules: typing.Optional[typing.Sequence[Code]] = None,
    ) -> None:
        '''(experimental) Props for creating a Python Ray job executable.

        :param glue_version: (experimental) Glue version.
        :param python_version: (experimental) The Python version to use.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param runtime: (experimental) Runtime. It is required for Ray jobs.
        :param s3_python_modules: (experimental) Additional Python modules that AWS Glue adds to the Python path before executing your script. Equivalent to a job parameter ``--s3-py-modules``. Default: - no extra python files and argument is not set

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.Job(self, "RayJob",
                executable=glue.JobExecutable.python_ray(
                    glue_version=glue.GlueVersion.V4_0,
                    python_version=glue.PythonVersion.THREE_NINE,
                    runtime=glue.Runtime.RAY_TWO_FOUR,
                    script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
                ),
                worker_type=glue.WorkerType.Z_2X,
                worker_count=2,
                description="an example Ray job"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96728d115db88df2280e8997d67958a9b8d05214b04966c306fbf00f84a6324f)
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument s3_python_modules", value=s3_python_modules, expected_type=type_hints["s3_python_modules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "glue_version": glue_version,
            "python_version": python_version,
            "script": script,
        }
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if runtime is not None:
            self._values["runtime"] = runtime
        if s3_python_modules is not None:
            self._values["s3_python_modules"] = s3_python_modules

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''(experimental) Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        :stability: experimental
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def python_version(self) -> "PythonVersion":
        '''(experimental) The Python version to use.

        :stability: experimental
        '''
        result = self._values.get("python_version")
        assert result is not None, "Required property 'python_version' is missing"
        return typing.cast("PythonVersion", result)

    @builtins.property
    def script(self) -> Code:
        '''(experimental) The script that executes a job.

        :stability: experimental
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        Only individual files are supported, directories are not supported.
        Equivalent to a job parameter ``--extra-files``.

        :default: [] - no extra files are copied to the working directory

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def runtime(self) -> typing.Optional["Runtime"]:
        '''(experimental) Runtime.

        It is required for Ray jobs.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional["Runtime"], result)

    @builtins.property
    def s3_python_modules(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional Python modules that AWS Glue adds to the Python path before executing your script.

        Equivalent to a job parameter ``--s3-py-modules``.

        :default: - no extra python files and argument is not set

        :see: https://docs.aws.amazon.com/glue/latest/dg/author-job-ray-job-parameters.html
        :stability: experimental
        '''
        result = self._values.get("s3_python_modules")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonRayExecutableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.PythonShellExecutableProps",
    jsii_struct_bases=[],
    name_mapping={
        "glue_version": "glueVersion",
        "python_version": "pythonVersion",
        "script": "script",
        "extra_files": "extraFiles",
        "extra_python_files": "extraPythonFiles",
        "runtime": "runtime",
    },
)
class PythonShellExecutableProps:
    def __init__(
        self,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        runtime: typing.Optional["Runtime"] = None,
    ) -> None:
        '''(experimental) Props for creating a Python shell job executable.

        :param glue_version: (experimental) Glue version.
        :param python_version: (experimental) The Python version to use.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param extra_python_files: (experimental) Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-py-files``. Default: - no extra python files and argument is not set
        :param runtime: (experimental) Runtime. It is required for Ray jobs.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # bucket: s3.Bucket
            
            glue.Job(self, "PythonShellJob",
                executable=glue.JobExecutable.python_shell(
                    glue_version=glue.GlueVersion.V1_0,
                    python_version=glue.PythonVersion.THREE,
                    script=glue.Code.from_bucket(bucket, "script.py")
                ),
                description="an example Python Shell job"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787eb0d11407cb3ae6ba15f28cff4370dd45126f9ce4e2ab093edba7a3b628e8)
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument extra_python_files", value=extra_python_files, expected_type=type_hints["extra_python_files"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "glue_version": glue_version,
            "python_version": python_version,
            "script": script,
        }
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if extra_python_files is not None:
            self._values["extra_python_files"] = extra_python_files
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''(experimental) Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        :stability: experimental
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def python_version(self) -> "PythonVersion":
        '''(experimental) The Python version to use.

        :stability: experimental
        '''
        result = self._values.get("python_version")
        assert result is not None, "Required property 'python_version' is missing"
        return typing.cast("PythonVersion", result)

    @builtins.property
    def script(self) -> Code:
        '''(experimental) The script that executes a job.

        :stability: experimental
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        Only individual files are supported, directories are not supported.
        Equivalent to a job parameter ``--extra-files``.

        :default: [] - no extra files are copied to the working directory

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_python_files(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional Python files that AWS Glue adds to the Python path before executing your script.

        Only individual files are supported, directories are not supported.
        Equivalent to a job parameter ``--extra-py-files``.

        :default: - no extra python files and argument is not set

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_python_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def runtime(self) -> typing.Optional["Runtime"]:
        '''(experimental) Runtime.

        It is required for Ray jobs.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional["Runtime"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonShellExecutableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.PythonSparkJobExecutableProps",
    jsii_struct_bases=[],
    name_mapping={
        "glue_version": "glueVersion",
        "python_version": "pythonVersion",
        "script": "script",
        "extra_files": "extraFiles",
        "extra_jars": "extraJars",
        "extra_jars_first": "extraJarsFirst",
        "extra_python_files": "extraPythonFiles",
        "runtime": "runtime",
    },
)
class PythonSparkJobExecutableProps:
    def __init__(
        self,
        *,
        glue_version: GlueVersion,
        python_version: "PythonVersion",
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
        runtime: typing.Optional["Runtime"] = None,
    ) -> None:
        '''(experimental) Props for creating a Python Spark (ETL or Streaming) job executable.

        :param glue_version: (experimental) Glue version.
        :param python_version: (experimental) The Python version to use.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param extra_jars: (experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-jars``. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: (experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath. Equivalent to a job parameter ``--user-jars-first``. Default: false - priority is not given to user-provided jars
        :param extra_python_files: (experimental) Additional Python files that AWS Glue adds to the Python path before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-py-files``. Default: - no extra python files and argument is not set
        :param runtime: (experimental) Runtime. It is required for Ray jobs.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.Job(self, "EnableRunQueuing",
                job_name="EtlJobWithRunQueuing",
                executable=glue.JobExecutable.python_etl(
                    glue_version=glue.GlueVersion.V4_0,
                    python_version=glue.PythonVersion.THREE,
                    script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
                ),
                job_run_queuing_enabled=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0bf4f1c4314f36fa21cf1fde861d972bb36e11678ce6f78e9dab93055f9ed4)
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument extra_jars", value=extra_jars, expected_type=type_hints["extra_jars"])
            check_type(argname="argument extra_jars_first", value=extra_jars_first, expected_type=type_hints["extra_jars_first"])
            check_type(argname="argument extra_python_files", value=extra_python_files, expected_type=type_hints["extra_python_files"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "glue_version": glue_version,
            "python_version": python_version,
            "script": script,
        }
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if extra_jars is not None:
            self._values["extra_jars"] = extra_jars
        if extra_jars_first is not None:
            self._values["extra_jars_first"] = extra_jars_first
        if extra_python_files is not None:
            self._values["extra_python_files"] = extra_python_files
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''(experimental) Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        :stability: experimental
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def python_version(self) -> "PythonVersion":
        '''(experimental) The Python version to use.

        :stability: experimental
        '''
        result = self._values.get("python_version")
        assert result is not None, "Required property 'python_version' is missing"
        return typing.cast("PythonVersion", result)

    @builtins.property
    def script(self) -> Code:
        '''(experimental) The script that executes a job.

        :stability: experimental
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        Only individual files are supported, directories are not supported.
        Equivalent to a job parameter ``--extra-files``.

        :default: [] - no extra files are copied to the working directory

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-jars``.

        :default: [] - no extra jars are added to the classpath

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_jars")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars_first(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath.

        Equivalent to a job parameter ``--user-jars-first``.

        :default: false - priority is not given to user-provided jars

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_jars_first")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def extra_python_files(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional Python files that AWS Glue adds to the Python path before executing your script.

        Only individual files are supported, directories are not supported.
        Equivalent to a job parameter ``--extra-py-files``.

        :default: - no extra python files and argument is not set

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_python_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def runtime(self) -> typing.Optional["Runtime"]:
        '''(experimental) Runtime.

        It is required for Ray jobs.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional["Runtime"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonSparkJobExecutableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.PythonVersion")
class PythonVersion(enum.Enum):
    '''(experimental) Python version.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.Job(self, "EnableRunQueuing",
            job_name="EtlJobWithRunQueuing",
            executable=glue.JobExecutable.python_etl(
                glue_version=glue.GlueVersion.V4_0,
                python_version=glue.PythonVersion.THREE,
                script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
            ),
            job_run_queuing_enabled=True
        )
    '''

    TWO = "TWO"
    '''(experimental) Python 2 (the exact version depends on GlueVersion and JobCommand used).

    :stability: experimental
    '''
    THREE = "THREE"
    '''(experimental) Python 3 (the exact version depends on GlueVersion and JobCommand used).

    :stability: experimental
    '''
    THREE_NINE = "THREE_NINE"
    '''(experimental) Python 3.9 (the exact version depends on GlueVersion and JobCommand used).

    :stability: experimental
    '''


class Runtime(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue-alpha.Runtime"):
    '''(experimental) AWS Glue runtime determines the runtime engine of the job.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.Job(self, "RayJob",
            executable=glue.JobExecutable.python_ray(
                glue_version=glue.GlueVersion.V4_0,
                python_version=glue.PythonVersion.THREE_NINE,
                runtime=glue.Runtime.RAY_TWO_FOUR,
                script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
            ),
            worker_type=glue.WorkerType.Z_2X,
            worker_count=2,
            description="an example Ray job"
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, runtime: builtins.str) -> "Runtime":
        '''(experimental) Custom runtime.

        :param runtime: custom runtime.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77ef351ef4776813c6253cf1f604175f461d8b9f9a8806473279f7e71a53adfe)
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        return typing.cast("Runtime", jsii.sinvoke(cls, "of", [runtime]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="RAY_TWO_FOUR")
    def RAY_TWO_FOUR(cls) -> "Runtime":
        '''(experimental) Runtime for a Glue for Ray 2.4.

        :stability: experimental
        '''
        return typing.cast("Runtime", jsii.sget(cls, "RAY_TWO_FOUR"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this Runtime.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


class S3Code(Code, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue-alpha.S3Code"):
    '''(experimental) Glue job Code from an S3 bucket.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_glue_alpha as glue_alpha
        from aws_cdk import aws_s3 as s3
        
        # bucket: s3.Bucket
        
        s3_code = glue_alpha.S3Code(bucket, "key")
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        key: builtins.str,
    ) -> None:
        '''
        :param bucket: -
        :param key: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7854e17fe796bdc5dc10fe3c8febb691186728550ca107493a43fc6979cafee)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        jsii.create(self.__class__, self, [bucket, key])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.Construct,
        grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> CodeConfig:
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param _scope: -
        :param grantable: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18fa6b6bc6e19007515f753b3e849efd4b7a16720ea785b0e155f20075d71602)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
            check_type(argname="argument grantable", value=grantable, expected_type=type_hints["grantable"])
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [_scope, grantable]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.S3Encryption",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "kms_key": "kmsKey"},
)
class S3Encryption:
    def __init__(
        self,
        *,
        mode: "S3EncryptionMode",
        kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    ) -> None:
        '''(experimental) S3 encryption configuration.

        :param mode: (experimental) Encryption mode.
        :param kms_key: (experimental) The KMS key to be used to encrypt the data. Default: no kms key if mode = S3_MANAGED. A key will be created if one is not provided and mode = KMS.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.SecurityConfiguration(self, "MySecurityConfiguration",
                cloud_watch_encryption=glue.CloudWatchEncryption(
                    mode=glue.CloudWatchEncryptionMode.KMS
                ),
                job_bookmarks_encryption=glue.JobBookmarksEncryption(
                    mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
                ),
                s3_encryption=glue.S3Encryption(
                    mode=glue.S3EncryptionMode.KMS
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d972222b3b5c087e70a7ab859853e97f1579eeee2ede763d551c41d4076f740e)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument kms_key", value=kms_key, expected_type=type_hints["kms_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if kms_key is not None:
            self._values["kms_key"] = kms_key

    @builtins.property
    def mode(self) -> "S3EncryptionMode":
        '''(experimental) Encryption mode.

        :stability: experimental
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast("S3EncryptionMode", result)

    @builtins.property
    def kms_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key to be used to encrypt the data.

        :default: no kms key if mode = S3_MANAGED. A key will be created if one is not provided and mode = KMS.

        :stability: experimental
        '''
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3Encryption(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.S3EncryptionMode")
class S3EncryptionMode(enum.Enum):
    '''(experimental) Encryption mode for S3.

    :see: https://docs.aws.amazon.com/glue/latest/webapi/API_S3Encryption.html#Glue-Type-S3Encryption-S3EncryptionMode
    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.SecurityConfiguration(self, "MySecurityConfiguration",
            cloud_watch_encryption=glue.CloudWatchEncryption(
                mode=glue.CloudWatchEncryptionMode.KMS
            ),
            job_bookmarks_encryption=glue.JobBookmarksEncryption(
                mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
            ),
            s3_encryption=glue.S3Encryption(
                mode=glue.S3EncryptionMode.KMS
            )
        )
    '''

    S3_MANAGED = "S3_MANAGED"
    '''(experimental) Server side encryption (SSE) with an Amazon S3-managed key.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html
    :stability: experimental
    '''
    KMS = "KMS"
    '''(experimental) Server-side encryption (SSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.ScalaJobExecutableProps",
    jsii_struct_bases=[],
    name_mapping={
        "class_name": "className",
        "glue_version": "glueVersion",
        "script": "script",
        "extra_files": "extraFiles",
        "extra_jars": "extraJars",
        "extra_jars_first": "extraJarsFirst",
        "runtime": "runtime",
    },
)
class ScalaJobExecutableProps:
    def __init__(
        self,
        *,
        class_name: builtins.str,
        glue_version: GlueVersion,
        script: Code,
        extra_files: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars: typing.Optional[typing.Sequence[Code]] = None,
        extra_jars_first: typing.Optional[builtins.bool] = None,
        runtime: typing.Optional[Runtime] = None,
    ) -> None:
        '''(experimental) Props for creating a Scala Spark (ETL or Streaming) job executable.

        :param class_name: (experimental) The fully qualified Scala class name that serves as the entry point for the job. Equivalent to a job parameter ``--class``.
        :param glue_version: (experimental) Glue version.
        :param script: (experimental) The script that executes a job.
        :param extra_files: (experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-files``. Default: [] - no extra files are copied to the working directory
        :param extra_jars: (experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-jars``. Default: [] - no extra jars are added to the classpath
        :param extra_jars_first: (experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath. Equivalent to a job parameter ``--user-jars-first``. Default: false - priority is not given to user-provided jars
        :param runtime: (experimental) Runtime. It is required for Ray jobs.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # bucket: s3.Bucket
            
            glue.Job(self, "ScalaSparkEtlJob",
                executable=glue.JobExecutable.scala_etl(
                    glue_version=glue.GlueVersion.V4_0,
                    script=glue.Code.from_bucket(bucket, "src/com/example/HelloWorld.scala"),
                    class_name="com.example.HelloWorld",
                    extra_jars=[glue.Code.from_bucket(bucket, "jars/HelloWorld.jar")]
                ),
                worker_type=glue.WorkerType.G_8X,
                description="an example Scala ETL job"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8895a1f83a364cc50cc706b326361b090931a87ba5ad2c1f9a0747bf6c0f7e7)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
            check_type(argname="argument glue_version", value=glue_version, expected_type=type_hints["glue_version"])
            check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            check_type(argname="argument extra_files", value=extra_files, expected_type=type_hints["extra_files"])
            check_type(argname="argument extra_jars", value=extra_jars, expected_type=type_hints["extra_jars"])
            check_type(argname="argument extra_jars_first", value=extra_jars_first, expected_type=type_hints["extra_jars_first"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "class_name": class_name,
            "glue_version": glue_version,
            "script": script,
        }
        if extra_files is not None:
            self._values["extra_files"] = extra_files
        if extra_jars is not None:
            self._values["extra_jars"] = extra_jars
        if extra_jars_first is not None:
            self._values["extra_jars_first"] = extra_jars_first
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def class_name(self) -> builtins.str:
        '''(experimental) The fully qualified Scala class name that serves as the entry point for the job.

        Equivalent to a job parameter ``--class``.

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("class_name")
        assert result is not None, "Required property 'class_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def glue_version(self) -> GlueVersion:
        '''(experimental) Glue version.

        :see: https://docs.aws.amazon.com/glue/latest/dg/release-notes.html
        :stability: experimental
        '''
        result = self._values.get("glue_version")
        assert result is not None, "Required property 'glue_version' is missing"
        return typing.cast(GlueVersion, result)

    @builtins.property
    def script(self) -> Code:
        '''(experimental) The script that executes a job.

        :stability: experimental
        '''
        result = self._values.get("script")
        assert result is not None, "Required property 'script' is missing"
        return typing.cast(Code, result)

    @builtins.property
    def extra_files(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional files, such as configuration files that AWS Glue copies to the working directory of your script before executing it.

        Only individual files are supported, directories are not supported.
        Equivalent to a job parameter ``--extra-files``.

        :default: [] - no extra files are copied to the working directory

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_files")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars(self) -> typing.Optional[typing.List[Code]]:
        '''(experimental) Additional Java .jar files that AWS Glue adds to the Java classpath before executing your script. Only individual files are supported, directories are not supported. Equivalent to a job parameter ``--extra-jars``.

        :default: [] - no extra jars are added to the classpath

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_jars")
        return typing.cast(typing.Optional[typing.List[Code]], result)

    @builtins.property
    def extra_jars_first(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Setting this value to true prioritizes the customer's extra JAR files in the classpath.

        Equivalent to a job parameter ``--user-jars-first``.

        :default: false - priority is not given to user-provided jars

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        '''
        result = self._values.get("extra_jars_first")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def runtime(self) -> typing.Optional[Runtime]:
        '''(experimental) Runtime.

        It is required for Ray jobs.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[Runtime], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScalaJobExecutableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Schema(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-glue-alpha.Schema"):
    '''
    :see: https://docs.aws.amazon.com/athena/latest/ug/data-types.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_database: glue.Database
        
        glue.S3Table(self, "MyTable",
            database=my_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            partition_keys=[glue.Column(
                name="year",
                type=glue.Schema.SMALL_INT
            ), glue.Column(
                name="month",
                type=glue.Schema.SMALL_INT
            )],
            data_format=glue.DataFormat.JSON
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="array")
    @builtins.classmethod
    def array(
        cls,
        *,
        input_string: builtins.str,
        is_primitive: builtins.bool,
    ) -> "Type":
        '''(experimental) Creates an array of some other type.

        :param input_string: (experimental) Glue InputString for this type.
        :param is_primitive: (experimental) Indicates whether this type is a primitive data type.

        :stability: experimental
        '''
        item_type = Type(input_string=input_string, is_primitive=is_primitive)

        return typing.cast("Type", jsii.sinvoke(cls, "array", [item_type]))

    @jsii.member(jsii_name="char")
    @builtins.classmethod
    def char(cls, length: jsii.Number) -> "Type":
        '''(experimental) Fixed length character data, with a specified length between 1 and 255.

        :param length: length between 1 and 255.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b92f46741e45dc5d5e256fe3738d53a8878b40fc430d149eec6fdbfe167229)
            check_type(argname="argument length", value=length, expected_type=type_hints["length"])
        return typing.cast("Type", jsii.sinvoke(cls, "char", [length]))

    @jsii.member(jsii_name="decimal")
    @builtins.classmethod
    def decimal(
        cls,
        precision: jsii.Number,
        scale: typing.Optional[jsii.Number] = None,
    ) -> "Type":
        '''(experimental) Creates a decimal type.

        TODO: Bounds

        :param precision: the total number of digits.
        :param scale: the number of digits in fractional part, the default is 0.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcdd8f07d6d5e4e87f54cd2104a8605a571a6abede0b42465e2352b51723b900)
            check_type(argname="argument precision", value=precision, expected_type=type_hints["precision"])
            check_type(argname="argument scale", value=scale, expected_type=type_hints["scale"])
        return typing.cast("Type", jsii.sinvoke(cls, "decimal", [precision, scale]))

    @jsii.member(jsii_name="map")
    @builtins.classmethod
    def map(
        cls,
        key_type: typing.Union["Type", typing.Dict[builtins.str, typing.Any]],
        *,
        input_string: builtins.str,
        is_primitive: builtins.bool,
    ) -> "Type":
        '''(experimental) Creates a map of some primitive key type to some value type.

        :param key_type: type of key, must be a primitive.
        :param input_string: (experimental) Glue InputString for this type.
        :param is_primitive: (experimental) Indicates whether this type is a primitive data type.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc04f65c508e37fca936dfd67a8b4a0f84a73b9ef9c446edcd34f17c738c8dae)
            check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
        value_type = Type(input_string=input_string, is_primitive=is_primitive)

        return typing.cast("Type", jsii.sinvoke(cls, "map", [key_type, value_type]))

    @jsii.member(jsii_name="struct")
    @builtins.classmethod
    def struct(
        cls,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    ) -> "Type":
        '''(experimental) Creates a nested structure containing individually named and typed columns.

        :param columns: the columns of the structure.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33f94b4c838eb0e3d03de4da6b4f3fe8e873ef98895fb940645c459801c4bb50)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
        return typing.cast("Type", jsii.sinvoke(cls, "struct", [columns]))

    @jsii.member(jsii_name="varchar")
    @builtins.classmethod
    def varchar(cls, length: jsii.Number) -> "Type":
        '''(experimental) Variable length character data, with a specified length between 1 and 65535.

        :param length: length between 1 and 65535.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba18137b7dd32100f635af375c8586adc2f9824c4ccd0a1b01168f5ba757da4)
            check_type(argname="argument length", value=length, expected_type=type_hints["length"])
        return typing.cast("Type", jsii.sinvoke(cls, "varchar", [length]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BIG_INT")
    def BIG_INT(cls) -> "Type":
        '''(experimental) A 64-bit signed INTEGER in two’s complement format, with a minimum value of -2^63 and a maximum value of 2^63-1.

        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "BIG_INT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BINARY")
    def BINARY(cls) -> "Type":
        '''
        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "BINARY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="BOOLEAN")
    def BOOLEAN(cls) -> "Type":
        '''
        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "BOOLEAN"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DATE")
    def DATE(cls) -> "Type":
        '''(experimental) Date type.

        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "DATE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOUBLE")
    def DOUBLE(cls) -> "Type":
        '''
        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "DOUBLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FLOAT")
    def FLOAT(cls) -> "Type":
        '''
        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "FLOAT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INTEGER")
    def INTEGER(cls) -> "Type":
        '''(experimental) A 32-bit signed INTEGER in two’s complement format, with a minimum value of -2^31 and a maximum value of 2^31-1.

        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "INTEGER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SMALL_INT")
    def SMALL_INT(cls) -> "Type":
        '''(experimental) A 16-bit signed INTEGER in two’s complement format, with a minimum value of -2^15 and a maximum value of 2^15-1.

        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "SMALL_INT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STRING")
    def STRING(cls) -> "Type":
        '''(experimental) Arbitrary-length string type.

        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "STRING"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TIMESTAMP")
    def TIMESTAMP(cls) -> "Type":
        '''(experimental) Timestamp type (date and time).

        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "TIMESTAMP"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="TINY_INT")
    def TINY_INT(cls) -> "Type":
        '''(experimental) A 8-bit signed INTEGER in two’s complement format, with a minimum value of -2^7 and a maximum value of 2^7-1.

        :stability: experimental
        '''
        return typing.cast("Type", jsii.sget(cls, "TINY_INT"))


@jsii.implements(ISecurityConfiguration)
class SecurityConfiguration(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.SecurityConfiguration",
):
    '''(experimental) A security configuration is a set of security properties that can be used by AWS Glue to encrypt data at rest.

    The following scenarios show some of the ways that you can use a security configuration.

    - Attach a security configuration to an AWS Glue crawler to write encrypted Amazon CloudWatch Logs.
    - Attach a security configuration to an extract, transform, and load (ETL) job to write encrypted Amazon Simple Storage Service (Amazon S3) targets and encrypted CloudWatch Logs.
    - Attach a security configuration to an ETL job to write its jobs bookmarks as encrypted Amazon S3 data.
    - Attach a security configuration to a development endpoint to write encrypted Amazon S3 targets.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.SecurityConfiguration(self, "MySecurityConfiguration",
            cloud_watch_encryption=glue.CloudWatchEncryption(
                mode=glue.CloudWatchEncryptionMode.KMS
            ),
            job_bookmarks_encryption=glue.JobBookmarksEncryption(
                mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
            ),
            s3_encryption=glue.S3Encryption(
                mode=glue.S3EncryptionMode.KMS
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_watch_encryption: typing.Optional[typing.Union[CloudWatchEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
        job_bookmarks_encryption: typing.Optional[typing.Union[JobBookmarksEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_encryption: typing.Optional[typing.Union[S3Encryption, typing.Dict[builtins.str, typing.Any]]] = None,
        security_configuration_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_watch_encryption: (experimental) The encryption configuration for Amazon CloudWatch Logs. Default: no cloudwatch logs encryption.
        :param job_bookmarks_encryption: (experimental) The encryption configuration for Glue Job Bookmarks. Default: no job bookmarks encryption.
        :param s3_encryption: (experimental) The encryption configuration for Amazon Simple Storage Service (Amazon S3) data. Default: no s3 encryption.
        :param security_configuration_name: (experimental) The name of the security configuration. Default: - generated by CDK.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd628a6199f5b5fb7644771f78b6cc6d9230e3c38bba0463810d192bceb52e8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecurityConfigurationProps(
            cloud_watch_encryption=cloud_watch_encryption,
            job_bookmarks_encryption=job_bookmarks_encryption,
            s3_encryption=s3_encryption,
            security_configuration_name=security_configuration_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecurityConfigurationName")
    @builtins.classmethod
    def from_security_configuration_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        security_configuration_name: builtins.str,
    ) -> ISecurityConfiguration:
        '''(experimental) Creates a Connection construct that represents an external security configuration.

        :param scope: The scope creating construct (usually ``this``).
        :param id: The construct's id.
        :param security_configuration_name: name of external security configuration.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a85db96fd444625c46f4574190ecd86214bed327c2f826ee3294853f69a42b6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument security_configuration_name", value=security_configuration_name, expected_type=type_hints["security_configuration_name"])
        return typing.cast(ISecurityConfiguration, jsii.sinvoke(cls, "fromSecurityConfigurationName", [scope, id, security_configuration_name]))

    @builtins.property
    @jsii.member(jsii_name="securityConfigurationName")
    def security_configuration_name(self) -> builtins.str:
        '''(experimental) The name of the security configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "securityConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="cloudWatchEncryptionKey")
    def cloud_watch_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used in CloudWatch encryption if it requires a kms key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "cloudWatchEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="jobBookmarksEncryptionKey")
    def job_bookmarks_encryption_key(
        self,
    ) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used in job bookmarks encryption if it requires a kms key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "jobBookmarksEncryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="s3EncryptionKey")
    def s3_encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used in S3 encryption if it requires a kms key.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "s3EncryptionKey"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.SecurityConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_watch_encryption": "cloudWatchEncryption",
        "job_bookmarks_encryption": "jobBookmarksEncryption",
        "s3_encryption": "s3Encryption",
        "security_configuration_name": "securityConfigurationName",
    },
)
class SecurityConfigurationProps:
    def __init__(
        self,
        *,
        cloud_watch_encryption: typing.Optional[typing.Union[CloudWatchEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
        job_bookmarks_encryption: typing.Optional[typing.Union[JobBookmarksEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_encryption: typing.Optional[typing.Union[S3Encryption, typing.Dict[builtins.str, typing.Any]]] = None,
        security_configuration_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Constructions properties of ``SecurityConfiguration``.

        :param cloud_watch_encryption: (experimental) The encryption configuration for Amazon CloudWatch Logs. Default: no cloudwatch logs encryption.
        :param job_bookmarks_encryption: (experimental) The encryption configuration for Glue Job Bookmarks. Default: no job bookmarks encryption.
        :param s3_encryption: (experimental) The encryption configuration for Amazon Simple Storage Service (Amazon S3) data. Default: no s3 encryption.
        :param security_configuration_name: (experimental) The name of the security configuration. Default: - generated by CDK.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.SecurityConfiguration(self, "MySecurityConfiguration",
                cloud_watch_encryption=glue.CloudWatchEncryption(
                    mode=glue.CloudWatchEncryptionMode.KMS
                ),
                job_bookmarks_encryption=glue.JobBookmarksEncryption(
                    mode=glue.JobBookmarksEncryptionMode.CLIENT_SIDE_KMS
                ),
                s3_encryption=glue.S3Encryption(
                    mode=glue.S3EncryptionMode.KMS
                )
            )
        '''
        if isinstance(cloud_watch_encryption, dict):
            cloud_watch_encryption = CloudWatchEncryption(**cloud_watch_encryption)
        if isinstance(job_bookmarks_encryption, dict):
            job_bookmarks_encryption = JobBookmarksEncryption(**job_bookmarks_encryption)
        if isinstance(s3_encryption, dict):
            s3_encryption = S3Encryption(**s3_encryption)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b8dd2838cd56b87c144ac347e4b66a78dd0c85a6196f1282adce12bd2e94f36)
            check_type(argname="argument cloud_watch_encryption", value=cloud_watch_encryption, expected_type=type_hints["cloud_watch_encryption"])
            check_type(argname="argument job_bookmarks_encryption", value=job_bookmarks_encryption, expected_type=type_hints["job_bookmarks_encryption"])
            check_type(argname="argument s3_encryption", value=s3_encryption, expected_type=type_hints["s3_encryption"])
            check_type(argname="argument security_configuration_name", value=security_configuration_name, expected_type=type_hints["security_configuration_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cloud_watch_encryption is not None:
            self._values["cloud_watch_encryption"] = cloud_watch_encryption
        if job_bookmarks_encryption is not None:
            self._values["job_bookmarks_encryption"] = job_bookmarks_encryption
        if s3_encryption is not None:
            self._values["s3_encryption"] = s3_encryption
        if security_configuration_name is not None:
            self._values["security_configuration_name"] = security_configuration_name

    @builtins.property
    def cloud_watch_encryption(self) -> typing.Optional[CloudWatchEncryption]:
        '''(experimental) The encryption configuration for Amazon CloudWatch Logs.

        :default: no cloudwatch logs encryption.

        :stability: experimental
        '''
        result = self._values.get("cloud_watch_encryption")
        return typing.cast(typing.Optional[CloudWatchEncryption], result)

    @builtins.property
    def job_bookmarks_encryption(self) -> typing.Optional[JobBookmarksEncryption]:
        '''(experimental) The encryption configuration for Glue Job Bookmarks.

        :default: no job bookmarks encryption.

        :stability: experimental
        '''
        result = self._values.get("job_bookmarks_encryption")
        return typing.cast(typing.Optional[JobBookmarksEncryption], result)

    @builtins.property
    def s3_encryption(self) -> typing.Optional[S3Encryption]:
        '''(experimental) The encryption configuration for Amazon Simple Storage Service (Amazon S3) data.

        :default: no s3 encryption.

        :stability: experimental
        '''
        result = self._values.get("s3_encryption")
        return typing.cast(typing.Optional[S3Encryption], result)

    @builtins.property
    def security_configuration_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the security configuration.

        :default: - generated by CDK.

        :stability: experimental
        '''
        result = self._values.get("security_configuration_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SerializationLibrary(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.SerializationLibrary",
):
    '''(experimental) Serialization library to use when serializing/deserializing (SerDe) table records.

    :see: https://cwiki.apache.org/confluence/display/Hive/SerDe
    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_glue_alpha as glue_alpha
        
        serialization_library = glue_alpha.SerializationLibrary.AVRO
    '''

    def __init__(self, class_name: builtins.str) -> None:
        '''
        :param class_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44b6eea0230610f203e5d4ed1dbd871c9ecc76a60681d0500a51e2d3815f193e)
            check_type(argname="argument class_name", value=class_name, expected_type=type_hints["class_name"])
        jsii.create(self.__class__, self, [class_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AVRO")
    def AVRO(cls) -> "SerializationLibrary":
        '''
        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/serde2/avro/AvroSerDe.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "AVRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDTRAIL")
    def CLOUDTRAIL(cls) -> "SerializationLibrary":
        '''
        :see: https://docs.aws.amazon.com/athena/latest/ug/cloudtrail.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "CLOUDTRAIL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="GROK")
    def GROK(cls) -> "SerializationLibrary":
        '''
        :see: https://docs.aws.amazon.com/athena/latest/ug/grok.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "GROK"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIVE_JSON")
    def HIVE_JSON(cls) -> "SerializationLibrary":
        '''
        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hive/hcatalog/data/JsonSerDe.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "HIVE_JSON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LAZY_SIMPLE")
    def LAZY_SIMPLE(cls) -> "SerializationLibrary":
        '''
        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/serde2/lazy/LazySimpleSerDe.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "LAZY_SIMPLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPEN_CSV")
    def OPEN_CSV(cls) -> "SerializationLibrary":
        '''
        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/serde2/OpenCSVSerde.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "OPEN_CSV"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OPENX_JSON")
    def OPENX_JSON(cls) -> "SerializationLibrary":
        '''
        :see: https://github.com/rcongiu/Hive-JSON-Serde
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "OPENX_JSON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORC")
    def ORC(cls) -> "SerializationLibrary":
        '''
        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/orc/OrcSerde.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "ORC"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARQUET")
    def PARQUET(cls) -> "SerializationLibrary":
        '''
        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/ql/io/parquet/serde/ParquetHiveSerDe.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "PARQUET"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="REGEXP")
    def REGEXP(cls) -> "SerializationLibrary":
        '''
        :see: https://svn.apache.org/repos/infra/websites/production/hive/content/javadocs/r3.1.3/api/org/apache/hadoop/hive/serde2/RegexSerDe.html
        :stability: experimental
        '''
        return typing.cast("SerializationLibrary", jsii.sget(cls, "REGEXP"))

    @builtins.property
    @jsii.member(jsii_name="className")
    def class_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "className"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.SparkUILoggingLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "prefix": "prefix"},
)
class SparkUILoggingLocation:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The Spark UI logging location.

        :param bucket: (experimental) The bucket where the Glue job stores the logs. Default: - a new bucket will be created.
        :param prefix: (experimental) The path inside the bucket (objects prefix) where the Glue job stores the logs. Default: - the logs will be written at the root of the bucket

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            from aws_cdk import aws_s3 as s3
            
            # bucket: s3.Bucket
            
            spark_uILogging_location = glue_alpha.SparkUILoggingLocation(
                bucket=bucket,
            
                # the properties below are optional
                prefix="prefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5697eede3034b2366456fa6abdccec9640fd76f2916540c3a178d004e5cd680a)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) The bucket where the Glue job stores the logs.

        :default: - a new bucket will be created.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path inside the bucket (objects prefix) where the Glue job stores the logs.

        :default: - the logs will be written at the root of the bucket

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkUILoggingLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.SparkUIProps",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "bucket": "bucket", "prefix": "prefix"},
)
class SparkUIProps:
    def __init__(
        self,
        *,
        enabled: builtins.bool,
        bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for enabling Spark UI monitoring feature for Spark-based Glue jobs.

        :param enabled: (experimental) Enable Spark UI.
        :param bucket: (experimental) The bucket where the Glue job stores the logs. Default: - a new bucket will be created.
        :param prefix: (experimental) The path inside the bucket (objects prefix) where the Glue job stores the logs. Use format ``'foo/bar/'`` Default: - the logs will be written at the root of the bucket

        :see: https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            glue.Job(self, "EnableSparkUI",
                job_name="EtlJobWithSparkUIPrefix",
                spark_uI=glue.SparkUIProps(
                    enabled=True
                ),
                executable=glue.JobExecutable.python_etl(
                    glue_version=glue.GlueVersion.V3_0,
                    python_version=glue.PythonVersion.THREE,
                    script=glue.Code.from_asset(path.join(__dirname, "job-script", "hello_world.py"))
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c613959b2bc20f05aa8f4578d26e870c2d4044aaaee1a5248ed0ddf8d4b75776)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if bucket is not None:
            self._values["bucket"] = bucket
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def enabled(self) -> builtins.bool:
        '''(experimental) Enable Spark UI.

        :stability: experimental
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''(experimental) The bucket where the Glue job stores the logs.

        :default: - a new bucket will be created.

        :stability: experimental
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path inside the bucket (objects prefix) where the Glue job stores the logs.

        Use format ``'foo/bar/'``

        :default: - the logs will be written at the root of the bucket

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SparkUIProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StorageParameter(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.StorageParameter",
):
    '''(experimental) A storage parameter. The list of storage parameters available is not exhaustive and other keys may be used.

    If you would like to specify a storage parameter that is not available as a static member of this class, use the ``StorageParameter.custom`` method.

    The list of storage parameters currently known within the CDK is listed.

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"*
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_database: glue.Database
        
        glue.S3Table(self, "MyTable",
            storage_parameters=[
                glue.StorageParameter.skip_header_line_count(1),
                glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
                glue.StorageParameter.custom("separatorChar", ",")
            ],
            # ...
            database=my_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            data_format=glue.DataFormat.JSON
        )
    '''

    def __init__(self, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f74283389af10eaf6da714f4aadddf86dec9f3da227641c23ae118f6dfd7b45)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.create(self.__class__, self, [key, value])

    @jsii.member(jsii_name="columnCountMismatchHandling")
    @builtins.classmethod
    def column_count_mismatch_handling(
        cls,
        value: ColumnCountMismatchHandlingAction,
    ) -> "StorageParameter":
        '''(experimental) Identifies if the file contains less or more values for a row than the number of columns specified in the external table definition.

        This property is only available for an uncompressed text file format.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39c7b662e4b538ebbd408dcac5b933ae4d1527472b30facbc0405a6a1d3bb14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "columnCountMismatchHandling", [value]))

    @jsii.member(jsii_name="compressionType")
    @builtins.classmethod
    def compression_type(cls, value: CompressionType) -> "StorageParameter":
        '''(experimental) The type of compression used on the table, when the file name does not contain an extension.

        This value overrides the compression type specified through the extension.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__666d2a40474ee489c242320aca5600aa88eb0e9ff6b3f6f2523138d1febe5b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "compressionType", [value]))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, key: builtins.str, value: typing.Any) -> "StorageParameter":
        '''(experimental) A custom storage parameter.

        :param key: - The key of the storage parameter.
        :param value: - The value of the storage parameter.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__972574c985d99d1bb6f6d431a08c62d778ff9dd7c7acaa151f9c4c535255e211)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "custom", [key, value]))

    @jsii.member(jsii_name="dataCleansingEnabled")
    @builtins.classmethod
    def data_cleansing_enabled(cls, value: builtins.bool) -> "StorageParameter":
        '''(experimental) Determines whether data handling is on for the table.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7446681fb6fa8d72452081fd5567c4cfb319974b0acc83e49ae911e49d15d02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "dataCleansingEnabled", [value]))

    @jsii.member(jsii_name="invalidCharHandling")
    @builtins.classmethod
    def invalid_char_handling(
        cls,
        value: InvalidCharHandlingAction,
    ) -> "StorageParameter":
        '''(experimental) Specifies the action to perform when query results contain invalid UTF-8 character values.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4fecfebea5461d7e6230a0187c52f9a9d764b9e29971ed3414e1d84633f26ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "invalidCharHandling", [value]))

    @jsii.member(jsii_name="numericOverflowHandling")
    @builtins.classmethod
    def numeric_overflow_handling(
        cls,
        value: NumericOverflowHandlingAction,
    ) -> "StorageParameter":
        '''(experimental) Specifies the action to perform when ORC data contains an integer (for example, BIGINT or int64) that is larger than the column definition (for example, SMALLINT or int16).

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bbe8806a487d42b3c7b3868e2419195fd8e623ea4a74692a316cc258efafb28)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "numericOverflowHandling", [value]))

    @jsii.member(jsii_name="numRows")
    @builtins.classmethod
    def num_rows(cls, value: jsii.Number) -> "StorageParameter":
        '''(experimental) A property that sets the numRows value for the table definition.

        To explicitly update an external table's statistics, set the numRows property to indicate the size of the table. Amazon Redshift doesn't analyze external tables to generate the table statistics that the query optimizer uses to generate a query plan. If table statistics aren't set for an external table, Amazon Redshift generates a query execution plan based on an assumption that external tables are the larger tables and local tables are the smaller tables.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0897c928202255a3b3383203c753ac3165280fbc81faec3dd559c25843d4d3d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "numRows", [value]))

    @jsii.member(jsii_name="orcSchemaResolution")
    @builtins.classmethod
    def orc_schema_resolution(cls, value: OrcColumnMappingType) -> "StorageParameter":
        '''(experimental) A property that sets the column mapping type for tables that use ORC data format.

        This property is ignored for other data formats. If this property is omitted, columns are mapped by ``OrcColumnMappingType.NAME`` by default.

        :param value: -

        :default: OrcColumnMappingType.NAME

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb88780e26a940311a2cf44dd5d68de1ff362d2d0ca028f0443bba7e4bb06a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "orcSchemaResolution", [value]))

    @jsii.member(jsii_name="replacementChar")
    @builtins.classmethod
    def replacement_char(cls, value: builtins.str) -> "StorageParameter":
        '''(experimental) Specifies the replacement character to use when you set ``INVALID_CHAR_HANDLING`` to ``REPLACE``.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4284890747f6d237b5fdefef7df7ed57b66bda672915eb23526cae4e1b45ac7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "replacementChar", [value]))

    @jsii.member(jsii_name="serializationNullFormat")
    @builtins.classmethod
    def serialization_null_format(cls, value: builtins.str) -> "StorageParameter":
        '''(experimental) A property that sets number of rows to skip at the beginning of each source file.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d196d1d149d7fb743eb77988c4d05f55b9e72876647220d0067b47caeab18a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "serializationNullFormat", [value]))

    @jsii.member(jsii_name="skipHeaderLineCount")
    @builtins.classmethod
    def skip_header_line_count(cls, value: jsii.Number) -> "StorageParameter":
        '''(experimental) The number of rows to skip at the top of a CSV file when the table is being created.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2e1fd759f08830451a50273269345e05b91bbd90e750e7b76b2bac5275870a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "skipHeaderLineCount", [value]))

    @jsii.member(jsii_name="surplusBytesHandling")
    @builtins.classmethod
    def surplus_bytes_handling(
        cls,
        value: "SurplusBytesHandlingAction",
    ) -> "StorageParameter":
        '''(experimental) Specifies how to handle data being loaded that exceeds the length of the data type defined for columns containing VARBYTE data.

        By default, Redshift Spectrum sets the value to null for data that exceeds the width of the column.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c04fd2fab2c9a95b1c92f9718dfe11ffeb2436d47a798d0f870aae58746f67a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "surplusBytesHandling", [value]))

    @jsii.member(jsii_name="surplusCharHandling")
    @builtins.classmethod
    def surplus_char_handling(
        cls,
        value: "SurplusCharHandlingAction",
    ) -> "StorageParameter":
        '''(experimental) Specifies how to handle data being loaded that exceeds the length of the data type defined for columns containing VARCHAR, CHAR, or string data.

        By default, Redshift Spectrum sets the value to null for data that exceeds the width of the column.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e1b9effa7f6a703549bb4dbdc074898313b647fe00864615574b5f4527a6efd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "surplusCharHandling", [value]))

    @jsii.member(jsii_name="writeKmsKeyId")
    @builtins.classmethod
    def write_kms_key_id(cls, value: builtins.str) -> "StorageParameter":
        '''(experimental) You can specify an AWS Key Management Service key to enable Server–Side Encryption (SSE) for Amazon S3 objects.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786b7e6901c19fc29fc68d4fe9cfd302c0d877d823b66a1fc00cd87af05bc1a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "writeKmsKeyId", [value]))

    @jsii.member(jsii_name="writeMaxFileSizeMb")
    @builtins.classmethod
    def write_max_file_size_mb(cls, value: jsii.Number) -> "StorageParameter":
        '''(experimental) A property that sets the maximum size (in MB) of each file written to Amazon S3 by CREATE EXTERNAL TABLE AS.

        The size must be a valid integer between 5 and 6200. The default maximum file size is 6,200 MB. This table property also applies to any subsequent INSERT statement into the same external table.

        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d6b28d6c7211b035722cff75146ec9b7f6d1ef3da62494976a7200ddf69ed8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "writeMaxFileSizeMb", [value]))

    @jsii.member(jsii_name="writeParallel")
    @builtins.classmethod
    def write_parallel(cls, value: "WriteParallel") -> "StorageParameter":
        '''(experimental) A property that sets whether CREATE EXTERNAL TABLE AS should write data in parallel.

        When 'write.parallel' is set to off, CREATE EXTERNAL TABLE AS writes to one or more data files serially onto Amazon S3. This table property also applies to any subsequent INSERT statement into the same external table.

        :param value: -

        :default: WriteParallel.ON

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__934bd25af2a5a54f5badd7296f8c59c0bd6be0399bcb84d225a10f0f5db755d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("StorageParameter", jsii.sinvoke(cls, "writeParallel", [value]))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "value"))


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.StorageParameters")
class StorageParameters(enum.Enum):
    '''(experimental) The storage parameter keys that are currently known, this list is not exhaustive and other keys may be used.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # glue_database: glue.IDatabase
        
        table = glue.Table(self, "Table",
            storage_parameters=[
                glue.StorageParameter.skip_header_line_count(1),
                glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
                glue.StorageParameter.custom("foo", "bar"),  # Will have no effect
                glue.StorageParameter.custom("separatorChar", ","),  # Will describe the separator char used in the data
                glue.StorageParameter.custom(glue.StorageParameters.WRITE_PARALLEL, "off")
            ],
            # ...
            database=glue_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            data_format=glue.DataFormat.CSV
        )
    '''

    SKIP_HEADER_LINE_COUNT = "SKIP_HEADER_LINE_COUNT"
    '''(experimental) The number of rows to skip at the top of a CSV file when the table is being created.

    :stability: experimental
    '''
    DATA_CLEANSING_ENABLED = "DATA_CLEANSING_ENABLED"
    '''(experimental) Determines whether data handling is on for the table.

    :stability: experimental
    '''
    COMPRESSION_TYPE = "COMPRESSION_TYPE"
    '''(experimental) The type of compression used on the table, when the file name does not contain an extension.

    This value overrides the compression type specified through the extension.

    :stability: experimental
    '''
    INVALID_CHAR_HANDLING = "INVALID_CHAR_HANDLING"
    '''(experimental) Specifies the action to perform when query results contain invalid UTF-8 character values.

    :stability: experimental
    '''
    REPLACEMENT_CHAR = "REPLACEMENT_CHAR"
    '''(experimental) Specifies the replacement character to use when you set ``INVALID_CHAR_HANDLING`` to ``REPLACE``.

    :stability: experimental
    '''
    NUMERIC_OVERFLOW_HANDLING = "NUMERIC_OVERFLOW_HANDLING"
    '''(experimental) Specifies the action to perform when ORC data contains an integer (for example, BIGINT or int64) that is larger than the column definition (for example, SMALLINT or int16).

    :stability: experimental
    '''
    SURPLUS_BYTES_HANDLING = "SURPLUS_BYTES_HANDLING"
    '''(experimental) Specifies how to handle data being loaded that exceeds the length of the data type defined for columns containing VARBYTE data.

    By default, Redshift Spectrum sets the value to null for data that exceeds the width of the column.

    :stability: experimental
    '''
    SURPLUS_CHAR_HANDLING = "SURPLUS_CHAR_HANDLING"
    '''(experimental) Specifies how to handle data being loaded that exceeds the length of the data type defined for columns containing VARCHAR, CHAR, or string data.

    By default, Redshift Spectrum sets the value to null for data that exceeds the width of the column.

    :stability: experimental
    '''
    COLUMN_COUNT_MISMATCH_HANDLING = "COLUMN_COUNT_MISMATCH_HANDLING"
    '''(experimental) Identifies if the file contains less or more values for a row than the number of columns specified in the external table definition.

    This property is only available for an uncompressed text file format.

    :stability: experimental
    '''
    NUM_ROWS = "NUM_ROWS"
    '''(experimental) A property that sets the numRows value for the table definition.

    To explicitly update an external table's statistics, set the numRows property to indicate the size of the table. Amazon Redshift doesn't analyze external tables to generate the table statistics that the query optimizer uses to generate a query plan. If table statistics aren't set for an external table, Amazon Redshift generates a query execution plan based on an assumption that external tables are the larger tables and local tables are the smaller tables.

    :stability: experimental
    '''
    SERIALIZATION_NULL_FORMAT = "SERIALIZATION_NULL_FORMAT"
    '''(experimental) A property that sets number of rows to skip at the beginning of each source file.

    :stability: experimental
    '''
    ORC_SCHEMA_RESOLUTION = "ORC_SCHEMA_RESOLUTION"
    '''(experimental) A property that sets the column mapping type for tables that use ORC data format.

    This property is ignored for other data formats.

    :stability: experimental
    '''
    WRITE_PARALLEL = "WRITE_PARALLEL"
    '''(experimental) A property that sets whether CREATE EXTERNAL TABLE AS should write data in parallel.

    When 'write.parallel' is set to off, CREATE EXTERNAL TABLE AS writes to one or more data files serially onto Amazon S3. This table property also applies to any subsequent INSERT statement into the same external table.

    :stability: experimental
    '''
    WRITE_MAX_FILESIZE_MB = "WRITE_MAX_FILESIZE_MB"
    '''(experimental) A property that sets the maximum size (in MB) of each file written to Amazon S3 by CREATE EXTERNAL TABLE AS.

    The size must be a valid integer between 5 and 6200. The default maximum file size is 6,200 MB. This table property also applies to any subsequent INSERT statement into the same external table.

    :stability: experimental
    '''
    WRITE_KMS_KEY_ID = "WRITE_KMS_KEY_ID"
    '''(experimental) You can specify an AWS Key Management Service key to enable Server–Side Encryption (SSE) for Amazon S3 objects.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.SurplusBytesHandlingAction")
class SurplusBytesHandlingAction(enum.Enum):
    '''(experimental) Specifies how to handle data being loaded that exceeds the length of the data type defined for columns containing VARBYTE data.

    By default, Redshift Spectrum sets the value to null for data that exceeds the width of the column.

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"* > *"surplus_bytes_handling"*
    :stability: experimental
    '''

    SET_TO_NULL = "SET_TO_NULL"
    '''(experimental) Replaces data that exceeds the column width with null.

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) Doesn't perform surplus byte handling.

    :stability: experimental
    '''
    FAIL = "FAIL"
    '''(experimental) Cancels queries that return data exceeding the column width.

    :stability: experimental
    '''
    DROP_ROW = "DROP_ROW"
    '''(experimental) Drop all rows that contain data exceeding column width.

    :stability: experimental
    '''
    TRUNCATE = "TRUNCATE"
    '''(experimental) Removes the characters that exceed the maximum number of characters defined for the column.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.SurplusCharHandlingAction")
class SurplusCharHandlingAction(enum.Enum):
    '''(experimental) Specifies how to handle data being loaded that exceeds the length of the data type defined for columns containing VARCHAR, CHAR, or string data.

    By default, Redshift Spectrum sets the value to null for data that exceeds the width of the column.

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"* > *"surplus_char_handling"*
    :stability: experimental
    '''

    SET_TO_NULL = "SET_TO_NULL"
    '''(experimental) Replaces data that exceeds the column width with null.

    :stability: experimental
    '''
    DISABLED = "DISABLED"
    '''(experimental) Doesn't perform surplus character handling.

    :stability: experimental
    '''
    FAIL = "FAIL"
    '''(experimental) Cancels queries that return data exceeding the column width.

    :stability: experimental
    '''
    DROP_ROW = "DROP_ROW"
    '''(experimental) Replaces each value in the row with null.

    :stability: experimental
    '''
    TRUNCATE = "TRUNCATE"
    '''(experimental) Removes the characters that exceed the maximum number of characters defined for the column.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.TableAttributes",
    jsii_struct_bases=[],
    name_mapping={"table_arn": "tableArn", "table_name": "tableName"},
)
class TableAttributes:
    def __init__(self, *, table_arn: builtins.str, table_name: builtins.str) -> None:
        '''
        :param table_arn: 
        :param table_name: 

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            
            table_attributes = glue_alpha.TableAttributes(
                table_arn="tableArn",
                table_name="tableName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a76a75ff6c3a793e7e5f24f77665e06ab62ec467008c0ae0a13c2537b6003d)
            check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "table_arn": table_arn,
            "table_name": table_name,
        }

    @builtins.property
    def table_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("table_arn")
        assert result is not None, "Required property 'table_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def table_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        result = self._values.get("table_name")
        assert result is not None, "Required property 'table_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITable)
class TableBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-glue-alpha.TableBase",
):
    '''(experimental) A Glue table.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_glue_alpha as glue_alpha
        
        table_base = glue_alpha.TableBase.from_table_arn(self, "MyTableBase", "tableArn")
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
        database: IDatabase,
        data_format: DataFormat,
        compressed: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        enable_partition_filtering: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
        partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param columns: (experimental) Columns of the table.
        :param database: (experimental) Database in which to store the table.
        :param data_format: (experimental) Storage type of the table's data.
        :param compressed: (experimental) Indicates whether the table's data is compressed or not. Default: false
        :param description: (experimental) Description of the table. Default: generated
        :param enable_partition_filtering: (experimental) Enables partition filtering. Default: - The parameter is not defined
        :param parameters: (experimental) The key/value pairs define properties associated with the table. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Default: - The parameter is not defined
        :param partition_indexes: (experimental) Partition indexes on the table. A maximum of 3 indexes are allowed on a table. Keys in the index must be part of the table's partition keys. Default: table has no partition indexes
        :param partition_keys: (experimental) Partition columns of the table. Default: table is not partitioned
        :param storage_parameters: (experimental) The user-supplied properties for the description of the physical storage of this table. These properties help describe the format of the data that is stored within the crawled data sources. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property. Default: - The parameter is not defined
        :param stored_as_sub_directories: (experimental) Indicates whether the table data is stored in subdirectories. Default: false
        :param table_name: (experimental) Name of the table. Default: - generated by CDK.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3498ddd8b03f8ca1e3bea08a9f07832747b340c2a3681dc513148655f79ad155)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = TableBaseProps(
            columns=columns,
            database=database,
            data_format=data_format,
            compressed=compressed,
            description=description,
            enable_partition_filtering=enable_partition_filtering,
            parameters=parameters,
            partition_indexes=partition_indexes,
            partition_keys=partition_keys,
            storage_parameters=storage_parameters,
            stored_as_sub_directories=stored_as_sub_directories,
            table_name=table_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromTableArn")
    @builtins.classmethod
    def from_table_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        table_arn: builtins.str,
    ) -> ITable:
        '''
        :param scope: -
        :param id: -
        :param table_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02bd4969b95beb4e956637865cbc28ff5818c6ec54f938297add787350585c81)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument table_arn", value=table_arn, expected_type=type_hints["table_arn"])
        return typing.cast(ITable, jsii.sinvoke(cls, "fromTableArn", [scope, id, table_arn]))

    @jsii.member(jsii_name="fromTableAttributes")
    @builtins.classmethod
    def from_table_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        table_arn: builtins.str,
        table_name: builtins.str,
    ) -> ITable:
        '''(experimental) Creates a Table construct that represents an external table.

        :param scope: The scope creating construct (usually ``this``).
        :param id: The construct's id.
        :param table_arn: 
        :param table_name: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58099cdb2e6af7cafb7eb58d27cec43a72e06cce30052aef55c41e9f4574cb47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = TableAttributes(table_arn=table_arn, table_name=table_name)

        return typing.cast(ITable, jsii.sinvoke(cls, "fromTableAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="addPartitionIndex")
    def add_partition_index(
        self,
        *,
        key_names: typing.Sequence[builtins.str],
        index_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Add a partition index to the table.

        You can have a maximum of 3 partition
        indexes to a table. Partition index keys must be a subset of the table's
        partition keys.

        :param key_names: (experimental) The partition key names that comprise the partition index. The names must correspond to a name in the table's partition keys.
        :param index_name: (experimental) The name of the partition index. Default: - a name will be generated for you.

        :see: https://docs.aws.amazon.com/glue/latest/dg/partition-indexes.html
        :stability: experimental
        '''
        index = PartitionIndex(key_names=key_names, index_name=index_name)

        return typing.cast(None, jsii.invoke(self, "addPartitionIndex", [index]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        actions: typing.Sequence[builtins.str],
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity custom permissions.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b9362ce2360a32cd6ed5b3e0b6fb67c0eeb2fadb38c5ce618002656d772e776)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, actions]))

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantReadWrite")
    @abc.abstractmethod
    def grant_read_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantToUnderlyingResources")
    def grant_to_underlying_resources(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        actions: typing.Sequence[builtins.str],
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant the given identity custom permissions to ALL underlying resources of the table.

        Permissions will be granted to the catalog, the database, and the table.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fefdc4d880c6035cf74f0867c529fd1390e46d666f130f14ef71eeb28507b1c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantToUnderlyingResources", [grantee, actions]))

    @jsii.member(jsii_name="grantWrite")
    @abc.abstractmethod
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="columns")
    def columns(self) -> typing.List[Column]:
        '''(experimental) This table's columns.

        :stability: experimental
        '''
        return typing.cast(typing.List[Column], jsii.get(self, "columns"))

    @builtins.property
    @jsii.member(jsii_name="compressed")
    def compressed(self) -> builtins.bool:
        '''(experimental) Indicates whether the table's data is compressed or not.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "compressed"))

    @builtins.property
    @jsii.member(jsii_name="database")
    def database(self) -> IDatabase:
        '''(experimental) Database this table belongs to.

        :stability: experimental
        '''
        return typing.cast(IDatabase, jsii.get(self, "database"))

    @builtins.property
    @jsii.member(jsii_name="dataFormat")
    def data_format(self) -> DataFormat:
        '''(experimental) Format of this table's data files.

        :stability: experimental
        '''
        return typing.cast(DataFormat, jsii.get(self, "dataFormat"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def _parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The tables' properties associated with the table.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters
        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    @abc.abstractmethod
    def table_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tableName")
    @abc.abstractmethod
    def table_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="tableResource")
    @abc.abstractmethod
    def _table_resource(self) -> _aws_cdk_aws_glue_ceddda9d.CfnTable:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="partitionIndexes")
    @abc.abstractmethod
    def partition_indexes(self) -> typing.Optional[typing.List[PartitionIndex]]:
        '''
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="partitionKeys")
    def partition_keys(self) -> typing.Optional[typing.List[Column]]:
        '''(experimental) This table's partition keys if the table is partitioned.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[Column]], jsii.get(self, "partitionKeys"))

    @builtins.property
    @jsii.member(jsii_name="storageParameters")
    def storage_parameters(self) -> typing.Optional[typing.List[StorageParameter]]:
        '''(experimental) The tables' storage descriptor properties.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[StorageParameter]], jsii.get(self, "storageParameters"))


class _TableBaseProxy(
    TableBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daad53122858b1d79a2d9a51e22fe701058f7a4a9f5b6d813930d2e34d3f2c63)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__316a7ca269e4227039ebebd0789404fc7ab5c3f9b3787007562ce4edf5df8225)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadWrite", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''
        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb08ef4e43dac45d9dc56da91de5195d72be73db28c81ee45853c2c2ac349abd)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="tableResource")
    def _table_resource(self) -> _aws_cdk_aws_glue_ceddda9d.CfnTable:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_glue_ceddda9d.CfnTable, jsii.get(self, "tableResource"))

    @builtins.property
    @jsii.member(jsii_name="partitionIndexes")
    def partition_indexes(self) -> typing.Optional[typing.List[PartitionIndex]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[PartitionIndex]], jsii.get(self, "partitionIndexes"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, TableBase).__jsii_proxy_class__ = lambda : _TableBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.TableBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "columns": "columns",
        "database": "database",
        "data_format": "dataFormat",
        "compressed": "compressed",
        "description": "description",
        "enable_partition_filtering": "enablePartitionFiltering",
        "parameters": "parameters",
        "partition_indexes": "partitionIndexes",
        "partition_keys": "partitionKeys",
        "storage_parameters": "storageParameters",
        "stored_as_sub_directories": "storedAsSubDirectories",
        "table_name": "tableName",
    },
)
class TableBaseProps:
    def __init__(
        self,
        *,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
        database: IDatabase,
        data_format: DataFormat,
        compressed: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        enable_partition_filtering: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
        partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param columns: (experimental) Columns of the table.
        :param database: (experimental) Database in which to store the table.
        :param data_format: (experimental) Storage type of the table's data.
        :param compressed: (experimental) Indicates whether the table's data is compressed or not. Default: false
        :param description: (experimental) Description of the table. Default: generated
        :param enable_partition_filtering: (experimental) Enables partition filtering. Default: - The parameter is not defined
        :param parameters: (experimental) The key/value pairs define properties associated with the table. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Default: - The parameter is not defined
        :param partition_indexes: (experimental) Partition indexes on the table. A maximum of 3 indexes are allowed on a table. Keys in the index must be part of the table's partition keys. Default: table has no partition indexes
        :param partition_keys: (experimental) Partition columns of the table. Default: table is not partitioned
        :param storage_parameters: (experimental) The user-supplied properties for the description of the physical storage of this table. These properties help describe the format of the data that is stored within the crawled data sources. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property. Default: - The parameter is not defined
        :param stored_as_sub_directories: (experimental) Indicates whether the table data is stored in subdirectories. Default: false
        :param table_name: (experimental) Name of the table. Default: - generated by CDK.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            
            # database: glue_alpha.Database
            # data_format: glue_alpha.DataFormat
            # storage_parameter: glue_alpha.StorageParameter
            
            table_base_props = glue_alpha.TableBaseProps(
                columns=[glue_alpha.Column(
                    name="name",
                    type=glue_alpha.Type(
                        input_string="inputString",
                        is_primitive=False
                    ),
            
                    # the properties below are optional
                    comment="comment"
                )],
                database=database,
                data_format=data_format,
            
                # the properties below are optional
                compressed=False,
                description="description",
                enable_partition_filtering=False,
                parameters={
                    "parameters_key": "parameters"
                },
                partition_indexes=[glue_alpha.PartitionIndex(
                    key_names=["keyNames"],
            
                    # the properties below are optional
                    index_name="indexName"
                )],
                partition_keys=[glue_alpha.Column(
                    name="name",
                    type=glue_alpha.Type(
                        input_string="inputString",
                        is_primitive=False
                    ),
            
                    # the properties below are optional
                    comment="comment"
                )],
                storage_parameters=[storage_parameter],
                stored_as_sub_directories=False,
                table_name="tableName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c621f615cea5a292fe84c07e10ca61e7529536864f1701be1f19b168483439de)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument compressed", value=compressed, expected_type=type_hints["compressed"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_partition_filtering", value=enable_partition_filtering, expected_type=type_hints["enable_partition_filtering"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument partition_indexes", value=partition_indexes, expected_type=type_hints["partition_indexes"])
            check_type(argname="argument partition_keys", value=partition_keys, expected_type=type_hints["partition_keys"])
            check_type(argname="argument storage_parameters", value=storage_parameters, expected_type=type_hints["storage_parameters"])
            check_type(argname="argument stored_as_sub_directories", value=stored_as_sub_directories, expected_type=type_hints["stored_as_sub_directories"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "database": database,
            "data_format": data_format,
        }
        if compressed is not None:
            self._values["compressed"] = compressed
        if description is not None:
            self._values["description"] = description
        if enable_partition_filtering is not None:
            self._values["enable_partition_filtering"] = enable_partition_filtering
        if parameters is not None:
            self._values["parameters"] = parameters
        if partition_indexes is not None:
            self._values["partition_indexes"] = partition_indexes
        if partition_keys is not None:
            self._values["partition_keys"] = partition_keys
        if storage_parameters is not None:
            self._values["storage_parameters"] = storage_parameters
        if stored_as_sub_directories is not None:
            self._values["stored_as_sub_directories"] = stored_as_sub_directories
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def columns(self) -> typing.List[Column]:
        '''(experimental) Columns of the table.

        :stability: experimental
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[Column], result)

    @builtins.property
    def database(self) -> IDatabase:
        '''(experimental) Database in which to store the table.

        :stability: experimental
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(IDatabase, result)

    @builtins.property
    def data_format(self) -> DataFormat:
        '''(experimental) Storage type of the table's data.

        :stability: experimental
        '''
        result = self._values.get("data_format")
        assert result is not None, "Required property 'data_format' is missing"
        return typing.cast(DataFormat, result)

    @builtins.property
    def compressed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the table's data is compressed or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("compressed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the table.

        :default: generated

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_partition_filtering(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables partition filtering.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/athena/latest/ug/glue-best-practices.html#glue-best-practices-partition-index
        :stability: experimental
        '''
        result = self._values.get("enable_partition_filtering")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The key/value pairs define properties associated with the table.

        The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def partition_indexes(self) -> typing.Optional[typing.List[PartitionIndex]]:
        '''(experimental) Partition indexes on the table.

        A maximum of 3 indexes
        are allowed on a table. Keys in the index must be part
        of the table's partition keys.

        :default: table has no partition indexes

        :stability: experimental
        '''
        result = self._values.get("partition_indexes")
        return typing.cast(typing.Optional[typing.List[PartitionIndex]], result)

    @builtins.property
    def partition_keys(self) -> typing.Optional[typing.List[Column]]:
        '''(experimental) Partition columns of the table.

        :default: table is not partitioned

        :stability: experimental
        '''
        result = self._values.get("partition_keys")
        return typing.cast(typing.Optional[typing.List[Column]], result)

    @builtins.property
    def storage_parameters(self) -> typing.Optional[typing.List[StorageParameter]]:
        '''(experimental) The user-supplied properties for the description of the physical storage of this table.

        These properties help describe the format of the data that is stored within the crawled data sources.

        The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed.

        Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"*
        :stability: experimental

        Example::

            # glue_database: glue.IDatabase
            
            table = glue.Table(self, "Table",
                storage_parameters=[
                    glue.StorageParameter.skip_header_line_count(1),
                    glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
                    glue.StorageParameter.custom("foo", "bar"),  # Will have no effect
                    glue.StorageParameter.custom("separatorChar", ","),  # Will describe the separator char used in the data
                    glue.StorageParameter.custom(glue.StorageParameters.WRITE_PARALLEL, "off")
                ],
                # ...
                database=glue_database,
                columns=[glue.Column(
                    name="col1",
                    type=glue.Schema.STRING
                )],
                data_format=glue.DataFormat.CSV
            )
        '''
        result = self._values.get("storage_parameters")
        return typing.cast(typing.Optional[typing.List[StorageParameter]], result)

    @builtins.property
    def stored_as_sub_directories(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the table data is stored in subdirectories.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stored_as_sub_directories")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the table.

        :default: - generated by CDK.

        :stability: experimental
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.TableEncryption")
class TableEncryption(enum.Enum):
    '''(experimental) Encryption options for a Table.

    :see: https://docs.aws.amazon.com/athena/latest/ug/encryption.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_database: glue.Database
        
        glue.S3Table(self, "MyTable",
            encryption=glue.TableEncryption.S3_MANAGED,
            # ...
            database=my_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            data_format=glue.DataFormat.JSON
        )
    '''

    S3_MANAGED = "S3_MANAGED"
    '''(experimental) Server side encryption (SSE) with an Amazon S3-managed key.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingServerSideEncryption.html
    :stability: experimental
    '''
    KMS = "KMS"
    '''(experimental) Server-side encryption (SSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingKMSEncryption.html
    :stability: experimental
    '''
    KMS_MANAGED = "KMS_MANAGED"
    '''(experimental) Server-side encryption (SSE) with an AWS KMS key managed by the KMS service.

    :stability: experimental
    '''
    CLIENT_SIDE_KMS = "CLIENT_SIDE_KMS"
    '''(experimental) Client-side encryption (CSE) with an AWS KMS key managed by the account owner.

    :see: https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.Type",
    jsii_struct_bases=[],
    name_mapping={"input_string": "inputString", "is_primitive": "isPrimitive"},
)
class Type:
    def __init__(
        self,
        *,
        input_string: builtins.str,
        is_primitive: builtins.bool,
    ) -> None:
        '''(experimental) Represents a type of a column in a table schema.

        :param input_string: (experimental) Glue InputString for this type.
        :param is_primitive: (experimental) Indicates whether this type is a primitive data type.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_database: glue.Database
            
            glue.S3Table(self, "MyTable",
                database=my_database,
                columns=[glue.Column(
                    name="col1",
                    type=glue.Schema.STRING
                )],
                partition_keys=[glue.Column(
                    name="year",
                    type=glue.Schema.SMALL_INT
                ), glue.Column(
                    name="month",
                    type=glue.Schema.SMALL_INT
                )],
                data_format=glue.DataFormat.JSON
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5fb0ad30c447263aceddf4b77f71aec991966bf6e2dc3a181ff400914c16d85)
            check_type(argname="argument input_string", value=input_string, expected_type=type_hints["input_string"])
            check_type(argname="argument is_primitive", value=is_primitive, expected_type=type_hints["is_primitive"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_string": input_string,
            "is_primitive": is_primitive,
        }

    @builtins.property
    def input_string(self) -> builtins.str:
        '''(experimental) Glue InputString for this type.

        :stability: experimental
        '''
        result = self._values.get("input_string")
        assert result is not None, "Required property 'input_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def is_primitive(self) -> builtins.bool:
        '''(experimental) Indicates whether this type is a primitive data type.

        :stability: experimental
        '''
        result = self._values.get("is_primitive")
        assert result is not None, "Required property 'is_primitive' is missing"
        return typing.cast(builtins.bool, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Type(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkerType(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.WorkerType",
):
    '''(experimental) The type of predefined worker that is allocated when a job runs.

    If you need to use a WorkerType that doesn't exist as a static member, you
    can instantiate a ``WorkerType`` object, e.g: ``WorkerType.of('other type')``.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # bucket: s3.Bucket
        
        glue.Job(self, "ScalaSparkEtlJob",
            executable=glue.JobExecutable.scala_etl(
                glue_version=glue.GlueVersion.V4_0,
                script=glue.Code.from_bucket(bucket, "src/com/example/HelloWorld.scala"),
                class_name="com.example.HelloWorld",
                extra_jars=[glue.Code.from_bucket(bucket, "jars/HelloWorld.jar")]
            ),
            worker_type=glue.WorkerType.G_8X,
            description="an example Scala ETL job"
        )
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, worker_type: builtins.str) -> "WorkerType":
        '''(experimental) Custom worker type.

        :param worker_type: custom worker type.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217f80c6bee3c0db54c77a2a2bd0aa17178f371ff924355e6d6d4576a10d15c0)
            check_type(argname="argument worker_type", value=worker_type, expected_type=type_hints["worker_type"])
        return typing.cast("WorkerType", jsii.sinvoke(cls, "of", [worker_type]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="G_025X")
    def G_025_X(cls) -> "WorkerType":
        '''(experimental) Each worker maps to 0.25 DPU (2 vCPU, 4 GB of memory, 64 GB disk), and provides 1 executor per worker. Suitable for low volume streaming jobs.

        :stability: experimental
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "G_025X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="G_1X")
    def G_1_X(cls) -> "WorkerType":
        '''(experimental) Each worker maps to 1 DPU (4 vCPU, 16 GB of memory, 64 GB disk), and provides 1 executor per worker.

        Suitable for memory-intensive jobs.

        :stability: experimental
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "G_1X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="G_2X")
    def G_2_X(cls) -> "WorkerType":
        '''(experimental) Each worker maps to 2 DPU (8 vCPU, 32 GB of memory, 128 GB disk), and provides 1 executor per worker.

        Suitable for memory-intensive jobs.

        :stability: experimental
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "G_2X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="G_4X")
    def G_4_X(cls) -> "WorkerType":
        '''(experimental) Each worker maps to 4 DPU (16 vCPU, 64 GB of memory, 256 GB disk), and provides 1 executor per worker.

        We recommend this worker type for jobs whose workloads contain your most demanding transforms, aggregations, joins, and queries. This worker type is available only for AWS Glue version 3.0 or later jobs.

        :stability: experimental
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "G_4X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="G_8X")
    def G_8_X(cls) -> "WorkerType":
        '''(experimental) Each worker maps to 8 DPU (32 vCPU, 128 GB of memory, 512 GB disk), and provides 1 executor per worker.

        We recommend this worker type for jobs whose workloads contain your most demanding transforms, aggregations, joins, and queries. This worker type is available only for AWS Glue version 3.0 or later jobs.

        :stability: experimental
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "G_8X"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="STANDARD")
    def STANDARD(cls) -> "WorkerType":
        '''(experimental) Each worker provides 4 vCPU, 16 GB of memory and a 50GB disk, and 2 executors per worker.

        :stability: experimental
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "STANDARD"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="Z_2X")
    def Z_2_X(cls) -> "WorkerType":
        '''(experimental) Each worker maps to 2 high-memory DPU [M-DPU] (8 vCPU, 64 GB of memory, 128 GB disk).

        Supported in Ray jobs.

        :stability: experimental
        '''
        return typing.cast("WorkerType", jsii.sget(cls, "Z_2X"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this WorkerType, as expected by Job resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.enum(jsii_type="@aws-cdk/aws-glue-alpha.WriteParallel")
class WriteParallel(enum.Enum):
    '''(experimental) Specifies how to handle data being loaded that exceeds the length of the data type defined for columns containing VARCHAR, CHAR, or string data.

    By default, Redshift Spectrum sets the value to null for data that exceeds the width of the column.

    :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"* > *"surplus_char_handling"*
    :stability: experimental
    '''

    ON = "ON"
    '''(experimental) Write data in parallel.

    :stability: experimental
    '''
    OFF = "OFF"
    '''(experimental) Write data serially.

    :stability: experimental
    '''


class AssetCode(
    Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.AssetCode",
):
    '''(experimental) Job Code from a local file.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_glue_alpha as glue_alpha
        import aws_cdk as cdk
        from aws_cdk import aws_iam as iam
        from aws_cdk import aws_kms as kms
        
        # docker_image: cdk.DockerImage
        # grantable: iam.IGrantable
        # key: kms.Key
        # local_bundling: cdk.ILocalBundling
        
        asset_code = glue_alpha.AssetCode("path",
            asset_hash="assetHash",
            asset_hash_type=cdk.AssetHashType.SOURCE,
            bundling=cdk.BundlingOptions(
                image=docker_image,
        
                # the properties below are optional
                bundling_file_access=cdk.BundlingFileAccess.VOLUME_COPY,
                command=["command"],
                entrypoint=["entrypoint"],
                environment={
                    "environment_key": "environment"
                },
                local=local_bundling,
                network="network",
                output_type=cdk.BundlingOutput.ARCHIVED,
                platform="platform",
                security_opt="securityOpt",
                user="user",
                volumes=[cdk.DockerVolume(
                    container_path="containerPath",
                    host_path="hostPath",
        
                    # the properties below are optional
                    consistency=cdk.DockerVolumeConsistency.CONSISTENT
                )],
                volumes_from=["volumesFrom"],
                working_directory="workingDirectory"
            ),
            deploy_time=False,
            exclude=["exclude"],
            follow_symlinks=cdk.SymlinkFollowMode.NEVER,
            ignore_mode=cdk.IgnoreMode.GLOB,
            readers=[grantable],
            source_kMSKey=key
        )
    '''

    def __init__(
        self,
        path: builtins.str,
        *,
        deploy_time: typing.Optional[builtins.bool] = None,
        readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
        source_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
        bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
        follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
        ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
    ) -> None:
        '''
        :param path: The path to the Code file.
        :param deploy_time: Whether or not the asset needs to exist beyond deployment time; i.e. are copied over to a different location and not needed afterwards. Setting this property to true has an impact on the lifecycle of the asset, because we will assume that it is safe to delete after the CloudFormation deployment succeeds. For example, Lambda Function assets are copied over to Lambda during deployment. Therefore, it is not necessary to store the asset in S3, so we consider those deployTime assets. Default: false
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_kms_key: The ARN of the KMS key used to encrypt the handler code. Default: - the default server-side encryption with Amazon S3 managed keys(SSE-S3) key will be used.
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container or a custom bundling provider. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise
        :param exclude: File paths matching the patterns will be excluded. See ``ignoreMode`` to set the matching behavior. Has no effect on Assets bundled using the ``bundling`` property. Default: - nothing is excluded
        :param follow_symlinks: A strategy for how to handle symlinks. Default: SymlinkFollowMode.NEVER
        :param ignore_mode: The ignore behavior to use for ``exclude`` patterns. Default: IgnoreMode.GLOB

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8659d1457c6b7393d9d7559014d5e5cf2fae91cdf81e1dcc8f010bdd5e6159d6)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        options = _aws_cdk_aws_s3_assets_ceddda9d.AssetOptions(
            deploy_time=deploy_time,
            readers=readers,
            source_kms_key=source_kms_key,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
            exclude=exclude,
            follow_symlinks=follow_symlinks,
            ignore_mode=ignore_mode,
        )

        jsii.create(self.__class__, self, [path, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _constructs_77d1e7e8.Construct,
        grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> CodeConfig:
        '''(experimental) Called when the Job is initialized to allow this object to bind.

        :param scope: -
        :param grantable: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02569161383966e61e7748be2a2760721daf0107762bdf02e3d7b51459e0adda)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument grantable", value=grantable, expected_type=type_hints["grantable"])
        return typing.cast(CodeConfig, jsii.invoke(self, "bind", [scope, grantable]))


@jsii.implements(IConnection)
class Connection(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.Connection",
):
    '''(experimental) An AWS Glue connection to a data source.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # security_group: ec2.SecurityGroup
        # subnet: ec2.Subnet
        
        glue.Connection(self, "MyConnection",
            type=glue.ConnectionType.NETWORK,
            # The security groups granting AWS Glue inbound access to the data source within the VPC
            security_groups=[security_group],
            # The VPC subnet which contains the data source
            subnet=subnet
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        type: ConnectionType,
        connection_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        match_criteria: typing.Optional[typing.Sequence[builtins.str]] = None,
        properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param type: (experimental) The type of the connection.
        :param connection_name: (experimental) The name of the connection. Default: cloudformation generated name
        :param description: (experimental) The description of the connection. Default: no description
        :param match_criteria: (experimental) A list of criteria that can be used in selecting this connection. This is useful for filtering the results of https://awscli.amazonaws.com/v2/documentation/api/latest/reference/glue/get-connections.html Default: no match criteria
        :param properties: (experimental) Key-Value pairs that define parameters for the connection. Default: empty properties
        :param security_groups: (experimental) The list of security groups needed to successfully make this connection e.g. to successfully connect to VPC. Default: no security group
        :param subnet: (experimental) The VPC subnet to connect to resources within a VPC. See more at https://docs.aws.amazon.com/glue/latest/dg/start-connecting.html. Default: no subnet

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e49faf739a72a3e5056a9506838a646b867a4b6b78cad2fc0eb56a8a3a4d314)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConnectionProps(
            type=type,
            connection_name=connection_name,
            description=description,
            match_criteria=match_criteria,
            properties=properties,
            security_groups=security_groups,
            subnet=subnet,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromConnectionArn")
    @builtins.classmethod
    def from_connection_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        connection_arn: builtins.str,
    ) -> IConnection:
        '''(experimental) Creates a Connection construct that represents an external connection.

        :param scope: The scope creating construct (usually ``this``).
        :param id: The construct's id.
        :param connection_arn: arn of external connection.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3a56fcf056a17ac1a36f3aeea6a054c7367495dbcff654385c491f79a8de6e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
        return typing.cast(IConnection, jsii.sinvoke(cls, "fromConnectionArn", [scope, id, connection_arn]))

    @jsii.member(jsii_name="fromConnectionName")
    @builtins.classmethod
    def from_connection_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        connection_name: builtins.str,
    ) -> IConnection:
        '''(experimental) Creates a Connection construct that represents an external connection.

        :param scope: The scope creating construct (usually ``this``).
        :param id: The construct's id.
        :param connection_name: name of external connection.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2376990bb2b0fdc1652696730260ad95accfa020e78a7421e67836ad9c49c867)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument connection_name", value=connection_name, expected_type=type_hints["connection_name"])
        return typing.cast(IConnection, jsii.sinvoke(cls, "fromConnectionName", [scope, id, connection_name]))

    @jsii.member(jsii_name="addProperty")
    def add_property(self, key: builtins.str, value: builtins.str) -> None:
        '''(experimental) Add additional connection parameters.

        :param key: parameter key.
        :param value: parameter value.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__664a10af42e73be7ad7fc6b49fd43b23cdb7750d16ad9c795923ec494e582778)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addProperty", [key, value]))

    @builtins.property
    @jsii.member(jsii_name="connectionArn")
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the connection.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionArn"))

    @builtins.property
    @jsii.member(jsii_name="connectionName")
    def connection_name(self) -> builtins.str:
        '''(experimental) The name of the connection.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectionName"))


@jsii.implements(IDataQualityRuleset)
class DataQualityRuleset(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.DataQualityRuleset",
):
    '''(experimental) A Glue Data Quality ruleset.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        glue.DataQualityRuleset(self, "MyDataQualityRuleset",
            client_token="client_token",
            description="description",
            ruleset_name="ruleset_name",
            ruleset_dqdl="ruleset_dqdl",
            tags={
                "key1": "value1",
                "key2": "value2"
            },
            target_table=glue.DataQualityTargetTable("database_name", "table_name")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ruleset_dqdl: builtins.str,
        target_table: DataQualityTargetTable,
        client_token: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        ruleset_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ruleset_dqdl: (experimental) The dqdl of the ruleset.
        :param target_table: (experimental) The target table of the ruleset.
        :param client_token: (experimental) The client token of the ruleset.
        :param description: (experimental) The description of the ruleset.
        :param ruleset_name: (experimental) The name of the ruleset. Default: cloudformation generated name
        :param tags: (experimental) Key-Value pairs that define tags for the ruleset. Default: empty tags

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e874ec3f48fcb87408229a566f69396601cc87f18c40fa5579a09664f117653)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DataQualityRulesetProps(
            ruleset_dqdl=ruleset_dqdl,
            target_table=target_table,
            client_token=client_token,
            description=description,
            ruleset_name=ruleset_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromRulesetArn")
    @builtins.classmethod
    def from_ruleset_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        ruleset_arn: builtins.str,
    ) -> IDataQualityRuleset:
        '''
        :param scope: -
        :param id: -
        :param ruleset_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f0037b4150747a57e755360c767a1a492219225586c5381f7515e9f8675b60)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ruleset_arn", value=ruleset_arn, expected_type=type_hints["ruleset_arn"])
        return typing.cast(IDataQualityRuleset, jsii.sinvoke(cls, "fromRulesetArn", [scope, id, ruleset_arn]))

    @jsii.member(jsii_name="fromRulesetName")
    @builtins.classmethod
    def from_ruleset_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        ruleset_name: builtins.str,
    ) -> IDataQualityRuleset:
        '''
        :param scope: -
        :param id: -
        :param ruleset_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73d686727005bdb9857f1aed58c7619b0390fa040ea2cf5eeef9e309883720e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ruleset_name", value=ruleset_name, expected_type=type_hints["ruleset_name"])
        return typing.cast(IDataQualityRuleset, jsii.sinvoke(cls, "fromRulesetName", [scope, id, ruleset_name]))

    @builtins.property
    @jsii.member(jsii_name="rulesetArn")
    def ruleset_arn(self) -> builtins.str:
        '''(experimental) ARN of this ruleset.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "rulesetArn"))

    @builtins.property
    @jsii.member(jsii_name="rulesetName")
    def ruleset_name(self) -> builtins.str:
        '''(experimental) Name of this ruleset.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "rulesetName"))


@jsii.implements(IDatabase)
class Database(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.Database",
):
    '''(experimental) A Glue database.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        from aws_cdk.aws_glue_alpha import S3Table, Database, DataFormat, Schema
        from aws_cdk.aws_lakeformation import CfnDataLakeSettings, CfnTag, CfnTagAssociation
        
        # stack: cdk.Stack
        # account_id: str
        
        
        tag_key = "aws"
        tag_values = ["dev"]
        
        database = Database(self, "Database")
        
        table = S3Table(self, "Table",
            database=database,
            columns=[Column(
                name="col1",
                type=Schema.STRING
            ), Column(
                name="col2",
                type=Schema.STRING
            )
            ],
            data_format=DataFormat.CSV
        )
        
        synthesizer = stack.synthesizer
        CfnDataLakeSettings(self, "DataLakeSettings",
            admins=[CfnDataLakeSettings.DataLakePrincipalProperty(
                data_lake_principal_identifier=stack.format_arn(
                    service="iam",
                    resource="role",
                    region="",
                    account=account_id,
                    resource_name="Admin"
                )
            ), CfnDataLakeSettings.DataLakePrincipalProperty(
                # The CDK cloudformation execution role.
                data_lake_principal_identifier=synthesizer.cloud_formation_execution_role_arn.replace("${AWS::Partition}", "aws")
            )
            ]
        )
        
        tag = CfnTag(self, "Tag",
            catalog_id=account_id,
            tag_key=tag_key,
            tag_values=tag_values
        )
        
        lf_tag_pair_property = CfnTagAssociation.LFTagPairProperty(
            catalog_id=account_id,
            tag_key=tag_key,
            tag_values=tag_values
        )
        
        tag_association = CfnTagAssociation(self, "TagAssociation",
            lf_tags=[lf_tag_pair_property],
            resource=CfnTagAssociation.ResourceProperty(
                table_with_columns=CfnTagAssociation.TableWithColumnsResourceProperty(
                    database_name=database.database_name,
                    column_names=["col1", "col2"],
                    catalog_id=account_id,
                    name=table.table_name
                )
            )
        )
        
        tag_association.node.add_dependency(tag)
        tag_association.node.add_dependency(table)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        database_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        location_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param database_name: (experimental) The name of the database. Default: - generated by CDK.
        :param description: (experimental) A description of the database. Default: - no database description
        :param location_uri: (experimental) The location of the database (for example, an HDFS path). Default: undefined. This field is optional in AWS::Glue::Database DatabaseInput

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f4b410df1b0bf1116ce03c0e8a707776efd2f03da87fd718bf64b6a4964b2cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DatabaseProps(
            database_name=database_name,
            description=description,
            location_uri=location_uri,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseArn")
    @builtins.classmethod
    def from_database_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        database_arn: builtins.str,
    ) -> IDatabase:
        '''
        :param scope: -
        :param id: -
        :param database_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b20be4513bbaa9c562fcfb165fa327a8e6c6d38a0b15481eca8493b9b5a7b8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument database_arn", value=database_arn, expected_type=type_hints["database_arn"])
        return typing.cast(IDatabase, jsii.sinvoke(cls, "fromDatabaseArn", [scope, id, database_arn]))

    @builtins.property
    @jsii.member(jsii_name="catalogArn")
    def catalog_arn(self) -> builtins.str:
        '''(experimental) ARN of the Glue catalog in which this database is stored.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "catalogArn"))

    @builtins.property
    @jsii.member(jsii_name="catalogId")
    def catalog_id(self) -> builtins.str:
        '''(experimental) The catalog id of the database (usually, the AWS account id).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "catalogId"))

    @builtins.property
    @jsii.member(jsii_name="databaseArn")
    def database_arn(self) -> builtins.str:
        '''(experimental) ARN of this database.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseArn"))

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> builtins.str:
        '''(experimental) Name of this database.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "databaseName"))

    @builtins.property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) Location URI of this database.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationUri"))


class ExternalTable(
    TableBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.ExternalTable",
):
    '''(experimental) A Glue table that targets an external data location (e.g. A table in a Redshift Cluster).

    :stability: experimental
    :resource: AWS::Glue::Table
    :exampleMetadata: infused

    Example::

        # my_connection: glue.Connection
        # my_database: glue.Database
        
        glue.ExternalTable(self, "MyTable",
            connection=my_connection,
            external_data_location="default_db_public_example",  # A table in Redshift
            # ...
            database=my_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            data_format=glue.DataFormat.JSON
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        connection: IConnection,
        external_data_location: builtins.str,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
        database: IDatabase,
        data_format: DataFormat,
        compressed: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        enable_partition_filtering: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
        partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param connection: (experimental) The connection the table will use when performing reads and writes. Default: - No connection
        :param external_data_location: (experimental) The data source location of the glue table, (e.g. ``default_db_public_example`` for Redshift). If this property is set, it will override both ``bucket`` and ``s3Prefix``. Default: - No outsourced data source location
        :param columns: (experimental) Columns of the table.
        :param database: (experimental) Database in which to store the table.
        :param data_format: (experimental) Storage type of the table's data.
        :param compressed: (experimental) Indicates whether the table's data is compressed or not. Default: false
        :param description: (experimental) Description of the table. Default: generated
        :param enable_partition_filtering: (experimental) Enables partition filtering. Default: - The parameter is not defined
        :param parameters: (experimental) The key/value pairs define properties associated with the table. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Default: - The parameter is not defined
        :param partition_indexes: (experimental) Partition indexes on the table. A maximum of 3 indexes are allowed on a table. Keys in the index must be part of the table's partition keys. Default: table has no partition indexes
        :param partition_keys: (experimental) Partition columns of the table. Default: table is not partitioned
        :param storage_parameters: (experimental) The user-supplied properties for the description of the physical storage of this table. These properties help describe the format of the data that is stored within the crawled data sources. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property. Default: - The parameter is not defined
        :param stored_as_sub_directories: (experimental) Indicates whether the table data is stored in subdirectories. Default: false
        :param table_name: (experimental) Name of the table. Default: - generated by CDK.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b251bd575556272c98729ccada78c9d0fedbddd35e4e50ccd72649f6882227)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ExternalTableProps(
            connection=connection,
            external_data_location=external_data_location,
            columns=columns,
            database=database,
            data_format=data_format,
            compressed=compressed,
            description=description,
            enable_partition_filtering=enable_partition_filtering,
            parameters=parameters,
            partition_indexes=partition_indexes,
            partition_keys=partition_keys,
            storage_parameters=storage_parameters,
            stored_as_sub_directories=stored_as_sub_directories,
            table_name=table_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the table.

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c617ebeabae95be649f31192a1508ef254d5bb2a8f19540978e253877af7dc16)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read and write permissions to the table.

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d8e02b4ae2bce8590c80e2ce7a5829b237b1f08f6385cd6a8b926b701f8156b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadWrite", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant write permissions to the table.

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a161912810e7c25318614d340cf493d532bdbc1c20d5857baaa8e004b812df93)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> IConnection:
        '''(experimental) The connection associated to this table.

        :stability: experimental
        '''
        return typing.cast(IConnection, jsii.get(self, "connection"))

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''(experimental) ARN of this table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) Name of this table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="tableResource")
    def _table_resource(self) -> _aws_cdk_aws_glue_ceddda9d.CfnTable:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_glue_ceddda9d.CfnTable, jsii.get(self, "tableResource"))

    @builtins.property
    @jsii.member(jsii_name="partitionIndexes")
    def partition_indexes(self) -> typing.Optional[typing.List[PartitionIndex]]:
        '''(experimental) This table's partition indexes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[PartitionIndex]], jsii.get(self, "partitionIndexes"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.ExternalTableProps",
    jsii_struct_bases=[TableBaseProps],
    name_mapping={
        "columns": "columns",
        "database": "database",
        "data_format": "dataFormat",
        "compressed": "compressed",
        "description": "description",
        "enable_partition_filtering": "enablePartitionFiltering",
        "parameters": "parameters",
        "partition_indexes": "partitionIndexes",
        "partition_keys": "partitionKeys",
        "storage_parameters": "storageParameters",
        "stored_as_sub_directories": "storedAsSubDirectories",
        "table_name": "tableName",
        "connection": "connection",
        "external_data_location": "externalDataLocation",
    },
)
class ExternalTableProps(TableBaseProps):
    def __init__(
        self,
        *,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
        database: IDatabase,
        data_format: DataFormat,
        compressed: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        enable_partition_filtering: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
        partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        connection: IConnection,
        external_data_location: builtins.str,
    ) -> None:
        '''
        :param columns: (experimental) Columns of the table.
        :param database: (experimental) Database in which to store the table.
        :param data_format: (experimental) Storage type of the table's data.
        :param compressed: (experimental) Indicates whether the table's data is compressed or not. Default: false
        :param description: (experimental) Description of the table. Default: generated
        :param enable_partition_filtering: (experimental) Enables partition filtering. Default: - The parameter is not defined
        :param parameters: (experimental) The key/value pairs define properties associated with the table. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Default: - The parameter is not defined
        :param partition_indexes: (experimental) Partition indexes on the table. A maximum of 3 indexes are allowed on a table. Keys in the index must be part of the table's partition keys. Default: table has no partition indexes
        :param partition_keys: (experimental) Partition columns of the table. Default: table is not partitioned
        :param storage_parameters: (experimental) The user-supplied properties for the description of the physical storage of this table. These properties help describe the format of the data that is stored within the crawled data sources. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property. Default: - The parameter is not defined
        :param stored_as_sub_directories: (experimental) Indicates whether the table data is stored in subdirectories. Default: false
        :param table_name: (experimental) Name of the table. Default: - generated by CDK.
        :param connection: (experimental) The connection the table will use when performing reads and writes. Default: - No connection
        :param external_data_location: (experimental) The data source location of the glue table, (e.g. ``default_db_public_example`` for Redshift). If this property is set, it will override both ``bucket`` and ``s3Prefix``. Default: - No outsourced data source location

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_connection: glue.Connection
            # my_database: glue.Database
            
            glue.ExternalTable(self, "MyTable",
                connection=my_connection,
                external_data_location="default_db_public_example",  # A table in Redshift
                # ...
                database=my_database,
                columns=[glue.Column(
                    name="col1",
                    type=glue.Schema.STRING
                )],
                data_format=glue.DataFormat.JSON
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a91c342ce35e1b47ced3892e3796a41cbe78a15258e691c0f83319c7bc95c8f0)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument compressed", value=compressed, expected_type=type_hints["compressed"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_partition_filtering", value=enable_partition_filtering, expected_type=type_hints["enable_partition_filtering"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument partition_indexes", value=partition_indexes, expected_type=type_hints["partition_indexes"])
            check_type(argname="argument partition_keys", value=partition_keys, expected_type=type_hints["partition_keys"])
            check_type(argname="argument storage_parameters", value=storage_parameters, expected_type=type_hints["storage_parameters"])
            check_type(argname="argument stored_as_sub_directories", value=stored_as_sub_directories, expected_type=type_hints["stored_as_sub_directories"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument external_data_location", value=external_data_location, expected_type=type_hints["external_data_location"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "database": database,
            "data_format": data_format,
            "connection": connection,
            "external_data_location": external_data_location,
        }
        if compressed is not None:
            self._values["compressed"] = compressed
        if description is not None:
            self._values["description"] = description
        if enable_partition_filtering is not None:
            self._values["enable_partition_filtering"] = enable_partition_filtering
        if parameters is not None:
            self._values["parameters"] = parameters
        if partition_indexes is not None:
            self._values["partition_indexes"] = partition_indexes
        if partition_keys is not None:
            self._values["partition_keys"] = partition_keys
        if storage_parameters is not None:
            self._values["storage_parameters"] = storage_parameters
        if stored_as_sub_directories is not None:
            self._values["stored_as_sub_directories"] = stored_as_sub_directories
        if table_name is not None:
            self._values["table_name"] = table_name

    @builtins.property
    def columns(self) -> typing.List[Column]:
        '''(experimental) Columns of the table.

        :stability: experimental
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[Column], result)

    @builtins.property
    def database(self) -> IDatabase:
        '''(experimental) Database in which to store the table.

        :stability: experimental
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(IDatabase, result)

    @builtins.property
    def data_format(self) -> DataFormat:
        '''(experimental) Storage type of the table's data.

        :stability: experimental
        '''
        result = self._values.get("data_format")
        assert result is not None, "Required property 'data_format' is missing"
        return typing.cast(DataFormat, result)

    @builtins.property
    def compressed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the table's data is compressed or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("compressed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the table.

        :default: generated

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_partition_filtering(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables partition filtering.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/athena/latest/ug/glue-best-practices.html#glue-best-practices-partition-index
        :stability: experimental
        '''
        result = self._values.get("enable_partition_filtering")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The key/value pairs define properties associated with the table.

        The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def partition_indexes(self) -> typing.Optional[typing.List[PartitionIndex]]:
        '''(experimental) Partition indexes on the table.

        A maximum of 3 indexes
        are allowed on a table. Keys in the index must be part
        of the table's partition keys.

        :default: table has no partition indexes

        :stability: experimental
        '''
        result = self._values.get("partition_indexes")
        return typing.cast(typing.Optional[typing.List[PartitionIndex]], result)

    @builtins.property
    def partition_keys(self) -> typing.Optional[typing.List[Column]]:
        '''(experimental) Partition columns of the table.

        :default: table is not partitioned

        :stability: experimental
        '''
        result = self._values.get("partition_keys")
        return typing.cast(typing.Optional[typing.List[Column]], result)

    @builtins.property
    def storage_parameters(self) -> typing.Optional[typing.List[StorageParameter]]:
        '''(experimental) The user-supplied properties for the description of the physical storage of this table.

        These properties help describe the format of the data that is stored within the crawled data sources.

        The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed.

        Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"*
        :stability: experimental

        Example::

            # glue_database: glue.IDatabase
            
            table = glue.Table(self, "Table",
                storage_parameters=[
                    glue.StorageParameter.skip_header_line_count(1),
                    glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
                    glue.StorageParameter.custom("foo", "bar"),  # Will have no effect
                    glue.StorageParameter.custom("separatorChar", ","),  # Will describe the separator char used in the data
                    glue.StorageParameter.custom(glue.StorageParameters.WRITE_PARALLEL, "off")
                ],
                # ...
                database=glue_database,
                columns=[glue.Column(
                    name="col1",
                    type=glue.Schema.STRING
                )],
                data_format=glue.DataFormat.CSV
            )
        '''
        result = self._values.get("storage_parameters")
        return typing.cast(typing.Optional[typing.List[StorageParameter]], result)

    @builtins.property
    def stored_as_sub_directories(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the table data is stored in subdirectories.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stored_as_sub_directories")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the table.

        :default: - generated by CDK.

        :stability: experimental
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection(self) -> IConnection:
        '''(experimental) The connection the table will use when performing reads and writes.

        :default: - No connection

        :stability: experimental
        '''
        result = self._values.get("connection")
        assert result is not None, "Required property 'connection' is missing"
        return typing.cast(IConnection, result)

    @builtins.property
    def external_data_location(self) -> builtins.str:
        '''(experimental) The data source location of the glue table, (e.g. ``default_db_public_example`` for Redshift).

        If this property is set, it will override both ``bucket`` and ``s3Prefix``.

        :default: - No outsourced data source location

        :stability: experimental
        '''
        result = self._values.get("external_data_location")
        assert result is not None, "Required property 'external_data_location' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalTableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class S3Table(
    TableBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.S3Table",
):
    '''(experimental) A Glue table that targets a S3 dataset.

    :stability: experimental
    :resource: AWS::Glue::Table
    :exampleMetadata: infused

    Example::

        # my_database: glue.Database
        
        glue.S3Table(self, "MyTable",
            database=my_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            partition_keys=[glue.Column(
                name="year",
                type=glue.Schema.SMALL_INT
            ), glue.Column(
                name="month",
                type=glue.Schema.SMALL_INT
            )],
            data_format=glue.DataFormat.JSON,
            enable_partition_filtering=True
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        encryption: typing.Optional[TableEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
        database: IDatabase,
        data_format: DataFormat,
        compressed: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        enable_partition_filtering: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
        partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: (experimental) S3 bucket in which to store data. Default: one is created for you
        :param encryption: (experimental) The kind of encryption to secure the data with. You can only provide this option if you are not explicitly passing in a bucket. If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``. If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``. Default: BucketEncryption.S3_MANAGED
        :param encryption_key: (experimental) External KMS key to use for bucket encryption. The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``. Default: key is managed by KMS.
        :param s3_prefix: (experimental) S3 prefix under which table objects are stored. Default: - No prefix. The data will be stored under the root of the bucket.
        :param columns: (experimental) Columns of the table.
        :param database: (experimental) Database in which to store the table.
        :param data_format: (experimental) Storage type of the table's data.
        :param compressed: (experimental) Indicates whether the table's data is compressed or not. Default: false
        :param description: (experimental) Description of the table. Default: generated
        :param enable_partition_filtering: (experimental) Enables partition filtering. Default: - The parameter is not defined
        :param parameters: (experimental) The key/value pairs define properties associated with the table. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Default: - The parameter is not defined
        :param partition_indexes: (experimental) Partition indexes on the table. A maximum of 3 indexes are allowed on a table. Keys in the index must be part of the table's partition keys. Default: table has no partition indexes
        :param partition_keys: (experimental) Partition columns of the table. Default: table is not partitioned
        :param storage_parameters: (experimental) The user-supplied properties for the description of the physical storage of this table. These properties help describe the format of the data that is stored within the crawled data sources. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property. Default: - The parameter is not defined
        :param stored_as_sub_directories: (experimental) Indicates whether the table data is stored in subdirectories. Default: false
        :param table_name: (experimental) Name of the table. Default: - generated by CDK.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b5cd7a8c51600d473f125b7e52d34d32dba95265780e87640a28f30e73ce95d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3TableProps(
            bucket=bucket,
            encryption=encryption,
            encryption_key=encryption_key,
            s3_prefix=s3_prefix,
            columns=columns,
            database=database,
            data_format=data_format,
            compressed=compressed,
            description=description,
            enable_partition_filtering=enable_partition_filtering,
            parameters=parameters,
            partition_indexes=partition_indexes,
            partition_keys=partition_keys,
            storage_parameters=storage_parameters,
            stored_as_sub_directories=stored_as_sub_directories,
            table_name=table_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="generateS3PrefixForGrant")
    def _generate_s3_prefix_for_grant(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "generateS3PrefixForGrant", []))

    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read permissions to the table and the underlying data stored in S3 to an IAM principal.

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3909b8e18b4eb038d1349092a370f0791a90c6e7f8380b7439f83993e01d04f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @jsii.member(jsii_name="grantReadWrite")
    def grant_read_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant read and write permissions to the table and the underlying data stored in S3 to an IAM principal.

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7a94485fcfc5ef062186c7655669b475fac2ccac917edd1bd396de160cd227)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadWrite", [grantee]))

    @jsii.member(jsii_name="grantWrite")
    def grant_write(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grant write permissions to the table and the underlying data stored in S3 to an IAM principal.

        :param grantee: the principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea067213729fc1f1f124734239ce0d21ea4e77d3fecd8d14ab5363d59122770b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWrite", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''(experimental) S3 bucket in which the table's data resides.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, jsii.get(self, "bucket"))

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(self) -> TableEncryption:
        '''(experimental) The type of encryption enabled for the table.

        :stability: experimental
        '''
        return typing.cast(TableEncryption, jsii.get(self, "encryption"))

    @builtins.property
    @jsii.member(jsii_name="s3Prefix")
    def s3_prefix(self) -> builtins.str:
        '''(experimental) S3 Key Prefix under which this table's files are stored in S3.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "s3Prefix"))

    @builtins.property
    @jsii.member(jsii_name="tableArn")
    def table_arn(self) -> builtins.str:
        '''(experimental) ARN of this table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableArn"))

    @builtins.property
    @jsii.member(jsii_name="tableName")
    def table_name(self) -> builtins.str:
        '''(experimental) Name of this table.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "tableName"))

    @builtins.property
    @jsii.member(jsii_name="tableResource")
    def _table_resource(self) -> _aws_cdk_aws_glue_ceddda9d.CfnTable:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_glue_ceddda9d.CfnTable, jsii.get(self, "tableResource"))

    @builtins.property
    @jsii.member(jsii_name="encryptionKey")
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) The KMS key used to secure the data if ``encryption`` is set to ``CSE-KMS`` or ``SSE-KMS``.

        Otherwise, ``undefined``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "encryptionKey"))

    @builtins.property
    @jsii.member(jsii_name="partitionIndexes")
    def partition_indexes(self) -> typing.Optional[typing.List[PartitionIndex]]:
        '''(experimental) This table's partition indexes.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[PartitionIndex]], jsii.get(self, "partitionIndexes"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.S3TableProps",
    jsii_struct_bases=[TableBaseProps],
    name_mapping={
        "columns": "columns",
        "database": "database",
        "data_format": "dataFormat",
        "compressed": "compressed",
        "description": "description",
        "enable_partition_filtering": "enablePartitionFiltering",
        "parameters": "parameters",
        "partition_indexes": "partitionIndexes",
        "partition_keys": "partitionKeys",
        "storage_parameters": "storageParameters",
        "stored_as_sub_directories": "storedAsSubDirectories",
        "table_name": "tableName",
        "bucket": "bucket",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "s3_prefix": "s3Prefix",
    },
)
class S3TableProps(TableBaseProps):
    def __init__(
        self,
        *,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
        database: IDatabase,
        data_format: DataFormat,
        compressed: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        enable_partition_filtering: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
        partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        encryption: typing.Optional[TableEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param columns: (experimental) Columns of the table.
        :param database: (experimental) Database in which to store the table.
        :param data_format: (experimental) Storage type of the table's data.
        :param compressed: (experimental) Indicates whether the table's data is compressed or not. Default: false
        :param description: (experimental) Description of the table. Default: generated
        :param enable_partition_filtering: (experimental) Enables partition filtering. Default: - The parameter is not defined
        :param parameters: (experimental) The key/value pairs define properties associated with the table. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Default: - The parameter is not defined
        :param partition_indexes: (experimental) Partition indexes on the table. A maximum of 3 indexes are allowed on a table. Keys in the index must be part of the table's partition keys. Default: table has no partition indexes
        :param partition_keys: (experimental) Partition columns of the table. Default: table is not partitioned
        :param storage_parameters: (experimental) The user-supplied properties for the description of the physical storage of this table. These properties help describe the format of the data that is stored within the crawled data sources. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property. Default: - The parameter is not defined
        :param stored_as_sub_directories: (experimental) Indicates whether the table data is stored in subdirectories. Default: false
        :param table_name: (experimental) Name of the table. Default: - generated by CDK.
        :param bucket: (experimental) S3 bucket in which to store data. Default: one is created for you
        :param encryption: (experimental) The kind of encryption to secure the data with. You can only provide this option if you are not explicitly passing in a bucket. If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``. If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``. Default: BucketEncryption.S3_MANAGED
        :param encryption_key: (experimental) External KMS key to use for bucket encryption. The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``. Default: key is managed by KMS.
        :param s3_prefix: (experimental) S3 prefix under which table objects are stored. Default: - No prefix. The data will be stored under the root of the bucket.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_database: glue.Database
            
            glue.S3Table(self, "MyTable",
                database=my_database,
                columns=[glue.Column(
                    name="col1",
                    type=glue.Schema.STRING
                )],
                partition_keys=[glue.Column(
                    name="year",
                    type=glue.Schema.SMALL_INT
                ), glue.Column(
                    name="month",
                    type=glue.Schema.SMALL_INT
                )],
                data_format=glue.DataFormat.JSON,
                enable_partition_filtering=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a30697598fc2a32c5e111aebc024dd5935b49f4f1807d70f75c9a4e8bff8268)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument compressed", value=compressed, expected_type=type_hints["compressed"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_partition_filtering", value=enable_partition_filtering, expected_type=type_hints["enable_partition_filtering"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument partition_indexes", value=partition_indexes, expected_type=type_hints["partition_indexes"])
            check_type(argname="argument partition_keys", value=partition_keys, expected_type=type_hints["partition_keys"])
            check_type(argname="argument storage_parameters", value=storage_parameters, expected_type=type_hints["storage_parameters"])
            check_type(argname="argument stored_as_sub_directories", value=stored_as_sub_directories, expected_type=type_hints["stored_as_sub_directories"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "database": database,
            "data_format": data_format,
        }
        if compressed is not None:
            self._values["compressed"] = compressed
        if description is not None:
            self._values["description"] = description
        if enable_partition_filtering is not None:
            self._values["enable_partition_filtering"] = enable_partition_filtering
        if parameters is not None:
            self._values["parameters"] = parameters
        if partition_indexes is not None:
            self._values["partition_indexes"] = partition_indexes
        if partition_keys is not None:
            self._values["partition_keys"] = partition_keys
        if storage_parameters is not None:
            self._values["storage_parameters"] = storage_parameters
        if stored_as_sub_directories is not None:
            self._values["stored_as_sub_directories"] = stored_as_sub_directories
        if table_name is not None:
            self._values["table_name"] = table_name
        if bucket is not None:
            self._values["bucket"] = bucket
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def columns(self) -> typing.List[Column]:
        '''(experimental) Columns of the table.

        :stability: experimental
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[Column], result)

    @builtins.property
    def database(self) -> IDatabase:
        '''(experimental) Database in which to store the table.

        :stability: experimental
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(IDatabase, result)

    @builtins.property
    def data_format(self) -> DataFormat:
        '''(experimental) Storage type of the table's data.

        :stability: experimental
        '''
        result = self._values.get("data_format")
        assert result is not None, "Required property 'data_format' is missing"
        return typing.cast(DataFormat, result)

    @builtins.property
    def compressed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the table's data is compressed or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("compressed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the table.

        :default: generated

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_partition_filtering(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables partition filtering.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/athena/latest/ug/glue-best-practices.html#glue-best-practices-partition-index
        :stability: experimental
        '''
        result = self._values.get("enable_partition_filtering")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The key/value pairs define properties associated with the table.

        The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def partition_indexes(self) -> typing.Optional[typing.List[PartitionIndex]]:
        '''(experimental) Partition indexes on the table.

        A maximum of 3 indexes
        are allowed on a table. Keys in the index must be part
        of the table's partition keys.

        :default: table has no partition indexes

        :stability: experimental
        '''
        result = self._values.get("partition_indexes")
        return typing.cast(typing.Optional[typing.List[PartitionIndex]], result)

    @builtins.property
    def partition_keys(self) -> typing.Optional[typing.List[Column]]:
        '''(experimental) Partition columns of the table.

        :default: table is not partitioned

        :stability: experimental
        '''
        result = self._values.get("partition_keys")
        return typing.cast(typing.Optional[typing.List[Column]], result)

    @builtins.property
    def storage_parameters(self) -> typing.Optional[typing.List[StorageParameter]]:
        '''(experimental) The user-supplied properties for the description of the physical storage of this table.

        These properties help describe the format of the data that is stored within the crawled data sources.

        The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed.

        Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"*
        :stability: experimental

        Example::

            # glue_database: glue.IDatabase
            
            table = glue.Table(self, "Table",
                storage_parameters=[
                    glue.StorageParameter.skip_header_line_count(1),
                    glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
                    glue.StorageParameter.custom("foo", "bar"),  # Will have no effect
                    glue.StorageParameter.custom("separatorChar", ","),  # Will describe the separator char used in the data
                    glue.StorageParameter.custom(glue.StorageParameters.WRITE_PARALLEL, "off")
                ],
                # ...
                database=glue_database,
                columns=[glue.Column(
                    name="col1",
                    type=glue.Schema.STRING
                )],
                data_format=glue.DataFormat.CSV
            )
        '''
        result = self._values.get("storage_parameters")
        return typing.cast(typing.Optional[typing.List[StorageParameter]], result)

    @builtins.property
    def stored_as_sub_directories(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the table data is stored in subdirectories.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stored_as_sub_directories")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the table.

        :default: - generated by CDK.

        :stability: experimental
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''(experimental) S3 bucket in which to store data.

        :default: one is created for you

        :stability: experimental
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def encryption(self) -> typing.Optional[TableEncryption]:
        '''(experimental) The kind of encryption to secure the data with.

        You can only provide this option if you are not explicitly passing in a bucket.

        If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``.
        If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``.

        :default: BucketEncryption.S3_MANAGED

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[TableEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) External KMS key to use for bucket encryption.

        The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``.

        :default: key is managed by KMS.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) S3 prefix under which table objects are stored.

        :default: - No prefix. The data will be stored under the root of the bucket.

        :stability: experimental
        '''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3TableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Table(
    S3Table,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-glue-alpha.Table",
):
    '''(deprecated) A Glue table.

    :deprecated: Use {@link S3Table } instead.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        # glue_database: glue.IDatabase
        
        table = glue.Table(self, "Table",
            storage_parameters=[
                glue.StorageParameter.skip_header_line_count(1),
                glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
                glue.StorageParameter.custom("foo", "bar"),  # Will have no effect
                glue.StorageParameter.custom("separatorChar", ","),  # Will describe the separator char used in the data
                glue.StorageParameter.custom(glue.StorageParameters.WRITE_PARALLEL, "off")
            ],
            # ...
            database=glue_database,
            columns=[glue.Column(
                name="col1",
                type=glue.Schema.STRING
            )],
            data_format=glue.DataFormat.CSV
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        encryption: typing.Optional[TableEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
        database: IDatabase,
        data_format: DataFormat,
        compressed: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        enable_partition_filtering: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
        partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket: (experimental) S3 bucket in which to store data. Default: one is created for you
        :param encryption: (experimental) The kind of encryption to secure the data with. You can only provide this option if you are not explicitly passing in a bucket. If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``. If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``. Default: BucketEncryption.S3_MANAGED
        :param encryption_key: (experimental) External KMS key to use for bucket encryption. The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``. Default: key is managed by KMS.
        :param s3_prefix: (experimental) S3 prefix under which table objects are stored. Default: - No prefix. The data will be stored under the root of the bucket.
        :param columns: (experimental) Columns of the table.
        :param database: (experimental) Database in which to store the table.
        :param data_format: (experimental) Storage type of the table's data.
        :param compressed: (experimental) Indicates whether the table's data is compressed or not. Default: false
        :param description: (experimental) Description of the table. Default: generated
        :param enable_partition_filtering: (experimental) Enables partition filtering. Default: - The parameter is not defined
        :param parameters: (experimental) The key/value pairs define properties associated with the table. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Default: - The parameter is not defined
        :param partition_indexes: (experimental) Partition indexes on the table. A maximum of 3 indexes are allowed on a table. Keys in the index must be part of the table's partition keys. Default: table has no partition indexes
        :param partition_keys: (experimental) Partition columns of the table. Default: table is not partitioned
        :param storage_parameters: (experimental) The user-supplied properties for the description of the physical storage of this table. These properties help describe the format of the data that is stored within the crawled data sources. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property. Default: - The parameter is not defined
        :param stored_as_sub_directories: (experimental) Indicates whether the table data is stored in subdirectories. Default: false
        :param table_name: (experimental) Name of the table. Default: - generated by CDK.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1146b20665153f742431bb500cb6e71362a22d8446ea9e132183e7be255411a3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = S3TableProps(
            bucket=bucket,
            encryption=encryption,
            encryption_key=encryption_key,
            s3_prefix=s3_prefix,
            columns=columns,
            database=database,
            data_format=data_format,
            compressed=compressed,
            description=description,
            enable_partition_filtering=enable_partition_filtering,
            parameters=parameters,
            partition_indexes=partition_indexes,
            partition_keys=partition_keys,
            storage_parameters=storage_parameters,
            stored_as_sub_directories=stored_as_sub_directories,
            table_name=table_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-glue-alpha.TableProps",
    jsii_struct_bases=[S3TableProps],
    name_mapping={
        "columns": "columns",
        "database": "database",
        "data_format": "dataFormat",
        "compressed": "compressed",
        "description": "description",
        "enable_partition_filtering": "enablePartitionFiltering",
        "parameters": "parameters",
        "partition_indexes": "partitionIndexes",
        "partition_keys": "partitionKeys",
        "storage_parameters": "storageParameters",
        "stored_as_sub_directories": "storedAsSubDirectories",
        "table_name": "tableName",
        "bucket": "bucket",
        "encryption": "encryption",
        "encryption_key": "encryptionKey",
        "s3_prefix": "s3Prefix",
    },
)
class TableProps(S3TableProps):
    def __init__(
        self,
        *,
        columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
        database: IDatabase,
        data_format: DataFormat,
        compressed: typing.Optional[builtins.bool] = None,
        description: typing.Optional[builtins.str] = None,
        enable_partition_filtering: typing.Optional[builtins.bool] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
        partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
        storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
        stored_as_sub_directories: typing.Optional[builtins.bool] = None,
        table_name: typing.Optional[builtins.str] = None,
        bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        encryption: typing.Optional[TableEncryption] = None,
        encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        s3_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param columns: (experimental) Columns of the table.
        :param database: (experimental) Database in which to store the table.
        :param data_format: (experimental) Storage type of the table's data.
        :param compressed: (experimental) Indicates whether the table's data is compressed or not. Default: false
        :param description: (experimental) Description of the table. Default: generated
        :param enable_partition_filtering: (experimental) Enables partition filtering. Default: - The parameter is not defined
        :param parameters: (experimental) The key/value pairs define properties associated with the table. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Default: - The parameter is not defined
        :param partition_indexes: (experimental) Partition indexes on the table. A maximum of 3 indexes are allowed on a table. Keys in the index must be part of the table's partition keys. Default: table has no partition indexes
        :param partition_keys: (experimental) Partition columns of the table. Default: table is not partitioned
        :param storage_parameters: (experimental) The user-supplied properties for the description of the physical storage of this table. These properties help describe the format of the data that is stored within the crawled data sources. The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed. Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property. Default: - The parameter is not defined
        :param stored_as_sub_directories: (experimental) Indicates whether the table data is stored in subdirectories. Default: false
        :param table_name: (experimental) Name of the table. Default: - generated by CDK.
        :param bucket: (experimental) S3 bucket in which to store data. Default: one is created for you
        :param encryption: (experimental) The kind of encryption to secure the data with. You can only provide this option if you are not explicitly passing in a bucket. If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``. If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``. Default: BucketEncryption.S3_MANAGED
        :param encryption_key: (experimental) External KMS key to use for bucket encryption. The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``. Default: key is managed by KMS.
        :param s3_prefix: (experimental) S3 prefix under which table objects are stored. Default: - No prefix. The data will be stored under the root of the bucket.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_glue_alpha as glue_alpha
            from aws_cdk import aws_kms as kms
            from aws_cdk import aws_s3 as s3
            
            # bucket: s3.Bucket
            # database: glue_alpha.Database
            # data_format: glue_alpha.DataFormat
            # key: kms.Key
            # storage_parameter: glue_alpha.StorageParameter
            
            table_props = glue_alpha.TableProps(
                columns=[glue_alpha.Column(
                    name="name",
                    type=glue_alpha.Type(
                        input_string="inputString",
                        is_primitive=False
                    ),
            
                    # the properties below are optional
                    comment="comment"
                )],
                database=database,
                data_format=data_format,
            
                # the properties below are optional
                bucket=bucket,
                compressed=False,
                description="description",
                enable_partition_filtering=False,
                encryption=glue_alpha.TableEncryption.S3_MANAGED,
                encryption_key=key,
                parameters={
                    "parameters_key": "parameters"
                },
                partition_indexes=[glue_alpha.PartitionIndex(
                    key_names=["keyNames"],
            
                    # the properties below are optional
                    index_name="indexName"
                )],
                partition_keys=[glue_alpha.Column(
                    name="name",
                    type=glue_alpha.Type(
                        input_string="inputString",
                        is_primitive=False
                    ),
            
                    # the properties below are optional
                    comment="comment"
                )],
                s3_prefix="s3Prefix",
                storage_parameters=[storage_parameter],
                stored_as_sub_directories=False,
                table_name="tableName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0336d5abace2b9645857eae2fba5aa1c4bbb0db1762c5d5031d2f8c64019d606)
            check_type(argname="argument columns", value=columns, expected_type=type_hints["columns"])
            check_type(argname="argument database", value=database, expected_type=type_hints["database"])
            check_type(argname="argument data_format", value=data_format, expected_type=type_hints["data_format"])
            check_type(argname="argument compressed", value=compressed, expected_type=type_hints["compressed"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_partition_filtering", value=enable_partition_filtering, expected_type=type_hints["enable_partition_filtering"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument partition_indexes", value=partition_indexes, expected_type=type_hints["partition_indexes"])
            check_type(argname="argument partition_keys", value=partition_keys, expected_type=type_hints["partition_keys"])
            check_type(argname="argument storage_parameters", value=storage_parameters, expected_type=type_hints["storage_parameters"])
            check_type(argname="argument stored_as_sub_directories", value=stored_as_sub_directories, expected_type=type_hints["stored_as_sub_directories"])
            check_type(argname="argument table_name", value=table_name, expected_type=type_hints["table_name"])
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument s3_prefix", value=s3_prefix, expected_type=type_hints["s3_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "columns": columns,
            "database": database,
            "data_format": data_format,
        }
        if compressed is not None:
            self._values["compressed"] = compressed
        if description is not None:
            self._values["description"] = description
        if enable_partition_filtering is not None:
            self._values["enable_partition_filtering"] = enable_partition_filtering
        if parameters is not None:
            self._values["parameters"] = parameters
        if partition_indexes is not None:
            self._values["partition_indexes"] = partition_indexes
        if partition_keys is not None:
            self._values["partition_keys"] = partition_keys
        if storage_parameters is not None:
            self._values["storage_parameters"] = storage_parameters
        if stored_as_sub_directories is not None:
            self._values["stored_as_sub_directories"] = stored_as_sub_directories
        if table_name is not None:
            self._values["table_name"] = table_name
        if bucket is not None:
            self._values["bucket"] = bucket
        if encryption is not None:
            self._values["encryption"] = encryption
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if s3_prefix is not None:
            self._values["s3_prefix"] = s3_prefix

    @builtins.property
    def columns(self) -> typing.List[Column]:
        '''(experimental) Columns of the table.

        :stability: experimental
        '''
        result = self._values.get("columns")
        assert result is not None, "Required property 'columns' is missing"
        return typing.cast(typing.List[Column], result)

    @builtins.property
    def database(self) -> IDatabase:
        '''(experimental) Database in which to store the table.

        :stability: experimental
        '''
        result = self._values.get("database")
        assert result is not None, "Required property 'database' is missing"
        return typing.cast(IDatabase, result)

    @builtins.property
    def data_format(self) -> DataFormat:
        '''(experimental) Storage type of the table's data.

        :stability: experimental
        '''
        result = self._values.get("data_format")
        assert result is not None, "Required property 'data_format' is missing"
        return typing.cast(DataFormat, result)

    @builtins.property
    def compressed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the table's data is compressed or not.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("compressed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the table.

        :default: generated

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_partition_filtering(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables partition filtering.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/athena/latest/ug/glue-best-practices.html#glue-best-practices-partition-index
        :stability: experimental
        '''
        result = self._values.get("enable_partition_filtering")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The key/value pairs define properties associated with the table.

        The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-glue-table-tableinput.html#cfn-glue-table-tableinput-parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def partition_indexes(self) -> typing.Optional[typing.List[PartitionIndex]]:
        '''(experimental) Partition indexes on the table.

        A maximum of 3 indexes
        are allowed on a table. Keys in the index must be part
        of the table's partition keys.

        :default: table has no partition indexes

        :stability: experimental
        '''
        result = self._values.get("partition_indexes")
        return typing.cast(typing.Optional[typing.List[PartitionIndex]], result)

    @builtins.property
    def partition_keys(self) -> typing.Optional[typing.List[Column]]:
        '''(experimental) Partition columns of the table.

        :default: table is not partitioned

        :stability: experimental
        '''
        result = self._values.get("partition_keys")
        return typing.cast(typing.Optional[typing.List[Column]], result)

    @builtins.property
    def storage_parameters(self) -> typing.Optional[typing.List[StorageParameter]]:
        '''(experimental) The user-supplied properties for the description of the physical storage of this table.

        These properties help describe the format of the data that is stored within the crawled data sources.

        The key/value pairs that are allowed to be submitted are not limited, however their functionality is not guaranteed.

        Some keys will be auto-populated by glue crawlers, however, you can override them by specifying the key and value in this property.

        :default: - The parameter is not defined

        :see: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#r_CREATE_EXTERNAL_TABLE-parameters - under *"TABLE PROPERTIES"*
        :stability: experimental

        Example::

            # glue_database: glue.IDatabase
            
            table = glue.Table(self, "Table",
                storage_parameters=[
                    glue.StorageParameter.skip_header_line_count(1),
                    glue.StorageParameter.compression_type(glue.CompressionType.GZIP),
                    glue.StorageParameter.custom("foo", "bar"),  # Will have no effect
                    glue.StorageParameter.custom("separatorChar", ","),  # Will describe the separator char used in the data
                    glue.StorageParameter.custom(glue.StorageParameters.WRITE_PARALLEL, "off")
                ],
                # ...
                database=glue_database,
                columns=[glue.Column(
                    name="col1",
                    type=glue.Schema.STRING
                )],
                data_format=glue.DataFormat.CSV
            )
        '''
        result = self._values.get("storage_parameters")
        return typing.cast(typing.Optional[typing.List[StorageParameter]], result)

    @builtins.property
    def stored_as_sub_directories(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the table data is stored in subdirectories.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("stored_as_sub_directories")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def table_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the table.

        :default: - generated by CDK.

        :stability: experimental
        '''
        result = self._values.get("table_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''(experimental) S3 bucket in which to store data.

        :default: one is created for you

        :stability: experimental
        '''
        result = self._values.get("bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def encryption(self) -> typing.Optional[TableEncryption]:
        '''(experimental) The kind of encryption to secure the data with.

        You can only provide this option if you are not explicitly passing in a bucket.

        If you choose ``SSE-KMS``, you *can* provide an un-managed KMS key with ``encryptionKey``.
        If you choose ``CSE-KMS``, you *must* provide an un-managed KMS key with ``encryptionKey``.

        :default: BucketEncryption.S3_MANAGED

        :stability: experimental
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[TableEncryption], result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(experimental) External KMS key to use for bucket encryption.

        The ``encryption`` property must be ``SSE-KMS`` or ``CSE-KMS``.

        :default: key is managed by KMS.

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def s3_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) S3 prefix under which table objects are stored.

        :default: - No prefix. The data will be stored under the root of the bucket.

        :stability: experimental
        '''
        result = self._values.get("s3_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AssetCode",
    "ClassificationString",
    "CloudWatchEncryption",
    "CloudWatchEncryptionMode",
    "Code",
    "CodeConfig",
    "Column",
    "ColumnCountMismatchHandlingAction",
    "CompressionType",
    "Connection",
    "ConnectionOptions",
    "ConnectionProps",
    "ConnectionType",
    "ContinuousLoggingProps",
    "DataFormat",
    "DataFormatProps",
    "DataQualityRuleset",
    "DataQualityRulesetProps",
    "DataQualityTargetTable",
    "Database",
    "DatabaseProps",
    "ExecutionClass",
    "ExternalTable",
    "ExternalTableProps",
    "GlueVersion",
    "IConnection",
    "IDataQualityRuleset",
    "IDatabase",
    "IJob",
    "ISecurityConfiguration",
    "ITable",
    "InputFormat",
    "InvalidCharHandlingAction",
    "Job",
    "JobAttributes",
    "JobBookmarksEncryption",
    "JobBookmarksEncryptionMode",
    "JobExecutable",
    "JobExecutableConfig",
    "JobLanguage",
    "JobProps",
    "JobState",
    "JobType",
    "MetricType",
    "NumericOverflowHandlingAction",
    "OrcColumnMappingType",
    "OutputFormat",
    "PartitionIndex",
    "PythonRayExecutableProps",
    "PythonShellExecutableProps",
    "PythonSparkJobExecutableProps",
    "PythonVersion",
    "Runtime",
    "S3Code",
    "S3Encryption",
    "S3EncryptionMode",
    "S3Table",
    "S3TableProps",
    "ScalaJobExecutableProps",
    "Schema",
    "SecurityConfiguration",
    "SecurityConfigurationProps",
    "SerializationLibrary",
    "SparkUILoggingLocation",
    "SparkUIProps",
    "StorageParameter",
    "StorageParameters",
    "SurplusBytesHandlingAction",
    "SurplusCharHandlingAction",
    "Table",
    "TableAttributes",
    "TableBase",
    "TableBaseProps",
    "TableEncryption",
    "TableProps",
    "Type",
    "WorkerType",
    "WriteParallel",
]

publication.publish()

def _typecheckingstub__2bfce587a58c2deea97e71eeab8754a97692804f6d43271eda89c6257eaebdfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceec14d1d7029d8fb7df76e4abb14bc79250421d85a9584f0271d9e7c4f4ef3f(
    *,
    mode: CloudWatchEncryptionMode,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7e88ca82e81ea6700503f28d9e5352c4a86e264d00afb35e761e591a7e0e24(
    path: builtins.str,
    *,
    deploy_time: typing.Optional[builtins.bool] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
    source_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d23f6002340150960cebd70816482874d96a0de7d52265f1fcd0ab459eea2a61(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b88388256be44082f9ce622ac393616c31af36dc246d0cb6ea3eb8e78b31dc1(
    scope: _constructs_77d1e7e8.Construct,
    grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7667596ec33fb86df61ee9e5603a0bed57aa6e48e3795e84685966147e79b05e(
    *,
    s3_location: typing.Union[_aws_cdk_aws_s3_ceddda9d.Location, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__043c8b76c78332fa2f7a0e1444ad14734d788355c87767ffb0dd0aac9a19fbdf(
    *,
    name: builtins.str,
    type: typing.Union[Type, typing.Dict[builtins.str, typing.Any]],
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1670baf78db937cd3601a16badd87755f3fc525b8fd6a352d45c2bc3994b494(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    match_criteria: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fa037db6ada98c73a1d8889753f75c2f3c7513c8a41daf149dc5769cdb83e8(
    *,
    connection_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    match_criteria: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
    type: ConnectionType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1f57c94567ffb3d89cdd8c9cd2b37bd37decd390b53c9bfdadd569dc797aa3f(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6be4bb41017f52f2aa453e36400fa3a47b2e6bf3a87cf64d46e0345d6f22428b(
    *,
    enabled: builtins.bool,
    conversion_pattern: typing.Optional[builtins.str] = None,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    log_stream_prefix: typing.Optional[builtins.str] = None,
    quiet: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5302ed9f621270e44cf453ed62f78ee39e66f12961a87e084ec3d874438a19f(
    *,
    input_format: InputFormat,
    output_format: OutputFormat,
    serialization_library: SerializationLibrary,
    classification_string: typing.Optional[ClassificationString] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abda2570732c667a87dd412c9aa6c70d5db49ac0b525ecc9c3c801e1271e451a(
    *,
    ruleset_dqdl: builtins.str,
    target_table: DataQualityTargetTable,
    client_token: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    ruleset_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18073ec885df4d5126a63d11958df64b1c8b43f719ce0fd6c6c594b457b6d4af(
    database_name: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d07df31a9d41958f45422a1d7914c5016d66ed0e46a7e97ab37e2dd3d42ecf38(
    *,
    database_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    location_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf24e914c5a2058c5a8ba633944792fe46a62d0d67ae96056f15edaf764112b(
    version: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f8eb7ba0850dad06f49887b6323e6019fa48cdf967d96e579591ff36e61765(
    metric_name: builtins.str,
    type: MetricType,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e9bb641a392e36442ae2624591822707bc3af7603043bcb85c82e6dde0aedff(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__192bf1eecc268b3f759e65151917fb49666d5a0144c2df120f2dd72e3fd5e4f4(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bab9c989bad00c9e92013f90e2646073cc90125f09e75268ec3f2999a69b9b8d(
    id: builtins.str,
    job_state: JobState,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b62843a9fea91eb93e6bf7bcd95a76fc790b72a6a7ae7024cf486b3fd9d20f7(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1fcdc972ccb29fe1572e8970cb83faccd76d7cee7f09ed3f5c9571bca7a886d(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__697ee4e4007ce058f39e7fc610b2c0c4457bbd6008e9287406b18505ed299434(
    class_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6176c370f308e8911be636fb1acf643512dbe9ca58823d8267644ab7efc406c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    executable: JobExecutable,
    connections: typing.Optional[typing.Sequence[IConnection]] = None,
    continuous_logging: typing.Optional[typing.Union[ContinuousLoggingProps, typing.Dict[builtins.str, typing.Any]]] = None,
    default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_profiling_metrics: typing.Optional[builtins.bool] = None,
    execution_class: typing.Optional[ExecutionClass] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_run_queuing_enabled: typing.Optional[builtins.bool] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    notify_delay_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_configuration: typing.Optional[ISecurityConfiguration] = None,
    spark_ui: typing.Optional[typing.Union[SparkUIProps, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    worker_count: typing.Optional[jsii.Number] = None,
    worker_type: typing.Optional[WorkerType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd8db6c08c7bba32e81d8cda162918f634f3065c707bdd1ddfb404e329994882(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    job_name: builtins.str,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c143c24940c0f180cf99d417380821b95c0287b9b01c42df4f74c6e7959a56b8(
    metric_name: builtins.str,
    type: MetricType,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d8262e07cdf8942bd30cd21bf9d73a8b85e3b2683e99b4f40ed03fbf49b57ac(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8a1d8b4180629a6e1364fed24a3f246786b2d528b0ef21dda37098ac2af2c9a(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0546c2bad534dee21310d2705463267023bd2bd40cd093c29b95dccda7c69228(
    id: builtins.str,
    job_state: JobState,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8390e01882a245ed021fa1f65648219d84b9932b1c593026055b61fe2c56a85(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b061eb382ce02e7e8798f77ad4abe593f170f59b9df192c9e6c5fb3de7901a33(
    id: builtins.str,
    *,
    target: typing.Optional[_aws_cdk_aws_events_ceddda9d.IRuleTarget] = None,
    cross_stack_scope: typing.Optional[_constructs_77d1e7e8.Construct] = None,
    description: typing.Optional[builtins.str] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f1f5ae0406d4aaf443249ea9377b38a10b1814ed1f9c1fb9f0cbc5f489fd89e(
    *,
    job_name: builtins.str,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a555ea81acfe554401802d7d44d70d3e1a6f96890ffbc28283fadb7ea81f9e(
    *,
    mode: JobBookmarksEncryptionMode,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__629e6b8d2f364b0c0cfaa00ca6e06725f3d280ad7a2366cf5df8f63e472fea40(
    *,
    glue_version: GlueVersion,
    language: JobLanguage,
    script: Code,
    type: JobType,
    class_name: typing.Optional[builtins.str] = None,
    extra_files: typing.Optional[typing.Sequence[Code]] = None,
    extra_jars: typing.Optional[typing.Sequence[Code]] = None,
    extra_jars_first: typing.Optional[builtins.bool] = None,
    extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
    python_version: typing.Optional[PythonVersion] = None,
    runtime: typing.Optional[Runtime] = None,
    s3_python_modules: typing.Optional[typing.Sequence[Code]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f47dc7b3a9514a79f7f82e52c4441b82161dce2eb5b67f22211660776beaa70(
    *,
    executable: JobExecutable,
    connections: typing.Optional[typing.Sequence[IConnection]] = None,
    continuous_logging: typing.Optional[typing.Union[ContinuousLoggingProps, typing.Dict[builtins.str, typing.Any]]] = None,
    default_arguments: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_profiling_metrics: typing.Optional[builtins.bool] = None,
    execution_class: typing.Optional[ExecutionClass] = None,
    job_name: typing.Optional[builtins.str] = None,
    job_run_queuing_enabled: typing.Optional[builtins.bool] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    max_concurrent_runs: typing.Optional[jsii.Number] = None,
    max_retries: typing.Optional[jsii.Number] = None,
    notify_delay_after: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_configuration: typing.Optional[ISecurityConfiguration] = None,
    spark_ui: typing.Optional[typing.Union[SparkUIProps, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    worker_count: typing.Optional[jsii.Number] = None,
    worker_type: typing.Optional[WorkerType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0683afe40f10e5c8c02ac80ffb25aca1e5830884e6b5e539accb9e36df90257d(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8952681a040fc7931f48438a2e01cd3c2bed40202b6f32cd606344a5ea10e810(
    class_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854153aaeace5af7af75594677e850d114f911156b5cd93d50a01feeff4a76a8(
    *,
    key_names: typing.Sequence[builtins.str],
    index_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96728d115db88df2280e8997d67958a9b8d05214b04966c306fbf00f84a6324f(
    *,
    glue_version: GlueVersion,
    python_version: PythonVersion,
    script: Code,
    extra_files: typing.Optional[typing.Sequence[Code]] = None,
    runtime: typing.Optional[Runtime] = None,
    s3_python_modules: typing.Optional[typing.Sequence[Code]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787eb0d11407cb3ae6ba15f28cff4370dd45126f9ce4e2ab093edba7a3b628e8(
    *,
    glue_version: GlueVersion,
    python_version: PythonVersion,
    script: Code,
    extra_files: typing.Optional[typing.Sequence[Code]] = None,
    extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
    runtime: typing.Optional[Runtime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0bf4f1c4314f36fa21cf1fde861d972bb36e11678ce6f78e9dab93055f9ed4(
    *,
    glue_version: GlueVersion,
    python_version: PythonVersion,
    script: Code,
    extra_files: typing.Optional[typing.Sequence[Code]] = None,
    extra_jars: typing.Optional[typing.Sequence[Code]] = None,
    extra_jars_first: typing.Optional[builtins.bool] = None,
    extra_python_files: typing.Optional[typing.Sequence[Code]] = None,
    runtime: typing.Optional[Runtime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77ef351ef4776813c6253cf1f604175f461d8b9f9a8806473279f7e71a53adfe(
    runtime: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7854e17fe796bdc5dc10fe3c8febb691186728550ca107493a43fc6979cafee(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18fa6b6bc6e19007515f753b3e849efd4b7a16720ea785b0e155f20075d71602(
    _scope: _constructs_77d1e7e8.Construct,
    grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d972222b3b5c087e70a7ab859853e97f1579eeee2ede763d551c41d4076f740e(
    *,
    mode: S3EncryptionMode,
    kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8895a1f83a364cc50cc706b326361b090931a87ba5ad2c1f9a0747bf6c0f7e7(
    *,
    class_name: builtins.str,
    glue_version: GlueVersion,
    script: Code,
    extra_files: typing.Optional[typing.Sequence[Code]] = None,
    extra_jars: typing.Optional[typing.Sequence[Code]] = None,
    extra_jars_first: typing.Optional[builtins.bool] = None,
    runtime: typing.Optional[Runtime] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b92f46741e45dc5d5e256fe3738d53a8878b40fc430d149eec6fdbfe167229(
    length: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcdd8f07d6d5e4e87f54cd2104a8605a571a6abede0b42465e2352b51723b900(
    precision: jsii.Number,
    scale: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc04f65c508e37fca936dfd67a8b4a0f84a73b9ef9c446edcd34f17c738c8dae(
    key_type: typing.Union[Type, typing.Dict[builtins.str, typing.Any]],
    *,
    input_string: builtins.str,
    is_primitive: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33f94b4c838eb0e3d03de4da6b4f3fe8e873ef98895fb940645c459801c4bb50(
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba18137b7dd32100f635af375c8586adc2f9824c4ccd0a1b01168f5ba757da4(
    length: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd628a6199f5b5fb7644771f78b6cc6d9230e3c38bba0463810d192bceb52e8d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_watch_encryption: typing.Optional[typing.Union[CloudWatchEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    job_bookmarks_encryption: typing.Optional[typing.Union[JobBookmarksEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_encryption: typing.Optional[typing.Union[S3Encryption, typing.Dict[builtins.str, typing.Any]]] = None,
    security_configuration_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a85db96fd444625c46f4574190ecd86214bed327c2f826ee3294853f69a42b6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    security_configuration_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b8dd2838cd56b87c144ac347e4b66a78dd0c85a6196f1282adce12bd2e94f36(
    *,
    cloud_watch_encryption: typing.Optional[typing.Union[CloudWatchEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    job_bookmarks_encryption: typing.Optional[typing.Union[JobBookmarksEncryption, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_encryption: typing.Optional[typing.Union[S3Encryption, typing.Dict[builtins.str, typing.Any]]] = None,
    security_configuration_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b6eea0230610f203e5d4ed1dbd871c9ecc76a60681d0500a51e2d3815f193e(
    class_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5697eede3034b2366456fa6abdccec9640fd76f2916540c3a178d004e5cd680a(
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c613959b2bc20f05aa8f4578d26e870c2d4044aaaee1a5248ed0ddf8d4b75776(
    *,
    enabled: builtins.bool,
    bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f74283389af10eaf6da714f4aadddf86dec9f3da227641c23ae118f6dfd7b45(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39c7b662e4b538ebbd408dcac5b933ae4d1527472b30facbc0405a6a1d3bb14(
    value: ColumnCountMismatchHandlingAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__666d2a40474ee489c242320aca5600aa88eb0e9ff6b3f6f2523138d1febe5b9b(
    value: CompressionType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__972574c985d99d1bb6f6d431a08c62d778ff9dd7c7acaa151f9c4c535255e211(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7446681fb6fa8d72452081fd5567c4cfb319974b0acc83e49ae911e49d15d02(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4fecfebea5461d7e6230a0187c52f9a9d764b9e29971ed3414e1d84633f26ba(
    value: InvalidCharHandlingAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bbe8806a487d42b3c7b3868e2419195fd8e623ea4a74692a316cc258efafb28(
    value: NumericOverflowHandlingAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0897c928202255a3b3383203c753ac3165280fbc81faec3dd559c25843d4d3d4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb88780e26a940311a2cf44dd5d68de1ff362d2d0ca028f0443bba7e4bb06a8(
    value: OrcColumnMappingType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4284890747f6d237b5fdefef7df7ed57b66bda672915eb23526cae4e1b45ac7b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d196d1d149d7fb743eb77988c4d05f55b9e72876647220d0067b47caeab18a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2e1fd759f08830451a50273269345e05b91bbd90e750e7b76b2bac5275870a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c04fd2fab2c9a95b1c92f9718dfe11ffeb2436d47a798d0f870aae58746f67a(
    value: SurplusBytesHandlingAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1b9effa7f6a703549bb4dbdc074898313b647fe00864615574b5f4527a6efd(
    value: SurplusCharHandlingAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786b7e6901c19fc29fc68d4fe9cfd302c0d877d823b66a1fc00cd87af05bc1a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6b28d6c7211b035722cff75146ec9b7f6d1ef3da62494976a7200ddf69ed8f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__934bd25af2a5a54f5badd7296f8c59c0bd6be0399bcb84d225a10f0f5db755d5(
    value: WriteParallel,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a76a75ff6c3a793e7e5f24f77665e06ab62ec467008c0ae0a13c2537b6003d(
    *,
    table_arn: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3498ddd8b03f8ca1e3bea08a9f07832747b340c2a3681dc513148655f79ad155(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    database: IDatabase,
    data_format: DataFormat,
    compressed: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    enable_partition_filtering: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
    partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
    stored_as_sub_directories: typing.Optional[builtins.bool] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02bd4969b95beb4e956637865cbc28ff5818c6ec54f938297add787350585c81(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    table_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58099cdb2e6af7cafb7eb58d27cec43a72e06cce30052aef55c41e9f4574cb47(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    table_arn: builtins.str,
    table_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b9362ce2360a32cd6ed5b3e0b6fb67c0eeb2fadb38c5ce618002656d772e776(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    actions: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fefdc4d880c6035cf74f0867c529fd1390e46d666f130f14ef71eeb28507b1c(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    actions: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daad53122858b1d79a2d9a51e22fe701058f7a4a9f5b6d813930d2e34d3f2c63(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__316a7ca269e4227039ebebd0789404fc7ab5c3f9b3787007562ce4edf5df8225(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb08ef4e43dac45d9dc56da91de5195d72be73db28c81ee45853c2c2ac349abd(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c621f615cea5a292fe84c07e10ca61e7529536864f1701be1f19b168483439de(
    *,
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    database: IDatabase,
    data_format: DataFormat,
    compressed: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    enable_partition_filtering: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
    partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
    stored_as_sub_directories: typing.Optional[builtins.bool] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5fb0ad30c447263aceddf4b77f71aec991966bf6e2dc3a181ff400914c16d85(
    *,
    input_string: builtins.str,
    is_primitive: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217f80c6bee3c0db54c77a2a2bd0aa17178f371ff924355e6d6d4576a10d15c0(
    worker_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8659d1457c6b7393d9d7559014d5e5cf2fae91cdf81e1dcc8f010bdd5e6159d6(
    path: builtins.str,
    *,
    deploy_time: typing.Optional[builtins.bool] = None,
    readers: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.IGrantable]] = None,
    source_kms_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_aws_cdk_ceddda9d.AssetHashType] = None,
    bundling: typing.Optional[typing.Union[_aws_cdk_ceddda9d.BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    exclude: typing.Optional[typing.Sequence[builtins.str]] = None,
    follow_symlinks: typing.Optional[_aws_cdk_ceddda9d.SymlinkFollowMode] = None,
    ignore_mode: typing.Optional[_aws_cdk_ceddda9d.IgnoreMode] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02569161383966e61e7748be2a2760721daf0107762bdf02e3d7b51459e0adda(
    scope: _constructs_77d1e7e8.Construct,
    grantable: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e49faf739a72a3e5056a9506838a646b867a4b6b78cad2fc0eb56a8a3a4d314(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    type: ConnectionType,
    connection_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    match_criteria: typing.Optional[typing.Sequence[builtins.str]] = None,
    properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    subnet: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISubnet] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3a56fcf056a17ac1a36f3aeea6a054c7367495dbcff654385c491f79a8de6e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    connection_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2376990bb2b0fdc1652696730260ad95accfa020e78a7421e67836ad9c49c867(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    connection_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__664a10af42e73be7ad7fc6b49fd43b23cdb7750d16ad9c795923ec494e582778(
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e874ec3f48fcb87408229a566f69396601cc87f18c40fa5579a09664f117653(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ruleset_dqdl: builtins.str,
    target_table: DataQualityTargetTable,
    client_token: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    ruleset_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f0037b4150747a57e755360c767a1a492219225586c5381f7515e9f8675b60(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    ruleset_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73d686727005bdb9857f1aed58c7619b0390fa040ea2cf5eeef9e309883720e1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    ruleset_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f4b410df1b0bf1116ce03c0e8a707776efd2f03da87fd718bf64b6a4964b2cd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    database_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    location_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b20be4513bbaa9c562fcfb165fa327a8e6c6d38a0b15481eca8493b9b5a7b8d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    database_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b251bd575556272c98729ccada78c9d0fedbddd35e4e50ccd72649f6882227(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    connection: IConnection,
    external_data_location: builtins.str,
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    database: IDatabase,
    data_format: DataFormat,
    compressed: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    enable_partition_filtering: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
    partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
    stored_as_sub_directories: typing.Optional[builtins.bool] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c617ebeabae95be649f31192a1508ef254d5bb2a8f19540978e253877af7dc16(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d8e02b4ae2bce8590c80e2ce7a5829b237b1f08f6385cd6a8b926b701f8156b(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a161912810e7c25318614d340cf493d532bdbc1c20d5857baaa8e004b812df93(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a91c342ce35e1b47ced3892e3796a41cbe78a15258e691c0f83319c7bc95c8f0(
    *,
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    database: IDatabase,
    data_format: DataFormat,
    compressed: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    enable_partition_filtering: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
    partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
    stored_as_sub_directories: typing.Optional[builtins.bool] = None,
    table_name: typing.Optional[builtins.str] = None,
    connection: IConnection,
    external_data_location: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b5cd7a8c51600d473f125b7e52d34d32dba95265780e87640a28f30e73ce95d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    encryption: typing.Optional[TableEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    database: IDatabase,
    data_format: DataFormat,
    compressed: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    enable_partition_filtering: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
    partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
    stored_as_sub_directories: typing.Optional[builtins.bool] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3909b8e18b4eb038d1349092a370f0791a90c6e7f8380b7439f83993e01d04f(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7a94485fcfc5ef062186c7655669b475fac2ccac917edd1bd396de160cd227(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea067213729fc1f1f124734239ce0d21ea4e77d3fecd8d14ab5363d59122770b(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a30697598fc2a32c5e111aebc024dd5935b49f4f1807d70f75c9a4e8bff8268(
    *,
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    database: IDatabase,
    data_format: DataFormat,
    compressed: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    enable_partition_filtering: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
    partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
    stored_as_sub_directories: typing.Optional[builtins.bool] = None,
    table_name: typing.Optional[builtins.str] = None,
    bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    encryption: typing.Optional[TableEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1146b20665153f742431bb500cb6e71362a22d8446ea9e132183e7be255411a3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    encryption: typing.Optional[TableEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    database: IDatabase,
    data_format: DataFormat,
    compressed: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    enable_partition_filtering: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
    partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
    stored_as_sub_directories: typing.Optional[builtins.bool] = None,
    table_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0336d5abace2b9645857eae2fba5aa1c4bbb0db1762c5d5031d2f8c64019d606(
    *,
    columns: typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]],
    database: IDatabase,
    data_format: DataFormat,
    compressed: typing.Optional[builtins.bool] = None,
    description: typing.Optional[builtins.str] = None,
    enable_partition_filtering: typing.Optional[builtins.bool] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    partition_indexes: typing.Optional[typing.Sequence[typing.Union[PartitionIndex, typing.Dict[builtins.str, typing.Any]]]] = None,
    partition_keys: typing.Optional[typing.Sequence[typing.Union[Column, typing.Dict[builtins.str, typing.Any]]]] = None,
    storage_parameters: typing.Optional[typing.Sequence[StorageParameter]] = None,
    stored_as_sub_directories: typing.Optional[builtins.bool] = None,
    table_name: typing.Optional[builtins.str] = None,
    bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    encryption: typing.Optional[TableEncryption] = None,
    encryption_key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    s3_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
