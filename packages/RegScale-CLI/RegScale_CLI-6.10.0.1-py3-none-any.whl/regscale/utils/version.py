"""Version utility functions"""

import logging
import re
from typing import Optional

from packaging.version import Version

from regscale.core.app.utils.api_handler import APIHandler
from regscale.utils.decorators import classproperty

logger = logging.getLogger(__name__)


class RegscaleVersion:
    """Regscale version utility class"""

    def __init__(self):
        self._regscale_version = None

    @classproperty
    def regscale_version(cls) -> str:
        """Fetch the platform version.

        :return: Platform version
        """
        cls._regscale_version = cls.get_platform_version()
        return cls._regscale_version

    @staticmethod
    def get_platform_version() -> str:
        """Fetch the platform version using the provided API handler.

        :param APIHandler api_handler: API handler
        """
        logger.debug("Fetching platform version using API handler")
        try:
            api_handler = APIHandler()
            response = api_handler.get("/assets/json/version.json")
            if response.status_code == 200:
                version_data = response.json()
                return version_data.get("version", "Unknown")
            else:
                logger.error(f"Failed to fetch version. Status code: {response.status_code}")
                return "dev"
        except Exception as e:
            logger.error(f"Error fetching version: {e}", exc_info=True)
            return "dev"

    @classmethod
    def compare_versions(cls, greater: str, lesser: Optional[str] = None) -> bool:
        """
        Compare two versions. Return True if version1 is greater than version2, False otherwise.

        :param str greater: Version 1 to compare with the platform version i.e. "1.0.0"
        :param str lesser: Version 2 to compare with the platform version i.e. "1.0.0"
        :return: Comparison result
        :rtype: bool
        """
        special_versions = {"dev": "9999.9999.9999", "localdev": "9998.9998.9998", "Unknown": "0.0.0"}
        if not lesser:
            lesser = cls.get_platform_version()
        lesser = special_versions.get(lesser, lesser)
        greater = special_versions.get(greater, greater)
        if not re.match(r"^\d+\.\d+(\.\d+)?$", lesser):
            logger.info(f"Invalid lesser version {lesser}, assuming dev")
            return True
        logger.debug(f"Comparing versions: {Version(greater)} >= {Version(lesser)}")
        return Version(greater) >= Version(lesser)
