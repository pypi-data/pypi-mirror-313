|pypi| |actions| |coverage|

edc-form-describer
------------------

Describe edc forms in markdown.

Generate a document describing the forms in an EDC module annotated with field names, table
names, choices, etc.

For example::

    >>> python manage.py make_forms_reference \
        --app_label effect_subject \
        --admin_site effect_subject_admin
        --visit_schedule visit_schedule


.. |pypi| image:: https://img.shields.io/pypi/v/edc-form-describer.svg
    :target: https://pypi.python.org/pypi/edc-form-describer

.. |actions| image:: https://github.com/clinicedc/edc-form-describer/actions/workflows/build.yml/badge.svg
  :target: https://github.com/clinicedc/edc-form-describer/actions/workflows/build.yml

.. |coverage| image:: https://coveralls.io/repos/github/clinicedc/edc-form-describer/badge.svg?branch=develop
    :target: https://coveralls.io/github/clinicedc/edc-form-describer?branch=develop
