import os

# Resolve absolute path to data/cache.db relative to this file's location,
# so it works correctly regardless of the working directory.
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))          # .../src/utils
DB_PATH = os.path.normpath(os.path.join(_BASE_DIR, "..", "..", "data", "cache.db"))

# Groq model — change here to update everywhere
MODEL = "openai/gpt-oss-120b"
