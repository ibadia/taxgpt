import tempfile
from pathlib import Path

import pytest
from django.test.utils import override_settings
from rest_framework.test import APIClient



@pytest.fixture(scope="session")
def celery_config():
    with override_settings(
        CELERY_TASK_EAGER_PROPAGATES=True,
        CELERY_TASK_ALWAYS_EAGER=True,
        BROKER_BACKEND="memory",
        CELERY_RESULT_BACKEND="cache+memory://",
    ):
        yield



@pytest.fixture(autouse=True)
def temp_file_storage_setting(settings):
    settings.MEDIA_ROOT = Path(tempfile.gettempdir())


@pytest.fixture(autouse=True)
def enable_db_access(db):
    """This method (fixture) will enable db access globally for all tests"""
    pass




@pytest.fixture
def secret_pwd():
    return "secret_pwd"


@pytest.fixture
def api_client():
    return APIClient()



