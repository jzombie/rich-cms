# Avoid Python Dependency Hell When Creating New Packages

## Example Scenario: Using Pydantic as a dependency in a package

When developing a Python package that depends on Pydantic, or any other library, and aiming to minimize dependency issues for users, there are several best practices you can follow to reduce the likelihood of creating or exacerbating dependency conflicts. Here’s a comprehensive guide:

### 1. **Specify Dependency Versions Carefully**

Use version specifiers to manage dependencies in a way that balances the need for specific functionality and stability with the flexibility required by other packages that might use yours. A few common strategies are:

- **Pinning Specific Versions**: Avoid unless necessary, as it forces users into specific versions, potentially causing conflicts.
  
- **Compatible Release**: Use the tilde operator (`~=`) to specify compatible releases. For example, `pydantic~=1.8` will allow any version >=1.8.0 and <2.0.0. This ensures you get bug fixes and minor updates without breaking backward compatibility.

- **Minimum Version**: Specify a minimum version that you know supports all the features your package needs, for example, `pydantic>=1.8`. This allows greater flexibility but risks future backward compatibility breaks.

- **Maximum Version**: Sometimes, especially when aware of upcoming changes that might break your package, specifying a maximum version can be useful. Combine this with a minimum version like `pydantic>=1.8,<2.0`.

Here’s how you might specify these in your `setup.py` or `pyproject.toml`:

```python
# setup.py example
install_requires=[
    'pydantic>=1.8,<2.0'
]
```

```toml
# pyproject.toml example
[tool.poetry.dependencies]
pydantic = "^1.8"
```

### 2. **Regularly Update Your Dependencies**

- **Stay Updated**: Keep track of new releases of your dependencies. Update the versions you rely on after testing to ensure they don't break your package. This can help you catch and fix compatibility issues early.

- **Use Dependency Bots**: Tools like Dependabot can automatically create pull requests to update dependencies in your project, helping you keep your package up-to-date.

### 3. **Testing Against Multiple Dependency Versions**

- **Test Matrix**: Use CI/CD tools like GitHub Actions, GitLab CI, or Travis CI to test your package against multiple versions of its dependencies. This helps ensure that your package works as expected across the range of allowed versions.

- **tox**: Use `tox` to automate testing across multiple environments and dependency versions.

Here’s an example `tox.ini` configuration that tests multiple Pydantic versions:

```ini
[tox]
envlist = py{36,37,38,39}-pydantic{1.8,1.9}

[testenv]
deps =
    pydantic1.8: pydantic>=1.8,<1.9
    pydantic1.9: pydantic>=1.9,<2.0
commands =
    pytest tests/
```

### 4. **Documentation**

- **Guidelines**: Provide clear documentation on how to install and configure your package, including notes about compatibility with common dependency versions.

- **Changelog**: Maintain a changelog to help users understand what changes have been made in each version, especially changes related to dependencies.

### 5. **Isolate Your Package Environment**

- **Virtual Environments**: Recommend that end users install your package within a virtual environment to avoid interfering with system-wide packages.

### 6. **Provide an Escape Hatch**

- **Extras**: Allow users to opt out of installing certain dependencies if they conflict with other packages. This can be managed with optional dependencies.

Using these strategies, you can help minimize dependency conflicts and provide a more robust and user-friendly Python package.
