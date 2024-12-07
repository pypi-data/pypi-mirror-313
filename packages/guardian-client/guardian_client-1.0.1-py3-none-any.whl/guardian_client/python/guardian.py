import json
import sys
import os

from guardian_client.python.api import GuardianAPIClient
import click
import pkg_resources

client_version = pkg_resources.get_distribution("guardian-client").version


GUARDIAN_ENDPOINT = os.getenv("GUARDIAN_ENDPOINT")
LOW, MEDIUM, HIGH, CRITICAL = "low", "medium", "high", "critical"
CRITICAL, ERROR, INFO, DEBUG = "critical", "error", "info", "debug"


@click.group()
@click.version_option(client_version, "-v", "--version")
@click.option(
    "--base-url",
    default=GUARDIAN_ENDPOINT,
    help="Base URL of the Guardian API. Overrides environment variable if set.",
)
@click.option(
    "--block-on-scan-errors",
    is_flag=True,
    help="Block if the scanning process failed on an incomplete scan",
)
@click.option(
    "--report-only",
    is_flag=True,
    help="Generate a JSON report only without evaluating scan results",
)
@click.option("--silent", is_flag=True, help="Do not print anything to stdout")
@click.option(
    "--log-level",
    default=INFO,
    type=str,
    required=False,
    help="Logging level if not silent (critical, error, info, debug)",
)
@click.pass_context
def cli(
    ctx,
    base_url: str,
    block_on_scan_errors: bool = True,
    report_only: bool = False,
    silent: bool = True,
    log_level: str = INFO,
) -> None:

    # Skip client initialization if help or version is requested
    if "--help" in sys.argv or "--version" in sys.argv or "-v" in sys.argv:
        return

    # In all cases other than help mode, base_url is required
    elif not base_url:
        click.echo("Error: Base URL is required", err=True)
        sys.exit(2)

    # Safety check that we are in CLI mode
    ctx.ensure_object(dict)

    guardian = GuardianAPIClient(
        base_url, log_level=log_level if not silent else CRITICAL
    )

    ctx.obj["SILENT"] = silent
    ctx.obj["BLOCK_ON_ERRORS"] = block_on_scan_errors
    ctx.obj["REPORT_ONLY"] = report_only
    ctx.obj["CLIENT"] = guardian


@cli.command()
@click.pass_context
@click.argument("model-uri", required=True)
@click.option(
    "--poll-interval-secs",
    default=5,
    type=int,
    required=False,
    help="Seconds to poll for scan status. If <= 0, the function returns immediately after submitting the scan",
)
def scan(
    ctx,
    model_uri: str,
    poll_interval_secs: int = 5,
) -> None:
    """
    Submits a scan request for the given URI
    """

    try:
        guardian: GuardianAPIClient = ctx.obj["CLIENT"]
        response = guardian.scan(model_uri, poll_interval_secs=poll_interval_secs)

        http_status_code = response.get("http_status_code")
        if not http_status_code or http_status_code // 100 != 2:
            click.echo(
                f"Error: Scan failed with status code: {http_status_code}, message: {response.get('error')}",
                err=True,
            )
            sys.exit(2)

        if not ctx.obj["SILENT"]:
            click.echo(json.dumps(response["scan_status_json"], indent=4))

        if ctx.obj["REPORT_ONLY"] or poll_interval_secs <= 0:
            sys.exit(0)

        if (
            response["scan_status_json"]["aggregate_eval_outcome"] == "ERROR"
            and ctx.obj["BLOCK_ON_ERRORS"]
        ):
            click.echo(
                f"Error: Scan failed with code: {response['scan_status_json']['error_code']}, message: {response['scan_status_json']['error_message']}",
                err=True,
            )
            sys.exit(2)

        if response["scan_status_json"]["aggregate_eval_outcome"] == "FAIL":
            click.echo(
                f"Error: Scan failed because it failed your organization's security policies",
                err=True,
            )
            sys.exit(1)
    except ValueError as e:
        click.echo(f"Error: Invalid arguments {e}", err=True)
        sys.exit(2)
    except Exception as e:
        click.echo(f"Error: Scan submission failed: {e}", err=True)
        sys.exit(2)

    sys.exit(0)


@cli.command()
@click.pass_context
@click.argument("scan-id", required=True)
def get_scan(ctx, scan_id: str):
    guardian: GuardianAPIClient = ctx.obj["CLIENT"]
    response = guardian.get_scan(scan_id)

    http_status_code = response.get("http_status_code")
    if (
        not http_status_code
        or http_status_code != 200
        or not response.get("scan_status_json")
    ):
        click.echo(
            f"Error: Scan retrieval failed with status code: {http_status_code}, message: {response.get('error')}",
            err=True,
        )
        sys.exit(2)

    if not ctx.obj["SILENT"]:
        click.echo(json.dumps(response["scan_status_json"], indent=4))

    if ctx.obj["REPORT_ONLY"]:
        sys.exit(0)

    if (
        response["scan_status_json"]["aggregate_eval_outcome"] == "ERROR"
        and ctx.obj["BLOCK_ON_ERRORS"]
    ):
        click.echo(
            f"Error: Scan failed with code: {response['scan_status_json']['error_code']}, message: {response['scan_status_json']['error_message']}",
            err=True,
        )
        sys.exit(2)

    if response["scan_status_json"]["aggregate_eval_outcome"] == "FAIL":
        click.echo(
            f"Error: Scan failed because it failed your organization's security policies",
            err=True,
        )
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    cli(obj={})
