import importlib

# List of modules to import symbols from for each product
modules_to_import = ['models', 'api']
apps = ['pickey', 'kiwi', 'kopi', 'lumina']
# Initialize the __all__ variable

__all__ = []

# Dynamically import all symbols from the specified modules
for app in apps:
  for module_name in modules_to_import:
    #print(f'Module: {__name__}.{app}.{module_name}')
    #rint(f'Package: {__name__}')
    module = importlib.import_module(f'{__name__}.{app}.{module_name}', package=f'{__name__}')
    for symbol in dir(module):
      if not symbol.startswith('_'):
        #print(symbol)
        globals()[symbol] = getattr(module, symbol)
        __all__.append(symbol)