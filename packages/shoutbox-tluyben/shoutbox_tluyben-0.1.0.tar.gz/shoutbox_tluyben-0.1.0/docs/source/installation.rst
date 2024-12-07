Installation Guide
=================

This guide covers the installation and setup of the Shoutbox Python library.

Requirements
-----------

- Python 3.7 or higher
- pip package manager
- A Shoutbox API key

Basic Installation
----------------

Install using pip:

.. code-block:: bash

    pip install shoutbox

Development Installation
---------------------

For development or contributing:

1. Clone the repository:

.. code-block:: bash

    git clone https://github.com/shoutboxnet/shoutbox-python.git
    cd shoutbox-python

2. Install development dependencies:

.. code-block:: bash

    pip install -r requirements-dev.txt

3. Install the package in editable mode:

.. code-block:: bash

    pip install -e .

Configuration
------------

API Key Setup
~~~~~~~~~~~

The library needs your Shoutbox API key to function. You can provide it in several ways:

1. Environment Variable:

.. code-block:: bash

    export SHOUTBOX_API_KEY=your-api-key-here

2. Direct initialization:

.. code-block:: python

    from shoutbox import ShoutboxClient

    client = ShoutboxClient(api_key='your-api-key-here')

3. Using a .env file:

Create a .env file in your project root:

.. code-block:: bash

    SHOUTBOX_API_KEY=your-api-key-here
    SHOUTBOX_FROM=default-sender@yourdomain.com
    SHOUTBOX_TO=default-recipient@example.com

Then use python-dotenv to load it:

.. code-block:: python

    from dotenv import load_dotenv
    load_dotenv()

Framework Integration
------------------

Flask
~~~~~

1. Install Flask:

.. code-block:: bash

    pip install flask

2. Basic setup:

.. code-block:: python

    from flask import Flask
    from shoutbox import ShoutboxClient

    app = Flask(__name__)
    client = ShoutboxClient()

Django
~~~~~~

1. Install Django:

.. code-block:: bash

    pip install django

2. Add to settings.py:

.. code-block:: python

    SHOUTBOX_API_KEY = 'your-api-key-here'

Verification
----------

To verify your installation:

.. code-block:: python

    from shoutbox import ShoutboxClient, Email

    client = ShoutboxClient()

    email = Email(
        from_email="sender@example.com",
        to="recipient@example.com",
        subject="Test Email",
        html="<h1>Installation Test</h1>"
    )

    try:
        response = client.send(email)
        print("Installation successful!")
    except Exception as e:
        print(f"Installation verification failed: {e}")

Development Tools
--------------

For development, several additional tools are available:

Testing
~~~~~~~

Run the test suite:

.. code-block:: bash

    make test

Code Style
~~~~~~~~~

Check code style:

.. code-block:: bash

    make cs

Fix code style issues:

.. code-block:: bash

    make cs-fix

Documentation
~~~~~~~~~~~

Build documentation:

.. code-block:: bash

    cd docs
    make html

Troubleshooting
-------------

Common Issues
~~~~~~~~~~~

1. **ImportError: No module named 'shoutbox'**
   
   - Verify the installation:
     .. code-block:: bash
         pip list | grep shoutbox

2. **ValueError: API key must be provided**
   
   - Check your environment variables
   - Verify API key in code

3. **SSL Certificate Verification Failed**
   
   - Update your CA certificates
   - Check SSL settings in client initialization

Getting Help
~~~~~~~~~~

If you encounter issues:

1. Check the documentation
2. Search GitHub issues
3. Create a new issue
4. Contact support

For critical issues, email support directly.
