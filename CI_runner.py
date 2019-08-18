import os
import django
import pytest

os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.tests.lib.unit_tests.test_settings.py"


if __name__ == "__main__":
    django.setup()
    pytest.main()
