from abc import ABC
from abc import abstractmethod
from types import MappingProxyType
from typing import Mapping
from typing import NamedTuple

from tecton_proto.common.secret_pb2 import SecretReference


class SecretCacheKey(NamedTuple):
    scope: str
    key: str


class SecretResolver(ABC):
    """Abstract Secret Resolver to resolve secret references to their values.

    Abstract class is used to allow for different implementations of secret resolution, for example,
    fetching secrets from MDS during materialization, or fetching secrets from a environment in local development.
    """

    @abstractmethod
    def resolve(self, secret: SecretReference) -> str:
        """Resolve the secret reference to its value."""
        raise NotImplementedError

    def resolve_map(self, secrets: Mapping[str, SecretReference]) -> Mapping:
        """Resolve a map of secret references to their values."""
        resolved_secrets_dict = {name: self.resolve(secret) for name, secret in secrets.items()}
        return MappingProxyType(resolved_secrets_dict)
