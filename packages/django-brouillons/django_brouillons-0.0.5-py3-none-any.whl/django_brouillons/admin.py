# Standard Library
from functools import reduce
from operator import or_

# Django
from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin
from django.contrib.admin.exceptions import DisallowedModelAdminToField
from django.contrib.admin.options import TO_FIELD_VAR
from django.contrib.admin.utils import unquote
from django.core.exceptions import ValidationError
from django.db.models import Case, F, Q, Value, When
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class PublishedChangesListFilter(admin.SimpleListFilter):
    title = _("Changes published")
    parameter_name = "changes_published"

    def lookups(self, request, model_admin):
        return (
            (1, _("Yes")),
            (0, _("No")),
        )

    def queryset(self, request, queryset):
        value = self.value()

        if value:
            lookups = [int(lookup) == 1 for lookup in value.split(",")]

            queryset = queryset.annotate(
                unpublished_changes=Case(
                    When(last_publication_date__isnull=True, then=Value(True)),
                    When(
                        last_publication_date__lt=F("last_edition_date"),
                        then=Value(True),
                    ),
                    default=Value(False),
                )
            )

            filters = []

            if True in lookups:
                filters.append(Q(unpublished_changes=False))
            if False in lookups:
                filters.append(Q(unpublished_changes=True))

            queryset = queryset.filter(reduce(or_, filters))

        return queryset


class DraftModelAdminMixin:
    """Mixin to handle drafts of models."""

    include_create_draft_link = True
    include_publish_draft_link = True
    include_version_link = True

    list_display = ("get_published_changed",)

    list_filter = (PublishedChangesListFilter,)

    readonly_fields = ("get_published_changed",)

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        if "/autocomplete/" in request.META.get(
            "REQUEST_URI", []
        ):  # If the request is an autocomplete request
            # Unfortunately, the only wait to know if the request is an autocomplete request is to check the URL because all django admin views are wrapped in a single view "catch_all_view" : https://github.com/django/django/blob/6ee37ada3241ed263d8d1c2901b030d964cbd161/django/contrib/admin/sites.py#L310

            qs = (
                self.model.publics.all()
            )  # Link to public version in autocomplete, override the method for a custom behavior
        else:
            qs = self.model.drafts.all()  # Display drafts by default in changelist

        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def get_object(self, request, object_id, from_field=None):
        """
        Return an instance matching the field and value provided, the primary
        key is used if no field is provided. Return ``None`` if no match is
        found or the object_id fails validation.
        """
        queryset = self.model._default_manager.all()  # Do not use get_queryset here
        model = queryset.model
        field = (
            model._meta.pk if from_field is None else model._meta.get_field(from_field)
        )
        try:
            object_id = field.to_python(object_id)
            return queryset.get(**{field.name: object_id})
        except (model.DoesNotExist, ValidationError, ValueError):
            return None

    def change_view(self, request, object_id, form_url="", extra_context=None):
        to_field = request.POST.get(TO_FIELD_VAR, request.GET.get(TO_FIELD_VAR))
        if to_field and not self.to_field_allowed(request, to_field):
            raise DisallowedModelAdminToField(
                "The field %s cannot be referenced." % to_field
            )

        obj = self.get_object(request, unquote(object_id), to_field)
        extra_context = extra_context or {}
        badge = '<sup class="draft-unpublished-badge">*</sup>'
        if obj is not None:
            if obj.last_publication_date:
                title = _(
                    "There are unpublished changes (last edition: {}, last publication: {})"
                ).format(
                    formats.date_format(obj.last_edition_date, "SHORT_DATETIME_FORMAT"),
                    formats.date_format(
                        obj.last_publication_date, "SHORT_DATETIME_FORMAT"
                    ),
                )
            else:
                title = _(
                    "There are unpublished changes (last edition: {}, last publication: never published)"
                ).format(
                    formats.date_format(obj.last_edition_date, "SHORT_DATETIME_FORMAT"),
                )

        if self.include_publish_draft_link or self.include_create_draft_link:
            if self.include_publish_draft_link:
                if obj is not None and obj.is_public and not obj.has_draft_version:
                    extra_context.update(
                        include_create_draft_link=self.include_create_draft_link,
                        include_publish_draft_link=False,  # We cannot publish public version
                        create_draft_link_label=_("Create a draft"),
                    )
                elif obj is not None and obj.is_draft:
                    if obj.has_unpublished_changes:
                        publish_draft_link_label = mark_safe(_("Publish draft") + badge)
                        publish_draft_link_title = title
                        publish_draft_link_disabled = False
                    else:
                        publish_draft_link_title = _(
                            "The last changes are already published (last publication: {})"
                        ).format(
                            formats.date_format(
                                obj.last_publication_date, "SHORT_DATETIME_FORMAT"
                            ),
                        )
                        publish_draft_link_label = _("Publish draft")
                        publish_draft_link_disabled = True

                    extra_context.update(
                        include_publish_draft_link=self.include_publish_draft_link,
                        publish_draft_link_label=publish_draft_link_label,
                        publish_draft_link_title=publish_draft_link_title,
                        publish_draft_link_disabled=publish_draft_link_disabled,
                    )

            # Handle form data after submit
            if (
                self.include_create_draft_link
                and obj is not None
                and "_createdraft" in request.POST
            ):
                draft_version = obj.create_draft()
                self.message_user(
                    request, _("New draft created"), level=messages.SUCCESS
                )
                draft_version_admin_url = reverse(
                    "admin:{}_{}_change".format(
                        draft_version._meta.app_label, draft_version._meta.model_name
                    ),
                    args=(draft_version.pk,),
                )
                return HttpResponseRedirect(draft_version_admin_url)

            if (
                self.include_publish_draft_link
                and obj is not None
                and "_publishdraft" in request.POST
            ):
                public_version = obj.publish_draft()
                self.message_user(
                    request, _("Publication successful"), level=messages.SUCCESS
                )
                public_version_admin_url = reverse(
                    "admin:{}_{}_change".format(
                        public_version._meta.app_label, public_version._meta.model_name
                    ),
                    args=(public_version.pk,),
                )
                return HttpResponseRedirect(public_version_admin_url)

        if self.include_version_link and obj is not None:
            version = (
                getattr(obj, "draft_version", None)
                if obj.has_draft_version
                else getattr(obj, "public_version", None)
            )
            if version is not None:
                version_link_title = ""

                if obj.is_public:
                    if obj.has_unpublished_changes:
                        version_link_label = mark_safe(_("Go to draft version") + badge)
                        version_link_title = title
                    else:
                        version_link_label = _("Go to draft version")
                else:
                    version_link_label = _("Go to public version")

                extra_context.update(
                    {
                        "include_version_link": True,
                        "version_link_label": version_link_label,
                        "version_link_title": version_link_title,
                        "version_link_url": reverse(
                            "admin:{}_{}_change".format(
                                version._meta.app_label, obj._meta.model_name
                            ),
                            args=(version.pk,),
                        ),
                    }
                )
            else:
                extra_context.update(include_version_link=False)

        return super().changeform_view(request, object_id, form_url, extra_context)

    @admin.display(description=_("Changes published"), boolean=True)
    def get_published_changed(self, obj):
        return obj.has_unpublished_changes is False


class DraftModelAdmin(DraftModelAdminMixin, ModelAdmin):
    """Draft model admin view."""
