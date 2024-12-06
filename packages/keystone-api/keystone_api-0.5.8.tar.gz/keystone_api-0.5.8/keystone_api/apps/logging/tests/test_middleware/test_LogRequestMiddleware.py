"""Unit tests for the `LogRequestMiddleware` class."""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.test.client import RequestFactory

from apps.logging.middleware import LogRequestMiddleware
from apps.logging.models import RequestLog


class LoggingToDatabase(TestCase):
    """Test the logging of requests to the database."""

    def test_authenticated_user(self) -> None:
        """Test requests are logged for authenticated users."""

        rf = RequestFactory()
        request = rf.get('/hello/')
        request.user = get_user_model().objects.create()

        middleware = LogRequestMiddleware(lambda x: HttpResponse())
        middleware(request)

        self.assertEqual(RequestLog.objects.count(), 1)
        self.assertEqual(RequestLog.objects.first().user, request.user)

    def test_anonymous_user(self) -> None:
        """Test requests are logged for anonymous users."""

        rf = RequestFactory()
        request = rf.get('/hello/')
        request.user = AnonymousUser()

        middleware = LogRequestMiddleware(lambda x: HttpResponse())
        middleware(request)

        self.assertEqual(RequestLog.objects.count(), 1)
        self.assertIsNone(RequestLog.objects.first().user)


class GetClientIP(TestCase):
    """Test the fetching of client IP data from incoming requests."""

    def test_ip_with_x_forwarded_for(self) -> None:
        """Test the fetching of IP data from the `HTTP_X_FORWARDED_FOR` header."""

        request = HttpRequest()
        request.META['HTTP_X_FORWARDED_FOR'] = '192.168.1.1, 10.0.0.1'

        client_ip = LogRequestMiddleware.get_client_ip(request)
        self.assertEqual(client_ip, '192.168.1.1')

    def test_ip_with_remote_addr(self) -> None:
        """Test the fetching of IP data from the `REMOTE_ADDR` header."""

        request = HttpRequest()
        request.META['REMOTE_ADDR'] = '192.168.1.1'

        client_ip = LogRequestMiddleware.get_client_ip(request)
        self.assertEqual(client_ip, '192.168.1.1')

    def test_ip_without_headers(self) -> None:
        """Test the return value is None when no headers are specified."""

        request = HttpRequest()
        client_ip = LogRequestMiddleware.get_client_ip(request)
        self.assertIsNone(client_ip)
