import yaml
from pathlib import Path


class Config:
    def __init__(self, config_path: str = "config.yml"):
        self.config_path = Path(config_path)
        self.data = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}

    def get(self, key: str, default=None):
        """Get a configuration value using dot notation (e.g., 'Tickets.ticket_role_id')."""
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value

    def __getitem__(self, key: str):
        """Get a configuration value using bracket notation."""
        return self.get(key)


# Global config instance
config = Config()

# Usage examples:
# config.get('Tickets.ticket_role_id')  # Using dot notation with get()
# config['Tickets.ticket_role_id']      # Using bracket notation
# config.get('NonExistent.Key', 'default_value')  # With default fallback
