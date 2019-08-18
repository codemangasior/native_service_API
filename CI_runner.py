import os
import django
import pytest

os.environ["DJANGO_SETTINGS_MODULE"] = "native_service_API.settings.py"


if __name__ == "__main__":
    django.setup()
    pytest.main()
