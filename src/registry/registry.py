import sys
import os
import inspect

# Handle imports for both direct execution and module import
try:
    # Try relative imports first (when imported as a module)
    from .. import converters
    from ..converters.converter_interface import ConverterInterface
except ImportError:
    # Fall back to absolute imports (when run directly or from main.py)
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    import converters
    from converters.converter_interface import ConverterInterface


class ConverterRegistry:
    """
    Registry for managing available converters.
    Automatically discovers and registers all converter classes.
    """
    def __init__(self):
        self.converters = {}
        self.format_map = {}  # Maps file format -> list of converter classes
        self._auto_register()
    
    def _auto_register(self):
        """
        Automatically discover and register all converter classes from the converters module.
        """
        # Get all classes from the converters module
        for name, obj in inspect.getmembers(converters, inspect.isclass):
            # Check if it's a subclass of ConverterInterface (but not the interface itself)
            if issubclass(obj, ConverterInterface) and obj is not ConverterInterface:
                self.register_converter(obj)
    
    def register_converter(self, converter_class):
        """
        Register a converter class in the registry.
        
        Args:
            converter_class: The converter class to register
        """
        self.converters[converter_class.__name__] = converter_class
        
        # Map supported formats to this converter
        if hasattr(converter_class, 'supported_formats'):
            for fmt in converter_class.supported_formats:
                if fmt not in self.format_map:
                    self.format_map[fmt] = []
                self.format_map[fmt].append(converter_class)
    
    def get_converter(self, name):
        """
        Retrieve a converter class by name.
        
        Args:
            name: The name of the converter class to retrieve
        
        Returns:
            The converter class if found, else None
        """
        return self.converters.get(name, None)
    
    def get_converters_for_format(self, format_type):
        """
        Get all converters that support a specific file format.
        
        Args:
            format_type: File format (e.g., 'mp4', 'jpg', 'csv')
        
        Returns:
            List of converter classes that support this format
        """
        return self.format_map.get(format_type.lower(), [])
    
    def get_converter_for_conversion(self, input_format, output_format):
        """
        Find the appropriate converter for a specific conversion.
        
        Args:
            input_format: Input file format
            output_format: Output file format
        
        Returns:
            Converter class that supports both formats, or None
        """
        input_converters = set(self.get_converters_for_format(input_format))
        output_converters = set(self.get_converters_for_format(output_format))
        
        # Find converters that support both formats
        compatible = input_converters & output_converters
        
        return compatible.pop() if compatible else None
    
    def list_converters(self):
        """
        List all registered converters with their supported formats.
        
        Returns:
            Dictionary mapping converter names to their supported formats
        """
        result = {}
        for name, converter_class in self.converters.items():
            if hasattr(converter_class, 'supported_formats'):
                result[name] = list(converter_class.supported_formats)
            else:
                result[name] = []
        return result
    

if __name__ == "__main__":
    print("Initializing converter registry...")
    registry = ConverterRegistry()
    
    print(f"\nRegistered {len(registry.converters)} converters:")
    for name in registry.converters.keys():
        print(f"  - {name}")
    
    print("\nSupported formats by converter:")
    for name, formats in registry.list_converters().items():
        print(f"  {name}: {', '.join(sorted(formats))}")
    
    print("\nFormat mapping (format -> converters):")
    for fmt in sorted(registry.format_map.keys()):
        converter_names = [c.__name__ for c in registry.format_map[fmt]]
        print(f"  {fmt}: {', '.join(converter_names)}")
    
    print("\nExample: Finding converter for mp4 -> gif...")
    converter = registry.get_converter_for_conversion('mp4', 'gif')
    if converter:
        print(f"  Found: {converter.__name__}")
    else:
        print("  No suitable converter found")
    
    print("\nExample: Finding converter for gif -> png...")
    converter = registry.get_converter_for_conversion('gif', 'png')
    if converter:
        print(f"  Found: {converter.__name__}")
    else:
        print("  No suitable converter found")
