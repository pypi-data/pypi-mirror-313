overscore
=========

Library for double underscore access notation

Overscore provides a way to retrieve (and store) multi-dimensional data using a single string
with double underscores.

Inspired by Django, the access string can be used as a routine argument or a URL parameter,
allowing for complex access within simple contexts::

    import overscore

    data = {
        "things": {
            "a": {
                "b": [
                    {
                        "1": "yep"
                    }
                ]
            }
        }
    }

    overscore.get(data, "things__a__b__0____1")
    # "yep"

All keys/indexes are separated by double underscores. Extra underscores dictate how to
parse that place in the path.

.. list-table:: Underscores and Behavior
    :header-rows: 1

    * - Underscores
      - Following
      - Meaning
      - Example
      - Equivalent
    * - 2
      - letters and numbers
      - key
      - a__b
      - ["a"]["b"]
    * - 2
      - numbers
      - index
      - a__1
      - ["a"][1]
    * - 3
      - numbers
      - negative index
      - a___2
      - ["a"][-2]
    * - 4
      - numbers
      - numerical key
      - a____3
      - ["a"]["3"]
    * - 5
      - numbers
      - neagtive numerical key
      - a_____4
      - ["a"]["-4"]
