# ognajD<sup><sup>_v0.2.4_</sup></sup>

Django app which handles ORM objects' versions.

## Description

**ognajD** is Django-compactible application which handles versionning for ORM models.
Main feature is for **ognjaD** to be a "plug-in" Django application, thus capable to 
work with "little-to-no" configuring and changes to Django project.

### Features
**ognajd** stores objects' versions in own table, relied on `contenttypes` application.

**ognajD** @ [v0.2.4](https://github.com/omelched/django-ognajd/releases/tag/v0.2.4) can:

 - catch object's save / update signals
 - store snapshot of object in DB with:
   - timestamp
   - serialized version
   - hash
 - object version may be serialized (currently, only JSON) as:
   - diff with previous version _(by default)_
   - raw dumps
 - inline with versione for admin models

### Usage example

[`sample-project`](sample_project) is a showcase django project, based on famous
[`polls`](https://docs.djangoproject.com/en/3.2/intro/tutorial01/#creating-the-polls-app) application.
You can reference to it for usage cases, examples, testing.You must never deploy `sample_project` in
production due to exposed `SECRET_KEY`.

## Getting Started

### Dependencies

#### Python packages

* `django~=3.2.7` <sub><sub>might work on lesser versions, not tested</sub></sub>
* `jsondiff~=1.3.0` <sub><sub>might work on lesser versions, not tested</sub></sub>

#### Django applications

* `contenttypes`

### Installing

#### Using Python Package Index

* make sure to use latest `pip`:
  ```shell
  python3 -m pip install --upgrade pip
  ```

* install `django-ognajd`:
  ```shell
  python3 -m pip install django-ognajd
  ```
  
#### OR download package from releases

* download release asset (`.tar.gz` or `.whl`)

* make sure to use latest `pip`:
  ```shell
  python3 -m pip install --upgrade pip
  ```

* install `django-ognajd` from file:
  ```shell
  python3 -m pip install /path/to/downloaded/asset.tar.gz # or .whl
  ```

#### OR clone from repository 

* clone project:
  ```shell
  git clone \
          --depth=1 \
          --branch=master \
          git@github.com:omelched/django-ognajd.git \
          </path/to/downloads>
  ```

* move `/django-ognajd/ognajd` solely to folder containing django apps
  ```shell
  mv      </path/to/downloads>/django-ognajd/ognajd \
          </path/to/django/project/apps>
  ```
  
* remove leftovers
  ```shell
  rm -rf  </path/to/downloads>/django-ognajd
  ```

### Configuring

#### Installing application

Add `ognajd` to `INSTALLED_APPS` in your Django project `settings.py`.
Make sure it is installed **before** `django.contrib.admin`. 

If you installed package [the third way](#or-clone-from-repository), `</path/to/django/project/apps>`
must be added to `PYTHONPATH`. If you not sure add code below in your Django project `manage.py` before calling `main()`:
```python
sys.path.append('</path/to/django/project/apps>')
```

#### Registering models

To register your model as eligible for versioning add attribute-class `VersioningMeta` to model class definition.
For typing, linters, autocompletion tyou can inherit from `ognajd.models.VersioningMeta`.

Then set preferred options.

e.g:

```python
# .../your_app/models.py

from django.db import models

from ognajd.models import VersioningMeta


class Question(models.Model):
    
    class VersioningMeta(VersioningMeta):
        store_diff = False

    ... # fields' definitions
```

#### `VersioningMeta` options

| Name                  | Description                                                             | Type    | Default |
|-----------------------|-------------------------------------------------------------------------|---------|---------|
| `enabled`             | `True`: if model will be versioned <br> `False`: if will not            | `bool`  | `True`  |
| `store_diff`          | `True`: model's history will be stored as diffs <br> `False`: as dumps  | `bool`  | `True`  |
| `save_empty_changes`  | `True`: if empty changes will be registered <br> `False`:  if will not  | `bool`  | `True`  |

## Authors

[@omelched](https://github.com/omelched) _(Denis Omelchenko)_

### Contributors

<img width=20% src="https://64.media.tumblr.com/7b59c6105c40d611aafac4539500fee1/tumblr_njiv6sUfgO1tvqkkro1_640.gifv" title="tumbleweed"/>

## Changelist

**ognajD** version history and changelist available at [releases](https://github.com/omelched/django-ognajd/releases) page.

## License

This project is licensed under the **GNU APGLv3** License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Inspiration, code snippets, etc.
* polls showcase app code from [sample-django](https://github.com/digitalocean/sample-django)
* index incrementer at model save from [`tinfoilboy`](https://stackoverflow.com/a/41230517)
