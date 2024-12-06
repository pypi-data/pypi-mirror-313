# Copyright ZettaBlock Labs 2024
import typer
import os
import configparser
import requests
from termcolor import colored
import json as j
from typing import Optional
from rich import print_json
from typing_extensions import Annotated
from zetta._utils.cli_options import common_env_option
from zetta._utils.async_utils import synchronizer
from zetta._utils.connections import check_api_status

from zetta.job import (
    worker_log_job,
    init_zetta_job_config,
    gitea_upload,
    send_finetune_request,
)

job_cli = typer.Typer(
    name="job", help="Build your models in Zetta Workspace.", no_args_is_help=True
)


SERVICE_LIST_JOBS_URL = "https://neo-dev.prod.zettablock.com/v1/api/jobs"
SERVICE_GET_JOB_URL = "https://neo-dev.prod.zettablock.com/v1/api/job"


@job_cli.command(name="list", help="List all build jobs that are currently running.")
@synchronizer.create_blocking
async def list(env: str = common_env_option(), json: bool = True):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get("default", "token", fallback=None)
        headers = {"Authorization": token}
        response = requests.get(SERVICE_LIST_JOBS_URL, headers=headers)
        data = response.json()
        if response.status_code == 200:
            print_array_info(data["data"], "jobs")
        else:
            raise ValueError(data["error"])
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    pass


def print_array_info(array, text_title):
    title = colored(text_title, "blue")
    line_length = 0
    for ele in array:
        lll = len(f"{ele['id']} {ele['job_type']} {ele['status']}")
        line_length = max(lll, line_length)
    box_width = max(70, line_length + 4)
    print(f"┌{'─' * 4} {title} {'─' * (box_width - len(text_title) - 8)}┐")
    longest_typ = 0
    for ele in array:
        if len(ele["job_type"]) > longest_typ:
            longest_typ = len(ele["job_type"])
    for ele in array:
        id = ele["id"]
        tye = ele["job_type"]
        status = ele["status"]
        c_status = colored(status, "green")
        if status == "Failed":
            c_status = colored(status, "red")
        elif status == "Running":
            c_status = colored(status, "blue")
        ele_info = f"{id} {tye}{' ' * (longest_typ-len(tye))} {c_status}"
        ll = len(id) + longest_typ + len(status) + 2
        print(f"│ {ele_info}{' ' * (box_width-ll-4)} │")
    print(f"└{'─' * (box_width - 2)}┘")


@job_cli.command(name="get", help="get a job status.")
@synchronizer.create_blocking
async def get(jobid, env: str = common_env_option()):
    try:
        zetta_root = os.path.expanduser("~")
        secrets_path = os.path.join(zetta_root, ".zetta/secrets")
        config = configparser.ConfigParser()
        config.read(secrets_path)
        token = config.get("default", "token", fallback=None)
        headers = {"Authorization": token}
        response = requests.get(f"{SERVICE_GET_JOB_URL}?id={jobid}", headers=headers)
        data = response.json()
        if response.status_code == 200:
            print_json(j.dumps(data["data"], indent=4))
        else:
            raise ValueError(data["error"])
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    pass


@job_cli.command(name="update", help="update a job.")
@synchronizer.create_blocking
async def update(json: bool = True):
    pass


@job_cli.command(name="cancel", help="cancel a running job for current user.")
@synchronizer.create_blocking
async def cancel(json: bool = True):
    pass


@job_cli.command(name="status", help="check the status of Zetta ai-network API.")
@synchronizer.create_blocking
async def status(env: str = common_env_option()):
    result = check_api_status(env)
    print(result["status"])
    return result


@job_cli.command(
    name="init", help="Initialize a new fine-tune job at designated location."
)
@synchronizer.create_blocking
async def init(
    project_name: Annotated[
        str,
        typer.Argument(
            ...,
            help="Name of the project, which will be used as the default output model name.",
        ),
    ],
    framework: str = "llama-factory",
    location: str = ".",
):
    """
    Initialize a new fine-tune project with name `project_name`. A config template will be downloaded at designated file location.
    `project_name` is the default name of the fine-tune model.
    """
    if framework == "llama-factory":
        config_path = init_zetta_job_config(project_name, location)
        print(f"Created config file at {config_path}. Fill in and get started!")
    else:
        print(f"Framework {framework} is not supported.")
    pass


@job_cli.command(
    name="run", help="Create a new fine-tune job with given configuration."
)
@synchronizer.create_blocking
async def run(
    config: Annotated[str, typer.Argument(..., help="Path to the config file.")],
    env: str = common_env_option(),
    gpu: Annotated[
        Optional[str], typer.Option(..., help="Type of the GPU to use.")
    ] = None,
    gpu_num: Annotated[
        Optional[str], typer.Option(..., help="Number of GPUs to use.")
    ] = 1,
):
    """
    Submit a new fine-tune job with given config file and optional hardware requirements.
    `config` can be a local file path or a URL to a public GitHub repository with `config.yaml` file in the root.
    Return a job id.
    """
    # parse job config
    if not os.path.exists(config):
        raise Exception(f"Config file not found at {config}")

    # send fine-tune request to service
    job_id = None
    try:
        response = send_finetune_request(config)
        job_id = response["data"]["id"]
        print(f"Job submitted successfully with job id: {job_id}")
    except Exception as e:
        print(f"Error: Failed to send fine-tune request: {e}")
        return

    try:
        # submit code to gitea
        commit_link = gitea_upload(config, job_id)
        # inform code commit link
        if commit_link is not None:
            print(f"Your files are snapshot at: {commit_link}")
        else:
            raise Exception("Failed to create code snapshot.")
    except Exception as e:
        print(f"Warning: {e}")


@job_cli.command(name="logs", help="Show the logs of a job with given job id.")
@synchronizer.create_blocking
async def logs(job_id: str):
    try:
        job = worker_log_job(job_id)
        print(job)
    except Exception as e:
        print(e)
