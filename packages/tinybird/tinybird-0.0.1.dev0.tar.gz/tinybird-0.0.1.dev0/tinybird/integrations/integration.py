from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class IntegrationInfo:
    """Identifies specific integrations at parent level (User, UserAccount...)"""

    integration_type: str
    integration_id: str
    date_created: datetime = field(default_factory=lambda: datetime.now())


class IntegrationException(Exception):
    """Generic integration exception."""

    pass
