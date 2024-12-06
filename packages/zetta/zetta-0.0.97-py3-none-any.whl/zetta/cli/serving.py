# Copyright ZettaBlock Labs 2024
import requests
import openai
import typer
import json
import os
import configparser
from zetta._utils.async_utils import synchronizer
from websockets.sync.client import connect
from websockets.exceptions import ConnectionClosedError

from openai import OpenAI


PROXY_SERVER = "35.238.202.166:8888"
NEO_HOST = "https://neo-dev.prod.zettablock.com"
API_SERVER = "http://35.238.202.166:8000"

serving_cli = typer.Typer(
    name="serving",
    help="Manage your inference serving in Zetta AI Network.",
    no_args_is_help=True,
)


def getToken():
    zetta_root = os.path.expanduser("~")
    secrets_path = os.path.join(zetta_root, ".zetta/secrets")
    config = configparser.ConfigParser()
    config.read(secrets_path)
    token = config.get("default", "token", fallback=None)
    return token


@serving_cli.command(
    name="list",
    help="List all the visible inference endpoints that are currently running.",
)
@synchronizer.create_blocking
async def list(model: str = "all"):
    url = f"{API_SERVER}/infer/list"
    response = requests.get(url, params={"model": model})
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        response.raise_for_status()


@serving_cli.command(
    name="status", help="Show the stats information of the inference endpoints."
)
@synchronizer.create_blocking
async def status():
    url = f"{API_SERVER}/serving/status"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=2))
    else:
        response.raise_for_status()


@serving_cli.command(name="deploy", help="Deploy a model for serving.")
@synchronizer.create_blocking
async def deploy(
    model: str = "",
    base_model: str = "",
    machine_type: str = "",
    duration: str = "",
    replica: int = 1,
):
    token = getToken()
    if token == "":
        token = "zt_KUHUZFsWMoedNnIpxEXiUeOpPSoiAILKmX"
    if not model.startswith("model_version"):
        print(
            "Please specify a model_version_id to deploy. you can get from ’zetta model version-list --model-id XXX‘"
        )
        return
    url = f"{NEO_HOST}/v1/api/job"
    data = {
        "name": "deployed by cli",
        "deployment": {
            "base_model": base_model,
            "model_version_id": model,
        },
        "type": "ModelDeployment",
    }
    headers = {
        "Authorization": token,
    }
    print(data)
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise Exception(
            f"Failed to deploy model: [{response.status_code}] {response.text}"
        )


@serving_cli.command(name="renew", help="Renew a model for serving.")
@synchronizer.create_blocking
async def renew(model: str = "", duration: str = ""):
    pass


@serving_cli.command(name="update", help="Update a serving config")
@synchronizer.create_blocking
async def update(config: str):
    # machine type, replica and remain-time can be change here
    pass


def stream_chat(model: str = "", msg: str = "", prompt: str = ""):
    msg_data = [
        {
            "role": "system",
            "content": prompt,
        },
        {
            "role": "user",
            "content": msg,
        },
    ]
    json_data = {
        "model": model,
        "messages": msg_data,
        "stream": True,
    }
    print(json_data)
    with connect(
        f"ws://{PROXY_SERVER}/ws/" + getUserName()
    ) as websocket:
        websocket.send(json.dumps(json_data))
        try:
            while 1:
                message = websocket.recv()
                print(message, end="")
        except ConnectionClosedError:
            pass


def getUserName():
    zetta_root = os.path.expanduser("~")
    path = os.path.join(zetta_root, ".zetta/profile")
    config = configparser.ConfigParser()
    config.read(path)
    name = config.get("default", "user_name", fallback=None)
    return name


@serving_cli.command(
    name="infer",
    help=" Do inference with model. e.g. zetta serving infer --model XXX --msg XXX --prompt(optional) XXX",
)
@synchronizer.create_blocking
async def chat(
    model: str = "",
    msg: str = "",
    prompt: str = "You are a helpful assistant.",
    endpoint: str = "any",
    stream: bool = True,
):
    if model == "":
        print(
            "Please specify a model to do inference. a valid model should start with 'model_' and contain repo-name, such as model_version_URpyIS65AfBJqBpNAibF8f6V@falcon-7B"
        )
        return
    if msg == "":
        print("Please input a message to chat.")
        return

    if stream:
        stream_chat(model, msg, prompt)
        return

    client = OpenAI(
        base_url=f"http://{PROXY_SERVER}/v1",
        api_key="",
    )
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": msg,
                },
            ],
            stream=stream,
        )
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
        return
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
        return
    if stream:
        ## print(completion.response.json())
        for chunk in completion:
            print(chunk.choices[0].delta.content)
    else:
        res = completion.choices[0].message.content.split("\n")
        print(res[0])
