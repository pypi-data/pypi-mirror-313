from collections import OrderedDict
from typing import Any, List, Union

from .bitfield import BitField


class TinyFlags:
    def __init__(self, fields: OrderedDict[str, Union[bool, List[Any], Any]], bits64: bool = False):
        self.fields = fields
        self.bitfield = BitField(bits64)
        self.bit_positions = {}
        self.bit_widths = {}
        self.option_mappings = {}
        self.current_position = 0
        if fields is not None:
            self.setup_fields()

    def setup_fields(self):
        """
        OrderedDict sets the positions.
        Flags/Options can be:
        - True/False
        - List of options, position = index
        """
        for field_name, options in self.fields.items():
            if isinstance(options, bool):
                # Boolean uses 1 bit
                self.bit_positions[field_name] = self.current_position
                self.bit_widths[field_name] = 1
                self.bitfield.set_bit(self.current_position, 1 if options else 0)
                self.current_position += 1
            elif isinstance(options, list):
                # List of options, need enough bits to store largest index, if odd number 1 is left over
                bit_width = (len(options) - 1).bit_length()
                self.bit_positions[field_name] = self.current_position
                self.bit_widths[field_name] = bit_width
                self.option_mappings[field_name] = {opt: idx for idx, opt in enumerate(options)}
                self.bitfield.set_bits(self.current_position, bit_width, 0)
                self.current_position += bit_width
            else:
                raise ValueError(f"Field {field_name} must be boolean or list of options")

    def set_value(self, field_name: str, value: Union[bool, Any]):
        if field_name not in self.bit_positions:
            raise ValueError(f"Unknown field: {field_name}")

        position = self.bit_positions[field_name]
        width = self.bit_widths[field_name]

        if width == 1:  # Boolean field
            self.bitfield.set_bit(position, 1 if value else 0)
        else:  # Option field
            if value not in self.option_mappings[field_name]:
                raise ValueError(f"Invalid value for {field_name}: {value}")
            option_value = self.option_mappings[field_name][value]
            self.bitfield.set_bits(position, width, option_value)

    def get_value(self, field_name: str) -> Union[bool, Any]:
        if field_name not in self.bit_positions:
            raise ValueError(f"Unknown field: {field_name}")

        position = self.bit_positions[field_name]
        width = self.bit_widths[field_name]

        if width == 1:  # Boolean field
            return bool(self.bitfield.get_bit(position))
        else:  # Option field
            value = self.bitfield.get_bits(position, width)
            # Reverse lookup in option_mappings
            for opt, idx in self.option_mappings[field_name].items():
                if idx == value:
                    return opt
            return None
