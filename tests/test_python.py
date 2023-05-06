import json
import os

import pytest

from joern_lib.detectors.python import expand_decorators


@pytest.fixture
def test_routes_data():
    return os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "data", "py-routes.json"
    )


def test_routes_parsing(test_routes_data):
    with open(test_routes_data) as fp:
        assert expand_decorators(json.load(fp))
