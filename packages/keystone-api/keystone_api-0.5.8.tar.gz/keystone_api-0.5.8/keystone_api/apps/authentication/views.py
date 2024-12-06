"""Application logic for rendering HTML templates and handling HTTP requests.

View objects handle the processing of incoming HTTP requests and return the
appropriately rendered HTML template or other HTTP response.
"""

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.users.serializers import RestrictedUserSerializer

__all__ = ['WhoAmIView']


class WhoAmIView(GenericAPIView):
    """Return user metadata for the currently authenticated user."""

    serializer_class = RestrictedUserSerializer
    permission_classes = []

    def get(self, request, *args, **kwargs) -> Response:
        """Return user metadata for the currently authenticated user.

        Returns:
            A 200 response with user data if authenticated, and a 404 response otherwise
        """

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.serializer_class(request.user)
        return Response(serializer.data)
