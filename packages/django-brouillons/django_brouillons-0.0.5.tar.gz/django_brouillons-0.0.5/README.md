# Django-brouillons

Handle "draft" and "public" versions of your models in Django ORM.

This module is still in a WIP version and should not be used in production if you don't know what you're doing.
This modules aims to handle with a quite complex subject that requires that you add unit tests to your project to be absolutely sure that it does what you're expect in your specific cases.
For now, we're aware that the module doesn't covers all of the cases of duplications of models tree, but we're hopping to increase them over the time.

It uses [django-clone](https://pypi.org/project/django-clone/) on the inside to duplicates django ORM models.
We recommend that you start with understanding how `django-clone` works before diving into `django-brouillons`.


![Pipeline badge](https://gitlab.com/kapt/open-source/django-brouillons/badges/main/pipeline.svg)
![Coverage badge](https://gitlab.com/kapt/open-source/django-brouillons/badges/main/coverage.svg)
![Release badge](https://gitlab.com/kapt/open-source/django-brouillons/-/badges/release.svg)

## How it is working ?

![Schema](docs/schemas/draft_and_public.jpg)

`Django-brouillons` duplicates objects of a given model that aims to be moderated in two versions `public` and `draft`.

The `draft` version can then be published so that its values are updated in the `public` version.

----

## Contributing

Feel free to send feedbacks on the module using it's [Home page](https://gitlab.com/kapt/open-source/django-brouillons).


See [CONTRIBUTING.md](CONTRIBUTING.md) for contributions.

----

## Install

1. Install the module from [PyPI](https://pypi.org/project/django-brouillons/):
    ```
    python3 -m pip install django-brouillons
    ```

    Or, if you're using poetry :
    ```
    poetry add django-brouillons
    ```

2. Add it in your `INSTALLED_APPS`:
    ```
      "django_brouillons",
    ```
----


## Config

### In your models

1. To handle `draft` and `public` status in a django model, inherit from the `DraftModel` class:

    ```
    from django_brouillons.models import DraftModel

    class DraftableObject(DraftModel):
      ...
    ```

2. Then you need to configure the [django-clone settings](https://github.com/tj-django/django-clone?tab=readme-ov-file#explicit-include-only-these-fields) for the model, and that will describe what strategy should be adopted regarding model related fields (for `Many to many`, `ForeignKey`, `OneToOne`, ...)

    ```
    from django_brouillons.models import DraftModel

    class DraftableObject(DraftModel):
      _clone_m2o_or_o2m_fields = ["draftable_object_many_to_many2_through"]
      _clone_linked_m2m_fields = ["many_to_many_objects"]

    ...
    many_to_many_objects = models.ManyToManyField("DraftableObjectManyToMany")
    many_to_many_2_objects_through = models.ManyToManyField(
        "DraftableObjectManyToMany2",
        through="DraftableObjectManyToMany2Through",
        through_fields=("draftable_object", "draftable_object_many_to_many_2"),
    )

    ```

As an example, you can have a look at the [test app models](tests/testapp/models.py).

In this example, the following will be applied:

- `many_to_many_objects` field : The `m2m` fields will reference the same related objects without duplicated the related objects
- `draftable_object_many_to_many2_through` field : The related objects of the table designed as `draftable_object_many_to_many2_through` related name will be duplicated


3. If your model contains some `CharFields` fields having `unique=True` they must be prefixed in the `Draft` version of the model, so that they remains unique between `Public` and `Draft` versions.

    This can be done filling the `_draft_prefixed_fields` attribute's of your model inheriting from the `DraftModel` abstract model :

    ```
    from django_brouillons.models import DraftModel

    class DraftableObject(DraftModel):
      _clone_m2o_or_o2m_fields = ["draftable_object_many_to_many2_through"]
      _clone_linked_m2m_fields = ["many_to_many_objects"]
      _draft_prefixed_fields = ["slug"]

      slug = models.SlugField(max_length=255, unique=True)
    ```

In this example, the `DraftableObject` contains a field `slug` that's unique.

Listing it in the `_draft_prefixed_fields` attribute indicates `django-brouillons` that the value must be prefixed with the value of the `_draft_prefix` attribute upon duplication in a `draft`.


### In the admin

Django-brouillon provides [admin integrations](django_brouillons/admin.py).

1. Model admin can inherit from the `DraftModelAdminMixin` or the `DraftModelAdmin` :

    ```
      from django_brouillons.admin import DraftModelAdminMixin
      @admin.register(DraftableObject)  # Must be referenced to allow autocomplete
      class DraftableObjectAdmin(
          DraftModelAdmin
      ):
        pass
    ```

    Doing so, several buttons will be added to your admin model change's view :

    - Navigate between the `Public` and `Draft` versions of the objects in the admin
    - Publish a `draft` version of an object into a `public` version
    - Create a `draft` version of an object having only a `public`

2. The `DraftModelAdminMixin` contains a `PublishedChangesListFilter` filter in its `list_filter` attribute that adds the the capability to filter objects having unpublished changes or not.

    This filter can manually be set in the `list_filter` if needed :

    ```
      from django_brouillons.admin import DraftModelAdminMixin, PublishedChangesListFilter
      @admin.register(DraftableObject)  # Must be referenced to allow autocomplete
      class DraftableObjectAdmin(
          DraftModelAdmin
      ):
        list_filter = (PublishedChangesListFilter,)
    ```


## Model API

Django-brouillons provides the following in it's model attributes :

- `DraftableObject.is_public` : Indicates if the current instance is public
- `DraftableObject.is_draft` : Indicates if the current instance is draft
- `DraftableObject.has_public_version` : Indicates if the current instance has a public version
- `DraftableObject.has_draft_version` : Indicates if the current instance has a draft version
- `DraftableObject.has_unpublished_changes` : Indicates if the current instance has pending unpublished changes
- `DraftableObject.create_draft()` : Creates a draft from a public version
- `DraftableObject.publish_draft()` : Publish changes of a draft version in a public version :
    - Creates and returns a new `public_version` if didn't exists
    - Updates and returns the `public_version` if already exists


## Tests

Tests are located in the `tests` packages.

Tests are written with [pytest](https://docs.pytest.org/en/).
They are based on a [testapp models](tests/testapp/models.py) :

![Test app models schema](docs/schemas/testapp_models.jpg)


To run the tests, you must launch the command [./launch_tests.sh](launch_tests.sh)

A coverage report can be generated using the command [./run_coverage.sh](run_coverage.sh)

