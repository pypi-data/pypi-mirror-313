import os
import subprocess
import sys
from pathlib import Path
from .utils import read_resource_file

def is_env_exists(env_name):
    result = subprocess.run(['conda', 'env', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Failed to list conda environments: {result.stderr}")
    env_list = result.stdout.splitlines()
    for env in env_list:
        if env_name in env:
            return True
    return False

def delete_and_create_env(env_name, env_yml_path):
    if is_env_exists(env_name):
        subprocess.run(['conda', 'env', 'remove', '--name', env_name, '-y'], check=True)
    scripts = [
        lambda : subprocess.run(['conda', 'env', 'create', '-f', env_yml_path], check=True),
        lambda : subprocess.run(['python', '-m', 'ipykernel', 'install', '--user', '--name', 'finlab-env'], check=True)
    ]
    for script in scripts:
        r = script()
        if r.returncode != 0:
            print(r.stderr)
            raise RuntimeError("Failed to create environment")

def install_jupyter_lab(workspace_path):
    
    # run jupyter lab workspace import finlab.jupyterlab-workspace

    result = subprocess.run(['conda', 'activate', 'base'], check=True)
    if result.returncode != 0:
        raise RuntimeError("Failed to activate base environment")
    
    is_windows = sys.platform == "win32" or sys.platform == "cygwin"
    if is_windows:
        install_script = os.path.join(workspace_path, 'install_jupyter.bat')
        with open(install_script, 'w') as f:
            f.write(read_resource_file('finlab.cli', 'install_jupyter.bat'))

        result = subprocess.run(['bash', 'install_jupyter.bat'], check=True)
        if result.returncode != 0:
            raise RuntimeError("Failed to install Jupyter Lab")
        os.remove(install_script)
    else:
        install_script = os.path.join(workspace_path, 'install_jupyter.sh')
        with open(install_script, 'w') as f:
            f.write(read_resource_file('finlab.cli', 'install_jupyter.sh'))

        result = subprocess.run(['bash', 'install_jupyter.sh'], check=True)
        if result.returncode != 0:
            raise RuntimeError("Failed to install Jupyter Lab")
        os.remove(install_script)

def create_operational_folder(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)


def register_init_command(click, cli, WORKSPACE_PATH):

    @cli.command()
    def init():
        """
        Initialize the FinLab environment and workspace.

        This command performs the initial setup required to get the FinLab environment
        up and running. It includes the following steps:

        1. Creating the workspace directory:
        - The command creates a directory structure for the workspace where all 
            necessary files and configurations will be stored.

        2. Creating the environment configuration:
        - The command reads the environment configuration (env.yml) from the 
            FinLab resources and writes it to the workspace directory.

        3. Creating and setting up the Conda environment:
        - The command deletes any existing Conda environment named 'finlab-env' 
            and creates a new one based on the environment configuration file.

        4. Installing Jupyter Lab:
        - The command installs Jupyter Lab in the newly created environment to 
            enable interactive notebook operations.

        The command provides feedback to the user through echo statements to indicate
        the progress of each step.

        Usage:
            finlab init
        """
        click.echo('Creating workspace...')
        create_operational_folder(WORKSPACE_PATH)
        env_txt = read_resource_file('finlab.cli', 'env.yml')
        env_config_path = os.path.join(WORKSPACE_PATH, 'env.yml')
        with click.open_file(env_config_path, 'w') as f:
            f.write(env_txt)
        
        click.echo('Workspace created successfully!')

        click.echo('Creating environment...')
        delete_and_create_env('finlab-env', env_config_path)
        os.remove(env_config_path)
        click.echo('Environment created successfully!')

        click.echo('Installing Jupyter Lab...')
        install_jupyter_lab(WORKSPACE_PATH)
        click.echo('Jupyter Lab installed successfully!')