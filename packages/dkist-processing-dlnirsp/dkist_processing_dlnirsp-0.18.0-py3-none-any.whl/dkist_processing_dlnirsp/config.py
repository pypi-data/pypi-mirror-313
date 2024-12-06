"""Configuration for the dkist-processing-dlnirsp package and logging thereof."""
from dkist_processing_common.config import DKISTProcessingCommonConfiguration


class DKISTProcessingDLNIRSPConfigurations(DKISTProcessingCommonConfiguration):
    """Configurations custom to the dkist-processing-dlnirsp package."""

    pass  # nothing custom.... yet


dkist_processing_dlnirsp_configurations = DKISTProcessingDLNIRSPConfigurations()
dkist_processing_dlnirsp_configurations.log_configurations()
