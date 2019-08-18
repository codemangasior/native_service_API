import os
import django
import pytest

os.environ["DJANGO_SETTINGS_MODULE"] = "Native_Service.test_settings"


if __name__ == "__main__":
    django.setup()
    pytest.main()
