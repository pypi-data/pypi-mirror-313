from fakts_next.grants.remote import RemoteGrant

from fakts_next.grants.remote.claimers.static import StaticClaimer
from fakts_next.grants.remote.discovery.static import StaticDiscovery
from fakts_next.grants.remote.demanders.static import StaticDemander
from fakts_next.grants.remote.demanders.redeem import RedeemDemander
from fakts_next.grants.remote.claimers.post import ClaimEndpointClaimer
from fakts_next.grants.remote.models import FaktsEndpoint, FaktValue
from typing import Dict


def build_remote_testing(value: Dict[str, FaktValue]) -> RemoteGrant:
    """Builds a remote grant for testing purposes

    Will always return the same value when claiming.

    Parameters
    ----------
    value : Dict[str, FaktValue]
        The value to return when claiming

    Returns
    -------
    RemoteGrant
        The remote grant

    """
    return RemoteGrant(
        discovery=StaticDiscovery(
            endpoint=FaktsEndpoint(base_url="https://example.com")
        ),
        claimer=StaticClaimer(value=value),
        demander=StaticDemander(token="token"),  # type: ignore
    )


def build_redeem_grant(
    url: str, manifest: Dict[str, FaktValue], redeem_token: str
) -> RemoteGrant:

    return RemoteGrant(
        discovery=StaticDiscovery(endpoint=FaktsEndpoint(base_url=url)),
        claimer=ClaimEndpointClaimer(),
        demander=RedeemDemander(manifest=manifest, token=redeem_token),
    )


def build_remote_testing_with_token(fakts_next_url: str, token: str) -> RemoteGrant:
    """Builds a remote grant for testing purposes

    This grant will use the given token to demand the configuration from fakts_next.
    This is great for testing purposes, or when an api token is known at compile time.

    Parameters
    ----------
    value : Dict[str, FaktValue]
        The value to return when claiming

    Returns
    -------
    RemoteGrant
        The remote grant

    """
    return RemoteGrant(
        discovery=StaticDiscovery(endpoint=FaktsEndpoint(base_url=fakts_next_url)),
        claimer=ClaimEndpointClaimer(),
        demander=StaticDemander(token=token),  # type: ignore
    )
