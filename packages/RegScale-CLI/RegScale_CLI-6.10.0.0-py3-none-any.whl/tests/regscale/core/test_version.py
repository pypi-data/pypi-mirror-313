"""Tests for the version module."""

from unittest.mock import patch
import pytest
import logging
from regscale.utils.version import RegscaleVersion

logger = logging.getLogger(__name__)


def test_get_platform_version():
    """Test get_platform_version method."""
    version = RegscaleVersion.get_platform_version()
    logger.info(f"Version: {version}")
    assert version


@pytest.mark.parametrize(
    "version1, platform_version, expected",
    [
        ("1.0.0", "1.0.1", False),
        ("1.2.0", "1.0.1", True),
        ("dev", "1.0.1", True),
        ("1.0.0", "dev", False),
        ("dev", "dev", True),
        ("localdev", "1.0.1", True),
        ("1.0.0", "localdev", False),
        ("localdev", "localdev", True),
        ("Unknown", "1.0.1", False),
        ("1.0.0", "Unknown", True),
        ("Unknown", "Unknown", True),
    ],
)
@patch.object(RegscaleVersion, "get_platform_version")
def test_compare_versions(mock_get_platform_version, version1, platform_version, expected):
    """Test compare_versions method."""
    mock_get_platform_version.return_value = platform_version
    result = RegscaleVersion.compare_versions(version1)
    logger.info(f"Comparing versions: {version1} and {platform_version}")
    logger.info(f"Version 1 is greater than Version 2: {result}")

    assert result == expected
