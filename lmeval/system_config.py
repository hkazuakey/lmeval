"""System dependent configuration."""

import immutabledict

CONFIG = immutabledict.immutabledict({
    "platform": "local",  # "google" or "local"
    "use_tempfile": False,
})