from typing import TYPE_CHECKING

from regscale import __version__
from regscale.integrations.commercial.tenablev2.variables import TenableVariables

# Delay import of Tenable libraries
if TYPE_CHECKING:
    from tenable.io import TenableIO  # type: ignore

REGSCALE_INC = "RegScale, Inc."
REGSCALE_CLI = "RegScale CLI"


def gen_tio() -> "TenableIO":
    """
    Generate Tenable Object

    :return: Tenable client
    :rtype: "TenableIO"
    """

    from tenable.io import TenableIO

    return TenableIO(
        url=TenableVariables.tenableUrl,
        access_key=TenableVariables.tenableAccessKey,
        secret_key=TenableVariables.tenableSecretKey,
        vendor=REGSCALE_INC,
        product=REGSCALE_CLI,
        build=__version__,
    )
