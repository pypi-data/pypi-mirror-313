
# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long

from enum import Enum

class CloudProvider(Enum):
    GCP = "cloud_gcp"
    AWS = "cloud_aws"
    AZURE = "cloud_azure"
    IBM = "cloud_ibm"
    ALIBABA = "cloud_alibaba"
    NO_CLOUD = "no_cloud"
    CLOUD_AGNOSTIC = "cloud_agnostic"
    OTHER = "other"
    UNKNWON = "unknown"

    def __str__(self):
        return self.value
