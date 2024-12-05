from django.contrib import admin, messages
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms import Textarea
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_object_actions import DjangoObjectActions, action

from milea_base.fields import ProgressBarField
from milea_base.utils import create_log_entry, get_setting

# Default Naming
admin.site.site_header = admin.site.site_title = get_setting("milea_base.SHORT_NAME")
admin.site.index_title = 'Dashboard'


# Default Admin
class MileaAdmin(DjangoObjectActions, admin.ModelAdmin):

    show_sysdata = True  # Zeigt die Systemfelder an (created, updated, ...)

    list_display = ('verbose_id',)
    list_display_links = ('verbose_id',)
    milea_readonly_fields = ('created_at', '_created_by', 'updated_at', '_updated_by',)
    admin_fieldsets = ()
    search_fields = ['id',]
    list_per_page = 10

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 9})},
    }

    ##################
    # Property Fields
    ##################

    def _created_by(self, obj=None):
        if obj and obj.created_by is not None:
            return str(obj.created_by)
        elif obj and obj.created_by is None:
            return "Systemuser"
        return None
    _created_by.short_description = _("created by")

    def _updated_by(self, obj=None):
        if obj and obj.updated_by is not None:
            return str(obj.updated_by)
        elif obj and obj.updated_by is None:
            return "Systemuser"
        return None
    _updated_by.short_description = _("updated by")

    def is_active_badge(self, obj):
        return format_html(
            '<span class="badge bg-{} me-1"></span> {}', 'success' if obj.is_active else 'secondary', '',
        )
    is_active_badge.short_description = _("active")

    ##################
    # Action Buttons
    ##################

    @action(label=_("inactive"), description=_("Click this Button to activate this object"), attrs={'icon': "ti ti-at-off", 'class': 'btn-inactive btn-danger'})
    def set_to_active(self, request, obj):
        request.user.has_perm("%s.change_%s" % (obj._meta.app_label, obj._meta.model_name))
        if request.user.has_perm("%s.change_%s" % (obj._meta.app_label, obj._meta.model_name)):
            obj.is_active = False if obj.is_active else True
            obj.save()
            create_log_entry(request.user.id, obj, new=False, form=None, msg=_("Status changed to active"))
            messages.success(request, _("%s has been activated") % obj.name)
            return HttpResponseRedirect(reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk]))
        else:
            raise PermissionDenied()

    @action(label=_("active"), description=_("Click this Button to deactivate this object"), attrs={'icon': "ti ti-power", 'class': 'btn-success'})
    def set_to_inactive(self, request, obj):
        if request.user.has_perm("%s.change_%s" % (obj._meta.app_label, obj._meta.model_name)):
            obj.is_active = False if obj.is_active else True
            obj.save()
            create_log_entry(request.user.id, obj, new=False, form=None, msg=_("Status changed to inactive"))
            messages.success(request, _("%s has been deactivated") % obj.name)
            return HttpResponseRedirect(reverse('admin:%s_%s_change' % (obj._meta.app_label, obj._meta.model_name), args=[obj.pk]))
        else:
            raise PermissionDenied()

    def get_change_actions(self, request, object_id, form_url):
        actions = super().get_change_actions(request, object_id, form_url)
        actions = list(actions)

        obj = self.model.objects.get(pk=object_id)
        if obj.is_active and 'set_to_active' in actions:
            actions.remove('set_to_active')
        elif not obj.is_active and 'set_to_inactive' in actions:
            actions.remove('set_to_inactive')

        return actions

    ##################
    # Django / Others
    ##################

    def get_list_display(self, request):
        list_display = super().get_list_display(request)

        # Remove default Progress Bar Field, and add the render function
        for field in self.model._meta.fields:
            if isinstance(field, ProgressBarField):

                def render_progress_bar(obj, field_name=field.name):
                    value = getattr(obj, field_name)
                    return getattr(self.model._meta.get_field(field_name), 'get_progress_bar_html')(value)

                method_name = f"get_{field.name}_bar"
                list_display = list(map(lambda x: x.replace(field.name, method_name), list_display))
                list_display = tuple(list_display)
                setattr(self, method_name, render_progress_bar)
                render_progress_bar.short_description = field.verbose_name

        return list_display

    def get_readonly_fields(self, request, obj=None):
        default = super().get_readonly_fields(request, obj)
        return self.milea_readonly_fields + default

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj=obj)

        # Add special fieldsets for superuser
        if request.user.is_superuser:
            fieldsets += self.admin_fieldsets

        # Add system data fieldset
        if self.show_sysdata:
            fieldsets += (
                (_("System data"), {
                    'classes': ('milea-system-data mt-3 col-lg-12',),
                    'fields': (('created_at', '_created_by', 'updated_at', '_updated_by'),),
                }),
            )

        return fieldsets

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj=obj)

        # Remove the fields for the system data row
        fields = [field for field in fields if field not in ('is_active', 'created_at', '_created_by', 'updated_at', '_updated_by')]

        return fields

    def get_search_results(self, request, queryset, search_term):
        # Allow search with verbose_id
        if self.model.OBJ_VERB_TAG and search_term.startswith('%s.' % self.model.OBJ_VERB_TAG):
            search_term = search_term.split('.')
            search_term = int(search_term[1])
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        return queryset, use_distinct

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Ridiculous override just to get rid of the "Hold down" text. Done is better than perfect...
        form_field = super().formfield_for_manytomany(db_field, request, **kwargs)
        msg = _("Hold down “Control”, or “Command” on a Mac, to select more than one.")
        form_field.help_text = form_field.help_text.replace(str(msg), '').strip()
        return form_field

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('created_by', 'updated_by')
