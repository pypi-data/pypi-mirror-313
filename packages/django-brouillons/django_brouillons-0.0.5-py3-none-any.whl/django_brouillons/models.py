# Standard Library
import itertools
from contextlib import suppress

# Django
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

# Third party
from model_clone.models import CloneModel

# Local application / specific library imports
from . import exceptions
from .managers import DraftManager, PublicManager


class VersionStatus(models.TextChoices):
    DRAFT = "DRAFT", _("Draft version")
    PUBLIC = "PUBLIC", _("Public version")


class DraftModel(CloneModel):
    USE_UNIQUE_DUPLICATE_SUFFIX = False
    _clone_excluded_fields = ["version_status"]
    _clone_excluded_o2o_fields = ["draft_version", "public_version"]

    # Fields that must be prefixed by _draft_prefix when creating a draft
    # and unprefixed when publishing a draft.
    # a list of strings
    _draft_prefixed_fields = []

    # String to insert before prefixed fields
    _draft_prefix = "draft-"

    # When creating a draft, we need to attach draft child objects to the draft version of their parent.
    # The _draft_parent_field (a string) is used to describe the name of the field that points to the parent object.
    _draft_parent_field = None

    version_status = models.CharField(
        choices=VersionStatus.choices,
        verbose_name=_("Version"),
        default=VersionStatus.DRAFT,
        max_length=20,
    )
    draft_version = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        related_name="public_version",
    )
    creation_date = models.DateTimeField(
        verbose_name=_("Creation date"), null=True, auto_now_add=True
    )
    first_publication_date = models.DateTimeField(
        verbose_name=_("First publication date"), null=True
    )
    last_edition_date = models.DateTimeField(
        verbose_name=_("Last modification date"), null=True, auto_now=True
    )
    last_publication_date = models.DateTimeField(
        verbose_name=_("Last publication date"), null=True
    )

    objects = models.Manager()
    publics = PublicManager()
    drafts = DraftManager()

    class Meta:
        abstract = True

    def __repr__(self):
        return super().__repr__() + f"({self.get_version_status_display()})"

    def save(self, *args, **kwargs):
        """
        For each field in _draft_prefixed_fields:
        - if the object saved is a draft
            prefix the value by _draft_prefix
        - else if it is a public version
            remove draft prefix
        """
        for field_name in self._draft_prefixed_fields:
            field_value = getattr(self, field_name, None)
            if field_value is not None:
                if self.is_draft and not field_value.startswith(self._draft_prefix):
                    setattr(self, field_name, self._draft_prefix + field_value)
                elif self.is_public and field_value.startswith(self._draft_prefix):
                    setattr(
                        self, field_name, field_value.replace(self._draft_prefix, "")
                    )
        return super().save(*args, **kwargs)

    @property
    def is_public(self):
        return self.version_status == VersionStatus.PUBLIC.value

    @property
    def is_draft(self):
        return not self.is_public

    @property
    def has_public_version(self):
        try:
            self.public_version
            return True
        except ObjectDoesNotExist:
            return False

    @property
    def has_draft_version(self):
        return self.draft_version is not None

    @property
    def has_unpublished_changes(self):
        draft_version = self.draft_version if self.has_draft_version else self

        if draft_version.last_publication_date is None:
            return True

        return draft_version.last_publication_date < draft_version.last_edition_date

    def make_clone(self, attrs=None, sub_clone=False, using=None, parent=None):
        """
        We must override make_clone to link a draft_version with its public_version,
        because this method is recursively called on all sub objects.
        """

        # If we clone a public_version to create a draft_version
        if self.version_status == VersionStatus.PUBLIC.value:
            # Public -> Draft
            draft_version = super().make_clone(
                attrs=attrs, sub_clone=sub_clone, using=using, parent=parent
            )
            self.draft_version = draft_version
            self.save(update_fields=["draft_version"])
            return draft_version
        # Else if we clone a draft_version to create a public_version
        else:
            # Draft -> Public
            public_version = super().make_clone(
                attrs=attrs, sub_clone=sub_clone, using=using, parent=parent
            )
            public_version.draft_version = self
            public_version.save(update_fields=["draft_version"])
            return public_version

    def create_draft(self, *args, attrs={}, **kwarg):
        with transaction.atomic():
            current_time = now()
            draft_version = getattr(self, "draft_version", None)
            public_version = getattr(self, "public_version", None)

            # If both public and draft version exist: we have a problem
            if draft_version is not None and public_version is not None:
                raise exceptions.InvalidVersionError(
                    "An object cannot have a public and a draft version"
                )

            if self.is_public:
                public_version = self

            elif self.is_draft:
                draft_version = self

            # If it is a public version without a draft, we need to create a new draft version
            if self.is_public and draft_version is None:
                if self.id:  # Only if self is already saved in database
                    attrs.update(
                        {
                            "version_status": VersionStatus.DRAFT.value,
                            "creation_date": current_time,
                            "last_edition_date": current_time,
                        }
                    )

                if self._draft_parent_field is not None:
                    parent = getattr(public_version, self._draft_parent_field, None)
                    if parent is not None:
                        if parent.draft_version is not None:
                            attrs.update(
                                {self._draft_parent_field: parent.draft_version}
                            )
                        else:
                            raise exceptions.ParentDraftVersionError(
                                f"Cannot create a draft of this object because no draft version of `{self._draft_parent_field}` exists"
                            )
                draft_version = self.make_clone(attrs=attrs)
                return draft_version
            else:
                # Draft version already exists
                raise exceptions.DraftVersionExistsError(
                    f"Draft version of object `{self}` already exists"
                )

    def publish_draft(self, attrs={}):
        with transaction.atomic():
            current_time = now()

            draft_version = getattr(self, "draft_version", None)
            public_version = getattr(self, "public_version", None)

            # If both public and draft version exist: we have a problem
            if draft_version is not None and public_version is not None:
                raise exceptions.InvalidVersionError(
                    "An object cannot have a public and a draft version"
                )

            if self.is_public:
                raise exceptions.PublishPublicVersionError(
                    "Cannot publish a public version"
                )
            else:
                draft_version = self

            # If it is a draft version without a public version, we need to create a clone
            if self.is_draft and public_version is None:
                draft_version.first_publication_date = current_time
                attrs.update(version_status=VersionStatus.PUBLIC.value)
                public_version = draft_version.make_clone(
                    attrs=attrs
                )  # the clone is the public version

                # make_clone triggers an update of last_edition_date field
                # we need to set last_publication_date to the same date as last_edition_date
                publication_time = public_version.last_edition_date
                public_version.last_publication_date = publication_time

                draft_version.version_status = VersionStatus.DRAFT.value
                draft_version.last_publication_date = publication_time
                draft_version.save(
                    update_fields=[
                        "first_publication_date",
                        "last_publication_date",
                        "version_status",
                    ]
                )
                return public_version

            # Else, copy the draft version to the public version: recreating related o2o, o2m and m2m

            # Copy regular fields
            for field in self._get_publish_fields():
                if not isinstance(field, models.OneToOneField):
                    setattr(
                        public_version, field.name, getattr(draft_version, field.name)
                    )

            # Copy o2o fields (in direction draft_version -> related o2o)
            to_delete_o2o = []
            for field in self._get_publish_fields():
                if isinstance(field, models.OneToOneField):
                    draft_sub_instance = getattr(draft_version, field.name, None)
                    public_sub_instance = getattr(public_version, field.name, None)
                    # Remove the related o2o object if it exists
                    if public_sub_instance:
                        setattr(public_version, field.name, None)
                        to_delete_o2o.append(public_sub_instance)

                    if draft_sub_instance:
                        # Re-create the o2o
                        public_sub_instance = draft_version._create_copy_of_instance(
                            draft_sub_instance,
                            force=True,
                            sub_clone=True,
                        )
                        public_sub_instance.save()
                        setattr(public_version, field.name, public_sub_instance)

            # Remove and recreate the o2m
            for f in itertools.chain(
                self._meta.related_objects, self._meta.concrete_fields
            ):
                if f.one_to_many:
                    if any(
                        [
                            f.get_accessor_name() in self._clone_m2o_or_o2m_fields,
                            self._clone_excluded_m2o_or_o2m_fields
                            and f.get_accessor_name()
                            not in self._clone_excluded_m2o_or_o2m_fields,
                        ]
                    ):
                        getattr(public_version, f.get_accessor_name()).all().delete()

            # Re-create the o2m
            public_version = draft_version._CloneMixin__duplicate_o2m_fields(
                public_version
            )

            # Remove and recreate the o2o
            for f in self._meta.related_objects:
                if f.one_to_one:
                    if any(
                        [
                            f.name in self._clone_o2o_fields
                            and f not in self._meta.concrete_fields,
                            self._clone_excluded_o2o_fields
                            and f.name not in self._clone_excluded_o2o_fields
                            and f not in self._meta.concrete_fields,
                        ]
                    ):
                        with suppress(ObjectDoesNotExist):
                            public_o2o = getattr(public_version, f.get_accessor_name())
                            public_o2o.delete()

            # Re-create the o2o
            public_version = draft_version._CloneMixin__duplicate_o2o_fields(
                public_version
            )

            # Force the linked m2m to be re-assigned
            public_version = draft_version._CloneMixin__duplicate_linked_m2m_fields(
                public_version
            )

            public_version.last_publication_date = current_time
            public_version.save()

            draft_version.last_publication_date = current_time
            draft_version.save(update_fields=["last_publication_date"])

            # Delete the o2o that were removed, after saving the public version otherwise the public version can be removed by a cascade constraint
            for obj in to_delete_o2o:
                obj.delete()

        return public_version

    def _get_publish_fields(self, exclude=[]):
        fields = []

        exclude.extend(self._draft_prefixed_fields)
        exclude.extend(["version_status", "draft_version"])
        exclude = set(exclude)

        for field in self._meta.concrete_fields:
            if all(
                [
                    not getattr(field, "primary_key", False),
                    field.name != self._draft_parent_field,
                    field.name not in exclude,
                ]
            ):
                fields.append(field)
        return fields
