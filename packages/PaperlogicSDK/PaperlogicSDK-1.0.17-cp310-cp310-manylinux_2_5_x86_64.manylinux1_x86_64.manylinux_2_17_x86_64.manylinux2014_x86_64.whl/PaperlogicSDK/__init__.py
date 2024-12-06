import click
import sys
from .sign import sign_pplg
from .timestamp import timestamp_pplg, timestamp_test

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    pass

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option('-pki', '--pki', type=int, help='Certificate Type', required=True, default=0)
@click.option('-uid', '--user_id', type=int, help='UserID')
@click.option('-e', '--email', type=str, help='Email')
@click.option('-pwd', '--pdf_password', type=str, help='PDF File Password')
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)

def sign(input_file, output_file, api_token, tenant_id, pki, user_id=None, email=None, environment='stg', pdf_password=None):
    """Sign document"""
    if environment == 'dev':
        click.echo("Development mode activated")
    elif environment == 'stg':
        click.echo("Staging mode activated")
    elif environment == 'prod':
        click.echo("Production mode activated")

    click.echo("Start Signing")

    kwargs = {'pdf_password': pdf_password} if pdf_password else {}
    res, msg = sign_pplg(input_file, output_file, api_token, tenant_id, pki, user_id, email, environment, **kwargs)

    if res:
        click.echo(f"Status: success")
        sys.exit(0)
    else:
        if msg == 'error.password.required':
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.password.incorrect \n
                    ErrorMessage: PDF file's password is not correct. Please provide correct password.''', 
                err=True
            )
        elif msg == 'error.pki.user_id.required':
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.pki.user_id.required \n
                    ErrorMessage: Sign by company seal requires user_id (group_id).''', 
                err=True
            )
        else:
            click.echo(f"Status: failure", err=True)
        sys.exit(1)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option('-pwd', '--pdf_password', type=str, help='PDF File Password')
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)
def timestamp(input_file, output_file, api_token, tenant_id, environment='stg', pdf_password=None):
    """Timestamp document"""
    if environment == 'dev':
        click.echo("Development mode activated")
    elif environment == 'stg':
        click.echo("Staging mode activated")
    elif environment == 'prod':
        click.echo("Production mode activated")

    click.echo(f"Start Timestamp")

    kwargs = {'pdf_password': pdf_password} if pdf_password else {}
    res, msg = timestamp_pplg(input_file, output_file, api_token, tenant_id, environment, **kwargs)

    if res:
        click.echo(f"Status: success")
        sys.exit(0)
    else:
        if msg == 'error.password.required':
            click.echo(f'''
                    Status: failure. \n 
                    Error: error.password.incorrect \n
                    ErrorMessage: PDF file's password is not correct. Please provide correct password.''', 
                err=True
            )
        else:
            click.echo(f"Status: failure", err=True)
        sys.exit(1)

@cli.command()
@click.option('-i', '--input_file', type=str, help='File input', required=True)
@click.option('-o', '--output_file', type=str, help='File output', required=True)
@click.option('-tk', '--api_token', type=str, help='API Token', required=True)
@click.option('-t', '--tenant_id', type=int, help='TenantID', required=True)
@click.option(
    '-env', '--environment',
    type=click.Choice(['dev', 'stg', 'prod'], case_sensitive=False),
    default='stg',
    help='Environment to run the SDK (dev/stg/prod)'
)
def testtimestamp(input_file, output_file, api_token, tenant_id, environment='stg'):
    """Test timestamp document"""
    click.echo(f"Start Timestamp")
    
    res = timestamp_test(input_file, output_file, api_token, tenant_id, environment)

    if res:
        click.echo(f"Status: success")
        sys.exit(0)
    else:
        click.echo(f"Status: failure", err=True)
        sys.exit(1)