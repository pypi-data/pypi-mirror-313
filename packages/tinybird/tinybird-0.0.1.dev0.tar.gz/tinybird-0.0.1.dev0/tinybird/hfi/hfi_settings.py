import importlib
import logging
import os
import sys
from typing import Optional

from tinybird.hfi.hfi_defaults import HfiDefaults
from tinybird_shared.redis_client.redis_client import DEFAULT_REDIS_CONFIG


def init():
    hfi_settings = {
        "redis": DEFAULT_REDIS_CONFIG,
        "jwt_secret": "abcd",
        "ch_ingestion_burst_size": HfiDefaults.CH_INGESTION_BURST_SIZE,
        "ch_ingestion_tokens_per_second_default": HfiDefaults.CH_INGESTION_TOKENS_PER_SECOND_DEFAULT,
        "ch_ingestion_tokens_per_second_gatherer_default": HfiDefaults.CH_INGESTION_TOKENS_PER_SECOND_GATHERER_DEFAULT,
        "ch_ingestion_internal_tables_period": 10,
        "allow_json_type": True,
    }
    if os.environ.get("HFI_CONFIG"):
        try:
            spec: Optional[importlib.machinery.ModuleSpec] = importlib.util.spec_from_file_location(
                "tinybird.settings", os.environ.get("HFI_CONFIG")
            )
            if spec is None:
                raise Exception("Spec not found")
            settings_override = importlib.util.module_from_spec(spec)
            if settings_override is None:
                raise Exception("Module not found")
            if spec.loader is None:
                raise Exception("Spec loader not found")
            spec.loader.exec_module(settings_override)
            hfi_settings.update(settings_override.conf())
        except Exception as e:
            logging.exception("failed to load configuration: %s" % e)
            sys.exit(4)
    return hfi_settings


hfi_settings = init()
