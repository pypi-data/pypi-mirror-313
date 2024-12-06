"""Facility model for RegScale."""

import warnings
from typing import Optional
from urllib.parse import urljoin

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.models.regscale_models.regscale_model import RegScaleModel


class Facility(RegScaleModel):
    """Data Model for Facilities"""

    _module_slug = "facilities"

    id: int = 0
    name: str = ""
    description: str = ""
    address: str = ""
    city: str = ""
    state: str = ""
    zipCode: str = ""
    status: str = ""
    latitude: float = 0
    longitude: float = 0
    createdBy: Optional[str] = None
    createdById: Optional[str] = None
    dateCreated: Optional[str] = None
    lastUpdatedBy: Optional[str] = None
    lastUpdatedById: Optional[str] = None
    isPublic: bool = True
    dateLastUpdated: Optional[str] = None

    def post(self, app: Application) -> Optional[dict]:
        """Post a Facility to RegScale

        :param Application app: The application instance
        :return: The response from the API or None
        :rtype: Optional[dict]
        """
        warnings.warn(
            "The 'post' method is deprecated, use 'create' method instead",
            DeprecationWarning,
        )
        api = Api()
        url = urljoin(app.config.get("domain", ""), "/api/facilities")
        data = self.dict()
        response = api.post(url, json=data)
        return response.json() if response.ok else None


class Facilities(Facility):
    def __init__(self, *args, **kwargs):
        warnings.warn(
            "The 'Facilities' class is deprecated, use 'Facility' instead",
            DeprecationWarning,
        )
        super().__init__(*args, **kwargs)
