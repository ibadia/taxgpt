import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyDecimal

from apps.user_app.models import AppUser
from core.models import ParsedDocuments


class UserFactory(DjangoModelFactory):
    class Meta:
        model = AppUser

    # Using a sequence to generate unique names
    email = factory.Sequence(lambda n: f"client{n}@example.com")
    user_id = factory.Sequence(lambda n: f"{n}")
    username = factory.Sequence(lambda n: f"client{n}dsm")

