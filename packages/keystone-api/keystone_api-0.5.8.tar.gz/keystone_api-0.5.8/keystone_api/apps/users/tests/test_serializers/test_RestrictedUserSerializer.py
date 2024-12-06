"""Unit tests for the `RestrictedUserSerializer` class."""

from django.test import TestCase

from apps.users.serializers import RestrictedUserSerializer


class Create(TestCase):
    """Test record creation."""

    def test_create_raises_not_permitted(self) -> None:
        """Test that the create method raises a `RuntimeError`."""

        serializer = RestrictedUserSerializer()
        with self.assertRaises(RuntimeError):
            serializer.create({'username': 'testuser', 'password': 'Password123!'})
