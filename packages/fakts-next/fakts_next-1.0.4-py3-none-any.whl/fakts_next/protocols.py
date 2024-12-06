from pydantic import BaseModel
from typing import Dict, Any, Optional, Union, Protocol, runtime_checkable


NestedFaktValue = Union[str, int, float, bool, None, Dict[str, Any]]
FaktValue = Union[str, int, float, bool, None, Dict[str, NestedFaktValue]]


@runtime_checkable
class FaktsGrant(Protocol):
    """FaktsGrant

    A FaktsGrant is a grant that can be used to load configuration
    from a specific source. It can be used to load configuration
    from a file, from a remote endpoint, from a database, etc.
    """

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



        Parameters
        ----------
        request : FaktsRequest
            The request object that may contain additional information needed for loading the configuration.

        Returns
        -------
        dict
            The configuration loaded from the grant.

        Raises
        ------

        GrantError
            If the grant failed to load the configuration.+



        """
        ...


@runtime_checkable
class FaktsCache(Protocol):
    """FaktsGrant

    A FaktsGrant is a grant that can be used to load configuration
    from a specific source. It can be used to load configuration
    from a file, from a remote endpoint, from a database, etc.
    """

    async def aload(self) -> Optional[Dict[str, FaktValue]]:
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



        Parameters
        ----------
        request : FaktsRequest
            The request object that may contain additional information needed for loading the configuration.

        Returns
        -------
        dict
            The configuration loaded from the grant.

        Raises
        ------

        GrantError
            If the grant failed to load the configuration.+



        """
        ...

    async def aset(self, value: Dict[str, FaktValue]) -> None:
        """Refreshes the configuration from the grant

        This function is used to refresh the configuration from the grant.
        This is used to refresh the configuration from the grant, and should
        be used to refresh the configuration from the grant.

        The request object is used to pass information
        """
        ...

    async def areset():
        """Resets the cache

        This function is used to reset the cache
        """
        ...
