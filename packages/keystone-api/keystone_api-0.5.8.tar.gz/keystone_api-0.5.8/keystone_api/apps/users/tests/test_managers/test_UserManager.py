"""Unit tests for the `UserManager` class."""

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.users.models import User


class UserCreation(TestCase):
    """Test the creation of user accounts."""

    def test_create_user(self) -> None:
        """Test the creation of generic user accounts."""

        user = User.objects.create_user(
            username='foobar',
            first_name='foo',
            last_name='bar',
            email="foo@bar.com",
            password="foobar123")

        self.assertEqual(user.username, "foobar")
        self.assertEqual(user.first_name, "foo")
        self.assertEqual(user.last_name, "bar")
        self.assertEqual(user.email, "foo@bar.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self) -> None:
        """Test the creation of superuser accounts."""

        admin_user = User.objects.create_superuser(
            username='foobar',
            first_name='foo',
            last_name='bar',
            email="foo@bar.com",
            password="foobar123")

        self.assertEqual(admin_user.username, "foobar")
        self.assertEqual(admin_user.first_name, "foo")
        self.assertEqual(admin_user.last_name, "bar")
        self.assertEqual(admin_user.email, "foo@bar.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_superusers_must_be_staff(self) -> None:
        """Test superusers are required to be staff users."""

        with self.assertRaisesRegex(ValueError, 'must set `is_staff=True`.'):
            User.objects.create_superuser(
                username='foobar',
                first_name='foo',
                last_name='bar',
                email="foo@bar.com",
                password="foobar123",
                is_staff=False)

    def test_superusers_must_be_superusers(self) -> None:
        """Test superusers are required to have superuser permissions."""

        with self.assertRaisesRegex(ValueError, 'must set  `is_superuser=True`'):
            User.objects.create_superuser(
                username='foobar',
                first_name='foo',
                last_name='bar',
                email="foo@bar.com",
                password="foobar123",
                is_superuser=False)

    def test_passwords_are_validated(self) -> None:
        """Test passwords are required to meet security criteria."""

        with self.assertRaisesRegex(ValidationError, 'This password is too short'):
            User.objects.create_user(
                username='foobar',
                password='short',
                first_name='foo',
                last_name='bar',
                email="foo@bar.com"
            )
