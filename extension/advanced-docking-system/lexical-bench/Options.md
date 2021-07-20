# Tests

- Need to fix:
    - FFI tests
        - Rust bindings ✔
        - Python bindings ✔
        - C bindings
        - C++ bindings
    - Travis CI integrations

# Rework the Options API

# Simplify Trait Bounds
- Remove some hard-coded, 64-bit logic afterwards
    - **TEST IT**

# Simplify API macros
- from_lexical, from_lexical_with_options
- to_lexical, to_lexical_with_options
    - Should be able to take a single function, and repeat types
