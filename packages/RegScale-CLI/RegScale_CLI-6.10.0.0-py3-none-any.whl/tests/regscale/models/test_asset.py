import pytest

from tests import CLITestFixture
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import Search
from regscale.models.regscale_models.asset import Asset


class TestAssets(CLITestFixture):
    bad_ssp_id = 10000
    good_ssp_id = 3
    regscale_module = "securityplans"

    # Can we create an instance of the Asset class?
    @staticmethod
    def test_asset_instance():
        asset = Asset(
            host_name="host.example.com",
            name="Host Name",
            type="Other",
            ipAddress="1.1.1.1",
            parentId=1,
            parentModule="securityplans",
            assetOwnerId="asdfasdf",
            status="Active (On Network)",
            assetType="Virtual Machine (VM)",
            dateCreated=get_current_datetime(),
            dateLastUpdated=get_current_datetime(),
            createdById="asdfasdf",
            lastUpdatedById="asdfasdf",
            assetCategory="Hardware",
            scanningTool="Rando Scanner",
            isPublic=True,
            tenantsId=0,
        )
        assert isinstance(asset, Asset)

    @staticmethod
    def test_bad_asset():
        asset = Asset(
            host_name="host.example.com",
            name="Host Name",
            type="Other",
            ipAddress="1.1.1.1",
            parentId=1,
            parentModule="securityplans",
            assetOwnerId="asdfasdf",
            status="Active (On Network)",
            assetType="Virtual Machine (VM)",
            dateCreated=get_current_datetime(),
            dateLastUpdated=get_current_datetime(),
            createdById="asdfasdf",
            lastUpdatedById="asdfasdf",
            assetCategory="Hardware",
            scanningTool="Rando Scanner",
            isPublic=True,
            tenantsId=0,
            fqdn=0,  # Bad attribute
        )
        # Check if an attribute error is raised
        with pytest.raises(AttributeError):
            asset.model_fields_set

    def test_assets_by_search(self):
        empty_search = Search(parentID=self.bad_ssp_id, module=self.regscale_module, sort="id")
        search = Search(parentID=self.good_ssp_id, module=self.regscale_module, sort="id")
        # this will return an empty list
        no_assets = Asset.get_all_by_search(empty_search)
        assets = Asset.get_all_by_search(search)
        assert no_assets == []
        assert len(assets) > 0
