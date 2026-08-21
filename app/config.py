"""
PACT Configuration Module.
Loads environment settings with sensible defaults for 24-hr hackathon resilience.
Automatically loads key-value pairs from .env if present.
"""

import os
from pathlib import Path


def load_dotenv():
    """Simple built-in .env file loader without external dependencies."""
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k = k.strip()
                v = v.strip().strip("'\"")
                if k and k not in os.environ:
                    os.environ[k] = v


load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DATABASE_NAME: str = os.getenv("DATABASE_NAME", "pact_db")

# Autopilot settings
AUTOPILOT_ENABLED: bool = os.getenv("AUTOPILOT_ENABLED", "true").lower() in ("true", "1", "yes")
AUTOPILOT_TIMEOUT_SECONDS: float = float(os.getenv("AUTOPILOT_TIMEOUT_SECONDS", "3.0"))

# Network & Server
HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "8000"))
DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
