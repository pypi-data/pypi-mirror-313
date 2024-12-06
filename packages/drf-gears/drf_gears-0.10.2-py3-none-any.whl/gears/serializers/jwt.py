from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JWTObtainPairSerializer(TokenObtainPairSerializer):
    """
    This is a helper serializer, which works with a JWTUserModelMixin.
    """

    @classmethod
    def get_token(cls, user):
        if not hasattr(user, 'build_token'):
            raise Exception(
                'JWTObtainPairSerializer must be used with a JWTUserModelMixin together'
            )
        return user.build_token()
