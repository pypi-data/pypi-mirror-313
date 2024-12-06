from hashlib import sha256

from injection.testing import test_injectable

from hundred.services.hasher import Hasher


@test_injectable(on=Hasher, inject=False, mode="fallback")
class SHA256Hasher(Hasher):
    __slots__ = ()

    def hash(self, value: str) -> str:
        b = value.encode()
        h = sha256(b, usedforsecurity=False).hexdigest()
        return f"sha256:{h}"

    def verify(self, value: str, hash: str) -> bool:
        return hash == self.hash(value)

    def needs_rehash(self, hash: str) -> bool:
        return True
