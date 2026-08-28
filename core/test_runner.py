"""Custom Django test runner configuration."""

from django.test.runner import DiscoverRunner

class TestProtocolClear(DiscoverRunner):
    """before each test, the test_protocol.log file is emptied."""

    def setup_test_environment(self, **kwargs):
        """Configures the test environment for test execution und empties the test_protocol.log file"""
        open("test_protocol.log", "w").close()

        super().setup_test_environment(**kwargs)