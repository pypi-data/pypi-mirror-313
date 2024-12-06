# Copyright ZettaBlock Labs 2024
import os

import boto3
import pyiceberg
from pyiceberg.catalog import load_catalog
from pyiceberg.schema import Schema

ICEBERG_DATA_LOCATION = "s3://ai-network-worker-demo/iceberg-data/"
S3_BUCKET = "ai-network-worker-demo"
AWS_DATA_CATALOG = "AwsDataCatalog"


def list_parquet_files(path_str):
    files = []
    for file in os.listdir(path_str):
        if file.endswith('.parquet'):
            files.append((os.path.join(path_str, file), file))
    return files


def upload_s3(parquet_file, bucket, key):
    """
    Args:
        :param parquet_file:
        :param bucket:
        :param key:
    """
    s3 = boto3.client('s3',
                      aws_access_key_id=os.getenv("AWS_KEY_ID"),
                      aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))
    s3.upload_file(parquet_file, bucket, key)
    return f's3://{bucket}/{key}'


def add_files_to_iceberg(table: pyiceberg.catalog.Table, parquet_file):
    table.add_files(parquet_file)


def create_iceberg_ns_and_table(ns: str = "ai-lake-test",
                                table_name: str = "imagenet-object-localization-challenge-nov26",
                                schema: Schema = None,
                                location: str = "s3://ai-network-worker-demo/iceberg-data/"):
    catalog = load_catalog(AWS_DATA_CATALOG, **{
        "type": "glue",
        "region": "us-east-1",
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": os.getenv("AWS_KEY_ID"),
        "s3.secret-access-key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "max-workers": 8
    })

    catalog.create_namespace_if_not_exists(ns)

    # Create an Iceberg table
    table = catalog.create_table_if_not_exists(
        identifier="{}.{}".format(ns, table_name),
        schema=schema,
        location=location)
    return table


def list_iceberg_tables(ns: str = "ai-lake-test"):
    catalog = load_catalog(AWS_DATA_CATALOG, **{
        "type": "glue",
        "region": "us-east-1",
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": os.getenv("AWS_KEY_ID"),
        "s3.secret-access-key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "max-workers": 8
    })

    tables = []
    for ns, tbl in catalog.list_tables(ns):
        tables.append('{}.{}'.format(ns, tbl))
    return tables


def list_iceberg_table(ns: str = "ai-lake-test", table: str = ""):
    catalog = load_catalog(AWS_DATA_CATALOG, **{
        "type": "glue",
        "region": "us-east-1",
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": os.getenv("AWS_KEY_ID"),
        "s3.secret-access-key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "max-workers": 8
    })

    return catalog.load_table("{}.{}".format(ns, table)).schema()


def get_catalog():
    catalog = load_catalog(AWS_DATA_CATALOG, **{
        "type": "glue",
        "region": "us-east-1",
        "py-io-impl": "pyiceberg.io.pyarrow.PyArrowFileIO",
        "s3.access-key-id": os.getenv("AWS_KEY_ID"),
        "s3.secret-access-key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "max-workers": 8
    })

    return catalog
