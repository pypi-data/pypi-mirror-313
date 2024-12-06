import sys

import yaml
import click

from datafold_sdk.sdk.utils import prepare_headers, prepare_api_url, post_data


@click.group()
def manager():
    """Monitors management."""


@manager.command()
@click.argument('yaml_file', type=click.Path(exists=True))
@click.option('--dangling-monitors-strategy', type=str, default='ignore',
              help="How to handle monitors not defined in the yaml file: ignore, delete, pause.")
@click.option('--dry-run', is_flag=True, help="Dry run the provisioning")
@click.pass_context
def provision(ctx: click.Context, yaml_file: str, dangling_monitors_strategy: str, dry_run: bool):
    with open(yaml_file, encoding='utf-8') as f:
        config = yaml.safe_load(f)
    headers = prepare_headers(ctx.obj.api_key)
    api_segment = "api/internal/monitors/provision"
    url = prepare_api_url(ctx.obj.host, api_segment)
    resp = post_data(url, json_data={
        'config': config,
        'dangling_monitors_strategy': dangling_monitors_strategy,
        'dry_run': dry_run
    }, headers=headers)
    if not resp.ok:
        print("Failed to provision monitors")
        print(resp.text)
        sys.exit(1)

    provisioning_result = resp.json()
    if dry_run:
        print("Dry run succeeded")
        print(f"Monitors to be created: {len(provisioning_result['created_monitors'])}")
        print(f"Monitors to be updated: {len(provisioning_result['updated_monitors'])}")
        print(f"Monitors to be deleted: {len(provisioning_result['deleted_monitors'])}")
        print(f"Monitors to be paused: {len(provisioning_result['paused_monitors'])}")
    else:
        print("Successfully provisioned monitors:")
        print(f" - created: {len(provisioning_result['created_monitors'])}")
        print(f" - updated: {len(provisioning_result['updated_monitors'])}")
        print(f" - deleted: {len(provisioning_result['deleted_monitors'])}")
        print(f" - paused: {len(provisioning_result['paused_monitors'])}")
