
[![Coverage Status](https://coveralls.io/repos/github/jzombie/rich-cms/badge.svg)](https://coveralls.io/github/jzombie/rich-cms)

# Rich-CMS

A hacky, prototype, Markdown-driven CMS, written in Python.

Note: This branch serves as a repository for thoughts, ideas, and preliminary versions of the CMS. It's not meant for distributing the final source code, although it's deliberately kept public. Be aware that this branch could undergo significant updates, including force-pushes, to disseminate intended changes.

Preview: https://zenosmosis.com

More to come...

## Serve (for development debugging)

```bash
cd docs
python3 -m http.server
```

## Coverage

```bash
coverage run -m unittest discover -s test
coverage report
```
