[![PyPi](https://img.shields.io/pypi/v/SecuriPy)](https://pypi.org/project/SecuriPy/)
# SecuriPy

SecuriPy is a Python library that provides a set of functions for encrypting and decrypting human-readable file formats into undefined non-readable files. It offers a simple yet powerful way to protect sensitive information from unauthorized access.

## Installation

To use SecuriPy, you will need Python 3.x installed on your system. You can install SecuriPy using pip, the Python package installer, by executing the following command:

```shell
pip install SecuriPy
```

## Usage

Import the `SecuriPy` module in your Python script to access the functions:

```python
from SecuriPy import Text, Image, File
```
OR
```python
from SecuriPy import *

## Security Considerations

- Use a strong and unique `secret_key` for each encryption operation to enhance security. Avoid using easily guessable or common phrases.
- Always encrypt sensitive information before storing or transmitting it. SecuriPy is a tool for obfuscating the data but does not provide additional security measures for data storage or transmission.

## Contributing

Contributions to SecuriPy are welcome! If you find any issues or have suggestions for improvement, please create a GitHub issue or submit a pull request.

## License

SecuriPy is released under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](https://github.com/Anupam1707/SecuriPy/blob/main/LICENSE) file for more details.

## Contact

If you have any questions, suggestions, or feedback, you can reach out to the project maintainers at [programmer.tiak@gmail.com](mailto:programmer.tiak@gmail.com).

Happy encrypting with SecuriPy!