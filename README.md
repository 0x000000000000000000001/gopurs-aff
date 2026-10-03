# Aff

## Local Go development

This checkout is part of the gopurs library family. Use the
[local Go development guide](../gopurs/README.md#develop-one-library-locally)
for toolchain setup, sibling dependencies, Spago configuration and Go commands.
The existing npm, Bower and Dhall commands below retain their JavaScript or
upstream roles.

### Run the same tests with Rust

With the sibling `../../purust/purust` compiler and `../../purust/purust-*`
library ports installed:

```sh
GOPURS_RUST=1 ./bin/test
```

This builds this checkout's TAST, adapts the Rust FFI from the Purust libraries,
generates concurrent Rust with the installed native Purust compiler, then builds
and runs `Test.Main` with Cargo. It checks all 45 Aff messages and runs the AVar
stress test. The Go and Rust backends use the same PureScript test sources;
cancellation tests explicitly wait for resource acquisition before killing.

```sh
./bin/test                           # Native Go compiler → Go application
GOPURS_JS=1 ./bin/test               # JavaScript gopurs → Go application
GOPURS_RUST=1 ./bin/test             # Native Rust compiler → Rust application
GOPURS_RUST=1 PURUST_JS=1 ./bin/test  # JavaScript Purust → Rust application
```

Add `-c` to rebuild the selected compiler. `PURUST_DIR` can select another Purust
checkout, and `PURS` selects the TAST-enabled PureScript frontend. Cargo's target
cache is kept in `.cache/purust-target` between Rust runs; `CARGO_TARGET_DIR` can
override it. Application stdout/stderr are retained in `output/rust-test.*`.
The `[purust] backend total` line measures Rust generation; the full command also
includes the frontend, Cargo and test execution.

The FFI overlay is generated from current library sources, with provenance in
`output/rust-ffi/manifest.json`. `Control.Extend`, `Data.Int.Bits` and
`Performance.Minibench` are present in the dependency closure but unused by this
suite; their unported Rust entry points fail explicitly if a new test calls them.


[![CI](https://github.com/purescript-contrib/purescript-aff/workflows/CI/badge.svg?branch=main)](https://github.com/purescript-contrib/purescript-aff/actions?query=workflow%3ACI+branch%3Amain)
[![Release](https://img.shields.io/github/release/purescript-contrib/purescript-aff.svg)](https://github.com/purescript-contrib/purescript-aff/releases)
[![Pursuit](https://pursuit.purescript.org/packages/purescript-aff/badge)](https://pursuit.purescript.org/packages/purescript-aff)
[![Maintainer: natefaubion](https://img.shields.io/badge/maintainer-natefaubion-teal.svg)](https://github.com/natefaubion)

An asynchronous effect monad and threading model for PureScript.

## Installation

Install `aff` with [Spago](https://github.com/purescript/spago):

```sh
spago install aff
```

## Quick start

This quick start covers common, minimal use cases for the library. Longer examples and tutorials can be found in the [docs directory](./docs).

```purescript
main :: Effect Unit
main = launchAff_ do
  response <- Ajax.get "http://foo.bar"
  log response.body
```

## Documentation

`aff` documentation is stored in a few places:

1. Module documentation is [published on Pursuit](https://pursuit.purescript.org/packages/purescript-aff).
2. Written documentation is kept in the [docs directory](./docs).
3. Usage examples can be found in [the test suite](./test).

If you get stuck, there are several ways to get help:

- [Open an issue](https://github.com/purescript-contrib/purescript-aff/issues) if you have encountered a bug or problem.
- Ask general questions on the [PureScript Discourse](https://discourse.purescript.org) forum or the [PureScript Discord](https://purescript.org/chat) chat.

## Contributing

You can contribute to `aff` in several ways:

1. If you encounter a problem or have a question, please [open an issue](https://github.com/purescript-contrib/purescript-aff/issues). We'll do our best to work with you to resolve or answer it.

2. If you would like to contribute code, tests, or documentation, please [read the contributor guide](./CONTRIBUTING.md). It's a short, helpful introduction to contributing to this library, including development instructions.

3. If you have written a library, tutorial, guide, or other resource based on this package, please share it on the [PureScript Discourse](https://discourse.purescript.org)! Writing libraries and learning resources are a great way to help this library succeed.
