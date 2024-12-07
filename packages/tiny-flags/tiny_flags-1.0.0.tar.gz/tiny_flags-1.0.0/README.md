# tiny_flags

A lightweight Python package for efficient settings management and manipulation. Easily handle language preferences, settings, and other flag-based configurations using minimal memory.

### Features

* 32-bit and 64-bit bitfield support (reserve one 32/64 bit integer)
* Automatic bit position management
* Boolean flags and multi-option settings
* Ordered dictionary configuration for easy use
* Memory efficient
* Perfect for storing app settings where complex queries are not required


## Installation

Install using `pip`:

```bash
pip install tiny_flags
```

### How to use?

Requires `OrderedDict`

```
from collections import OrderedDict
from tiny_flags import TinyFlags
```

## Define your settings

```
fields = OrderedDict([
    ('language', ['english', 'spanish', 'french']),  # Uses 2 bits, might make sense to add even number and mark the last as '_option'
    ('dark_mode', False),                            # Uses 1 bit, initial value
    ('notifications', True)                          # Uses 1 bit, initial value
])
```

You can easily create your settings structure by looking at the below example. One should think ahead before implementing the structure of the ordered dictionary and it might make sense to reserve some extra for the list options for later use.
NOTE!: The order matters and changing it later can create some issues in migrating to a new structure. Think ahead in what you need, don't remove rather just add. If you don't need an option then perhaps leave it and rename with _ prefix, and just ignore it.
Boolean flags are easy, it is just True or False, but the list options take up the same space whether odd or even number of items given. It might make sense for you to add the last option in such list and use _ prefix as for deprecated options mentioned above.
Booleans use 1 bit position, and option list uses 1 bit position for every 2 items (even with 1 item 1 bit position is reserved, so be careful about odd numbers)

## Initialize manager

```
manager = TinyFlags(fields)
```

Default value is 32bit, but give True for 64bit, `TinyFlags(fields, True)`. Check that your environment supports 64bit integers before trying to use them.

## Set values

```
manager.set_value('language', 'spanish')
```
For options lists just select the category first followed by the option you wish to set.

```
manager.set_value('dark_mode', True)
```
For boolean flags, just use the key and give `True/False` to enable/disable.

## Get values

```
print(manager.get_value('language'))       # 'spanish'
print(manager.get_value('dark_mode'))      # True
print(manager.get_value('notifications'))  # True
```

## Some details and thoughts on using tiny_flags

When using a database there are of course drawbacks on using a bitfield for settings for example if you need complex queries on the bits then put them in their own columns.
If you need to do complex queries on the settings, for those kinds of settings it is not the best solution.
Indexing will index the full integer not the individual bits.
Changing settings later might be cumbersome, but if popularity picks up I can add a migration tool or if you have pioneering spirit please contribute.

## Testing and development

Setup Development Environment & clone the repository
```
git clone https://github.com/FistOfTheNorthStar/tiny_flags
cd tiny_flags
```
Install `pip install -e .`
Running Tests `pytest tests/`

There is also a `dev_lint.sh` script lints and installs the development version. Check it out if you are interested.

Contributions are welcome.

## License
Distributed under the MIT License. See LICENSE for more information.

## Todo for the future
Add more option mappings possibilities
See if 32/64bit values should have a forced type
Test with actual DB (MongoDB 32/64 bit ints)
