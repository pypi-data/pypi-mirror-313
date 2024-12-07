from rangy import Converter, ConverterRegistry
from datetime import date

# Create converters for built-in types

class DateConverter(Converter):
    def __init__(self):
        super().__init__(int, self.to_number, self.to_string)

    def to_string(self, d):
        if isinstance(d, date):
            return d.isoformat()
        else:
            raise TypeError("Not a date")


    def to_number(self,  d):
        if isinstance(d, date):
            return d.toordinal()
        else:
            raise TypeError("Not a date")

def register_builtins():
    date_converter = DateConverter()
    int_converter = Converter(int)
    float_converter = Converter(float)

    # Register DateConverter *first*!
    ConverterRegistry.register(date_converter)  # Changed order
    ConverterRegistry.register(float_converter)
    ConverterRegistry.register(int_converter) # Changed order
    converters = [date_converter,int_converter, float_converter]
    for converter in converters:
        try:
            ConverterRegistry.get(converter._type)
        except KeyError:
            ConverterRegistry.register(converter)

register_builtins()