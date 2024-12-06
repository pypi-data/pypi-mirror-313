from pydantic import Field
from typing import Any, Dict
from fakts_next.grants.remote.models import FaktsEndpoint, FaktValue
from pydantic import BaseModel


class StaticClaimer(BaseModel):
    """A claimer that always claims
    the same configuration

    This is mostly used for testing purposes.

    """

    value: Dict[str, Any] = Field(
        default_factory=lambda: {},
        exclude=True,
    )
    """ An ssl context to use for the connection to the endpoint"""

    async def aclaim(
        self,
        token: str,
        endpoint: FaktsEndpoint,
    ) -> Dict[str, FaktValue]:
        """Claim the configuration from the endpoint"""

        return self.value
