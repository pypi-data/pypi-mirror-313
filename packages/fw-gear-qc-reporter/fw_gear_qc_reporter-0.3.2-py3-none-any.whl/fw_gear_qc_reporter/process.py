import logging
import typing as t

import pandas as pd
from dotty_dict import Dotty

from .parser import QCResultConfig, QCResultFieldConfig

log = logging.getLogger(__name__)

DF_COLUMNS = [
    ("file_id", "str"),
    ("version", "str"),
    ("filename", "str"),
    ("subject_label", "str"),
    ("session_label", "str"),
    ("acquisition_label", "str"),
    ("analysis.label", "str"),
    ("session_url", "str"),
    ("state", "str"),
    ("qc_namespace", "str"),
    ("qc_val", "str"),
    ("data", "object"),
    ("key", "str"),
    ("value", "object"),
]


def process_fields(
    accum: t.List[pd.DataFrame], fields: dict, result: dict, row: dict
) -> None:
    """Process any field definitions for this qc result.

    If any fields need to be split up into multiple rows, process that here.
    Given a dataframe, input row, QC result and field defs, append the processed rows
    to the dataframe.

    Args:
        accum: List accumulator of DF rows
        fields: Field definitions for this qc result
        result: This qc result
        row: Row template for appending.
    """
    for field_name, action in fields.items():
        field = result.get(field_name)
        # Unfold dict field
        if isinstance(field, dict) and action == "unfold":
            for k, v in field.items():
                row["data"] = None
                row["key"] = k
                row["val"] = v
                accum.append(pd.DataFrame.from_dict(row, orient="index").T)
        # Unfold list field
        elif isinstance(field, list) and action == "unfold":  # list
            for v in field:
                row["data"] = v
                accum.append(pd.DataFrame.from_dict(row, orient="index").T)
        else:
            row["data"] = field
            accum.append(pd.DataFrame.from_dict(row, orient="index").T)


def process_qc_results(  # noqa: PLR0913
    accum: t.List[pd.DataFrame],
    new_row: dict,
    gear_name: str,
    qc_results: dict,
    field_configs: Dotty,
    global_config: QCResultConfig,
):
    """Process QC results for a gear.

    Args:
        accum: List accumulator of DF rows
        new_row: Row template for this group of results.
        gear_name: Name of gear which produced QC result.
        qc_results: Actual qc results.
        fields: Any field definitions relating to these results.
        successes: Whether or not to report on successes too.
    """
    report_successes = global_config.report_success
    excludes = global_config.excludes
    for name, result in qc_results.items():
        if name in excludes or not isinstance(result, dict):
            continue

        # Allow field specific override if set, otherwise fall back
        # to global config
        field_config = field_configs.get(gear_name, {}).get(name, {})
        if isinstance(field_config, QCResultFieldConfig):
            fail_names = field_config.fail_names
            state_name = field_config.state_name
            true_means_fail = field_config.true_means_fail
            fields = field_config.data
        else:
            fail_names = global_config.fail_names
            state_name = global_config.state_name
            true_means_fail = global_config.true_means_fail
            fields = None

        if state_name not in result:
            continue
        state = result[state_name]
        if isinstance(state, str):
            # If result is pass and we're not reporting successes, skip
            if state.lower() not in fail_names and not report_successes:
                continue
        elif isinstance(state, bool):
            # If result is a pass
            if (not state and true_means_fail) or (state and not true_means_fail):
                # If pass and not reporting successes, skip
                if not report_successes:
                    continue
        else:
            # Don't know how to handle other types ATM
            log.warning(
                f"State value `{state}` from state key '{state_name}' is unknown type "
                f"{type(state)}.  Expected either `str` or `bool`"
            )
            continue

        new_row.update(
            {
                "qc_namespace": gear_name,
                "qc_val": name,
                "state": str(state).lower(),
            }
        )
        if not fields:
            # No fields defined for this gear in config.
            new_row["data"] = result.get("data")
            accum.append(pd.DataFrame.from_dict(new_row, orient="index").T)
            continue
        process_fields(accum, fields, result, new_row)


async def process_df(
    df: pd.DataFrame, config: QCResultConfig, fields: Dotty, df_num: int
) -> t.List[pd.DataFrame]:
    """Process a qc result dataframe.

    Args:
        df: Input dataframe
        config: Configuration for dataview processing.
        fields: Any custom field definitions
        df_num: Helper for logging to identify which DF this is.

    Returns:
        t.List[pd.DataFrame]: Processed dataframe list
            * One row per each QC result
            * Data unfolded as per custom config.
    """
    non_null = df[~df["qc"].isna()]
    df_len = non_null.shape[0]
    accum: t.List[pd.DataFrame] = []
    if df_len < 1:
        return [
            pd.DataFrame({name: pd.Series(dtype=dtype) for (name, dtype) in DF_COLUMNS})
        ]

    decis = int(df_len / 10) or 1
    log.info(f"Dataframe {df_num} -- processing {df_len} rows")

    for i, row in enumerate(non_null.itertuples()):
        # Report on progress every 10%, if there is only one row (decis == 1) then don't
        if i % decis == 0 and decis != 1:
            log.info(f"Dataframe {df_num} -- done {i}/{df_len} ({100*i/df_len:.2f}%)")

        # Make a new row as a dictionary removing Index and qc
        new_row = {k: v for k, v in row._asdict().items() if k not in ["Index", "qc"]}
        for gear_name, qc_results in row.qc.items():
            process_qc_results(accum, new_row, gear_name, qc_results, fields, config)
    return accum
