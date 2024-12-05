# dyn_import_utils

`dyn_import_utils` is a Python utility for dynamically importing modules and packages from file paths. 
It simplifies importing code that resides outside the standard Python module search path.

---

## Features

- Dynamically import Python modules from arbitrary file paths.
- Load entire packages from directories containing `__init__.py`.
- Lightweight and easy to integrate into existing projects.
- The input path can be absolute or relative,
   in case of a relative path, the base path of the calling module is used

---

## Installation

Install `dyn_import_utils` via pip:

```bash
pip install dyn_import_utils
```

---

## Usage

### Lib import
```python
import dyn_import_utils
```

### Importing a Module
Use `import_module` to load a module dynamically from its file path:

```python
# Dynamically load a module
module = dyn_import_utils.import_module("path/to/module.py")

# Use the module
print(module.some_function())
```

### Importing a Package
Use `import_package` to load a package dynamically from its directory:

```python
# Dynamically load a package
package = dyn_import_utils.import_package("path/to/package")

# Use the package
print(package.some_function())
```

### Adding a Directory to `sys.path`
Temporarily add a directory to the Python module search path:

```python
dyn_import_utils.add_sys_path("path/to/directory")
```

---

## Example

### Example Module: `hello.py`

```python
# hello.py
def greet():
    return "Hello, world!"
```

### Dynamically Loading the Module

```python
import dyn_import_utils

module = dyn_import_utils.import_module("hello.py")
print(module.greet())  # Output: Hello, world!
```

---

## License

`dyn_import_utils` is released under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Links

- **PyPI**: [https://pypi.org/project/dyn_import_utils/](https://pypi.org/project/dyn_import_utils/)  


