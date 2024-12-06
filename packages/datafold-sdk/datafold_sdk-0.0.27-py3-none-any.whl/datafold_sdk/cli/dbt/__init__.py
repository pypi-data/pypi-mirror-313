import logging
from typing import Optional

import click

from datafold_sdk.sdk.dbt import check_artifacts, check_pks_in_manifest, submit_artifacts, wait_for_completion
from datafold_sdk.sdk.utils import print_table

from datafold_sdk import sdk_log

logger = logging.getLogger(__file__)
logger.addHandler(sdk_log.SDKLogHandler())

RUN_TYPES = ['production', 'pull_request']


@click.group()
@click.pass_context
def manager(ctx):
    """Run datafold dbt --help for the dbt CI integration."""


@manager.command()
@click.option('--ci-config-id',
              help="The ID of the CI config in Datafold (see CI settings screen)",
              type=int,
              required=True)
@click.option('--run-type',
              help="Submit the manifest as either 'production' or 'pull_request'",
              type=click.Choice(RUN_TYPES),
              required=True)
@click.option('--target-folder',
              help="Path to the target folder of the dbt run (default is './target/')",
              required=False,
              default='./target/',
              show_default=True,
              type=click.Path(exists=True))
@click.option('--commit-sha',
              help="Override the commit sha",
              type=str,
              required=False)
@click.option('--run-id',
              help="Specify unique run id to link base and PR builds",
              type=str,
              required=False)
@click.pass_context
def upload(
    ctx,
    ci_config_id: int,
    run_type: str,
    target_folder,
    commit_sha: Optional[str] = None,
    run_id: Optional[str] = None
):
    """Uploads the artifacts of a dbt run."""
    submit_artifacts(
        host=ctx.obj.host,
        api_key=ctx.obj.api_key,
        ci_config_id=ci_config_id,
        run_type=run_type,
        target_folder=click.format_filename(target_folder),
        commit_sha=commit_sha,
        run_id=run_id
    )


@manager.command()
@click.option('--ci-config-id',
              help="The ID of the CI config in Datafold (see CI settings screen)",
              type=int,
              required=True)
@click.option('--run-type',
              help="Submit the manifest as either 'production' or 'pull_request'",
              type=click.Choice(RUN_TYPES),
              required=True)
@click.option('--branch',
              help='Branch',
              type=str,
              required=True)
@click.option('--commit-sha',
              help='The commit sha',
              type=str,
              required=True)
@click.pass_context
def check_post_upload_dbt_artifacts(ctx: click.Context, ci_config_id: int, run_type: str, branch: str, commit_sha: str):
    check_artifacts(
        host=ctx.obj.host,
        api_key=ctx.obj.api_key,
        ci_config_id=ci_config_id,
        run_type=run_type,
        branch=branch,
        commit_sha=commit_sha,
    )


@manager.command()
@click.option('--ci-config-id',
              help="The ID of the CI config in Datafold (see CI settings screen)",
              type=int,
              required=True)
@click.option('--run-type',
              help="Submit the manifest as either 'production' or 'pull_request'",
              type=click.Choice(RUN_TYPES),
              required=True)
@click.option('--target-folder',
              help="Path to the target folder of the dbt run",
              default='./target/',
              show_default=True,
              type=click.Path(exists=True))
@click.option('--timeout',
              help="The maximum wait time in minutes",
              type=int,
              default=60,
              show_default=True,
              required=False)
@click.option('--commit-sha',
              help="Override the commit sha",
              type=str,
              required=False)
@click.pass_context
def upload_and_wait(ctx, ci_config_id: int, run_type: str, target_folder, timeout: int, commit_sha: Optional[str] = None):
    """Uploads the artifacts of dbt and waits for the data diff to complete"""
    sha = submit_artifacts(host=ctx.obj.host,
                           api_key=ctx.obj.api_key,
                           ci_config_id=ci_config_id,
                           run_type=run_type,
                           target_folder=click.format_filename(target_folder),
                           commit_sha=commit_sha)
    # This only makes sense for Pull Requests,
    # otherwise there won't be a PR
    if run_type == 'pull_request':
        wait_for_completion(
            host=ctx.obj.host,
            api_key=ctx.obj.api_key,
            ci_config_id=ci_config_id,
            commit_sha=sha,
            wait_in_minutes=timeout
        )


@manager.command()
@click.option('--ci-config-id',
              help="The ID of the CI config in Datafold (see CI settings screen)",
              type=int,
              required=True)
@click.argument('manifest', type=str)
@click.pass_context
def check_primary_keys(ctx, ci_config_id: int, manifest: str):
    """Checks primary keys for models defined in MANIFEST file."""
    with open(manifest, 'rb') as file:
        data = file.read()

    result = check_pks_in_manifest(
        host=ctx.obj.host,
        api_key=ctx.obj.api_key,
        ci_config_id=ci_config_id,
        manifest=data
    )
    rows = []
    for res in sorted(result, key=lambda x: (x.source, x.dbt_fqn, id(x))):
        rows.append((
            res.source,
            '.'.join(res.dbt_fqn),
            ', '.join(res.sql_pks),
            res.dbt_original_file_path,
            res.dbt_patch_path or '',
            ', '.join(res.warnings),
        ))
    print_table(rows)
