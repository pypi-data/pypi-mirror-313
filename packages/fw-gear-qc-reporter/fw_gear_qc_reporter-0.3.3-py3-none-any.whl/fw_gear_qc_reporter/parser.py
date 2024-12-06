"""Parser module to parse gear config.json."""

import logging
from typing import Tuple

from dotty_dict import Dotty, dotty
from fw_client import FWClient
from fw_gear import GearContext
from ruamel.yaml import YAML

from fw_gear_qc_reporter.qc_config import (
    DCIODVFY_CONFIG,
    DICOM_FIXER_CONFIG,
    QCResultConfig,
    QCResultFieldConfig,
)

from . import NAME, __version__

backoff_logger = logging.getLogger("backoff")


def parse_config(
    gear_context: GearContext,
) -> Tuple[FWClient, Dotty, QCResultConfig, dict, dict]:
    """Parse system generated config.json

    Args:
        gear_context: Gear context

    Returns:
        Tuple[FWClient, Dotty, dict, dict]:
            * Authenticated API client
            * Custom field rules
            * Report options
            * Parent container
    """
    debug = gear_context.config.opts.get("debug")
    if not debug:
        backoff_logger.setLevel(logging.WARNING)

    api_input = gear_context.config.get_input("api-key")

    if api_input is None:
        raise ValueError("API key input is missing in config.json.")

    api_key = api_input.get("key", "")

    if api_key == "":
        raise ValueError("API key is empty in input.")

    client = FWClient(
        api_key=api_key,
        client_name=NAME,
        client_version=__version__,
        read_timeout=20,
        connect_timeout=10,
    )
    metadata_rules_file = gear_context.config.get_input_path("metadata-rules")
    rules = {}
    if metadata_rules_file:
        reader = YAML(typ="safe")
        with open(metadata_rules_file, "r", encoding="utf-8") as fp:
            rules = reader.load(fp)

    # Load global config
    config = QCResultConfig()
    config.excludes.extend(rules.get("excluded_qc_results", []))
    overrides = rules.get("excluded_qc_results_override")
    if overrides is not None:
        config.excludes = overrides
    config.top_level_namespace = rules.get("top_level_namespace", "qc")
    config.report_success = gear_context.config.opts.get("report-on-success", False)

    # Load field-specific configs
    fields = dotty({})
    for k, v in rules.get("fields", {}).items():
        conf = QCResultFieldConfig.from_global(config)
        if "fail_names" in v:
            conf.fail_names = v.get("fail_names", [])
        if "state_name" in v:
            conf.state_name = v.get("state_name", "")
        if "true_means_fail" in v:
            conf.true_means_fail = v.get("true_means_fail", True)
        # NOTE: Change this to be a dotty dict if we want to support
        #   more than 1-level nested fields within a given QC-result
        sub_fields = {}
        for subk, subv in v.get("data", {}).items():
            sub_fields[subk] = subv
        conf.data = sub_fields
        fields[k] = conf

    fields.update(DCIODVFY_CONFIG)
    fields.update(DICOM_FIXER_CONFIG)

    report_options = {
        "output_format": gear_context.config.opts.get("output-format"),
        "intermediates": gear_context.config.opts.get("intermediate-containers"),
        "include_analyses": not gear_context.config.opts.get("skip-analyses"),
    }

    dest = client.get(f"/api/containers/{gear_context.config.destination['id']}")
    return client, fields, config, report_options, dest.parent
