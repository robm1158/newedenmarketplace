from enum import Enum

class region(Enum):
    DELVE = 10000060
    DOMAIN = 10000043
    THE_FORGE = 10000002
print(region.DELVE.name)
print(region.DELVE.value)

