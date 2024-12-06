import io
import os
import time
from datetime import datetime 
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
import contextlib
from .login import _login
from .notebook import execute_notebook_with_login_info


def add_schedule(name, schedule_type, schedule_time, WORKSPACE_PATH):

    user = _login(WORKSPACE_PATH)

    if 'schedule' not in user.data:
        user.data['schedule'] = []

    # prevent same type and name
    for s in user.data['schedule']:
        if s['name'] == name and s['type'] == schedule_type:
            input_value = input("Enter 'y' to override or 'n' to cancel: ")
            if input_value == 'n':
                return
            else:
                user.data['schedule'].remove(s)
                break

    # check schedule_time format
    for t in schedule_time:
        try:
            time.strptime(t, '%H:%M')
        except ValueError:
            raise ValueError(f"Invalid time format: {t}")
    
    user.data['schedule'].append({
        'name': name,
        'type': schedule_type,
        'time': schedule_time
    })

    user.to_file()


def register_schedule_commands(click, schedule, WORKSPACE_PATH):

    nb_names = [f.split('.ipynb')[0] for f in os.listdir(WORKSPACE_PATH) if f.endswith('.ipynb')]
    choice = click.Choice(nb_names)

    @schedule.command()
    @click.argument('name', type=choice)
    @click.argument('times', nargs=-1)
    def nb(name, times):
        """Schedule a notebook to run at a specific time."""
        schedule_type = 'notebook'
        add_schedule(name, schedule_type, times, WORKSPACE_PATH=WORKSPACE_PATH)

    @schedule.command()
    @click.argument('name', default='default')
    @click.argument('times', nargs=-1)
    def pm(name, times):
        """Schedule a portfolio to sync at a specific time."""
        schedule_type = 'portfolio'
        add_schedule(name, schedule_type, times, WORKSPACE_PATH)

    @schedule.command()
    @click.argument('type', type=click.Choice(['nb', 'pm']))
    @click.argument('name')
    def remove(type, name):
        """Remove a schedule."""

        type = 'notebook' if type == 'nb' else 'portfolio'
        user = _login(WORKSPACE_PATH)
        if 'schedule' not in user.data:
            click.echo('No schedules found')
            return

        for s in user.data['schedule']:
            if s['name'] == name and s['type'] == type:
                user.data['schedule'].remove(s)
                user.to_file()
                click.echo(f"Schedule {name} removed successfully")
                return

        click.echo(f"Schedule {name} not found")

    @schedule.command()
    def list():
        """List all schedules."""
        user = _login(WORKSPACE_PATH)
        if 'schedule' not in user.data:
            click.echo('No schedules found')
            return

        for s in user.data['schedule']:
            click.echo(f"{s['name']} - {s['type']} - {s['time']}")

    @schedule.command()
    def run():
        """Run all schedules."""
        user = _login(WORKSPACE_PATH)
        schedules = user.data['schedule']

        from finlab.cli.portfolio_sync_manager import update_portfolio_with_login, sync_portfolio_with_login
        from finlab.cli.login import set_token


        run_records = {s['name']: {"last_run": "Never", "success": "N/A", "stdout": "N/A", "stderr": "N/A"} for s in schedules}

        def record_run(name, func):

            f_stdout = io.StringIO()
            f_stderr = io.StringIO()

            with contextlib.redirect_stdout(f_stdout), contextlib.redirect_stderr(f_stderr):
                try:
                    func(name)
                except:
                    pass

            run_records[name]['last_run'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            run_records[name]['success'] = "Success" if func(name) else "Fail"
            run_records[name]['stdout'] = f_stdout.getvalue().strip()
            run_records[name]['stderr'] = f_stderr.getvalue().strip()


        def update_notebook(name):

            set_token(WORKSPACE_PATH)
            print(f"Running notebook: {name}")
            return execute_notebook_with_login_info(name, WORKSPACE_PATH)

        def update_portfolio(name):

            set_token(user.data['firebase_login_data']['api_token'])
            result1 = update_portfolio_with_login(name)
            result2 = sync_portfolio_with_login(WORKSPACE_PATH, name)
            return result1 and result2

        console = Console()

        def highlight(text, color):
            return f"[{color}]{text}[/{color}]"
        
        def highlight_success(text):
            if text == "Success":
                return highlight(text, 'green')
            elif text == "Fail":
                return highlight(text, 'red')
            
            return highlight(text, 'blue')

        def display_schedule():
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            table = Table(title="FinLab Backtesting Scheduler", show_header=True, 
                          caption=f"current time: [bold][yellow]{current_time}[/yellow][/bold]",
                          title_justify='left', caption_justify='left')
            table.add_column("Event", justify="center")
            table.add_column("type", justify="center")
            table.add_column("Scheduled Time", justify="center")
            table.add_column("Last Run", justify="center")
            table.add_column("Success", justify="center")

            next_run = schedule.next_run()
            next_event = next((s for s in schedules if any(next_run.strftime('%H:%M') == t for t in s['time'])), None)
            next_event_name = next_event['name'] if next_event else "None"

            for schedule_data in schedules:
                for time_str in schedule_data['time']:
                    if time_str == next_run.strftime('%H:%M'):
                        table.add_row(highlight(schedule_data['name'], 'green'), schedule_data['type'], f"[bold][green]{time_str}[/green][/bold]", run_records[schedule_data['name']]["last_run"], highlight_success(run_records[schedule_data['name']]["success"]))
                    else:
                        table.add_row(schedule_data['name'], schedule_data['type'], time_str, run_records[schedule_data['name']]["last_run"], highlight_success(run_records[schedule_data['name']]["success"]))

            console.clear()
            console.print(table)


        import schedule

        for s in schedules:
            for t in s['time']:
                if s['type'] == 'notebook':
                    schedule.every().day.at(t).do(record_run, s['name'], update_notebook)
                elif s['type'] == 'portfolio':
                    schedule.every().day.at(t).do(record_run, s['name'], update_portfolio)
                else:
                    raise ValueError(f"Unknown schedule type: {s['type']}")
        while True:
            display_schedule()
            time.sleep(10)
            schedule.run_pending()
