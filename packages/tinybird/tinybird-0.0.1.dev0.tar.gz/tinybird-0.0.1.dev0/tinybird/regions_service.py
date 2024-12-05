from typing import Any, Dict, List, Optional, TypedDict

from tinybird.config import get_display_host


class Region(TypedDict):
    name: str
    provider: str
    api_host: str
    host: str
    default_password: Optional[str]
    telemetry_token: Optional[str]


PUBLIC_REGIONS: List[Region] = [
    {
        "name": "europe-west3",
        "provider": "gcp",
        "api_host": "https://api.tinybird.co",
        "host": "https://app.tinybird.co/gcp/europe-west3",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "us-east4",
        "provider": "gcp",
        "api_host": "https://api.us-east.tinybird.co",
        "host": "https://app.tinybird.co/gcp/us-east4",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "us-east-1",
        "provider": "aws",
        "api_host": "https://api.us-east.aws.tinybird.co",
        "host": "https://app.tinybird.co/aws/us-east-1",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "us-west-2",
        "provider": "aws",
        "api_host": "https://api.us-west-2.aws.tinybird.co",
        "host": "https://app.tinybird.co/aws/us-west-2",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "eu-central-1",
        "provider": "aws",
        "api_host": "https://api.eu-central-1.aws.tinybird.co",
        "host": "https://app.tinybird.co/aws/eu-central-1",
        "default_password": "",
        "telemetry_token": "",
    },
]

WADUS_REGIONS: List[Region] = [
    {
        "name": "wadus-1",
        "provider": "gcp",
        "api_host": "https://api.wadus1.gcp.tinybird.co",
        "host": "https://app.wadus.tinybird.co/gcp/wadus1",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "wadus-2",
        "provider": "gcp",
        "api_host": "https://api.wadus2.gcp.tinybird.co",
        "host": "https://app.wadus.tinybird.co/gcp/wadus2",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "wadus-3",
        "provider": "gcp",
        "api_host": "https://api.wadus3.gcp.tinybird.co",
        "host": "https://app.wadus.tinybird.co/gcp/wadus3",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "wadus-4",
        "provider": "gcp",
        "api_host": "https://api.wadus4.gcp.tinybird.co",
        "host": "https://app.wadus.tinybird.co/gcp/wadus4",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "wadus-5",
        "provider": "gcp",
        "api_host": "https://api.wadus5.gcp.tinybird.co",
        "host": "https://app.wadus.tinybird.co/gcp/wadus5",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "wadus-6",
        "provider": "gcp",
        "api_host": "https://api.wadus6.gcp.tinybird.co",
        "host": "https://app.wadus.tinybird.co/gcp/wadus6",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "aws-wadus-1",
        "provider": "aws",
        "api_host": "https://api.wadus1.aws.tinybird.co",
        "host": "https://app.wadus.tinybird.co/aws/wadus1",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "aws-wadus-2",
        "provider": "aws",
        "api_host": "https://api.wadus2.aws.tinybird.co",
        "host": "https://app.wadus.tinybird.co/aws/wadus2",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "aws-wadus-3",
        "provider": "aws",
        "api_host": "https://api.wadus3.aws.tinybird.co",
        "host": "https://app.wadus.tinybird.co/aws/wadus3",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "aws-wadus-4",
        "provider": "aws",
        "api_host": "https://api.wadus4.aws.tinybird.co",
        "host": "https://app.wadus.tinybird.co/aws/wadus4",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "aws-wadus-5",
        "provider": "aws",
        "api_host": "https://api.wadus5.aws.tinybird.co",
        "host": "https://app.wadus.tinybird.co/aws/wadus5",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "aws-wadus-6",
        "provider": "aws",
        "api_host": "https://api.wadus6.aws.tinybird.co",
        "host": "https://app.wadus.tinybird.co/aws/wadus6",
        "default_password": "",
        "telemetry_token": "",
    },
]

SPLIT_REGIONS: List[Region] = [
    {
        "name": "split-us-east",
        "provider": "aws",
        "api_host": "https://api.split.tinybird.co",
        "host": "https://app.tinybird.co/aws/split-us-east",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "split-us-west-2",
        "provider": "aws",
        "api_host": "https://api.split.us-west-2.aws.tinybird.co",
        "host": "https://app.tinybird.co/aws/split-us-west-2",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "ap-east",
        "provider": "aws",
        "api_host": "https://api.ap-east.aws.tinybird.co",
        "host": "https://app.tinybird.co/aws/ap-east",
        "default_password": "",
        "telemetry_token": "",
    },
]

INDITEX_REGIONS: List[Region] = [
    {
        "name": "inditex-tech",
        "provider": "gcp",
        "api_host": "https://inditex-tech.tinybird.co",
        "host": "https://app.inditex.tinybird.co/gcp/inditex-tech",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "inditex-c-stg",
        "provider": "gcp",
        "api_host": "https://inditex-c-stg.tinybird.co",
        "host": "https://app.inditex.tinybird.co/gcp/inditex-c-stg",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "inditex-c-pro",
        "provider": "gcp",
        "api_host": "https://inditex-c-pro.tinybird.co",
        "host": "https://app.inditex.tinybird.co/gcp/inditex-c-pro",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "inditex-z-stg",
        "provider": "gcp",
        "api_host": "https://inditex-z-stg.tinybird.co",
        "host": "https://app.inditex.tinybird.co/gcp/inditex-z-stg",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "inditex-rt-pro",
        "provider": "gcp",
        "api_host": "https://inditex-rt-pro.tinybird.co",
        "host": "https://app.inditex.tinybird.co/gcp/inditex-rt-pro",
        "default_password": "",
        "telemetry_token": "",
    },
    {
        "name": "inditex-pro",
        "provider": "gcp",
        "api_host": "https://inditex-pro.tinybird.co",
        "host": "https://app.inditex.tinybird.co/gcp/inditex-pro",
        "default_password": "",
        "telemetry_token": "",
    },
]


class RegionsService:
    _settings: Dict[str, Any] = {}

    @classmethod
    def init(cls, settings: Dict[str, Any]) -> None:
        cls._settings.update(settings)

    @classmethod
    def get_available_regions(cls) -> List[Region]:
        available_regions = cls._settings.get("available_regions", {})
        return [cls.map_region(available_regions[region]) for region in available_regions]

    @classmethod
    def get_regions(cls) -> List[Region]:
        available_regions = cls.get_available_regions()
        host = cls._settings.get("host", "")
        if host and "inditex" in host:
            regions = INDITEX_REGIONS
        elif host and "split" in host:
            regions = SPLIT_REGIONS
        elif host and "wadus" in host:
            regions = WADUS_REGIONS
        else:
            regions = PUBLIC_REGIONS

        extra_regions = [
            RegionsService.map_region(region)
            for region in regions
            if region["api_host"] not in [r["api_host"] for r in available_regions]
        ]

        return available_regions + extra_regions

    @classmethod
    def map_region(cls, region: Dict[str, Any] | Region) -> Region:
        return {
            "host": get_display_host(region["api_host"]),
            "api_host": region["api_host"],
            "name": region["name"],
            "provider": region.get("provider", "unknown"),
            "default_password": "",
            "telemetry_token": cls.add_telemetry_token(region),
        }

    @classmethod
    def add_telemetry_token(cls, region: Dict[str, Any] | Region) -> str:
        """
        Returns the telemetry token if the region api_host is in the list of public regions.

        Examples:
            >>> settings = {"telemetry_token": "token123"}
            >>> RegionsService.init(settings)
            >>> region = {"api_host": "https://api.tinybird.co"}
            >>> RegionsService.add_telemetry_token(region)
            'token123'

            >>> region = {"api_host": "https://api.split.tinybird.co"}
            >>> RegionsService.add_telemetry_token(region)
            ''

            >>> region = {}
            >>> RegionsService.add_telemetry_token(region)
            ''

        Args:
            region (Dict[str, Any]): A dictionary containing region information.

        Returns:
            str: The telemetry token if the API host is in PUBLIC_REGIONS; otherwise, an empty string.
        """
        if region.get("api_host", None) not in [r["api_host"] for r in PUBLIC_REGIONS]:
            return ""

        return cls._settings.get("telemetry_token", "")

    @classmethod
    def get_region_by_id(cls, region_id: str) -> Optional[Dict[str, Any]]:
        all_regions: Dict[str, Any] = cls._settings.get("all_regions", {})
        return all_regions.get(region_id, None)
