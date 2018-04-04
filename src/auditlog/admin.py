from django.contrib import admin
from .models import LogEntry
from .mixins import LogEntryAdminMixin
from .filters import ResourceTypeFilter


class LogEntryAdmin(admin.ModelAdmin, LogEntryAdminMixin):
    list_display = ['created_date', 'created_time', 'resource_type',
                    'resource_url', 'action', 'msg_short', 'user_url']
    search_fields = ['timestamp', 'object_repr', 'changes', 'actor__email']
    list_filter = ['action', ResourceTypeFilter]
    readonly_fields = ['created', 'resource_url', 'action', 'user_url', 'msg']
    fieldsets = [
        (None, {'fields': ['created', 'user_url', 'resource_url']}),
        ('Changes', {'fields': ['action', 'msg']}),
    ]
    date_hierarchy = 'timestamp'

    def has_add_permission(self, request):
        # As audit admin doesn't allow log creation from admin
        return False


admin.site.register(LogEntry, LogEntryAdmin)
