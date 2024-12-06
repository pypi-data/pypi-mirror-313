# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from common.geid.geid_client import GEIDClient


class TestGEIDClient:
    client = GEIDClient()

    def test_01_get_GEID(self):
        geid = self.client.get_GEID()
        assert isinstance(geid, str)
        assert len(geid) == 47

    def test_02_get_bulk_GEID(self):
        geids = self.client.get_GEID_bulk(5)
        assert isinstance(geids, list)
        assert len(geids) == 5
