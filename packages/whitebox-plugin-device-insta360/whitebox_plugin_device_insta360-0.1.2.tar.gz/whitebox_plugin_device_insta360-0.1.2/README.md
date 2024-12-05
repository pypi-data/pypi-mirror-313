# Whitebox Plugin - Insta360 Camera Support

This is a plugin for [whitebox](https://gitlab.com/whitebox-aero) that enables support for Insta360 cameras
using the [insta360 library](https://gitlab.com/whitebox-aero/insta360).

## Installation

Simply install the plugin to whitebox:

```
poetry add whitebox-plugin-device-insta360
```

## Adding Plugin to Whitebox Locally (For Development)

1. Set up whitebox locally.
2. Clone this repository.
3. Add plugin to whitebox using the following command: `poetry add -e path/to/plugin.`
4. Run the whitebox server.

## Running Plugin Tests Locally

1. Ensure you have the plugin installed in whitebox like mentioned above.
2. Run the tests: `make test`.

## Contribution Guidelines

1. Write tests for each new feature.
2. Ensure coverage is 90% or more.
3. [Google style docstrings](https://mkdocstrings.github.io/griffe/docstrings/#google-style)
   should be used for all functions and classes.
