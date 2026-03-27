from pydantic import BaseModel
from enum import Enum

class BuyingPrice(str, Enum):
    vhigh = "vhigh"
    high = "high"
    med = "med"
    low = "low"

class MaintPrice(str, Enum):
    vhigh = "vhigh"
    high = "high"
    med = "med"
    low = "low"

class Doors(str, Enum):
    two = "2"
    three = "3"
    four = "4"
    five_more = "5more"

class Persons(str, Enum):
    two = "2"
    four = "4"
    more = "more"

class LugBoot(str, Enum):
    small = "small"
    med = "med"
    big = "big"

class Safety(str, Enum):
    low = "low"
    med = "med"
    high = "high"

class CarFeatures(BaseModel):
    buying: BuyingPrice
    maint: MaintPrice
    doors: Doors
    persons: Persons
    lug_boot: LugBoot
    safety: Safety

class CarPrediction(BaseModel):
    label: str
    confidence: float
