# Aff

## Local Go development

This checkout is part of the gopurs library family. Use the
[local Go development guide](../gopurs/README.md#develop-one-library-locally)
for toolchain setup, sibling dependencies, Spago configuration and Go commands.
The existing npm, Bower and Dhall commands below retain their JavaScript or
upstream roles.

### Select the compiler host

The same gopurs compiler can run as native Go, JavaScript or native Rust. Every
mode generates Go from this checkout's TAST, then builds and runs the same Go
application. The runner checks all 45 Aff messages and runs the 1,000-item AVar
stress test. Cancellation tests explicitly wait for resource acquisition before
killing.

```sh
./bin/test                 # gopurs compiled in Go → Go application
GOPURS_JS=1 ./bin/test     # gopurs compiled in JavaScript → Go application
GOPURS_RUST=1 ./bin/test   # gopurs compiled in Rust → Go application
```

Build the Rust-hosted compiler once with `npm run build:rust` in `../gopurs`, or
use `GOPURS_RUST=1 ./bin/test -c`. Its bootstrap requires Cargo, the sibling
`../../purust/purust` compiler and the `../../purust/purust-*` library ports.
`PURUST_DIR` selects another Purust checkout; `PURUST_JS=1` selects its JavaScript
executable **only when bootstrapping gopurs**. The resulting `gopurs-rust`
executable runs directly and embeds the Go FFI parser.

Add `-c` to rebuild the selected gopurs compiler. `GOPURS_PURS` selects the typed
frontend used for bootstrap; `PURS` selects it for this project's Spago build.
Application stdout/stderr are retained in `output/test.*`.
The `[gopurs] backend total` line measures Go generation in all three modes; the
full command also includes the frontend, Go build and test execution.

On machines with at least 32 GiB of RAM, the launcher selects eight preparation
and PBO workers for all three hosts, including `GOPURS_RUST=1 ./bin/test`.
`GOPURS_PREPARE_JOBS` and `GOPURS_PBO_JOBS` override these choices explicitly.
The initial `[gopurs] workers:` line shows the effective limits and pipeline state.


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
