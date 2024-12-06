class VersionError(Exception):
    pass


class DraftVersionExistsError(VersionError):
    pass


class PublishPublicVersionError(VersionError):
    pass


class InvalidVersionError(VersionError):
    pass


class ParentDraftVersionError(VersionError):
    pass
