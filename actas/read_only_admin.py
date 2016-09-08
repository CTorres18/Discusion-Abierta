__author__ = 'Nicolas'

from django.contrib import admin


class ReadOnlyModelAdmin(admin.ModelAdmin):

    actions = None

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return {}
        else:
            return self.fields or [f.name for f in self.model._meta.fields]

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        else:
            return False

    # Allow viewing objects but not actually changing them.
    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False
