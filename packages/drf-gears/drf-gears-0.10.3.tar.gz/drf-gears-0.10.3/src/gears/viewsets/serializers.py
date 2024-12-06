import warnings


class SerializersMixin(object):
    """
    SerializersMixin implements the mapping logic for managing serializers according
    to the action, request, type so on.

    Example:
        serializers = {
            None: DefaultSerializer,  # will be used this one if none of rest are not suitable
            "list": ListSerializer,  # will be used for the list() method of ViewSet
            "retrieve": RetrieveSerializer,  # will be used for the retrieve() method of ViewSet
            "create": CreateSerializer,  # will be used for the create() method of ViewSet
            "update": UpdateSerializer,  # will be used for the update() method of ViewSet
            "partial_update": UpdateSerializer,  # will be used for the partial_update() method of ViewSet
            "destroy": DestroySerializer,  # will be used for the destroy() method of ViewSet
            "read_only": ReadOnlySerializer,  # will be used for the list() and retrieve() methods of ViewSet
            "write_only": WriteOnlySerializer,  # will be used for the create(), update() and partial_update() methods of ViewSet
            "custom_action": CustomActionSerializer,  # will be used for the custom ViewSet method named as `custom_action`
            "my_serializer": MySerializer,  # will be used if the serializer_name attribute is set

            # NOT IMPLEMENTED YET
            # get=GetOnlySerializer,  # will be used for the GET requests of ViewSet
            # post=PostOnlySerializer,  # will be used for the POST requests of ViewSet
            # put=PutOnlySerializer,  # will be used for the PUT requests of ViewSet
            # patch=PatchOnlySerializer,  # will be used for the PATCH requests of ViewSet
            # delete=DeleteOnlySerializer,  # will be used for the DELETE requests of ViewSet

        }

    Priority: specified by name, action, method, default
    """
    serializers = {}
    default_serializer_name = None  # None as a key for dict
    _serializers = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, "serializer_class"):
            self._serializers[self.default_serializer_name] = self.serializer_class

        # Back consistency warning
        _d = "default"
        if _d in self.serializers.keys() and self.default_serializer_name != _d:
            warnings.warn(
                "Since version 0.10.1 the name of default serializer is `None`. "
                "You have to rename it if you still use the `default` key. "
                "You're able to provide any custom value for setting the name of the "
                "default key with the option `default_serializer_name`. "
                "Notice that it was renamed: default_name -> default_serializer_name."
            )

        self._serializers.update(self.serializers)

        if self.default_serializer_name not in self.serializers:
            raise ValueError(
                "Need to specify either 'serializer_class' or "
                "serializer's default class"
            )


    def get_serializer_class(self, serializer_name=None):
        return (
            self.__by_name(serializer_name)
            or self.__by_action()
            or self.__by_action_group()
            or self.__default()
            or super().get_serializer_class()
        )

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class(
            serializer_name=kwargs.pop('serializer_name', None)
        )
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def __by_name(self, name: str):
        return self._serializers.get(name)

    def __by_action(self):
        return self._serializers.get(self.action)

    def __by_action_group(self):
        if self.action in ("create", "update", "partial_update",):
            action = "write_only"
        elif self.action in ("list", "retrieve",):
            action = "read_only"
        else:
            return
        return self._serializers.get(action)

    # def __by_method(self):
    #     return

    def __default(self):
        # "default" is for the back consistency
        return self._serializers.get(self.default_serializer_name or "default")
