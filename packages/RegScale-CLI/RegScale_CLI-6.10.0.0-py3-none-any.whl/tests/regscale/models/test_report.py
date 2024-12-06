import pytest

from regscale.core.app.utils.report_utils import ReportGenerator
from regscale.models import Asset
from tests.models.test_fixture import CLITestFixture


class TestImport(CLITestFixture):
    """
    Test for Report Generator
    """

    def test_basic_report(self):
        """
        Test the basic report
        """
        assets = Asset.get_all_by_parent(3, "securityplans")
        ReportGenerator(assets)

    def test_advanced_report(self):
        """
        Test the advanced report
        """
        assets = Asset.get_all_by_parent(3, "securityplans")
        ReportGenerator(objects=assets, to_file=True, report_name="test_report")

    def test_save_to_regscale(self):
        """
        Test saving the report to Regscale
        """
        assets = Asset.get_all_by_parent(3, "securityplans")
        ReportGenerator(
            objects=assets, to_file=True, report_name="test_report", regscale_id=3, regscale_module="securityplans"
        )
