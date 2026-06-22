import os
import pytest
from dotenv import load_dotenv
from tools.api_helper import APIHelper

# Load sensitive data from the local .env file
load_dotenv()


@pytest.fixture(scope="session")
def user_id():
    return os.getenv("X_USER_ID")

@pytest.fixture()
def api_helper(user_id):
    yield APIHelper(x_user_id=user_id)