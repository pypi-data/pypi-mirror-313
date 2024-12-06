from typing import List, Dict
from fakts_next.grants.errors import GrantError
from fakts_next.grants.base import BaseFaktsGrant
import logging
from fakts_next.protocols import FaktsGrant, FaktValue
from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


class FailsafeGrant(BaseFaktsGrant):
    """
    Represent a Grant that loads configuration from a selection
    of other grants. It will try to load the grants in order,
    and will return the values from the first grant that succeeds.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    grants: List[FaktsGrant]

    async def aload(self) -> Dict[str, FaktValue]:
        """Loads the configuration from the grant

        It will try to load the grants in order, and will return the values from the first grant that succeeds.


        Parameters
        ----------
        request : FaktsRequest
            The request object that may contain additional information needed for loading the configuration.

        Returns
        -------
        dict
            The configuration loaded from the grant.


        """
        for grant in self.grants:
            try:
                config = await grant.aload()
                return config
            except GrantError:
                logger.exception(f"Failed to load {grant}", exc_info=True)
                continue

        raise GrantError("Failed to load any grants")

    async def arefresh(self) -> Dict[str, FaktValue]:
        """Loads the configuration from the grant

        It will try to load the grants in order, and will return the values from the first grant that succeeds.


        Parameters
        ----------
        request : FaktsRequest
            The request object that may contain additional information needed for loading the configuration.

        Returns
        -------
        dict
            The configuration loaded from the grant.


        """
        for grant in self.grants:
            try:
                config = await grant.arefresh()
                return config
            except GrantError:
                logger.exception(f"Failed to load {grant}", exc_info=True)
                continue

        raise GrantError("Failed to load any grants")
