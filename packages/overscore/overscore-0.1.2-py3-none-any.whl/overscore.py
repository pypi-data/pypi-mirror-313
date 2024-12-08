"""
description: |
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
"""

# pylint: disable=too-many-branches

import re

NUMBER = re.compile(r"^\d+$")   # regex matching a number

WORD = re.compile(r"^(\w|\-)+$")     # regex matching a word

class OverscoreError(Exception):
    """
    description: Used for any overscore issues encountered.
    document: 40
    """

def parse(
    text:str    # path to parse
)->list:
    """
    description: Parses text to a list of keys/indexes
    usage: |
        ::

            import overscore

            overscore.parse("a-b__0___1____2_____3")
            # [
            #     "a-b",
            #     0,
            #     -1,
            #     "2",
            #     "-3"
            # ]
    document: 20
    """

    count = 0
    place = []
    places = []

    state = "place"

    for letter in text:

        if state == "place":

            place.append(letter)

            if letter != '_':
                state = "placing"

        elif state == "placing":

            if letter == '_':
                count += 1
            else:
                count = 0

            if count == 2 and letter == '_':
                places.append(''.join(place[:-1]))
                place = []
                count = 0
                state = "place"
            else:
                place.append(letter)

    if place:
        places.append(''.join(place))

    path = []

    for place in places:
        if '0' <= place[0] and place[0] <= '9':
            path.append(int(place))
        elif place[:1] == '_' and '0' <= place[1] and place[1] <= '9':
            path.append(-int(place[1:]))
        elif place[:2] == '__' and '0' <= place[2] and place[2] <= '9':
            path.append(place[2:])
        elif place[:3] == '___' and '0' <= place[3] and place[3] <= '9':
            path.append(str(-int(place[3:])))
        else:
            path.append(place)

    return path


def compile(
    path:list   # The path to compile
)->str:
    """
    description: Compiles a list of keys/indexes to text
    usage: |
        ::

            import overscore

            overscore.compile(["a-b", 0, -1, "2", "-3"])
            # "a-b__0___1____2_____3"
    document: 30
    """

    places = []

    for place in path:

        if isinstance(place, int) and place > -1:

            places.append(str(place))

        elif isinstance(place, int) and place < 0:

            places.append(f"_{abs(place)}")

        elif isinstance(place, str) and len(place) and place[0] == "-" and NUMBER.match(place[1:]):

            places.append(f"___{place[1:]}")

        elif isinstance(place, str) and NUMBER.match(place):

            places.append(f"__{place}")

        elif isinstance(place, str) and WORD.match(place):

            places.append(place)

        else:

            raise OverscoreError(f"cannot compile {place}")

    return "__".join(places)



def has(
    data,   # The multidimensional data
    path    # The double underscored path to the intended value
)->bool:
    """
    description: Indicates whether path exists in data
    parameters:
        data:
            type:
            - dict
            - list
            - str
        path:
            type:
            - list
            - str
    returns: Whether path exists in data
    document: 0
    usage: |
        You can check via a string::

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

            overscore.has(data, "things__a__b__0____1")
            # True

        Or using via a list::

            overscore.has(data, ["things", "a", "b", 0, "1"])
            # True
    """

    if isinstance(path, str):
        path = parse(path)

    for place in path:
        if isinstance(place, int):
            if (
                (not isinstance(data, list)) or
                (place >= 0 and len(data) < place + 1) or
                (place < 0 and len(data) < abs(place))
            ):
                return False
        else:
            if (
                (not isinstance(data, dict)) or
                (place not in data)
            ):
                return False
        data = data[place]

    return True


def get(
    data,   # The multidimensional data
    path    # The double underscored path to the intended value
):
    """
    description: Retrieves the value in multidimensional data at the double underscored path
    parameters:
        data:
            type:
            - dict
            - list
            - str
        path:
            type:
            - list
            - str
    returns: The value in data at path or None if not found
    document: 5
    usage: |
        You can retrieve via a string::

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

        Or using via a list::

            overscore.get(data, ["things", "a", "b", 0, "1"])
            # "yep"
    """

    if isinstance(path, str):
        path = parse(path)

    for place in path:
        if isinstance(place, int):
            if (
                (not isinstance(data, list)) or
                (place >= 0 and len(data) < place + 1) or
                (place < 0 and len(data) < abs(place))
            ):
                return None
        else:
            if (
                (not isinstance(data, dict)) or
                (place not in data)
            ):
                return None
        data = data[place]

    return data


def set(
    data,   # The multidimensional data
    path,   # The double underscored path to the intended value
    value   # The value to store
):
    """
    description: |
        Stores a value in multidimensional data at the double underscored path, creating necessary structures along the way
    parameters:
        data:
            type:
            - dict
            - list
            - str
        path:
            type:
            - list
            - str
    document: 10
    usage: |
        You can store via a string::

            import overscore

            data = {}

            overscore.set(data, "things__a__b___2____1", "yep")
            data
            # {
            #     "things": {
            #         "a": {
            #             "b": [
            #                 {
            #                     "1": "yep"
            #                 },
            #                 None
            #             ]
            #         }
            #     }
            # }

        Or using via a list::

            overscore.set(data, ["things", "a", "b", -2, "1"], "sure")
            data
            # {
            #     "things": {
            #         "a": {
            #             "b": [
            #                 {
            #                     "1": "sure"
            #                 },
            #                 None
            #             ]
            #         }
            #     }
            # }
    """

    if isinstance(path, str):
        path = parse(path)

    for index, place in enumerate(path):

        if index < len(path) - 1:
            default = {} if isinstance(path[index+1], str) else []
        else:
            default = value

        if isinstance(data, dict):

            if isinstance(place, int):
                raise OverscoreError(f"index {place} invalid for dict {data}")

            if place not in data:
                data[place] = default

        else:

            if isinstance(place, str):
                raise OverscoreError(f"key {place} invalid for list {data}")

            while (
                (place >= 0 and len(data) < place + 1) or
                (place < 0 and len(data) < abs(place))
            ):
                data.append(None)

            if data[place] is None:
                data[place] = default

        if index < len(path) - 1:
            data = data[place]
        elif data[place] != value:
            data[place] = value
