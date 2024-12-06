# Django
from django.db.models import Q

# Local application / specific library imports
from .models import VersionStatus

draft_version_q = Q(version_status=VersionStatus.DRAFT.value)
public_version_q = Q(version_status=VersionStatus.PUBLIC.value)
