# Advanced Python Utilities Module

This module provides a comprehensive set of utilities for advanced Python programming, including HTTP communication, string handling, logging enhancements, introspection, dynamic importing, property descriptors, data class extensions, and serialization. It is designed to facilitate complex application development by offering robust tools that extend Python's standard capabilities.

## Table of Contents

- [HTTP Communication Utilities](#http-communication-utilities)
- [String Handling Enhancements](#string-handling-enhancements)
- [Advanced Logging System](#advanced-logging-system)
- [Introspection and Reflection Utilities](#introspection-and-reflection-utilities)
- [Dynamic Importing Tools](#dynamic-importing-tools)
- [Advanced Property Descriptors](#advanced-property-descriptors)
- [Data Class Extensions and Configuration Handling](#data-class-extensions-and-configuration-handling)
- [Serialization and Deserialization Utilities](#serialization-and-deserialization-utilities)

## HTTP Communication Utilities

### Overview

This component provides a robust toolkit for handling HTTP communication. It includes advanced features for error handling, response parsing, cookie management, and URL processing. The utilities streamline building HTTP clients and services by abstracting common patterns and offering flexible, extensible components.

### Key Features

- **HTTPException Hierarchy**: A comprehensive set of exception classes for handling HTTP errors, based on status codes and error types.
- **Response Handling**: Utilities for parsing and processing HTTP responses, including automatic JSON decoding and error checking.
- **Cookie Management**: Tools for managing HTTP cookies, including parsing and formatting.
- **URL Processing**: Classes and functions for manipulating URLs, including query parameters and path components.
- **Serialization Decorators**: Decorators to facilitate serialization and deserialization of complex objects within the HTTP context.
- **Namespace Augmentation**: Enhancements to the HTTP namespace for convenient access to common utilities like `HTTP.URL`, `HTTP.Agent`, and `HTTP.Exception`.

## String Handling Enhancements

### Overview

Provides advanced string handling utilities focused on character encoding detection, conversion, and manipulation. It defines the `Str` class, acting as a wrapper around string or bytes objects, offering methods to handle various encoding scenarios and to facilitate text processing.

### Key Features

- **Encoding and Decoding**: Convert between bytes and string representations, handling different character encodings.
- **Charset Detection**: Automatically detects the character encoding of input data using custom logic and libraries.
- **Lazy Proxying**: Proxies common string methods to the underlying string representation, allowing `Str` instances to behave like regular strings.
- **Tokenization**: Methods to split strings into tokens based on regular expression patterns.

## Advanced Logging System

### Overview

Enhances the standard Python logging system by introducing custom log levels, additional logging utilities, and a more flexible logger configuration. It provides advanced logging capabilities suitable for complex applications that require detailed logging and traceability.

### Key Features

- **Custom Log Levels**: Defines additional log levels like `NOTICE`, `DEPRECATE`, and `VERBOSE` for finer-grained logging.
- **Logger Configuration**: Supports configuration from files (e.g., `logging.toml`), environment variables, or default settings.
- **Logger Extensions**: Provides a `Logger` class with enhanced methods for logging, including context-aware logging and deduplication of messages.
- **Integration with Modules**: Automatically injects the custom logger into modules, ensuring consistent logging behavior across the application.

## Introspection and Reflection Utilities

### Overview

Offers a collection of utility functions and classes for introspection, type checking, and reflection. It includes functions to analyze objects, their types, inheritance hierarchies, and modules.

### Key Features

- **Type Checking Functions**: Utilities like `is_callable`, `is_collection`, and `is_iterable` for checking object types.
- **Inheritance Utilities**: Functions to iterate over an object's MRO, get attributes from superclasses, and analyze class hierarchies.
- **Module and Object Inspection**: Tools to get the module of an object, its fully qualified name, source file, and other metadata.
- **Stack Inspection**: Functions to analyze the call stack, filter stack traces, and determine stack frame offsets.

## Dynamic Importing Tools

### Overview

Provides utilities for dynamic importing of modules and objects, with support for caching, handling optional dependencies, and enhanced error reporting.

### Key Features

- **Dynamic Importing**: Functions like `import_object` to import modules or objects by name at runtime.
- **Caching Imports**: `cached_import` function to memoize imports and improve performance.
- **Optional Dependencies**: `optional` function to handle optional imports gracefully, returning `None` or a default value if the module is not available.
- **Error Handling**: Detailed logging and error messages to aid in debugging import issues, including suggestions for missing packages.

## Advanced Property Descriptors

### Overview

Provides advanced property descriptors for Python classes, allowing the creation of instance, class, and mixed properties with optional caching capabilities. It includes decorators and base classes to facilitate the definition of properties that can behave differently depending on access context.

### Key Features

- **Custom Property Decorators**: Decorators like `@prop` and `@pin` to define properties with custom behaviors.
- **Caching Support**: Ability to cache property results, optimizing performance for expensive computations.
- **Context-Aware Properties**: Properties that can differentiate between being accessed from an instance or a class.
- **Async Support**: Supports both synchronous and asynchronous property methods.

## Data Class Extensions and Configuration Handling

### Overview

Extends the standard `dataclass` module with additional features such as validation, serialization, dynamic class creation, and integration with custom logging mechanisms.

### Key Features

- **Custom Data Classes**: Enhanced `dataclass` decorator that supports extra parameters, memoization, and custom initialization.
- **Validation**: Automatic validation of field types and default values against the defined schema.
- **Serialization Methods**: Methods like `as_dict`, `as_json`, and `as_sql` for converting instances to different formats.
- **Dynamic Class Creation**: Utilities like `autoclass` and `simple` to generate classes dynamically based on configuration schemas.
- **Operator Overloading**: Overloaded operators (`&`, `|`, `^`, `-`, `+`) for combining and comparing data class instances.

## Serialization and Deserialization Utilities

### Overview

Provides advanced serialization and deserialization utilities, supporting multiple serialization backends, compression algorithms, and encoding schemes. It allows custom serialization of complex objects, automatic detection of serialization formats, and flexible data encoding and decoding options.

### Key Features

- **Multiple Backends**: Supports serialization backends like `orjson` and standard `json`, with automatic selection.
- **Custom Serialization**: Ability to register custom serialization functions for specific classes.
- **Compression Support**: Utilizes compression libraries like `zstd` or `gzip` to compress serialized data.
- **Flexible Encoding**: Supports multiple encoding schemes such as Base16, Base32, Base64, Base85, and Base2048.
- **Automatic Backend Detection**: Deserialization functions automatically detect the serialization backend used.
- **Error Handling**: Robust exception handling and context-aware suppression of errors.

# Tasks

## lint

Requires: venv, update

Runs all defined pre-commit hooks.

```bash
.venv/bin/pre-commit run --config ci/.pre-commit-config.yaml --color always --all
```

## force-update

Run: once
Requires: venv

Update all pre-commit hook versions to latest releases.

```bash

    .venv/bin/pre-commit autoupdate --config ci/.pre-commit-config.yaml --color always

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
    changes="$(git ls-files --deleted --modified --exclude-standard)"
    changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

    if [[ "$uncommited" =~ "\bci/\.pre-commit-config\.yaml\b" ]] || [[ "$changes" =~ "\bci/\.pre-commit-config\.yaml\b" ]]; then
        xc add-precommit
    fi
```

## publish

Run: once
Requires: venv, update

Input: mode
Environment: mode=patch

Bumps project new version, build and publish the package to repository.

```bash

xc bump "$mode"

.venv/bin/poetry build
.venv/bin/poetry publish

```

## clean

Run: once

Clean up the project working directory: remove build/, .venv/, and .ruff_cache/ directories, as well as all .pyc files and __pycache__ directories.

```bash

    rm -rf build/ || true
    rm -rf .ruff_cache/ || true

    find . -name "*.pyc" -delete || true
    find . -name "__pycache__" -type d -exec rm -rf {} + || true
```

## clean-all

Run: once

Clean up the project working directory: remove build/, .venv/, and .ruff_cache/ directories, as well as all .pyc files and __pycache__ directories.

```bash

    xc clean
    rm log/* || true
    rm -rf .venv/ || true
```

## venv

Run: once

Make virtualenv for project build & test tools, install pre-push hook.

```bash

    if [ ! -d ".venv" ]; then
        virtualenv --python python3.11 ".venv"
        .venv/bin/python -m pip install --upgrade pip
        .venv/bin/python -m pip install --upgrade \
            pipdeptree \
            poetry \
            pre-commit \
            tomli tomli_w

        .venv/bin/poetry config virtualenvs.create false
        .venv/bin/poetry install || .venv/bin/poetry update

        .venv/bin/pre-commit install \
            --config ci/.pre-commit-config.yaml \
            --color always \
            --hook-type pre-push \
            --install-hooks \
            --overwrite
    else
        [ -f ".venv/bin/activate" ]

    fi
```

## update

Run: once

Autoupdate pre-commit hooks if the last update was more than 7 days ago.

```bash

    ctime="$(date +%s)"
    mtime="$(git log -1 --format=%ct ci/.pre-commit-config.yaml)"

    result=$(((7*86400) - (ctime - mtime)))

    if [ "$result" -le 0 ]; then
        xc force-update
    fi
```

## bump

Run: once
Requires: venv

Inputs: mode
Environment: mode=patch

Prepare and commit a version update in a Git repository. Checks for uncommitted changes, ensures the current branch is master, verifies if there are any changes since the last tag, and bumps the version number.

After validating the readiness for an update, it prompts to proceed. Once confirmed, the script updates the pyproject.toml and .pre-commit-config.yaml files if necessary, commits the changes, tags the new version, and pushes the updates to the remote repository.

```bash
#!/bin/zsh

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
    if [ -n "$uncommited" ]; then
        echo "uncommited changes found"
        exit 1
    fi

    #

    branch="$(git rev-parse --quiet --abbrev-ref HEAD 2>/dev/null)"
    if [ -z "$branch" ]; then
        exit 1
    elif [ "$branch" == "master" ]; then
        echo "using main master mode"
    else
        exit 1
    fi

    #

    changes="$(git ls-files --deleted --modified --exclude-standard)"
    changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

    if [ "$changes" == "README.md" ]; then
        echo "pipeline development mode"
    elif [ -n "$changes" ]; then
        echo "uncommited changes found"
        exit 1
    fi

    git fetch --tags --force
    current="$(git describe --tags --abbrev=0)" || retval="$?"
    if [ "$retval" -eq 128 ]; then
        current="0.0.0"
    elif [ "$retval" -gt 0 ]; then
        echo "something goes wrong on last used git tag fetch"
        exit "$retval"
    fi
    [ -z "$current" ] && exit 1

    if [ "$current" = '0.0.0' ]; then
        amount="1"
    else
        amount="$(git rev-list --count $current..HEAD)"
    fi

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"

    if [ "$amount" -eq 0 ] && [ -z "$uncommited" ]; then
        echo "no changes since $current"
        exit 1
    fi

    version="$(bump "$mode" "$current")"
    [ -z "$version" ] && exit 1

    revision="$(git rev-parse "$version" 2>/dev/null)" || retval="$?"

    if [ "$retval" -eq 128 ]; then
        echo "future tag $revision not found, continue"

    elif [ -z "$retval" ] && [ -n "$revision" ]; then

        echo "future tag $version already set to commit $revision, sync with remote branch!"
        exit 1

    else
        echo "something went wrong, version: '$version' revision: '$revision', retval: '$retval'"
        exit 2
    fi

    # non destructive stop here

    if [ -d "tests/" ]; then
        xc test
    fi

    xc lint
    git-restore-mtime --skip-missing || echo "datetime restoration failed, return: $?, skip"
    ls -la
    echo "we ready for bump $current -> $version, press ENTER twice to proceed or ESC+ENTER to exit"

    counter=0
    while : ; do
        read -r key

        if [[ $key == $'\e' ]]; then
            exit 1

        elif [ -z "$key" ]; then
            counter=$((counter + 1))
            if [ "$counter" -eq 2 ]; then
                break
            fi
        fi
    done

    # actions starts here

    xc add-precommit

    xc update-pyproject "$current" "$version"
    xc add-pyproject

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
    if [ -n "$uncommited" ]; then
        git commit -m "$branch: $version"
    fi

    git tag -a "$version" -m "$version"
    git push --tags
    git push origin "$branch"

    echo "version updated to $version"
```

## add-precommit

Requires: venv

Check and format ci/.pre-commit-config.yaml. If any changes are made, it stages the file for the next commit.

```bash

    file="ci/.pre-commit-config.yaml"

    .venv/bin/pre-commit run check-yaml --config "$file" --color always --file "$file" || value="$?"

    while true; do
        value="0"
        .venv/bin/pre-commit run yamlfix --config "$file" --color always --file "$file" || value="$?"

        if [ "$value" -eq 0 ]; then
            break

        elif [ "$value" -eq 1 ]; then
            continue

        else
            exit "$value"

        fi
    done

    uncommited="$(git diff --cached --name-only | sort -u | tr '\n' ' ' | xargs)"
    changes="$(git ls-files --deleted --modified --exclude-standard)"
    changes="$(printf "$changes" | sort -u | tr '\n' ' ' | xargs)"

    if [[ "$uncommited" =~ "\bci/\.pre-commit-config\.yaml\b" ]] || [[ "$changes" =~ "\bci/\.pre-commit-config\.yaml\b" ]]; then
        git add "$file"
        git commit -m "(ci/cd): autoupdate pre-commit"
    fi
```

## add-pyproject

Requires: venv

Check and format pyproject.toml. If any changes are made, it stages the file for the next commit.

```bash

    file="pyproject.toml"

    .venv/bin/pre-commit run check-toml --config ci/.pre-commit-config.yaml --color always --file "$file" || value="$?"

    while true; do
        value="0"
        .venv/bin/pre-commit run pretty-format-toml --config ci/.pre-commit-config.yaml --color always --file "$file" || value="$?"

        if [ "$value" -eq 0 ]; then
            break

        elif [ "$value" -eq 1 ]; then
            continue

        else
            exit "$value"

        fi
    done

    changes="$(git diff "$file")" || exit "$?"
    changes="$(printf "$changes" | wc -l)"
    if [ "$changes" -ne 0 ]; then
        git add "$file"
    fi
```

## update-pyproject

Run: once
Requires: venv

Update version in pyproject.toml file based on provided old and new version tags. It validates the version format and ensures the current tag matches the project's version before writing the new version.

```python
#!.venv/bin/python
from os import environ
from sys import argv, exit
from re import match
from pathlib import Path

import tomli_w
import tomllib

ROOT = Path(environ['PWD'])

def get_version(string):
    try:
        return match(r'^(\d+\.\d+\.\d+)$', string).group(1)
    except Exception:
        print(f'could not parse version from {string}')
        exit(3)

if __name__ == '__main__':
    try:
        current_tag = get_version(argv[1])
        version_tag = get_version(argv[2])
    except IndexError:
        print('usage: xc update-pyproject <old_tag> <new_tag>')
        exit(1)

    path = ROOT / 'pyproject.toml'
    try:
        with open(path, 'rb') as fd:
            data = tomllib.load(fd)

    except Exception:
        print(f'could not load {path}')
        exit(2)

    try:
        current_ver = get_version(data['tool']['poetry']['version'])
        print(f'project version: {current_ver}')

    except KeyError:
        print(f'could not find version in {data}')
        exit(2)

    if current_tag != current_ver:
        if current_ver == version_tag:
            print(f'current version {current_ver} == {version_tag}, no update needed')
            exit(0)

        print(f'current tag {current_tag} != {current_ver} current version')
        exit(4)

    data['tool']['poetry']['version'] = version_tag

    try:
        with open(path, 'wb') as fd:
            tomli_w.dump(data, fd)

        print(f'project version -> {version_tag}')

    except Exception:
        print(f'could not write {path} with {data=}')
        exit(5)
```

## test

Run: once
Requires: venv

```bash

    .venv/bin/poetry run pytest -svx
```
