from ..exceptions.views import GearsViewException


class ServiceDataViewSetMixin(object):
    def get_renderer_context(self):
        context = super().get_renderer_context()
        try:
            context.update({
                'service': self.get_service_data(self.request)
            })
        except AttributeError:
            GearsViewException("The method get_service_data not found.")
        return context
