from injection.testing import test_singleton

from hundred.services.authenticator import JWTAuthenticator, StatelessAuthenticator


@test_singleton(on=StatelessAuthenticator, inject=False, mode="fallback")
def __test_jwt_authenticator() -> StatelessAuthenticator:
    return JWTAuthenticator("TEST_SECRET_KEY", verify_expiration=False)
