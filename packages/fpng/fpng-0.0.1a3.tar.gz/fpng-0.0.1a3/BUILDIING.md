# Building

Note: The build method may vary depending on the version. When building previous versions, please refer to the BUILDING.md with that version.


## Preparation
```sh
# Upgrade PIP
python -m pip install --upgrade pip

# Clone code including submodule
git clone --recurse-submodules https://github.com/dofuuz/py-fpng-nb.git

cd py-fpng-nb
```


## Build package(wheel)
```sh
pip wheel -v .
```


## Install
Install built .whl package(not .tar.gz sdist).
```sh
pip install ./fpng-[...].whl
```


## Test
```sh
# Install dependencies
pip install pytest

# Test (using installed py-fpng-nb)
python -m pytest tests/
```
