class PermissionsMixin:
    """
    PermissionsMixin ...
    """
    permission_classes = []
    permission_classes_as_global = True  # use permission_classes globally if True
    default_name = 'default'
    permissions = {}

    def get_permission_classes(self):
        global_classes = []
        if self.permission_classes_as_global:
            global_classes.extend(self.permission_classes)

        classes = self.permissions.get(self.action) \
                        or self.permissions.get(self.default_name)
        if classes:
            global_classes.extend(classes)

        return global_classes

    def get_permissions(self):
        return [permission() for permission in self.get_permission_classes()]
