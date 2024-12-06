from finlab.ffn_core import tabulate
from nbformat import v4 as nbf
from urllib.parse import quote
from pathlib import Path
import pandas as pd
import subprocess
import requests
import nbformat
import finlab
import json
import time
import os
import re

from .login import _login

firebase_config = {
    "apiKey": "AIzaSyB9Ogv6Vbwfy6_I0aLEfcpsPhqhlc4FSTw",
    "authDomain": "fdata-299302.firebaseapp.com",
    "projectId": "fdata-299302",
    "storageBucket": "fdata-299302.appspot.com",
    "messagingSenderId": "748308483506",
    "appId": "1:748308483506:web:7c78dd82b422cd4ea5a8ab",
}


def list_strategies(token, user_id, verbose=True):

    headers = {"Authorization": f"Bearer {token}"}

    doc_ref = f"https://firestore.googleapis.com/v1/projects/{firebase_config['projectId']}/databases/(default)/documents/users/{user_id}"
    response = requests.get(doc_ref, headers=headers)
    data = response.json()

    strategy_names = list(data["fields"]["strategies"]["mapValue"]["fields"].keys())

    strategies = {}
    for sname in strategy_names:
        strategies[sname] = data["fields"]["strategies"]["mapValue"]["fields"][sname][
            "mapValue"
        ]["fields"]

        r1 = list(
            strategies[sname]["ndays_return"]["mapValue"]["fields"]["1"].values()
        )[0]
        r5 = list(
            strategies[sname]["ndays_return"]["mapValue"]["fields"]["5"].values()
        )[0]
        r20 = list(
            strategies[sname]["ndays_return"]["mapValue"]["fields"]["20"].values()
        )[0]
        r60 = list(
            strategies[sname]["ndays_return"]["mapValue"]["fields"]["60"].values()
        )[0]
        max_drawdown = list(strategies[sname]["max_drawdown"].values())[0]
        annual_return = list(strategies[sname]["annual_return"].values())[0]
        sharpe_ratio = list(strategies[sname]["sharpe_ratio"].values())[0]

        strategies[sname] = {
            "day %": r1,
            "week %": r5,
            "month %": r20,
            "season %": r60,
            "MDD": max_drawdown,
            "CAGR": annual_return,
            "SHARPE": sharpe_ratio,
        }

    ret = pd.DataFrame(strategies).astype(float).T
    percentage_cols = ["day %", "week %", "month %", "season %", "MDD", "CAGR"]
    ret[percentage_cols] = ret[percentage_cols].map(lambda x: f"{x:.2%}")
    ret["SHARPE"] = ret["SHARPE"].map(lambda x: f"{x:.2f}")

    if verbose:
        print(tabulate(ret, headers=ret.columns).to_markdown())

    return ret

def is_auto_update_enabled(token, user_id):

    headers = {"Authorization": f"Bearer {token}"}

    doc_ref = f"https://firestore.googleapis.com/v1/projects/{firebase_config['projectId']}/databases/(default)/documents/users/{user_id}"
    response = requests.get(doc_ref, headers=headers)
    data = response.json()
    print(data)
    if "kernel" in data["fields"] and "autoUpdate" in data["fields"]["kernel"]["mapValue"]["fields"]:
        return data["fields"]["kernel"]["mapValue"]["fields"]['autoUpdate']['booleanValue']
    return False


def get_notebook_data(token, user_id, strategy_name):

    headers = {"Authorization": f"Bearer {token}"}

    doc_ref = f"https://firestore.googleapis.com/v1/projects/{firebase_config['projectId']}/databases/(default)/documents/users/{user_id}/strategies/{strategy_name}/codes/code"
    response = requests.get(doc_ref, headers=headers)

    if response.status_code != 200:
        return None

    return response.json()


def extract_cell_text(notebook_data, strategy_name, is_user=False):

    cells = []

    if notebook_data is None:
        return {"success": False, "error": "Notebook not found"}

    for cell in notebook_data["fields"]["code"]["arrayValue"]["values"]:
        cells.append(cell["stringValue"])

    if is_user:
        # that means the author is the same as the user
        first_line = f"%env FINLAB_STRATEGY_NAME={strategy_name}"
        if len(cells) != 0:
            cells = [first_line] + cells
        else:
            cells.append(first_line)

    return cells


def pull_notebook(
    token, user_id, strategy_name, path, output_file_name=None, notebook_data=None
):

    if notebook_data is None:
        notebook_data = get_notebook_data(token, user_id, strategy_name)

    if notebook_data is None:
        return {"success": False, "error": "Notebook not found"}

    cells = extract_cell_text(
        notebook_data, is_user=output_file_name is None, strategy_name=strategy_name
    )

    nb = nbf.new_notebook()
    nb.cells = [nbf.new_code_cell(cell) for cell in cells]

    # set default kernel
    nb.metadata["kernelspec"] = {
        "display_name": "finlab-env",
        "language": "python",
        "name": "finlab-env",
    }

    if output_file_name is None:
        output_file_name = strategy_name
    file_path = os.path.join(path, f"{output_file_name}.ipynb")
    nbformat.write(nb, file_path)
    return {
        "success": True,
        "file_path": file_path,
        "updateTime": notebook_data["updateTime"],
    }


def create_notebook(strategy_name, path):
    nb = nbf.new_notebook()
    nb.cells = [nbf.new_code_cell(f"%env FINLAB_STRATEGY_NAME={strategy_name}")]
    nbformat.write(nb, path)
    return {"success": True, "file_path": path}


def push_notebook(token, user_id, strategy_name, path):

    headers = {"Authorization": f"Bearer {token}"}

    nb = nbformat.read(os.path.join(path, f"{strategy_name}.ipynb"), as_version=4)

    cells = []
    for cell in nb.cells:
        cells.append({"stringValue": cell.source})

    if len(cells) != 0:
        if "FINLAB_STRATEGY_NAME" in cells[0]["stringValue"]:
            split_line = cells[0]["stringValue"].split("\n", 1)
            if len(split_line) == 2:
                cells[0]["stringValue"] = split_line[1]
            else:
                cells[0]["stringValue"] = ""

            if cells[0]["stringValue"].strip(" \n\r\t") == "":
                cells = cells[1:]

    data = {"fields": {"code": {"arrayValue": {"values": cells}}}}

    doc_ref = f"https://firestore.googleapis.com/v1/projects/{firebase_config['projectId']}/databases/(default)/documents/users/{user_id}/strategies/{strategy_name}/codes/code"

    response = requests.patch(doc_ref, headers=headers, json=data)
    if "error" in response.json():
        return {"success": False, "error": response.json()["error"]}

    return {"success": True}


import requests
import time


def update_strategy_status(token, user_id, strategy_name, status):
    headers = {"Authorization": f"Bearer {token}"}

    doc_ref = f"https://firestore.googleapis.com/v1/projects/{firebase_config['projectId']}/databases/(default)/documents/users/{user_id}"

    quoted_strategy_name = f"`{strategy_name}`"

    data = {
        "fields": {
            "strategies": {
                "mapValue": {
                    "fields": {
                        "營收股價雙渦輪": {
                            "mapValue": {
                                "fields": {
                                    "status": {
                                        "mapValue": {
                                            "fields": {
                                                "start_time": {
                                                    "doubleValue": time.time()
                                                },
                                                "status": {"stringValue": status},
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    params = {"updateMask.fieldPaths": [f"strategies.{quoted_strategy_name}.status"]}

    response = requests.patch(doc_ref, headers=headers, json=data, params=params)

    if "error" in response.json():
        return {"success": False, "error": response.json()["error"]}

    return {"success": True}


def create_ipynb_file(file_content, file_name, folder_path):
    file_path = Path(folder_path) / file_name
    notebook_content = {
        "cells": [
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [file_content],
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 2,
    }
    with open(file_path, "w") as f:
        json.dump(notebook_content, f)


def is_jupyter_lab_running():
    try:
        result = subprocess.run(
            ["pgrep", "-f", "jupyter-lab"], check=True, stdout=subprocess.PIPE
        )
        return bool(result.stdout)
    except subprocess.CalledProcessError:
        return False


def get_jupyter_url():
    process = subprocess.Popen(
        ["jupyter", "lab", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    while True:
        output = process.stdout.readline().decode("utf-8")
        if output == "" and process.poll() is not None:
            break
        if output:
            url_match = re.search(r"http://localhost:\d+/\?token=[\w:]+", output)
            if url_match:
                return url_match.group(0)
    return None


def open_ipynb_file(WORKSPACE_PATH, file_name, envs, open_url=True):

    setting_file = """{"data":{"layout-restorer:data":{"down":{"size":0,"widgets":[]},"left":{"collapsed":true,"visible":false,"widgets":["filebrowser","running-sessions","@jupyterlab/toc:plugin"],"widgetStates":{"jp-running-sessions":{"sizes":[0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666,0.16666666666666666],"expansionStates":[false,false,false,false,false,false]},"extensionmanager.main-view":{"sizes":[0.3333333333333333,0.3333333333333333,0.3333333333333333],"expansionStates":[false,false,false]}}},"right":{"collapsed":true,"visible":false,"widgets":["jp-property-inspector","debugger-sidebar"],"widgetStates":{"jp-debugger-sidebar":{"sizes":[0.2,0.2,0.2,0.2,0.2],"expansionStates":[false,false,false,false,false]}}},"relativeSizes":[0,1,0],"top":{"simpleVisibility":true}}},"metadata":{"id":"finlab","last_modified":"2024-09-07T16:09:21.164963+00:00","created":"2024-09-07T16:09:21.164963+00:00"}}"""
    with open(f"{WORKSPACE_PATH}/finlab.jupyterlab-workspace", "w") as f:
        f.write(setting_file)

    command = (
        f"jupyter lab workspace import {WORKSPACE_PATH}/finlab.jupyterlab-workspace"
    )
    subprocess.Popen(
        ["bash", "-c", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    env = os.environ.copy()
    env.update(envs)
    command = (
        """eval "$(conda shell.bash activate)" && jupyter lab --ServerApp.root_dir=\""""
        + WORKSPACE_PATH
        + """\" --no-browser  --LabApp.tornado_settings=\"{'headers': {'Content-Security-Policy': \\"frame-ancestors 'self' http://localhost:5173 http://127.0.0.1:8888\\"}}" &"""
    )
    print(command)

    url = get_jupyter_url()
    if not url:
        print("Starting Jupyter Lab...")
        subprocess.Popen(
            ["bash", "-c", command],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        time.sleep(5)

    url = get_jupyter_url()
    if url:
        print(f"Jupyter Lab is running at {url}")
        token = url.split("=")[-1]
        port = url.split(":")[-1].split("/")[0]

        file_name = quote(file_name)
        openning_url = f"http://localhost:{port}/lab/workspaces/finlab/tree/{file_name}?token={token}?reset"
        print(openning_url)

        # use pywebview to open the url
        if open_url:
            import webview

            window = webview.create_window("FinLab", openning_url)
            webview.start()

        return openning_url

    raise Exception("Failed to start Jupyter Lab")


def execute_ipynb_file(file_name, folder_path, envs):
    file_path = Path(folder_path) / file_name

    env = os.environ.copy()
    env.update(envs)
    command = f'eval "$(conda shell.bash activate)" && jupyter nbconvert --to notebook --execute {file_path} --output {file_name}'
    result = subprocess.run(["bash", "-c", command], check=False, env=env)
    if result.returncode != 0:
        return False
    return True


def execute_notebook_with_login_info(name, workspace_path):

    envs = os.environ.copy()
    envs.update(
        {
            "FINLAB_API_TOKEN": finlab.get_token(),
            "FINLAB_STRATEGY_NAME": name,
        }
    )
    result = execute_ipynb_file(name, workspace_path, envs)
    if not result:
        return False
    return True


def register_notebook_commands(click, nb, workspace_path):

    from finlab.cli.login import _login, set_token

    os.path.isdir(workspace_path) or os.makedirs(workspace_path)

    nb_names = [
        f.split(".ipynb")[0] for f in os.listdir(workspace_path) if f.endswith(".ipynb")
    ]
    choice = click.Choice(nb_names)

    @nb.command()
    @click.argument("name")
    def pull(name):
        """
        Download a notebook from the cloud
        """
        user = _login(workspace_path)
        result = pull_notebook(
            user.data["firebase_login_data"]["firebase_token"],
            user.data["firebase_login_data"]["user_id"],
            name,
            workspace_path,
        )
        if not result["success"]:
            click.echo(f"Failed to pull notebook: {result['error']}")
            return

        click.echo(f"Notebook pulled successfully to {result['file_path']}")

    @nb.command()
    @click.argument("name", type=choice)
    def push(name):
        """
        Upload a notebook to the cloud and override the existing one.
        """
        user = _login(workspace_path)
        result = push_notebook(
            user.data["firebase_login_data"]["firebase_token"],
            user.data["firebase_login_data"]["user_id"],
            name,
            workspace_path,
        )
        if not result["success"]:
            click.echo(f"Failed to push notebook: {result['error']}")
            return

        click.echo(f"Notebook pushed successfully to Firebase")

    @nb.command()
    @click.argument("name")
    def jupyter(name):
        """
        Open Jupyter Lab with the specified notebook.
        """
        user = _login(workspace_path)
        set_token(workspace_path)

        envs = os.environ.copy()
        envs.update({"FINLAB_API_TOKEN": finlab.get_token()})

        nb_path = os.path.join(workspace_path, name + ".ipynb")
        if not os.path.exists(nb_path):
            create_notebook(name, nb_path)

        open_ipynb_file(workspace_path, name, envs)

    @nb.command()
    @click.argument("name")
    def open(name):
        """
        Open the specified notebook in Jupyter Lab.
        """
        user = _login(workspace_path)
        set_token(workspace_path)

        envs = os.environ.copy()
        envs.update({"FINLAB_API_TOKEN": finlab.get_token()})

        nb_path = os.path.join(workspace_path, name + ".ipynb")
        if not os.path.exists(nb_path):
            create_notebook(name, nb_path)

        file_path = os.path.join(workspace_path, name + ".ipynb")
        click.launch(file_path)

    @nb.command()
    @click.argument("name", type=choice)
    def remove(name):
        """
        Remove the specified notebook.
        """
        nb_path = os.path.join(workspace_path, name + ".ipynb")
        if os.path.exists(nb_path):
            os.remove(nb_path)
            click.echo(f"Notebook {name} removed successfully")
        else:
            click.echo(f"Notebook {name} not found")

    @nb.command()
    @click.argument("name", type=choice)
    def run(name):
        """
        Execute the specified notebook.
        """
        user = _login(workspace_path)
        set_token(workspace_path)

        import finlab

        execute_notebook_with_login_info(name, workspace_path)
