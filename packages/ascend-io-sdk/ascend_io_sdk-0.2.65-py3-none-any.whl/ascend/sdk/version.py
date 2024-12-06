import os
import toml

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "poetry/pyproject.toml")) as f:
  VERSION = toml.load(f)["tool"]["poetry"]["version"]
