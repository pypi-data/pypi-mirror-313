"""OpenAPI CLI configuration management.

This module provides a class for managing OpenAPI CLI configuration,
including adding, updating, and removing API aliases.
"""

import json
from pathlib import Path


class Config:
    """OpenAPI CLI configuration manager."""

    def __init__(self):
        """Initialize the configuration manager."""
        self.config_dir = Path.home() / ".openapi_cli_generator"
        self.config_file = self.config_dir / "config.json"
        self._ensure_config_exists()
        self.load_config()

    def _ensure_config_exists(self):
        """Ensure config directory and file exist."""
        self.config_dir.mkdir(exist_ok=True)
        if not self.config_file.exists():
            self.config_file.write_text("{}")

    def load_config(self):
        """Load configuration from file."""
        with open(self.config_file) as f:
            self.config = json.load(f)

    def save_config(self):
        """Save configuration to file."""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=2)

    def add_alias(self, name, url):
        """Add a new API alias."""
        if "aliases" not in self.config:
            self.config["aliases"] = {}
        if name in self.config["aliases"]:
            raise ValueError(
                f"Alias '{name}' already exists. Use update_alias to modify it."
            )
        self.config["aliases"][name] = url
        self.save_config()

    def get_alias(self, name):
        """Get URL for an alias."""
        if "aliases" not in self.config or name not in self.config["aliases"]:
            raise KeyError(f"Alias '{name}' not found")
        return self.config["aliases"][name]

    def list_aliases(self):
        """List all available aliases."""
        return self.config.get("aliases", {})

    def remove_alias(self, name):
        """Remove an API alias."""
        if "aliases" not in self.config or name not in self.config["aliases"]:
            raise KeyError(f"Alias '{name}' not found")
        del self.config["aliases"][name]
        self.save_config()

    def update_alias(self, name, url):
        """Update an existing API alias."""
        if "aliases" not in self.config or name not in self.config["aliases"]:
            raise KeyError(f"Alias '{name}' not found")
        self.config["aliases"][name] = url
        self.save_config()
