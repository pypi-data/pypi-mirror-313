# Django
from django.db import models
from django.utils.timezone import now


class PublicManager(models.Manager):
    def get_queryset(self):
        # Local application / specific library imports
        from .queries import public_version_q

        return super().get_queryset().filter(public_version_q)

    def create(self, *args, **kwargs):
        # Local application / specific library imports
        from .models import VersionStatus

        kwargs.update(
            {
                "version_status": VersionStatus.PUBLIC.value,
                "first_publication_date": now(),
            }
        )
        return super().create(*args, **kwargs)


class DraftManager(models.Manager):
    def get_queryset(self):
        # Local application / specific library imports
        from .queries import draft_version_q

        return super().get_queryset().filter(draft_version_q)

    def create(self, *args, **kwargs):
        # Local application / specific library imports
        from .models import VersionStatus

        kwargs.update(version_status=VersionStatus.DRAFT.value)
        return super().create(*args, **kwargs)
