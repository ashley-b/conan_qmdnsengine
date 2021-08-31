# Conan qmdnsengine recipe

## Description

Simple Conan recipe for https://www.github.com/nitroshare/qmdnsengine

This library provides an implementation of multicast DNS as per RFC 6762.

## Useage

Example conanfile.txt for consumers
```
[requires]
qmdnsengine/0.2.0

[generators]
CMakeDeps
CMakeToolchain
```
