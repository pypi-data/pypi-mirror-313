from pydantic import BaseModel


class BillingDetails(BaseModel):
    origin_provider: str
    origin_region: str
    destination_provider: str
    destination_region: str
