# Vite Registry Python

A free Python module to help you control your Windows registry

## Use Cases

- CRUD your registry

## Features

- Easy to control your registry with a few lines of coding

## Requirements

- **Python**: 2.x or 3.x or higher

## Quick Start

If you prefer to install this package into your own Python project, please follow the installation steps below

## Installation

#### Require the current package using pip:

```bash
pip install viteregistry
```

## Testing

``` python
from ViteRegistry import *

result = read_registry('HKEY_LOCAL_MACHINE', "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\DefaultProductKey", "ProductId")
print('Product ID: ', )
```

## Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) for details.

### Security

If you discover any security related issues, please email contact@adminvitelicense.io or use the issue tracker.

## Credits

- [Funny Dev., JSC](https://github.com/funnydevjsc)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
