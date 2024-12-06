"""Main module."""

import asyncio
import itertools
import logging
import typing as t
from pathlib import Path

import pandas as pd
from dotty_dict import Dotty
from fw_client import FWClient

from .dataviews import generate_params, get_dataview
from .process import QCResultConfig, process_df

log = logging.getLogger(__name__)


async def run_dataviews(
    client: FWClient, opts: dict, top_level: str, destination: dict
) -> t.List[pd.DataFrame]:
    """Run all dataviews.

    Args:
        client: API client
        opts: Dataview launching options
        top_level: Top level namespace key
        destination: Analysis parent

    Returns:
        t.List[pd.DataFrame]: Raw dataframes.
    """
    params = generate_params(opts, destination)
    log.info(f"Launching {len(params)} dataview(s)")
    tasks = []
    for i, param in enumerate(params):
        tasks.append(asyncio.create_task(get_dataview(client, top_level, param, i)))

    return await asyncio.gather(*tasks)


async def build_df(
    client: FWClient,
    config: QCResultConfig,
    options: dict,
    fields: Dotty,
    destination: dict,
) -> pd.DataFrame:
    """Run and post-process dataviews

    Args:
        client: API Client
        config: Global post-process config.
        options: Report output options
        fields: Dictionary of custom field configs.
        destination: Analysis parent.

    Returns:
        pd.DataFrame: Single processed dataframe.
    """
    dfs = await run_dataviews(client, options, config.top_level_namespace, destination)
    log.info("Finished running dataviews")
    tasks = []
    for i, df in enumerate(dfs):
        tasks.append(asyncio.create_task(process_df(df, config, fields, i)))

    result = await asyncio.gather(*tasks)
    log.info("Creating final dataframe.")

    # Check if there are any results
    if not result or all(not inner_list for inner_list in result):
        log.warning("No QC data found.")
        return pd.DataFrame()  # Return an empty DataFrame if no data
    return pd.concat(list(itertools.chain(*result)))


async def run(  # noqa: PLR0913
    client: FWClient,
    fields: Dotty,
    config: QCResultConfig,
    options: dict,
    destination: dict,
    outdir: Path,
) -> int:
    """Run qc_reporter

    Args:
        client: API Client
        fields: Custom fields
        config: Configuration options for processing QC values
        options: Report output options
        destination: Destination container
        outdir: Output directory

    Returns:
        int: Return code
    """

    out = await build_df(client, config, options, fields, destination)

    if out.empty:
        log.info("No QC data found. Exiting without generating output.")
        return 0

    format_ = options["output_format"]
    out_file = outdir / f"{destination['id']}_report.{format_}"
    log.info(f"Saving {out.shape[0]} rows to {out_file}")
    if format_ == "csv":
        out.to_csv(out_file, index=False)
    elif format_ == "json":
        out.to_json(out_file, orient="records")
    else:
        log.error(f"Unknown output format type: {options['output_format']}")
        return 1

    return 0
