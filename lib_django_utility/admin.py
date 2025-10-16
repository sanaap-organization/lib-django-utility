from django import forms
from django.contrib import admin


def get_related_field(name, admin_order_field=None, short_description=None):
    related_names = name.split("__")

    def dynamic_attribute(obj):
        for related_name in related_names:
            obj = getattr(obj, related_name)
            if obj is None:
                break
        return obj

    dynamic_attribute.admin_order_field = admin_order_field or name
    dynamic_attribute.short_description = short_description or related_names[-2].title().replace(
        "_", " "
    )
    return dynamic_attribute


class RelatedFieldAdminMixin:
    def __getattr__(self, attr):
        if "__" in attr:
            return get_related_field(attr)
        # not dynamic lookup, default behaviour
        return self.__getattribute__(attr)

    def get_list_display(self, request):
        list_display = list(self.list_display)
        list_display.append("is_active")
        return list_display

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model.all_objects.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def soft_delete_selected(self, request, queryset):
        """Soft delete the selected objects."""
        for obj in queryset:
            obj.delete(soft=True)
        self.message_user(request, "Selected records were soft deleted.")

    soft_delete_selected.short_description = "Soft delete selected objects"

    def restore_selected(self, request, queryset):
        """Restore the selected objects."""
        for obj in queryset:
            obj.restore()
        self.message_user(request, "Selected records were restored.")

    restore_selected.short_description = "Restore selected objects"

    actions = ["soft_delete_selected", "restore_selected"]


class CustomModelChoiceFieldMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the queryset for ModelChoiceField fields
        for field_name, field in self.fields.items():
            if isinstance(field, forms.ModelChoiceField):
                # Example: Only include active users
                field.queryset = field.queryset.model.objects.all()


class CustomAdminModelForm(CustomModelChoiceFieldMixin, forms.ModelForm):
    pass


class BaseModelAdmin(RelatedFieldAdminMixin, admin.ModelAdmin):
    form = CustomAdminModelForm

    # Ensure all inline forms also use the custom form
    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = self.form
        return super().get_form(request, obj, **kwargs)
