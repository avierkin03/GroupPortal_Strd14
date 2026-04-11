from django.core.exceptions import PermissionDenied

class UserMaterial(object):
    def dispatch(self, request, *args, **kwargs):
        isinstance = self.get_object()
        if isinstance.creator == self.request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)