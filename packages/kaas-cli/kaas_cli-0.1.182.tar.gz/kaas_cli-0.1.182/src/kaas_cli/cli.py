from __future__ import annotations

import json
import sys
from dataclasses import asdict
from typing import TYPE_CHECKING

import click
import click.exceptions

from kaas_cli import __version__

from .client import KaasClient
from .config import DEFAULT_DIRECTORY, DEFAULT_TOKEN, SERVER_URL, CustomHelpOption
from .run_kontrol import RunKontrol
from .types import KontrolVersion
from .utils import get_foundry_out_dir

if TYPE_CHECKING:
    from click.core import Context


@click.group()
@click.version_option(version=__version__, prog_name='kaas-cli')
@click.pass_context
def cli(
    ctx: Context,
) -> None:
    """KaaS Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj["client"] = KaasClient(
        url=SERVER_URL,
    )


@cli.command(
    cls=CustomHelpOption,
    help="Upload proofs to the remote server. VAULT_SPEC should be in the format <ORG_NAME>/<VAULT_NAME>:<TAG>",
)
@click.argument('vault_spec', required=True)
@click.option(
    "-d",
    "--directory",
    default='',
    show_default=True,
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
    help="Directory containing proofs to upload",
)
@click.option("--url", "-u", required=False, default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", required=False, default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.option("--tag", required=False, help="Tag of the version to upload")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Show verbose output")
@click.pass_context
def upload(
    ctx: Context, vault_spec: str, directory: str, url: str, token: str | None, tag: str | None, verbose: bool
) -> None:
    try:
        org_name, vault_and_tag = vault_spec.split('/')
        vault_name, tag_name = vault_and_tag.split(':')
    except ValueError:
        click.echo("Invalid vault specification. Use the format orgName/vaultName:tag or @orgName/vaultName:tag")
        return

    try:
        ctx.ensure_object(dict)
        client: KaasClient = KaasClient(url=url, token=token, vault=vault_name, org=org_name)
        ctx.obj["client"] = client
        if not directory:
            directory = get_foundry_out_dir()
        response_message = client.upload_files_s3(directory=directory, tag=tag_name or tag, verbose=verbose)
        if verbose:
            click.echo(response_message)
    except Exception as e:
        click.echo(e)
        sys.exit(1)


@cli.command(
    cls=CustomHelpOption,
    help="Download proofs from the remote server. VAULT_SPEC should be in the format <ORG_NAME>/<VAULT_NAME>:<TAG> or @<ORG_NAME>/<VAULT_NAME>:<TAG>",
)
@click.argument("vault_spec", required=True)
@click.option(
    "-d",
    "--directory",
    default='',
    show_default=True,
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
    help="Directory to save downloaded proofs",
)
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.option("--verbose", "-v", is_flag=True, default=False, help="Show verbose output")
@click.pass_context
def download(
    ctx: Context,
    vault_spec: str,
    directory: str,
    url: str,
    token: str | None,
    verbose: bool,
) -> None:
    try:
        org_name, vault_and_tag = vault_spec.split('/')
        vault_name, tag_name_or_file_name = vault_and_tag.split(':')
    except ValueError:
        click.echo("Invalid vault specification. Use the format orgName/vaultName:tag or @orgName/vaultName:tag")
        return None

    if not org_name or not vault_name:
        click.echo(
            "Invalid vault specification. Use the format orgName/vaultName:tag or @orgName/vaultName:tag",
        )
        return None
    ctx.ensure_object(dict)
    client: KaasClient = KaasClient(url=url, token=token, vault=vault_name, org=org_name)
    ctx.obj["client"] = client
    if not directory:
        directory = get_foundry_out_dir()
    if not tag_name_or_file_name:
        message = client.download_latest_version(org_name, vault_name, target_directory=directory, verbose=verbose)
        if verbose:
            click.echo(message)
        return None

    try:
        message = client.download_version_or_tag(
            org_name, vault_name, tag_name_or_file_name, target_directory=directory, verbose=verbose
        )
        if verbose:
            click.echo(message)
        return None
    except ValueError:
        click.echo("Invalid vault specification. Use the format orgName/vaultName:tag")
        return None


@cli.command(cls=CustomHelpOption, help="Say hello.")
@click.option("-n", "--name", default="World", show_default=True, help="Name to say hello to")
@click.pass_context
def hello(ctx: Context, name: str) -> None:
    client: KaasClient = ctx.obj["client"]
    client.hello(name=name)


@cli.command(cls=CustomHelpOption, help="Login to the system.")
@click.pass_context
def login(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    data = client.login()
    click.echo(f"Your user code: {data.user_code}")
    click.echo(f"Open the link and type your code {data.verification_uri}")
    click.echo("Then hit 'enter'")
    input_value = click.prompt("Press Enter to continue or type 'q' to quit", default="", show_default=False)
    if input_value.lower() == 'q':
        click.echo("You left authentication")
        sys.exit(1)
        return
    click.echo("You pressed Enter. The application continues...")
    confirm_success = client.confirm_login(data.device_code).success
    if not confirm_success:
        click.echo("Authentication failed")
        sys.exit(1)
        return
    click.echo("Access token received. We store it in cache folder")


@cli.command(cls=CustomHelpOption, help="List local proofs.", aliases=['l', 'ls'])
@click.option(
    "-d",
    "--directory",
    default=DEFAULT_DIRECTORY,
    show_default=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory to list local proofs",
)
@click.option("--remote", is_flag=True, help="List remote proofs instead of local proofs", default=False)
@click.pass_context
def list(ctx: Context, directory: str = DEFAULT_DIRECTORY, remote: bool = False) -> None:
    client: KaasClient = ctx.obj["client"]
    if remote:
        proofs = client.list_remote()
    else:
        proofs = client.list_local_proofs(directory=directory)
    if not proofs:
        click.echo('No proofs found')
    for proof in proofs:
        click.echo(proof)


@cli.command(cls=CustomHelpOption, help="List remote vaults.")
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.pass_context
def list_vaults(ctx: Context, token: str, url: str) -> None:
    client: KaasClient = KaasClient(url=url, token=token)
    vaults = client.list_vaults()
    for vault in vaults:
        if isinstance(vault, dict):
            org_name = vault.get('organization', {}).get('name', 'Unknown')
            vault_name = vault.get('name', 'Unknown')
            click.echo(f"{org_name}/{vault_name}")
        else:
            click.echo("Invalid vault structure received.")


@cli.command(cls=CustomHelpOption, help="List you organizations.")
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.pass_context
def list_orgs(ctx: Context, token: str, url: str) -> None:
    client: KaasClient = KaasClient(url=url, token=token)
    orgs = client.list_orgs()
    for org in orgs:
        if isinstance(org, dict):
            org_name = org.get('name', 'Unknown')
            click.echo(f"{org_name}")
        else:
            click.echo("Invalid vault structure received.")


@cli.command(
    cls=CustomHelpOption,
    name="list-caches",
    help="""List remote caches.\n
    $ kaas-cli list-caches <ORG_NAME>/<VAULT_NAME>""",
)
@click.argument("org_vault", required=True)
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.pass_context
def list_caches(ctx: Context, org_vault: str, token: str, url: str) -> None:
    click.echo(f"Default Token: {DEFAULT_TOKEN}")
    client: KaasClient = KaasClient(url=url, token=token)
    org_name, vault_name = org_vault.split('/')
    caches = client.list_caches(org_name, vault_name)
    click.echo(json.dumps([asdict(cache) for cache in caches], indent=2))


@cli.command(cls=CustomHelpOption, name="check-auth", help="Check authentication status.")
@click.option("--url", "-u", default=SERVER_URL, show_default=True, help="Server URL")
@click.option("--token", "-t", default=DEFAULT_TOKEN, help="Personal access key for vault")
@click.pass_context
def check_auth(ctx: Context, token: str, url: str) -> None:
    client: KaasClient = KaasClient(url=url, token=token)
    error_message = f"Authentication failed, please use {click.style('--token', fg='red')} flag or {click.style('kaas-cli login', fg='red')} to authenticate."
    try:
        is_authenticated = client.check()
        if is_authenticated:
            click.echo("You are currently authenticated.")
        else:
            click.echo(error_message)
            sys.exit(1)
    except Exception:
        click.echo(error_message)
        sys.exit(1)


@cli.command(cls=CustomHelpOption, name="logout", help="Log out from the system.")
@click.pass_context
def logout(ctx: Context) -> None:
    client: KaasClient = ctx.obj["client"]
    logout_success = client.logout()
    if logout_success:
        click.echo("You have been logged out successfully.")
    else:
        click.echo("Logout failed. You may not be logged in.")


@cli.command(
    cls=CustomHelpOption,
    name="run",
    help="Run Proofs locally, in a container or remotely on kaas provided compute machines",
)
@click.option(
    "--mode",
    "-m",
    required=False,
    default="local",
    show_default=True,
    help="Mode to run the command in: local, remote, or container",
    type=click.Choice(['local', 'remote', 'container'], case_sensitive=False),
)
@click.option(
    "--watch",
    "-w",
    required=False,
    default=False,
    is_flag=True,
    help="Watch the job execution status. Wait until the job is completed",
)
@click.option(
    "--kontrol-version",
    "-kv",
    required=False,
    default="v0.0.0",
    show_default=True,
    help="Version of Kontrol to run",
    type=KontrolVersion(),
)
@click.option(
    "--url",
    "-u",
    required=False,
    default=SERVER_URL,
    show_default=True,
    help="API Server URL",
)
@click.option(
    "--vault-spec",
    "-vs",
    "vault",
    required=False,
    help="Organization and vault to use for remote mode. VAULT_SPEC should be in the format <ORG_NAME>/<VAULT_NAME>",
)
@click.option(
    "--token",
    "-t",
    required=False,
    help="Personal access key for vault. See https://kaas.runtimeverification.com/app/profile/keys",
)
@click.option(
    "--branch",
    "-b",
    required=False,
    help="Git repository branch to use for remote mode",
)
@click.option("--extra-build-args", "-eb", required=False, help="Extra arguments to build the proof")
@click.option("--extra-prove-args", "-ep", required=False, help="Extra arguments to pass to Kontrol's prove command")
@click.pass_context
def run(
    ctx: Context,
    mode: str,
    kontrol_version: KontrolVersion,
    url: str,
    vault: str,
    token: str,
    branch: str,
    extra_build_args: str,
    extra_prove_args: str,
    watch: bool,
) -> None:
    click.echo(f"Running Kontrol in {mode} mode")
    if mode == "remote":
        if not all([vault, token, branch]):
            missing_args = []
            if not vault:
                missing_args.append("--vault-spec VAULT_SPEC")
            if not token:
                missing_args.append("--token PERSONAL_KEY")
            if not branch:
                missing_args.append("--branch GIT_BRANCH")
            click.echo(f"You must provide all of the following options: {', '.join(missing_args)}")
            sys.exit(1)
        try:
            org_name, vault_name = vault.split('/')
        except ValueError:
            click.echo("Invalid vault specification. Use the format orgName/vaultName or @orgName/vaultName")
            sys.exit(1)
        ctx.ensure_object(dict)
        client: KaasClient = KaasClient(url=url, token=token, vault=vault_name, org=org_name)
        ctx.obj["client"] = client
        is_authenticated = client.check()
        if not is_authenticated:
            click.echo("You are not authenticated. Please use 'kaas-cli login' to authenticate.")
            click.echo(
                "Check kaas token is enabled in your account. https://kaas.runtimeverification.com/app/profile/keys"
            )
            sys.exit(1)
        run_kontrol = RunKontrol(
            kontrol_version, mode, extra_build_args, extra_prove_args, org_name, vault_name, branch, client, watch
        )
        if run_kontrol.run():
            click.echo("Kontrol ran successfully...")
            return None
        else:
            click.echo("An error occurred while running Kontrol")
            sys.exit(1)
    else:
        run_kontrol = RunKontrol(kontrol_version, mode, extra_build_args, extra_prove_args, watch=watch)
        if run_kontrol.run():
            click.echo("Kontrol ran successfully...")
            return None
        else:
            click.echo("An error occurred while running Kontrol")
            sys.exit(1)
