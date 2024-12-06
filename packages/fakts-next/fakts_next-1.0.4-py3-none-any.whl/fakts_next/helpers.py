from fakts_next.fakts import get_current_fakts_next
from koil.helpers import unkoil
from .protocols import FaktValue

async def afakt(key: str) -> FaktValue:
    return await get_current_fakts_next().aget(key)


def fakt(key: str) -> FaktValue:
    return unkoil(afakt, key)