# Installation

`pipx` is recommended.

```
pipx install git+https://github.com/hliao2/elfextract
```

or

```
pip install git+https://github.com/hliao2/elfextract
```

# Usage

## Extract all functions

```
elfextract <file>
```

## Extract specified functions

```
elfextract -f <funcs> <file>
```

where `<funcs>` is a list of functions separated by comma.
