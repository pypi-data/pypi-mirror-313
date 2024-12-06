# Draft

If you add the DraftModel on a model, all existing instance will be draft instances. You may then:
- create a public version of all drafts with `instance.publish_draft()` method
- or set the `version_status` field to `VersionStatus.PUBLIC.value` to transform them to public versions without draft versions

To create a new draft only version, use `YourModel.drafts.create(...)`.
To create a draft of a public version use `YourInstance.create_draft()`.
To create a new publics only version, use `YourModel.publics.create(...)`.
To publish a draft version use `YourInstance.publish_draft()`.
To get only drafts or publics versions of related objects, use `YourModelInstance.your_related_field(manager="drafts")`.

## TODO

- [ ] do not ignore slug field when publishing
- [ ] copy m2m to draft
- [ ] test m2m and fk fields
- [ ] refactor tests (draft only items / public only items / isolated test models)

## Note

### Public objects linked to draft objects

A public object can be linked to a draft object: for example a Component is always the public version.
So we do not want to enforce that a draft object is linked only with related draft objects and public object linked with related public objects.

### Parent

When we create_draft() on Composition, if no draft already exists we must create a draft Composition linked to a draft Product.
But the create_draft() method has no idea that `product` is the FK "parent": this is why we define a `_draft_parent_field = "product"`

### Set "publics" as default manager

With Django==3.2, when default_manager_name is "publics", m2m.remove(obj) does not work...
