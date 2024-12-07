# python-sdk
Python SDK for The Platform Specification

Provides the API types for The Platform Specification, for usage within Python and Pydantic v2.

Expects the CRD manifests within the `crd/` folder, which can be generated from the Platform Spec `go-sdk` project with `make manifests`.

Run `poetry install --with=dev && bin/generate` to generate the Python API.
