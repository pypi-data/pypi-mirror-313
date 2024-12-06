import yaml
from fakts_next.protocols import FaktValue
from typing import Dict
from pydantic import BaseModel, ConfigDict
from fakts_next.grants.base import BaseFaktsGrant


class YamlGrant(BaseFaktsGrant):
    """
    Represent a Grant that loads configuration from a YAML file.

    Attributes
    ----------
    filepath : str
        The path of the YAML file.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    filepath: str

    async def aload(self) -> Dict[str, FaktValue]:
        """Loads the YAML file and returns the configuration."""
        with open(self.filepath, "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)  # type: ignore #TODO: Check why this is not working

        return config
