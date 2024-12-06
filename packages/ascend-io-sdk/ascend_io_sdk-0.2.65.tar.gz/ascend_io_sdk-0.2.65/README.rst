.. raw::html
    <hidden>test</hidde>

==============================
The Ascend.io Python SDK
==============================

This package contains the `Ascend Python SDK <https://developer.ascend.io/docs/python-sdk>`_. This SDK is used to script the management of the
`Ascend.io <https://www.ascend.io>`_ Data Automation Platform. The SDK can be used to create your own customizations of the
platform configuration, integrate with   CI/CD or other tools, as well as fully automate your environment.

* **Automation.** Integrate Ascend with any combination of workflow and/or CI/CD tools your organization uses on a daily basis.
* **Transparency.** Ascend deploys within your Cloud tenant (GCP, AWS, Azure) so you can see everything the platform is doing.
* **Control.** Manage your Ascend Platform, build dataflows, extract metadata, and more in a completely programmatic way

---------------
Get Started
---------------
You will need access to an Ascend.io installation. Developers can `sign up for a free trial <https://www.ascend.io/signup/>`_.
If you are already an Ascend customer, have your administrator add you to the platform.

Once you have access to the Platform, `create your developer API Access Keys <https://developer.ascend.io/docs/developer-keys>`_
and `configure your local authentication file <https://developer.ascend.io/docs/python-sdk#authorization>`_. Remember to change
the word *trial* in your local authentication file to the name of your Ascend.io instance.


Install the python library using `pip <https://pip.pypa.io/en/latest/>`_::

    $ pip3 install ascend-io-sdk

Start writing your automations with the `Python Client <https://developer.ascend.io/docs/python-sdk-client-ref>`_.

------------------
Run the Examples
------------------
If running some sample code works for you, try out the Ascend Python SDK by listing the dataflows
within your Ascend instance::

    from ascend.sdk.client import Client
    from tabulate import tabulate

    hostname = 'my-host-name'
    client = Client(hostname)
    services = []
    for ds in client.list_data_services().data:
        services.append([ds.id, ds.name, ds.created_at, ds.updated_at])

    print(tabulate(sorted(services, key=lambda x: x[1]), headers=["id", "name", "created at"]))

We release updates to the SDK all the time. If some features are missing, you get stuck, or you find
something that you don't think is right, please let us know. We're here to make the developer experience
as easy and enjoyable as possible. We know that fabulous Developer Relations is key!

---------------
Read the Docs
---------------
* `Ascend.io Python SDK Documentation <https://developer.ascend.io/docs/python-sdk>`_
* `Ascend Developer Hub <https://developer.ascend.io>`_
* `Ascend.io <https://www.ascend.io>`_

