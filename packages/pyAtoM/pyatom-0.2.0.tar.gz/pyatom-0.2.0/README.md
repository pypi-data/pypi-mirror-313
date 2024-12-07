# pyAtoM

Python Library for the AtoM Archival Description Platform API

This library provides a Python class for working with the AtoM Archival Description Rest API

https://accesstomemory.org/en/docs/2.8/dev-manual/api/api-intro/

The Library provides APIs for the following:

* Get a record by its Slug
* Get a record by its identifier
* Search for records
* Download a digital object attached to a record


## License

The package is available as open source under the terms of the Apache License 2.0


## Installation

pyAtoM is available from the Python Package Index (PyPI)

https://pypi.org/project/pyAtoM/

To install pyAtoM, simply run this simple command in your terminal of choice:


    $ pip install pyAtoM


## Examples

Finding records by Slug


    from pyAtoM import *

    client = AccessToMemory(username="demo@example.com", password="demo", server="demo.accesstomemory.org")

    slug: str = "my-slug"

    item: dict = client.get(slug)


Searching for Records


    from pyAtoM import *

    client = AccessToMemory(username="demo@example.com", password="demo", server="demo.accesstomemory.org")

    queries: list = []

    queries.append(Query(query_value="horses", query_field=QueryField.title))
    queries.append(Query(query_value='Sudbury', query_operator=QueryOperator.or_terms, query_field=QueryField.all))

    for result in client.search(query_terms=queries):
        print(result)


