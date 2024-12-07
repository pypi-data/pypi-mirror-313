from dotenv import dotenv_values
from typing import Dict
import base64
import fnmatch
import importlib.metadata
import io
import json
import os
import platform
import qupiato.cli.config as c
import re
import requests
import sys
import tempfile
import uuid
import websockets
import zipfile


async def ws_api_call(req: Dict):
    async with websockets.connect(c.DEPLOYER_WS_URL) as ws:
        await ws.send(json.dumps(req))

        while True:
            try:
                resp = await ws.recv()
                data = json.loads(resp)
                yield data
            except websockets.exceptions.ConnectionClosedOK:
                break

            except websockets.exceptions.ConnectionClosedError:
                break


def encode_secret():
    for root, _, files in os.walk('.'):
        for file in files:
            file_path = os.path.join(root, file)
            norm_path = os.path.normpath(file_path)

            if os.path.basename(norm_path) == '.env':
                env = ''
                env_config = dotenv_values(norm_path)
                for key, value in env_config.items():
                    env += f"{key}={value}\n"
                env_bytes = base64.b64encode(env.encode('utf-8'))
                env_string = env_bytes.decode('utf-8')
                return env_string


# 현재 디렉토리와 하위 디렉토리에 있는 모든 파일 압축
def create_zip_archive(zip_filename):
    ignored_patterns = load_qignore()

    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk('.'):
            for file in files:
                file_path = os.path.join(root, file)
                norm_path = os.path.normpath(file_path)
                d_name = os.path.dirname(norm_path)

                if os.path.basename(norm_path).startswith('.env'):
                    continue
                if os.path.basename(norm_path) == 'db.json':
                    continue
                if os.path.basename(norm_path).startswith('.bash'):
                    continue
                if d_name and d_name.startswith('.'):
                    continue
                if d_name and d_name == '__pycache__':
                    continue
                if d_name and os.path.basename(d_name).startswith('.'):
                    continue
                if d_name and os.path.basename(d_name) == 'logs':
                    continue
                if os.path.basename(norm_path).endswith('.ipynb'):
                    continue
                if os.path.basename(norm_path).endswith('.zip'):
                    continue
                if os.path.basename(norm_path).endswith('.tar.gz'):
                    continue
                if os.path.basename(norm_path).endswith('.log'):
                    continue
                if os.path.basename(norm_path) == 'code':
                    continue
                if is_ignored(norm_path, ignored_patterns):
                    continue
                if is_ignored(os.path.basename(norm_path), ignored_patterns):
                    continue
                if os.path.basename(norm_path) == 'qupiato':
                    continue

                zipf.write(file_path, os.path.relpath(file_path))


def load_qignore(file_path=".qignore"):
    if not os.path.isfile(file_path):
        return set()
    with open(file_path, "r") as f:
        ignored_patterns = set(
            line.strip() for line in f if line.strip() and not line.startswith("#")
        )
    return ignored_patterns


def is_ignored(file_path, ignored_patterns):
    for pattern in ignored_patterns:
        if pattern.endswith("/"):
            pattern = pattern + "*"

        if fnmatch.fnmatch(file_path, pattern):
            return True
    return False


def upload_using_api(zip_filename):
    url = f"{c.API_SERVER_URL}/deployments/upload"
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    files = {"file": (zip_filename, open(zip_filename, "rb"))}
    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200 and response.status_code != 201:
        raise Exception("Failed to upload zip file")

    return os.path.basename(zip_filename)


def create_and_upload_to_gcs_bucket():
    with tempfile.TemporaryDirectory() as temp_dir:
        zipfile_name = os.path.join(temp_dir, f'{str(uuid.uuid4()).replace("-", "")}.zip')

        create_zip_archive(zipfile_name)
        object_key = upload_using_api(zipfile_name)
        print(f"done. {object_key}")
        return object_key


def get_version():
    version = importlib.metadata.version('pyqqq-cli')
    return version


def search_strategies(params=''):
    url = f"{c.API_SERVER_URL}/strategy/publish"
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        if response.status_code == 404:
            return None
        else:
            code, message = response.json().values()
            raise Exception(f"Failed to search strategies {message}")

    return response.json()


def pull_strategy(name, filename):
    url = f"{c.API_SERVER_URL}/deployments/download"
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.get(url, headers=headers, params={'file': filename}, stream=True)

    if response.status_code != 200:
        raise Exception("Failed to search strategies")

    with io.BytesIO() as buffer:
        for chunk in response.iter_content(None):
            buffer.write(chunk)

        with zipfile.ZipFile(buffer) as zipf:
            zipf.extractall(name)


# 전략의 공개 설정
def publish_strategy(entryfile, strategy_name, zipfile):
    entry_dir = os.path.dirname(os.path.normpath(entryfile))
    markdown = None
    for root, _, files in os.walk(entry_dir or '.'):
        if markdown is not None:
            break

        for file in files:
            file_path = os.path.join(root, file)
            norm_path = os.path.normpath(file_path)
            d_name = os.path.dirname(norm_path)

            if entry_dir == d_name and re.match('readme.md', os.path.basename(norm_path), re.I):
                markdown = norm_path
                break

    url = f"{c.API_SERVER_URL}/strategy/publish"
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    payload = {
        'strategy': strategy_name,
        'zipfile': zipfile,
    }

    if markdown:
        files = {"file": (os.path.basename(markdown), open(markdown, "rb"), "application/octet-stream")}
        response = requests.post(url, headers=headers, files=files, data=payload)
    else:
        response = requests.post(url, headers=headers, data=payload)

    if response.status_code != 200 and response.status_code != 201:
        raise Exception(f"Publishing failed with status code {response.status_code}")

    return response.json()


# 사용자 정보 조회
def get_user(uid):
    url = f"{c.API_SERVER_URL}/users/{uid}"
    headers = {
        'Authorization': f'Bearer {get_token()}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to search strategies")

    return response.json()


# websocket 메시지에 추가될 agent 정보
def get_agent():
    operating_system = {
        'Linux': 'linux',
        'Darwin': 'mac',
        'Windows': 'win',
    }
    os = operating_system.get(platform.system(), 'unknown')
    version = get_version()

    return {
        'name': 'command_line',
        'os': os,
        'version': version
    }


def get_token():
    if c.PYQQQ_API_KEY:
        return c.PYQQQ_API_KEY

    elif os.path.exists(c.CREDENTIAL_FILE_PATH):
        with open(c.CREDENTIAL_FILE_PATH, 'r') as f:
            return f.read().strip()

    else:
        print("ERROR: Key not found.")
        print("")
        print("Please set PYQQQ_API_KEY environment variable or create a file at ~/.qred with the API key.")
        sys.exit(1)
