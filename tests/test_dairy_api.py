import skill.dairy_api as dairy_api
import pytest
import requests_mock

class TestDiaryAPI:
    def test_get_url(self):
        assert dairy_api.base_url()

