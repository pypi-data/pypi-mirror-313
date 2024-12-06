class ConditionalQuerysetMixin:
    """
    ConditionalQuerysetMixin gives you an ability to have multiple `get_queryset`
    methods for every needs.

    Querysets mapping
    `querysets` - is a dictionary of named querysets. You can provide different
    querysets for any action.

    Named queryset method
    Use named methods like `get_name_queryset`, where `name` is an any name.

    ViewSet actions
    If ConditionalQuerysetMixin can't find a mapped or named queryset, it will try to
    find a method with a ViewSet action instead of name.
    E.g: `get_list_queryset`, `get_update_queryset`, get_custom_action_queryset.
    """
    querysets = {}

    def get_queryset(self, **kwargs):
        queryset = super().get_queryset()
        name = kwargs.get('name', self.action)
        if name:
            queryset = self.querysets.get(name, queryset)
        method = self.try_method(f"get_{name}_queryset")
        if method:
            queryset = method(queryset)
        return queryset

    def try_method(self, method_name: str):
        return getattr(self, method_name, None)
