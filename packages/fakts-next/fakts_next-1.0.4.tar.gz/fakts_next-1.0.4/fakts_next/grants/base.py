from typing import Dict
from fakts_next.protocols import FaktValue
from pydantic import BaseModel


class BaseFaktsGrant(BaseModel):

    async def aload(self) -> Dict[str, FaktValue]:
        """Loads the configuration from the grant

        Depending on the grant, this function may load the configuration
        from a file, from a remote endpoint, from a database, etc, the
        implementation of the grant will determine how the configuration
        is loaded.

        Generally, the grant should use preconfigured values to set the
        configuration retrievel logic, and should not use the request
        object to determine how to load the configuration.

        The request object is used to pass information between different
        grants, and should only be used to forward conditional information
        like "skip cache" or "force refresh". Which are mainly handled
        by meta grants.



        Returns
        -------
        dict
            The configuration loaded from the grant.

        Raises
        ------

        GrantError
            If the grant failed to load the configuration.+



        """
        raise NotImplementedError("aload not implemented by the grant")

    async def arefresh(self) -> Dict[str, FaktValue]:
        """Refreshes the configuration from the grant

        This function is used to refresh the configuration from the grant.
        This is used to refresh the configuration from the grant, and should
        be used to refresh the configuration from the grant.

        The request object is used to pass information
        """
        return await self.aload()
