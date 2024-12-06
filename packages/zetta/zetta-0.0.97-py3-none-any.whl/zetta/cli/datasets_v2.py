# Copyright ZettaBlock Labs 2024
import pyarrow.parquet
import typer
import pyarrow.parquet as pq

from zetta._utils.async_utils import synchronizer
from zetta.cli.utils import ICEBERG_DATA_LOCATION, S3_BUCKET, \
    list_parquet_files, upload_s3, create_iceberg_ns_and_table, list_iceberg_tables, list_iceberg_table, get_catalog

datasetsv2_cli = typer.Typer(
    name="datasetsv2",
    help="Manage your datasets in Zetta AI Network v2.",
    no_args_is_help=True,
)

SERVICE_CREATE_DATASET_URL = "https://neo-dev.prod.zettablock.com/v1/api/asset"
SERVICE_GITEA_URL = "https://gitea.stag-vxzy.zettablock.com"

"""
test:

1, use https://github.com/Zettablock/ai-lake-research/blob/main/sdk_poc.py#L126 to create parquets files

2, prepare aws credentials in ENV

export AWS_KEY_ID=<removed>
export AWS_SECRET_ACCESS_KEY=<removed>

3, run zetta datasetsv2 create to create iceberg table
"""


# TODO:
#  use Neo to create dataset and get pre-signed url to upload parquet files
#  register metadata to Neo
#  list datasets
#  read data from datasets in iceberg


@datasetsv2_cli.command(name="create", help="create new iceberg dataset (namespace and table) from parquet files")
@synchronizer.create_blocking
async def create(namespace: str = typer.Option("ai-lake-test",
                                               help="Name of the dataset namespace"),
                 dataset: str = typer.Option("imagenet-object-localization-challenge-dec03",
                                             help="Name of the dataset"),
                 path: str = typer.Option("/Users/cpei/zb/ai-lake-research/test_par",
                                          help="Path of the dataset")):
    print('Load parquets from {} to {}.{}'.format(dataset, namespace, dataset))
    s3_file_lst = []
    # list parquet files
    parquet_files = list_parquet_files(path)
    for parquet_file, file_name in parquet_files:
        s3_path = upload_s3(parquet_file, S3_BUCKET, "{}-{}/{}".format(namespace, dataset, file_name))
        print(s3_path)
        s3_file_lst.append(s3_path)
    print('s3_file_lst:', s3_file_lst)
    # create iceberg namespace and table
    table = create_iceberg_ns_and_table(
        ns=namespace,
        table_name=dataset,
        schema=pq.read_schema(parquet_files[0][0]),
        location=ICEBERG_DATA_LOCATION
    )
    # add files to iceberg table
    print("add files to iceberg table")
    table.add_files(file_paths=s3_file_lst)


@datasetsv2_cli.command(name="list", help="list iceberg dataset(s)")
@synchronizer.create_blocking
async def ls(namespace: str = typer.Option("ai-lake-test",
                                           help="Name of the dataset namespace"),
             dataset: str = typer.Option("",
                                         help="Name of the dataset")):
    print('list {}.{}'.format(namespace, dataset))
    if not dataset:
        print(list_iceberg_tables(ns=namespace))
    else:
        print(list_iceberg_table(ns=namespace, table=dataset))


@datasetsv2_cli.command(name="read", help="read iceberg dataset(s) to pandas")
@synchronizer.create_blocking
async def read(namespace: str = typer.Option("ai-lake-test",
                                             help="Name of the dataset namespace"),
               dataset: str = typer.Option("",
                                           help="Name of the dataset"),
               limit: int = typer.Option(10,
                                         help="Limit of the data to read")):
    print('read {}.{} limit = {}'.format(namespace, dataset, limit))
    catalog = get_catalog()
    rows = catalog.load_table('{}.{}'.format(namespace, dataset)).scan(limit=limit).to_pandas()
    print(rows)


@datasetsv2_cli.command(name="save", help="save iceberg dataset(s) to local parquet files")
@synchronizer.create_blocking
async def save(namespace: str = typer.Option("ai-lake-test",
                                             help="Name of the dataset namespace"),
               dataset: str = typer.Option("",
                                           help="Name of the dataset"),
               limit: int = typer.Option(10,
                                         help="Limit of the data to read")):
    print('save {}.{} limit = {}'.format(namespace, dataset, limit))
    catalog = get_catalog()
    rows = catalog.load_table('{}.{}'.format(namespace, dataset)).scan(limit=limit).to_arrow()
    pyarrow.parquet.write_table(rows, '{}-{}.parquet'.format(namespace, dataset))

