from .data_encryptor import DataEncryptor
from configparser import ConfigParser
from .form_factory import create_user_form
import click
import os


def config_to_json(config_file):
    config = ConfigParser()
    config.read(config_file)
    
    return {section: dict(config.items(section)) for section in config.sections()}

def encode_file_to_string(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return file_content.decode('latin1')

def decode_string_to_file(encoded_string, output_path):
    decoded_content = encoded_string.encode('latin1')
    with open(output_path, 'wb') as file:
        file.write(decoded_content)

def check_and_fill_envs(broker_type):
    if broker_type == 'sinopac':
        env_names = {
            'SHIOAJI_API_KEY': 'password',
            'SHIOAJI_SECRET_KEY': 'password',
            'SHIOAJI_CERT_PERSON_ID': 'password',
            'SHIOAJI_CERT_PASSWORD': 'password',
            'SHIOAJI_CERT_PATH': 'file'
        }
    elif broker_type == 'fugle':
        env_names = {
            'FUGLE_CONFIG_PATH': 'file',
            'FUGLE_MARKET_API_KEY': 'password',
            'FUGLE_ACCOUNT_PASSWORD': 'password',
            'FUGLE_CERT_PASSWORD': 'password',
        }

    delisted = []

    for env_name in env_names:
        if env_name in os.environ:
            delisted.append(env_name)

    for env_name in delisted:
        env_names.pop(env_name)

    if len(env_names):

        form_data = create_user_form(env_names)

        if form_data['action'] == 'save':
            for env_name, value in form_data.items():
                os.environ[env_name] = value
            return True
        else:
            return False
        
    return True
    

        
def add_broker(broker, WORKSPACE_PATH='.', name='default'):
    if broker == 'fugle':
        try:
            from fugle_trade.sdk import SDK
        except ImportError:
            click.echo("Failed to add broker: package not installed. Please run 'pip install fugle-trade'")
            return False
        from finlab.online.fugle_account import FugleAccount
        constructor = FugleAccount
    elif broker == 'sinopac':
        try:
            import shioaji
        except ImportError:
            click.echo("Failed to add broker: package not installed. Please run 'pip install shioaji'")
            return False
        from finlab.online.sinopac_account import SinopacAccount
        constructor = SinopacAccount
    else:
        raise ValueError(f"Broker {broker} is not supported")

    success = check_and_fill_envs(broker)
    print(success, 'test')
    if not success:
        return False

    try:
        account = constructor()
        click.echo(f"Broker {name} added successfully")
    except Exception as e:
        click.echo(f"Failed to add broker: {e}")
        return False
    
    # encrypt account login info

    if broker == 'sinopac':
        from finlab.online.sinopac_account import SinopacAccount
        try:
            SinopacAccount()
        except:
            click.echo("Failed to add broker: Sinopac account cannot be initialized. Please check your environment variables.")
            return
        env_names = ['SHIOAJI_API_KEY', 'SHIOAJI_SECRET_KEY', 'SHIOAJI_CERT_PERSON_ID', 'SHIOAJI_CERT_PASSWORD']
        file_path = {
            'SHIOAJI_CERT_PATH': os.environ['SHIOAJI_CERT_PATH']
        }
        config_data = {}
    elif broker == 'fugle':
        from configparser import ConfigParser
        from finlab.online.fugle_account import FugleAccount
        from fugle_trade.util import setup_keyring, ft_get_password

        try:
            FugleAccount()
        except:
            click.echo("Failed to add broker: Fugle account cannot be initialized. Please check your environment variables.")
            return

        config = ConfigParser()
        config.read(os.environ['FUGLE_CONFIG_PATH'])

        os.environ['FUGLE_ACCOUNT'] = config['User']['Account']
        os.environ['FUGLE_ACCOUNT_PASSWORD'] = ft_get_password("fugle_trade_sdk:account", config['User']['Account'])
        os.environ['FUGLE_CERT_PASSWORD'] = ft_get_password("fugle_trade_sdk:cert", config['User']['Account'])

        env_names = ['FUGLE_MARKET_API_KEY', 'FUGLE_ACCOUNT', 'FUGLE_ACCOUNT_PASSWORD', 'FUGLE_CERT_PASSWORD']

        file_path = {
            'certificate': config.get('Cert', 'Path')
        }

        config_data = {

            'Core': {
                'Entry': config.get('Core', 'Entry'),
            },
            'Cert': {
                'Path': config.get('Cert', 'Path'),
            },
            'Api': {
                'Key': config.get('Api', 'Key'),
                'Secret': config.get('Api', 'Secret'),
            },
            'User': {
                'Account': config.get('User', 'Account'),
            },
        }

    broker_data = {
        'env': {env_name: os.environ[env_name] for env_name in env_names},
        'config': config_data,
        'files': {name: (path.split('.')[-1], encode_file_to_string(path)) for name, path in file_path.items()},
        'broker_name': broker,
        'name': name
    }

    user = DataEncryptor.from_file(os.path.join(WORKSPACE_PATH, 'user.txt'))
    if 'broker' not in user.data:
        user.data['broker'] = {}
    user.data['broker'][broker_data['name']] = broker_data
    user.to_file()
    return True


def create_account_from_broker_info(info, WORKSPACE_PATH='.'):

    name = info['name']

    # setting env from info
    os.environ.update(info['env'])

    # setting file path
    if 'files' in info:
        account_path = os.path.join(WORKSPACE_PATH, f'{name}_account')
        if not os.path.exists(account_path):
            os.mkdir(account_path)

        for name, (postfix, content) in info['files'].items():
            file_path = os.path.join(account_path, f'{name}.{postfix}')
            decode_string_to_file(content, file_path)
            os.environ[name] = file_path

    if info['broker_name'] == 'fugle':

        # create ini file
        from configparser import ConfigParser
        config = ConfigParser()

        config['Core'] = info['config']['Core']
        config['Cert'] = info['config']['Cert']
        config['Api'] = info['config']['Api']
        config['User'] = info['config']['User']
        config['Cert']['Path'] = os.path.join(account_path, f'certificate.p12')

        with open(os.path.join(account_path, 'config.ini'), 'w') as f:
            config.write(f)

        os.environ['FUGLE_CONFIG_PATH'] = os.path.join(account_path, 'config.ini')

        from finlab.online.fugle_account import FugleAccount
        from fugle_trade.util import set_password, setup_keyring

        aid = config["User"]["Account"]
        setup_keyring(aid)
        set_password("fugle_trade_sdk:account", aid, os.environ['FUGLE_ACCOUNT_PASSWORD'])
        set_password("fugle_trade_sdk:cert", aid, os.environ['FUGLE_CERT_PASSWORD'])

        account = FugleAccount()
    else:
        from finlab.online.sinopac_account import SinopacAccount
        account = SinopacAccount()

    # remove all the files
    if 'files' in info:
        for name, (postfix, content) in info['files'].items():
            file_path = os.path.join(account_path, f'{name}.{postfix}')
            os.remove(file_path)

    return account


def register_broker_commands(click, broker, WORKSPACE_PATH):

    from finlab.cli.login import _login

    @broker.command()
    @click.argument('name', default='default')
    @click.option('--broker')
    def add(name, broker):

        """Add a broker account."""

        if name == 'default':
            name = broker

        user = _login(WORKSPACE_PATH)
        success = add_broker(broker, WORKSPACE_PATH, name)
        if not success:
            click.echo(f"Failed to add broker {name}")
        else:
            click.echo(f"Broker {name} added successfully")


    @broker.command()
    def list():

        """List all brokers."""
        user = _login(WORKSPACE_PATH)
        broker_names = user.data['broker'].keys()
        for broker in broker_names:
            click.echo(broker)


    @broker.command()
    def test():
        """Test all brokers."""
        user = _login(WORKSPACE_PATH)
        for name, broker_info in user.data['broker'].items():
            try:
                account = create_account_from_broker_info(broker_info)
                click.echo(f"Broker {name} tested successfully")
            except Exception as e:
                import traceback
                traceback.print_exc()
                click.echo(f"Failed to test broker {name}: {e}")
        
        click.echo(user.data['firebase_login_data']['api_token'])


    @broker.command()
    @click.argument('name', default='default')
    @click.option('--broker')
    def remove(name):
        
        """Remove a broker account."""

        user = DataEncryptor.from_file(os.path.join(WORKSPACE_PATH, 'user.txt'))
        if name in user.data['broker']:
            user.data['broker'].pop(name, None)
            user.to_file()
            click.echo(f"Broker {name} removed successfully")
        else:
            click.echo(f"Broker {name} not found")