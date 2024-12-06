import os

TRUSS_DEVELOPMENT_MODE = os.environ.get("TRUSS_DEVELOPMENT_MODE", "false").lower() == "true"
