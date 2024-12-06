from rest_framework_simplejwt.views import TokenObtainPairView

from ..serializers.jwt import JWTObtainPairSerializer


class JWTObtainPairView(TokenObtainPairView):
    """
    This is a helper view for handling the JWT gears.
    Use it, if you need a power of JWT tokens with a payload inside.
    """

    serializer_class = JWTObtainPairSerializer
