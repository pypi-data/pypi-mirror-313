========
tomlhold
========

Overview
--------

A dict-like holder for TOML data.

Installation
------------

To install tomlhold, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install tomlhold

Example
-------

Here's a simple example.

.. code-block:: python

    import tomlhold

    # Example 1: Create Holder from a TOML string
    toml_data = """
    [database]
    server = "192.168.1.1"
    ports = [ 8001, 8001, 8002 ]
    connection_max = 5000
    enabled = true
    """
    h = tomlhold.Holder(toml_data)

    # Access a single value
    print(h["database", "server"])

    # Example 2: Access nested values using multiple indices
    print(h["database", "ports", 2])

    # Example 3: Update a value
    h["database", "connection_max"] = 10000
    print(h["database", "connection_max"])

    # Example 4: Add a new section and key-value pair
    h["new_section", "new_key"] = "New Value"
    print(h["new_section", "new_key"])

    # Example 5: TOML compatibility enforcement (invalid TOML raises an error)
    try:
        h["new_section", "invalid_key"] = {"invalid": object()}
    except Exception as e:
        print(f"Error: {e}")  # Ensures only TOML-compatible data is allowed

    # Example 6: Create Holder from a dictionary and convert it to TOML format
    data_dict = {
        "title": "Example",
        "owner": {
            "name": "John Doe",
            "dob": "1979-05-27T07:32:00Z"
        }
    }
    h = tomlhold.Holder.fromdict(data_dict)
    print(h)

    # Example 7: Iterate through Holder object like a regular dictionary
    for section, values in h.items():
        print(section, values)

    # Output:
        # 192.168.1.1
        # 8002
        # 10000
        # New Value
        # Error: type <class 'object'> is not allowed
        # title = "Example"
        #
        # [owner]
        # name = "John Doe"
        # dob = "1979-05-27T07:32:00Z"
        #
        # title Example
        # owner {'name': 'John Doe', 'dob': '1979-05-27T07:32:00Z'}

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/tomlhold>`_
* `Download <https://pypi.org/project/tomlhold/#files>`_
* `Source <https://github.com/johannes-programming/tomlhold>`_

Credits
-------

* Author: Johannes
* Email: johannes-programming@mailfence.com

Thank you for using ``tomlhold``!