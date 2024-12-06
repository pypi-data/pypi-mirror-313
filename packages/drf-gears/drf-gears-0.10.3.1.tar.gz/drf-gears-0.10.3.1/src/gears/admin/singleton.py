from django.contrib import admin
from django.urls import path


class SingletonModelAdmin(admin.ModelAdmin):
    def get_urls(self):
        urlpatterns = super().get_urls()
        try:
            model_name = self.model.__class__.__name__.lower()
            custom_urlpatterns = [
                path(r'',
                     self.admin_site.admin_view(self.change_view),
                     {'object_id': str(self.model.get().pk)},
                     name=f'{self.model._meta.app_label}_{model_name}_change',
                     ),
            ]
        except AttributeError as e:
            custom_urlpatterns = []
        return custom_urlpatterns + urlpatterns

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
