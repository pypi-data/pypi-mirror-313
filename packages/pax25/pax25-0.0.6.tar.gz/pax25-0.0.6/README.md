# PAX25

pax25 is intended to be a full AX.25 stack with:

AX.25 V2 stack (not 2.2; no MOD128, no SREJ, no XID)
Multiple physical interfaces (KISS, AXIP) support

Target Python is 3.13. Earlier versions of the 3.X branch will not work, but later versions will likely work.

At present, only the application layer is working, with files as input and output. Support for real-world networking is incoming.

## Documentation

[Documentation for Pax25](https://foxyfoxie.gitlab.io/pax25/) is built and published based on the contents of the `documentation` directory. It is based on [mkdocs](https://www.mkdocs.org/), the configuration for which is found in the repository root.
