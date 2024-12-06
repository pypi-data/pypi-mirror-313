import pytest
from ecos.api.client import EcosClient

def test_search_statistics():
    client = EcosClient()
    result = client.search_statistics("금리")
    assert result is not None
    assert len(result) > 0
    assert "금리" in str(result['STAT_NAME'].values) 