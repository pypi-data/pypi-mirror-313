import os
import rich_click as click

WORKSPACE_PATH = os.path.join("workspace")

from finlab.cli.workspace import register_init_command
from finlab.cli.login import register_auth_commands
from finlab.cli.broker import register_broker_commands
from finlab.cli.portfolio_sync_manager import register_pm_command
from finlab.cli.notebook import register_notebook_commands
from finlab.cli.schedule import register_schedule_commands

@click.group()
def cli():
    """
    Command Line Interface (CLI) for FinLab.

    This CLI provides various commands to manage the FinLab environment, 
    including operations for authentication, broker management, notebook 
    operations, portfolio management, and scheduling tasks. The main command 
    group (cli) serves as the entry point for all subcommands and subgroups.
    """
    pass

@cli.group()
def auth():
    """
    Authentication operations for FinLab.

    This command group handles user authentication tasks, including login and 
    logout operations. The commands in this group ensure secure access to 
    FinLab resources by managing user credentials and session information.
    """
    pass

@cli.group()
def broker():
    """
    Broker operations for managing broker accounts in FinLab.

    This command group includes commands for adding, listing, testing, and 
    removing broker accounts. It allows users to manage their broker 
    integrations and perform necessary operations to ensure seamless 
    communication between FinLab and their brokerage accounts.
    """
    pass

@cli.group()
def nb():
    """
    Notebook operations for strategies.

    

    This command group includes commands for managing Jupyter notebooks within 
    the FinLab environment. Users can pull notebooks from the cloud, push 
    local notebooks to the cloud, open notebooks in Jupyter Lab, remove 
    notebooks, and execute notebooks.
    """
    pass

@cli.group()
def pm():
    """
    Portfolio manager operations for FinLab.

    This command group includes commands for managing portfolios that sync 
    with broker accounts. Users can create new portfolios, update existing 
    portfolios, check the status of portfolios, and sync portfolios with their 
    broker accounts.
    """
    pass

@cli.group()
def schedule():
    """
    Schedule tasks for automated operations in FinLab.

    This command group includes commands for scheduling tasks to run 
    automatically at specified times. Users can schedule notebook executions 
    and portfolio synchronizations, list all scheduled tasks, and remove 
    specific scheduled tasks.
    """
    pass

register_init_command(click, cli, WORKSPACE_PATH)
register_auth_commands(click, auth, WORKSPACE_PATH)
register_broker_commands(click, broker, WORKSPACE_PATH)
register_notebook_commands(click, nb, WORKSPACE_PATH)
register_pm_command(click, pm, WORKSPACE_PATH)
register_schedule_commands(click, schedule, WORKSPACE_PATH)


if __name__ == "__main__":
    cli()