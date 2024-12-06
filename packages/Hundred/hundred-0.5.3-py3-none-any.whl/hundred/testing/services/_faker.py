from faker import Faker
from injection.testing import test_injectable


@test_injectable(inject=False, mode="fallback")
def fake_factory() -> Faker:
    return Faker()
