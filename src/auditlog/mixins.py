import json

from django.conf import settings
try:
    from django.core import urlresolvers
except ImportError:
    from django import urls as urlresolvers
try:
    from django.urls.exceptions import NoReverseMatch
except ImportError:
    from django.core.urlresolvers import NoReverseMatch
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

MAX = 75


class LogEntryAdminMixin(object):

    def created_date(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d')
    created_date.short_description = _('Date')

    def created_time(self, obj):
        return obj.timestamp.strftime('%H:%M:%S')
    created_time.short_description = _('Time')

    def created(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    created.short_description = _('Created')

    def user_url(self, obj):
        if obj.actor:
            app_label, model = settings.AUTH_USER_MODEL.split('.')
            viewname = 'admin:%s_%s_change' % (app_label, model.lower())
            try:
                link = urlresolvers.reverse(viewname, args=[obj.actor.id])
            except NoReverseMatch:
                return u'%s' % (obj.actor)
            return format_html(u'<a href="{}">{}</a>', link, obj.actor)

        return _('system')
    user_url.short_description = _('User')

    def resource_url(self, obj):
        app_label, model = obj.content_type.app_label, obj.content_type.model
        viewname = 'admin:%s_%s_change' % (app_label, model)
        try:
            args = [obj.object_pk] if obj.object_id is None else [obj.object_id]
            link = urlresolvers.reverse(viewname, args=args)
        except NoReverseMatch:
            return obj.object_repr
        else:
            return format_html(u'<a target="_blank" href="{}">{}</a>', link, obj.object_repr)
    resource_url.short_description = _('Resource URL')

    def resource_type(self, obj):
        model_class = obj.content_type.model_class()
        if model_class:
            label = model_class._meta.verbose_name
        else:
            label = obj.content_type.model
        return _(label).title()
    resource_type.short_description = _('Resource Type')

    def msg_short(self, obj):
        if obj.action == obj.Action.DELETE:
            return ''
        return '{}'.format(len(obj.changes_display_dict))
    msg_short.short_description = _('Changes')

    def msg(self, obj):
        if obj.action == 2:
            return  # delete

        msg = '<table><tr><th>#</th><th>Field</th><th>From</th><th>To</th></tr>'
        for i, field in enumerate(sorted(obj.changes_display_dict), 1):
            # TODO: move sensitive field names to settings
            value = [i, field] + (['***', '***'] if field == 'password' else obj.changes_display_dict[field])
            msg += format_html('<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>', *value)

        msg += '</table>'
        return mark_safe(msg)
    msg.short_description = _('Changes')
