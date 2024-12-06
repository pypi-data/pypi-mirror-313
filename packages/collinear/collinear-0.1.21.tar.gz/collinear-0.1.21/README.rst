Collinear AI Python SDK
======================

This is a simple python package, providing access to Collinear AI API's


.. code-block:: python

    from collinear import Collinear
    from collinear.judge.types import ConversationMessage
    c = Collinear(access_token='YOUR_API_KEY')

    pointwise_response = await c.judge.collinear_guard.pointwise(
    [ConversationMessage(role='user',content='How are you')]
    ,{'role':'assistant','content':'I am good how are you?'})

    classification_response = await c.judge.collinear_guard.classification('response',
    [ConversationMessage(role='user',content='How are you')],
    {'role':'assistant','content':'I am good how are you?'})





You should list packages that your package uses in the `requirements.txt` file.
Listing your package depencencies ensures that these packages are also installed when someone installs your package.
Explicitly stating versions of dependencies can increase the reproducibility in the function of your package that might depend on particular versions of other packages.

Python package dependencies can indicate minimum package versions (``>=``) or the exact version number (``==``) that is required.

.. code-block:: txt

    pandas==1.0.0
    numpy>=1.18.4


License
-------

It's important to let users and developers know under what circumstance they can use, modify and redistribute your code.

The ``LICENSE`` file associated with your package should contain the text for the packages license.
The example in this package is for the MIT license.


Versioning
----------

A version number is essential for releasing your package.
`Semantic versioning <https://semver.org/>`_ is a useful method for informative versioning.

It can be useful to store this in a separate file, so that it can be referenced from multiple places (e.g. ``setup.py`` and the main documentation).

`Git tagging <https://drive.google.com/drive/folders/1CJj28JmAOG5IQY_DzQDtFVosg60VpjNs?usp=sharing>`_ can be used to mark significant points in your projects development.
These tags can also be used to trigger version releases, for example using `GitHub Actions <https://github.com/marketplace/actions/tag-release-on-push-action>`_.

Including Other Files
---------------------

You may want to include example data or other non-python files in your package.
Be aware that the documentation for including non-python files is `notoriously bad <https://stackoverflow.com/a/14159430/8103477>`_, as most methods have been depreciated.

To include data in your source and binary distributions:

* In the ``setup.py`` file ``setup(...)`` function call, include ``include_package_data = True``.
* Alongside your `setup.py` file, provide a `MANIFEST.in` file.

The ``MANIFEST.in`` file should list any non-python files that you wish to include distributions.

A ``MANIFEST.in`` file includes single files, or all files of a type, as below:

.. code-block:: txt

    include README.rst
    recursive-include examplepackage/examples *.csv


Distributing
------------

Storing your source code in an open repository allows others to view and critique your code. Python code can be distributed in a number of formats, as described by this `overview of python packages <https://packaging.python.org/overview/>`_.

To allow others to install and use your code more easily, consider uploading your package to the Python Package Index (PyPI).
PyPI is an online repository of python packages and is the default repository used by ``pip``.

Please see this `guide to packaging projects <https://packaging.python.org/tutorials/packaging-projects/>`_ for instructions on uploading your package to PyPI.
