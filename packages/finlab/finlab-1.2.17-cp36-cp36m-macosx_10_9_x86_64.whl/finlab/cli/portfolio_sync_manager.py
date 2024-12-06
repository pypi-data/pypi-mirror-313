import os
import finlab
from .login import _login, set_token
from finlab.portfolio import PortfolioSyncManager, create_report_from_cloud, Portfolio
from .broker import create_account_from_broker_info

def update_portfolio_with_login(name):

    p = PortfolioSyncManager.from_cloud(name)

    if not 'config' in p.data:
        print('No config found, please create a portfolio first.')
        return

    reports = {}    
    for name, weight in p.data['config']['weights'].items():
        report = create_report_from_cloud(name)
        if not report:
            print(f"Failed to create report for {name}")
            return
        reports[name] = (report, weight)

    params = p.data['config']['params']
    kwargs = params.pop('kwargs', {})
    params.update(kwargs)

    p.update(Portfolio(reports), **params)
    p.to_cloud(name)
    return True

def sync_portfolio_with_login(workspace_path, name, broker_name=None, consider_margin_as_asset=True):

    user = _login(workspace_path)

    os.environ['FINLAB_API_TOKEN'] = user.data['firebase_login_data']['api_token']
    if 'broker' not in user.data:
        print('No broker found, please add a broker first.')
        return False

    try:
        p = PortfolioSyncManager.from_cloud(name)
    except:
        print(f'No portfolio {name} found, please create a portfolio first.')
        return False


    if 'broker_name' not in p.data['config'] and not broker_name:
        print('No broker name found in the portfolio config.')
        return False
    
    broker_name = broker_name or p.data['config']['broker_name']

    p.data['config']['broker_name'] = broker_name

    account = create_account_from_broker_info(user.data['broker'][broker_name])
    p.sync(account, consider_margin_as_asset=consider_margin_as_asset)

    p.to_cloud(name)

    print(f'Portfolio {name} synced successfully.')
    return True


def register_pm_command(click, pm, WORKSPACE_PATH):

    from finlab.cli.login import _login
    @pm.command()
    @click.argument('weights', nargs=-1)
    @click.option('--name', default='default', type=str, help='name of the portfolio manager')
    @click.option('--total_balance', default=0, type=int, help='Total balance.')
    @click.option('--rebalance_safety_weight', default=0.2, type=float, help='Rebalance safety weight.')
    @click.option('--smooth_transition', default=True, type=bool, help='Smooth transition.')
    @click.option('--force_override_difference', default=False, type=bool, help='Force override difference.')
    @click.option('--margin_trading', default=False, type=bool, help='Margin trading.')
    def create(weights, name, total_balance, rebalance_safety_weight, smooth_transition, force_override_difference, margin_trading):
        """Create a portfolio manager with the given strategy weights."""
        

        user = _login(WORKSPACE_PATH)
        api_token = user.data['firebase_login_data']['api_token']
        os.environ['FINLAB_API_TOKEN'] = api_token

        result = {}
        weights = {weights[i]: float(weights[i+1]) for i in range(0, len(weights), 2)}
        for report_name, weight in weights.items():
            report = create_report_from_cloud(report_name)
            result[report_name] = (report, weight)

        if name:

            try:
                PortfolioSyncManager.from_cloud(name)
                raise ValueError(f"Portfolio {name} already exists")
            except:
                pass

            psm = PortfolioSyncManager()
            psm.update(Portfolio(result), total_balance=total_balance, 
                            rebalance_safety_weight=rebalance_safety_weight,
                            smooth_transition=smooth_transition,
                            force_override_difference=force_override_difference, 
                            margin_trading=margin_trading)
            
            psm.to_cloud(name)

    @pm.command()
    @click.argument('name', default='default')
    def update(name):
        """Update the portfolio with the given name."""
        set_token(WORKSPACE_PATH)
        update_portfolio_with_login(name)

    @pm.command()
    @click.argument('name', default='default')
    def status(name):

        """Prints the status of the portfolio."""
        user = _login(WORKSPACE_PATH)
        api_token = user.data['firebase_login_data']['api_token']
        os.environ['FINLAB_API_TOKEN'] = api_token

        p = PortfolioSyncManager.from_cloud(name)
        click.echo(p.__str__())


    @pm.command()
    @click.argument('name', default='default')
    @click.option('--broker', default=None, help='Name of the broker to sync with.')
    @click.option('--consider_margin_as_asset', default=True, type=bool, help='Consider margin as asset.')
    def sync(name, broker, consider_margin_as_asset):
        """Sync the portfolio with the broker account."""
        sync_portfolio_with_login(WORKSPACE_PATH, name, broker, consider_margin_as_asset)

