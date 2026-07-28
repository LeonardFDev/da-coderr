from django.test.runner import DiscoverRunner

class TestProtocolClear(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        open("test_protocol.log", "w").close()

        super().setup_test_environment(**kwargs)