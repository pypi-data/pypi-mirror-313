"""Base test class for Bjarkan SDK tests."""
import pytest


class TestBase:
    """Base test class with common utilities."""

    @pytest.fixture(autouse=True)
    async def setup(self, sdk):
        """Setup test environment."""
        self.sdk = sdk
        yield
        await self.sdk.close()

    async def assert_success_response(self, response):
        """Assert that a response indicates success."""
        assert isinstance(response, dict)
        assert response.get("status") == "success"
