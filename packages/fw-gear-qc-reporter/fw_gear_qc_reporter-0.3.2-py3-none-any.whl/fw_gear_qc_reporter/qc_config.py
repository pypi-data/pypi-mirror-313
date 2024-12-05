import typing as t
from dataclasses import dataclass, field


# Field override config
@dataclass
class QCResultFieldConfig:
    fail_names: t.List[str] = field(
        default_factory=lambda: ["fail", "failure", "failed"]
    )
    state_name: str = "state"
    true_means_fail: bool = True
    data: dict = field(default_factory=lambda: dict())

    @classmethod
    def from_global(cls, global_config: "QCResultConfig"):
        return cls(
            fail_names=global_config.fail_names,
            state_name=global_config.state_name,
            true_means_fail=global_config.true_means_fail,
        )


# Global config values


@dataclass
class QCResultConfig(QCResultFieldConfig):
    report_success: bool = False
    top_level_namespace: str = "qc"
    excludes: t.List[str] = field(default_factory=lambda: ["job_info", "gear_info"])


DEFAULT_GEAR_CONFIG = {
    "dicom-qc": {
        "dciodvfy": QCResultFieldConfig(
            data={"data": "unfold"},
        ),
    },
    "dicom-fixer": {
        "fixed": QCResultFieldConfig(
            data={"events": "unfold"},
        ),
    },
}

# Default value configuration for Flywheel-owned gears
# Hardcode custom config for dicom-qc's dciodvfy
DCIODVFY_CONFIG = {
    "dicom-qc": {
        "dciodvfy": QCResultFieldConfig(
            data={"data": "unfold"},
        ),
    },
}

# Hard code custom config for dicom-fixer gear
DICOM_FIXER_CONFIG = {
    "dicom-fixer": {
        "fixed": QCResultFieldConfig(
            data={"events": "unfold"},
        ),
    },
}
