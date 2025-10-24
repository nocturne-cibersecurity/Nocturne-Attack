
---

### 2) `pyproject.toml`
```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "nocturne"
version = "0.1.0"
description = "Nocturne"
readme = "README.md"
license = {text = "MIT"}
authors = [{name="Rodrigo López", email="rodrigolopezpizarro271@gmail.com"}]
dependencies = [
  "requests>=2.28",
  "urllib3>=1.26",
  "stem>=1.8.0"
]

[project.scripts]
nocturne = "nocturne.cli:main"
