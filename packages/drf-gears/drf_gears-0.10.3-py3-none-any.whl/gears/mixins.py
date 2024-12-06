# class MeViewSetMixin:
#     available_methods = []
#
#     def get_user(self, request):
#         return request.user
#
#     @action(methods=['get'])
#     def me(self, request, *args, **kwargs):
#         user = self.get_user(request)
#         if not user.is_authenticated:
#             return Response(status=status.404)
#         serializer = self.get_serializer(instance=user)
#         return Response(serializer.data)
#
#     @me.mark('patch')
#     def me_update(self, request, *args, **kwargs):
#         pass
