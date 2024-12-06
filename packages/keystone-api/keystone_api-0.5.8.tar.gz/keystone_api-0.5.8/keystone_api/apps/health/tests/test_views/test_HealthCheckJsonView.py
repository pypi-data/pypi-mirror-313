"""Unit tests for the `HealthCheckJsonView` class."""

import json

from django.http import JsonResponse
from django.test import TestCase

from apps.health.tests.test_views.utils import create_mock_plugin
from apps.health.views import HealthCheckJsonView


class RenderResponse(TestCase):
    """Tests for the `render_response` function."""

    def test_return_matches_health_checks(self) -> None:
        """Test the rendering of application health checks as JSON data."""

        health_checks = {
            'plugin1': create_mock_plugin(1, 'OK', True),
            'plugin2': create_mock_plugin(0, 'Error', False)
        }

        health_check_json = {
            'plugin1': {
                'status': 200,
                'message': 'OK',
                'critical_service': True
            },
            'plugin2': {
                'status': 500,
                'message': 'Error',
                'critical_service': False
            }
        }

        response = HealthCheckJsonView.render_response(health_checks)
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.dumps(health_check_json), response.content.decode())
