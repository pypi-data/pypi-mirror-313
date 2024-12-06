import click

from .waterlevels import waterlevels, waterlevels_run
from .salinities import salinities, salinities_run
from .summaries import summaries, summaries_run
from .rainfall import rainfall

from .. import __version__, Report, CURRENT_RPERIOD
from ..utils import get_logger

logger = get_logger()


@click.group()
def wraptn():
    # bump commit
    pass


@click.command()
@click.option("-p", "--reporting-period", default=CURRENT_RPERIOD)
@click.option("-v", "--verbose", count=True)
@click.option("-s1", "--step1/--no-step1", default=True)
@click.option("-s2", "--step2/--no-step2", default=True)
@click.option("-s3", "--step3/--no-step3", default=True)
@click.option("-s4", "--step4/--no-step4", default=True)
@click.option("-s5", "--step5/--no-step5", default=True)
@click.option("-s6", "--step6/--no-step6", default=True)
@click.option("-s7", "--step7/--no-step6", default=True)
@click.option("-s", "--static/--no-static", default=True)
@click.option("--nbs/--no-nbs", default=True)
@click.option("--local/--no-local", default=True)
@click.option("-r", "--report", default="")
@click.option("--figures/--no-figures", default=True)
@click.argument("resource", required=False)
def run(
    resource,
    reporting_period,
    verbose,
    step1,
    step2,
    step3,
    step4,
    step5,
    step6,
    step7,
    static,
    nbs,
    local,
    report,
    figures,
):
    handlers = []
    if verbose == 1:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
    if verbose == 2:
        handlers.append({"sink": sys.stdout, "level": "INFO"})
        handlers.append({"sink": "wraptn_cli.log", "level": "DEBUG"})
    config = {
        "handlers": handlers,
    }
    logger.configure(**config)

    logger.warning(f"wraptn.__version__ = {__version__}")
    wl_resource_keys = []
    tds_resource_keys = []
    if resource is None:
        r = Report(report, reporting_period)
        df = r.read_table("Report_Resources_mapping")
        wl_resource_keys = [r for r in df[df.param == "WL"].resource_key.unique() if r]
        tds_resource_keys = [
            r for r in df[df.param == "TDS"].resource_key.unique() if r
        ]
    else:
        if resource.endswith("_WL"):
            wl_resource_keys.append(resource)
        if resource.endswith("_TDS"):
            tds_resource_keys.append(resource)
    logger.info(
        f"CLI will run WL resources: {wl_resource_keys} and TDS resources: {tds_resource_keys}"
    )
    for rk in wl_resource_keys:
        waterlevels_run(
            rk,
            reporting_period,
            verbose,
            step1,
            step2,
            step3,
            static,
            report,
            figures,
        )
    for rk in tds_resource_keys:
        salinities_run(
            rk,
            reporting_period,
            verbose,
            step4,
            step5,
            step6,
            step7,
            static,
            report,
            figures,
        )
    if report:
        summaries_run(reporting_period, report, verbose, resource, local, nbs)


wraptn.add_command(waterlevels)
wraptn.add_command(salinities)
wraptn.add_command(summaries)
wraptn.add_command(rainfall)
wraptn.add_command(run)
