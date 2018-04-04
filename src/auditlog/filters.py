from django.contrib.admin import SimpleListFilter
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

class ResourceTypeFilter(SimpleListFilter):
    title = _('Resource Type')
    parameter_name = 'resource_type'

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        content_types = ContentType.objects.filter(pk__in=qs.values_list('content_type')).order_by('model')
        for content_type in content_types:
            model_class = content_type.model_class()
            if model_class:
                label = model_class._meta.verbose_name
            else:
                label = content_type.model
            yield (content_type.id, _(label).title())

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return queryset.filter(content_type_id=self.value())
